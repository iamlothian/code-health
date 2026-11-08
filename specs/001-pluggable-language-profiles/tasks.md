---
description: "Task list for Pluggable Language & Framework Profiles (Java & Spring Boot)"
---

# Tasks: Pluggable Language & Framework Profiles (Java & Spring Boot)

**Input**: Design documents from `specs/001-pluggable-language-profiles/`  
**Prerequisites**: [plan.md](./plan.md) (required), [spec.md](./spec.md) (required), [data-model.md](./data-model.md), [contracts/](./contracts/)

## Task Format

```text
[ID] [markers] [Story] Description
```

**Markers**:
- **[P]**: Can run in parallel (different files, no dependencies)
- **[TDD]**: Must follow RED-GREEN-REFACTOR (write test → fail → implement → pass → refactor)
- **[REVIEW]**: Requires code review before proceeding to next task
- **[SUBAGENT]**: Can be delegated to a subagent for parallel execution

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project dependency configuration and optional extras

- [x] T001 Update `pyproject.toml` to add optional dependency group `[project.optional-dependencies] java = ["tree-sitter>=0.23.0", "tree-sitter-java>=0.23.0"]` and sync lockfile

**Execution notes**: Verify `uv sync` succeeds and Python core dependencies remain unchanged.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Unified Intermediate Representation (IR), profile contracts, and universal scorer

**CRITICAL**: No user story work can begin until this phase is complete.

- [x] T002 [P] [TDD] Define language-neutral IR dataclasses in `scripts/_code_health/ir_models.py` (`IRAnnotation`, `IRParam`, `IRCall`, `IRExceptHandler`, `IRField`, `IRFunction`, `IRClass`, `IRModule`, `MissingNativeParserError`, `RulePenalty`)
- [x] T003 [P] [TDD] Implement Universal 5-Dimension Scorer in `scripts/_code_health/ir_scorer.py` evaluating SRP, Size, Complexity, Clean Code, and Security on IR objects
- [x] T004 [P] Implement `LanguageProfile` and `FrameworkProfile` registry & protocols in `scripts/_code_health/profiles.py`
- [x] T005 [TDD] Implement Python AST-to-IR adapter in `scripts/_code_health/profiles.py` and verify identical scoring parity against legacy Python tests
- [x] T006 [REVIEW] **Checkpoint**: Foundational IR models, scorer, and Python profile adapter pass unit tests. Get approval before starting User Stories.

---

## Phase 3: User Story 1 - Automatic Multi-Language Code Health Evaluation (Priority: P1) MVP

**Goal**: Automatically detect and analyze `.java` files alongside `.py` files without manual `--lang` configuration.  
**Independent Test**: Run `python scripts/code_health.py` on a `.java` file, a `.py` file, and a mixed directory; verify each is automatically parsed and scored.

### Tests for User Story 1

> Write these tests FIRST in `tests/unit/test_java_spring_health.py`. Verify they FAIL before implementation.

- [x] T007 [P] [TDD] [US1] Write unit tests for multi-language file discovery, package inference, and Java CST parsing into IR
- [x] T008 [P] [TDD] [US1] Write unit tests for Java LCOM4 class cohesion resolving explicit `this.field` and implicit declared field references

### Implementation for User Story 1

- [x] T009 [P] [US1] Update `is_test_file_path` and `_GitLogAccumulator` in `scripts/_code_health/module_engine.py` to recognize Java test naming conventions (`src/test/java/`, `*Test.java`, `*Tests.java`, `*IT.java`) and track `.java` Git history
- [x] T010 [P] [US1] Update `CodeHealthRunner._discover_files` and `_infer_packages` in `scripts/_code_health/reporting.py` to discover `.java` files and detect Java package namespaces
- [x] T011 [US1] Implement native Tree-Sitter Java parser in `scripts/_code_health/java_parser.py` converting Java classes, methods, records, annotations, and field accesses into `IRModule`
- [x] T012 [US1] Implement Java Language Profile in `scripts/_code_health/profiles.py` with Java metric rules (LOC, CC, CogC, Javadoc hygiene, and LCOM4 exemptions for records/enums)
- [x] T013 [US1] Wire Java file dispatch into `ModuleAnalyzer.analyze()` in `scripts/_code_health/module_engine.py` using `java_parser.py` and `ir_scorer.py`
- [x] T014 [US1] [REVIEW] **Checkpoint**: User Story 1 fully functional. Verify single-file, multi-file, and mixed Python/Java scans run and pass.

