# Quickstart & Validation Guide: Vanilla JavaScript Language Profile

**Date**: 2026-11-09  
**Feature**: Vanilla JavaScript (ECMAScript) Language Profile  
**Spec**: [spec.md](./spec.md)  
**Plan**: [plan.md](./plan.md)  

---

## 1. Prerequisites & Environment Setup

Verify the Python environment (Python >= 3.11):

```bash
# Ensure virtual environment is activated
.venv\Scripts\activate   # Windows
# or source .venv/bin/activate (macOS/Linux)

# Install JavaScript optional dependency
uv pip install tree-sitter tree-sitter-javascript
```

---

## 2. Validation Scenarios

### Scenario 1: Clean Modern JavaScript Module (Target: Grade A $\ge 90.0$)

Analyze a cohesive, well-structured modern ECMAScript module with default parameters, strict equality, and JSDoc documentation:

```bash
python scripts/code_health.py samples/javascript/clean_math_service.js --no-git
```

**Expected Outcome**:
- Composite Score: $\ge 90.0$ (**Grade A**)
- 0 critical findings
- Function qualifying names properly extracted (`Calculator.add`, `formatResult`)
- Clean Code score $\ge 90.0$ with zero parameter typing penalties.

---

### Scenario 2: Smell-Laden JavaScript Module (Target: Grade D/F with Line-Numbered Findings)

Analyze a legacy/anti-pattern JavaScript file containing `var`, loose equality `==`, `eval`, string timers, `__proto__`, and `with`:

```bash
python scripts/code_health.py samples/javascript/smelly_legacy_script.js --no-git
```

**Expected Outcome**:
- Composite Score: $\le 65.0$ (**Grade D or F**)
- Clean Code findings:
  - `Clean: legacy 'var' declaration(s) detected (prefer 'const' or 'let')`
  - `Clean: loose equality comparison(s) (==/!=) trigger implicit type coercion`
  - `Clean: empty catch block swallows exception`
- Security findings:
  - `Security: dynamic code execution via eval`
  - `Security: string argument to setTimeout causes implicit code evaluation`
  - `Security: direct prototype mutation via '__proto__'`
  - `Security: 'with' statement obscures lexical scope`

---

### Scenario 3: Missing Parser Guard & Installation Guide (Target: Exit Code 2)

Simulate missing `tree-sitter-javascript` by overriding the import or running in a bare Python environment:

```bash
# Console format
python scripts/code_health.py samples/javascript/clean_math_service.js --no-git
# Exit code: 2
# Stderr outputs prominent banner with uv and pip commands

# JSON format
python scripts/code_health.py samples/javascript/clean_math_service.js --format json
# Stdout outputs valid JSON with "status": "missing_native_parser"
```

---

### Scenario 4: Polyglot Codebase Scan

Scan mixed-language directories containing Python, Java, and JavaScript files:

```bash
python scripts/code_health.py samples/ --no-git
```

**Expected Outcome**:
- All `.py`, `.java`, and `.js` source files discovered.
- `node_modules` and `*.min.js` automatically skipped.
- Composite repository scorecard aggregates all three languages.

---

### Scenario 5: Full Automated Test Suite

Run the full pytest suite covering unit tests and scorecard baselines:

```bash
pytest -v
```

**Expected Outcome**:
- 100% of existing Python and Java tests pass.
- All new JavaScript unit tests in `tests/unit/test_javascript_health.py` pass.
