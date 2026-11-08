# Code Health Analyzer & Deterministic Scorecard — Design Specification

**Date:** 2026-11-07
**Status:** Draft (Pending Approval)
**Scope:** `scripts/code_health.py`, `docs/CODE-HEALTH-REPORT.md`, `docs/code-health-scorecard.json`, `tests/unit/test_code_health.py`

---

## 1. Intent & Why

We need a deterministic, repeatable way to evaluate and document the "code health" of the `kb-spec` Python source (`src/kb/`) and test (`tests/`) codebase across five core engineering pillars:
1. **Single Responsibility Principle (SRP) & Cohesion** — classes and methods should have one reason to change.
2. **Size & Readability** — avoiding large functions, God classes, and bloated modules so code stays easy to read and reason about.
3. **Complexity & Control Flow** — keeping branching and cognitive load low.
4. **Clean Code & Maintainability** — type safety, documentation, error handling hygiene, DRYness, and focused test assertions.
5. **Security & Boundary Hygiene** — enforcing subprocess safety, cross-platform path confinement, and transactional Git rules defined in `GEMINI.md`.

Critically, the analyzer must also serve as a **fast, iterative CLI tool for coding agents and developers**. When an agent writes or modifies a single file or folder, it can run `python scripts/code_health.py path/to/file.py` to immediately see the scorecard on the console, inspect exact penalty reasons for any low-scoring method or class, and refactor before committing.

---

## 2. Goals, Non-Goals, and Anti-Goals

### Goals
- **Standalone, Project-Agnostic Analyzer (`scripts/code_health.py`):**
  - 100% decoupled from `kb` or any target repository's domain/packages so it can be lifted directly into a standalone Antigravity plugin or skill later.
  - Zero hard external dependencies: uses strictly the Python 3.11+ standard library (`ast`, `tokenize`, `subprocess`, `pathlib`, `collections`, `dataclasses`, `argparse`, `json`, `sys`), with optional `rich` rendering if installed in the environment and a clean ANSI/ASCII table fallback when `rich` is absent.
  - Auto-detects project layout generically (e.g., classifying test files via `test_*.py`, `*_test.py`, `conftest.py`, or `/tests/` path segments; classifying internal vs external imports dynamically from scanned top-level package names rather than hardcoding `kb.*`).
- **Deterministic Rubric (0–100):** Every method/function, class, and file receives an exact, reproducible 0–100 composite score and letter grade (`A` 90–100, `B` 80–89, `C` 70–79, `D` 60–69, `F` <60) derived purely from AST analysis, token/line inspection, and `git log` history.
- **Fast Iterative Agent CLI (`scripts/code_health.py`):**
  - Accepts one or more target paths (a single `.py` file, a directory, or defaults to auto-discovered Python directories in cwd).
  - Outputs a scannable console scorecard by default (with `--format console|json|markdown` options).
  - Supports filtering (`--min-grade`, `--only-flagged`, `--symbol <name>`, `--no-git` for instant sub-second AST-only checks during tight inner-loop coding).
  - Supports exporting full Markdown (`--markdown-out`) and machine-readable JSON (`--json-out`) reports.
  - Supports a quality gate threshold (`--fail-under <score>`) and optional `--config <json>` to override thresholds or weights per project.
- **Comprehensive Baseline Report (`docs/CODE-HEALTH-REPORT.md` & `docs/code-health-scorecard.json`):**
  - Full baseline evaluation of all 17 source files (`src/kb/`) and 36 test files (`tests/`), every class, and every function/method.
  - Git history hotspot & co-change coupling analysis.
  - Security audit against cross-platform path confinement, subprocess safety, and transactional Git rules.
  - Deep-dive qualitative architectural review of the lowest-scoring hotspots with concrete refactoring roadmaps.

### Non-Goals
- **Refactoring production code in this phase:** We will **not** modify existing `src/kb/` or existing `tests/` files to fix code smells during this task.
- **Coupling to project packages or third-party linters:** `scripts/code_health.py` must never import from `kb` or require third-party packages to run (`python scripts/code_health.py` works in any bare Python 3.11+ environment).

