# Design Document: Vanilla JavaScript (ECMAScript) Language Profile

**Date**: 2026-11-09  
**Status**: Approved Candidate (Post-Builder Check)  
**Target Module**: `scripts/_code_health/`  

---

## 1. Intent and Why

`py-code-health` provides deterministic, zero-runtime-execution code health scorecards (0–100, Grade A–F) across five weighted dimensions: Single Responsibility & Cohesion (30%), Size & Readability (20%), Complexity & Control Flow (25%), Clean Code (15%), and Security (10%).

The tool previously supported Python (via standard library `ast`) and Java (via `tree-sitter-java`). Adding vanilla JavaScript (ECMAScript standard language) expands `py-code-health` to polyglot environments, web frontends, and script repositories without introducing external runtime dependencies on Node.js or npm.

---

## 2. Goals, Non-Goals, and Anti-Goals

### Goals
- **Full AST/CST Parse Fidelity**: Parse ECMAScript source files (`.js`, `.mjs`, `.cjs`) using `tree-sitter` and `tree-sitter-javascript` into the language-neutral Universal Intermediate Representation (`IRModule`, `IRClass`, `IRFunction`).
- **Comprehensive Unit Extraction**:
  - Functions: Function declarations (`function f() {}`), function expressions (`const f = function() {}`), arrow functions (`const f = () => {}`), generator functions (`function*`), async functions (`async function`), object/class methods, and BDD test blocks (`it(...)`, `test(...)`).
  - Classes: ES6 class definitions (`class C extends B {}`), constructors, instance/static methods, getters/setters, class fields.
  - Modules: Imports (`import ...`, `require(...)`), exports (`export ...`, `module.exports`), effective non-comment/non-blank LOC.
- **Five-Dimension Scoring**:
  - **Single Responsibility (30%)**: LCOM4 class cohesion (methods accessing fields / `this.x`), function fan-out, file-level function/class counts, Git churn and coupling.
  - **Size & Conciseness (20%)**: Effective LOC, parameter count (flagging >5 params), maximum nesting depth (flagging depth >3).
  - **Complexity & Readability (25%)**: Cyclomatic complexity (branching on `if`, `switch`/`case`, `for`, `while`, `do-while`, `catch`, ternary `? :`, logical short-circuits `&&`, `||`, nullish coalescing `??`), cognitive complexity (nesting penalties, break/continue), return statement count (>4).
  - **Clean Code & Idioms (15%)**:
    - Missing JSDoc documentation on public/exported functions & classes.
    - Parameter reasoning & type inference: JSDoc is encouraged but not strictly required. Parameters with default values (e.g. `param = 0`) are inferred as typed. Unannotated parameters without defaults lose `-2.0 pts` (cap `10.0 pts`).
    - Anti-coercion & code hygiene: Loose equality operators (`==`, `!=` triggering implicit type coercion: `-2.0 pts` each, cap `10.0 pts`), legacy `var` declarations (`-3.0 pts` each, cap `15.0 pts`), and empty `catch` blocks (`-10.0 pts`).
  - **Security & Hygiene (10%)**: Dynamic evaluation (`eval` and `new Function`: `-40.0 pts`), string arguments passed to timer APIs (`setTimeout("...")`, `setInterval("...")`: `-20.0 pts`), and direct prototype mutation (`__proto__`: `-25.0 pts`).
- **Missing Dependency Handling**: If `tree-sitter` or `tree-sitter-javascript` is missing when JavaScript files are targeted, halt immediately with exit code `2`, printing a prominent warning with copy-paste installation commands for `uv` and `pip` (in both console and JSON formats).
- **Directory and File Discovery**:
  - Automatically analyze `.js`, `.mjs`, `.cjs` files.
  - Automatically ignore `node_modules`, `dist`, `build`, `.next`, and `.nuxt` directories.
  - Support CLI overrides via `--lang javascript` (and alias `--lang js`).
- **Test Recognition**: Recognize test files by path/name (`*.test.js`, `*.spec.js`, `*_test.js`, or files within `test/`, `tests/`, `__tests__/`) and recognize test assertion calls (`assert`, `expect`, `should`, `toBe`, `toEqual`, `to.equal`).

### Non-Goals
- Runtime or environment variants (Node.js backend APIs like `child_process`/`fs`, browser DOM libraries, jQuery, Express, React). These will be implemented in subsequent framework profiles.
- TypeScript parsing (`.ts`, `.tsx`) or type-checking compilers.
- Formatting or AST code modification (the tool is read-only).

### Anti-Goals
- No regex/heuristic fallback parser for JavaScript. When `tree-sitter-javascript` is missing, the analyzer must fail fast with exit code 2 rather than emit inaccurate metrics.
- No dependency on Node.js, npm, or external subprocesses.

---

## 3. Constraints

