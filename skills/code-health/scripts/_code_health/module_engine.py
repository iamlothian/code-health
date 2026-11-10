"""Module-level AST, duplicate detection, and git history analyzers."""

from __future__ import annotations

import ast
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
import subprocess

from _code_health.ast_engine import (
    UnitScorer,
    count_effective_loc,
    docstring_lines,
    has_exempt_base,
)
from _code_health.models import (
    AnalysisContext,
    ClassReport,
    DimensionScores,
    FileReport,
    FunctionReport,
    GitFileStats,
    RubricConfig,
    penalty_item,
)


@dataclass(frozen=True)
class _ModuleMetrics:
    """Internal bundle of module-level structural metrics."""

    tree: ast.Module
    loc: int
    is_test: bool
    non_exempt_cls: int
    fn_cnt: int
    imp_cnt: int
    mid_imp: int
    dup_blocks: int
    gstat: GitFileStats | None


@dataclass
class _GitLogAccumulator:
    """Accumulator for parsing git log commit blocks."""

    commits: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    feats: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    authors: dict[str, str] = field(default_factory=dict)
    cochanges: dict[str, dict[str, int]] = field(default_factory=lambda: defaultdict(lambda: defaultdict(int)))
    radii: dict[str, list[int]] = field(default_factory=lambda: defaultdict(list))

    def record_block(self, lines: list[str]) -> None:
        """Record a single parsed git commit block."""
        header = lines[0].split("|", 2) + ["", ""]
        feat_inc = int(header[2].lower().startswith("feat"))
        files = [ln.replace("\\", "/") for ln in lines[1:]]
        source_files = [f for f in files if f.endswith((".py", ".java", ".js", ".mjs", ".cjs"))]
        for f in source_files:
            self.commits[f] += 1
            self.feats[f] += feat_inc
            self.authors.setdefault(f, header[1])
            self.radii[f].append(len(files))
            for peer in set(source_files) - {f}:
                self.cochanges[f][peer] += 1

    def to_stats(self) -> dict[str, GitFileStats]:
        """Convert accumulated counts into per-file GitFileStats."""
        return {
            f: GitFileStats(
                cnt, self.feats[f], sum(1 for c in self.cochanges[f].values() if c >= 3),
                round(sum(self.radii[f]) / len(self.radii[f]), 1), self.authors.get(f, ""),
            )
            for f, cnt in self.commits.items()
        }


def is_test_file_path(rel_path: str) -> bool:
    """Determine generically if a relative POSIX path is a test file."""
    parts = rel_path.replace("\\", "/").split("/")
    fname = parts[-1]
    is_py = fname.startswith("test_") or fname.endswith("_test.py") or fname == "conftest.py"
    is_java = fname.endswith(("Test.java", "Tests.java", "IT.java"))
    is_js = (
        fname.endswith((".test.js", ".spec.js", "_test.js", ".test.mjs", ".spec.mjs", ".test.cjs", ".spec.cjs"))
        or (fname.startswith("test_") and fname.endswith((".js", ".mjs", ".cjs")))
    )
    is_test_dir = bool({"tests", "test", "__tests__"} & set(parts))
    return is_test_dir or is_py or is_java or is_js


def collect_git_stats(repo_root: Path) -> dict[str, GitFileStats]:
    """Collect commit churn, feat touch count, and co-change coupling per file from git log."""
    try:
        res = subprocess.run(
            ["git", "log", "--no-merges", "--name-only", "--pretty=format:COMMIT:%H|%an|%s"],
            cwd=repo_root, capture_output=True, text=True, check=True, encoding="utf-8", errors="replace",
        )
    except (subprocess.SubprocessError, OSError):
        return {}
    return _parse_git_log_output(res.stdout)


def _parse_git_log_output(stdout: str) -> dict[str, GitFileStats]:
    """Parse git log output into per-file GitFileStats."""
    acc = _GitLogAccumulator()
    for block in stdout.split("COMMIT:"):
        lines = list(filter(None, (ln.strip() for ln in block.splitlines())))
        if len(lines) >= 2:
            acc.record_block(lines)
    return acc.to_stats()


