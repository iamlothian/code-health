# Quickstart & Validation Guide: TypeScript Language Profile

**Date**: 2026-11-09  
**Feature**: TypeScript Language Profile  
**Spec**: [spec.md](./spec.md)  
**Plan**: [plan.md](./plan.md)  

---

## 1. Prerequisites & Environment Setup

Verify the Python environment (Python >= 3.11):

```bash
# Ensure virtual environment is activated
.venv\Scripts\activate   # Windows
# or source .venv/bin/activate (macOS/Linux)

# Install TypeScript optional dependency
uv pip install tree-sitter tree-sitter-typescript
```

---

## 2. Validation Scenarios

### Scenario 1: Clean Modern TypeScript Module (Target: Grade A $\ge 90.0$)

Analyze a cohesive, well-typed TypeScript module with parameter typing, explicit return types, strict equality, and TSDoc documentation:

```bash
python scripts/code_health.py samples/typescript/clean_math_service.ts --no-git
```

**Expected Outcome**:
- Composite Score: $\ge 90.0$ (**Grade A**)
- 0 critical findings
- Method qualifying names properly extracted (`Calculator.add`, `formatResult`)
- Clean Code score $\ge 90.0$ with zero parameter typing or return type penalties.

---

### Scenario 2: Smell-Laden TypeScript Module (Target: Grade D/F with Line-Numbered Findings)

Analyze a smelly TypeScript file containing `any`, `@ts-ignore`, non-null assertions `!`, untyped parameters, missing return types, `var`, loose equality `==`, and `eval`:

```bash
python scripts/code_health.py samples/typescript/smelly_legacy_script.ts --no-git
```

**Expected Outcome**:
- Composite Score: $\le 65.0$ (**Grade D or F**)
- Clean Code findings:
  - `Clean (TS): explicit 'any' type usage(s) defeat type safety`
  - `Clean (TS): '@ts-ignore'/'@ts-nocheck' directive(s) suppress compiler checks`
  - `Clean (TS): non-null assertion(s) ('!') bypass strict null checks`
  - `Clean: untyped param(s)`
  - `Clean: missing return type annotation`
  - `Clean: legacy 'var' declaration(s) detected (prefer 'const' or 'let')`
  - `Clean: loose equality comparison(s) (==/!=) trigger implicit type coercion`
- Security findings:
  - `Security: dynamic code execution via eval`

---

### Scenario 3: Missing Parser Guard & Installation Guide (Target: Exit Code 2)

Simulate missing `tree-sitter-typescript` by running in an environment lacking `tree-sitter-typescript`:

```bash
# Console format
python scripts/code_health.py samples/typescript/clean_math_service.ts --no-git
# Exit code: 2
# Stderr outputs prominent banner with uv and pip commands

# JSON format
python scripts/code_health.py samples/typescript/clean_math_service.ts --format json
# Stdout outputs valid JSON with "status": "missing_native_parser"
```

---

### Scenario 4: Polyglot Codebase Scan

Scan mixed-language directories containing Python, Java, JavaScript, and TypeScript files:

```bash
python scripts/code_health.py samples/ --no-git
```

**Expected Outcome**:
- All `.py`, `.java`, `.js`, and `.ts` source files discovered.
- `node_modules`, `*.d.ts`, and `*.min.*` automatically skipped.
- Composite repository scorecard aggregates all languages.

---

### Scenario 5: Full Automated Test Suite

Run the full pytest suite covering unit tests and scorecard baselines:

```bash
pytest tests/unit/test_typescript_health.py -v
```

**Expected Outcome**:
- 100% of TypeScript tests pass.
- 100% of existing unit tests in `test_code_health.py`, `test_java_spring_health.py`, and `test_javascript_health.py` pass without regression.
