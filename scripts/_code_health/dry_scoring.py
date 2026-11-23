"""Deterministic clone clustering, subsumption, and DRY scoring for Code Health."""

from __future__ import annotations

from dataclasses import dataclass, replace

from _code_health.dry_models import (
    CloneGroup,
    CloneLocation,
    DrySummary,
    FileDryMetrics,
    FileTokenStream,
    RawCloneMatch,
)
from _code_health.models import (
    DimensionScores,
    FileReport,
    RubricConfig,
    clamp_score,
)

_TYPE_RANK = {"type1": 0, "type2": 1, "type3": 2}
_TYPE_FROM_RANK = ("type1", "type2", "type3")
_TYPE_PENALTY = {"type1": 5.0, "type2": 4.0, "type3": 3.0}
_SUBSUMPTION_OVERLAP = 0.75
_SNAP_IOU = 0.80
_BIN_SIZE = 64


class _UnionFind:
    """Disjoint-set structure for transitive clone grouping."""

    def __init__(self) -> None:
        self._parent: list[int] = []

    def add(self) -> int:
        """Create and return a new singleton set node ID."""
        node = len(self._parent)
        self._parent.append(node)
        return node

    def find(self, x: int) -> int:
        """Return canonical representative for node x with path compression."""
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        while self._parent[x] != root:
            nxt = self._parent[x]
            self._parent[x] = root
            x = nxt
        return root

    def union(self, a: int, b: int) -> None:
        """Merge the sets containing a and b deterministically."""
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self._parent[max(ra, rb)] = min(ra, rb)


class _SnapIndex:
    """Spatial index that snaps >= 0.80 IoU overlapping intervals to one node."""

    def __init__(self) -> None:
        self.bins: dict[tuple[int, int], list[tuple[int, int, int]]] = {}
        self.nodes: list[tuple[int, int, int]] = []
        self.uf = _UnionFind()

    def _overlap_iou(self, start: int, end: int, cs: int, ce: int) -> float:
        inter = min(end, ce) - max(start, cs)
        if inter <= 0:
            return 0.0
        iou = inter / (max(end, ce) - min(start, cs))
        cont = inter / min(end - start, ce - cs)
        return iou if (iou >= 0.65 or (cont >= _SNAP_IOU and iou >= 0.50)) else 0.0

    def snap(self, file_idx: int, start: int, end: int) -> int:
        """Return existing canonical node ID if IoU/containment threshold met, else create one."""
        b0, b1 = start // _BIN_SIZE, max(start // _BIN_SIZE, (end - 1) // _BIN_SIZE)
        best_id, best_iou = -1, 0.0
        for b_idx in range(b0, b1 + 1):
            for cs, ce, cid in self.bins.get((file_idx, b_idx), ()):
                iou = self._overlap_iou(start, end, cs, ce)
                if iou > best_iou:
                    best_iou, best_id = iou, cid
        if best_id >= 0:
            return best_id
        nid = self.uf.add()
        self.nodes.append((file_idx, start, end))
        for b_idx in range(b0, b1 + 1):
            self.bins.setdefault((file_idx, b_idx), []).append((start, end, nid))
        return nid


