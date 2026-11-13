# `py-code-health`

Deterministic multi-language code health analyzer for **Python**, **Java** (including **Spring Boot**), **TypeScript / TSX** (`.ts`, `.tsx`, `.mts`, `.cts`), **JavaScript / JSX** (`.js`, `.jsx`, `.mjs`, `.cjs`), and Web UI frameworks (**React**, **Next.js**, **Angular**).

Scores every **file**, **class**, and **function/method** on an objective `0–100` (`A–F`) rubric across five weighted dimensions:

1. **Single Responsibility & Cohesion (`30%`)** — Responsibility separation across concerns, dependency fan-out, class cohesion, and Git history churn signals.
2. **Size & Conciseness (`25%`)** — Function, class, and file length, parameter counts, and nesting depth.
3. **Complexity & Readability (`20%`)** — Control-flow branching, cognitive load, and early-exit structure.
4. **Clean Code & Idioms (`15%`)** — Static typing/documentation coverage, language idioms, error-handling discipline, and test assertion hygiene.
5. **Security & Operational Hygiene (`10%`)** — Static checks for unsafe dynamic execution, injection sinks, and framework boundary violations.

See [Scoring Rubric Reference](skills/code-health/references/scoring-rubric.md) for all formulas, thresholds, and penalties, and browse the refactoring playbooks in [`skills/code-health/references/`](skills/code-health/references/):
[Python](skills/code-health/references/python-playbook.md) ·
[Java](skills/code-health/references/java-playbook.md) ·
[Spring Boot](skills/code-health/references/java-spring-playbook.md) ·
[JavaScript](skills/code-health/references/javascript-playbook.md) ·
[TypeScript](skills/code-health/references/typescript-playbook.md) ·
[React](skills/code-health/references/react-playbook.md) ·
[Next.js](skills/code-health/references/nextjs-playbook.md) ·
[Angular](skills/code-health/references/angular-playbook.md)

---

## Language Support & Auto-Discovery

The analyzer automatically detects language and UI framework profiles from file extensions, syntax, imports, and manifests:
- **Python**: `.py` (Native Python stdlib `ast`, zero dependencies on Python 3.11+)
- **Java**: `.java` (Native Tree-Sitter CST via `tree-sitter-java`)
- **JavaScript / JSX**: `.js`, `.jsx`, `.mjs`, `.cjs` (Native Tree-Sitter CST via `tree-sitter-javascript`)
- **TypeScript / TSX**: `.ts`, `.tsx`, `.mts`, `.cts` (Native Tree-Sitter CST via `tree-sitter-typescript`)
- **Web UI Framework Profiles**: `--framework {auto,react,nextjs,angular,none}` with automatic detection from JSX/TSX syntax, framework imports (`react`, `next/*`, `@angular/*`), `'use client'` / `'use server'` directives, and `package.json` dependencies.

> [!NOTE]
> Minified JavaScript/ESM/CJS files (`*.min.js`, `*.min.mjs`, `*.min.cjs`, `*.bundle.js`) and generated bundle files with lines exceeding 1,000 characters are automatically skipped during discovery.

---

## Installation & Mandatory Native Parser Gate

Python analysis runs out of the box with zero external dependencies.

Analyzing Java or JavaScript requires their respective native Tree-Sitter parsers. There is **zero heuristic fallback**; missing dependencies immediately exit with code `2`:

```bash
# For JavaScript / JSX support:
uv pip install "tree-sitter>=0.23.0" "tree-sitter-javascript>=0.23.0"
# Or with pip:
pip install "tree-sitter>=0.23.0" "tree-sitter-javascript>=0.23.0"

# For TypeScript / TSX support:
uv pip install "tree-sitter>=0.23.0" "tree-sitter-typescript>=0.23.0"

# For Java support:
uv pip install "tree-sitter>=0.23.0" "tree-sitter-java>=0.23.0"
```

---

## Usage Examples

```bash
# Score an entire repository across all languages (auto-detected)
python scripts/code_health.py src tests

# Restrict scan to JavaScript or TypeScript
python scripts/code_health.py src --lang javascript --no-git
python scripts/code_health.py src --lang js --no-git
python scripts/code_health.py src --lang typescript --no-git
python scripts/code_health.py src --lang ts --no-git

# Force a Web UI framework profile (auto-detected by default)
python scripts/code_health.py src --framework react --no-git
python scripts/code_health.py src --framework nextjs --no-git
python scripts/code_health.py src --framework angular --no-git

# Fast agent iteration on a single file or symbol
python scripts/code_health.py src/services/auth.js --no-git
python scripts/code_health.py src/services/auth.js --symbol AuthService.login --no-git

# Quality-gate enforcement in CI (exits 1 if score < 90.0)
python scripts/code_health.py src --fail-under 90.0 --only-flagged

# Export JSON and Markdown scorecards
python scripts/code_health.py src tests --json-out scorecard.json --markdown-out REPORT.md
```

---

## Self-Health Check & Tests

```bash
# Verify repo code health score is >= 90.0 (Grade A)
python scripts/code_health.py scripts tests/unit/test_javascript_health.py --fail-under 90.0

# Run full test suite
pytest -v
```
