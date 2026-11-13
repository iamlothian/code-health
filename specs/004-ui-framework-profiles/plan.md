# Implementation Plan: Web UI Framework Code Health Profiles

**Branch**: `evaluate_ui_frameworks` | **Date**: 2026-11-12 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/004-ui-framework-profiles/spec.md`

---

## Summary

Extend `py-code-health` with modular, pluggable **Web UI Framework Profiles** (`react`, `nextjs`, and `angular`) across **TypeScript** (`.ts`, `.tsx`, `.mts`, `.cts`) and **JavaScript** (`.js`, `.jsx`, `.mjs`, `.cjs`), while preserving strict isolation between raw language rules and framework concepts.

Parsers (`ts_parser.py` and `js_parser.py`, sharing a focused `ecmascript_ui.py` CST helper) extract only generic syntax primitives—decorators, module directives (`"use client"`, `"use server"`), imports, JSX element counts, branch/loop context on calls, and DOM/JSX attribute sinks—without embedding any framework names or rules. All UI concern mappings (`network_io`, `storage_io`, `dom_mutation`, `render_ui`, `presentation`), XSS sink rules, React Rules of Hooks / hook-sprawl / array-index-key checks, Next.js `app/` server-client boundary checks, and Angular DI layering / unmanaged `.subscribe()` / lifecycle exemption checks live exclusively inside `scripts/_code_health/profiles_ui.py` (`ReactFrameworkProfile`, `NextJsFrameworkProfile`, `AngularFrameworkProfile`).

`resolve_active_profiles()` dynamically composes per-file `LanguageProfile(..., frameworks=[...])` instances using cached `package.json` dependency detection and file imports (or `--framework` overrides), ensuring `--framework none` and non-UI backend/utility files run pure language rules only. Existing React-importing TSX baselines (`task_board_legacy.tsx`, `task_filter_bar.tsx`) will be relocated to dedicated React framework samples and replaced in `samples/typescript/` with pure, framework-free TypeScript samples.

---

## Technical Context

**Language/Version**: Python 3.11+ (Runtime and analyzer engine)  
**Target Languages Evaluated**: TypeScript (`.ts`, `.tsx`, `.mts`, `.cts`), JavaScript (`.js`, `.jsx`, `.mjs`, `.cjs`), plus existing Python (`.py`) and Java (`.java`)  
**Primary Dependencies**:
- Core analyzer: Zero external dependencies (Python stdlib: `ast`, `dataclasses`, `functools`, `json`, `pathlib`, `re`, `subprocess`, `tomllib`).
- Optional native TypeScript grammar extras: `tree-sitter>=0.23.0`, `tree-sitter-typescript>=0.23.0`.
- Optional native JavaScript grammar extras: `tree-sitter>=0.23.0`, `tree-sitter-javascript>=0.23.0` (natively parses `.jsx` syntax).
**Storage**: File-based reports (`JSON`, `Markdown`, console stdout).  
**Testing**: `pytest>=8.0.0` with CST fixtures and baseline scorecard pairs; self-health dogfooding via `scripts/code_health.py --fail-under 90.0`.  
**Target Platform**: Cross-platform (Windows, macOS, Linux).  
**Project Type**: Standalone CLI tool + Antigravity agent skill.  
**Performance Goals**: Sub-second CST parsing per file (<500ms); cached `package.json` lookup per repo root so multi-file scans remain <15s for 50 files in `--no-git` mode.  
**Constraints**: Zero new PyPI dependencies; strict isolation between raw language profiles/parsers and framework profiles; Grade A (`>= 90.0`) self-health and `< 350 LOC` for all new/modified Python modules in `scripts/_code_health/`; zero regressions on non-UI baselines.  
**Scale/Scope**: Phase 1 covers React, Next.js, and Angular across JS/TS (`Vue` `.vue` and `Svelte` `.svelte` SFCs deferred to Phase 2).

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Note: `.specify/memory/constitution.md` in this repository is currently the uncustomized template; gates below evaluate alignment against the repository's established architectural invariants (from `docs/specs/2026-11-07-code-health-analyzer-design.md` and `specs/001`–`003`):

| Invariant / Principle | Status | Notes |
|:---|:---:|:---|
| **I. Zero-Dependency Core & No New Extras** | **PASS** | Uses existing `tree-sitter-typescript` and `tree-sitter-javascript` (`language()` already parses JSX with zero errors). Core Python analysis remains stdlib-only. |
| **II. Strict Language vs. Framework Isolation** | **PASS** | Parsers emit generic CST facts only; raw `TypeScriptLanguageProfile` / `JavaScriptLanguageProfile` default to `frameworks=[]`; `profiles_ui.py` owns all UI rules and concern maps. |
| **III. Deterministic CLI & Native Parser Gate** | **PASS** | Extends `--framework` (`auto`, `react`, `nextjs`, `angular`, `spring-boot`, `none`), keeps `--lang` deterministic, preserves exit code `2` missing-parser contract. |
| **IV. Self-Health & Modularity (`>= 90.0`, `< 350 LOC`)** | **PASS** | Extracts shared ECMAScript UI CST helpers into `ecmascript_ui.py` and UI profiles into `profiles_ui.py` so `js_parser.py` shrinks below 350 LOC and all modules stay Grade A. |
| **V. Baseline Integrity & Test-First** | **PASS** | Relocates React-importing TSX baselines to `samples/typescript-react/` and replaces them with pure TS samples in `samples/typescript/` so baseline suites remain 100% honest and green. |

---

## Project Structure

### Documentation (this feature)

```text
specs/004-ui-framework-profiles/
├── spec.md              # Feature specification (with resolved Q1–Q5 & Brainstorm Log)
├── plan.md              # This file (/speckit-plan output)
├── research.md          # Phase 0: CST & isolation design research
├── data-model.md        # Phase 1: Generic IR primitives, FrameworkProfile hooks, rule matrix
├── quickstart.md        # Phase 1: End-to-end validation guide
├── contracts/           # Phase 1: CLI and FrameworkProfile contracts
│   ├── cli-contract.md
│   └── profile-contract.md
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2: Actionable tasks (/speckit-tasks output)
```

### Source Code (repository root)

```text
scripts/
├── code_health.py                       # Update --framework help/choices documentation
└── _code_health/
    ├── ir_models.py                     # Generic CST telemetry + FrameworkProfile hooks (return type, LCOM4, module eval)
    ├── ir_scorer.py                     # Honor profile hooks (LCOM4 exemptions, return type / ctor docstring exemptions)
    ├── ecmascript_ui.py                 # [NEW] Shared generic JS/TS CST helper (decorators, directives, JSX, HOC unwrap, sinks)
    ├── ts_parser.py                     # Wire decorators, directives, HOC unwrap, generic UI CST scan via ecmascript_ui
    ├── js_parser.py                     # Support .jsx, wire directives, HOC unwrap, generic UI CST scan; trim < 350 LOC
    ├── profiles_js.py                   # Compose frameworks in JavaScriptLanguageProfile.evaluate_function/class
    ├── profiles_ts.py                   # Compose frameworks in TypeScriptLanguageProfile.evaluate_function/class
    ├── profiles_ui.py                   # [NEW] ReactFrameworkProfile, NextJsFrameworkProfile, AngularFrameworkProfile, UI_CONCERN_MAP
    ├── profiles.py                      # Cached package.json + import framework detection & per-file composition
    ├── module_engine.py                 # Register .jsx, pass imports/directives to profiles & module-level framework rules
    └── reporting.py                     # Discover .jsx and skip *.min.jsx assets

