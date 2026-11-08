# `py-code-health`

Standalone, zero-dependency deterministic Python AST and Git code health analyzer (`Python >= 3.11` stdlib only).

Scores every **file**, **class**, and **function/method** on a `0–100` (`A–F`) rubric across five weighted dimensions:

1. **Single Responsibility & Cohesion (`30%`)** — Mixed I/O concern buckets, external call fan-out, class `LCOM4` connected components, internal module import fan-out, and Git history signals (churn, co-change coupling, and divergent change).
2. **Size & Conciseness (`20%`)** — Effective non-blank/non-comment/non-docstring LOC, parameter count (with CLI entrypoint decorator exemptions), and nesting depth.
3. **Complexity & Readability (`25%`)** — Cyclomatic complexity (`CC`), cognitive complexity (`Cog`), and return statement count.
4. **Clean Code & Idioms (`15%`)** — Type annotations, public docstrings, test assertion hygiene (`1–8` assertions per test), bare/swallowed `except` handlers, mid-file imports, and duplicate AST blocks.
5. **Security & Operational Hygiene (`10%`)** — Unsafe execution/deserialization (`eval`, `exec`, `pickle`, `yaml.load`), `subprocess` `shell=True`, and transactional file-write vs branch-checkout ordering.

## Usage

```bash
# Score an entire repository (or specific folders/files) in console format
python scripts/code_health.py src tests

# Fast agent iteration on a single file or symbol (skipping git log)
python scripts/code_health.py path/to/file.py --no-git
python scripts/code_health.py path/to/file.py --symbol MyClass.my_method --no-git

# Show only flagged items or enforce a minimum score threshold in CI
python scripts/code_health.py src tests --only-flagged --fail-under 85.0

# Export JSON and Markdown scorecards
python scripts/code_health.py src tests --json-out scorecard.json --markdown-out REPORT.md
```

## Self-Health Check & Tests

```bash
python scripts/code_health.py scripts tests/unit/test_code_health.py --fail-under 100.0
pytest -v
```
