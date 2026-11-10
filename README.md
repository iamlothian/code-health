# `py-code-health`

Deterministic multi-language code health analyzer for **Python**, **Java** (including **Spring Boot**), and **Vanilla JavaScript** (`.js`, `.mjs`, `.cjs`).

Scores every **file**, **class**, and **function/method** on an objective `0–100` (`A–F`) rubric across five weighted dimensions:

1. **Single Responsibility & Cohesion (`30%`)** — Mixed I/O concern buckets, external call fan-out, class `LCOM4` connected components, internal module import fan-out, and Git history signals (churn, co-change coupling, and divergent change).
2. **Size & Conciseness (`25%`)** — Effective non-blank/non-comment/non-docstring LOC, parameter count (with entrypoint decorator exemptions), and nesting depth.
3. **Complexity & Readability (`20%`)** — Cyclomatic complexity (`CC`), cognitive complexity (`Cog`), and return statement count.
4. **Clean Code & Idioms (`15%`)** — Type annotations, JSDoc/docstrings, test assertion hygiene (`1–8` assertions per test), bare/swallowed `except`/`catch` handlers, legacy `var` declarations, loose equality coercion (`==`/`!=`), and `debugger;` statements.
5. **Security & Operational Hygiene (`10%`)** — Unsafe execution (`eval`, `new Function`, `exec`, `pickle`), string timers (`setTimeout`/`setInterval`), prototype mutation (`__proto__`, `setPrototypeOf`), `with` statements, SQL injection concatenation, and `subprocess` `shell=True`.

---

## Language Support & Auto-Discovery

The analyzer automatically detects language profiles from file extensions:
- **Python**: `.py` (Native Python stdlib `ast`, zero dependencies on Python 3.11+)
- **Java**: `.java` (Native Tree-Sitter CST via `tree-sitter-java`)
- **Vanilla JavaScript**: `.js`, `.mjs`, `.cjs` (Native Tree-Sitter CST via `tree-sitter-javascript`)

> [!NOTE]
> Minified JavaScript files (`*.min.js`) and generated bundle files with lines exceeding 1,000 characters are automatically skipped during discovery.

---

## Installation & Mandatory Native Parser Gate

Python analysis runs out of the box with zero external dependencies.

Analyzing Java or JavaScript requires their respective native Tree-Sitter parsers. There is **zero heuristic fallback**; missing dependencies immediately exit with code `2`:

```bash
# For JavaScript support:
uv pip install "tree-sitter>=0.23.0" "tree-sitter-javascript>=0.23.0"
# Or with pip:
pip install "tree-sitter>=0.23.0" "tree-sitter-javascript>=0.23.0"

# For Java support:
uv pip install "tree-sitter>=0.23.0" "tree-sitter-java>=0.23.0"
```

---

## Usage Examples

```bash
# Score an entire repository across all languages (auto-detected)
python scripts/code_health.py src tests

# Restrict scan to Vanilla JavaScript
python scripts/code_health.py src --lang javascript --no-git
# Or using the shorthand alias:
python scripts/code_health.py src --lang js --no-git

# Fast agent iteration on a single file or symbol
python scripts/code_health.py src/services/auth.js --no-git
python scripts/code_health.py src/services/auth.js --symbol AuthService.login --no-git

# Quality-gate enforcement in CI (exits 1 if score < 90.0)
python scripts/code_health.py src --fail-under 90.0 --only-flagged

# Export JSON and Markdown scorecards
python scripts/code_health.py src tests --json-out scorecard.json --markdown-out REPORT.md
```

---

## ECMAScript & JavaScript Code Health Rules

### Clean Code & Anti-Coercion
- **Parameter Defaults & JSDoc**: Parameter defaults (`param = default`) and JSDoc `@param {type}` infer typing with zero penalty. Untyped, un-defaulted parameters in non-test functions incur `-2.0 pts` each (capped at `-10.0 pts`).
- **Legacy `var`**: `-3.0 pts` per `var` declaration (capped at `-15.0 pts`). Prefer `const` or `let`.
- **Loose Equality (`==` / `!=`)**: `-2.0 pts` per comparison (capped at `-10.0 pts`). Implicit type coercion risk; prefer strict equality (`===` / `!==`).
- **Empty `catch` Block**: `-10.0 pts` per swallowed exception.
- **`debugger;` Statement**: `-10.0 pts` per occurrence.

### Security & Operational Hygiene
- **Dynamic Code Execution**: `eval(...)` and `new Function(...)` deduct `-40.0 pts`.
- **Implicit Timer Evaluation**: `setTimeout` or `setInterval` called with a string argument deducts `-20.0 pts`.
- **Prototype Mutation**: Direct `__proto__` mutation or `Object.setPrototypeOf` deducts `-25.0 pts`.
- **Scope Obscurity**: `with` statement deducts `-30.0 pts`.

### Test Suite & BDD Recognition
- Test blocks (`it(...)`, `test(...)`) inside `*.test.js`, `*.spec.js`, or `__tests__/` are extracted as test functions.
- Recognized assertion matchers include Node `assert`, Jest/Vitest `expect(...)` / `toBe(...)` / `toEqual(...)`, and Chai `should` / `equal`.
- Assertion hygiene: `0` assertions deducts `-30.0 pts`; `>8` assertions deducts `-3.0 pts` per assertion over 8.

---

## Self-Health Check & Tests

```bash
# Verify repo code health score is >= 90.0 (Grade A)
python scripts/code_health.py scripts tests/unit/test_javascript_health.py --fail-under 90.0

# Run full test suite
pytest -v
```