@dataclass(slots=True)
class _FileAccumulator:
    """Per-file DRY metric accumulator over merged clone groups."""

    intervals: dict[str, list[tuple[int, int]]]
    blocks: dict[str, int]
    penalties: dict[str, float]
    findings: dict[str, list[str]]

    @classmethod
    def from_streams(cls, streams: list[FileTokenStream]) -> _FileAccumulator:
        """Initialize empty buckets keyed by every analyzed file path."""
        return cls(
            {s.file_path: [] for s in streams},
            {s.file_path: 0 for s in streams},
            {s.file_path: 0.0 for s in streams},
            {s.file_path: [] for s in streams},
        )

    def record_group(self, grp: CloneGroup) -> None:
        """Record occurrence line spans, duplicate counts, penalties, and findings."""
        weight = _TYPE_PENALTY.get(grp.clone_type, 3.0)
        by_file: dict[str, list[CloneLocation]] = {}
        for occ in grp.occurrences:
            by_file.setdefault(occ.file_path, []).append(occ)
        for path, local_occs in by_file.items():
            is_intra = grp.scope == "intra_file"
            billed = local_occs[1:] if is_intra else local_occs
            for occ in billed:
                eff_end = min(occ.end_line, occ.start_line + occ.loc - 1)
                self.intervals.setdefault(path, []).append((occ.start_line, eff_end))
            copies = len(billed)
            self.blocks[path] += copies
            pts = copies * weight
            self.penalties[path] += pts
            self.findings[path].append(_format_finding(grp, local_occs[0], pts))

    def build_metric(self, stream: FileTokenStream, cfg: RubricConfig) -> FileDryMetrics:
        """Finalize merged duplicated_loc and bounded penalty for one file."""
        dup_loc = _merge_line_intervals(self.intervals[stream.file_path], stream.loc)
        ratio = max(0.0, min(100.0, round((dup_loc / stream.loc * 100.0) if stream.loc > 0 else 0.0, 2)))
        max_ideal = cfg.dry_max_ideal_pct_test if stream.is_test else cfg.dry_max_ideal_pct_src
        max_cap = cfg.dry_max_penalty_test if stream.is_test else cfg.dry_max_penalty_src
        density_pen = round(0.5 * max(0.0, ratio - max_ideal), 1)
        blocks = self.blocks[stream.file_path]
        raw_pen = self.penalties[stream.file_path] + density_pen
        penalty = round(min(max_cap, raw_pen), 1) if (blocks > 0 or raw_pen > 0.0) else 0.0
        findings = list(self.findings[stream.file_path])
        if density_pen > 0.0:
            findings.append(f"Clean (DRY): duplication_ratio={ratio:.1f}% (>{max_ideal:.1f}%) (-{density_pen:.1f} pts)")
        return FileDryMetrics(
            duplicate_blocks=blocks,
            duplicated_loc=dup_loc,
            duplication_ratio=ratio,
            dry_score=clamp_score(100.0 - penalty),
            dry_penalty=penalty,
            findings=findings,
        )


def _within_thresholds(match: RawCloneMatch, streams: list[FileTokenStream], cfg: RubricConfig) -> bool:
    sa, sb = streams[match.file_a], streams[match.file_b]
    is_test = sa.is_test or sb.is_test
    min_toks = cfg.dry_min_tokens_test if is_test else cfg.dry_min_tokens
    min_lines = cfg.dry_min_lines_test if is_test else cfg.dry_min_lines
    if min(match.end_a - match.start_a, match.end_b - match.start_b) < min_toks:
        return False
    if (int(sa.lines[match.end_a - 1]) - int(sa.lines[match.start_a]) + 1) < min_lines:
        return False
    if (int(sb.lines[match.end_b - 1]) - int(sb.lines[match.start_b]) + 1) < min_lines:
        return False
    if min(len(set(sa.lines[match.start_a:match.end_a])), len(set(sb.lines[match.start_b:match.end_b]))) < min_lines:
        return False
    return match.clone_type != "type3" or match.similarity >= cfg.dry_type3_similarity


def _normalize_match(match: RawCloneMatch, streams: list[FileTokenStream], cfg: RubricConfig) -> RawCloneMatch | None:
    sa_s, ea_s, fa = match.start_a, match.end_a, match.file_a
    sb_s, eb_s, fb = match.start_b, match.end_b, match.file_b
    if (fa, sa_s, ea_s) > (fb, sb_s, eb_s):
        fa, sa_s, ea_s, fb, sb_s, eb_s = fb, sb_s, eb_s, fa, sa_s, ea_s
    non_empty = ea_s > sa_s and eb_s > sb_s
    disjoint = fa != fb or ea_s <= sb_s
    if not (non_empty and disjoint):
        return None
    ordered = RawCloneMatch(fa, sa_s, ea_s, fb, sb_s, eb_s, match.clone_type, match.similarity)
    return ordered if _within_thresholds(ordered, streams, cfg) else None


