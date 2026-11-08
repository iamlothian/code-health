# Code Health Analyzer & Baseline Report Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a standalone, project-agnostic, deterministic Python Code Health Analyzer CLI (`scripts/code_health.py`) and generate the comprehensive repository scorecard (`docs/code-health-scorecard.json`) and architectural health report (`docs/CODE-HEALTH-REPORT.md`).

**Architecture:** `scripts/code_health.py` is a self-contained, zero-hard-dependency Python 3.11+ static & git history analyzer that parses Python ASTs, computes exact 0–100 scores across 5 dimensions (SRP & Cohesion, Size & Readability, Complexity, Clean Code, Security) for every method, class, and file, and renders scorecards to the console (Rich with plain-text fallback), JSON, or Markdown. It is accompanied by unit tests (`tests/unit/test_code_health.py`) and the full baseline report for `kb-spec`.

**Tech Stack:** Python 3.11+ standard library (`ast`, `tokenize`, `subprocess`, `pathlib`, `argparse`, `dataclasses`, `json`, `tomllib`), optional `rich` console tables, `pytest`.

**Spec:** `docs/superpowers/specs/2026-11-07-code-health-analyzer-design.md`

## Global Constraints

- **Project-Agnostic & Standalone:** `scripts/code_health.py` must NOT import anything from `kb` or hardcode `kb.*` package names. It must be directly extractable into a standalone plugin.
- **Zero Required External Dependencies:** Must run with Python 3.11+ stdlib alone; `rich` is imported via `try/except ImportError` with a clean plain-text table fallback.
- **No Production Code Changes:** Do NOT modify any file under `src/kb/` or existing test files under `tests/`.
- **Deterministic Scoring:** Composite score = `0.30 * SRP + 0.25 * Size + 0.20 * Complexity + 0.15 * Clean + 0.10 * Security`, clamped `[0.0, 100.0]`, graded `A` (`>=90`), `B` (`>=80`), `C` (`>=70`), `D` (`>=60`), `F` (`<60`).
- **Cross-Platform Path & Subprocess Safety:** Follow `GEMINI.md` rules (normalize backslashes, validate paths, pass explicit arg lists to `subprocess.run`).

## Review Focus

1. **Empty or comment-only `__init__.py` files:** Must score `100.0 (A)` across all dimensions without false-positive missing-docstring penalties.
2. **Stateless or 1–2 method classes (e.g., Pydantic models, custom Exceptions, Click/Typer command classes):** Must not be penalized for `LCOM4 > 1` when method count `<= 2` or when inheriting from `BaseModel` / `Exception` / `Enum`.
3. **Single-file or uncommitted file invocation outside git or with `--no-git`:** Must gracefully skip git history penalties and score `100.0` on the git sub-component rather than crashing or penalizing.
4. **Decorated CLI / MCP / route entrypoints (`@app.command`, `@mcp.tool`, etc.):** Must allow up to 6 parameters before size penalties and exempt CLI option boolean defaults from the boolean-trap SRP penalty.
5. **Windows path formatting in reports and CLI filters:** Paths in JSON/Markdown and `--symbol` / file path matching must normalize `\` to `/` so scores and outputs are identical across Windows and POSIX.

---

### Task 1: Core Data Models, Rubric Configuration, and AST Function/Method Analyzer

**Files:**
- Create: `scripts/code_health.py`
- Test: `tests/unit/test_code_health.py`

**Interfaces:**
- Produces in `scripts/code_health.py`:
  - `RubricConfig` dataclass (loads defaults or overrides from JSON/TOML dict)
  - `DimensionScores` dataclass (`srp: float`, `size: float`, `complexity: float`, `clean: float`, `security: float`, `composite: float`, `grade: str`)
  - `FunctionReport` dataclass (`name: str`, `qualname: str`, `file_path: str`, `lineno: int`, `end_lineno: int`, `loc: int`, `params_count: int`, `max_nesting: int`, `cyclomatic_complexity: int`, `cognitive_complexity: int`, `returns_count: int`, `concerns: list[str]`, `external_calls_count: int`, `is_test: bool`, `scores: DimensionScores`, `findings: list[str]`)
  - `score_to_grade(score: float) -> str`
  - `analyze_function_node(node: ast.FunctionDef | ast.AsyncFunctionDef, source_lines: list[str], file_path: str, is_test: bool, config: RubricConfig, class_name: str | None = None) -> FunctionReport`

- [ ] **Step 1: Write failing unit tests for function-level deterministic scoring in `tests/unit/test_code_health.py`**

```python
import ast
from pathlib import Path
import importlib.util

