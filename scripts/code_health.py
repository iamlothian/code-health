"""Standalone, project-agnostic deterministic Python Code Health Analyzer.

Evaluates Python files, classes, and functions/methods across five weighted dimensions:
  1. Single Responsibility & Cohesion (SRP) — 30%
  2. Size & Readability — 25%
  3. Complexity & Control Flow — 20%
  4. Clean Code & Maintainability — 15%
  5. Security & Boundary Hygiene — 10%
"""

from __future__ import annotations

import argparse
import ast
from dataclasses import asdict
import json
from pathlib import Path
import sys
import tomllib
from typing import Any

_SCRIPTS_DIR = str(Path(__file__).resolve().parent)
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from _code_health.ast_engine import UnitScorer, compute_lcom4, count_effective_loc  # noqa: E402
from _code_health.ir_models import MissingNativeParserError  # noqa: E402
from _code_health.models import (  # noqa: E402
    AnalysisContext,
    ClassReport,
    CodebaseHealthReport,
    DimensionScores,
    FileReport,
    FunctionReport,
    GitFileStats,
    RenderFilter,
    RubricConfig,
    clamp_score,
    score_to_grade,
)
from _code_health.module_engine import (  # noqa: E402
    ModuleAnalyzer,
    collect_git_stats,
    is_test_file_path,
)
from _code_health.reporting import CodeHealthRunner, ScorecardFormatter  # noqa: E402

__all__ = [
    "AnalysisContext",
    "ClassReport",
    "CodeHealthRunner",
    "CodebaseHealthReport",
    "DimensionScores",
    "FileReport",
    "FunctionReport",
    "GitFileStats",
    "RenderFilter",
    "RubricConfig",
    "ScorecardFormatter",
    "analyze_class_node",
    "analyze_file",
    "analyze_function_node",
    "analyze_paths",
    "clamp_score",
    "collect_git_stats",
    "compute_lcom4",
    "count_effective_loc",
    "is_test_file_path",
    "main",
    "score_to_grade",
]


def analyze_function_node(
    node: ast.FunctionDef | ast.AsyncFunctionDef, source_lines: list[str], file_path: str, is_test: bool, **kwargs: Any
) -> FunctionReport:
    """Analyze a single AST FunctionDef/AsyncFunctionDef and return its FunctionReport."""
    cfg = kwargs.get("config") or RubricConfig()
    ctx = AnalysisContext(source_lines, file_path.replace("\\", "/"), is_test, cfg, kwargs.get("class_name"))
    return UnitScorer(ctx).analyze_function(node)


def analyze_class_node(
    node: ast.ClassDef, source_lines: list[str], file_path: str, is_test: bool, *args: Any, **kwargs: Any
) -> ClassReport:
    """Analyze a single AST ClassDef and return its ClassReport."""
    cfg = (args[0] if args else kwargs.get("config")) or RubricConfig()
    ctx = AnalysisContext(source_lines, file_path.replace("\\", "/"), is_test, cfg)
    return UnitScorer(ctx).analyze_class(node)


def analyze_file(
    file_path: Path, repo_root: Path, internal_packages: set[str], config: RubricConfig | None = None, **kwargs: Any
) -> FileReport:
    """Analyze a Python file and return its FileReport."""
    return ModuleAnalyzer(repo_root, internal_packages, config or RubricConfig(), kwargs.get("git_stats")).analyze(file_path)


def analyze_paths(paths: list[Path], repo_root: Path | None = None, **kwargs: Any) -> CodebaseHealthReport:
    """Analyze target files or directories and return a CodebaseHealthReport."""
    git_mode = "git" if kwargs.get("use_git", True) else "no-git"
    return CodeHealthRunner(repo_root=repo_root, config=kwargs.get("config"), git_mode=git_mode).run(paths)


def _parse_config_text(raw: str, suffix: str) -> dict[str, Any]:
    """Parse raw config text from JSON or TOML."""
    if suffix == ".toml":
        return dict(tomllib.loads(raw).get("tool", {}).get("code_health", {}))
    return dict(json.loads(raw))


