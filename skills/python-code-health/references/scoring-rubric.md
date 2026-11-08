# Deterministic Code Health Scoring Rubric & Reference Guide

This document defines the mathematical models, metric thresholds, penalty weights, and exemptions used by the deterministic Python Code Health Analyzer (`code_health.py`).

---

## 1. Core Principles

- **Deterministic & Reproducible:** Every function/method, class, and module receives a score from `0.0` to `100.0` and a letter grade calculated purely from AST structure, line tokens, and Git history. Scores never vary across identical code states.
- **Actionable Penalty Findings:** Every deducted point generates a descriptive finding string with line numbers and penalty values (e.g. `LOC=45 (>25) (-30.0 pts)`), showing agents exactly what to refactor.
- **Decoupled & Zero-Dependency:** Relies exclusively on Python 3.11+ standard library (`ast`, `dataclasses`, `subprocess`, `pathlib`, `tomllib`).

---

## 2. Composite Score Formula & Grade Scale

Every analyzed unit (function, class, file, or codebase) is evaluated across 5 weighted dimensions clamped to $[0.0, 100.0]$:

$$\text{Composite Score} = 0.30 \cdot S_{\text{SRP}} + 0.25 \cdot S_{\text{Size}} + 0.20 \cdot S_{\text{Complexity}} + 0.15 \cdot S_{\text{Clean}} + 0.10 \cdot S_{\text{Security}}$$

| Dimension | Weight | Primary Focus |
| :--- | :---: | :--- |
| **SRP & Cohesion ($S_{\text{SRP}}$)** | **30%** | Single responsibility, concern domain isolation, external call fan-out, boolean flag parameters, and class LCOM4. |
| **Size & Readability ($S_{\text{Size}}$)** | **25%** | Effective non-blank, non-comment lines of code (LOC), parameter count, and maximum nesting depth. |
| **Complexity & Control Flow ($S_{\text{Complexity}}$)** | **20%** | Cyclomatic complexity (CC), cognitive complexity (CogC), and return statement count. |
| **Clean Code & Maintainability ($S_{\text{Clean}}$)** | **15%** | Type annotations, docstrings, exception handling hygiene, and test assertion quality. |
| **Security & Operational Hygiene ($S_{\text{Security}}$)** | **10%** | Unsafe execution/deserialization, subprocess safety, path boundary confinement, and transactional Git mutations. |

### Letter Grade Scale

| Grade | Score Range | Description | Target Recommendation |
| :---: | :---: | :--- | :--- |
| **A** | **90.0 – 100.0** | **Healthy / Clean Code** | Excellent design; passes all strict quality gates. |
| **B** | **80.0 – 89.9** | **Good Quality** | Minor design smells; acceptable for production, minor cleanup recommended. |
| **C** | **70.0 – 79.9** | **Moderate Smell** | Multiple smells or high complexity; refactoring recommended before merge. |
| **D** | **60.0 – 69.9** | **Unhealthy / High Risk** | Significant architectural violations; refactoring required. |
| **F** | **< 60.0** | **Critical Hotspot** | Severe God-class, extreme bloat, or security risks; immediate refactoring needed. |

---

## 3. Function & Method Rubric

Starts at `100.0` in each dimension and applies deductions.

### 3.1 Single Responsibility & Cohesion ($S_{\text{SRP}}$, 30%)
*(Tests are exempt from SRP checks and score 100.0)*

1. **Concern Domain Mixing:**
   Functions are scanned for distinct operational concerns across 6 predefined buckets:
   - `presentation`: `print`, `console.print`, `err_console.print`, `typer.echo`, `click.echo`, `Table`, `Panel`, `Markdown`, `Confirm.ask`
   - `cli_or_rpc_framework`: `typer.Option`, `typer.Argument`, `typer.Exit`, `click.Context`, `FastMCP`
   - `filesystem_io`: `read_text`, `write_text`, `read_bytes`, `write_bytes`, `mkdir`, `unlink`, `rmdir`, `rglob`, `glob`, `iterdir`, `open`, `os.walk`, `shutil.*`
   - `subprocess_git`: `subprocess.run`, `subprocess.Popen`, `subprocess.check_output`, `shutil.which`, `checkout_branch`, `commit_all`, `create_pr_or_mr`
   - `serialization`: `yaml.safe_load`, `yaml.dump`, `json.loads`, `json.dumps`, `tomllib.loads`, `pickle.loads`
   - `domain_computation`: Pure algorithmic data transformations or AST visits.
   - **Penalty:** If distinct concerns > 2, deduct **-12.0 pts** per concern over 2:
     $$\text{Penalty} = (\text{concerns} - 2) \cdot 12.0$$

2. **External Call Fan-Out:**
   Counts distinct external non-stdlib function/method calls:
   - **Penalty:** If external calls > 6, deduct **-3.0 pts** per excess call (capped at -36.0 pts):
     $$\text{Penalty} = \min(36.0, (\text{ext\_calls} - 6) \cdot 3.0)$$

