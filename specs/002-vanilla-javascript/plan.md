# Implementation Plan: Vanilla JavaScript (ECMAScript) Language Profile

**Branch**: `add_vanilla_javascript` | **Date**: 2026-11-09 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `specs/002-vanilla-javascript/spec.md`

---

## Summary

Extend `py-code-health` with a native vanilla JavaScript (ECMAScript) language profile using `tree-sitter-javascript`. The engine parses `.js`, `.mjs`, and `.cjs` files into the language-neutral Universal Intermediate Representation (`IRModule`, `IRClass`, `IRFunction`) and deterministically scores them across all five weighted health dimensions (SRP, Size, Complexity, Clean Code, Security). 

The profile prioritizes type reasoning and structural clarity: parameter default values are inferred as typed, while implicit type coercion smells (loose equality `==`/`!=`), legacy `var`, empty catch blocks, `debugger;`, and high-risk security constructs (`eval`, `new Function`, `setTimeout` string arguments, `__proto__`, `with`) are flagged with exact line-numbered findings. If optional native parser dependencies are absent, the CLI terminates with exit code 2 and outputs copy-paste installation commands.

---

## Technical Context

**Language/Version**: Python 3.11+ (Runtime and analyzer engine)  
**Target Languages Evaluated**: Python (`.py`), Java 11–21+ (`.java`), JavaScript ES6+ (`.js`, `.mjs`, `.cjs`)  
**Primary Dependencies**:  
- Core analyzer: Zero external dependencies (Python stdlib: `ast`, `dataclasses`, `re`, `subprocess`, `pathlib`, `json`, `tomllib`).  
- Optional native Java grammar extras: `tree-sitter>=0.23.0`, `tree-sitter-java>=0.23.0`.  
- Optional native JavaScript grammar extras: `tree-sitter>=0.23.0`, `tree-sitter-javascript>=0.23.0`.  
**Storage**: File-based reports (`JSON`, `Markdown`, console stdout).  
**Testing**: `pytest>=8.0.0` with AST/CST fixtures; self-health dogfooding check via `code_health.py`.  
**Target Platform**: Cross-platform (Windows, macOS, Linux).  
**Project Type**: Standalone CLI tool + Antigravity agent skill.  
**Performance Goals**: Sub-second AST parsing per JavaScript file (<500ms); <15 seconds for a 50-file repository in `--no-git` mode.  
**Constraints**: Zero required external dependencies for core Python usage; fail-fast with exit code 2 if `tree-sitter-javascript` is missing; 100% backward compatibility for existing Python and Java tests.

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|:---|:---:|:---|
| **Principle I: Library-First** | **PASS** | JavaScript parsing and scoring are modularized into decoupled components (`js_parser.py`, `profiles_js.py`, `ir_scorer.py`, `module_engine.py`) with clean programmatic interfaces. |
| **Principle II: CLI Interface** | **PASS** | Exposes functionality via CLI (`--lang javascript`, `--lang js`, auto-detection), supporting console, JSON, and markdown output formats, with exit code 2 on missing dependencies. |
| **Principle III: Test-First & Determinism** | **PASS** | TDD approach with comprehensive pytest unit tests covering clean JS, code smells, syntax errors, missing parser gates, and scorecard baseline comparisons. |
| **Principle IV: Backward Compatibility** | **PASS** | Python and Java scoring pipelines, AST adapters, and CLI outputs remain 100% unaffected. |

---

## Project Structure

### Documentation (this feature)

```text
specs/002-vanilla-javascript/
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
├── pyproject.toml                         # Add optional [project.optional-dependencies] javascript
├── scripts/
│   ├── code_health.py                     # CLI entrypoint with updated --lang choices
│   └── _code_health/
│       ├── __init__.py
│       ├── models.py                      # Add node_modules, dist, build to IGNORED_SCAN_DIRS
│       ├── ir_models.py                   # IRFunction extended with JS rule fields
│       ├── profiles.py                    # Export JAVASCRIPT_PROFILE and auto-detection
│       ├── profiles_js.py                 # JavaScriptLanguageProfile implementation
│       ├── js_parser.py                   # Tree-sitter-javascript parser + ParserGuard
│       ├── ir_scorer.py                   # UniversalIRScorer evaluation with JS profile
│       ├── module_engine.py               # Dispatcher for .js/.mjs/.cjs and Git stats
│       └── reporting.py                   # File discovery (.js, .mjs, .cjs) and minified skips
├── samples/
│   └── javascript/                        # Baseline sample codebases (good vs bad)
│       ├── clean_math_service.js
│       └── smelly_legacy_script.js
└── tests/
    └── unit/
        ├── test_code_health.py            # Existing Python regression suite
        ├── test_java_spring_health.py     # Existing Java regression suite
        └── test_javascript_health.py      # New JavaScript unit & gate tests
```

**Structure Decision**: Parallels Java's implementation cleanly within `scripts/_code_health/` (`js_parser.py` and `profiles_js.py`), maintaining a unified CLI and universal IR.

---

## Execution Strategy

### TDD Requirements

- **`scripts/_code_health/js_parser.py`**: [TDD] CST extraction of functions, arrow functions, classes, methods, parameter defaults, and control flow complexity branches.
- **`scripts/_code_health/profiles_js.py`**: [TDD] Rule evaluations (legacy `var`, loose equality `==`/`!=`, dynamic `eval`/`new Function`, timer string arguments, `__proto__`, `with`, `debugger;`).
- **Missing Parser Guard**: [TDD] Verification of exit code 2, error banner, and structured JSON output when `tree-sitter-javascript` is absent.
- **File Discovery & Minified Skip**: [TDD] Directory traversal ignoring `node_modules` and skipping `*.min.js` and extreme-length lines.

### Parallel Execution Opportunities

- `js_parser.py` and `profiles_js.py` can be drafted and refined with mock IR fixtures.
- Test fixture samples (`samples/javascript/`) can be constructed in parallel with parser development.

### Human Checkpoints

1. **After Spec & Plan**: Confirm design artifacts and architecture (this checkpoint).
2. **After Parser & Profile Implementation**: Verify unit tests pass and clean JS achieves Grade A.
3. **After Full Test Suite**: Run all 76+ existing tests plus new JS tests before final branch completion.

### Review Gates

- **IR Extension Safety**: Verify `IRFunction` modifications default gracefully to preserve 100% Python/Java compatibility.
- **Security Deductions**: Verify dynamic code execution and prototype pollution deductions trigger exact expected penalties without false positives.

---

## Complexity Tracking

*No constitutional violations identified. No unjustified architectural complexity.*
