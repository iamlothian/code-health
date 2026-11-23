# CLI & Output Contract: Multi-Language Duplicate Code & DRY Metrics

**Date**: 2026-11-22  
**Feature**: `005-dry-metrics-support`  
**Spec**: [spec.md](../spec.md)

---

## 1. Command Line Interface (`scripts/code_health.py`)

```bash
python scripts/code_health.py [paths...] [options]
```

### Added / Extended Flags

| Flag | Argument | Description | Default |
| :--- | :--- | :--- | :--- |
| `--no-dry` | *(flag)* | Skip duplicate code & DRY detection (`dry_score=100.0`, `clone_groups_count=0`). | Enabled (`dry` mode) |
| `--config` | `PATH` | Optional JSON/TOML config; supports `dry_*` thresholds and `dry_exclude_globs` (JSON/TOML list automatically coerced to `tuple[str, ...]`). | `RubricConfig()` defaults |

### Exit Codes (Preserved)
- `0`: Analysis completed (and `scores.composite >= --fail-under` if specified).
- `1`: Quality gate failed (`scores.composite < --fail-under`).
- `2`: Missing mandatory native Tree-Sitter parser for targeted `.java`, `.js`/`.jsx`/`.mjs`/`.cjs`, or `.ts`/`.tsx`/`.mts`/`.cts` files.

---

## 2. Programmatic API Contract (`scripts/code_health.py` & `reporting.py`)

- `analyze_file(file_path, repo_root, internal_packages, config=None, **kwargs) -> FileReport`: runs full intra-file DRY detection and returns identical `FileReport` DRY fields/scores to a single-file `CodeHealthRunner.run([file_path])`.
- `analyze_paths(paths, repo_root=None, **kwargs) -> CodebaseHealthReport`: accepts `use_dry: bool = True` (maps to `dry_mode="dry" | "no-dry"`).
- `CodeHealthRunner(repo_root=None, config=None, git_mode="git", lang_override=None, framework_override=None, dry_mode="dry")`: runs single-pass streaming analysis across discovered files + codebase DRY clustering.
- Public exports in `code_health.__all__`: adds `"CloneGroup"`, `"CloneLocation"`, `"DrySummary"`.

---

## 3. JSON Output Schema Additions (`--format json` / `--json-out`)

Each `files[*]` entry includes (in addition to all existing fields):
```json
{
  "file_path": "src/service.py",
  "duplicate_blocks": 2,
  "duplicated_loc": 18,
  "duplication_ratio": 22.5,
  "dry_score": 83.7,
  "findings": [
    "Clean (DRY): Type-1 clone [DRY-001] at L10-L27 in 'process_a' duplicates src/worker.py:L14-L31 ('process_b') (-5.0 pts)",
    "Clean (DRY): duplication_ratio=22.5% (>10.0%) (-6.3 pts)"
  ]
}
```

Top-level `CodebaseHealthReport` JSON adds `"dry"`:
```json
{
  "dry": {
    "total_loc": 420,
    "duplicated_loc": 36,
    "duplication_ratio": 8.6,
    "dry_score": 96.4,
    "clone_groups_count": 1,
    "type1_groups": 1,
    "type2_groups": 0,
    "type3_groups": 0,
    "intra_file_groups": 0,
    "cross_file_groups": 1,
    "clone_groups": [
      {
        "group_id": "DRY-001",
        "clone_type": "type1",
        "scope": "cross_file",
        "similarity": 1.0,
        "tokens": 62,
        "loc": 18,
        "occurrences": [
          {"file_path": "src/service.py", "start_line": 10, "end_line": 27, "symbol": "process_a", "loc": 18, "token_count": 62},
          {"file_path": "src/worker.py", "start_line": 14, "end_line": 31, "symbol": "process_b", "loc": 18, "token_count": 62}
        ]
      }
    ]
  }
}
```

---

## 4. Console & Markdown Output Contracts

- **Console (`--format console`):**
  - When `report.dry.clone_groups_count == 0`: **no extra DRY summary section is emitted** — preserves existing duplicate-free scorecard output verbatim.
  - When `report.dry.clone_groups_count > 0`: renders a `[DUPLICATE CODE & DRY SUMMARY]` banner after `[FILES SCORECARD]` showing `Duplicated LOC`, `Duplication Ratio`, `DRY Score`, Type-1/2/3 & scope counts, and a compact clone-group table (`ID | Type | Sim | Scope | LOC | Locations`), while individual `Clean (DRY): ...` findings appear under `[FILES SCORECARD]`.
- **Markdown (`--format markdown` / `--markdown-out`):**
  - Always includes `- **DRY / Duplication:** ...` in the summary list when `clone_groups_count > 0` and renders a `## Duplicate Code & DRY Findings` Markdown table (`Group | Type | Similarity | Scope | LOC | Occurrences`).