def _load_custom_config(config_path: Path | None) -> RubricConfig:
    """Load RubricConfig from optional JSON or TOML file."""
    if config_path is None or not config_path.is_file():
        return RubricConfig()
    data = _parse_config_text(config_path.read_text(encoding="utf-8"), config_path.suffix)
    valid = RubricConfig.__dataclass_fields__
    return RubricConfig(**dict(filter(lambda kv: kv[0] in valid, data.items())))


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="code_health", description="Standalone deterministic Python Code Health Analyzer.")
    parser.add_argument("paths", nargs="*", default=[], help="Target Python files or folders (default: src tests or cwd).")
    parser.add_argument("--format", choices=["console", "json", "markdown"], default="console", help="Stdout format.")
    parser.add_argument("--only-flagged", action="store_true", help="Only show items with findings or grade < B.")
    parser.add_argument("--min-grade", choices=["A", "B", "C", "D", "F"], default=None, help="Filter at or below grade.")
    parser.add_argument("--symbol", default=None, help="Filter classes/functions matching substring.")
    parser.add_argument("--no-git", action="store_true", help="Skip git log analysis for instant AST checks.")
    parser.add_argument("--json-out", type=Path, default=None, help="Write full JSON scorecard to path.")
    parser.add_argument("--markdown-out", type=Path, default=None, help="Write Markdown scorecard to path.")
    parser.add_argument("--config", type=Path, default=None, help="Optional JSON/TOML config file.")
    parser.add_argument("--fail-under", type=float, default=None, help="Exit 1 if score is below threshold.")
    parser.add_argument("--lang", choices=["auto", "python", "java", "javascript", "js", "typescript", "ts"], default="auto", help="Target language (default: auto).")
    parser.add_argument(
        "--framework",
        default="auto",
        help="Framework profile override: auto, react, nextjs, angular, spring-boot, none (default: auto).",
    )
    return parser


def _write_file_output(out_path: Path | None, content: str) -> None:
    """Write content to out_path if provided."""
    if out_path is not None:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content, encoding="utf-8")


def _emit_outputs(args: argparse.Namespace, report: CodebaseHealthReport) -> None:
    """Write optional file outputs and render requested stdout format."""
    show_all = report.files_count <= 2 or bool(args.symbol or args.min_grade)
    fmt = ScorecardFormatter(RenderFilter(args.only_flagged, args.min_grade, args.symbol, show_all))
    json_text = json.dumps(asdict(report), indent=2)
    md_text = fmt.render_markdown(report)
    _write_file_output(args.json_out, json_text)
    _write_file_output(args.markdown_out, md_text)
    out_map = {"json": json_text + "\n", "markdown": md_text, "console": fmt.render_console(report)}
    sys.stdout.write(out_map[args.format])


def _resolve_targets(raw_paths: list[str], cwd: Path) -> list[Path]:
    """Resolve target CLI paths or default to src/tests/cwd."""
    if raw_paths:
        return [Path(p) for p in raw_paths]
    defaults = [cwd / d for d in ("src", "tests") if (cwd / d).exists()]
    return defaults or [cwd]


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint for standalone code health analysis."""
    args = _build_arg_parser().parse_args(argv)
    cwd = Path.cwd()
    targets = _resolve_targets(args.paths, cwd)
    git_mode = "no-git" if args.no_git else "git"
    lang = None if args.lang == "auto" else args.lang
    framework = None if args.framework == "auto" else args.framework
    try:
        report = CodeHealthRunner(
            cwd,
            _load_custom_config(args.config),
            git_mode,
            lang_override=lang,
            framework_override=framework,
        ).run(targets)
    except MissingNativeParserError as err:
        if args.format == "json":
            payload = {
                "status": "missing_native_parser",
                "language": err.language,
                "missing_packages": err.missing_packages,
                "install_commands": getattr(err, "install_commands", {}),
                "message": str(err),
            }
            sys.stdout.write(json.dumps(payload, indent=2) + "\n")
        else:
            sys.stderr.write(str(err) + "\n")
        return 2
    _emit_outputs(args, report)
    return int(args.fail_under is not None and report.scores.composite < args.fail_under)


if __name__ == "__main__":
    raise SystemExit(main())
