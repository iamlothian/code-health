# Implementation Plan: Multi-Language Duplicate Code & DRY Metrics Support

**Branch**: `dry_metrics_support_plan` | **Date**: 2026-11-22 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/005-dry-metrics-support/spec.md`

---

## Summary

Extend `py-code-health` with deterministic, memory- and compute-efficient **Type-1 (exact)**, **Type-2 (parameterized / renamed)**, and **Type-3 (near-miss / gapped & scattered)** duplicate code detection—both **intra-file** and **cross-file**—across **Python**, **Java**, **JavaScript/JSX**, and **TypeScript/TSX**, accompanied by actionable per-file and codebase-wide DRY metrics.

Single-pass parsing extracts compact flat typed-array token streams (`array('I')` + `array('B')`, ~13 bytes/token) and immediately discards every AST/CST before cross-file analysis. Contiguous Type-1/2 clones and bounded-gap Type-3 clones (`<= 12` tokens) use 64-bit Mersenne Winnowing + diagonal-deduplicated extension + strict identifier bijection; function/method-level scattered Type-3 clones use deterministic SourcererCC frequency-ordered prefix filtering + ordered statement-hash `SequenceMatcher(autojunk=False)`. Subsumption, Union-Find clustering (`DRY-001..DRY-NNN`), and interval merging integrate DRY deductions into `Clean Code (15%)` alongside first-class `dry_score`, `duplication_ratio`, `duplicated_loc`, and `DrySummary` outputs, while automatically excluding standard generated code and keeping test cases self-contained via relaxed thresholds and `src`/`test` partition isolation.

---

## Technical Context

**Language/Version**: Python 3.11+ (Runtime and analyzer engine; Windows verification via Python 3.13 for prebuilt Tree-Sitter wheels)  
**Target Languages Evaluated**: Python (`.py`), Java (`.java`), JavaScript/JSX (`.js`, `.jsx`, `.mjs`, `.cjs`), TypeScript/TSX (`.ts`, `.tsx`, `.mts`, `.cts`)  
**Primary Dependencies**:
- Core DRY & Python analysis: Zero external dependencies (Python stdlib: `array`, `ast`, `bisect`, `collections`, `dataclasses`, `difflib`, `fnmatch`, `math`, `re`, `tokenize`).
- Optional native CST parsers (reused as-is): `tree-sitter>=0.23.0`, `tree-sitter-java>=0.23.0`, `tree-sitter-javascript>=0.23.0`, `tree-sitter-typescript>=0.23.0`.
**Storage**: File-based scorecards (`JSON`, `Markdown`, console stdout).  
**Testing**: `pytest>=8.0.0` unit, polyglot, performance/memory (`tracemalloc`), mirror parity, and 160-baseline regression tests; self-health gate via `scripts/code_health.py --fail-under 90.0`.  
**Target Platform**: Cross-platform (Windows, macOS, Linux).  
**Project Type**: Standalone CLI & Python library + bundled Antigravity skill (`skills/code-health/`).  
**Performance Goals**: `< 2.5s` wall-clock time on a 100-file (~15,000 LOC) multi-file corpus (`SC-004`).  
**Constraints**: `< 25 MB` peak `tracemalloc` memory allocation on 100-file (~15,000 LOC) scan; zero new PyPI dependencies; 100% deterministic outputs; every analyzer file `<= 350` LOC and `<= 5` internal imports (`Grade A >= 90.0`).  
**Scale/Scope**: Intra-file and cross-file Type-1/2/3 detection within `python`, `java`, and shared `ecmascript` (JS + TS) buckets, isolated across `src` vs. `test` partitions and calibrated empirically against all 160 baseline samples.

---

## Constitution Check

*GATE: Evaluated before Phase 0 research and re-checked after Phase 1 design.*

Note: `.specify/memory/constitution.md` in this repository is currently the unfilled template; gates below verify alignment against the repository's established engineering invariants (matching `specs/004-ui-framework-profiles/plan.md`):

| Invariant / Principle | Pre-Design | Post-Design | Notes |
| :--- | :---: | :---: | :--- |
| **I. Zero-Dependency Core & No New Extras** | **PASS** | **PASS** | Uses Python 3.11+ stdlib only; Java/JS/TS reuse existing Tree-Sitter packages with zero double-parsing. |
| **II. Bounded Memory & Deterministic Scaling** | **PASS** | **PASS** | Typed arrays (~13 B/tok), immediate AST/CST disposal, packed 64-bit Winnowing, bucket caps (`64`), and SourcererCC prefix filtering ensure deterministic `< 2.5s` / `< 25 MB` scaling. |
| **III. Deterministic CLI & Backward Compatibility** | **PASS** | **PASS** | Preserves 5-dimension `DimensionScores`, positional `FileReport`/`CodebaseHealthReport` args, clean duplicate-free console formatting, and adds `--no-dry` + config overrides. |
| **IV. Self-Health & Modularity (`>= 90.0`, `<= 350` LOC, `<= 5` imports)** | **PASS** | **PASS** | Splits DRY logic into 5 focused modules (`dry_models`, `dry_tokens`, `dry_type3`, `dry_scoring`, `dry_engine`) with facade re-exports keeping `dry_engine` (`5`), `module_engine` (`5`), `reporting` (`3`), `ts_parser` (`5`), and `code_health` (`5`) within import caps. |
| **V. Skill Parity, Baseline Integrity & Test-First** | **PASS** | **PASS** | Enforces byte-for-byte sync to `skills/code-health/scripts/`, updates rubric/playbooks cleanly (`README.md` free of penalty points), and empirically calibrates across all 160 baseline samples. |

---

## Project Structure

### Documentation (this feature)

```text
specs/005-dry-metrics-support/
├── spec.md                              # Feature specification (FR-001..FR-016, SC-001..SC-007, Q1..Q5, Brainstorm Log)
├── plan.md                              # This file (/speckit-plan output)
├── research.md                          # Phase 0: Data layout, Winnowing, SourcererCC, exclusions & calibration decisions
├── data-model.md                        # Phase 1: Public DRY models, slotted stream models, config & scoring rules
├── quickstart.md                        # Phase 1: End-to-end CLI, benchmark & self-health validation guide
├── contracts/                           # Phase 1: External & internal interface contracts
│   ├── cli-contract.md
│   └── dry-engine-contract.md
├── checklists/
│   └── requirements.md                  # Spec validation checklist (16/16 passing)
└── tasks.md                             # Phase 2 output (/speckit-tasks — not created by /speckit-plan)
```

*Companion TDD Task Plan:* [docs/superpowers/plans/2026-11-22-dry-metrics-support.md](../../docs/superpowers/plans/2026-11-22-dry-metrics-support.md)

### Source Code (repository root)

```text
scripts/
├── code_health.py                       # Add --no-dry flag, dry_exclude_globs coercion, analyze_paths(use_dry), exports
└── _code_health/
    ├── dry_models.py                    # [NEW] CloneLocation, CloneGroup, FileDryMetrics, DrySummary, slotted stream/match types
    ├── dry_tokens.py                    # [NEW] TokenInterner, is_generated_source, Python tokenize + shared CST token extractors
    ├── dry_type3.py                     # [NEW] Deterministic SourcererCC frequency-ordered prefix filter + statement LCS Type-3
    ├── dry_scoring.py                   # [NEW] Subsumption, Union-Find clustering (DRY-001..), symbol attribution & DRY scoring
    ├── dry_engine.py                    # [NEW] Winnowing index, diagonal-dedup extension, gap-stitching & DryAnalyzer facade
    ├── models.py                        # Add RubricConfig DRY fields, FileReport/CodebaseHealthReport DRY fields & re-exports
    ├── ir_models.py                     # Add IRModule.token_stream: Any = None
    ├── java_parser.py                   # Single-pass extract_cst_tokens hook via optional interner
    ├── js_parser.py                     # Single-pass extract_cst_tokens hook via optional interner
    ├── ts_parser.py                     # Single-pass extract_cst_tokens hook via optional interner
    ├── module_engine.py                 # Remove _detect_duplicate_blocks, add analyze_with_stream & local DRY parity
    └── reporting.py                     # CodeHealthRunner(dry_mode) streaming pass + conditional DRY summary in Console/Markdown