3. **Boolean Default Flag Parameters:**
   Functions taking boolean parameters with default values (e.g., `def run(flag: bool = True)`) often indicate violating SRP by executing two distinct branches.
   - *(CLI / RPC entrypoint decorators like `@app.command`, `@mcp.tool`, `@router.get` are exempt).*
   - **Penalty:** Deduct **-6.0 pts** per boolean default parameter:
     $$\text{Penalty} = N_{\text{bool\_defaults}} \cdot 6.0$$

---

### 3.2 Size & Readability ($S_{\text{Size}}$, 25%)

1. **Effective Lines of Code (LOC):**
   Calculated strictly on executable statements (excluding blanks, comments, and docstring spans).
   - **Source code (`src/`):**
     - Ideal: $\le 25$ LOC.
     - Between 26 and 50 LOC: **-1.5 pts / line**.
     - Above 50 LOC: **-2.5 pts / line**.
     $$\text{Penalty}_{\text{src}} = \max(0, \min(\text{LOC}, 50) - 25) \cdot 1.5 + \max(0, \text{LOC} - 50) \cdot 2.5$$
   - **Test code (`tests/`):**
     - Ideal: $\le 40$ LOC.
     - Between 41 and 75 LOC: **-1.0 pt / line**.
     - Above 75 LOC: **-2.0 pts / line**.
     $$\text{Penalty}_{\text{test}} = \max(0, \min(\text{LOC}, 75) - 40) \cdot 1.0 + \max(0, \text{LOC} - 75) \cdot 2.0$$

2. **Parameter Count ($N_{\text{params}}$, excluding `self` / `cls`):**
   - Standard functions: Ideal $\le 4$ parameters.
   - CLI/RPC entrypoint functions: Ideal $\le 6$ parameters.
   - **Penalty:** Deduct **-6.0 pts** per parameter exceeding the threshold:
     $$\text{Penalty} = (N_{\text{params}} - N_{\text{max}}) \cdot 6.0$$

3. **Max Nesting Depth ($D_{\text{nest}}$):**
   Depth of control flow structures (`if`, `for`, `while`, `try`, `with`, `match`).
   - Ideal: $\le 3$ levels.
   - **Penalty:** Deduct **-10.0 pts** per nesting level above 3:
     $$\text{Penalty} = \max(0, D_{\text{nest}} - 3) \cdot 10.0$$

---

### 3.3 Complexity & Control Flow ($S_{\text{Complexity}}$, 20%)

1. **Cyclomatic Complexity (CC):**
   Branches evaluated: `1 + count(If, For, AsyncFor, While, ExceptHandler, With, Assert [in src], Comprehension if, BoolOp values - 1, IfExp, MatchCase)`.
   - Ideal: $\le 5$.
   - Between 6 and 10 CC: **-4.0 pts / point**.
   - Above 10 CC: **-7.0 pts / point**.
   $$\text{Penalty} = \max(0, \min(\text{CC}, 10) - 5) \cdot 4.0 + \max(0, \text{CC} - 10) \cdot 7.0$$

2. **Cognitive Complexity (CogC):**
   Penalizes nested control structures by nesting depth ($+1 + \text{depth}$ for `if`/`for`/`while`/`except`/`match`), $+1$ for `elif`/`else`, and $+1$ for compound boolean chains.
   - Ideal: $\le 8$.
   - **Penalty:** Deduct **-2.5 pts** per point over 8:
     $$\text{Penalty} = \max(0, \text{CogC} - 8) \cdot 2.5$$

3. **Return Statement Count:**
   - Ideal: $\le 3$ return statements.
   - **Penalty:** Deduct **-4.0 pts** per return statement above 3:
     $$\text{Penalty} = \max(0, N_{\text{returns}} - 3) \cdot 4.0$$

---

### 3.4 Clean Code & Maintainability ($S_{\text{Clean}}$, 15%)

1. **Type Annotations (Source Code):**
   - Missing return type annotation (`-> None`, etc.): **-10.0 pts** (exempt for `__init__`, `__repr__`, etc.).
   - Untyped parameter (excluding `self`/`cls`): **-5.0 pts** each (capped at -25.0 pts).

2. **Docstring Presence (Source Code):**
   - Missing docstring on public function/method (does not start with `_`):
     - Functions $\le 10$ LOC: **-5.0 pts**.
     - Functions $> 10$ LOC: **-10.0 pts**.

3. **Exception Handling Hygiene:**
   - Bare `except:`: Deduct **-25.0 pts**.
   - Swallowed broad `except Exception:` (body contains only `pass`, `continue`, or immediate return): Deduct **-10.0 pts** per occurrence.

4. **Test Quality Signals (Tests Only):**
   - Test function (`test_*`) with `0` assertions: Deduct **-30.0 pts**.
   - Test function with $> 8$ assertions: Deduct **-3.0 pts** per assertion over 8 (capped at -30.0 pts).

---

### 3.5 Security & Boundary Hygiene ($S_{\text{Security}}$, 10%)
*(Tests score 100.0)*

