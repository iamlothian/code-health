"""Data models for multi-language duplicate code detection and DRY metrics."""

from __future__ import annotations

from array import array
from dataclasses import dataclass, field


@dataclass(frozen=True)
class CloneLocation:
    """Single occurrence of a duplicated code region within a source or test file."""

    file_path: str
    start_line: int
    end_line: int
    symbol: str
    loc: int
    token_count: int


@dataclass(frozen=True)
class CloneGroup:
    """Cluster of two or more matching code occurrences forming a single clone group."""

    group_id: str
    clone_type: str
    scope: str
    similarity: float
    tokens: int
    loc: int
    occurrences: list[CloneLocation] = field(default_factory=list)


@dataclass(frozen=True)
class FileDryMetrics:
    """Per-file duplication metrics, Clean Code DRY deduction, and actionable findings."""

    duplicate_blocks: int = 0
    duplicated_loc: int = 0
    duplication_ratio: float = 0.0
    dry_score: float = 100.0
    dry_penalty: float = 0.0
    findings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class DrySummary:
    """Aggregated codebase-wide duplicate code counts, duplication ratio, and clone groups."""

    total_loc: int = 0
    duplicated_loc: int = 0
    duplication_ratio: float = 0.0
    dry_score: float = 100.0
    clone_groups_count: int = 0
    type1_groups: int = 0
    type2_groups: int = 0
    type3_groups: int = 0
    intra_file_groups: int = 0
    cross_file_groups: int = 0
    clone_groups: list[CloneGroup] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class PyTokenMeta:
    """Metadata bundle passed into Python token stream extraction."""

    rel_path: str
    is_test: bool
    loc: int
    block_bounds: tuple[tuple[str, int, int, int], ...]


@dataclass(frozen=True, slots=True)
class BlockSpan:
    """Executable token and line bounds for a single function or method."""

    symbol: str
    start_tok: int
    end_tok: int
    start_line: int
    end_line: int
    loc: int
    stmt_count: int


@dataclass(frozen=True, slots=True)
class FileTokenStream:
    """Compact flat-array token stream extracted in a single pass per source file."""

    file_path: str
    language: str
    is_test: bool
    loc: int
    exact_ids: array[int]
    norm_ids: array[int]
    lines: array[int]
    tok_kinds: array[int]
    stmt_starts: array[int]
    blocks: tuple[BlockSpan, ...]


@dataclass(frozen=True, slots=True)
class RawCloneMatch:
    """Unclustered pairwise clone candidate in file-index and token coordinates."""

    file_a: int
    start_a: int
    end_a: int
    file_b: int
    start_b: int
    end_b: int
    clone_type: str
    similarity: float