- **Python Version**: Python >= 3.11 compatible stdlib.
- **Optional Native Parsers**: The core Python analyzer must remain zero-dependency. JavaScript parser packages (`tree-sitter`, `tree-sitter-javascript`) must be declared as optional dependencies under `[project.optional-dependencies] javascript = [...]`.
- **Consistency**: Output data structures (`CodebaseHealthReport`, `FileReport`, `ClassReport`, `FunctionReport`) and grading scale (`A`: 90–100, `B`: 80–89, `C`: 70–79, `D`: 60–69, `F`: <60) must remain strictly uniform across Python, Java, and JavaScript.

---

## 4. Evaluated Approaches

### Approach 1: Native Tree-Sitter CST via `tree-sitter-javascript` into Universal IR (Selected)
- **Mechanism**: Use `tree-sitter` and `tree-sitter-javascript` to parse JS into Concrete Syntax Trees, then traverse and normalize them into `IRModule`, `IRClass`, and `IRFunction`. Evaluate with `UniversalIRScorer`.
- **Pros**: Matches Java's design; provides 100% accurate AST across ES6+, modern syntax, closures, and arrow functions; zero Node.js runtime requirement.
- **Cons**: Requires optional native Python wheel `tree-sitter-javascript`.
- **Decision**: **Selected**. Chosen for deterministic scoring accuracy, architectural consistency, and parity with Java.

### Approach 2: External Node.js / ESTree CLI Bridge (Rejected)
- **Mechanism**: Execute a Node.js process using tools like Acorn/Espree to generate ESTree JSON, ingested via standard I/O.
- **Pros**: Uses JavaScript's native ecosystem.
- **Cons**: Requires Node.js installed on the host system; high subprocess invocation latency; violates the tool's standalone Python design.
- **Decision**: **Rejected**.

### Approach 3: Heuristic / Regex Tokenization (Rejected)
- **Mechanism**: Scan JavaScript source code using regex patterns and tokenizers.
- **Pros**: Zero third-party dependencies.
- **Cons**: Cannot reliably compute cognitive complexity, handle nested arrow functions or closures, parse multiline template literals, or inspect class field accesses for LCOM4.
- **Decision**: **Rejected**.

---

## 5. Architectural & Technical Specification

### 5.1 Architecture Overview

```
                      +-----------------------------+
                      |       code_health.py        |
                      |   CLI & Target Discovery    |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |       ModuleAnalyzer        |
                      |      (module_engine.py)     |
                      +--------------+--------------+
                                     |
               +---------------------+---------------------+
               |                     |                     |
               v                     v                     v
          .py files             .java files         .js / .mjs / .cjs
        (ast_engine.py)       (java_parser.py)        (js_parser.py)
               |                     |                     |
               v                     v                     v
          Python AST             Java CST            JavaScript CST
               |                     |                     |
               +---------------------+---------------------+
                                     |
                                     v
                      +-----------------------------+
                      |   Universal IR Structure    |
                      | (IRModule, IRClass, Func)   |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |      UniversalIRScorer      |
                      |    (with JAVASCRIPT_PROFILE)|
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |      Scorecard Output       |
                      |  (Console / JSON / Markdown)|
                      +-----------------------------+
```

### 5.2 Dependency & Packaging (`pyproject.toml`)
Add optional dependency group:
```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
]
java = [
    "tree-sitter>=0.23.0",
    "tree-sitter-java>=0.23.0",
]
javascript = [
    "tree-sitter>=0.23.0",
    "tree-sitter-javascript>=0.23.0",
]
```

### 5.3 JavaScript AST Parser (`scripts/_code_health/js_parser.py`)
- `check_javascript_dependencies()`: Verifies `tree_sitter` and `tree_sitter_javascript` imports; raises `MissingNativeParserError("javascript", ["tree-sitter", "tree-sitter-javascript"])` on failure.
- `parse_javascript_file(path: Path, rel_path: str, is_test: bool) -> IRModule`:
  - Reads source bytes.
  - Builds CST via `Parser(Language(tree_sitter_javascript.language()))`.
  - Walks top-level and nested statements.
  - Extracts classes (`class_declaration`, `class`), their methods, fields, and constructors.
  - Extracts functions:
    - `function_declaration`
    - `generator_function_declaration`
    - `variable_declarator` where the value is an `arrow_function` or `function`
    - `method_definition` inside classes or object literals
    - Callbacks in BDD test statements (`it("title", () => {})`, `test("title", () => {})`) labeled with `name="test: " + title` and `is_test=True`.
  - Calculates cyclomatic complexity:
    - Branches: `if_statement`, `switch_case`, `for_statement`, `for_in_statement`, `for_of_statement`, `while_statement`, `do_statement`, `catch_clause`, `ternary_expression`, `binary_expression` (`&&`, `||`, `??`).
  - Calculates cognitive complexity:
    - Nesting increments on control structures, switch statements, ternary expressions, and catch clauses.
  - Extracts parameters:
    - Detects default value assignments (`assignment_pattern` / default initializers) and marks `has_default=True`.
    - Parses JSDoc comment blocks immediately preceding the function, extracting `@param {type}` and `@return`/`@returns {type}` when present.
  - Extracts calls (`call_expression`) and checks for string concatenation in arguments, timer string execution (`setTimeout("string", ...)`), and `new Function(...)`.
  - Extracts except/catch handlers (`catch_clause`), checking whether the block is empty.
  - Detects `var` variable declarations, loose equality comparisons (`==`, `!=`), and direct prototype assignments (`__proto__`).
  - Extracts class fields and field accesses (`this.x`) to compute LCOM4.

