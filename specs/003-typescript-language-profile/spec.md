# Feature Specification: TypeScript Language Profile

**Feature Branch**: `add_typescript_support`

**Created**: 2026-11-09

**Status**: Draft

**Input**: User description: "I want to add typescript language support"

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Automatic TypeScript & TSX Source Discovery and Health Evaluation (Priority: P1)

As a developer or AI coding agent working in TypeScript or polyglot codebases, I want the code health analyzer to automatically discover `.ts`, `.tsx`, `.mts`, and `.cts` files and evaluate them on a deterministic 0–100 scale (Grades A–F), so that I get an immediate, objective assessment of code quality and maintainability without manual configuration.

**Why this priority**: Core value of the analyzer. Users must be able to point the CLI at any TypeScript file or polyglot project directory and receive an objective health scorecard covering functions, classes, methods, and module metrics.

**Independent Test**: Can be tested independently by running `python scripts/code_health.py` against a TypeScript file or TSX file and verifying that functions, classes, methods, and file metrics are parsed, graded, and displayed with exact line numbers.

**Acceptance Scenarios**:

1. **Given** a directory containing `.ts`, `.tsx`, `.mts`, or `.cts` source files and native parser dependencies installed, **When** `code_health.py` is executed pointing to that directory, **Then** the system automatically discovers the TypeScript files, computes composite and dimension scores (SRP, Size, Complexity, Clean Code, Security), assigns a letter grade (A–F), and reports line-numbered findings.
2. **Given** a polyglot repository containing Python, Java, JavaScript, and TypeScript files, **When** `code_health.py` scans the root directory, **Then** all four languages are evaluated according to their respective rules and aggregated into a unified repository scorecard.
3. **Given** a project containing a `node_modules`, `dist`, or `build` directory, **When** the analyzer runs across the project, **Then** vendor and artifact directories are automatically ignored without requiring explicit CLI ignore flags.
4. **Given** a project containing ambient declaration files (`*.d.ts`, `*.d.mts`, `*.d.cts`), **When** file discovery traverses the directory, **Then** ambient declaration files are automatically excluded from analysis because they contain no executable logic.

---

### User Story 2 - Missing Native Parser Guard and Actionable Installation Prompt (Priority: P2)

As a developer or CI engineer analyzing TypeScript in an environment where optional native parsing packages (`tree-sitter` and `tree-sitter-typescript`) are not installed, I want the tool to halt immediately with exit code 2 and display exact copy-paste installation commands, so that I can resolve missing dependencies without guesswork or silent degraded parsing.

**Why this priority**: Strict AST fidelity is a core architectural invariant. Heuristic or regex parsing produces flawed complexity and cohesion metrics. A fail-fast guard with actionable guidance ensures reliable results.

**Independent Test**: Can be tested by running the analyzer against a `.ts` file in an environment lacking `tree-sitter-typescript` and verifying that the process halts with exit code 2 and outputs copy-paste `uv` and `pip` installation commands.

**Acceptance Scenarios**:

1. **Given** an environment without `tree-sitter-typescript` installed, **When** `code_health.py` is invoked targeting a `.ts` or `.tsx` file, **Then** execution terminates with exit code `2`, printing a prominent warning that native AST analysis requires `tree-sitter-typescript` and displaying exact installation commands for `uv` and `pip`.
2. **Given** an environment without `tree-sitter-typescript` installed, **When** `code_health.py` is invoked with `--format json` targeting TypeScript files, **Then** the process emits a JSON document with `"status": "missing_native_parser"`, package names, and copy-paste install commands, exiting with code 2.
3. **Given** an environment without `tree-sitter-typescript` installed, **When** `code_health.py` is invoked purely on Python, Java, or JavaScript files, **Then** execution succeeds without triggering TypeScript parser warnings.

---

### User Story 3 - Strict Typing, Clean Code, and Type Safety Escape Hatch Detection (Priority: P3)

As a developer writing or reviewing TypeScript, I want the scorecard to enforce strict signature typing and penalize type safety escape hatches (`any`, `@ts-ignore`, `@ts-nocheck`, `!`), while rewarding idiomatic type annotations and clean code, so that code maintainability and compiler guarantees are preserved.

