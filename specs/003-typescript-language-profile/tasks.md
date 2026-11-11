---
description: "Phased task breakdown for TypeScript Language Profile"
---

# Tasks: TypeScript Language Profile

**Input**: Design documents from `specs/003-typescript-language-profile/`  
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

- [x] T001 Update `pyproject.toml` to add optional dependency group `[project.optional-dependencies] typescript = ["tree-sitter>=0.23.0", "tree-sitter-typescript>=0.23.0"]` and sync dependencies
- [x] T002 [P] Update `scripts/_code_health/reporting.py` and `scripts/_code_health/models.py` to ensure declaration files (`*.d.ts`, `*.d.mts`, `*.d.cts`) and minified TypeScript files (`*.min.ts`) are excluded from file discovery

---

## Phase 2: Foundational (IR & Model Extension)

**Purpose**: Unified Intermediate Representation (IR) backward-compatible extensions for TypeScript telemetry

**CRITICAL**: No user story work can begin until this phase is complete.

- [x] T003 [P] [TDD] Extend `IRFunction` in `scripts/_code_health/ir_models.py` with backward-compatible fields: `explicit_any_count: int = 0`, `ts_ignore_count: int = 0`, `non_null_assertion_count: int = 0`
- [x] T004 [P] [TDD] Update tests in `tests/unit/test_ir_foundation.py` to verify `IRFunction` additions maintain 100% backward compatibility with Python, Java, and JavaScript models
- [x] T005 [REVIEW] **Checkpoint**: Foundational IR model extensions verified with existing tests passing. Confirm ready for User Stories.

---

## Phase 3: User Story 1 - Automatic TypeScript & TSX Source Discovery and Health Evaluation (Priority: P1) 🎯 MVP

**Goal**: Automatically detect, parse, and score `.ts`, `.tsx`, `.mts`, and `.cts` source files into `IRModule` with composite 0–100 scores and letter grades.  
**Independent Test**: Execute `python scripts/code_health.py` pointing to a TypeScript or TSX file and verify that classes, methods, functions, and file-level metrics are parsed and displayed with exact line numbers.

### Tests for User Story 1

> Write these tests FIRST in `tests/unit/test_typescript_health.py`. Verify they FAIL before implementation.

- [x] T006 [P] [TDD] [US1] Write unit tests in `tests/unit/test_typescript_health.py` for TypeScript file discovery (`.ts`, `.tsx`, `.mts`, `.cts`), ambient declaration skip (`*.d.ts`), minified asset skip (`*.min.ts` and lines > 1,000 chars), and CLI `--lang typescript` / `--lang ts` flag handling
- [x] T007 [P] [TDD] [US1] Write unit tests in `tests/unit/test_typescript_health.py` for Tree-Sitter TypeScript/TSX parsing of classes, methods, function declarations, named arrow functions, TSX components, constructor parameter properties, and pure contracts (interfaces/type aliases) into `IRModule` with hierarchical qualnames

### Implementation for User Story 1

- [x] T008 [P] [US1] Update `is_test_file_path` and `_GitLogAccumulator` in `scripts/_code_health/module_engine.py` to recognize TypeScript test conventions (`*.test.ts`, `*.spec.ts`, `*.test.tsx`, `*.spec.tsx`, etc.) and track `.ts`, `.tsx`, `.mts`, `.cts` Git churn
- [x] T009 [P] [US1] Update `CodeHealthRunner._discover_files` in `scripts/_code_health/reporting.py` to discover `.ts`, `.tsx`, `.mts`, `.cts` files, filter ignored directories, and automatically skip ambient declaration files (`*.d.ts`) and minified assets (`*.min.ts`)
- [x] T010 [US1] Implement Tree-Sitter TypeScript & TSX parser in `scripts/_code_health/ts_parser.py` converting TS/TSX classes, methods, function declarations, named arrow functions, and constructor parameter properties into `IRModule`, absorbing inline callbacks and treating interfaces/types as non-behavioral contracts
- [x] T011 [US1] Implement `TypeScriptLanguageProfile` in `scripts/_code_health/profiles_ts.py` and register `TYPESCRIPT_PROFILE` in `scripts/_code_health/profiles.py`
- [x] T012 [US1] Wire TypeScript file dispatch into `ModuleAnalyzer.analyze()` in `scripts/_code_health/module_engine.py` using `ts_parser.py` and `ir_scorer.py`
- [x] T013 [US1] Update `_build_arg_parser()` and `main()` in `scripts/code_health.py` to add `"typescript"` and `"ts"` choices to `--lang`
- [x] T014 [US1] [REVIEW] **Checkpoint**: User Story 1 MVP fully functional. Verify single-file, multi-file, and mixed polyglot directory scans produce accurate scorecards.

---

## Phase 4: User Story 2 - Missing Native Parser Guard and Actionable Install Prompt (Priority: P2)