def _is_pair_contained(cand: RawCloneMatch, kept: RawCloneMatch) -> bool:
    inter_a = min(cand.end_a, kept.end_a) - max(cand.start_a, kept.start_a)
    inter_b = min(cand.end_b, kept.end_b) - max(cand.start_b, kept.start_b)
    if inter_a <= 0 or inter_b <= 0:
        return False
    ov_a = inter_a / (cand.end_a - cand.start_a)
    ov_b = inter_b / (cand.end_b - cand.start_b)
    return ov_a >= _SUBSUMPTION_OVERLAP and ov_b >= _SUBSUMPTION_OVERLAP


def _is_subsumed(cand: RawCloneMatch, bins_b: dict[tuple[int, int, int], list[RawCloneMatch]]) -> bool:
    seen: set[int] = set()
    b0, b1 = cand.start_b // _BIN_SIZE, max(cand.start_b // _BIN_SIZE, (cand.end_b - 1) // _BIN_SIZE)
    for b_idx in range(b0, b1 + 1):
        for kept in bins_b.get((cand.file_a, cand.file_b, b_idx), ()):
            if id(kept) not in seen:
                seen.add(id(kept))
                if _is_pair_contained(cand, kept):
                    return True
    return False


def _filter_subsumed(matches: list[RawCloneMatch]) -> list[RawCloneMatch]:
    ordered = sorted(
        matches,
        key=lambda m: (
            _TYPE_RANK.get(m.clone_type, 2),
            -min(m.end_a - m.start_a, m.end_b - m.start_b),
            m.file_a,
            m.start_a,
            m.file_b,
            m.start_b,
        ),
    )
    kept: list[RawCloneMatch] = []
    bins_b: dict[tuple[int, int, int], list[RawCloneMatch]] = {}
    for cand in ordered:
        if _is_subsumed(cand, bins_b):
            continue
        kept.append(cand)
        b0, b1 = cand.start_b // _BIN_SIZE, max(cand.start_b // _BIN_SIZE, (cand.end_b - 1) // _BIN_SIZE)
        for b_idx in range(b0, b1 + 1):
            bins_b.setdefault((cand.file_a, cand.file_b, b_idx), []).append(cand)
    return kept


def _find_symbol(stream: FileTokenStream, start_tok: int, end_tok: int) -> str:
    s_line, e_line = int(stream.lines[start_tok]), int(stream.lines[end_tok - 1])
    best: tuple[int, int, str] = (0, 0, "<module>")
    for blk in stream.blocks:
        if blk.end_tok > blk.start_tok:
            ov, span = min(end_tok, blk.end_tok) - max(start_tok, blk.start_tok), blk.end_tok - blk.start_tok
        else:
            ov, span = min(e_line, blk.end_line) - max(s_line, blk.start_line) + 1, blk.end_line - blk.start_line + 1
        if ov > 0 and (ov, -span) > (best[0], best[1]):
            best = (ov, -span, blk.symbol)
    return best[2]


def _make_location(stream: FileTokenStream, start_tok: int, end_tok: int) -> CloneLocation:
    s_line, e_line = int(stream.lines[start_tok]), int(stream.lines[end_tok - 1])
    if s_line > e_line:
        s_line, e_line = e_line, s_line
    loc = max(1, len(set(stream.lines[start_tok:end_tok])))
    return CloneLocation(stream.file_path, s_line, e_line, _find_symbol(stream, start_tok, end_tok), loc, end_tok - start_tok)