---

## Phase 4: User Story 2 - Mandatory Native Parser Warning & Installation Prompt (Priority: P2)

**Goal**: Guarantee zero silent failures or imprecise parsing: halt with exit code `2` and display copy-paste `uv`/`pip` installation commands when `tree-sitter-java` is missing.  
**Independent Test**: Execute `code_health.py` on a Java file in an environment without `tree-sitter-java`; verify exit code 2 and warning output. Verify Python files are completely unaffected.

### Tests for User Story 2

> Write these tests FIRST in `tests/unit/test_java_spring_health.py`. Verify they FAIL before implementation.

- [x] T015 [P] [TDD] [US2] Write unit tests mocking missing `tree_sitter_java`, verifying `MissingNativeParserError` is raised and CLI returns exit code 2 with installation commands
- [x] T016 [P] [TDD] [US2] Write unit tests verifying purely Python files never trigger the missing Java parser warning

### Implementation for User Story 2

- [x] T017 [US2] Implement parser guard `check_java_dependencies()` in `scripts/_code_health/java_parser.py` raising `MissingNativeParserError` with formatted commands when `tree-sitter` or `tree-sitter-java` is missing
- [x] T018 [US2] Update `main()` and output rendering in `scripts/code_health.py` to catch `MissingNativeParserError`, write warning banner to stderr/console, emit structured JSON under `--format json`, and exit with code `2`
- [x] T019 [US2] [REVIEW] **Checkpoint**: User Story 2 verified. Missing grammar dependencies cleanly halt with actionable commands without crashing or breaking Python analysis.

---

## Phase 5: User Story 3 - Framework-Aware Architectural Health for Spring Boot (Priority: P3)

**Goal**: Detect Spring Boot stereotypes and enforce architectural rules (field `@Autowired`, `@RestController` direct `@Repository` injection, transaction boundary misuse, and SQL string concatenation).  
**Independent Test**: Analyze sample clean vs. smell-laden Spring Boot classes and verify exact line-numbered findings with penalty deductions.

### Tests for User Story 3

> Write these tests FIRST in `tests/unit/test_java_spring_health.py`. Verify they FAIL before implementation.

- [ ] T020 [P] [TDD] [US3] Unit tests for `@Autowired` field injection detection (-8.0 pts Clean Code)
- [ ] T021 [P] [TDD] [US3] Unit tests for `@RestController` directly injecting `@Repository` / `EntityManager` (-20.0 pts SRP)
- [ ] T022 [P] [TDD] [US3] Unit tests for `@Transactional` on `@RestController` or `private` methods (-15.0 to -20.0 pts)
- [ ] T023 [P] [TDD] [US3] Unit tests for string-concatenated SQL queries in `JdbcTemplate` / `EntityManager` (-40.0 pts Security)
- [ ] T024 [P] [TDD] [US3] Unit tests for web entrypoint parameter limit relaxation ($\le 6$ parameters for `@GetMapping`, `@PostMapping`, etc.)

### Implementation for User Story 3

- [ ] T025 [P] [US3] Implement `SPRING_BOOT_FRAMEWORK` profile in `scripts/_code_health/profiles.py` with concern mappings, stereotype definitions, and LCOM4 exemptions (`@Entity`, `@Data`, `@Configuration`)
- [ ] T026 [US3] Implement Spring Boot architectural rule evaluators in `scripts/_code_health/profiles.py` for field injection, layering, transaction boundaries, and query concatenation
- [ ] T027 [US3] Implement workspace auto-detection of Spring Boot in `resolve_active_profiles()` inspecting `pom.xml`, `build.gradle`, or source imports (`org.springframework.*`)
- [ ] T028 [US3] [REVIEW] **Checkpoint**: User Story 3 fully functional. Verify clean Spring Boot service scores Grade A and anti-patterns receive exact line-numbered deductions.