### 5.4 JavaScript Language Profile (`scripts/_code_health/profiles_js.py` & `profiles.py`)
- `JAVASCRIPT_PROFILE = JavaScriptLanguageProfile(name="javascript", file_extensions=(".js", ".mjs", ".cjs"))`
- `JavaScriptLanguageProfile`:
  - Evaluates JavaScript-specific rules:
    - `var` declarations: `-3.0 pts` per `var` declaration (cap `15.0 pts`) in Clean Code.
    - Loose equality `==` / `!=`: `-2.0 pts` per loose comparison (cap `10.0 pts`) in Clean Code.
    - Dynamic eval (`eval`, `new Function`): `-40.0 pts` in Security.
    - String arguments in timers (`setTimeout`, `setInterval`): `-20.0 pts` in Security.
    - Prototype pollution (`__proto__` mutation): `-25.0 pts` in Security.
  - `is_test_assert_call`: Recognizes standard assertions (`assert`, `assertEquals`, `expect`, `to.equal`, `toBe`, `toEqual`, `should`).
  - Typing & reasoning evaluation:
    - Parameters with explicit JSDoc `{type}` or default values (`has_default=True`) are counted as typed.
    - Untyped, un-defaulted parameters in non-test functions incur `-2.0 pts` each (cap `10.0 pts`).
    - Functions with JSDoc `@return`/`@returns` or void/constructor returns are counted as having return types.

### 5.5 CLI & Module Integration
- Update `scripts/_code_health/models.py`:
  - Add `node_modules`, `dist`, `build`, `.next`, `.nuxt` to `IGNORED_SCAN_DIRS`.
- Update `scripts/_code_health/ir_models.py`:
  - Add optional fields with defaults to `IRFunction` (`var_declarations_count: int = 0`, `loose_comparisons_count: int = 0`, `has_proto_mutation: bool = False`) to maintain 100% backward compatibility.
- Update `scripts/_code_health/module_engine.py`:
  - Update `is_test_file_path` to recognize `.test.js`, `.spec.js`, `_test.js`, and `__tests__/`.
  - Route `.js`, `.mjs`, `.cjs` files to `self._analyze_javascript(...)` (evaluating file LOC and Git churn at module level, mirroring Java).
  - Update `_GitLogAccumulator` to count source commits for `.js`, `.mjs`, `.cjs`.
- Update `scripts/_code_health/reporting.py`:
  - In `_discover_files`, support `.js`, `.mjs`, `.cjs` when `lang_override` is `"javascript"` / `"js"` or auto.
- Update `scripts/code_health.py`:
  - Add `"javascript"`, `"js"` to `--lang` argument choices.

---

## 6. Resolved Decisions and Builder Calls

### User Decision
- **JSDoc & Type Reasoning**: JSDoc is not mandatory for every function. Type inference (e.g. from parameter default values `param = default`) and structure reasoning are prioritized. Excessive type coercion (such as loose equality `==`/`!=`) is penalized to ensure code reasoning is straightforward.

### Builder Calls (Settled Technical Defaults)
- **Call 1 (Universal IR Field Extensions)**: `IRFunction` is extended with `var_declarations_count`, `loose_comparisons_count`, and `has_proto_mutation` (defaulting to 0/False). This keeps IR models language-neutral and backward-compatible with Python and Java.
- **Call 2 (Penalty Points & Caps)**:
  - Dynamic eval (`new Function` / `eval`): `-40.0 pts` in Security.
  - Prototype mutation (`__proto__`): `-25.0 pts` in Security.
  - Timer string execution (`setTimeout("...")`): `-20.0 pts` in Security.
  - Loose equality (`==` / `!=`): `-2.0 pts` per occurrence (cap `10.0 pts`) in Clean Code.
  - Legacy `var`: `-3.0 pts` per declaration (cap `15.0 pts`) in Clean Code.
  - Empty `catch` block: `-10.0 pts` in Clean Code.
- **Call 3 (BDD Test Extraction)**: Callbacks inside `it("title", ...)` and `test("title", ...)` are extracted as `IRFunction` units with `name="test: " + title` and `is_test=True`. Assertion recognition includes `assert`, `expect`, `should`, `toBe`, `toEqual`.
- **Call 4 (Module Scope Parity)**: `_analyze_javascript` mirrors `_analyze_java`: module-level score evaluates file LOC penalties and Git churn/coupling, delegating unit rules to functions, classes, and the Universal IR scorer.