**Why this priority**: TypeScript's primary value is compile-time type safety and self-documenting code contracts. Permitting untyped signatures, unconstrained `any`, compiler suppressions, or non-null assertions defeats these benefits and breeds hidden runtime bugs.

**Independent Test**: Can be tested by analyzing a clean TypeScript file (strictly typed parameters, explicit return types, no `any`, strict equality) against a smelly file containing `any`, `@ts-ignore`, non-null assertions `!`, untyped parameters, missing return types, and loose equality `==`, verifying exact penalty deductions.

**Acceptance Scenarios**:

1. **Given** a non-test TypeScript function declaring parameters without type annotations and without default initializers, **When** evaluated, **Then** Clean Code deducts `-5.0 pts` per untyped parameter (capped at `-25.0 pts`).
2. **Given** a function parameter with a default initializer (e.g., `value = 10`) or optional marker (`name?: string`), **When** evaluated, **Then** it is recognized as typed and receives zero untyped parameter penalty.
3. **Given** a non-test, non-constructor function missing an explicit return type annotation, **When** evaluated, **Then** Clean Code deducts `-10.0 pts`.
4. **Given** code utilizing explicit `any` (`: any`, `as any`, `<any>x`, `Array<any>`), **When** evaluated, **Then** Clean Code deducts `-5.0 pts` per occurrence (capped at `-20.0 pts`).
5. **Given** comments containing compiler suppression directives (`@ts-ignore` or `@ts-nocheck`), **When** evaluated, **Then** Clean Code deducts `-10.0 pts` per directive (capped at `-20.0 pts`), whereas `@ts-expect-error` is not penalized.
6. **Given** expressions utilizing the non-null assertion operator (`!`), **When** evaluated, **Then** Clean Code deducts `-2.0 pts` per occurrence (capped at `-10.0 pts`).
7. **Given** a function declaring a boolean parameter with a default value (`flag: boolean = false` or `flag = false`), **When** evaluated, **Then** Single Responsibility (SRP) deducts `-6.0 pts` for a boolean flag parameter.
8. **Given** code containing loose equality (`==`/`!=`), `var` declarations, empty `catch` blocks, or lingering `debugger;` statements, **When** evaluated, **Then** Clean Code deducts corresponding ECMAScript hygiene penalties.

---

### User Story 4 - Core Language Security and Boundary Hygiene (Priority: P4)

As a security-conscious engineer, I want the code health scorecard to flag dangerous dynamic execution sinks, timer string evaluations, prototype pollution patterns, and SQL/query string concatenations, so that vulnerabilities are surfaced during local development and CI quality gates.

**Why this priority**: Dynamic code execution (`eval`, `new Function`), direct prototype tampering (`__proto__`), and unparameterized SQL/database queries represent critical security vulnerabilities in TypeScript server-side and client-side applications.

**Independent Test**: Can be tested by running the analyzer against TypeScript files with `eval()`, `new Function()`, `setTimeout("code", delay)`, `obj.__proto__` mutations, and query calls with string concatenation, confirming exact Security deductions and findings.

**Acceptance Scenarios**:

1. **Given** a function invoking `eval(...)` or `new Function(...)`, **When** analyzed, **Then** Security deducts `-40.0 pts` and flags unsafe dynamic evaluation.
2. **Given** a call to `setTimeout(...)` or `setInterval(...)` where the first argument is a string literal, **When** analyzed, **Then** Security deducts `-20.0 pts` for implicit string evaluation.
3. **Given** an assignment or property access mutating `__proto__` or calling `Object.setPrototypeOf`, **When** analyzed, **Then** Security deducts `-25.0 pts` for dangerous prototype modification.
4. **Given** code containing a `with (...)` statement, **When** analyzed, **Then** Security deducts `-30.0 pts` for scope obscurity.
5. **Given** a database or ORM query method (`query`, `execute`, `raw`, `$queryRawUnsafe`, `$executeRawUnsafe`) called with a string concatenation (`+`) or template literal interpolation (`${...}`), **When** analyzed, **Then** Security deducts `-40.0 pts` for potential SQL/query injection.

