# CLI Contract: JavaScript Language Support

**Date**: 2026-11-09  
**Feature**: Vanilla JavaScript (ECMAScript) Language Profile  
**Spec**: [spec.md](../spec.md)  

---

## 1. Command Line Interface

```bash
python scripts/code_health.py [paths...] [options]
```

### Options

| Flag | Argument | Description | Default |
|:---|:---|:---|:---|
| `--lang` | `auto`, `python`, `java`, `javascript`, `js` | Target programming language filter. | `auto` |
| `--format` | `console`, `json`, `markdown` | Standard output format. | `console` |
| `--no-git` | flag | Skip Git log churn and co-change coupling analysis. | `False` |
| `--fail-under` | `FLOAT` | Terminate with exit code 1 if composite score is below threshold. | `None` |
| `--symbol` | `STRING` | Filter class or function scorecards by qualifying name substring. | `None` |
| `--only-flagged` | flag | Display only units with findings or grade < B. | `False` |
| `--json-out` | `PATH` | Write full JSON scorecard to specified path. | `None` |
| `--markdown-out` | `PATH` | Write Markdown scorecard to specified path. | `None` |

---

## 2. Exit Codes

| Exit Code | Condition | Behavior |
|:---:|:---|:---|
| `0` | Success | Analysis completed and composite score satisfies `--fail-under` (or `--fail-under` not provided). |
| `1` | Quality Gate Failure | Analysis completed, but composite score is strictly below `--fail-under`. |
| `2` | Missing Native Parser | Optional parser packages (`tree-sitter` and `tree-sitter-javascript`) are not installed when targeting JavaScript. Outputs installation guidance. |

---

## 3. Missing Parser Output Contracts

### 3.1 Console Format (`--format console` or default)
Emitted to `stderr`:

```text
================================================================================
MISSING NATIVE PARSER: javascript
================================================================================
Full-fidelity AST code health analysis for JavaScript requires native parser packages:
  - tree-sitter
  - tree-sitter-javascript

Heuristic or fallback parsing is disabled to guarantee deterministic 100% AST accuracy.

To install dependencies, run:
  uv:   uv pip install tree-sitter tree-sitter-javascript
  pip:  pip install tree-sitter tree-sitter-javascript

Or install project extras:
  uv sync --extra javascript
================================================================================
```

### 3.2 JSON Format (`--format json`)
Emitted to `stdout` with exit code 2:

```json
{
  "status": "missing_native_parser",
  "language": "javascript",
  "missing_packages": [
    "tree-sitter",
    "tree-sitter-javascript"
  ],
  "install_commands": {
    "uv": "uv pip install tree-sitter tree-sitter-javascript",
    "pip": "pip install tree-sitter tree-sitter-javascript",
    "uv_extra": "uv sync --extra javascript"
  },
  "message": "Full-fidelity AST code health analysis for JavaScript requires native parser packages..."
}
```

---

## 4. File Discovery Contract

- **Included extensions**: `.js`, `.mjs`, `.cjs`
- **Automatically ignored directories**: `node_modules`, `dist`, `build`, `.next`, `.nuxt`, `coverage`, `venv`, `.venv`, `.git`
- **Minified asset skip**: Files ending with `*.min.js` or files whose first 50 lines include any line with $> 1{,}000$ characters are skipped with log notice: `Skipped minified asset: <path>`.
