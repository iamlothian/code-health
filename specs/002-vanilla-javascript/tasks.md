---
description: "Phased task breakdown for Vanilla JavaScript (ECMAScript) Language Profile"
---

# Tasks: Vanilla JavaScript (ECMAScript) Language Profile

**Input**: Design documents from `specs/002-vanilla-javascript/`  
**Prerequisites**: [plan.md](./plan.md) (required), [spec.md](./spec.md) (required), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/](./contracts/)

## Task Format

```text
[ID] [markers] [Story] Description
```

**Markers**:
- **`[P]`**: Can run in parallel (different files, no shared mutable dependencies)
- **`[TDD]`**: Must follow RED-GREEN-REFACTOR (write test → fail → implement → pass → refactor)
- **`[REVIEW]`**: Requires human code review / approval before proceeding past checkpoint
- **`[SUBAGENT]`**: Can be delegated to an independent subagent

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project dependency configuration and scan exclusion directories

- [x] T001 Update `pyproject.toml` to add optional dependency group `[project.optional-dependencies] javascript = ["tree-sitter>=0.23.0", "tree-sitter-javascript>=0.23.0"]` and sync with `uv sync --extra dev`
- [x] T002 [P] Update `IGNORED_SCAN_DIRS` in `scripts/_code_health/models.py` to add `node_modules`, `dist`, `build`, `.next`, `.nuxt`

---

## Phase 2: Foundational (IR & Model Extension)

**Purpose**: Unified Intermediate Representation (IR) backward-compatible extensions for JavaScript rule tracking

**CRITICAL**: No user story work can begin until this phase is complete.

- [x] T003 [P] [TDD] Extend `IRFunction` in `scripts/_code_health/ir_models.py` with backward-compatible fields: `var_declarations_count: int = 0`, `loose_comparisons_count: int = 0`, `has_proto_mutation: bool = False`, `has_with_statement: bool = False`, `has_debugger_statement: bool = False`
- [x] T004 [P] [TDD] Update tests in `tests/unit/test_ir_foundation.py` to verify `IRFunction` additions maintain 100% backward compatibility with Python and Java models
- [x] T005 [REVIEW] **Checkpoint**: Foundational IR model extensions verified with existing tests passing. Confirm ready for User Stories.

---

## Phase 3: User Story 1 - Automatic JavaScript Source Discovery and Health Evaluation (Priority: P1) 🎯 MVP

**Goal**: Automatically detect, parse, and score `.js`, `.mjs`, and `.cjs` source files into `IRModule` with composite 0–100 scores and letter grades.  
**Independent Test**: Execute `python scripts/code_health.py` pointing to a JavaScript file and verify that classes, methods, functions, and file-level metrics are parsed and displayed with exact line numbers.

### Tests for User Story 1

> Write these tests FIRST in `tests/unit/test_javascript_health.py`. Verify they FAIL before implementation.

- [x] T006 [P] [TDD] [US1] Write unit tests in `tests/unit/test_javascript_health.py` for JavaScript file discovery (`.js`, `.mjs`, `.cjs`), minified asset skip (`*.min.js` and lines > 1,000 chars), and CLI `--lang javascript` / `--lang js` flag handling
- [x] T007 [P] [TDD] [US1] Write unit tests in `tests/unit/test_javascript_health.py` for Tree-Sitter JavaScript CST parsing of ES6+ classes, methods, function declarations, and named arrow functions into `IRModule` with hierarchical qualnames (`Class.method`, `object.method`, variable name)

### Implementation for User Story 1

- [x] T008 [P] [US1] Update `is_test_file_path` and `_GitLogAccumulator` in `scripts/_code_health/module_engine.py` to recognize JavaScript test conventions (`*.test.js`, `*.spec.js`, `*_test.js`, `__tests__/`) and track `.js`, `.mjs`, `.cjs` Git churn
- [x] T009 [P] [US1] Update `CodeHealthRunner._discover_files` in `scripts/_code_health/reporting.py` to discover `.js`, `.mjs`, `.cjs` files, filter ignored directories, and automatically skip minified assets (`*.min.js` and lines > 1,000 chars) with a log notice
- [x] T010 [US1] Implement Tree-Sitter JavaScript parser in `scripts/_code_health/js_parser.py` converting JS classes, methods, function declarations, and named arrow functions into `IRModule`, absorbing inline callbacks into parent scope metrics
- [x] T011 [US1] Implement `JavaScriptLanguageProfile` in `scripts/_code_health/profiles_js.py` and register `JAVASCRIPT_PROFILE` in `scripts/_code_health/profiles.py`
- [x] T012 [US1] Wire JavaScript file dispatch into `ModuleAnalyzer.analyze()` in `scripts/_code_health/module_engine.py` using `js_parser.py` and `ir_scorer.py`
- [x] T013 [US1] Update `_build_arg_parser()` and `main()` in `scripts/code_health.py` to add `"javascript"` and `"js"` choices to `--lang`
- [x] T014 [US1] [REVIEW] **Checkpoint**: User Story 1 MVP fully functional. Verify single-file, multi-file, and mixed Python/Java/JS directory scans produce accurate scorecards.