samples/
├── manifest.json                        # Relocate React TSX pair; add pure TS replacement + React/Next.js/Angular pairs
├── SCORECARD_BASELINES.md               # Update baseline catalog
├── typescript/                          # Replace task_board_legacy.tsx / task_filter_bar.tsx with pure TS pair
├── typescript-react/                    # [NEW] Relocated task_board_legacy.tsx, task_filter_bar.tsx + React hooks/XSS pair
├── typescript-nextjs/                   # [NEW] Next.js App Router boundary good/bad pair
└── typescript-angular/                  # [NEW] Angular DI layering & subscription hygiene good/bad pair

tests/
└── unit/
    ├── test_language_scorecard_samples.py # Update manifest sample count assertion
    └── test_ui_framework_health.py        # [NEW] Auto-detection, isolation, React, Next.js, Angular, and .jsx tests
```

**Structure Decision**: Extracting shared ECMAScript CST logic into `ecmascript_ui.py` and UI framework rules into `profiles_ui.py` guarantees zero duplication between `js_parser.py` and `ts_parser.py`, keeps every module under 350 LOC (Grade A self-health), and maintains a strict architectural boundary between raw language parsing and framework rules.

---

## Complexity Tracking

*No constitutional violations identified. Extracting `ecmascript_ui.py` and `profiles_ui.py` reduces complexity and brings `js_parser.py` under the 350-LOC threshold.*
