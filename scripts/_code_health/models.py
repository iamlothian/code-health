"""Data models, configuration thresholds, and AST constants for Code Health Analyzer."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RubricConfig:
    """Configuration weights and thresholds for deterministic code health scoring."""

    weight_srp: float = 0.30
    weight_size: float = 0.25
    weight_complexity: float = 0.20
    weight_clean: float = 0.15
    weight_security: float = 0.10
    max_ideal_func_loc_src: int = 25
    max_mid_func_loc_src: int = 50
    max_ideal_func_loc_test: int = 40
    max_mid_func_loc_test: int = 75
    max_ideal_params: int = 4
    max_entrypoint_params: int = 6
    max_ideal_nesting: int = 3
    max_ideal_cc: int = 5
    max_mid_cc: int = 10
    max_ideal_cogc: int = 8
    max_ideal_returns: int = 3
    max_ideal_concerns: int = 2
    max_ideal_external_calls: int = 6
    max_ideal_class_loc: int = 200
    max_ideal_class_methods: int = 10
    max_ideal_class_attrs: int = 7
    max_ideal_class_cc: int = 25
    max_ideal_file_loc: int = 350
    max_mid_file_loc: int = 600
    max_ideal_internal_imports: int = 5
    max_ideal_commits: int = 8


def clamp_score(value: float) -> float:
    """Clamp a score into [0.0, 100.0] rounded to 1 decimal place."""
    return round(max(0.0, min(100.0, value)), 1)


def score_to_grade(score: float) -> str:
    """Map a 0-100 composite score to an A-F letter grade."""
    for threshold, grade in ((90.0, "A"), (80.0, "B"), (70.0, "C"), (60.0, "D")):
        if score >= threshold:
            return grade
    return "F"


def penalty_item(excess: float, weight: float, msg: str, cap: float = 100.0) -> tuple[float, list[str]]:
    """Return (clamped_penalty, [formatted_finding]) when excess > 0."""
    if excess <= 0:
        return 0.0, []
    pen = round(min(cap, excess * weight), 1)
    return pen, [f"{msg} (-{pen:.1f} pts)"]


@dataclass(frozen=True)
class DimensionScores:
    """Five-dimension health scores and weighted composite grade."""

    srp: float
    size: float
    complexity: float
    clean: float
    security: float
    composite: float
    grade: str

    @classmethod
    def from_raw(cls, raw: tuple[float, float, float, float, float], config: RubricConfig) -> DimensionScores:
        """Create clamped DimensionScores from (srp, size, complexity, clean, security) with worst-dimension ceiling."""
        s_srp, s_size, s_comp, s_clean, s_sec = (clamp_score(v) for v in raw)
        weighted = (
            config.weight_srp * s_srp
            + config.weight_size * s_size
            + config.weight_complexity * s_comp
            + config.weight_clean * s_clean
            + config.weight_security * s_sec
        )
        min_dim = min(s_srp, s_size, s_comp, s_clean, s_sec)
        if min_dim < 75.0:
            weighted = min(weighted, min_dim + 5.0, 79.5)
        comp = clamp_score(weighted)
        return cls(s_srp, s_size, s_comp, s_clean, s_sec, comp, score_to_grade(comp))


@dataclass
class FunctionReport:
    """Deterministic health evaluation of a single function or method."""

    name: str
    qualname: str
    file_path: str
    lineno: int
    end_lineno: int
    loc: int
    params_count: int
    max_nesting: int
    cyclomatic_complexity: int
    cognitive_complexity: int
    returns_count: int
    concerns: list[str]
    external_calls_count: int
    is_test: bool
    scores: DimensionScores
    findings: list[str] = field(default_factory=list)


@dataclass
class ClassReport:
    """Deterministic health evaluation of a single class."""

    name: str
    file_path: str
    lineno: int
    end_lineno: int
    loc: int
    methods_count: int
    attrs_count: int
    lcom4: int
    total_cc: int
    scores: DimensionScores
    findings: list[str] = field(default_factory=list)
    methods: list[FunctionReport] = field(default_factory=list)


@dataclass
class GitFileStats:
    """Git history metrics for a single file."""

    commits: int = 0
    feat_commits: int = 0
    cochange_peers: int = 0
    avg_blast_radius: float = 0.0
    last_author: str = ""


@dataclass
class FileReport:
    """Deterministic health evaluation of a Python file/module."""

    file_path: str
    is_test: bool
    loc: int
    internal_imports: list[str]
    duplicate_blocks: int
    mid_file_imports: int
    git: GitFileStats | None
    scores: DimensionScores
    findings: list[str] = field(default_factory=list)
    classes: list[ClassReport] = field(default_factory=list)
    functions: list[FunctionReport] = field(default_factory=list)


@dataclass
class CodebaseHealthReport:
    """Aggregated deterministic health report across a set of target paths."""

    target_paths: list[str]
    files_count: int
    src_files_count: int
    test_files_count: int
    classes_count: int
    functions_count: int
    scores: DimensionScores
    src_scores: DimensionScores
    test_scores: DimensionScores
    grade_counts: dict[str, int]
    files: list[FileReport] = field(default_factory=list)


@dataclass(frozen=True)
class AnalysisContext:
    """Context parameters for analyzing AST nodes within a source file."""

    source_lines: list[str]
    file_path: str
    is_test: bool
    config: RubricConfig
    class_name: str | None = None


@dataclass(frozen=True)
class RenderFilter:
    """Display filter criteria for console and markdown scorecard rendering."""

    only_flagged: bool = False
    min_grade: str | None = None
    symbol: str | None = None
    show_all_funcs: bool = False


ENTRYPOINT_DECORATORS = {"command", "tool", "resource", "prompt", "get", "post", "put", "delete", "patch", "route", "callback"}
CONCERN_EXACT_MAP: dict[str, str] = {
    **{k: "presentation" for k in ("print", "console.print", "err_console.print", "typer.echo", "click.echo", "Table", "Panel", "Markdown", "Confirm.ask")},
    **{k: "cli_or_rpc_framework" for k in ("typer.Option", "typer.Argument", "typer.Exit", "click.Context", "FastMCP")},
    **{k: "filesystem_io" for k in ("read_text", "write_text", "read_bytes", "write_bytes", "mkdir", "unlink", "rmdir", "rglob", "glob", "iterdir", "open", "os.walk", "shutil.copy", "shutil.copy2", "shutil.copytree", "shutil.rmtree", "shutil.move")},
    **{k: "subprocess_git" for k in ("subprocess.run", "subprocess.Popen", "subprocess.check_output", "subprocess.call", "shutil.which", "checkout_branch", "commit_all", "create_pr_or_mr", "is_behind_remote")},
    **{k: "serialization" for k in ("yaml.safe_load", "yaml.load", "yaml.dump", "yaml.safe_dump", "json.loads", "json.dumps", "json.load", "json.dump", "tomllib.loads", "tomllib.load", "pickle.loads", "pickle.load")},
}
CONCERN_SHORT_MAP: dict[str, str] = {
    **{k: "presentation" for k in ("Table", "Panel", "Markdown")},
    **{k: "cli_or_rpc_framework" for k in ("Option", "Argument", "Exit")},
    **{k: "filesystem_io" for k in ("read_text", "write_text", "mkdir", "unlink", "rglob", "glob")},
    **{k: "subprocess_git" for k in ("checkout_branch", "commit_all", "create_pr_or_mr")},
    **{k: "serialization" for k in ("safe_load", "safe_dump", "loads", "dumps")},
}
STDLIB_TRIVIAL_CALLS = {
    "len", "min", "max", "sum", "round", "sorted", "set", "list", "dict", "tuple", "str", "int",
    "float", "bool", "any", "all", "enumerate", "zip", "range", "isinstance", "getattr", "hasattr",
    "append", "extend", "add", "get", "items", "keys", "values", "split", "splitlines", "strip",
    "lstrip", "rstrip", "replace", "startswith", "endswith", "lower", "upper", "join", "pop",
    "as_posix", "is_file", "is_dir", "exists", "walk", "dump", "update", "setdefault", "resolve",
    "relative_to", "is_relative_to", "parse_args", "add_argument", "get_docstring", "asdict",
    "defaultdict", "Path", "cwd", "write", "parse", "from_raw", "penalty_item", "count_effective_loc",
    "filter", "is_test_file_path",
}
EXEMPT_LCOM_BASES = {
    "BaseModel", "Exception", "RuntimeError", "ValueError", "Enum", "StrEnum", "IntEnum",
    "TypedDict", "NamedTuple", "TyperGroup", "TyperCommand", "Protocol",
    "FrameworkProfile", "LanguageProfile",
}
IGNORED_SCAN_DIRS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", "build", "dist", ".superpowers", ".agents", ".specify",
}
GRADE_ORDER = {"A": 5, "B": 4, "C": 3, "D": 2, "F": 1}
