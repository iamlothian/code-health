# CLI Contract: Web UI Framework Code Health Profiles

**Date**: 2026-11-12  
**Feature**: Web UI Framework Code Health Profiles (`004-ui-framework-profiles`)  
**Spec**: [spec.md](../spec.md)

---

## 1. Command Line Interface

```bash
python scripts/code_health.py [paths...] [options]
```

### Updated Flags

| Flag | Argument | Description | Default |
|:---|:---|:---|:---|
| `--lang` | `auto`, `python`, `java`, `javascript`, `js`, `typescript`, `ts` | Target programming language filter. | `auto` |
| `--framework` | `auto`, `react`, `nextjs`, `angular`, `spring-boot`, `none` | Framework profile override (`none` disables all framework rules). | `auto` |

---

## 2. File Discovery & Test Recognition Contract

### JavaScript Extensions (Updated)
- **Source extensions**: `.js`, `.jsx`, `.mjs`, `.cjs`
- **Test naming patterns**: `*.test.js`, `*.spec.js`, `*_test.js`, `*.test.jsx`, `*.spec.jsx`, `*_test.jsx`, `*.test.mjs`, `*.spec.mjs`, `*.test.cjs`, `*.spec.cjs`, `test_*.js`, `test_*.jsx`, or inside `test/`, `tests/`, `__tests__/`.
- **Skipped minified assets**: `*.min.js`, `*.min.jsx`, `*.min.mjs`, `*.min.cjs`, or lines `> 1000` chars in first 50 lines.

### TypeScript Extensions (Preserved)
- **Source extensions**: `.ts`, `.tsx`, `.mts`, `.cts`
- **Skipped declarations & minified**: `*.d.ts`, `*.d.mts`, `*.d.cts`, `*.min.ts`, `*.min.tsx`, `*.min.mts`, `*.min.cts`.

---

## 3. Native Parser Gate (Exit Code 2)

- Targeting `.jsx` files uses `tree-sitter-javascript` (`MissingNativeParserError("javascript", ["tree-sitter", "tree-sitter-javascript"])` if absent).
- Targeting `.ts`/`.tsx` files uses `tree-sitter-typescript` (`MissingNativeParserError("typescript", ["tree-sitter", "tree-sitter-typescript"])` if absent).
- Zero new PyPI packages are introduced; core Python analysis remains zero-dependency.
