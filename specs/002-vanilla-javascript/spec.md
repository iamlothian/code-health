# Feature Specification: Vanilla JavaScript (ECMAScript) Language Profile

**Feature Branch**: `add_vanilla_javascript`

**Created**: 2026-11-09

**Status**: Draft

**Input**: User description: "Please add support for vanilla javascript. Lets keep the basic profile for the javascript ecmascript language, we can later add framework and environment variants like node.js and jquery. No jsDoc required, they are encouraged though, rather type inference should be used, for JS it's important for readers to be able to reason what an object structure is and what types a variable contains, relying on type coercion too much can make that difficult."

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Automatic JavaScript Source Discovery and Health Evaluation (Priority: P1)

As a developer or AI coding agent working in JavaScript or polyglot codebases, I want the code health analyzer to automatically discover `.js`, `.mjs`, and `.cjs` files and evaluate them on a deterministic 0–100 scale (Grades A–F), so that I get an immediate, objective assessment of code quality and maintainability without manual configuration.

**Why this priority**: Core value of the analyzer. Users should be able to point the CLI at any JavaScript file or polyglot project directory and receive an objective health scorecard.

**Independent Test**: Can be tested independently by running `python scripts/code_health.py` against a JavaScript file and verifying that functions, classes, methods, and file metrics are parsed, graded, and displayed with exact line numbers.

**Acceptance Scenarios**:

1. **Given** a directory containing `.js`, `.mjs`, or `.cjs` source files and native parser dependencies installed, **When** `code_health.py` is executed pointing to that directory, **Then** the system automatically discovers the JavaScript files, computes composite and dimension scores (SRP, Size, Complexity, Clean Code, Security), assigns a letter grade (A–F), and reports line-numbered findings.
2. **Given** a polyglot repository containing Python, Java, and JavaScript files, **When** `code_health.py` scans the root directory, **Then** all three languages are evaluated according to their respective rules and aggregated into a unified repository scorecard.
3. **Given** a project containing a `node_modules`, `dist`, or `build` directory, **When** the analyzer runs across the project, **Then** vendor and artifact directories are automatically ignored without requiring explicit CLI ignore flags.

---

### User Story 2 - Missing Native Parser Guard and Actionable Installation Prompt (Priority: P2)

As a developer or CI engineer analyzing JavaScript in an environment where optional native parsing packages (`tree-sitter` and `tree-sitter-javascript`) are not installed, I want the tool to halt immediately with exit code 2 and display exact copy-paste installation commands, so that I can resolve missing dependencies without guesswork or silent degraded parsing.

**Why this priority**: Strict AST fidelity is a core architectural invariant. Heuristic or regex parsing produces flawed complexity and cohesion metrics. A fail-fast guard with actionable guidance ensures reliable results.

**Independent Test**: Can be tested by running the analyzer against a `.js` file in an environment lacking `tree-sitter-javascript` and verifying that the process halts with exit code 2 and outputs copy-paste `uv` and `pip` installation commands.

**Acceptance Scenarios**:

1. **Given** an environment without `tree-sitter-javascript` installed, **When** `code_health.py` is invoked targeting a `.js` file or directory with JavaScript source files, **Then** execution terminates with exit code `2`, printing a prominent warning that native AST analysis requires `tree-sitter-javascript` and displaying exact installation commands for `uv` and `pip`.
2. **Given** an environment without `tree-sitter-javascript` installed, **When** `code_health.py` is invoked with `--format json` targeting JavaScript files, **Then** the process emits a JSON document with `"status": "missing_native_parser"`, package names, and copy-paste install commands, exiting with code 2.
3. **Given** an environment without `tree-sitter-javascript` installed, **When** `code_health.py` is invoked purely on Python or Java files, **Then** execution succeeds without triggering JavaScript parser warnings.

---

### User Story 3 - Type Reasoning, Anti-Coercion, and Clean Code Quality (Priority: P3)

As a developer writing or reviewing vanilla JavaScript, I want the scorecard to reward clear type reasoning (such as parameter default values and JSDoc) while penalizing excessive implicit type coercion (like loose equality `==`/`!=`) and legacy patterns (`var`, empty `catch` blocks), so that code maintainability and predictability are preserved without mandating verbose annotations for every function.

