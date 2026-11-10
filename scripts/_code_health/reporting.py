"""Console and Markdown formatters and codebase runner for Code Health Analyzer."""

from __future__ import annotations

from pathlib import Path

from _code_health.models import (
    GRADE_ORDER,
    IGNORED_SCAN_DIRS,
    ClassReport,
    CodebaseHealthReport,
    DimensionScores,
    FileReport,
    FunctionReport,
    RenderFilter,
    RubricConfig,
)
from _code_health.module_engine import ModuleAnalyzer, collect_git_stats


def _is_minified_or_bundled(path: Path) -> bool:
    """Return True if path is a minified or bundled JavaScript file."""
    name = path.name.lower()
    if name.endswith((".min.js", ".min.mjs", ".min.cjs")):
        return True
    if path.suffix.lower() in {".js", ".mjs", ".cjs"}:
        try:
            with path.open("r", encoding="utf-8", errors="replace") as f:
                for idx, line in enumerate(f):
                    if idx >= 50:
                        break
                    if len(line) > 1000:
                        return True
        except OSError:
            pass
    return False


class ScorecardFormatter:
    """Formats CodebaseHealthReport into console or Markdown output."""

    def __init__(self, flt: RenderFilter) -> None:
        self.flt = flt

    def matches(self, grade: str, findings: list[str], name: str, scope: str = "") -> bool:
        """Return True if an item satisfies the active RenderFilter."""
        sym_q = (self.flt.symbol or "").lower()
        need_flag = max(int(self.flt.only_flagged), int(scope == "func") * int(not self.flt.show_all_funcs))
        flag_ok = int(need_flag == 0) + int(grade not in {"A", "B"}) + len(findings)
        limit = GRADE_ORDER.get((self.flt.min_grade or "A").upper(), 5)
        checks = (sym_q in name.lower(), flag_ok > 0, GRADE_ORDER.get(grade, 0) <= limit)
        return all(checks)

    def render_console(self, report: CodebaseHealthReport) -> str:
        """Render console scorecard."""
        sc = report.scores
        lines = [
            "=" * 96,
            f"CODE HEALTH SCORECARD | Score: {sc.composite:.1f}/100 (Grade {sc.grade}) | "
            f"Files: {report.files_count} (src: {report.src_files_count}, test: {report.test_files_count}) | "
            f"Classes: {report.classes_count} | Functions/Methods: {report.functions_count}",
            f"Dimensions -> SRP: {sc.srp:.1f} | Size: {sc.size:.1f} | Complexity: {sc.complexity:.1f} | Clean: {sc.clean:.1f} | Security: {sc.security:.1f}",
            "=" * 96,
        ]
        if not self.flt.symbol:
            lines.extend(self._console_files(report.files))
        classes = [c for f in report.files for c in f.classes]
        funcs = [fn for f in report.files for fn in f.functions] + [m for c in classes for m in c.methods]
        lines.extend(self._console_classes(classes))
        lines.extend(self._console_functions(funcs))
        return "\n".join(lines) + "\n"

    def _console_files(self, files: list[FileReport]) -> list[str]:
        matched = [f for f in files if self.matches(f.scores.grade, f.findings, f.file_path)]
        lines = [
            "\n[FILES SCORECARD]",
            f"{'File':<46} {'Kind':<5} {'LOC':>5} {'Git':>4} {'SRP':>5} {'Size':>5} {'Comp':>5} {'Cln':>5} {'Sec':>5} {'Score':>6} {'Grd':>3}",
            "-" * 96,
        ]
        for f in matched:
            git_c = f.git.commits if f.git else "-"
            kind = ("src", "test")[int(f.is_test)]
            lines.append(
                f"{f.file_path:<46} {kind:<5} {f.loc:>5} {str(git_c):>4} "
                f"{f.scores.srp:>5.1f} {f.scores.size:>5.1f} {f.scores.complexity:>5.1f} "
                f"{f.scores.clean:>5.1f} {f.scores.security:>5.1f} {f.scores.composite:>6.1f} {f.scores.grade:>3}"
            )
            lines.extend(f"    - {item}" for item in f.findings)
        return lines

    def _console_classes(self, classes: list[ClassReport]) -> list[str]:
        matched = [
            c for c in sorted(classes, key=lambda x: (x.scores.composite, x.file_path, x.lineno))
            if self.matches(c.scores.grade, c.findings, f"{c.file_path}:{c.name}")
        ]
        if not matched:
            return []
        lines = [
            "\n[CLASSES SCORECARD]",
            f"{'Class (file:line)':<50} {'LOC':>5} {'Mth':>4} {'LCOM4':>5} {'CC':>4} {'Score':>6} {'Grd':>3}",
            "-" * 96,
        ]
        for c in matched:
            label = f"{c.file_path}:{c.lineno} {c.name}"[:50]
            lines.append(f"{label:<50} {c.loc:>5} {c.methods_count:>4} {c.lcom4:>5} {c.total_cc:>4} {c.scores.composite:>6.1f} {c.scores.grade:>3}")
            lines.extend(f"    - {item}" for item in c.findings)
        return lines

    def _console_functions(self, funcs: list[FunctionReport]) -> list[str]:
        matched = [
            fn for fn in sorted(funcs, key=lambda x: (x.scores.composite, x.file_path, x.lineno))
            if self.matches(fn.scores.grade, fn.findings, f"{fn.file_path}:{fn.qualname}", "func")
        ]
        if not matched:
            return []
        title = "\n[FUNCTIONS & METHODS SCORECARD]" if self.flt.show_all_funcs else "\n[FLAGGED FUNCTIONS & METHODS (Grade C/D/F or Findings)]"
        lines = [
            title,
            f"{'Symbol (file:line)':<52} {'LOC':>4} {'CC':>3} {'Cog':>4} {'Prm':>3} {'Nst':>3} {'Score':>6} {'Grd':>3}",
            "-" * 96,
        ]
        for fn in matched:
            label = f"{fn.file_path}:{fn.lineno} {fn.qualname}"[:52]
            lines.append(
                f"{label:<52} {fn.loc:>4} {fn.cyclomatic_complexity:>3} {fn.cognitive_complexity:>4} "
                f"{fn.params_count:>3} {fn.max_nesting:>3} {fn.scores.composite:>6.1f} {fn.scores.grade:>3}"
            )
            lines.extend(f"    - {item}" for item in fn.findings)
        return lines

    def render_markdown(self, report: CodebaseHealthReport) -> str:
        """Render Markdown scorecard summary."""
        sc = report.scores
        lines = [
            "# Deterministic Code Health Scorecard",
            "",
            f"- **Overall Score:** `{sc.composite:.1f} / 100` (**Grade {sc.grade}**)",
            f"- **Source (`src`) Score:** `{report.src_scores.composite:.1f} / 100` (**Grade {report.src_scores.grade}**)",
            f"- **Tests (`tests`) Score:** `{report.test_scores.composite:.1f} / 100` (**Grade {report.test_scores.grade}**)",
            f"- **Scope:** {report.files_count} files ({report.src_files_count} source, {report.test_files_count} test), {report.classes_count} classes, {report.functions_count} functions/methods",
            "",
            "## File Scorecard",
            "",
            "| File | Kind | LOC | Commits | SRP | Size | Complexity | Clean | Security | Score | Grade |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|:---:|",
        ]
        for f in report.files:
            if self.matches(f.scores.grade, f.findings, f.file_path):
                commits = str(f.git.commits) if f.git else "-"
                lines.append(
                    f"| `{f.file_path}` | {'test' if f.is_test else 'src'} | {f.loc} | {commits} | {f.scores.srp:.1f} | "
                    f"{f.scores.size:.1f} | {f.scores.complexity:.1f} | {f.scores.clean:.1f} | "
                    f"{f.scores.security:.1f} | **{f.scores.composite:.1f}** | **{f.scores.grade}** |"
                )
        return "\n".join(lines) + "\n"