1. **Unsafe Execution & Deserialization:**
   - Calls to `eval()`, `exec()`, `pickle.loads()`, `pickle.load()`: Deduct **-40.0 pts** each.
   - Unsafe `yaml.load()` without explicit `SafeLoader` or `yaml.safe_load`: Deduct **-40.0 pts**.
   - Subprocess calls with `shell=True`: Deduct **-40.0 pts**.

2. **Subprocess Argument Safety:**
   - Passing subprocess commands as raw concatenated strings instead of argument lists: Deduct **-15.0 pts**.

3. **Destructive Path Boundary Confinement:**
   - Accepting raw path arguments and invoking write/unlink operations without `.resolve()` or `.is_relative_to()` boundary check: Deduct **-15.0 pts**.

4. **Transactional Git Mutation Hygiene:**
   - Mutating files (`write_text`, `unlink`, `rmtree`) before checking out a Git branch within the same function: Deduct **-25.0 pts**.

---

## 4. Class Rubric

A class score blends its **class-level structural metrics (60%)** with the **mean score of its methods (40%)**:

$$\text{Class Dimension} = 0.60 \cdot S_{\text{structural}} + 0.40 \cdot \overline{S}_{\text{methods}}$$

*(Security dimension takes the minimum security score among its methods).*

### Structural Penalties:
1. **Lack of Cohesion of Methods (LCOM4):**
   - Undirected graph where nodes are instance methods, and edges connect methods that access common `self.<attr>` or call each other via `self.<method>()`.
   - Ideal: $\text{LCOM4} \le 1$.
   - **Penalty:** If class has $> 2$ methods and $\text{LCOM4} > 1$, deduct **-15.0 pts** per disconnected component over 1:
     $$\text{Penalty} = (\text{LCOM4} - 1) \cdot 15.0$$
2. **Method Count:** Ideal $\le 10$ methods. Deduct **-4.0 pts** per method over 10.
3. **Instance Attribute Count:** Ideal $\le 7$ distinct `self` attributes accessed. Deduct **-4.0 pts** per attribute over 7.
4. **Class LOC:** Ideal $\le 200$ LOC. Deduct **-0.4 pts** per line over 200.
5. **Total Class Cyclomatic Complexity ($\sum \text{CC}$):** Ideal $\le 25$. Deduct **-1.5 pts** per point over 25.
6. **Class Docstring:** Missing docstring on public class deducts **-15.0 pts** from Clean Code.

### Class LCOM4 Exemptions:
The following patterns are exempt from LCOM4 cohesion penalties:
- Data models inheriting from `BaseModel`, `dataclass`, `TypedDict`, `NamedTuple`.
- Enum classes (`Enum`, `StrEnum`, `IntEnum`).
- Exception classes inheriting from `Exception` or classes ending in `Error` / `Exception`.
- CLI command groups (`TyperGroup`, `TyperCommand`, `Protocol`).
- Small utility classes with $\le 2$ methods.

---

## 5. File / Module Rubric

A file score blends its **module-level architecture & Git metrics (50%)** with the **LOC-weighted average of all classes and functions in the file (50%)**:

$$\text{File Dimension} = 0.50 \cdot S_{\text{module}} + 0.50 \cdot \sum \left( \frac{\text{LOC}_u}{\text{LOC}_{\text{total}}} \cdot S_u \right)$$

### Module-Level Penalties:
1. **Multi-Class Bloat:** More than 4 non-exempt classes in a single source module: **-3.0 pts** per extra class.
2. **Top-Level Function Sprawl:** More than 15 top-level functions in a single source module: **-3.0 pts** per extra function.
3. **Internal Package Import Fan-Out:** More than 5 distinct internal package imports: **-5.0 pts** per dependency over 5.
4. **File LOC:**
   - Ideal: $\le 350$ LOC.
   - 351 to 600 LOC: **-0.15 pts / line**.
   - Above 600 LOC: **-0.25 pts / line**.
5. **Clean Code:**
   - Missing module docstring (source files): **-10.0 pts**.
   - Mid-file / late imports (imports after line 50 or inside functions, excluding `TYPE_CHECKING`): **-4.0 pts** each (capped at -20.0 pts).
   - Duplicate code blocks ($\ge 6$ identical AST statements repeated): **-5.0 pts** each (capped at -25.0 pts).
6. **Git History Signals (when Git is enabled):**
   - Commit Churn: $> 8$ commits touching the file deducts **-2.0 pts** per commit over 8 (capped at -25.0 pts).
   - Co-Change Coupling: Co-changes repeatedly with $\ge 3$ peer files deducts **-3.0 pts** per peer (capped at -15.0 pts).
   - Multi-Feature Churn: File touched across $\ge 4$ distinct `feat(...)` commits deducts **-10.0 pts**.
7. **Empty `__init__.py` Exemption:**
   - Files named `__init__.py` with no executable statements and $\le 10$ lines automatically receive **100.0 (Grade A)** across all dimensions.