---

### User Story 5 - Test Suite and Assertion Hygiene Recognition (Priority: P5)

As an engineer maintaining TypeScript test suites, I want test files (`*.test.ts`, `*.spec.ts`, `*.test.tsx`, `*.spec.tsx`, `__tests__/`) and BDD test blocks (`it`, `test`) to be automatically recognized, with their assertions evaluated, so that tests are not incorrectly penalized for missing docstrings or class structures.

**Why this priority**: Testing files follow distinct idioms (BDD callbacks, assertion chains). Without test-specific recognition, tests trigger false positives on SRP, docstrings, or size rules.

**Independent Test**: Can be tested by running the analyzer against TypeScript test files with Jest/Vitest/Mocha test suites, verifying that assertion counts (`expect`, `assert`, `should`, `toBe`, `toEqual`) are recognized and tests with 0 assertions or >8 assertions are flagged appropriately.

**Acceptance Scenarios**:

1. **Given** a file matching test patterns (`*.test.ts`, `*.spec.ts`, `*.test.tsx`, `*.spec.tsx`, `__tests__/*`), **When** analyzed, **Then** it is marked as a test file, exempting it from source-level docstring and module SRP rules.
2. **Given** test blocks defined via `it("title", () => { ... })` or `test("title", () => { ... })`, **When** analyzed, **Then** each callback is extracted as an `IRFunction` with `is_test=True` and its name set to the test title.
3. **Given** a test function containing zero assertion calls (`expect`, `assert`, `should`, `toBe`, `toEqual`), **When** analyzed, **Then** Clean Code deducts `-30.0 pts` for 0 assertions.
4. **Given** a test function containing more than 8 assertions, **When** analyzed, **Then** Clean Code deducts `-3.0 pts` per excess assertion (capped at `-30.0 pts`).

---

### Edge Cases

- **TSX and JSX Expressions**: Components defined in `.tsx` files containing JSX syntax (`<Component prop={val} />`) parse cleanly via `tree_sitter_typescript.language_tsx()` without syntax errors or artificial LOC/complexity distortion.
- **Constructor Parameter Properties**: Classes declaring parameter properties in constructors (`constructor(private readonly service: Service, public count = 0)`) have those properties extracted as `IRField` instances on the class, allowing LCOM4 cohesion analysis to properly link methods that access `this.service` or `this.count`.
- **Pure Contracts (Interfaces & Type Aliases)**: Module-level `interface` and `type` declarations contribute to module effective LOC but are not emitted as behavioral `IRClass` instances, preventing false penalties for missing methods or disconnected LCOM4 components.
- **Abstract Classes and Methods**: Abstract classes (`abstract class C`) and abstract method signatures (`abstract run(): void;`) parse without errors and are extracted with proper qualifying names.
- **Empty or Comment-Only Files**: Empty `.ts` files or files containing only license headers and comments receive a score of 100.0 (Grade A) with zero penalties.
- **Minified and Bundled Assets**: Files ending in `*.min.ts` or files where line length exceeds 1,000 characters within the first 50 lines are identified as generated or minified bundles and skipped during directory scans.
- **Ambient Declaration Files**: Files ending in `*.d.ts`, `*.d.mts`, and `*.d.cts` are excluded during directory scans.
- **Malformed Syntax or Parse Errors**: If a TypeScript file contains invalid syntax (indicated by error nodes in the CST), the analyzer records a file-level finding with the line number, grades the file as 0.0 (Grade F), and continues scanning the remainder of the repository without crashing.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST automatically detect TypeScript source files by file extension (`.ts`, `.tsx`, `.mts`, `.cts`) during file discovery unless overridden via `--lang`.
- **FR-002**: System MUST support `--lang typescript` and alias `--lang ts` CLI flags to restrict analysis targets to TypeScript.
- **FR-003**: System MUST require native `tree-sitter` and `tree-sitter-typescript` packages for TypeScript CST analysis, strictly forbidding regex or heuristic fallback parsers.
- **FR-004**: System MUST halt execution with exit code `2` when `tree-sitter` or `tree-sitter-typescript` is missing when targeting TypeScript files, outputting clear `uv` and `pip` installation commands in console and JSON formats.
- **FR-005**: System MUST translate parsed TypeScript AST/CST nodes into the language-neutral Intermediate Representation (`IRModule`, `IRClass`, `IRFunction`, `IRField`, `IRCall`, `IRAnnotation`, `IRExceptHandler`).
- **FR-006**: System MUST evaluate TypeScript code against the universal 5-dimension rubric:
  - Single Responsibility & Cohesion (30%)
  - Size & Conciseness (20%)
  - Complexity & Readability (25%)
  - Clean Code & Maintainability (15%)
  - Security & Operational Hygiene (10%)