### Anti-Goals
- **Non-deterministic LLM-guessed scores:** Scores must never vary between runs on the same code state.
- **Opaque penalties:** Every point deducted from a method, class, or file must produce a human- and agent-readable finding string (e.g., `LOC=118 (>25): -45.0 pts`, `LCOM4=4 (disconnected method groups): -20.0 pts`, `Broad except Exception at L49: -5.0 pts`) so an agent knows *exactly* what to fix.

---

## 3. Approaches Considered

1. **Approach 1: Hybrid Deterministic AST/Git Analyzer + Qualitative Architectural Audit (Selected)**
   - Build a zero-extra-dependency Python AST + `git log` analyzer (`scripts/code_health.py`) with configurable CLI flags for single-file/directory console output and full report generation, paired with a deep-dive architectural analysis in `docs/CODE-HEALTH-REPORT.md`.
   - *Trade-off:* Requires writing custom AST visitors for complexity, LCOM4 cohesion, responsibility fan-out, and `GEMINI.md` security checks, but gives 100% tailored, actionable diagnostics with zero new dependencies.
2. **Approach 2: Third-Party Static Analysis Pipeline (`radon` + `bandit` + `ruff`)**
   - Wrap external CLI tools.
   - *Rejected because:* Adds external dependencies, lacks LCOM4 class cohesion, responsibility mixing, and `GEMINI.md`-specific security checks.
3. **Approach 3: One-Off Scratch Script + Static Markdown Report**
   - *Rejected because:* Does not provide a reusable CLI tool for agents to iteratively check new or modified code.

---

## 4. Deterministic Scoring Rubric Specification

Every **Method/Function**, **Class**, and **File** is scored across 5 dimensions (each clamped to `[0.0, 100.0]`), combined via weighted average:

$$\text{Composite Score} = 0.30 \cdot S_{\text{SRP}} + 0.25 \cdot S_{\text{Size}} + 0.20 \cdot S_{\text{Complexity}} + 0.15 \cdot S_{\text{Clean}} + 0.10 \cdot S_{\text{Security}}$$

### Grade Scale
- **A (Healthy):** `90.0 – 100.0`
- **B (Good):** `80.0 – 89.9`
- **C (Moderate Smell):** `70.0 – 79.9`
- **D (Unhealthy / Refactor Recommended):** `60.0 – 69.9`
- **F (Critical Hotspot):** `< 60.0`

---

### 4.1 Method / Function Rubric (`src/` and `tests/`)

Starts at `100.0` in each dimension:

1. **Single Responsibility & Cohesion ($S_{\text{SRP}}$, 30%)**
   - **Responsibility Domain Mixing:** Each function is scanned for distinct operational concerns using generic AST heuristics (no project-specific symbol names):
     - `presentation` (`print`, `console.print`, `err_console`, `Table`, `Panel`, `Markdown`, `typer.echo`, `click.echo`, `logging`)
     - `cli_or_rpc_framework` (`typer.Option`, `typer.Argument`, `typer.Exit`, `click`, `@app.command`, `@mcp.tool`, `FastAPI`, `APIRouter`)
     - `filesystem_io` (`read_text`, `write_text`, `read_bytes`, `write_bytes`, `mkdir`, `unlink`, `shutil`, `os.walk`, `glob`, `rglob`, `open`, `tempfile`)
     - `subprocess_git` (`subprocess.run`, `subprocess.Popen`, `subprocess.check_output`, `shutil.which`, `.clone(`, `.checkout_branch(`, `.commit_all(`, `.push(`)
     - `serialization` (`yaml.safe_load`, `yaml.dump`, `json.loads`, `json.dumps`, `tomllib`, `pickle`, `csv`)
     - `domain_computation` (pure data transformation, regex/AST parsing, mathematical scoring, model validation)
     - Deduct **-12 pts** for each distinct concern beyond 2 inside a single function (in source files).
   - **Call Fan-Out:** Count distinct external functions/methods called (`N_calls`). If `N_calls > 6`, deduct **-3 pts** per call over 6 (max -36).
   - **Boolean Flag Parameters (SRP Smell):** Each `bool` parameter with a default value in source functions (excluding decorated CLI/MCP/route entrypoints) deducts **-6 pts** (signals a function doing two different things based on a flag).