**Why this priority**: In dynamically typed ECMAScript, reasoning about object structure and parameter types without unintended coercion bugs is essential for long-term health. Mandating JSDoc on every helper function is overly dogmatic, but penalizing un-defaulted, untyped parameters and loose equality enforces clarity.

**Independent Test**: Can be tested by analyzing a clean JavaScript file using modern ES6+ idioms (default parameters, strict equality `===`, `const`/`let`) against a file containing `var`, `==`, un-defaulted untyped parameters, and empty `catch` blocks, verifying exact penalty deductions.

**Acceptance Scenarios**:

1. **Given** a JavaScript function with default parameter initializers (e.g., `function connect(host = "localhost", port = 8080)`), **When** evaluated, **Then** the parameters are inferred as typed and receive zero parameter typing penalties.
2. **Given** a non-test JavaScript function declaring parameters with neither default initializers nor JSDoc `@param {type}` tags, **When** evaluated, **Then** the Clean Code dimension deducts `-2.0 pts` per untyped parameter (capped at `-10.0 pts`) and flags the unannotated parameter.
3. **Given** code utilizing loose equality operators (`==` or `!=`), **When** evaluated, **Then** the Clean Code dimension deducts `-2.0 pts` per operator (capped at `-10.0 pts`), warning that implicit type coercion obscures comparisons.
4. **Given** code containing legacy `var` declarations, **When** evaluated, **Then** the Clean Code dimension deducts `-3.0 pts` per `var` statement (capped at `-15.0 pts`), recommending `const` or `let`.
5. **Given** a `catch` block with an empty body, **When** evaluated, **Then** the Clean Code dimension deducts `-10.0 pts` for swallowed exceptions.

---

### User Story 4 - Core Language Security and Boundary Hygiene (Priority: P4)

As a security-conscious engineer, I want the code health scorecard to flag dangerous ECMAScript dynamic execution sinks and prototype pollution patterns, so that security vulnerabilities are surfaced during local development and CI quality gates.

**Why this priority**: Dynamic code evaluation (`eval`, `new Function`) and direct prototype modification (`__proto__`) represent major attack vectors in JavaScript applications.

**Independent Test**: Can be tested by running the analyzer against JavaScript files with `eval()`, `new Function()`, `setTimeout("code", delay)`, and `obj.__proto__` mutations, confirming exact Security deductions and findings.

**Acceptance Scenarios**:

1. **Given** a function invoking `eval(...)` or `new Function(...)`, **When** analyzed, **Then** the Security dimension deducts `-40.0 pts` and flags unsafe dynamic evaluation.
2. **Given** a call to `setTimeout(...)` or `setInterval(...)` where the first argument is a string literal, **When** analyzed, **Then** the Security dimension deducts `-20.0 pts` for implicit string evaluation.
3. **Given** an assignment or property access mutating `__proto__`, **When** analyzed, **Then** the Security dimension deducts `-25.0 pts` for dangerous prototype modification.
4. **Given** code containing a `with (...)` statement or lingering `debugger;` statement, **When** analyzed, **Then** `with` deducts `-30.0 pts` under Security for scope obscurity, and `debugger;` deducts `-10.0 pts` under Clean Code for lingering debug artifacts.

---

### User Story 5 - Test Suite and Assertion Hygiene Recognition (Priority: P5)

As an engineer maintaining JavaScript test suites, I want test files (`*.test.js`, `*.spec.js`, `__tests__/`) and BDD test blocks (`it`, `test`) to be automatically recognized, with their assertions evaluated, so that tests are not incorrectly penalized for missing docstrings or class structures.

**Why this priority**: Testing files follow distinct idioms (BDD callbacks, assertion chains). Without test-specific recognition, tests trigger false positives on SRP, docstrings, or size rules.

**Independent Test**: Can be tested by running the analyzer against test files with Jest/Mocha/Vitest-style test suites, verifying that assertion counts (`expect`, `assert`, `should`) are properly recognized and tests with 0 assertions or >8 assertions are flagged appropriately.

**Acceptance Scenarios**:

