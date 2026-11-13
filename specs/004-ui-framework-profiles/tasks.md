---
description: "Phased TDD task breakdown for Web UI Framework Code Health Profiles with per-phase dogfood code health checks"
---

# Tasks: Web UI Framework Code Health Profiles

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add modular, pluggable Web UI Framework code health profiles (`react`, `nextjs`, `angular`) across TypeScript (`.ts`, `.tsx`, `.mts`, `.cts`) and JavaScript (`.js`, `.jsx`, `.mjs`, `.cjs`), strictly isolated from raw language profiles and CST parsers.

**Architecture:** `ts_parser.py` and `js_parser.py` (sharing `ecmascript_ui.py`) extract generic syntax primitives only (`IRAnnotation`, `IRCall.in_branch_or_loop`, `IRFunction.jsx_elements_count`, `IRFunction.dom_write_sinks`, `IRFunction.array_index_keys`, `IRModule.directives`, `IRModule.imports`). All UI concern maps (`UI_CONCERN_MAP`), XSS sink rules, React/Next.js hook & boundary checks, and Angular DI layering & subscription rules live exclusively in `scripts/_code_health/profiles_ui.py`, composed dynamically per file by `resolve_active_profiles()`.

**Tech Stack:** Python 3.11+ stdlib, existing `tree-sitter>=0.23.0`, `tree-sitter-typescript>=0.23.0`, `tree-sitter-javascript>=0.23.0`, `pytest>=8.0.0`.

**Input:** Design documents from `specs/004-ui-framework-profiles/`  
**Prerequisites:** [spec.md](./spec.md), [plan.md](./plan.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/](./contracts/)

## Global Constraints

- Zero new PyPI dependencies (`tree-sitter-javascript` natively parses JSX; Angular uses `tree-sitter-typescript`).
- Core Python analysis remains 100% stdlib-only and zero-dependency.
- Strict isolation: parsers (`js_parser.py`, `ts_parser.py`, `ecmascript_ui.py`), `ir_scorer.py`, and raw `JavaScriptLanguageProfile` / `TypeScriptLanguageProfile` MUST NOT reference `react`, `nextjs`, `angular`, or framework-specific rules.
- Every new and modified Python module under `scripts/_code_health/` MUST remain `< 350` effective LOC and achieve Grade A (`>= 90.0`) on dogfood scans.
- 100% deterministic reproducibility and zero regressions on Python, Java, Spring Boot, non-UI JS, and non-UI TS baselines.

## Review Focus

1. **Monorepo non-UI file isolation:** A pure Node/utility `.ts`/`.js` file inside a repo whose `package.json` declares `"react"` or `"next"` must NOT receive UI framework findings when it lacks UI imports/JSX/`app/` path (tested in US1 / US4).
2. **Malformed or missing `package.json`:** Invalid JSON or unreadable `package.json` must gracefully fall back to per-file imports without crashing (tested in US1).
3. **Custom hooks (`use*`) vs. components:** Standalone `use*.ts` hook modules and custom hooks must NOT trigger Next.js missing `"use client"` or component hook-sprawl false positives, while conditional hooks inside `if`/`for` still fail (tested in US2).
4. **Branching inside `useEffect` vs. conditional `useEffect`:** An `if` inside `useEffect(() => { if (ready) ... })` is valid and must NOT trigger Rules of Hooks, whereas `if (ready) { useEffect(...) }` MUST trigger (tested in US2).
5. **Angular RxJS teardown & lifecycle exemptions:** `.subscribe()` paired with `takeUntilDestroyed`, `takeUntil`, `DestroyRef`, or `ngOnDestroy` `.unsubscribe()` must NOT trigger unmanaged subscription penalties, and DI constructors / `@Component` LCOM4 must not false-positive (tested in US3).

## Task Format

```text
[ID] [markers] [Story] Description
```

**Markers**:
- **`[P]`**: Can run in parallel (different files, no shared mutable dependencies)
- **`[TDD]`**: Must follow RED-GREEN-REFACTOR (write test → verify fail → implement → verify pass → refactor)
- **`[REVIEW]`**: Requires human code review / approval before proceeding past checkpoint
- **`[SUBAGENT]`**: Can be delegated to an independent subagent

**Dogfood Gate Command (run at the end of every phase)**:
```powershell
uv run --python 3.12 --with tree-sitter --with tree-sitter-typescript --with tree-sitter-javascript --with tree-sitter-java python scripts/code_health.py scripts/ --only-flagged --fail-under 90.0 --no-git
```

