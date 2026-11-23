# Internal Module & Engine Contract: Multi-Language DRY Detection

**Date**: 2026-11-22  
**Feature**: `005-dry-metrics-support`  
**Spec**: [spec.md](../spec.md)

---

## 1. Module Dependency & Modularity Budget

All new and modified modules under `scripts/_code_health/` MUST satisfy `py-code-health`'s self-health quality gates:
- Functions `<= 25` effective LOC, cyclomatic complexity `CC <= 5`, parameters `<= 4`.
- Files `<= 350` effective LOC, internal module imports `<= 5`.
- Strict DAG (zero circular imports):

```text
dry_models.py (0 internal imports)
   ├── models.py (1: dry_models)
   ├── dry_tokens.py (2: dry_models, ir_models)
   ├── dry_type3.py (2: dry_models, models)
   └── dry_scoring.py (2: dry_models, models)
          └── dry_engine.py (5: dry_models, dry_tokens, dry_type3, dry_scoring, models)
                 ├── module_engine.py (5: ast_engine, dry_engine, ir_scorer, models, profiles)
                 └── reporting.py (3: dry_engine, models, module_engine)
```

---

## 2. Module Interface Signatures

### `scripts/_code_health/dry_tokens.py`
- `class TokenInterner(exclude_globs: tuple[str, ...] = ())`
  - `.exclude_globs: tuple[str, ...]`
  - `.intern(lexeme: str) -> int` (deterministic IDs starting at `16`).
- `is_generated_source(file_path: str, head_lines: list[str], annotations: tuple[str, ...] = (), exclude_globs: tuple[str, ...] = ()) -> bool`
- `extract_python_tokens(tree: ast.Module, raw_text: str, meta: PyTokenMeta, interner: TokenInterner) -> FileTokenStream | None`
- `extract_cst_tokens(root: Any, source_bytes: bytes, ir_mod: IRModule, interner: TokenInterner) -> FileTokenStream | None`

### Native Parser Contracts (`java_parser.py`, `js_parser.py`, `ts_parser.py`)
- `parse_java_file(file_path: Path, rel_path: str, is_test: bool, interner: Any = None) -> IRModule`
- `parse_javascript_file(file_path: Path, rel_path: str, is_test: bool, interner: Any = None) -> IRModule`
- `parse_typescript_file(file_path: Path, rel_path: str, is_test: bool, interner: Any = None) -> IRModule`
- Contract: when `interner is not None` and `not ir_mod.syntax_errors`, attach `ir_mod.token_stream = extract_cst_tokens(...)` inside the single parse pass; otherwise leave `token_stream = None`. Java/JS/TS parsers never retain the Tree-Sitter `tree` object on `IRModule`.

### `scripts/_code_health/dry_type3.py`
- `detect_block_type3_clones(streams: list[FileTokenStream], existing_matches: list[RawCloneMatch], config: RubricConfig) -> list[RawCloneMatch]`
- Invariants: compares only within `(stream.language, stream.is_test)`, collapses identical shingle sets before prefix indexing, caps posting lists at `MAX_POSTING = 64`, uses `difflib.SequenceMatcher(..., autojunk=False)`.

### `scripts/_code_health/dry_scoring.py`
- `cluster_and_score_clones(streams: list[FileTokenStream], matches: list[RawCloneMatch], config: RubricConfig) -> tuple[dict[str, FileDryMetrics], DrySummary]`
- `apply_dry_metrics(report: FileReport, dry: FileDryMetrics, cfg: RubricConfig) -> FileReport`

### `scripts/_code_health/dry_engine.py`
- `class DryAnalyzer(config: RubricConfig)`
  - `.analyze(streams: list[FileTokenStream]) -> tuple[dict[str, FileDryMetrics], DrySummary]`
- Facade re-exports for `module_engine.py` / `reporting.py` import-budget hygiene: `PyTokenMeta`, `TokenInterner`, `apply_dry_metrics`, `extract_python_tokens`.
- Bounds: `MAX_BUCKET = 64` in Winnowing index; diagonal deduplication `seen_diags[(fa, fb, pos_b - pos_a)] = end_a`; intra-file non-overlap guard `end_a <= start_b`.

### `scripts/_code_health/module_engine.py`
- `ModuleAnalyzer.analyze_with_stream(file_path: Path, interner: Any = None, run_local_dry: bool = True) -> tuple[FileReport, Any]`
- `ModuleAnalyzer.analyze(file_path: Path) -> FileReport`: delegates to `analyze_with_stream(file_path, TokenInterner(self.cfg.dry_exclude_globs), run_local_dry=True)[0]`.
- Immediately clears `ir_mod.token_stream = None` upon extraction so `IRModule` holds no extra memory.