def _merge_line_intervals(intervals: list[tuple[int, int]], max_loc: int) -> int:
    if not intervals or max_loc <= 0:
        return 0
    ordered = sorted(intervals)
    cur_s, cur_e = ordered[0]
    total = 0
    for s_val, e_val in ordered[1:]:
        if s_val <= cur_e + 1:
            cur_e = max(cur_e, e_val)
        else:
            total += cur_e - cur_s + 1
            cur_s, cur_e = s_val, e_val
    return min(max_loc, total + cur_e - cur_s + 1)


def _format_finding(group: CloneGroup, local_occ: CloneLocation, billed_pts: float) -> str:
    peers = [
        occ
        for occ in group.occurrences
        if (occ.file_path, occ.start_line, occ.end_line)
        != (local_occ.file_path, local_occ.start_line, local_occ.end_line)
    ]
    peer_str = ", ".join(f"{p.file_path}:{p.start_line}-{p.end_line} ({p.symbol})" for p in peers[:3])
    if len(peers) > 3:
        peer_str += f" (+{len(peers) - 3} more)"
    sim_tag = f", {group.similarity * 100:.1f}%" if group.clone_type == "type3" else ""
    return (
        f"Clean (DRY): {group.group_id} ({group.clone_type}{sim_tag}, {group.tokens} toks, "
        f"{local_occ.loc} LOC) L{local_occ.start_line}-{local_occ.end_line} "
        f"in {local_occ.symbol} matches {peer_str} (-{billed_pts:.1f} pts)"
    )


def _assemble_group(
    streams: list[FileTokenStream],
    nodes: list[tuple[int, int, int]],
    members: list[int],
    stats: tuple[int, float],
) -> tuple[tuple[int, int, int, str, int], CloneGroup]:
    raw_occs = sorted(
        (_make_location(streams[nodes[i][0]], nodes[i][1], nodes[i][2]) for i in members),
        key=lambda o: (-o.token_count, o.file_path, o.start_line, o.end_line),
    )
    kept_occs: list[CloneLocation] = []
    for occ in raw_occs:
        same_f = [k for k in kept_occs if k.file_path == occ.file_path]
        if not any(min(occ.end_line, k.end_line) >= max(occ.start_line, k.start_line) for k in same_f):
            kept_occs.append(occ)
    occs = sorted(kept_occs, key=lambda o: (o.file_path, o.start_line, o.end_line, o.symbol))
    rank, min_sim = stats
    scope = "cross_file" if len({o.file_path for o in occs}) > 1 else "intra_file"
    rep_tokens = max(o.token_count for o in occs)
    rep_loc = max(o.loc for o in occs)
    grp = CloneGroup(
        "", _TYPE_FROM_RANK[rank], scope, round(min_sim, 4), rep_tokens, rep_loc, occs,
    )
    sort_key = (-(rep_loc * len(occs)), -rep_tokens, -len(occs), occs[0].file_path, occs[0].start_line)
    return sort_key, grp


def _dedup_intra_method_groups(raw_groups: list[tuple[tuple[int, int, int, str, int], CloneGroup]]) -> list[CloneGroup]:
    raw_groups.sort(key=lambda item: item[0])
    seen_self: dict[tuple[str, str], list[tuple[int, int]]] = {}
    selected: list[CloneGroup] = []
    for _, grp in raw_groups:
        if len(grp.occurrences) < 2:
            continue
        syms = {(o.file_path, o.symbol) for o in grp.occurrences}
        if len(syms) == 1:
            key = next(iter(syms))
            spans = seen_self.setdefault(key, [])
            if key[1] != "<module>" and all(
                any((min(o.end_line, e) - max(o.start_line, s) + 1) / max(1, o.end_line - o.start_line + 1) >= 0.5 for s, e in spans)
                for o in grp.occurrences
            ):
                continue
            spans.extend((o.start_line, o.end_line) for o in grp.occurrences)
        selected.append(grp)
    return [replace(grp, group_id=f"DRY-{idx:03d}") for idx, grp in enumerate(selected, start=1)]