---

## Phase 1: Setup (Discovery & CLI Configuration)

**Purpose**: Enable `.jsx` discovery/test recognition and document UI `--framework` overrides cleanly without changing scoring behavior yet.

- [x] T001 [P] [TDD] Add `.jsx` discovery and `.jsx` test naming tests (`*.test.jsx`, `*.spec.jsx`, `test_*.jsx`, `*.min.jsx` skip) in `tests/unit/test_ui_framework_health.py`; run `pytest tests/unit/test_ui_framework_health.py -v` and confirm failure before implementation
- [x] T002 [P] Update `scripts/_code_health/reporting.py` (`CodeHealthRunner._discover_files`, `_is_minified_or_bundled`) and `scripts/_code_health/module_engine.py` (`_NATIVE_PARSERS`, `is_test_file_path`, `_GitLogAccumulator.record_block`) to include `.jsx` / `*.min.jsx` routed to `parse_javascript_file`
- [x] T003 [P] Update `scripts/code_health.py` (`_build_arg_parser`) `--framework` help text to document `auto, react, nextjs, angular, spring-boot, none`
- [x] T004 **Dogfood Code Health Check (Phase 1)**: Run dogfood scan on `scripts/` (`--fail-under 90.0 --no-git`) and confirm `reporting.py`, `module_engine.py`, and `code_health.py` maintain Grade A (`>= 90.0`) and `< 350 LOC`

**Checkpoint**: Phase 1 unit tests pass and dogfood scan passes `>= 90.0`.

---

## Phase 2: Foundational (Generic IR Primitives & Shared ECMAScript CST Helpers)

**Purpose**: Extend generic language-neutral IR models, add `FrameworkProfile` evaluation/exemption hooks, and build the shared `ecmascript_ui.py` CST extraction helper (reducing `js_parser.py` below 350 LOC).

**CRITICAL**: No user story work can begin until this phase is complete.

- [x] T005 [P] [TDD] Add tests in `tests/unit/test_ir_foundation.py` verifying backward-compatible defaults on `IRCall.in_branch_or_loop`, `IRFunction` (`jsx_elements_count`, `dom_write_sinks`, `array_index_keys`), `IRModule.directives`, and `FrameworkProfile` hooks (`evaluate_module`, `extra_concerns`, `requires_explicit_return_type`, `requires_constructor_docstring`, `is_lcom4_exempt`) plus module-level `security` penalty blending in `ModuleAnalyzer`; run `pytest tests/unit/test_ir_foundation.py -v` and verify FAIL
- [x] T006 [TDD] Extend `scripts/_code_health/ir_models.py` (`IRCall`, `IRFunction`, `IRModule`, `FrameworkProfile`, `LanguageProfile`) and update `scripts/_code_health/ir_scorer.py` (`score_class`, `score_function` merging `extra_concerns`, `_score_source_clean_ir`) and `scripts/_code_health/module_engine.py` (`_score_ir_module`, `_blend_scores` applying module-level `srp`/`size`/`clean`/`security` penalties from `evaluate_module`); verify `test_ir_foundation.py` PASSES
- [x] T007 [P] [TDD] Write unit tests in `tests/unit/test_ui_framework_health.py` for generic CST extraction (`extract_decorators`, `extract_directives`, `unwrap_wrapper_callable` for `React.memo`/`forwardRef`, `jsx_elements_count`, `dom_write_sinks`, `array_index_keys`, `in_branch_or_loop` tracking); verify FAIL
- [x] T008 [TDD] Create `scripts/_code_health/ecmascript_ui.py` (`< 200 LOC`, clean small helpers) and wire it into `scripts/_code_health/ts_parser.py` and `scripts/_code_health/js_parser.py` (while trimming `js_parser.py` `< 350 LOC`); update `scripts/_code_health/profiles_js.py` and `scripts/_code_health/profiles_ts.py` so `frameworks: list[FrameworkProfile]` delegate to `LanguageProfile.evaluate_function` / `evaluate_class`; verify T007 tests PASS
- [x] T009 **Dogfood Code Health Check (Phase 2)**: Run dogfood scan on `scripts/` (`--fail-under 90.0 --no-git`) and confirm `ir_models.py`, `ir_scorer.py`, `ecmascript_ui.py`, `ts_parser.py`, `js_parser.py`, `profiles_js.py`, and `profiles_ts.py` all score Grade A (`>= 90.0`) with `js_parser.py <= 350 LOC`
- [x] T010 [REVIEW] **Checkpoint**: Foundational IR primitives, shared CST extraction, and all existing tests pass without regressions. Confirm ready for User Stories.