- **FR-007**: System MUST calculate Cyclomatic Complexity for TypeScript functions by counting branching constructs: `if_statement`, `switch_case`, `for_statement`, `for_in_statement`, `for_of_statement`, `while_statement`, `do_statement`, `catch_clause`, `ternary_expression`, and logical binary expressions (`&&`, `||`, `??`).
- **FR-008**: System MUST calculate Cognitive Complexity with nesting penalties for nested control flow structures, catch blocks, and ternary expressions.
- **FR-009**: System MUST calculate LCOM4 class cohesion for classes by analyzing method accesses to `this.<field>` properties, including fields declared via constructor parameter properties.
- **FR-010**: System MUST penalize unannotated, un-defaulted parameters in non-test functions by deducting `-5.0 pts` per untyped parameter (capped at `-25.0 pts`) under Clean Code.
- **FR-011**: System MUST penalize missing return type annotations on non-test, non-constructor functions by deducting `-10.0 pts` under Clean Code.
- **FR-012**: System MUST penalize explicit `any` usage (`: any`, `as any`, `<any>`, `Array<any>`) by deducting `-5.0 pts` per occurrence (capped at `-20.0 pts`) under Clean Code.
- **FR-013**: System MUST penalize compiler suppression directives (`@ts-ignore`, `@ts-nocheck`) in comments by deducting `-10.0 pts` per directive (capped at `-20.0 pts`) under Clean Code, while exempting `@ts-expect-error`.
- **FR-014**: System MUST penalize non-null assertion operators (`!`) by deducting `-2.0 pts` per occurrence (capped at `-10.0 pts`) under Clean Code.
- **FR-015**: System MUST penalize boolean default flag parameters (`flag: boolean = false` or `flag = false`) by deducting `-6.0 pts` under Single Responsibility (SRP).
- **FR-016**: System MUST penalize loose equality operators (`==`, `!=`) by deducting `-2.0 pts` per occurrence (cap `-10.0 pts`), legacy `var` declarations by deducting `-3.0 pts` per declaration (cap `-15.0 pts`), empty `catch` blocks by deducting `-10.0 pts`, and lingering `debugger;` statements by deducting `-10.0 pts` under Clean Code.
- **FR-017**: System MUST penalize dynamic evaluation (`eval(...)`, `new Function(...)`) by deducting `-40.0 pts`, timer string execution (`setTimeout("string", ...)` / `setInterval("string", ...)`) by deducting `-20.0 pts`, direct prototype mutations (`__proto__`, `Object.setPrototypeOf`) by deducting `-25.0 pts`, and `with` statements by deducting `-30.0 pts` under Security.
- **FR-018**: System MUST penalize database and ORM query calls (`query`, `execute`, `raw`, `$queryRawUnsafe`, `$executeRawUnsafe`) containing string concatenation or template literal interpolation by deducting `-40.0 pts` under Security.
- **FR-019**: System MUST recognize TypeScript test files (`*.test.ts`, `*.spec.ts`, `*_test.ts`, `*.test.tsx`, `*.spec.tsx`, etc.), extracting BDD test blocks (`it`, `test`) and recognizing assertion matchers (`assert`, `expect`, `should`, `toBe`, `toEqual`, `to.equal`).
- **FR-020**: System MUST automatically ignore vendor and build directories (`node_modules`, `dist`, `build`, `.next`, `.nuxt`) and ambient declaration files (`*.d.ts`, `*.d.mts`, `*.d.cts`) during file discovery.
- **FR-021**: System MUST support Git commit churn, touch count, and co-change coupling for `.ts`, `.tsx`, `.mts`, and `.cts` files identically to `.py`, `.java`, and `.js` files.
- **FR-022**: System MUST treat `interface` and `type` alias declarations as structural contracts rather than behavioral classes, exempting them from class LCOM4 penalties.
- **FR-023**: System MUST automatically detect and skip minified or bundled TypeScript files (`*.min.ts` and files exceeding 1,000 characters per line within the first 50 lines).
- **FR-024**: System MUST handle malformed TypeScript files containing syntax errors gracefully by recording a file-level syntax error finding with line location and assigning the file a score of 0.0 (Grade F), without halting the analysis of other repository files.
- **FR-025**: System MUST assign hierarchical qualifying names (`qualname`) using dot notation for classes (`Class.method`), object literals (`object.method`), and assigned variable identifiers for arrow functions.
- **FR-026**: System MUST maintain 100% backward compatibility for all existing Python, Java, and JavaScript AST analysis, CLI arguments, and output schemas.