2. **Size & Readability ($S_{\text{Size}}$, 25%)**
   - **Lines of Code (`LOC`, non-blank, non-comment, non-docstring physical span or statement span):**
     - Source (`src/`): Ideal `≤ 25` lines. For `26..50`: **-1.5 pts/line**. For `> 50`: **-2.5 pts/line**.
     - Tests (`tests/`): Ideal `≤ 40` lines. For `41..75`: **-1.0 pt/line**. For `> 75`: **-2.0 pts/line**.
   - **Parameter Count (`N_params`, excluding `self`/`cls`):**
     - Ideal `≤ 4` (or `≤ 6` for `@app.command` CLI entrypoints). Deduct **-6 pts** per parameter above threshold.
   - **Max Nesting Depth (`D_nest` of control structures `if/for/while/try/with/match`):**
     - Ideal `≤ 3`. Deduct **-10 pts** per nesting level above 3.

3. **Complexity & Control Flow ($S_{\text{Complexity}}$, 20%)**
   - **Cyclomatic Complexity (`CC`):** `1 + count(If, For, AsyncFor, While, ExceptHandler, With, Assert [in src], Comprehension-if, BoolOp values - 1, IfExp, MatchCase)`.
     - Ideal `≤ 5`. For `6..10`: **-4 pts** per point over 5. For `> 10`: **-7 pts** per point over 10.
   - **Cognitive Complexity (`CogC`):** Increments by `1 + current_nesting_depth` for each nested branching/looping construct (`if`, `for`, `while`, `except`, `match`), `+1` for `elif`/`else`, `+1` for each boolean operator sequence.
     - Ideal `≤ 8`. Deduct **-2.5 pts** per point over 8.
   - **Return Statement Count (`N_returns`):**
     - Ideal `≤ 3`. Deduct **-4 pts** per `return` over 3.

4. **Clean Code & Maintainability ($S_{\text{Clean}}$, 15%)**
   - **Type Annotation Coverage (in `src/`):**
     - Missing return type annotation: **-10 pts**.
     - Each untyped parameter (excluding `self`/`cls`): **-5 pts** (up to -25).
   - **Docstring Presence (in `src/`):**
     - Public function/method (`not name.startswith("_")`) missing docstring: **-10 pts** (or **-5 pts** if `LOC <= 10`).
   - **Exception Handling Hygiene:**
     - Bare `except:`: **-25 pts**.
     - `except Exception:` that swallows the error (`pass` or literal return without logging/re-raising/recording error): **-10 pts** per occurrence.
   - **Test Quality Signals (in `tests/` only):**
     - Test function (`test_*`) with `0` assertions (`assert`, `pytest.raises`, `pytest.warns`, helper `assert_*`): **-30 pts**.
     - Test function with `> 8` assertions (testing too many behaviors in one test): **-3 pts** per assertion over 8.

5. **Security & Boundary Hygiene ($S_{\text{Security}}$, 10%)**
   - **Unsafe Execution / Deserialization:** `eval()`, `exec()`, `yaml.load()` (without `SafeLoader`), `pickle.loads()`, `subprocess.*(..., shell=True)`: **-40 pts** each.
   - **Subprocess Hygiene:** `subprocess.run` / `Popen` call without `check=` or using string command instead of list args: **-15 pts**.
   - **Cross-Platform Path Confinement:**
     - Function accepts a raw path/string parameter and constructs `Path(...)` for destructive/write file I/O without boundary confinement (`.is_relative_to(...)`, `.resolve()`, or checking `startswith(("/", "\\"))` when validating relative paths): **-15 pts** (flagged as boundary review item).
   - **Git / CLI Argument Injection:**
     - Calling `git` subprocess commands (`checkout`, `clone`, `push`, `remote`, `fetch`) with variable arguments without hyphen validation (`startswith("-")`) or `--` positional separator: **-20 pts**.
   - **Transactional Git Lifecycle:**
     - Calling file-writing operations (`write_text`, `mkdir`, `unlink`) before branch checkout (`checkout` / `checkout_branch`) within the same workflow method: **-25 pts**.

---

### 4.2 Class Rubric

