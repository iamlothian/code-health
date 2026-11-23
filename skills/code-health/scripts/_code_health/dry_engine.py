"""Multi-language Winnowing clone detection engine and public DRY facade."""

from __future__ import annotations

from array import array
from collections import deque
from dataclasses import dataclass, field
from typing import Sequence

from _code_health.dry_models import (
    DrySummary,
    FileDryMetrics,
    FileTokenStream,
    PyTokenMeta,
    RawCloneMatch,
)
from _code_health.dry_scoring import apply_dry_metrics, cluster_and_score_clones
from _code_health.dry_tokens import KIND_IDENT, TokenInterner, extract_python_tokens
from _code_health.dry_type3 import detect_block_type3_clones
from _code_health.models import RubricConfig

K = 16
W = 10
MAX_BUCKET = 64
_MAX_NEIGHBORS = 8
_MERSENNE_61 = (1 << 61) - 1
_BASE = 1_000_000_007
_BASE_POW = pow(_BASE, K - 1, _MERSENNE_61)
_POS_MASK = 0xFFFFFFF
_ECMASCRIPT_LANGS = frozenset({"javascript", "jsx", "typescript", "tsx", "ecmascript"})

__all__ = [
    "K",
    "W",
    "MAX_BUCKET",
    "DryAnalyzer",
    "PyTokenMeta",
    "TokenInterner",
    "apply_dry_metrics",
    "extract_python_tokens",
]


@dataclass(slots=True)
class _PairContext:
    file_a: int
    file_b: int
    sa: FileTokenStream
    sb: FileTokenStream
    block_ids_a: array[int]
    block_ids_b: array[int]
    exact_only: bool


@dataclass(slots=True)
class _MatchState:
    la: int
    ra: int
    lb: int
    rb: int
    block_a: int
    block_b: int
    fwd: dict[int, int] = field(default_factory=dict)
    rev: dict[int, int] = field(default_factory=dict)
    all_exact: bool = True

    def check_bijection(self, exa: int, exb: int) -> bool:
        """Enforce 1-to-1 identifier mapping across the current clone span."""
        if (exa in self.fwd and self.fwd[exa] != exb) or (exb in self.rev and self.rev[exb] != exa):
            return False
        self.fwd[exa] = exb
        self.rev[exb] = exa
        return True