---

## Phase 4: User Story 2 - Missing Native Parser Guard and Actionable Install Prompt (Priority: P2)

**Goal**: Guarantee zero silent failures or heuristic degradation: halt with exit code `2` and display copy-paste `uv` and `pip` installation commands when `tree-sitter` or `tree-sitter-javascript` is missing.  
**Independent Test**: Execute `code_health.py` on a JavaScript file in an environment lacking `tree-sitter-javascript`; verify exit code 2 and warning banner in console mode, and valid JSON payload in `--format json` mode. Verify Python and Java analysis are unaffected.

### Tests for User Story 2

> Write these tests FIRST in `tests/unit/test_javascript_health.py`. Verify they FAIL before implementation.

- [x] T015 [P] [TDD] [US2] Write unit tests in `tests/unit/test_javascript_health.py` mocking missing `tree_sitter_javascript`, verifying `MissingNativeParserError` halts with exit code 2 and outputs copy-paste installation commands in both console and JSON formats
- [x] T016 [P] [TDD] [US2] Write unit tests in `tests/unit/test_javascript_health.py` verifying purely Python or Java runs never trigger missing JavaScript parser errors

### Implementation for User Story 2

- [x] T017 [US2] Implement parser guard `check_javascript_dependencies()` in `scripts/_code_health/js_parser.py` raising `MissingNativeParserError("javascript", ["tree-sitter", "tree-sitter-javascript"])` when packages are missing
- [x] T018 [US2] Update `main()` in `scripts/code_health.py` to ensure `MissingNativeParserError` formatting and exit code 2 handle `"javascript"` seamlessly
- [x] T019 [US2] [REVIEW] **Checkpoint**: User Story 2 verified. Missing dependencies fail fast with exit code 2 and actionable guidance without affecting other languages.

---

## Phase 5: User Story 3 - Type Reasoning, Anti-Coercion, and Clean Code Quality (Priority: P3)

**Goal**: Reward parameter type reasoning (defaults and JSDoc) while penalizing implicit type coercion smells (loose equality `==`/`!=`), legacy `var` declarations, and empty `catch` blocks.  
**Independent Test**: Analyze a clean modern JS file vs. a legacy file containing `var`, `==`, un-defaulted untyped parameters, and empty catch blocks; verify exact penalty deductions.

### Tests for User Story 3

> Write these tests FIRST in `tests/unit/test_javascript_health.py`. Verify they FAIL before implementation.

- [x] T020 [P] [TDD] [US3] Write unit tests in `tests/unit/test_javascript_health.py` verifying parameter default initializers (`param = defaultValue`) and JSDoc `@param {type}` tags are inferred as typed with zero penalty
- [x] T021 [P] [TDD] [US3] Write unit tests in `tests/unit/test_javascript_health.py` verifying un-defaulted untyped parameters in non-test functions incur `-2.0 pts` each (cap `-10.0 pts`)
- [x] T022 [P] [TDD] [US3] Write unit tests in `tests/unit/test_javascript_health.py` verifying loose equality `==`/`!=` incurs `-2.0 pts` each (cap `-10.0 pts`), legacy `var` incurs `-3.0 pts` each (cap `-15.0 pts`), and empty `catch` blocks incur `-10.0 pts`

### Implementation for User Story 3

- [x] T023 [US3] In `scripts/_code_health/js_parser.py`, extract parameter default initializers (`assignment_pattern`), JSDoc blocks, `var` declarations count, `==`/`!=` comparison counts, and empty catch bodies into `IRFunction`
- [x] T024 [US3] In `scripts/_code_health/profiles_js.py`, implement `JavaScriptLanguageProfile.evaluate_function` to deduct penalties for legacy `var`, loose equality, empty catch blocks, and parameter typing
- [x] T025 [US3] [REVIEW] **Checkpoint**: User Story 3 verified. Type reasoning and anti-coercion rules calculate exact penalties and pass unit tests.

---

## Phase 6: User Story 4 - Core Language Security and Boundary Hygiene (Priority: P4)

**Goal**: Detect and penalize high-risk ECMAScript dynamic execution sinks (`eval`, `new Function`), timer string execution (`setTimeout("string", ...)`), direct prototype mutations (`__proto__`), `with` statements, and lingering `debugger;` statements.  
**Independent Test**: Analyze JavaScript code with dynamic evaluation, string timers, `__proto__`, `with`, and `debugger;`, verifying exact line-numbered Security and Clean Code penalties.

### Tests for User Story 4

> Write these tests FIRST in `tests/unit/test_javascript_health.py`. Verify they FAIL before implementation.