1. **Given** a file matching test patterns (`*.test.js`, `*.spec.js`, `__tests__/*`), **When** analyzed, **Then** it is marked as a test file, exempting it from source-level docstring and module SRP rules.
2. **Given** test blocks defined via `it("title", () => { ... })` or `test("title", () => { ... })`, **When** analyzed, **Then** each callback is extracted as an `IRFunction` with `is_test=True` and its name set to the test title.
3. **Given** a test function containing zero assertion calls (`expect`, `assert`, `should`, `toBe`, `toEqual`), **When** analyzed, **Then** the test receives a `-30.0 pt` penalty in Clean Code for having 0 assertions.
4. **Given** a test function containing more than 8 assertions, **When** analyzed, **Then** it receives a deduction of `-3.0 pts` per excess assertion (capped at `-30.0 pts`).

---

### Edge Cases

- **Procedural Script Files (No Functions or Classes)**: Files containing purely top-level procedural statements are scored at the module level for LOC, Git churn, and module-level hygiene without crashing.
- **Empty or Comment-Only Files**: Empty `.js` files or files containing only license headers/comments receive a score of 100.0 (Grade A) with zero penalties.
- **Modern ECMAScript Features**: Arrow functions with expression bodies (`x => x * 2`), destructuring parameters, rest parameters (`...args`), async/await, generators, nullish coalescing (`??`), and optional chaining (`?.`) parse cleanly and calculate cyclomatic/cognitive complexity accurately.
- **Inline Callbacks and Anonymous Closures**: Inline callbacks passed to array methods (`.map()`, `.filter()`, `.reduce()`), event handlers, or IIFEs are absorbed into their enclosing parent function's metrics (contributing to its LOC, cyclomatic/cognitive complexity, and nesting depth) rather than generating standalone `<anonymous>` function reports. Only top-level function declarations, class/object methods, and functions assigned to named variables (`const fn = () => {}`) are extracted as discrete unit scorecards.
- **Object Literal Methods and Class Fields**: Methods declared in ES6 classes or object literals (`const obj = { method() {} }`) are extracted as functions with proper qualifying names.
- **Vendor & Build Directories**: Standard JavaScript distribution directories (`node_modules`, `dist`, `build`, `.next`, `.nuxt`) are ignored during recursive directory scans.
- **Minified and Bundled Assets**: Files ending in `*.min.js` or files where line length exceeds 1,000 characters within the first 50 lines are identified as generated or minified bundles. They are automatically skipped during directory scans with an informative message (`"Skipped minified asset: <path>"`), preventing artificial LOC and complexity spikes from corrupting repository scorecards.
- **Malformed Syntax or Parse Errors**: If a JavaScript file contains invalid syntax (indicated by syntax error nodes in the tree-sitter CST), the analyzer records a file-level finding with the line number, grades the file as 0.0 (Grade F), and continues scanning the remainder of the repository without terminating the process.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST automatically detect JavaScript source files by file extension (`.js`, `.mjs`, `.cjs`) during file discovery unless overridden via `--lang`.
- **FR-002**: System MUST support `--lang javascript` and alias `--lang js` CLI flags to restrict analysis targets to JavaScript.
- **FR-003**: System MUST require native `tree-sitter` and `tree-sitter-javascript` packages for JavaScript CST analysis, strictly forbidding regex or heuristic fallback parsers.
- **FR-004**: System MUST halt execution with exit code `2` when `tree-sitter` or `tree-sitter-javascript` is missing when targeting JavaScript files, outputting clear `uv` and `pip` installation commands in console and JSON formats.
- **FR-005**: System MUST translate parsed JavaScript AST/CST nodes into the language-neutral Intermediate Representation (`IRModule`, `IRClass`, `IRFunction`, `IRField`, `IRCall`, `IRAnnotation`, `IRExceptHandler`).
- **FR-006**: System MUST evaluate JavaScript code against the universal 5-dimension rubric:
  - Single Responsibility & Cohesion (30%)
  - Size & Conciseness (20%)
  - Complexity & Readability (25%)
  - Clean Code & Maintainability (15%)
  - Security & Operational Hygiene (10%)