---

### Key Entities

- **TypeScriptLanguageProfile**: Language profile defining TypeScript file extensions (`.ts`, `.tsx`, `.mts`, `.cts`), strict parameter typing, return type annotation enforcement, escape hatch detection (`any`, `@ts-ignore`, non-null assertions), query injection checking, and test assertion recognition.
- **TypeScriptParser**: Subsystem utilizing `tree-sitter-typescript` (`language_typescript` and `language_tsx`) to construct CSTs and transform them into normalized IR units (`IRModule`, `IRClass`, `IRFunction`, `IRField`).
- **IRFunction**: Language-neutral representation extended with backward-compatible telemetry fields (`explicit_any_count: int = 0`, `ts_ignore_count: int = 0`, `non_null_assertion_count: int = 0`).
- **ParserGuard**: Validation guard ensuring `tree-sitter` and `tree-sitter-typescript` are available, halting with exit code `2` upon absence.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of existing unit tests in `tests/unit/` (Python, Java, and JavaScript test suites) pass without modification.
- **SC-002**: A clean TypeScript module utilizing strict typing, explicit return types, no `any`, and no compiler suppression directives achieves a composite score $\ge 90.0$ (Grade A) with zero critical findings.
- **SC-003**: A smell-laden TypeScript module containing `any`, `@ts-ignore`, non-null assertions `!`, untyped parameters, missing return types, loose equality `==`, and `eval` triggers exact line-numbered findings with corresponding penalty deductions, dropping its grade to C, D, or F.
- **SC-004**: When `tree-sitter-typescript` is not installed, 100% of invocations targeting TypeScript files halt with exit code `2` and display copy-paste installation commands in both console and JSON modes.
- **SC-005**: File discovery automatically ignores `node_modules`, `dist`, `build`, and ambient declaration files (`*.d.ts`), preventing scanning of third-party package code or non-executable types.
- **SC-006**: AST parsing and scoring of a standard TypeScript file (<300 LOC) completes in under 500ms in `--no-git` mode.
- **SC-007**: All new Python source files introduced to support TypeScript achieve a self-health composite score $\ge 90.0$ (Grade A).

---

## Assumptions

- **Target Language Standard**: Targets modern TypeScript standard specifications (TS 5.x / ES2024+), parsed via `tree-sitter-typescript` with JSX support for `.tsx`.
- **Cross-File Type Checking Out of Scope**: Cross-file semantic type checking (such as executing `tsc` or running the TypeScript language service compiler) is out of scope; analysis is strictly fast, deterministic per-file CST parsing combined with repository Git history.
- **Framework Variants Deferred**: Framework-specific architectural rules (e.g., NestJS controllers, Angular components, React hooks) are deferred to future `FrameworkProfile` extensions.
- **Dependency Packaging**: Core Python analysis remains 100% zero-dependency. TypeScript analysis requires optional dependencies declared under `[project.optional-dependencies] typescript = ["tree-sitter>=0.23.0", "tree-sitter-typescript>=0.23.0"]`.
- **Operating Systems**: Supported across Windows, macOS, and Linux without platform-specific code paths.