def _load_code_health():
    spec = importlib.util.spec_from_file_location(
        "code_health", Path(__file__).resolve().parents[2] / "scripts" / "code_health.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod

def test_clean_small_function_scores_grade_a():
    ch = _load_code_health()
    code = '''
def calculate_discount(price: float, rate: float) -> float:
    """Compute discounted price."""
    if rate <= 0:
        return price
    return price * (1.0 - rate)
'''
    tree = ast.parse(code)
    fn_node = tree.body[0]
    report = ch.analyze_function_node(
        fn_node, code.splitlines(), "src/pricing.py", is_test=False, config=ch.RubricConfig()
    )
    assert report.scores.grade == "A"
    assert report.scores.composite >= 95.0
    assert report.cyclomatic_complexity == 2
    assert report.findings == []

def test_bloated_complex_function_penalizes_srp_size_complexity_clean_security():
    ch = _load_code_health()
    body_lines = ['def mega_handler(raw_path, flag=True, a=1, b=2, c=3, d=4):']
    body_lines.append('    p = Path(raw_path)')
    body_lines.append('    p.write_text("dirty")')
    body_lines.append('    subprocess.run("git checkout " + raw_path, shell=True)')
    body_lines.append('    data = yaml.load(p.read_text())')
    body_lines.append('    console.print(data)')
    for i in range(55):
        body_lines.append(f'    if a == {i}:')
        body_lines.append('        if b > 0:')
        body_lines.append('            if c > 0:')
        body_lines.append('                if d > 0:')
        body_lines.append(f'                    print({i})')
    body_lines.append('    try:')
    body_lines.append('        pass')
    body_lines.append('    except Exception:')
    body_lines.append('        pass')
    code = "\n".join(body_lines)
    tree = ast.parse(code)
    report = ch.analyze_function_node(
        tree.body[0], code.splitlines(), "src/handler.py", is_test=False, config=ch.RubricConfig()
    )
    assert report.scores.grade == "F"
    assert report.scores.srp < 70.0
    assert report.scores.size < 50.0
    assert report.scores.complexity < 50.0
    assert report.scores.clean < 70.0
    assert report.scores.security < 60.0
    assert any("LOC=" in f for f in report.findings)
    assert any("shell=True" in f or "yaml.load" in f for f in report.findings)

def test_cli_decorated_entrypoint_exempts_boolean_defaults_and_allows_6_params():
    ch = _load_code_health()
    code = '''
@app.command("run")
def run_cmd(a: str, b: str, c: str, d: str, e: bool = False, f: bool = True) -> None:
    """CLI entrypoint."""
    return None
'''
    tree = ast.parse(code)
    report = ch.analyze_function_node(
        tree.body[0], code.splitlines(), "src/cli.py", is_test=False, config=ch.RubricConfig()
    )
    assert report.scores.size == 100.0
    assert not any("bool default" in f for f in report.findings)
```

- [ ] **Step 2: Run pytest to verify the tests fail**

Run: `uv run pytest tests/unit/test_code_health.py -v`
Expected: FAIL (`FileNotFoundError` for `scripts/code_health.py`)

- [ ] **Step 3: Implement `RubricConfig`, `DimensionScores`, `FunctionReport`, and `analyze_function_node` in `scripts/code_health.py`**

Implement the exact rubric formulas from Spec §4.1:
- Compute non-blank, non-comment, non-docstring `loc` inside the function span.
- Compute `cyclomatic_complexity`, `cognitive_complexity`, `max_nesting`, `returns_count`.
- Detect operational concerns (`presentation`, `cli_or_rpc_framework`, `filesystem_io`, `subprocess_git`, `serialization`, `domain_computation`), external call fan-out, and boolean trap parameters.
- Detect missing return/param type annotations, missing public docstrings, bare/swallowed `except Exception:`, test assertion counts (`0` or `>8`), and security boundary issues (`eval`/`exec`/`yaml.load`/`shell=True`, subprocess hygiene, path confinement without `.is_relative_to`/`.resolve`, git commands without `--` or hyphen checks, file writes before `checkout_branch`).

- [ ] **Step 4: Run pytest to verify Task 1 tests pass**

Run: `uv run pytest tests/unit/test_code_health.py -v`
Expected: PASS (3 passed)

---

### Task 2: Class Cohesion (LCOM4), File Aggregator, Duplicate Detection & Git History Analyzer

**Files:**
- Modify: `scripts/code_health.py`
- Test: `tests/unit/test_code_health.py`

**Interfaces:**
- Consumes: `RubricConfig`, `DimensionScores`, `FunctionReport`, `analyze_function_node`
- Produces in `scripts/code_health.py`:
  - `ClassReport` dataclass (`name: str`, `file_path: str`, `lineno: int`, `end_lineno: int`, `loc: int`, `methods_count: int`, `attrs_count: int`, `lcom4: int`, `total_cc: int`, `scores: DimensionScores`, `findings: list[str]`, `methods: list[FunctionReport]`)
  - `GitFileStats` dataclass (`commits: int`, `feat_commits: int`, `cochange_peers: int`, `avg_blast_radius: float`, `last_author: str`)
  - `FileReport` dataclass (`file_path: str`, `is_test: bool`, `loc: int`, `internal_imports: list[str]`, `duplicate_blocks: int`, `mid_file_imports: int`, `git: GitFileStats | None`, `scores: DimensionScores`, `findings: list[str]`, `classes: list[ClassReport]`, `functions: list[FunctionReport]`)
  - `compute_lcom4(class_node: ast.ClassDef) -> tuple[int, set[str]]`
  - `analyze_class_node(node: ast.ClassDef, source_lines: list[str], file_path: str, is_test: bool, config: RubricConfig) -> ClassReport`
  - `collect_git_stats(repo_root: Path) -> dict[str, GitFileStats]`
  - `analyze_file(file_path: Path, repo_root: Path, internal_packages: set[str], config: RubricConfig, git_stats: dict[str, GitFileStats] | None = None) -> FileReport`

- [ ] **Step 1: Add unit tests in `tests/unit/test_code_health.py` for LCOM4 class cohesion, model/exception exemptions, empty `__init__.py`, duplicate blocks, and file scoring**

```python
def test_lcom4_cohesive_vs_disconnected_class():
    ch = _load_code_health()
    cohesive_code = '''
class CohesiveService:
    """Single responsibility service."""
    def __init__(self, db: str) -> None:
        self.db = db
    def fetch(self, key: str) -> str:
        """Fetch item."""
        return f"{self.db}:{key}"
    def save(self, key: str, val: str) -> str:
        """Save item."""
        return self.fetch(key) + val
'''
    disconnected_code = '''
class DisconnectedGodClass:
    """Does two unrelated things."""
    def a1(self) -> int:
        """Group A1."""
        return self.x + 1
    def a2(self) -> int:
        """Group A2."""
        return self.x + 2
    def b1(self) -> str:
        """Group B1."""
        return self.y.strip()
    def b2(self) -> str:
        """Group B2."""
        return self.y.lower()
'''
    c_node = ast.parse(cohesive_code).body[0]
    d_node = ast.parse(disconnected_code).body[0]
    c_rep = ch.analyze_class_node(c_node, cohesive_code.splitlines(), "src/svc.py", False, ch.RubricConfig())
    d_rep = ch.analyze_class_node(d_node, disconnected_code.splitlines(), "src/god.py", False, ch.RubricConfig())
    assert c_rep.lcom4 == 1
    assert c_rep.scores.grade == "A"
    assert d_rep.lcom4 == 2
    assert d_rep.scores.srp < c_rep.scores.srp
    assert any("LCOM4=2" in f for f in d_rep.findings)

def test_empty_init_py_scores_100(tmp_path: Path):
    ch = _load_code_health()
    init_file = tmp_path / "src" / "pkg" / "__init__.py"
    init_file.parent.mkdir(parents=True)
    init_file.write_text('"""Package."""\n', encoding="utf-8")
    rep = ch.analyze_file(init_file, tmp_path, {"pkg"}, ch.RubricConfig(), git_stats=None)
    assert rep.scores.composite == 100.0
    assert rep.scores.grade == "A"
```

- [ ] **Step 2: Run pytest to verify the new tests fail**

Run: `uv run pytest tests/unit/test_code_health.py -v`
Expected: FAIL (`AttributeError: module 'code_health' has no attribute 'analyze_class_node'`)

- [ ] **Step 3: Implement `compute_lcom4`, `analyze_class_node`, `collect_git_stats`, and `analyze_file` in `scripts/code_health.py`**

Implement Spec §4.2 and §4.3:
- `compute_lcom4`: Build an undirected graph over non-dunder instance methods where edges connect methods sharing `self.<attr>` or calling `self.<method>()`. Count connected components via BFS. Exempt classes with `<= 2` methods or base classes matching `BaseModel`, `Exception`, `Error`, `Enum`, `TypedDict`, `NamedTuple`, `TyperGroup`, `TyperCommand`.
- `collect_git_stats`: Run `git log --no-merges --name-only --pretty=format:COMMIT:%H|%s` once at `repo_root` (if git is available and `--no-git` is not set), computing commit count, `feat` commit count, and co-change peers per `.py` file with normalized POSIX paths.
- `analyze_file`: Handle empty `__init__.py` as `100.0 (A)`, detect mid-file imports, detect duplicate statement windows (`>= 6` normalized AST lines), compute internal module fan-out, and combine module metrics (50%) with LOC-weighted child class/function scores (50%).

- [ ] **Step 4: Run pytest to verify Task 2 tests pass**

Run: `uv run pytest tests/unit/test_code_health.py -v`
Expected: PASS

---

### Task 3: Configurable CLI Runner, Console/JSON/Markdown Formatters & Self-Tests

**Files:**
- Modify: `scripts/code_health.py`
- Test: `tests/unit/test_code_health.py`

**Interfaces:**
- Consumes: `FileReport`, `ClassReport`, `FunctionReport`, `analyze_file`, `collect_git_stats`
- Produces in `scripts/code_health.py`:
  - `CodebaseHealthReport` dataclass (`target_paths: list[str]`, `files_count: int`, `src_files_count: int`, `test_files_count: int`, `classes_count: int`, `functions_count: int`, `scores: DimensionScores`, `src_scores: DimensionScores`, `test_scores: DimensionScores`, `grade_counts: dict[str, int]`, `files: list[FileReport]`)
  - `analyze_paths(paths: list[Path], repo_root: Path | None = None, use_git: bool = True, config: RubricConfig | None = None) -> CodebaseHealthReport`
  - `render_console(report: CodebaseHealthReport, only_flagged: bool = False, min_grade: str | None = None, symbol_filter: str | None = None) -> str`
  - `render_markdown(report: CodebaseHealthReport, only_flagged: bool = False, min_grade: str | None = None, symbol_filter: str | None = None) -> str`
  - `main(argv: list[str] | None = None) -> int`

- [ ] **Step 1: Add CLI and formatter unit tests in `tests/unit/test_code_health.py`**

```python
import json

def test_cli_single_file_and_folder_and_json_output(tmp_path: Path, capsys):
    ch = _load_code_health()
    pkg = tmp_path / "sample_pkg"
    pkg.mkdir()
    f1 = pkg / "mod.py"
    f1.write_text(
        '"""Sample module."""\n\ndef add(a: int, b: int) -> int:\n    """Add."""\n    return a + b\n',
        encoding="utf-8",
    )
    # 1. Single file console mode
    rc = ch.main([str(f1), "--no-git"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "mod.py" in out
    assert "add" in out

    # 2. Folder JSON mode + --json-out
    json_out = tmp_path / "scorecard.json"
    rc2 = ch.main([str(pkg), "--no-git", "--format", "json", "--json-out", str(json_out)])
    out2 = capsys.readouterr().out
    assert rc2 == 0
    data = json.loads(out2)
    assert data["files_count"] == 1
    assert json_out.is_file()

    # 3. --fail-under gate returns non-zero when threshold exceeds score
    rc3 = ch.main([str(f1), "--no-git", "--fail-under", "101.0"])
    assert rc3 == 1
```

- [ ] **Step 2: Run pytest to verify the CLI tests fail**

Run: `uv run pytest tests/unit/test_code_health.py -v`
Expected: FAIL (`AttributeError: module 'code_health' has no attribute 'main'`)

- [ ] **Step 3: Implement `analyze_paths`, `render_console`, `render_markdown`, `to_dict`, and `main` in `scripts/code_health.py`**

Support all CLI arguments from Spec §5:
- Positional `paths` (defaulting to auto-discovered `src`/`tests` or current directory)
- `--format console|json|markdown`
- `--only-flagged`, `--min-grade A|B|C|D|F`, `--symbol <substring>`, `--no-git`
- `--json-out <path>`, `--markdown-out <path>`, `--config <path>`, `--fail-under <float>`
- When a single file or `--symbol` is targeted in console mode, display all methods/functions in that scope along with their detailed penalty reasons so an agent gets immediate, granular feedback.

- [ ] **Step 4: Run pytest on `tests/unit/test_code_health.py` and run `scripts/code_health.py` on itself**

Run: `uv run pytest tests/unit/test_code_health.py -v`
Run: `uv run python scripts/code_health.py scripts/code_health.py --no-git`
Expected: All unit tests PASS, and `scripts/code_health.py` itself scores Grade `A` or `B` (`>= 85.0`) with clean modular functions.

---

### Task 4: Full Repository Scorecard Execution & Architectural Code Health Report (`docs/CODE-HEALTH-REPORT.md`)

**Files:**
- Create: `docs/code-health-scorecard.json`
- Create: `docs/CODE-HEALTH-REPORT.md`

**Interfaces:**
- Consumes: `scripts/code_health.py` CLI and JSON scorecard output

- [ ] **Step 1: Execute `scripts/code_health.py` across `src` and `tests` to generate `docs/code-health-scorecard.json`**

Run: `uv run python scripts/code_health.py src tests --json-out docs/code-health-scorecard.json`
Expected: Exit code 0, `docs/code-health-scorecard.json` created with deterministic scores for all 53 files, all classes, and all functions/methods.

- [ ] **Step 2: Write `docs/CODE-HEALTH-REPORT.md` combining the complete deterministic scorecards with deep-dive architectural, git-history, clean-code, OOP/SRP, and security analysis**

Include:
1. **Executive Summary & Repository Health Scorecard** (overall score, `src/` vs `tests/` breakdown, grade distributions, how agents/developers can run `scripts/code_health.py` on single files or folders).
2. **Deterministic Rubric Specification** (exact weights, equations, and thresholds).
3. **Git History & Evolutionary Hotspot Analysis** (commit churn table, co-change coupling analysis, Divergent Change in `cli.py`, `wizard.py`, `workspace.py`, `mcp_server.py`, and Shotgun Surgery across feature specs 001–012).
4. **Security & `GEMINI.md` Compliance Audit** (evaluation of `git_adapter.py`, `router.py`, `workspace.py`, `lifecycle.py`, `wizard.py`, `mcp_server.py`, `cli.py` against path traversal/confinement, hyphenated git arg injection, and branch-before-mutation rules, highlighting both compliant guards and any remaining gaps).
5. **Architectural & OOP / Single Responsibility Deep-Dives** (specific line-linked findings and concrete refactoring blueprints for the lowest-scoring files, classes, and functions in `src/kb/` and `tests/`).
6. **Complete Deterministic Scorecards** (every file, every class, and every method/function with exact dimension scores, composite score, grade, and penalty reasons).

- [ ] **Step 3: Run full test suite to verify nothing in the repository was broken**

Run: `uv run pytest`
Expected: All existing tests + new `tests/unit/test_code_health.py` pass.
