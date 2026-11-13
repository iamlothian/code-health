# Quickstart & Validation Guide: Web UI Framework Code Health Profiles

**Date**: 2026-11-12  
**Feature**: Web UI Framework Code Health Profiles (`004-ui-framework-profiles`)  
**Spec**: [spec.md](./spec.md)

---

## Prerequisites

- Python 3.11+ (tested with Python 3.12 via `uv`)
- Existing optional grammar extras (no new packages required):
  ```powershell
  uv run --python 3.12 --with pytest --with tree-sitter --with tree-sitter-typescript --with tree-sitter-javascript --with tree-sitter-java pytest -q
  ```

---

## End-to-End Validation Scenarios

### 1. Run Full Automated Test Suite & Baseline Samples
```powershell
uv run --python 3.12 --with pytest --with tree-sitter --with tree-sitter-typescript --with tree-sitter-javascript --with tree-sitter-java pytest -v
```
Expected: All existing Python, Java, Spring Boot, JavaScript, and TypeScript tests pass alongside new `tests/unit/test_ui_framework_health.py` and updated `samples/manifest.json` baselines.

### 2. Validate React & Next.js Good vs. Bad Scorecards (TSX & JSX)
```powershell
uv run --python 3.12 --with tree-sitter --with tree-sitter-typescript python scripts/code_health.py samples/typescript-react/ --framework react --no-git
uv run --python 3.12 --with tree-sitter --with tree-sitter-typescript python scripts/code_health.py samples/typescript-nextjs/ --framework nextjs --no-git
```
Expected:
- Clean React/Next.js components (including components omitting explicit `: React.JSX.Element`) score **Grade A (`>= 90.0`)**.
- Smelly components with `dangerouslySetInnerHTML`, conditional `useEffect`, hook sprawl, `key={idx}`, or `"use client"` importing `next/headers` drop to **Grade D/F (`< 70.0`)** with exact line-numbered findings.

### 3. Validate Angular Layering & Subscription Hygiene
```powershell
uv run --python 3.12 --with tree-sitter --with tree-sitter-typescript python scripts/code_health.py samples/typescript-angular/ --framework angular --no-git
```
Expected:
- `@Component` injecting `HttpClient` directly and calling `.subscribe()` without teardown is penalized in SRP and Clean Code (`< 70.0`), while DI constructors and template-bound components incur no spurious docstring or LCOM4 penalties.

### 4. Validate Framework Isolation (`--framework none` & Non-UI TS)
```powershell
uv run --python 3.12 --with tree-sitter --with tree-sitter-typescript python scripts/code_health.py samples/typescript/ --framework auto --no-git
```
Expected: Pure TypeScript samples in `samples/typescript/` run without UI framework rules (`frameworks=[]`), and `--framework none` strips UI framework penalties from any UI file.

### 5. Self-Health Quality Gate
```powershell
uv run --python 3.12 --with tree-sitter --with tree-sitter-typescript --with tree-sitter-javascript --with tree-sitter-java python scripts/code_health.py scripts/ --fail-under 90.0 --no-git
```
Expected: Exit code `0`, every file in `scripts/_code_health/` scores `>= 90.0` (Grade A) and stays `< 350` LOC.