class CodeHealthRunner:
    """Orchestrates file discovery, package inference, and codebase health aggregation."""

    def __init__(
        self,
        repo_root: Path | None = None,
        config: RubricConfig | None = None,
        git_mode: str = "git",
        lang_override: str | None = None,
        framework_override: str | None = None,
    ) -> None:
        self.repo_root = (repo_root or Path.cwd()).resolve()
        self.cfg = config or RubricConfig()
        self.use_git = git_mode != "no-git"
        self.lang_override = lang_override
        self.framework_override = framework_override

    def run(self, paths: list[Path]) -> CodebaseHealthReport:
        """Discover and analyze all Python, Java, and JavaScript files under paths."""
        py_files = self._discover_files(paths)
        pkgs = self._infer_packages(py_files)
        git_stats = collect_git_stats(self.repo_root) if self.use_git else None
        analyzer = ModuleAnalyzer(
            self.repo_root, pkgs, self.cfg, git_stats, self.lang_override, self.framework_override
        )
        reports = sorted((analyzer.analyze(f) for f in py_files), key=lambda r: (r.scores.composite, r.file_path))
        return self._build_report(paths, reports)

    def _discover_files(self, target_paths: list[Path]) -> list[Path]:
        resolved = [p.resolve() for p in target_paths]
        if self.lang_override == "python":
            valid_exts = {".py"}
        elif self.lang_override == "java":
            valid_exts = {".java"}
        elif self.lang_override in {"javascript", "js"}:
            valid_exts = {".js", ".mjs", ".cjs"}
        else:
            valid_exts = {".py", ".java", ".js", ".mjs", ".cjs"}
        direct = {r for r in resolved if r.is_file() and r.suffix.lower() in valid_exts}
        walked = {
            c.resolve() for r in resolved if r.is_dir()
            for ext in valid_exts for c in r.rglob(f"*{ext}")
            if not (IGNORED_SCAN_DIRS & set(c.parts))
        }
        all_candidates = direct | walked
        filtered = {f for f in all_candidates if not _is_minified_or_bundled(f)}
        return sorted(filtered, key=lambda x: x.as_posix())

    def _infer_packages(self, py_files: list[Path]) -> set[str]:
        pkgs = {f.parent.name for f in py_files if f.name == "__init__.py"}
        src_dir = self.repo_root / "src"
        if src_dir.is_dir():
            pkgs.update(c.name for c in src_dir.iterdir() if c.is_dir() and (c / "__init__.py").is_file())
        return pkgs - {"tests", "test", "docs", "scripts", "specs"}

    def _build_report(self, paths: list[Path], reports: list[FileReport]) -> CodebaseHealthReport:
        src_files = [f for f in reports if not f.is_test]
        test_files = [f for f in reports if f.is_test]
        classes = [c for f in reports for c in f.classes]
        funcs = [fn for f in reports for fn in f.functions] + [m for c in classes for m in c.methods]
        grades = {g: sum(1 for f in reports if f.scores.grade == g) for g in ("A", "B", "C", "D", "F")}
        return CodebaseHealthReport(
            [p.as_posix() for p in paths], len(reports), len(src_files), len(test_files), len(classes), len(funcs),
            self._aggregate(reports), self._aggregate(src_files), self._aggregate(test_files), grades, reports,
        )

    def _aggregate(self, files: list[FileReport]) -> DimensionScores:
        if not files:
            return DimensionScores.from_raw((100, 100, 100, 100, 100), self.cfg)
        weights = [max(5, f.loc) for f in files]
        total_w = sum(weights)
        raw = (
            sum(w * f.scores.srp for w, f in zip(weights, files)) / total_w,
            sum(w * f.scores.size for w, f in zip(weights, files)) / total_w,
            sum(w * f.scores.complexity for w, f in zip(weights, files)) / total_w,
            sum(w * f.scores.clean for w, f in zip(weights, files)) / total_w,
            sum(w * f.scores.security for w, f in zip(weights, files)) / total_w,
        )
        return DimensionScores.from_raw(raw, self.cfg)