def _import_node_modules(node: ast.AST) -> list[str]:
    """Extract imported module names from an Import or ImportFrom node."""
    if isinstance(node, ast.Import):
        return [a.name for a in node.names]
    if isinstance(node, ast.ImportFrom) and node.module and node.module != "__future__":
        return [node.module]
    return []


def _extract_module_imports(tree: ast.Module, internal_packages: set[str]) -> tuple[list[str], int]:
    """Return (sorted_internal_imports, mid_file_imports_count)."""
    nodes = list(ast.walk(tree))
    pairs = [(getattr(n, "lineno", 1), m) for n in nodes for m in _import_node_modules(n)]
    mid = sum(1 for ln, _ in pairs if ln > 60)
    internal = sorted({m for _, m in pairs if m.split(".")[0] in internal_packages})
    return internal, mid


def _detect_duplicate_blocks(tree: ast.Module) -> int:
    """Count repeated sequences of >= 6 normalized AST statements within a module."""
    windows: dict[tuple[str, ...], int] = defaultdict(int)
    bodies = [getattr(n, "body", None) for n in ast.walk(tree)]
    for body in (b for b in bodies if isinstance(b, list) and len(b) >= 6):
        dumped = [ast.dump(s, annotate_fields=True, include_attributes=False) for s in body if not isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]
        for i in range(max(0, len(dumped) - 5)):
            windows[tuple(dumped[i : i + 6])] += 1
    return sum(cnt - 1 for cnt in windows.values() if cnt > 1)