def _build_groups(streams: list[FileTokenStream], matches: list[RawCloneMatch]) -> list[CloneGroup]:
    index = _SnapIndex()
    edge_meta: list[tuple[int, str, float]] = []
    for m in matches:
        na = index.snap(m.file_a, m.start_a, m.end_a)
        nb = index.snap(m.file_b, m.start_b, m.end_b)
        index.uf.union(na, nb)
        edge_meta.append((na, m.clone_type, m.similarity))
    comp_nodes: dict[int, list[int]] = {}
    for idx in range(len(index.nodes)):
        comp_nodes.setdefault(index.uf.find(idx), []).append(idx)
    comp_stats: dict[int, tuple[int, float]] = {}
    for na, ctype, sim in edge_meta:
        root = index.uf.find(na)
        prev_rank, prev_sim = comp_stats.get(root, (0, 1.0))
        comp_stats[root] = (max(prev_rank, _TYPE_RANK.get(ctype, 2)), min(prev_sim, sim))
    raw_groups = [
        _assemble_group(streams, index.nodes, members, comp_stats[root])
        for root, members in comp_nodes.items()
        if len(members) >= 2
    ]
    return _dedup_intra_method_groups(raw_groups)


def _score_per_file(
    streams: list[FileTokenStream], groups: list[CloneGroup], cfg: RubricConfig
) -> tuple[dict[str, FileDryMetrics], DrySummary]:
    acc = _FileAccumulator.from_streams(streams)
    for grp in groups:
        acc.record_group(grp)
    per_file = {s.file_path: acc.build_metric(s, cfg) for s in streams}
    total_loc, total_dup = sum(s.loc for s in streams), sum(m.duplicated_loc for m in per_file.values())
    ratio = max(0.0, min(100.0, round((total_dup / total_loc * 100.0) if total_loc > 0 else 0.0, 2)))
    weights = [max(5, s.loc) for s in streams]
    total_w = sum(weights)
    dry_score = clamp_score(sum(w * per_file[s.file_path].dry_score for w, s in zip(weights, streams)) / total_w) if total_w > 0 else 100.0
    summary = DrySummary(
        total_loc, total_dup, ratio, dry_score, len(groups),
        sum(1 for g in groups if g.clone_type == "type1"), sum(1 for g in groups if g.clone_type == "type2"),
        sum(1 for g in groups if g.clone_type == "type3"), sum(1 for g in groups if g.scope == "intra_file"),
        sum(1 for g in groups if g.scope == "cross_file"), groups,
    )
    return per_file, summary


def cluster_and_score_clones(
    streams: list[FileTokenStream],
    matches: list[RawCloneMatch],
    config: RubricConfig,
) -> tuple[dict[str, FileDryMetrics], DrySummary]:
    """Filter subsumed clones, cluster via IoU snapping + Union-Find, and compute DRY metrics."""
    valid = [nm for m in matches if (nm := _normalize_match(m, streams, config)) is not None]
    return _score_per_file(streams, _build_groups(streams, _filter_subsumed(valid)), config)


def apply_dry_metrics(report: FileReport, dry: FileDryMetrics, cfg: RubricConfig) -> FileReport:
    """Apply DRY findings, duplicated LOC, and Clean Code penalty to a FileReport."""
    if dry.duplicate_blocks == 0 and dry.duplicated_loc == 0 and dry.dry_penalty == 0.0 and not dry.findings:
        return report
    new_clean = clamp_score(report.scores.clean - dry.dry_penalty)
    if report.is_test and report.scores.clean >= 75.0:
        new_clean = max(75.0, new_clean)
    s = report.scores
    new_scores = DimensionScores.from_raw((s.srp, s.size, s.complexity, new_clean, s.security), cfg)
    return replace(
        report, duplicate_blocks=dry.duplicate_blocks, duplicated_loc=dry.duplicated_loc,
        duplication_ratio=dry.duplication_ratio, dry_score=dry.dry_score,
        scores=new_scores, findings=[*report.findings, *dry.findings],
    )
