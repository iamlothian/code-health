# Implementation Plan: TypeScript Language Profile

**Branch**: `add_typescript_support` | **Date**: 2026-11-09 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `specs/003-typescript-language-profile/spec.md`

---

## Summary

Extend `py-code-health` with a native TypeScript language profile using `tree-sitter-typescript` (supporting `.ts`, `.tsx`, `.mts`, and `.cts`). The engine parses source and TSX components into the language-neutral Universal Intermediate Representation (`IRModule`, `IRClass`, `IRFunction`) and deterministically scores them across all five weighted health dimensions (SRP, Size, Complexity, Clean Code, Security).

The profile enforces strict signature typing and surfaces type-safety escape hatches: penalizing untyped parameters (`-5.0 pts`), missing return types on functions (`-10.0 pts`), explicit `any` (`-5.0 pts`), `@ts-ignore`/`@ts-nocheck` compiler suppressions (`-10.0 pts`), and non-null assertions `!` (`-2.0 pts`). Pure contracts (`interface`, `type` aliases) contribute to LOC without triggering false class LCOM4 penalties, and constructor parameter properties are extracted as class fields to track cohesion accurately. Dynamic execution (`eval`, `new Function`), timer string evaluation, prototype tampering, and query string concatenation are flagged under Security. If optional parser dependencies are absent, the CLI terminates with exit code 2 and outputs copy-paste installation commands.

---

## Technical Context

**Language/Version**: Python 3.11+ (Runtime and analyzer engine)  
**Target Languages Evaluated**: Python (`.py`), Java (`.java`), JavaScript (`.js`, `.mjs`, `.cjs`), TypeScript (`.ts`, `.tsx`, `.mts`, `.cts`)  
**Primary Dependencies**:  
- Core analyzer: Zero external dependencies (Python stdlib: `ast`, `dataclasses`, `re`, `subprocess`, `pathlib`, `json`, `tomllib`).  
- Optional native Java grammar extras: `tree-sitter>=0.23.0`, `tree-sitter-java>=0.23.0`.  
- Optional native JavaScript grammar extras: `tree-sitter>=0.23.0`, `tree-sitter-javascript>=0.23.0`.  
- Optional native TypeScript grammar extras: `tree-sitter>=0.23.0`, `tree-sitter-typescript>=0.23.0`.  
**Storage**: File-based reports (`JSON`, `Markdown`, console stdout).  
**Testing**: `pytest>=8.0.0` with AST/CST fixtures; self-health dogfooding check via `code_health.py`.  
**Target Platform**: Cross-platform (Windows, macOS, Linux).  
**Project Type**: Standalone CLI tool + Antigravity agent skill.  
**Performance Goals**: Sub-second AST parsing per TypeScript file (<500ms); <15 seconds for a 50-file repository in `--no-git` mode.  
**Constraints**: Zero required external dependencies for core Python usage; fail-fast with exit code 2 if `tree-sitter-typescript` is missing; 100% backward compatibility for existing Python, Java, and JavaScript tests; Grade A self-health for all new/modified files in `scripts/_code_health/`.

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|:---|:---:|:---|
| **Principle I: Library-First** | **PASS** | TypeScript parsing and scoring are modularized into decoupled components (`ts_parser.py`, `profiles_ts.py`, `ir_scorer.py`, `module_engine.py`) with clean programmatic interfaces. |
| **Principle II: CLI Interface** | **PASS** | Exposes functionality via CLI (`--lang typescript`, `--lang ts`, auto-detection), supporting console, JSON, and markdown output formats, with exit code 2 on missing dependencies. |
| **Principle III: Test-First & Determinism** | **PASS** | TDD approach with comprehensive pytest unit tests covering clean TS, TSX, code smells, escape hatches, syntax errors, missing parser gates, and scorecard baseline comparisons. |
| **Principle IV: Backward Compatibility** | **PASS** | Python, Java, and JavaScript scoring pipelines, AST adapters, and CLI outputs remain 100% unaffected. |

---

## Project Structure

### Documentation (this feature)