---

## Phase 3: User Story 1 - Automatic UI Framework Detection & Browser XSS Protection (Priority: P1) 🎯 MVP

**Goal**: Auto-detect `react`, `nextjs`, and `angular` from cached `package.json` + per-file imports (with `--framework` override and `--framework none` isolation), map web UI operational concerns (`UI_CONCERN_MAP`), and flag browser/framework XSS sinks.

**Independent Test**: Run `code_health.py` on TSX/JSX/TS files containing `dangerouslySetInnerHTML`, `innerHTML =`, `document.write`, `bypassSecurityTrustHtml`, or mixed `fetch` + `localStorage` + JSX rendering; verify Security and SRP penalties and verify `--framework none` and non-UI backend files remain unaffected.

### Tests for User Story 1

> Write these tests FIRST in `tests/unit/test_ui_framework_health.py`. Verify they FAIL before implementation.

- [x] T011 [P] [TDD] [US1] [US4] Write tests for `resolve_active_profiles` covering `package.json` + import auto-detection (`react`, `nextjs`, `angular`), `--framework` overrides (`react`, `nextjs`, `angular`, `none`), malformed/missing `package.json` fallback, and monorepo non-UI backend `.ts`/`.js` isolation
- [x] T012 [P] [TDD] [US1] Write tests for `UI_CONCERN_MAP` (`network_io`, `storage_io`, `dom_mutation`, `presentation`, `render_ui`) triggering SRP mixed-concern penalties and XSS sinks (`dangerouslySetInnerHTML`, `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `bypassSecurityTrust*`) triggering `-35.0 pts` Security deductions

### Implementation for User Story 1

- [x] T013 [US1] Create `scripts/_code_health/profiles_ui.py` defining `UI_CONCERN_MAP`, shared XSS/UI evaluation helpers, and initial `ReactFrameworkProfile`, `NextJsFrameworkProfile`, and `AngularFrameworkProfile` registration stubs (`REACT_FRAMEWORK`, `NEXTJS_FRAMEWORK`, `ANGULAR_FRAMEWORK`)
- [x] T014 [US1] Refactor and extend `resolve_active_profiles` in `scripts/_code_health/profiles.py` with cached `package.json` inspection (`functools.lru_cache` + safe JSON parsing) and clean helper decomposition (reducing `resolve_active_profiles` CC `<= 5`) and pass `imports` + `has_jsx` from `ModuleAnalyzer._score_ir_module` in `scripts/_code_health/module_engine.py`
- [x] T015 [US1] Verify T011–T012 tests PASS and run full pytest suite (`uv run --python 3.12 ... pytest -q`)
- [x] T016 [US1] **Dogfood Code Health Check (Phase 3)**: Run dogfood scan on `scripts/` (`--fail-under 90.0 --no-git`) and confirm `profiles_ui.py`, `profiles.py`, and `module_engine.py` score Grade A (`>= 90.0`) with `< 350 LOC`
- [ ] T017 [US1] [REVIEW] **Checkpoint**: MVP auto-detection, isolation, UI concerns, and browser XSS checks verified.

---

## Phase 4: User Story 2 - React & Next.js Component, Hook, and Boundary Hygiene (Priority: P2)

**Goal**: Enforce React Rules of Hooks (conditional/looped hooks), effect/state sprawl limits, array-index JSX `key` detection, `React.memo`/`forwardRef` wrapper coverage, JSX component return-type exemption, and Next.js `"use client"` / `app/` boundary rules.

**Independent Test**: Run `code_health.py` on React TSX/JSX and Next.js App Router samples; verify flawed patterns drop `< 70.0` (Grade D/F) while clean idiomatic React components omitting `: React.JSX.Element` and `use*` hook modules score `>= 90.0` (Grade A).

### Tests for User Story 2

> Write these tests FIRST in `tests/unit/test_ui_framework_health.py`. Verify they FAIL before implementation.

- [x] T018 [P] [TDD] [US2] Write React rule tests: conditional `useEffect` inside `if` (`-25.0 pts` Clean) vs valid `if` inside `useEffect(() => { if (...) {} })` (0 penalty), `> 2` effects / `> 5` `useState` sprawl on components (exempting small custom `use*` hooks), `key={idx}` in `.map(...)` (`-8.0 pts` Clean), `React.memo`/`forwardRef` extraction, and JSX component return-type exemption (preserving typed prop checks)
- [x] T019 [P] [TDD] [US2] Write Next.js boundary tests: `"use client"` importing `fs`/`node:fs`/`next/headers`/`server-only` (`-30.0 pts` Security), `app/` component calling `useState`/`useEffect` without `"use client"` (`-15.0 pts` Clean), and exemptions for `pages/` routes and standalone `use*` hook files

### Implementation for User Story 2

- [x] T020 [US2] Implement React rule methods in `ReactFrameworkProfile` inside `scripts/_code_health/profiles_ui.py` (`requires_explicit_return_type`, Rules of Hooks check, effect/state sprawl check, array-index key check)
- [x] T021 [US2] Implement `NextJsFrameworkProfile.evaluate_module` in `scripts/_code_health/profiles_ui.py` for `"use client"` server-import leaks and `app/` missing `"use client"` client-hook checks (with `pages/` and `use*` exemptions)
- [x] T022 [US2] Verify T018–T019 tests PASS across both `.tsx` and `.jsx` fixtures
- [x] T023 [US2] **Dogfood Code Health Check (Phase 4)**: Run dogfood scan on `scripts/` (`--fail-under 90.0 --no-git`) and confirm `profiles_ui.py` remains `< 350 LOC` and Grade A (`>= 90.0`)
- [ ] T024 [US2] [REVIEW] **Checkpoint**: React and Next.js rules verified on both TypeScript and JavaScript fixtures.

---

## Phase 5: User Story 3 - Angular Component Layering, Lifecycle, and Subscription Hygiene (Priority: P3)

**Goal**: Recognize Angular decorators (`@Component`, `@Directive`, `@Injectable`, `@Pipe`, `@NgModule`), flag `@Component`/`@Directive` directly injecting `HttpClient`, flag unmanaged `.subscribe()` memory leaks, flag `bypassSecurityTrust*` XSS sinks, and exempt Angular DI constructors and template-bound classes from false docstring/LCOM4 penalties.

**Independent Test**: Run `code_health.py --framework angular` on flawed vs. clean Angular `@Component` files; verify layering/subscription/XSS findings drop flawed components `< 70.0` while clean `@Component` + `@Injectable` service code scores `>= 90.0` (Grade A).

### Tests for User Story 3

> Write these tests FIRST in `tests/unit/test_ui_framework_health.py`. Verify they FAIL before implementation.

- [x] T025 [P] [TDD] [US3] Write Angular tests: `@Component` injecting `HttpClient` via constructor or `inject(HttpClient)` (`-20.0 pts` SRP), unmanaged `.subscribe()` without `takeUntilDestroyed` / `takeUntil` / `DestroyRef` / `unsubscribe` (`-15.0 pts` Clean), proper teardown with `takeUntilDestroyed()` or `ngOnDestroy` `.unsubscribe()` (0 penalty), `bypassSecurityTrustHtml` (`-35.0 pts` Security), DI constructor docstring exemption, and `@Component` LCOM4 exemption

### Implementation for User Story 3

- [x] T026 [US3] Implement `AngularFrameworkProfile` in `scripts/_code_health/profiles_ui.py` (entrypoint/LCOM4 annotations, `requires_constructor_docstring`, `HttpClient` DI layering check, unmanaged `.subscribe()` detection, `bypassSecurityTrust*` security checks)
- [x] T027 [US3] Verify T025 tests PASS and confirm Angular rules never activate on `.js`/`.jsx` files under `auto`
- [x] T028 [US3] **Dogfood Code Health Check (Phase 5)**: Run dogfood scan on `scripts/` (`--fail-under 90.0 --no-git`) and confirm `profiles_ui.py` stays `< 350 LOC` and Grade A (`>= 90.0`)
- [x] T029 [US3] [REVIEW] **Checkpoint**: Angular rules and exemptions verified.

---

## Phase 6: User Story 4 - Baseline Relocation, Framework Sample Pairs & Polyglot Isolation (Priority: P4)

**Goal**: Move `task_board_legacy.tsx` and `task_filter_bar.tsx` into `samples/typescript-react/`, replace Scenario 5 in `samples/typescript/` with a pure framework-free TypeScript pair, and add verified Good/Bad benchmark pairs for React Hooks/XSS, Next.js App Router, and Angular.

**Independent Test**: Run `pytest tests/unit/test_language_scorecard_samples.py -v` and verify every sample pair strictly separates Good (Grade A `>= 90.0`) from Bad (Grade C/D/F `< 80.0`) and matches its `.expected.json` and `SCORECARD_BASELINES.md`.

### Implementation & Samples

- [x] T030 [P] [US4] Relocate `task_board_legacy.tsx` and `task_filter_bar.tsx` (+ `.expected.json`) from `samples/typescript/` to `samples/typescript-react/` with React-aware `.expected.json` snapshots; create a pure, framework-free TypeScript replacement pair (`samples/typescript/task_board_service_clean.ts` & `samples/typescript/task_board_service_legacy.ts` + `.expected.json`)
- [x] T031 [P] [SUBAGENT] [US4] Create new Good/Bad benchmark pairs + `.expected.json` sidecars for React Hooks/XSS (`samples/typescript-react/`), Next.js App Router boundaries (`samples/typescript-nextjs/`), and Angular DI/subscription hygiene (`samples/typescript-angular/`)
- [x] T032 [US4] Update `samples/manifest.json`, `samples/SCORECARD_BASELINES.md`, and the manifest count assertion in `tests/unit/test_language_scorecard_samples.py`
- [x] T033 [US4] Run `pytest tests/unit/test_language_scorecard_samples.py -v` and verify all baseline pairs pass
- [x] T034 [US4] **Dogfood Code Health Check (Phase 6)**: Run dogfood scan on `scripts/` (`--fail-under 90.0 --no-git`) and confirm zero regressions

**Checkpoint**: All multi-language and UI framework baseline pairs verified and passing.

---

## Phase 7: Polish, Full Regression & Final Dogfood Gate

**Purpose**: Finalize quickstart validation, verify zero-dependency pure-Python CLI execution, check self-health across the entire `scripts/` directory, and document final verification results.

- [x] T035 [P] Update `README.md` / `skills/code-health/SKILL.md` (if applicable) to document `--framework react|nextjs|angular` and `.jsx` support *(note: keep `skills/code-health/scripts/` sync separate unless requested)*
- [x] T036 Execute every validation command in `specs/004-ui-framework-profiles/quickstart.md`, including zero-dependency Python mode (`python scripts/code_health.py scripts/code_health.py --no-git`)
- [x] T037 Run full automated test suite (`uv run --python 3.12 --with pytest --with tree-sitter --with tree-sitter-typescript --with tree-sitter-javascript --with tree-sitter-java pytest -v`) — 100% pass required
- [x] T038 **Final Dogfood Code Health Check (Phase 7)**: Run `uv run --python 3.12 --with tree-sitter --with tree-sitter-typescript --with tree-sitter-javascript --with tree-sitter-java python scripts/code_health.py scripts/ --fail-under 90.0 --no-git` and verify every file in `scripts/_code_health/` is Grade A (`>= 90.0`) and `< 350 LOC`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately.
- **Phase 2 (Foundational)**: Depends on Phase 1 — **BLOCKS** all user stories (US1–US4).
- **Phase 3 (US1 - Auto-Detection & XSS MVP)**: Depends on Phase 2 — establishes `profiles_ui.py` and `resolve_active_profiles`.
- **Phase 4 (US2 - React & Next.js)** and **Phase 5 (US3 - Angular)**: Both depend on Phase 3 (`profiles_ui.py`) and can run sequentially or in parallel (`[SUBAGENT]`) if modifying distinct sections/files, though keeping them sequential avoids merge conflicts in `profiles_ui.py` and `test_ui_framework_health.py`.
- **Phase 6 (US4 - Sample Relocation & Benchmark Pairs)**: Depends on Phases 3–5 being complete so expected scorecard JSON snapshots are deterministic.
- **Phase 7 (Polish & Final Gate)**: Depends on Phase 6.

### Parallel Opportunities

- Phase 1: `T001`, `T002`, `T003` can run in parallel.
- Phase 2: `T005` and `T007` (tests) can run in parallel before implementation (`T006`, `T008`).
- Phase 3: `T011` and `T012` (tests) can run in parallel.
- Phase 4: `T018` and `T019` (tests) can run in parallel.
- Phase 6: `T030` (pure TS replacement + React relocation) and `T031` (new Next.js/Angular pairs) can run in parallel across distinct sample directories.