class ModuleAnalyzer:
    """Evaluates a Python module/file across AST units, duplicate blocks, imports, and git churn."""

    def __init__(
        self,
        repo_root: Path,
        internal_packages: set[str],
        config: RubricConfig,
        git_stats: dict[str, GitFileStats] | None,
        lang_override: str | None = None,
        framework_override: str | None = None,
    ) -> None:
        self.repo_root = repo_root.resolve()
        self.internal_packages = internal_packages
        self.cfg = config
        self.git_stats = git_stats
        self.lang_override = lang_override
        self.framework_override = framework_override

    def analyze(self, file_path: Path) -> FileReport:
        """Analyze a single Python, Java, or JavaScript file and return its FileReport."""
        resolved = file_path.resolve()
        rel_path = resolved.relative_to(self.repo_root).as_posix() if resolved.is_relative_to(self.repo_root) else resolved.name
        is_test = is_test_file_path(rel_path)
        gstat = self.git_stats.get(rel_path) if self.git_stats else None

        if resolved.suffix.lower() == ".java":
            return self._analyze_java(resolved, rel_path, is_test, gstat)
        if resolved.suffix.lower() in {".js", ".mjs", ".cjs"}:
            return self._analyze_javascript(resolved, rel_path, is_test, gstat)

        raw_text = resolved.read_text(encoding="utf-8", errors="replace")
        lines = raw_text.splitlines()
        tree = ast.parse(raw_text, filename=rel_path)

        if self._is_empty_init(resolved.name, tree, lines):
            return FileReport(rel_path, is_test, 0, [], 0, 0, gstat, DimensionScores.from_raw((100, 100, 100, 100, 100), self.cfg))

        classes, functions, non_exempt_cls = self._analyze_units(tree, lines, rel_path, is_test)
        loc = count_effective_loc(tree, lines)
        int_imports, mid_imports = _extract_module_imports(tree, self.internal_packages)
        dup_blocks = _detect_duplicate_blocks(tree)
        m_info = _ModuleMetrics(tree, loc, is_test, non_exempt_cls, len(functions), len(int_imports), mid_imports, dup_blocks, gstat)
        mod_scores, findings = self._score_module(m_info)
        scores = self._blend_scores(mod_scores, classes, functions)
        return FileReport(rel_path, is_test, loc, int_imports, dup_blocks, mid_imports, gstat, scores, findings, classes, functions)

    def _analyze_java(self, resolved: Path, rel_path: str, is_test: bool, gstat: GitFileStats | None) -> FileReport:
        from _code_health.ir_scorer import UniversalIRScorer
        from _code_health.java_parser import parse_java_file
        from _code_health.profiles import resolve_active_profiles

        ir_mod = parse_java_file(resolved, rel_path, is_test)
        profile = resolve_active_profiles(
            self.repo_root, resolved, lang_override=self.lang_override, framework_override=self.framework_override
        )
        scorer = UniversalIRScorer(self.cfg, profile)

        classes = [scorer.score_class(c, rel_path, is_test) for c in ir_mod.classes]
        functions = [scorer.score_function(f, rel_path, is_test) for f in ir_mod.functions]

        srp_pen, g_findings = self._score_git_srp(gstat) if gstat else (0.0, [])
        mod_loc_pen = round(max(0, min(ir_mod.loc, self.cfg.max_mid_file_loc) - self.cfg.max_ideal_file_loc) * 0.15 + max(0, ir_mod.loc - self.cfg.max_mid_file_loc) * 0.25, 1)
        p_loc, f_loc = penalty_item(mod_loc_pen, 1.0, f"Size: file LOC={ir_mod.loc} (>{self.cfg.max_ideal_file_loc})", cap=100.0)

        mod_scores = (100.0 - srp_pen, 100.0 - p_loc, 100.0)
        scores = self._blend_scores(mod_scores, classes, functions)
        return FileReport(rel_path, is_test, ir_mod.loc, [], 0, 0, gstat, scores, g_findings + f_loc, classes, functions)

    def _analyze_javascript(self, resolved: Path, rel_path: str, is_test: bool, gstat: GitFileStats | None) -> FileReport:
        from _code_health.ir_scorer import UniversalIRScorer
        from _code_health.js_parser import parse_javascript_file
        from _code_health.profiles import resolve_active_profiles

        ir_mod = parse_javascript_file(resolved, rel_path, is_test)
        profile = resolve_active_profiles(
            self.repo_root, resolved, lang_override=self.lang_override, framework_override=self.framework_override
        )
        scorer = UniversalIRScorer(self.cfg, profile)

        classes = [scorer.score_class(c, rel_path, is_test) for c in ir_mod.classes]
        functions = [scorer.score_function(f, rel_path, is_test) for f in ir_mod.functions]

        srp_pen, g_findings = self._score_git_srp(gstat) if gstat else (0.0, [])
        mod_loc_pen = round(max(0, min(ir_mod.loc, self.cfg.max_mid_file_loc) - self.cfg.max_ideal_file_loc) * 0.15 + max(0, ir_mod.loc - self.cfg.max_mid_file_loc) * 0.25, 1)
        p_loc, f_loc = penalty_item(mod_loc_pen, 1.0, f"Size: file LOC={ir_mod.loc} (>{self.cfg.max_ideal_file_loc})", cap=100.0)

        mod_scores = (100.0 - srp_pen, 100.0 - p_loc, 100.0)
        scores = self._blend_scores(mod_scores, classes, functions)
        return FileReport(rel_path, is_test, ir_mod.loc, [], 0, 0, gstat, scores, g_findings + f_loc, classes, functions)

    def _analyze_units(
        self, tree: ast.Module, lines: list[str], rel_path: str, is_test: bool
    ) -> tuple[list[ClassReport], list[FunctionReport], int]:
        scorer = UnitScorer(AnalysisContext(lines, rel_path, is_test, self.cfg))
        class_nodes = [n for n in tree.body if isinstance(n, ast.ClassDef)]
        classes = [scorer.analyze_class(n) for n in class_nodes]
        functions = [scorer.analyze_function(n) for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        non_exempt_cls = sum(1 for n in class_nodes if not has_exempt_base(n))
        return classes, functions, non_exempt_cls

    def _is_empty_init(self, name: str, tree: ast.Module, lines: list[str]) -> bool:
        doc = docstring_lines(tree)
        has_exec = any(getattr(n, "lineno", 0) not in doc for n in tree.body)
        return name == "__init__.py" and not has_exec and len(lines) <= 10

    def _score_module(self, m: _ModuleMetrics) -> tuple[tuple[float, float, float], list[str]]:
        srp, f_srp = self._score_module_srp(m)
        loc_pen = round(max(0, min(m.loc, self.cfg.max_mid_file_loc) - self.cfg.max_ideal_file_loc) * 0.15 + max(0, m.loc - self.cfg.max_mid_file_loc) * 0.25, 1)
        p_loc, f_loc = penalty_item(loc_pen, 1.0, f"Size: file LOC={m.loc} (>{self.cfg.max_ideal_file_loc})", cap=100.0)
        no_doc = int(not m.is_test) * int(ast.get_docstring(m.tree) is None)
        p_doc, f_doc = penalty_item(no_doc, 10.0, "Clean: missing module docstring")
        p_mid, f_mid = penalty_item(m.mid_imp, 4.0, f"Clean: {m.mid_imp} mid-file/late import(s)", cap=20.0)
        p_dup, f_dup = penalty_item(m.dup_blocks, 5.0, f"Clean: {m.dup_blocks} duplicate code block(s) detected", cap=25.0)
        return (srp, 100.0 - p_loc, 100.0 - p_doc - p_mid - p_dup), f_srp + f_loc + f_doc + f_mid + f_dup

    def _score_module_srp(self, m: _ModuleMetrics) -> tuple[float, list[str]]:
        src_mult = int(not m.is_test)
        p1, f1 = penalty_item((m.non_exempt_cls - 4) * src_mult, 3.0, f"SRP: {m.non_exempt_cls} non-model classes in single module")
        p2, f2 = penalty_item((m.fn_cnt - 15) * src_mult, 3.0, f"SRP: {m.fn_cnt} top-level functions in module (>15)")
        p3, f3 = penalty_item((m.imp_cnt - self.cfg.max_ideal_internal_imports) * src_mult, 5.0, f"SRP: imports {m.imp_cnt} internal modules (>{self.cfg.max_ideal_internal_imports})")
        g_pen, g_findings = self._score_git_srp(m.gstat) if m.gstat else (0.0, [])
        return 100.0 - p1 - p2 - p3 - g_pen, f1 + f2 + f3 + g_findings

    def _score_git_srp(self, gstat: GitFileStats) -> tuple[float, list[str]]:
        p1, f1 = penalty_item(gstat.commits - self.cfg.max_ideal_commits, 2.0, f"Git Churn: {gstat.commits} commits touching file (>{self.cfg.max_ideal_commits})", cap=25.0)
        p2, f2 = penalty_item(gstat.cochange_peers - 3, 3.0, f"Git Coupling: co-changes repeatedly with {gstat.cochange_peers} peer files", cap=15.0)
        p3, f3 = penalty_item(int(gstat.feat_commits >= 4), 10.0, f"Git Divergent Change: modified across {gstat.feat_commits} feature commits")
        return p1 + p2 + p3, f1 + f2 + f3

    def _blend_scores(
        self, mod_scores: tuple[float, float, float], classes: list[ClassReport], functions: list[FunctionReport]
    ) -> DimensionScores:
        units = [(max(1, c.loc), c.scores) for c in classes] + [(max(1, f.loc), f.scores) for f in functions]
        if not units:
            return DimensionScores.from_raw((mod_scores[0], mod_scores[1], 100.0, mod_scores[2], 100.0), self.cfg)
        total_w = sum(w for w, _ in units)
        u_srp = sum(w * s.srp for w, s in units) / total_w - (100.0 - mod_scores[0])
        u_size = sum(w * s.size for w, s in units) / total_w - (100.0 - mod_scores[1])
        u_comp = sum(w * s.complexity for w, s in units) / total_w
        u_clean = sum(w * s.clean for w, s in units) / total_w - (100.0 - mod_scores[2])
        u_sec = min(s.security for _, s in units)
        return DimensionScores.from_raw((u_srp, u_size, u_comp, u_clean, u_sec), self.cfg)
