# Interface Contract: CLI & Tool Output

**Feature**: [spec.md](../spec.md) | **Date**: 2026-11-08

This document defines the CLI arguments, return codes, and structured output schemas for `scripts/code_health.py`.

---

## 1. CLI Arguments & Options

```text
usage: code_health [-h] [--format {console,json,markdown}] [--only-flagged]
                   [--min-grade {A,B,C,D,F}] [--symbol SYMBOL] [--no-git]
                   [--json-out JSON_OUT] [--markdown-out MARKDOWN_OUT]
                   [--config CONFIG] [--fail-under FAIL_UNDER]
                   [--lang {auto,python,java}]
                   [--framework {auto,spring-boot,python-cli-mcp,none}]
                   [paths ...]
```

### New Arguments

| Option | Values | Default | Description |
| :--- | :--- | :--- | :--- |
| `--lang` | `auto`, `python`, `java` | `auto` | Target programming language. When `auto`, detected from file extension. |
| `--framework` | `auto`, `spring-boot`, `python-cli-mcp`, `none` | `auto` | Framework profile to layer. When `auto`, inferred from build files or imports. |

---

## 2. Process Exit Codes

| Code | Meaning | Condition |
| :---: | :--- | :--- |
| `0` | **Success / Passed Quality Gate** | Analysis succeeded and composite score $\ge$ `--fail-under` (or `--fail-under` omitted). |
| `1` | **Quality Gate Failure** | Analysis succeeded, but composite score $<$ `--fail-under`. |
| `2` | **Missing Native Parser** | Target files require optional native parser packages (`tree-sitter` and `tree-sitter-java`) that are not installed. |
| `>2` | **Syntax or Execution Error** | Malformed input, unreadable files, or internal crash. |

---

## 3. Exit Code 2 Warning & Instructions Format

When exit code 2 is returned in human-readable mode (`--format console` or `markdown`):

```text
[WARNING] Native Java AST parser ('tree-sitter-java') is not installed.
To analyze Java files, install the native parser dependencies:
  • uv (ephemeral): uv run --with tree-sitter --with tree-sitter-java python scripts/code_health.py <paths>
  • uv (project):   uv pip install "tree-sitter>=0.23.0" "tree-sitter-java>=0.23.0"
  • pip:            pip install "py-code-health[java]"  (or: pip install tree-sitter tree-sitter-java)
```

In JSON mode (`--format json`):

```json
{
  "status": "missing_native_parser",
  "language": "java",
  "missing_packages": ["tree-sitter", "tree-sitter-java"],
  "install_commands": {
    "uv_ephemeral": "uv run --with tree-sitter --with tree-sitter-java python scripts/code_health.py",
    "uv_project": "uv pip install 'tree-sitter>=0.23.0' 'tree-sitter-java>=0.23.0'",
    "pip": "pip install 'py-code-health[java]'"
  },
  "message": "Native Java AST parser ('tree-sitter-java') is not installed."
}
```