```text
specs/003-typescript-language-profile/
├── spec.md              # Feature specification
├── plan.md              # Implementation plan (this file)
├── research.md          # Phase 0: Technology decisions & tradeoffs
├── data-model.md        # Phase 1: IR & Profile entity definitions
├── quickstart.md        # Phase 1: Validation and verification guide
├── contracts/           # Phase 1: CLI and Profile interfaces
│   ├── cli-contract.md
│   └── profile-contract.md
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2: Actionable tasks (/speckit-tasks output)
```

### Source Code (repository root)

```text
py-code-health/
├── pyproject.toml                         # Add optional [project.optional-dependencies] typescript
├── scripts/
│   ├── code_health.py                     # CLI entrypoint with updated --lang choices (typescript, ts)
│   └── _code_health/
│       ├── __init__.py
│       ├── models.py                      # Verify IGNORED_SCAN_DIRS and thresholds
│       ├── ir_models.py                   # IRFunction extended with TS telemetry fields
│       ├── profiles.py                    # Export TYPESCRIPT_PROFILE and auto-detection
│       ├── profiles_ts.py                 # TypeScriptLanguageProfile implementation
│       ├── ts_parser.py                   # Tree-sitter-typescript parser + TSX support + ParserGuard
│       ├── ir_scorer.py                   # UniversalIRScorer evaluation with TS profile
│       ├── module_engine.py               # Dispatcher for .ts/.tsx/.mts/.cts and Git stats
│       └── reporting.py                   # File discovery (.ts, .tsx, .mts, .cts) and declaration skips
├── samples/
│   └── typescript/                        # Baseline sample codebases (good vs bad)
│       ├── clean_math_service.ts
│       └── smelly_legacy_script.ts
└── tests/
    └── unit/
        ├── test_code_health.py            # Existing Python regression suite
        ├── test_java_spring_health.py     # Existing Java regression suite
        ├── test_javascript_health.py      # Existing JavaScript regression suite
        └── test_typescript_health.py      # New TypeScript unit & gate tests
```

**Structure Decision**: Introduces dedicated `ts_parser.py` and `profiles_ts.py` modules within `scripts/_code_health/`, preserving Grade A self-health by keeping all files under the 350-LOC threshold and isolating `tree-sitter-typescript`.

---

## Execution Strategy

### TDD Requirements

- **`scripts/_code_health/ts_parser.py`**: [TDD] CST extraction of functions, arrow functions, classes, methods, constructor parameter properties, parameter defaults/optionals, return types, TSX elements, and escape hatch counters (`any`, `@ts-ignore`, `!`).
- **`scripts/_code_health/profiles_ts.py`**: [TDD] Rule evaluations (strict typing, return type annotation, explicit `any`, `@ts-ignore`, non-null assertions `!`, SQL/query string concat, boolean flags, ECMAScript hygiene).
- **Missing Parser Guard**: [TDD] Verification of exit code 2, error banner, and structured JSON output when `tree-sitter-typescript` is absent.
- **File Discovery & Declaration Skip**: [TDD] Directory traversal discovering `.ts`, `.tsx`, `.mts`, `.cts` while skipping `*.d.ts` and `*.min.ts`.

### Parallel Execution Opportunities

- `ts_parser.py` and `profiles_ts.py` can be drafted and refined with mock IR fixtures.
- Test fixture samples (`samples/typescript/`) can be constructed in parallel with parser development.

### Human Checkpoints

1. **After Spec & Plan**: Confirm design artifacts and architecture (this checkpoint).
2. **After Parser & Profile Implementation**: Verify unit tests pass and clean TypeScript achieves Grade A.
3. **After Full Test Suite**: Run all existing tests plus new TypeScript tests before final branch completion.

### Review Gates

- **IR Extension Safety**: Verify `IRFunction` modifications default gracefully to preserve 100% Python/Java/JS compatibility.
- **Type Safety Deductions**: Verify `any`, `@ts-ignore`, non-null assertions, and query concatenation trigger exact expected penalties without false positives.

---

## Complexity Tracking

*No constitutional violations identified. No unjustified architectural complexity.*