Starts at `100.0` in each dimension, combining class-level structural metrics (60%) with the mean of its methods' dimension scores (40%):

1. **Single Responsibility & Cohesion ($S_{\text{SRP}}$, 30%)**
   - **LCOM4 (Lack of Cohesion of Methods — Connected Components):**
     - Construct an undirected graph where nodes are non-dunder, non-property instance methods, and an edge exists between $m_1$ and $m_2$ if they access a common `self.<attr>` or one calls `self.<other>()`.
     - Ideal: `LCOM4 <= 1` (single cohesive component, or stateless utility class with ≤3 methods).
     - If `LCOM4 > 1` on a class with `> 2` methods: deduct **-15 pts** per extra disconnected component `(LCOM4 - 1) * 15`.
   - **Method Count (`N_methods`):**
     - Ideal `≤ 10` methods. Deduct **-4 pts** per method over 10.
   - **Instance Attribute Count (`N_attrs` accessed on `self`):**
     - Ideal `≤ 7`. Deduct **-4 pts** per attribute over 7.

2. **Size & Readability ($S_{\text{Size}}$, 25%)**
   - **Class LOC:** Ideal `≤ 200` lines. Deduct **-0.4 pts** per line over 200.
   - Plus 40% blend of child method Size scores.

3. **Complexity ($S_{\text{Complexity}}$, 20%)**
   - Total class Cyclomatic Complexity (`sum(method CC)`): Ideal `≤ 25`. Deduct **-1.5 pts** per point over 25.
   - Plus 40% blend of child method Complexity scores.

4. **Clean Code ($S_{\text{Clean}}$, 15%)**
   - Missing class docstring in `src/`: **-15 pts**.
   - Plus blend of child method Clean Code scores.

5. **Security ($S_{\text{Security}}$, 10%)**
   - Minimum/blend of child method Security scores.

---

### 4.3 File / Module Rubric

Combines module-level structural & git-history metrics (50%) with the LOC-weighted average of all top-level functions and classes in the file (50%):

1. **Single Responsibility & Git Churn Coupling ($S_{\text{SRP}}$, 30%)**
   - **Module Size / Multi-Class Bloat:** More than 3 non-Model/non-Exception classes or > 15 top-level functions in a source module: **-3 pts** per extra unit.
   - **Distinct Internal Module Imports (Fan-Out Coupling):** Automatically infers internal top-level package names from the scanned workspace (or `pyproject.toml`). Ideal `≤ 5` internal module imports. Deduct **-5 pts** per internal module dependency over 5 (identifies "God orchestrator" modules).
   - **Git History Signals (when git analysis is enabled):**
     - **Commit Churn (`N_commits` touching file):** Ideal `≤ 8`. Deduct **-2 pts** per commit over 8 (max -25).
     - **Co-Change Coupling (`N_cochange_peers` — distinct files changed in the same commit across ≥ 3 commits, or average commit blast radius):** High co-change coupling deducts up to **-15 pts**.
     - **Multi-Feature Churn:** Touching the same file across ≥ 4 distinct `feat(...)` commits (violating Open-Closed / Single Reason to Change): **-10 pts**.

2. **Size & Readability ($S_{\text{Size}}$, 25%)**
   - **File LOC:** Ideal `≤ 350` lines. For `351..600`: **-0.15 pts/line**. For `> 600`: **-0.25 pts/line**.
   - Plus weighted child Size scores.

3. **Complexity ($S_{\text{Complexity}}$, 20%)**
   - Weighted child Complexity scores + penalty if module top-level code has branching (`CC > 3`).

4. **Clean Code ($S_{\text{Clean}}$, 15%)**
   - Module docstring presence (`-10 pts` if missing in `src/`).
   - Mid-file imports (imports after line 50 or inside functions, excluding `TYPE_CHECKING`): **-4 pts** each.
   - Duplicate code blocks (≥ 6 identical normalized AST statement lines repeated within the file): **-5 pts** per duplicate block.

5. **Security ($S_{\text{Security}}$, 10%)**
   - Weighted/worst child Security score in the file.

---

## 5. CLI Interface & Agent Workflow Design (`scripts/code_health.py`)