**Goal**: Guarantee zero silent failures or heuristic degradation: halt with exit code `2` and display copy-paste `uv` and `pip` installation commands when `tree-sitter` or `tree-sitter-typescript` is missing.  
**Independent Test**: Execute `code_health.py` on a TypeScript file in an environment lacking `tree-sitter-typescript`; verify exit code 2 and warning banner in console mode, and valid JSON payload in `--format json` mode. Verify Python, Java, and JavaScript analysis are unaffected.

### Tests for User Story 2

> Write these tests FIRST in `tests/unit/test_typescript_health.py`. Verify they FAIL before implementation.

- [x] T015 [P] [TDD] [US2] Write unit tests in `tests/unit/test_typescript_health.py` mocking missing `tree_sitter_typescript`, verifying `MissingNativeParserError` halts with exit code 2 and outputs copy-paste installation commands in both console and JSON formats
- [x] T016 [P] [TDD] [US2] Write unit tests in `tests/unit/test_typescript_health.py` verifying purely Python, Java, or JavaScript runs never trigger missing TypeScript parser errors

### Implementation for User Story 2

- [x] T017 [US2] Implement parser guard `check_typescript_dependencies()` in `scripts/_code_health/ts_parser.py` raising `MissingNativeParserError("typescript", ["tree-sitter", "tree-sitter-typescript"])` when packages are missing
- [x] T018 [US2] Update `main()` in `scripts/code_health.py` to ensure `MissingNativeParserError` formatting and exit code 2 handle `"typescript"` seamlessly
- [ ] T019 [US2] [REVIEW] **Checkpoint**: User Story 2 verified. Missing dependencies fail fast with exit code 2 and actionable guidance without affecting other languages.

---

## Phase 5: User Story 3 - Strict Typing, Clean Code, and Type Safety Escape Hatch Detection (Priority: P3)

**Goal**: Enforce strict signature typing (untyped params: `-5.0 pts`, missing return types: `-10.0 pts`) and surface type-safety escape hatches: explicit `any` (`-5.0 pts`), `@ts-ignore`/`@ts-nocheck` (`-10.0 pts`), non-null assertions `!` (`-2.0 pts`), and boolean default flags (`-6.0 pts` SRP).  
**Independent Test**: Analyze a clean TypeScript file vs. a smelly file containing `any`, `@ts-ignore`, non-null assertions `!`, untyped parameters, missing return types, `var`, and loose equality `==`; verify exact penalty deductions.

### Tests for User Story 3

> Write these tests FIRST in `tests/unit/test_typescript_health.py`. Verify they FAIL before implementation.

- [ ] T020 [P] [TDD] [US3] Write unit tests in `tests/unit/test_typescript_health.py` verifying strict parameter typing (untyped un-defaulted params: `-5.0 pts` each, cap `-25.0 pts`), missing return types (`-10.0 pts`), and parameter defaults/optionals recognized as typed
- [ ] T021 [P] [TDD] [US3] Write unit tests in `tests/unit/test_typescript_health.py` verifying explicit `any` (`-5.0 pts`, cap `-20.0 pts`), `@ts-ignore`/`@ts-nocheck` (`-10.0 pts`, cap `-20.0 pts`), and non-null assertion `!` (`-2.0 pts`, cap `-10.0 pts`)
- [ ] T022 [P] [TDD] [US3] Write unit tests in `tests/unit/test_typescript_health.py` verifying boolean default flags (`flag: boolean = false`: `-6.0 pts` under SRP), legacy `var` (`-3.0 pts`), loose equality `==`/`!=` (`-2.0 pts`), empty catch blocks (`-10.0 pts`), and `debugger;` (`-10.0 pts`)

### Implementation for User Story 3

- [ ] T023 [US3] In `scripts/_code_health/ts_parser.py`, extract parameter types, return types, `any` occurrences, `@ts-ignore`/`@ts-nocheck` comments, `!` non-null assertions, and boolean defaults into `IRFunction`
- [ ] T024 [US3] In `scripts/_code_health/profiles_ts.py` and `scripts/_code_health/ir_scorer.py`, implement rule deductions for strict typing, escape hatches (`any`, `@ts-ignore`, `!`), boolean default flags, and ECMAScript hygiene
- [ ] T025 [US3] [REVIEW] **Checkpoint**: User Story 3 verified. Strict typing and escape hatch detection calculate exact penalties and pass unit tests.

---

## Phase 6: User Story 4 - Core Language Security and Boundary Hygiene (Priority: P4)

**Goal**: Detect and penalize high-risk dynamic execution sinks (`eval`, `new Function`), timer string execution, direct prototype mutations (`__proto__`, `Object.setPrototypeOf`), `with` statements, and SQL/query string concatenation/template literal interpolation.  
**Independent Test**: Analyze TypeScript code with dynamic evaluation, string timers, `__proto__`, `with`, and query string interpolation, verifying exact line-numbered Security penalties.