- **FR-007**: System MUST calculate Cyclomatic Complexity for JavaScript functions by counting branching constructs: `if_statement`, `switch_case`, `for_statement`, `for_in_statement`, `for_of_statement`, `while_statement`, `do_statement`, `catch_clause`, `ternary_expression`, and logical binary expressions (`&&`, `||`, `??`).
- **FR-008**: System MUST calculate Cognitive Complexity with nesting penalties for nested control flow structures, catch blocks, and ternary expressions.
- **FR-009**: System MUST calculate LCOM4 class cohesion for ES6 classes by analyzing method accesses to `this.<field>` properties.
- **FR-010**: System MUST infer parameter types from default initializers (`param = defaultValue`) or JSDoc `@param {type}` tags, deducting `-2.0 pts` (cap `-10.0 pts`) only for un-defaulted, untyped parameters in non-test functions.
- **FR-011**: System MUST penalize loose equality operators (`==`, `!=`) by deducting `-2.0 pts` per occurrence (cap `-10.0 pts`) under Clean Code.
- **FR-012**: System MUST penalize legacy `var` declarations by deducting `-3.0 pts` per declaration (cap `-15.0 pts`) under Clean Code.
- **FR-013**: System MUST penalize dynamic evaluation (`eval(...)`, `new Function(...)`) by deducting `-40.0 pts` under Security.
- **FR-014**: System MUST penalize timer string execution (`setTimeout("string", ...)` / `setInterval("string", ...)`) by deducting `-20.0 pts` under Security.
- **FR-015**: System MUST penalize direct prototype mutations (`__proto__`) by deducting `-25.0 pts` under Security.
- **FR-016**: System MUST recognize JavaScript test files (`*.test.js`, `*.spec.js`, `*_test.js`, and files within `test/`, `tests/`, `__tests__/`), extracting BDD test blocks (`it`, `test`) and recognizing assertion matchers (`assert`, `expect`, `should`, `toBe`, `toEqual`, `to.equal`).
- **FR-017**: System MUST automatically ignore vendor and build directories (`node_modules`, `dist`, `build`, `.next`, `.nuxt`) during codebase directory traversal.
- **FR-018**: System MUST support Git commit churn, touch count, and co-change coupling for `.js`, `.mjs`, and `.cjs` files identically to `.py` and `.java` files.
- **FR-019**: System MUST maintain 100% backward compatibility for all existing Python and Java AST analysis, CLI arguments, and output schemas.
- **FR-020**: System MUST extract function declarations, class/object methods, and functions assigned to named variables as discrete `IRFunction` units, while absorbing inline anonymous callbacks into the enclosing parent function's scope metrics.
- **FR-021**: System MUST handle malformed JavaScript files containing syntax errors gracefully by recording a file-level syntax error finding with line location and assigning the file a score of 0.0 (Grade F), without halting the analysis of other repository files.
- **FR-022**: System MUST automatically detect and skip minified or bundled JavaScript files (identifying `*.min.js` and files exceeding 1,000 characters per line within the first 50 lines), logging a notice and excluding them from aggregate codebase scoring.
- **FR-023**: System MUST penalize `with` statements by deducting `-30.0 pts` under Security & Operational Hygiene.
- **FR-024**: System MUST penalize `debugger;` statements by deducting `-10.0 pts` under Clean Code & Maintainability.
- **FR-025**: System MUST assign hierarchical qualifying names (`qualname`) using dot notation for classes (`Class.method`), object literals (`object.method`), and assigned variable identifiers for arrow functions, enabling uniform symbol display and `--symbol` CLI filtering.

---

### Key Entities

- **JavaScriptLanguageProfile**: Language profile defining ECMAScript file extensions (`.js`, `.mjs`, `.cjs`), JSDoc conventions, anti-coercion checks (`==`/`!=`), legacy variable detection (`var`), security evaluation (`eval`, `new Function`, string timers, prototype mutation), and test assertion recognition.
- **IRModule / IRClass / IRFunction**: Language-neutral data models extended with backward-compatible optional fields (`var_declarations_count`, `loose_comparisons_count`, `has_proto_mutation`) representing parsed code elements.
- **JavaScriptParser**: Subsystem utilizing `tree-sitter-javascript` to construct Concrete Syntax Trees and transform them into normalized IR units.
- **ParserGuard**: Validation guard ensuring `tree-sitter` and `tree-sitter-javascript` are available, halting with exit code `2` upon absence.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of existing unit tests in `tests/unit/` (Python and Java test suites) pass without modification.
- **SC-002**: A clean JavaScript module utilizing ES6+ standards, default parameters, and strict equality achieves a composite score $\ge 90.0$ (Grade A) with zero critical findings.
- **SC-003**: A smell-laden JavaScript module containing `var`, loose equality `==`, empty `catch` blocks, `eval`, string timers, and un-defaulted untyped parameters triggers exact line-numbered findings with corresponding penalty deductions, dropping its grade to C, D, or F.
- **SC-004**: When `tree-sitter-javascript` is not installed, 100% of invocations targeting JavaScript files halt with exit code `2` and display copy-paste installation commands in both console and JSON modes.
- **SC-005**: File discovery automatically ignores `node_modules`, `dist`, and `build` directories, preventing scanning of third-party package code.
- **SC-006**: AST parsing and scoring of a standard JavaScript file (<300 LOC) completes in under 500ms in `--no-git` mode.
- **SC-007**: All new Python source files introduced to support JavaScript achieve a self-health composite score $\ge 90.0$ (Grade A).