class _GapStitcher:
    """Chain contiguous normalized seeds separated by small Type-3 gaps."""

    def __init__(self, ctx: _PairContext, seeds: list[tuple[int, int, int, int]], cfg: RubricConfig) -> None:
        self.ctx = ctx
        self.ordered = sorted(seeds)
        self.cfg = cfg
        self.max_ov = min(6, cfg.dry_max_gap_tokens // 2)
        self.consumed: set[int] = set()

    def _can_chain(self, ra: int, rb: int, nxt: tuple[int, int, int, int], lb_cap: int) -> bool:
        nla, nra, nlb, nrb = nxt
        ga, gb = nla - ra, nlb - rb
        same_blk = (
            self.ctx.block_ids_a[nla] == self.ctx.block_ids_a[ra - 1]
            and self.ctx.block_ids_b[nlb] == self.ctx.block_ids_b[rb - 1]
        )
        in_gap = -self.max_ov <= ga <= self.cfg.dry_max_gap_tokens and -self.max_ov <= gb <= self.cfg.dry_max_gap_tokens
        return same_blk and nra > ra and nrb > rb and in_gap and nra <= lb_cap

    def _extend_from(self, start_idx: int) -> tuple[tuple[int, int, int, int], int, list[int]]:
        la, ra, lb, rb = self.ordered[start_idx]
        lb_cap = lb if self.ctx.file_a == self.ctx.file_b else _POS_MASK
        matched, chain, pos = ra - la, [start_idx], start_idx + 1
        max_reach = self.cfg.dry_max_gap_tokens
        while pos < len(self.ordered) and self.ordered[pos][0] <= ra + max_reach:
            cand = self.ordered[pos]
            if pos not in self.consumed and self._can_chain(ra, rb, cand, lb_cap):
                matched += min(cand[1] - max(ra, cand[0]), cand[3] - max(rb, cand[2]))
                ra, rb = cand[1], cand[3]
                chain.append(pos)
            pos += 1
        return (la, ra, lb, rb), matched, chain

    def stitch(self, full_matches: list[RawCloneMatch], min_t: int, min_l: int) -> list[RawCloneMatch]:
        """Return non-overlapping gapped Type-3 matches meeting thresholds."""
        stitched: list[RawCloneMatch] = []
        for idx in range(len(self.ordered)):
            if idx in self.consumed:
                continue
            span, matched, chain = self._extend_from(idx)
            if len(chain) < 2 or not _meets_span_thresholds(self.ctx, span, min_t, min_l):
                continue
            sim = round(matched / max(span[1] - span[0], span[3] - span[2]), 4)
            if sim >= self.cfg.dry_type3_similarity and not _span_is_covered(span, full_matches):
                self.consumed.update(chain)
                stitched.append(RawCloneMatch(self.ctx.file_a, span[0], span[1], self.ctx.file_b, span[2], span[3], "type3", sim))
        return stitched


def _build_token_block_ids(stream: FileTokenStream) -> array[int]:
    ids = array("i", [-1] * len(stream.exact_ids))
    ranked = sorted(enumerate(stream.blocks), key=lambda item: -(item[1].end_tok - item[1].start_tok))
    for orig_idx, blk in ranked:
        s_tok = max(0, blk.start_tok)
        e_tok = min(len(ids), blk.end_tok)
        for pos in range(s_tok, e_tok):
            ids[pos] = orig_idx
    return ids


def _update_window(dq: deque[tuple[int, int]], h: int, pos: int) -> None:
    if dq and dq[0][1] <= pos - W:
        dq.popleft()
    while dq and dq[-1][0] >= h:
        dq.pop()
    dq.append((h, pos))


def _winnow_stream(ids: Sequence[int]) -> list[tuple[int, int]]:
    length = len(ids)
    if length < K:
        return []
    h = 0
    for val in ids[:K]:
        h = (h * _BASE + val + 1) % _MERSENNE_61
    dq: deque[tuple[int, int]] = deque()
    fps: list[tuple[int, int]] = []
    last_pos = -1
    for pos in range(length - K + 1):
        if pos > 0:
            out_v = ((ids[pos - 1] + 1) * _BASE_POW) % _MERSENNE_61
            h = ((h - out_v) * _BASE + ids[pos + K - 1] + 1) % _MERSENNE_61
        _update_window(dq, h, pos)
        if pos >= W - 1 and dq[0][1] != last_pos:
            fps.append(dq[0])
            last_pos = dq[0][1]
    return fps


def _index_partition(
    streams: list[FileTokenStream],
    block_ids_all: list[array[int]],
    indices: list[int],
    use_norm: bool,
) -> dict[int, list[int]]:
    buckets: dict[int, list[int]] = {}
    for fidx in indices:
        stream = streams[fidx]
        seq = stream.norm_ids if use_norm else stream.exact_ids
        skip_mod = stream.is_test and bool(stream.blocks)
        blk_ids = block_ids_all[fidx]
        packed_hi = fidx << 28
        for h, pos in _winnow_stream(seq):
            if blk_ids[pos] != blk_ids[pos + K - 1] or (skip_mod and blk_ids[pos] < 0):
                continue
            bucket = buckets.setdefault(h, [])
            if len(bucket) < MAX_BUCKET:
                bucket.append(packed_hi | pos)
    return buckets


def _add_bucket_pairs(
    locs: list[int], min_toks: int, pair_sets: dict[tuple[int, int], set[tuple[int, int]]]
) -> None:
    count = len(locs)
    for i in range(count):
        fa, pa = locs[i] >> 28, locs[i] & _POS_MASK
        paired = 0
        for j in range(i + 1, count):
            fb, pb = locs[j] >> 28, locs[j] & _POS_MASK
            if fa != fb or pb - pa >= min_toks:
                pair_sets.setdefault((fa, fb), set()).add((pa, pb))
                paired += 1
                if paired >= _MAX_NEIGHBORS:
                    break


def _collect_candidate_pairs(
    buckets: dict[int, list[int]], min_toks: int
) -> dict[tuple[int, int], list[tuple[int, int]]]:
    pair_sets: dict[tuple[int, int], set[tuple[int, int]]] = {}
    for locs in buckets.values():
        if len(locs) >= 2:
            _add_bucket_pairs(locs, min_toks, pair_sets)
    return {key: sorted(vals) for key, vals in pair_sets.items()}


def _step_match(ctx: _PairContext, ia: int, ib: int, state: _MatchState) -> bool:
    if ctx.block_ids_a[ia] != state.block_a or ctx.block_ids_b[ib] != state.block_b:
        return False
    sa, sb = ctx.sa, ctx.sb
    exa, exb = sa.exact_ids[ia], sb.exact_ids[ib]
    if ctx.exact_only:
        return exa == exb
    if sa.norm_ids[ia] != sb.norm_ids[ib] or sa.tok_kinds[ia] != sb.tok_kinds[ib]:
        return False
    if sa.tok_kinds[ia] == KIND_IDENT and not state.check_bijection(exa, exb):
        return False
    state.all_exact = state.all_exact and (exa == exb)
    return True


def _extend_steps(ctx: _PairContext, state: _MatchState, budget: int, step: int) -> None:
    for _ in range(max(0, budget)):
        ia = state.la - 1 if step < 0 else state.ra
        ib = state.lb - 1 if step < 0 else state.rb
        if not _step_match(ctx, ia, ib, state):
            break
        if step < 0:
            state.la -= 1
            state.lb -= 1
        else:
            state.ra += 1
            state.rb += 1


def _verify_and_extend(
    ctx: _PairContext, pa: int, pb: int, min_start_a: int
) -> tuple[int, int, int, int, str] | None:
    if ctx.exact_only:
        if ctx.sa.exact_ids[pa : pa + K] != ctx.sb.exact_ids[pb : pb + K]:
            return None
    elif ctx.sa.norm_ids[pa : pa + K] != ctx.sb.norm_ids[pb : pb + K]:
        return None
    state = _MatchState(pa, pa + K, pb, pb + K, ctx.block_ids_a[pa], ctx.block_ids_b[pb])
    for off in range(K):
        if not _step_match(ctx, pa + off, pb + off, state):
            return None
    same_file = ctx.file_a == ctx.file_b
    delta = pb - pa if same_file else 0
    left_cap = (delta - (state.ra - state.la)) if same_file else pa
    _extend_steps(ctx, state, min(pa - min_start_a, pb, left_cap), -1)
    len_a, len_b = len(ctx.sa.norm_ids), len(ctx.sb.norm_ids)
    right_cap = (delta - (state.ra - state.la)) if same_file else len_a
    _extend_steps(ctx, state, min(len_a - state.ra, len_b - state.rb, right_cap), 1)
    ctype = "type1" if state.all_exact else "type2"
    return state.la, state.ra, state.lb, state.rb, ctype


def _has_min_lines(lines: Sequence[int], start: int, end: int, min_lines: int) -> bool:
    if min_lines <= 1:
        return end > start
    distinct, prev = 1, lines[start]
    for k in range(start + 1, end):
        val = lines[k]
        if val != prev:
            distinct += 1
            prev = val
            if distinct >= min_lines:
                return True
    return False


def _meets_span_thresholds(
    ctx: _PairContext, span: tuple[int, int, int, int], min_toks: int, min_lines: int
) -> bool:
    la, ra, lb, rb = span
    if min(ra - la, rb - lb) < min_toks:
        return False
    return _has_min_lines(ctx.sa.lines, la, ra, min_lines) and _has_min_lines(ctx.sb.lines, lb, rb, min_lines)


def _span_is_covered(span: tuple[int, int, int, int], full_matches: list[RawCloneMatch]) -> bool:
    la, ra, lb, rb = span
    for m in full_matches:
        ova = (min(ra, m.end_a) - max(la, m.start_a)) >= 0.75 * (ra - la)
        ovb = (min(rb, m.end_b) - max(lb, m.start_b)) >= 0.75 * (rb - lb)
        if ova and ovb:
            return True
    return False


def _scan_file_pair(
    ctx: _PairContext, pairs: list[tuple[int, int]], cfg: RubricConfig
) -> list[RawCloneMatch]:
    min_t = cfg.dry_min_tokens_test if ctx.sa.is_test else cfg.dry_min_tokens
    min_l = cfg.dry_min_lines_test if ctx.sa.is_test else cfg.dry_min_lines
    diag_last_end: dict[int, int] = {}
    matches: list[RawCloneMatch] = []
    seeds: list[tuple[int, int, int, int]] = []
    for pa, pb in pairs:
        delta = pb - pa
        min_start = diag_last_end.get(delta, 0)
        if pa < min_start:
            continue
        ext = _verify_and_extend(ctx, pa, pb, min_start)
        if ext is None:
            continue
        la, ra, lb, rb, ctype = ext
        diag_last_end[delta] = max(min_start, ra)
        seeds.append((la, ra, lb, rb))
        if _meets_span_thresholds(ctx, (la, ra, lb, rb), min_t, min_l):
            matches.append(RawCloneMatch(ctx.file_a, la, ra, ctx.file_b, lb, rb, ctype, 1.0))
    if not ctx.exact_only and len(seeds) >= 2:
        matches.extend(_GapStitcher(ctx, seeds, cfg).stitch(matches, min_t, min_l))
    return matches


def _run_pass(
    streams: list[FileTokenStream],
    block_ids_all: list[array[int]],
    indices: list[int],
    params: tuple[RubricConfig, bool],
) -> list[RawCloneMatch]:
    cfg, exact_only = params
    is_test = streams[indices[0]].is_test
    min_toks = cfg.dry_min_tokens_test if is_test else cfg.dry_min_tokens
    buckets = _index_partition(streams, block_ids_all, indices, use_norm=not exact_only)
    pair_map = _collect_candidate_pairs(buckets, min_toks)
    matches: list[RawCloneMatch] = []
    for (fa, fb), pairs in pair_map.items():
        ctx = _PairContext(fa, fb, streams[fa], streams[fb], block_ids_all[fa], block_ids_all[fb], exact_only)
        matches.extend(_scan_file_pair(ctx, pairs, cfg))
    return matches


class DryAnalyzer:
    """Detect exact, parameterized, and Type-3 code clones across languages."""

    def __init__(self, config: RubricConfig) -> None:
        self.config = config

    def analyze(
        self, streams: list[FileTokenStream]
    ) -> tuple[dict[str, FileDryMetrics], DrySummary]:
        """Run partitioned Winnowing, gap-stitching, SourcererCC Type-3, and scoring."""
        ordered = sorted(streams, key=lambda s: s.file_path)
        block_ids_all = [_build_token_block_ids(s) for s in ordered]
        partitions: dict[tuple[bool, str], list[int]] = {}
        for idx, stream in enumerate(ordered):
            bucket = "ecmascript" if stream.language in _ECMASCRIPT_LANGS else stream.language
            partitions.setdefault((stream.is_test, bucket), []).append(idx)
        matches: list[RawCloneMatch] = []
        for indices in partitions.values():
            matches.extend(_run_pass(ordered, block_ids_all, indices, (self.config, True)))
            matches.extend(_run_pass(ordered, block_ids_all, indices, (self.config, False)))
        matches.extend(detect_block_type3_clones(ordered, matches, self.config))
        return cluster_and_score_clones(ordered, matches, self.config)