### Tests for User Story 4

> Write these tests FIRST in `tests/unit/test_typescript_health.py`. Verify they FAIL before implementation.

- [ ] T026 [P] [TDD] [US4] Write unit tests in `tests/unit/test_typescript_health.py` verifying `eval(...)` and `new Function(...)` deduct `-40.0 pts`, string timers deduct `-20.0 pts`, direct `__proto__` mutations deduct `-25.0 pts`, and `with` deducts `-30.0 pts` under Security
- [ ] T027 [P] [TDD] [US4] Write unit tests in `tests/unit/test_typescript_health.py` verifying database/ORM query calls (`query`, `execute`, `raw`, `$queryRawUnsafe`, `$executeRawUnsafe`) with string concatenation or template literal interpolation deduct `-40.0 pts` under Security

### Implementation for User Story 4

- [ ] T028 [US4] In `scripts/_code_health/ts_parser.py`, detect calls to `eval`, `new Function`, string arguments in timers, `__proto__` assignments, `with_statement`, and SQL/query string concatenation/template interpolation
- [ ] T029 [US4] In `scripts/_code_health/profiles_ts.py`, implement Security deductions in `evaluate_function` for all security and query injection constructs
- [ ] T030 [US4] [REVIEW] **Checkpoint**: User Story 4 verified. All security smells and query injection patterns trigger exact findings and deductions without false positives.

---

## Phase 7: User Story 5 - Test Suite and Assertion Hygiene Recognition (Priority: P5)

**Goal**: Recognize TypeScript test files (`*.test.ts`, `*.spec.ts`, `*.test.tsx`, `*.spec.tsx`, `__tests__/`) and BDD test blocks (`it`, `test`), extract assertions (Jest/Vitest/Mocha `expect`, `assert`, `should`, `toBe`, `toEqual`), and evaluate assertion hygiene.  
**Independent Test**: Analyze test files with valid assertion counts (1–8) vs. 0 assertions or >8 assertions; verify accurate recognition and test hygiene deductions.

### Tests for User Story 5

> Write these tests FIRST in `tests/unit/test_typescript_health.py`. Verify they FAIL before implementation.

- [ ] T031 [P] [TDD] [US5] Write unit tests in `tests/unit/test_typescript_health.py` verifying test file detection (`*.test.ts`, `*.spec.ts`, `*.test.tsx`, `*.spec.tsx`, `__tests__/`) and BDD test block extraction (`it(...)`, `test(...)`) with `is_test=True` and `name="test: " + title`
- [ ] T032 [P] [TDD] [US5] Write unit tests in `tests/unit/test_typescript_health.py` verifying assertion matcher recognition (`expect`, `assert`, `should`, `toBe`, `toEqual`) and assertion hygiene (flagging 0 assertions or >8 assertions)

### Implementation for User Story 5

- [ ] T033 [US5] In `scripts/_code_health/ts_parser.py`, extract callbacks inside `it()` and `test()` call expressions as `IRFunction(is_test=True, name="test: " + title)`
- [ ] T034 [US5] In `scripts/_code_health/profiles_ts.py` and `scripts/_code_health/ir_scorer.py`, recognize assertion matchers and deduplicate assertion counts for TypeScript test callbacks
- [ ] T035 [US5] [REVIEW] **Checkpoint**: User Story 5 verified. Test suites evaluate accurately without false docstring or assertion penalties.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Verification samples, self-health dogfooding, regression testing, and documentation

- [ ] T036 [P] Create sample TypeScript codebases in `samples/typescript/`: `clean_math_service.ts` (target: Grade A $\ge 90.0$) and `smelly_legacy_script.ts` (target: Grade D/F)
- [ ] T037 [P] Run `quickstart.md` validation scenarios against `samples/typescript/` and verify all expected scores and findings match
- [ ] T038 Run self-health dogfooding check: execute `python scripts/code_health.py scripts/_code_health/ --no-git` and verify all new and modified modules maintain Grade A ($\ge 90.0$) and LOC $\le 350$
- [ ] T039 Run full test suite across Python, Java, JavaScript, and TypeScript via `pytest tests/unit/ -v` and verify 100% pass rate
- [ ] T040 [REVIEW] Final review against spec and constitutional principles before feature branch completion

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories proceed sequentially by priority (US1 → US2 → US3 → US4 → US5)
- **Polish (Phase 8)**: Depends on all user stories completing successfully

### Parallel Opportunities

- T001 and T002 in Setup can proceed in parallel
- T003 and T004 in Foundational can proceed in parallel
- Test writing tasks marked `[P]` within each User Story can proceed in parallel
- `samples/typescript/` sample creation (T036) can be authored in parallel with Polish validation
