# Quickstart & Validation Guide: Multi-Language & Spring Boot Code Health

**Feature**: [spec.md](./spec.md) | **Date**: 2026-11-08

This guide outlines runnable scenarios to validate multi-language discovery, the mandatory native parser warning, and Spring Boot architectural checks.

---

## 1. Prerequisites

Run in Python 3.11+:
```bash
# Verify environment is clean
uv run python --version
```

---

## 2. Validation Scenarios

### Scenario 1: Python Backward Compatibility Gate
Ensure existing Python AST analysis continues to score Grade A without changes:
```bash
uv run python scripts/code_health.py tests/unit/test_code_health.py --no-git
```
**Expected Outcome**: Exits 0, renders Python unit test scorecard with Grade A (100.0).

---

### Scenario 2: Native Parser Warning & Prompt on Missing Dependencies
Test handling of Java files when `tree-sitter-java` is not installed:

1. **Attempt Java analysis in clean environment**:
   ```bash
   uv run python scripts/code_health.py path/to/MyService.java --no-git
   ```
   **Expected Outcome**: Exits with code `2`, prints warning banner with installation commands for `uv` and `pip`.

2. **Verify JSON machine-readable response**:
   ```bash
   uv run python scripts/code_health.py path/to/MyService.java --format json --no-git
   ```
   **Expected Outcome**: Exits 2, outputs valid JSON payload with `"status": "missing_native_parser"` and installation commands.

3. **Run Java analysis with `tree-sitter-java` installed**:
   ```bash
   uv run --with tree-sitter --with tree-sitter-java python scripts/code_health.py path/to/MyService.java --no-git
   ```
   **Expected Outcome**: Exits 0, parses full Java CST, displays scorecard with composite grade.

---

### Scenario 3: Spring Boot Anti-Pattern Detection
Analyze a sample Spring Boot controller declaring field injection and direct repository dependency:
```bash
uv run --with tree-sitter --with tree-sitter-java python scripts/code_health.py sample/UserController.java --no-git
```
**Expected Output Findings**:
- `Clean (Spring): @Autowired field injection detected on 'userRepository' (-8.0 pts)`
- `SRP (Spring): @RestController directly injects UserRepository (-20.0 pts)`
- Score reflects deductions across Clean Code and SRP dimensions.

---

### Scenario 4: Automated Test Suite & Self-Health Gate
Run all unit tests and verify self-health grade:
```bash
uv run pytest tests/unit/
uv run python scripts/code_health.py scripts tests --fail-under 90.0 --no-git
```
**Expected Outcome**: All unit tests pass, and self-health check scores $\ge 90.0$ (Grade A).