```bash
# 1. Fast iterative check on a single file (console output, sub-second)
uv run python scripts/code_health.py src/kb/wizard.py

# 2. Check a specific symbol or only show items graded C/D/F
uv run python scripts/code_health.py src/kb/cli.py --only-flagged
uv run python scripts/code_health.py src/kb/wizard.py --symbol migrate_spec

# 3. Skip git log during rapid edit-check loops
uv run python scripts/code_health.py src/kb/search.py --no-git

# 4. Run on a folder or the entire repo and generate full reports
uv run python scripts/code_health.py src tests \
  --json-out docs/code-health-scorecard.json \
  --markdown-out docs/CODE-HEALTH-REPORT.md
```

### CLI Arguments
- `paths` (positional, zero or more, default: `["src", "tests"]`): Files or directories to analyze.
- `--format` (`console` | `json` | `markdown`, default: `console`): Primary stdout output format.
- `--only-flagged`: Only display files, classes, and methods scoring below grade `B` (`< 80.0`) or with explicit findings.
- `--min-grade` (`A`|`B`|`C`|`D`|`F`): Filter displayed symbols at or below a grade.
- `--symbol <substring>`: Filter output to classes/methods matching `<substring>` (with full penalty breakdown).
- `--no-git`: Skip `git log` history analysis for instant AST-only scoring on uncommitted/single files.
- `--json-out <path>`: Write the complete deterministic scorecard JSON to disk.
- `--markdown-out <path>`: Write the Markdown scorecard summary to disk.
- `--fail-under <float>`: Exit with code `1` if the overall or target composite score is below `<float>`.

### Console Output Structure
When run on a single file or directory in `console` mode:
1. **Overall Summary Banner:** Target scope, File count, Class count, Function/Method count, Overall Score & Grade, Dimension averages.
2. **Files Table:** Path, Kind (`src`/`test`), LOC, Git Commits, SRP, Size, Complexity, Clean, Security, Composite Score, Grade.
3. **Classes Table:** File, Class Name, LOC, Methods, LCOM4, Composite Score, Grade, Top Findings.
4. **Flagged / Worst Methods Table (or all methods when targeting a single file):** `file:line`, Symbol (`Class.method` or `func`), LOC, CC, CogC, Params, Nesting, Composite Score, Grade, and exact bulleted **Penalty Reasons** (so the agent knows precisely what to refactor).

---

## 6. Report Structure (`docs/CODE-HEALTH-REPORT.md`)

The comprehensive Markdown report will contain:
1. **Executive Summary & Repository Health Scorecard** (Overall score, `src/` vs `tests/` breakdown, grade distribution histograms).
2. **Deterministic Rubric Specification** (Exact formulas, weights, and penalty thresholds).
3. **Git History & Evolutionary Hotspot Analysis** (Commit churn ranking, co-change coupling matrix, "Shotgun Surgery" and "Divergent Change" smells evidenced by git history).
4. **Security & `GEMINI.md` Compliance Audit** (Subprocess safety, path traversal/confinement verification across all boundary entrypoints, transactional branch-before-mutation verification).
5. **OOP, Clean Code & Single Responsibility Deep-Dives** (Detailed architectural diagnosis of the top hotspots: `src/kb/cli.py`, `src/kb/wizard.py`, `src/kb/workspace.py`, `src/kb/mcp_server.py`, `src/kb/blueprints.py`, `src/kb/search.py`, and key test suites, with concrete refactoring blueprints).
6. **Complete Deterministic Scorecards:**
   - All 53 Files (17 source + 36 test) ranked by score.
   - All Classes ranked by score (with LCOM4 and method counts).
   - All Functions & Methods in `src/` and `tests/` with scores, grades, and findings.

---

## 7. Builder Decisions (Defaulted)
- **Test file `tests/unit/test_code_health.py`:** We will include unit tests for `scripts/code_health.py` to verify that deterministic scoring, LCOM4 calculation, cyclomatic/cognitive complexity, and CLI flags (`single file`, `directory`, `--json`, `--no-git`) work reliably.
- **Empty `__init__.py` handling:** Empty package marker files (`<= 5` lines with no executable statements) are graded `100.0 (A)` without penalizing for missing docstrings.
