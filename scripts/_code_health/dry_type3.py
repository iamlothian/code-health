"""SourcererCC prefix-filtered Type-3 block clone detector."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from difflib import SequenceMatcher
import math
from typing import Sequence

from _code_health.dry_models import BlockSpan, FileTokenStream, RawCloneMatch
from _code_health.models import RubricConfig

_NGRAM = 3
_MAX_POSTING = 64
_EXISTING_COVERAGE = 0.75
_ECMASCRIPT_LANGS = frozenset({"javascript", "jsx", "typescript", "tsx", "ecmascript"})


@dataclass(slots=True)
class _BlockEntry:
    file_idx: int
    start: int
    end: int
    tok_len: int
    shingles: tuple[int, ...]
    shingle_set: frozenset[int]
    stmts: tuple[tuple[int, ...], ...]
    stmt_set: frozenset[tuple[int, ...]]
    norm_ref: Sequence[int]


def _language_bucket(language: str) -> str:
    return "ecmascript" if language in _ECMASCRIPT_LANGS else language


def _collect_stmt_seqs(stream: FileTokenStream, start: int, end: int) -> tuple[tuple[int, ...], ...]:
    starts = [int(s) for s in stream.stmt_starts if start <= int(s) < end]
    if len(starts) < 3:
        return ()
    norm = stream.norm_ids
    seqs: list[tuple[int, ...]] = []
    for idx, pos in enumerate(starts):
        nxt = starts[idx + 1] if idx + 1 < len(starts) else end
        seqs.append(tuple(int(norm[k]) for k in range(pos, nxt)))
    return tuple(seqs)


def _stmt_shingles(stmts: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    occ: dict[tuple[int, ...], int] = {}
    bag: list[int] = []
    for stmt in stmts:
        h = 2166136261
        for tok in stmt:
            h = ((h ^ tok) * 16777619) & 0xFFFFFFFFFFFF
        cnt = occ.get(stmt, 0)
        occ[stmt] = cnt + 1
        bag.append((h << 8) | min(cnt, 255))
    return tuple(sorted(bag))


def _token_shingles(norm: Sequence[int], start: int, end: int) -> tuple[int, ...]:
    occ: dict[int, int] = {}
    bag: list[int] = []
    for i in range(start, end - 2):
        gram = (int(norm[i]) << 40) | (int(norm[i + 1]) << 20) | int(norm[i + 2])
        cnt = occ.get(gram, 0)
        occ[gram] = cnt + 1
        bag.append((gram << 8) | min(cnt, 255))
    return tuple(sorted(bag))


def _build_block_entry(file_idx: int, stream: FileTokenStream, blk: BlockSpan) -> _BlockEntry:
    norm = stream.norm_ids
    stmts = _collect_stmt_seqs(stream, blk.start_tok, blk.end_tok)
    shingles = _stmt_shingles(stmts) if stmts else _token_shingles(norm, blk.start_tok, blk.end_tok)
    return _BlockEntry(
        file_idx=file_idx,
        start=blk.start_tok,
        end=blk.end_tok,
        tok_len=blk.end_tok - blk.start_tok,
        shingles=shingles,
        shingle_set=frozenset(shingles),
        stmts=stmts,
        stmt_set=frozenset(stmts),
        norm_ref=norm,
    )


def _is_leaf_block(blk: BlockSpan, pool: list[BlockSpan]) -> bool:
    span = blk.end_tok - blk.start_tok
    for other in pool:
        if other is not blk and blk.start_tok <= other.start_tok and other.end_tok <= blk.end_tok:
            if (other.end_tok - other.start_tok) < span:
                return False
    return True


def _eligible_entries(file_idx: int, stream: FileTokenStream, cfg: RubricConfig) -> list[_BlockEntry]:
    min_t = max(_NGRAM, cfg.dry_min_tokens_test if stream.is_test else cfg.dry_min_tokens)
    min_l = cfg.dry_min_lines_test if stream.is_test else cfg.dry_min_lines
    raw: list[BlockSpan] = []
    for blk in stream.blocks:
        if blk.end_tok - blk.start_tok < min_t or blk.start_tok < 0:
            continue
        lines_spanned = len({int(stream.lines[k]) for k in range(blk.start_tok, blk.end_tok)})
        if lines_spanned >= min_l:
            raw.append(blk)
    return [_build_block_entry(file_idx, stream, blk) for blk in raw if _is_leaf_block(blk, raw)]


def _build_prefix_index(
    rep_shingles: list[tuple[int, ...]], theta: float
) -> dict[int, list[int]]:
    df: Counter[int] = Counter()
    for sh_set in rep_shingles:
        df.update(sh_set)
    inverted: dict[int, list[int]] = {}
    for rep_idx, sh_set in enumerate(rep_shingles):
        ordered = sorted(sh_set, key=lambda sh: (df[sh], sh))
        prefix_len = max(1, len(ordered) - math.ceil(theta * len(ordered)) + 1)
        for sh in ordered[:prefix_len]:
            posting = inverted.setdefault(sh, [])
            if len(posting) < _MAX_POSTING:
                posting.append(rep_idx)
    return inverted


def _collect_rep_pairs(
    rep_shingles: list[tuple[int, ...]],
    inverted: dict[int, list[int]],
    theta: float,
) -> set[tuple[int, int]]:
    pairs: set[tuple[int, int]] = set()
    for posting in inverted.values():
        count = len(posting)
        for i in range(count):
            ra = posting[i]
            len_a = len(rep_shingles[ra])
            for j in range(i + 1, count):
                rb = posting[j]
                len_b = len(rep_shingles[rb])
                if min(len_a, len_b) >= theta * max(len_a, len_b):
                    pairs.add((ra, rb) if ra < rb else (rb, ra))
    return pairs


def _index_existing(existing: list[RawCloneMatch]) -> dict[tuple[int, int], list[tuple[int, int, int, int]]]:
    by_pair: dict[tuple[int, int], list[tuple[int, int, int, int]]] = {}
    for m in existing:
        if m.file_a <= m.file_b:
            by_pair.setdefault((m.file_a, m.file_b), []).append((m.start_a, m.end_a, m.start_b, m.end_b))
        else:
            by_pair.setdefault((m.file_b, m.file_a), []).append((m.start_b, m.end_b, m.start_a, m.end_a))
    return by_pair


def _is_covered(
    a: _BlockEntry, b: _BlockEntry, existing_map: dict[tuple[int, int], list[tuple[int, int, int, int]]]
) -> bool:
    for sa, ea, sb, eb in existing_map.get((a.file_idx, b.file_idx), ()):
        ov_a = (min(a.end, ea) - max(a.start, sa)) / a.tok_len
        ov_b = (min(b.end, eb) - max(b.start, sb)) / b.tok_len
        if ov_a >= _EXISTING_COVERAGE and ov_b >= _EXISTING_COVERAGE:
            return True
    return False


def _passes_prefilter(
    a: _BlockEntry,
    b: _BlockEntry,
    existing_map: dict[tuple[int, int], list[tuple[int, int, int, int]]],
    theta: float,
) -> bool:
    if a.file_idx == b.file_idx and a.end > b.start:
        return False
    if min(a.tok_len, b.tok_len) < theta * max(a.tok_len, b.tok_len):
        return False
    if _is_covered(a, b, existing_map):
        return False
    if a.stmts and b.stmts:
        common = a.stmt_set & b.stmt_set
        if not common:
            return False
        max_m = min(sum(1 for s in a.stmts if s in common), sum(1 for s in b.stmts if s in common))
        return (2.0 * max_m / (len(a.stmts) + len(b.stmts))) >= theta
    inter = len(a.shingle_set & b.shingle_set)
    denom = len(a.shingle_set) + len(b.shingle_set)
    return denom > 0 and (2.0 * inter / denom) >= max(0.15, theta - 0.45)


def _sequence_similarity(a: _BlockEntry, b: _BlockEntry) -> float:
    if not (a.stmts and b.stmts):
        return SequenceMatcher(None, a.norm_ref[a.start : a.end], b.norm_ref[b.start : b.end], autojunk=False).ratio()
    matcher = SequenceMatcher(None, a.stmts, b.stmts, autojunk=False)
    unweighted = matcher.ratio()
    matched_toks = sum(
        sum(len(a.stmts[i + k]) for k in range(n))
        for i, _, n in matcher.get_matching_blocks()
    )
    total_stmt_toks = sum(len(s) for s in a.stmts) + sum(len(s) for s in b.stmts)
    weighted = (2.0 * matched_toks / total_stmt_toks) if total_stmt_toks > 0 else 0.0
    return min(unweighted, weighted)


def _score_pair(
    a: _BlockEntry,
    b: _BlockEntry,
    existing_map: dict[tuple[int, int], list[tuple[int, int, int, int]]],
    theta: float,
) -> RawCloneMatch | None:
    if (a.file_idx, a.start, a.end) > (b.file_idx, b.start, b.end):
        a, b = b, a
    if not _passes_prefilter(a, b, existing_map, theta):
        return None
    sim = _sequence_similarity(a, b)
    if sim < theta:
        return None
    return RawCloneMatch(a.file_idx, a.start, a.end, b.file_idx, b.start, b.end, "type3", round(sim, 4))


def _expand_rep_pair(
    members_a: list[_BlockEntry],
    members_b: list[_BlockEntry],
    params: tuple[dict[tuple[int, int], list[tuple[int, int, int, int]]], float, bool],
) -> list[RawCloneMatch]:
    existing_map, theta, same_rep = params
    out: list[RawCloneMatch] = []
    cap_a = members_a[:_MAX_POSTING]
    cap_b = members_b[:_MAX_POSTING]
    for i, blk_a in enumerate(cap_a):
        start_j = i + 1 if same_rep else 0
        for blk_b in cap_b[start_j:]:
            match = _score_pair(blk_a, blk_b, existing_map, theta)
            if match is not None:
                out.append(match)
    return out


def _detect_partition_clones(
    entries: list[_BlockEntry],
    existing_map: dict[tuple[int, int], list[tuple[int, int, int, int]]],
    theta: float,
) -> list[RawCloneMatch]:
    groups: dict[tuple[int, ...], list[_BlockEntry]] = {}
    for entry in entries:
        groups.setdefault(entry.shingles, []).append(entry)
    rep_shingles = list(groups.keys())
    rep_members = list(groups.values())
    inverted = _build_prefix_index(rep_shingles, theta)
    rep_pairs = _collect_rep_pairs(rep_shingles, inverted, theta)
    for idx, members in enumerate(rep_members):
        if len(members) >= 2:
            rep_pairs.add((idx, idx))
    matches: list[RawCloneMatch] = []
    for ra, rb in sorted(rep_pairs):
        matches.extend(_expand_rep_pair(rep_members[ra], rep_members[rb], (existing_map, theta, ra == rb)))
    return matches


def detect_block_type3_clones(
    streams: list[FileTokenStream],
    existing_matches: list[RawCloneMatch],
    config: RubricConfig,
) -> list[RawCloneMatch]:
    """Detect scattered near-miss Type-3 clones via SourcererCC prefix filtering."""
    theta = config.dry_type3_similarity
    existing_map = _index_existing(existing_matches)
    partitions: dict[tuple[bool, str], list[_BlockEntry]] = {}
    for idx, stream in enumerate(streams):
        entries = _eligible_entries(idx, stream, config)
        if entries:
            key = (stream.is_test, _language_bucket(stream.language))
            partitions.setdefault(key, []).extend(entries)
    results: list[RawCloneMatch] = []
    for entries in partitions.values():
        results.extend(_detect_partition_clones(entries, existing_map, theta))
    return results