---

## Phase 6: User Story 4 - Multi-Language Quality Gates and CI Integration (Priority: P4)

**Goal**: Support CI enforcement via `--fail-under` and recognize Java test frameworks (JUnit 5, AssertJ, MockMvc).  
**Independent Test**: Run `code_health.py` with `--fail-under` against clean vs failing Java projects; verify exit codes 0 and 1. Verify Java test assertion counting.

### Tests for User Story 4

> Write these tests FIRST in `tests/unit/test_java_spring_health.py`. Verify they FAIL before implementation.

- [ ] T029 [P] [TDD] [US4] Write unit tests for Java test assertion recognition (`@Test`, `assertEquals`, `assertThat`, MockMvc `.andExpect()`)
- [ ] T030 [P] [TDD] [US4] Write unit tests verifying `--fail-under` gate exits with code 1 when composite score is below threshold on Java projects

### Implementation for User Story 4

- [ ] T031 [US4] Implement Java test assertion detector in `scripts/_code_health/java_parser.py` and `profiles.py`
- [ ] T032 [US4] Add `--lang` and `--framework` CLI argument overrides in `scripts/code_health.py`
- [ ] T033 [US4] [REVIEW] **Checkpoint**: User Story 4 verified. Quality gates and test suites work seamlessly across Python and Java.

---

## Phase 7: Polish, Generic Skill Scaffolding & Self-Health Dogfooding Gate

**Purpose**: Agent skill authoring, documentation, and quality verification

- [ ] T034 [P] Create generic agent skill at `skills/code-health/SKILL.md` with auto-detection instructions, missing parser protocol, and playbook links
- [ ] T035 [P] Create Spring Boot refactoring playbook at `skills/code-health/references/java-spring-playbook.md`
- [ ] T036 [P] Update `skills/code-health/references/scoring-rubric.md` documenting Java metrics and Spring Boot rules
- [ ] T037 Sync updated `scripts/` engine into `skills/code-health/scripts/` and `skills/python-code-health/scripts/`
- [ ] T038 Run full test suite: `uv run pytest tests/unit/`
- [ ] T039 [REVIEW] Run dogfooding self-health check: `uv run python scripts/code_health.py scripts tests --fail-under 90.0 --no-git` verifying Grade A ($\ge 90.0$) across all codebase files

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately.
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories.
- **User Stories (Phases 3–6)**:
  - Phase 3 (US1: Core Java AST & Discovery) is the core multi-language engine.
  - Phase 4 (US2: Parser Guard) protects execution when grammar wheels are absent.
  - Phase 5 (US3: Spring Boot Rules) builds on Java AST extraction.
  - Phase 6 (US4: CI Quality Gates) integrates full test assertion & threshold rules.
- **Polish (Phase 7)**: Depends on all user stories passing verification.

### Within Each User Story

1. Tests marked `[TDD]` MUST be written and fail before implementation code.
2. IR models and parsers before profile rule evaluators.
3. Rule evaluators before CLI/runner wiring.
4. Checkpoints marked `[REVIEW]` require verification before moving to the next phase.

---

## Superpowers Execution

### Execution Discipline by Marker

- **[TDD]**: Follow RED-GREEN-REFACTOR. Write failing test in `tests/unit/test_java_spring_health.py` → run test to confirm failure → write minimal implementation → confirm pass → refactor for clean code health.
- **[SUBAGENT]**: Tasks marked `[SUBAGENT]` can be dispatched to parallel subagents.
- **[REVIEW]**: Checkpoints require pausing, running verification, and confirming explicit pass criteria.
- **[P]**: Parallel tasks across independent files can execute concurrently.

### Checkpoint Protocol

At every phase boundary:
1. Summarize completed tasks in the phase.
2. Run `uv run pytest tests/unit/` to confirm green tests.
3. Verify no regressions on existing Python scorecards.
4. Report status to user before advancing.