---

## Assumptions

- **Target Language Standard**: Targets modern ECMAScript standard specifications (ES6 through ES2024+), parsed via `tree-sitter-javascript`.
- **Environment Variants Out of Scope**: Framework- and environment-specific profiles (e.g. Node.js backend APIs, DOM APIs, jQuery, Express, React) are explicitly deferred to future profile extensions.
- **Dependency Packaging**: Core Python analysis remains 100% zero-dependency. JavaScript analysis requires optional dependencies declared under `[project.optional-dependencies] javascript = ["tree-sitter>=0.23.0", "tree-sitter-javascript>=0.23.0"]`.
- **Operating Systems**: Supported across Windows, macOS, and Linux without platform-specific code paths.

---

## Open Questions & Brainstorm Log

### Open Questions

| ID | Category | Question | Status | Resolution |
|:---|:---|:---|:---|:---|
| OQ-001 | Boundary Conditions | How should inline callbacks, arrow expressions, and IIFEs be extracted and scored? | Resolved | Option A: Parent Scope Absorption. Extract only top-level declarations, class/object methods, and named functions (`const fn = () => {}`); inline callbacks contribute to enclosing scope metrics. |
| OQ-002 | Error Scenarios | How should syntax errors or malformed JavaScript files be handled? | Resolved | Option A: Resilient Skip & Grade F. Record a file-level finding with the line number and grade the file 0.0 (Grade F), allowing multi-file scans to continue smoothly. |
| OQ-003 | Scale & Performance | How should minified, generated, or bundled JavaScript files be handled? | Resolved | Option A: Automatic Detection & Skip. Skip `*.min.js` and files with lines exceeding 1,000 characters in the first 50 lines to prevent distorted LOC/complexity metrics. |
| OQ-004 | Security & Hygiene | How should deprecated/dangerous ECMAScript statements (`with` and `debugger`) be penalized? | Resolved | Option A: Penalize Both. `with` incurs `-30.0 pts` under Security/Operational Hygiene, and `debugger;` incurs `-10.0 pts` under Clean Code. |
| OQ-005 | User Experience | How should function and method qualifying names (`qualname`) be formatted for CLI reports and `--symbol`? | Resolved | Option A: Hierarchical Dot-Notation. Use `Class.method`, `object.method`, and assigned variable identifier for arrow functions. |

### Brainstorm Log

- **2026-11-09**: Initialized speckit-superspec brainstorming session. Explored Category 1 (Boundary Conditions & Code Unit Granularity). Resolved OQ-001: inline callbacks (`.map()`, `.filter()`, IIFEs) are absorbed into parent function metrics rather than generating separate `<anonymous>` scorecard entries, preventing scorecard clutter while preserving complexity fidelity.
- **2026-11-09**: Explored Category 2 (Error Scenarios & Syntax Fault Tolerance). Resolved OQ-002: syntax errors trigger a file-level finding with Grade F (0.0) without crashing broader repository analysis.
- **2026-11-09**: Explored Category 3 (Scale, Performance & Bundled Assets). Resolved OQ-003: automated skip for `*.min.js` and minified/bundled scripts with extreme line lengths (>1,000 chars), ensuring clean repository metrics.
- **2026-11-09**: Explored Category 4 (Security & Operational Hygiene Language Constructs). Resolved OQ-004: penalized `with` (-30.0 pts Security) and `debugger;` (-10.0 pts Clean Code) with line-numbered findings.
- **2026-11-09**: Explored Category 5 (User Experience & Symbol Qualnames). Resolved OQ-005: standardized hierarchical dot-notation (`Class.method`, `object.method`, variable name) for symbol representation and `--symbol` CLI filtering.