skills/code-health/
├── SKILL.md                             # Document --no-dry & DRY summary table
├── references/                          # Update scoring-rubric.md & all 8 language/framework playbooks
└── scripts/                             # Byte-for-byte mirror of scripts/

samples/<profile>/                       # Empirically calibrated .expected.json, manifest.json, SCORECARD_BASELINES.md (affected only)

tests/unit/
├── test_dry_models_and_tokens.py        # [NEW] Models, config defaults, extractors, generated-code filter tests
├── test_dry_engine.py                   # [NEW] Winnowing, bijection, gap-stitching, SourcererCC, clustering & scoring tests
└── test_dry_integration.py              # [NEW] CLI, formats, polyglot matrix, 100-file benchmark, determinism & mirror parity tests
```

**Structure Decision:** Decomposing the DRY subsystem into five small single-purpose modules (`dry_models.py`, `dry_tokens.py`, `dry_type3.py`, `dry_scoring.py`, `dry_engine.py`) with `dry_engine.py` and `models.py` acting as clean re-export facades guarantees a strict acyclic dependency graph, keeps every module comfortably under 350 LOC and at `<= 5` internal imports (`Grade A` self-health), and prevents any code duplication between `js_parser.py`, `ts_parser.py`, and `java_parser.py`.

---

## Complexity Tracking

*No constitutional violations identified. All new modules and modifications fit cleanly within `<= 350` LOC and `<= 5` internal imports without external runtime dependencies.*

---

## Design Artifacts

| Artifact | Purpose | Link |
| :--- | :--- | :--- |
| **Phase 0 Research** | Algorithm trade-offs, memory footprint & exclusion rationale | [research.md](./research.md) |
| **Data Model** | Entity schemas, typed-array encodings & penalty state machine | [data-model.md](./data-model.md) |
| **CLI & Output Contract** | Flags, config coercion, JSON/Console/Markdown output rules | [cli-contract.md](./contracts/cli-contract.md) |
| **Engine Contract** | Internal DAG, import budgets, parser & analyzer signatures | [dry-engine-contract.md](./contracts/dry-engine-contract.md) |
| **Quickstart Validation** | End-to-end verification scenarios, benchmark & self-health gates | [quickstart.md](./quickstart.md) |
| **TDD Task Plan** | Step-by-step executable plan with test assertions (8 tasks) | [2026-11-22-dry-metrics-support.md](../../docs/superpowers/plans/2026-11-22-dry-metrics-support.md) |