- [x] T026 [P] [TDD] [US4] Write unit tests in `tests/unit/test_javascript_health.py` verifying `eval(...)` and `new Function(...)` deduct `-40.0 pts` under Security
- [x] T027 [P] [TDD] [US4] Write unit tests in `tests/unit/test_javascript_health.py` verifying `setTimeout`/`setInterval` with string arguments deducts `-20.0 pts` and direct `__proto__` mutations deduct `-25.0 pts` under Security
- [x] T028 [P] [TDD] [US4] Write unit tests in `tests/unit/test_javascript_health.py` verifying `with` statements deduct `-30.0 pts` under Security and `debugger;` statements deduct `-10.0 pts` under Clean Code

### Implementation for User Story 4

- [x] T029 [US4] In `scripts/_code_health/js_parser.py`, detect calls to `eval`, `new Function`, string arguments in `setTimeout`/`setInterval`, `__proto__` assignments, `with_statement`, and `debugger_statement`
- [x] T030 [US4] In `scripts/_code_health/profiles_js.py`, implement Security and Clean Code rule deductions in `evaluate_function` for all security and operational hygiene constructs
- [x] T031 [US4] [REVIEW] **Checkpoint**: User Story 4 verified. All security smells trigger exact findings and deductions without false positives.

---

## Phase 7: User Story 5 - Test Suite and Assertion Hygiene Recognition (Priority: P5)

**Goal**: Recognize JavaScript test files (`*.test.js`, `*.spec.js`, `__tests__/`) and BDD test blocks (`it`, `test`), extract assertions (Node `assert`, Jest/Vitest `expect`, Chai `should`, `toBe`, `toEqual`), and evaluate assertion hygiene.  
**Independent Test**: Analyze test files with valid assertion counts (1–8) vs. 0 assertions or >8 assertions; verify accurate recognition and test hygiene deductions.

### Tests for User Story 5

> Write these tests FIRST in `tests/unit/test_javascript_health.py`. Verify they FAIL before implementation.

- [x] T032 [P] [TDD] [US5] Write unit tests in `tests/unit/test_javascript_health.py` verifying test file detection (`*.test.js`, `*.spec.js`, `__tests__/`) and BDD test block extraction (`it(...)`, `test(...)`) with `is_test=True` and `name="test: " + title`
- [x] T033 [P] [TDD] [US5] Write unit tests in `tests/unit/test_javascript_health.py` verifying assertion matcher recognition (Node `assert`, Jest/Vitest `expect`, Chai `should`, `toBe`, `toEqual`) and assertion hygiene (flagging 0 assertions or >8 assertions)

### Implementation for User Story 5

- [x] T034 [US5] In `scripts/_code_health/js_parser.py`, extract callbacks inside `it()` and `test()` call expressions as `IRFunction(is_test=True, name="test: " + title)`
- [x] T035 [US5] In `scripts/_code_health/profiles_js.py`, implement `JavaScriptLanguageProfile.is_test_assert_call` recognizing Node, Jest, Vitest, Chai, and Mocha assertion matchers
- [x] T036 [US5] [REVIEW] **Checkpoint**: User Story 5 verified. Test suites evaluate accurately without false docstring or assertion penalties.

---

## Phase 8: Polish, Baseline Samples, and Documentation

**Purpose**: Create baseline sample scorecards, sync skill references, update documentation, and perform self-health verification

- [x] T037 [P] Create baseline JavaScript sample files in `samples/javascript/`:
  - `samples/javascript/clean_math_service.js` (Grade A, clean ES6+, default parameters, strict equality)
  - `samples/javascript/smelly_legacy_script.js` (Grade D/F, var, ==, eval, with, debugger, string timers, __proto__)
- [x] T038 [P] [TDD] Add JavaScript sample scorecard baseline comparisons to `tests/unit/test_language_scorecard_samples.py` ensuring clean JS strictly outscores smelly JS and achieves Grade A
- [x] T039 [P] Update `skills/code-health/` with JavaScript rubric references and sync scripts
- [x] T040 Update `README.md` to document JavaScript support, optional dependencies, and usage examples
- [x] T041 Run full self-health check: `python scripts/code_health.py scripts tests/unit/test_javascript_health.py --fail-under 90.0` and execute full pytest suite `pytest -v`
- [x] T042 [REVIEW] **Final Checkpoint**: Verify all 42 tasks complete, all acceptance criteria satisfied, and git status is clean.

---

## Dependencies & Execution Sequence

```
Phase 1: Setup (T001, T002)
   │
   ▼
Phase 2: Foundational IR (T003, T004) ──► T005 [REVIEW]
   │
   ▼
Phase 3: US1 - Auto Discovery & Evaluation (T006 - T013) ──► T014 [REVIEW]
   │
   ▼
Phase 4: US2 - Missing Parser Guard (T015 - T018) ──► T019 [REVIEW]
   │
   ▼
Phase 5: US3 - Type Reasoning & Clean Code (T020 - T024) ──► T025 [REVIEW]
   │
   ▼
Phase 6: US4 - Core Language Security (T026 - T030) ──► T031 [REVIEW]
   │
   ▼
Phase 7: US5 - Test Suite & Assertion Hygiene (T032 - T035) ──► T036 [REVIEW]
   │
   ▼
Phase 8: Polish, Samples & Verification (T037 - T041) ──► T042 [FINAL REVIEW]
```
