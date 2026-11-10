# Design Document: TypeScript Language Profile

**Date**: 2026-11-09  
**Status**: Approved Candidate (Post-Builder Check)  
**Target Module**: `scripts/_code_health/`  

---

## 1. Intent and Why

`py-code-health` provides deterministic, zero-runtime-execution code health scorecards (`0–100`, Grades `A–F`) across five weighted dimensions: Single Responsibility & Cohesion (`30%`), Size & Readability (`25%`), Complexity & Control Flow (`20%`), Clean Code & Maintainability (`15%`), and Security & Boundary Hygiene (`10%`).

The analyzer currently supports Python (via `ast`), Java (via `tree-sitter-java`), and vanilla JavaScript (via `tree-sitter-javascript`). Adding TypeScript support extends `py-code-health` to modern typed web, backend, and full-stack TypeScript/TSX codebases without requiring a Node.js runtime or `tsc` subprocess, while enforcing TypeScript-specific type-safety and maintainability standards aligned with the Google TypeScript Style Guide, `typescript-eslint` strict rules, and SonarQube TypeScript rules.

---

## 2. Goals, Non-Goals, and Anti-Goals

### Goals
- **Full AST/CST Parse Fidelity**: Parse TypeScript source files (`.ts`, `.mts`, `.cts`) via `tree_sitter_typescript.language_typescript()` and JSX-enabled TypeScript files (`.tsx`) via `tree_sitter_typescript.language_tsx()` into the language-neutral Universal Intermediate Representation (`IRModule`, `IRClass`, `IRFunction`).
- **Comprehensive Unit Extraction**:
  - **Functions**: Function declarations (`function f(): T {}`), generator functions (`function*`), arrow functions (`const f = (): T => {}`), function expressions, class/object methods, and BDD test blocks (`it(...)`, `test(...)`). Inline callbacks (`.map()`, `.filter()`, IIFEs) are absorbed into their enclosing parent function's complexity and LOC metrics.
  - **Classes & Contracts**: Classes (`class C implements I {}`), abstract classes, constructors (including TypeScript constructor parameter properties like `constructor(private readonly db: Db)`), instance/static methods, getters/setters, and class fields. Pure contract declarations (`interface` and `type` aliases) are treated as structural contracts rather than behavioral classes and are exempt from class LCOM4 penalties.
  - **Modules**: Imports (`import ...`, `import type ...`), exports (`export ...`), effective non-comment/non-blank LOC, and Git history churn/coupling.
- **Five-Dimension Scoring**:
  - **Single Responsibility & Cohesion (30%)**:
    - Class LCOM4 connected components across `this.<field>` accesses (including fields declared via constructor parameter properties `public`/`private`/`protected`/`readonly`).
    - Function concern mixing, external call fan-out (`>6`), and boolean flag parameters with defaults (`flag: boolean = false` or `flag = false`: `-6.0 pts`).
    - File-level Git commit churn, co-change coupling, and divergent feature changes.
  - **Size & Readability (25%)**: Effective LOC, parameter count (`>4` standard, `>6` entrypoints), and maximum nesting depth (`>3`).
  - **Complexity & Control Flow (20%)**: Cyclomatic complexity (`if`, `switch`/`case`, `for`, `for...in`, `for...of`, `while`, `do...while`, `catch`, ternary `? :`, logical `&&`, `||`, `??`), cognitive complexity with nesting increments, and return statement count (`>3`).
  - **Clean Code & Maintainability (15%) — TypeScript-Tailored**:
    - **Strict Signature Typing (Python Parity)**:
      - Untyped parameters without default values in non-test functions incur `-5.0 pts` each (cap `-25.0 pts`). Optional parameters (`param?: string`) or parameters with default values (`param = 0`) or explicit type annotations (`param: string`) are recognized as typed.
      - Missing explicit return type annotations on non-test, non-constructor functions incur `-10.0 pts`.
      - Missing TSDoc/JSDoc comment block (`/** ... */`) on public functions (`-5.0 pts` if LOC $\le 10$, `-10.0 pts` if LOC $> 10$) and classes (`-15.0 pts`).
    - **Type Safety Escape Hatches**:
      - Explicit `any` usage (`: any`, `as any`, `<any>`, `Array<any>`): `-5.0 pts` per occurrence (cap `-20.0 pts`).
      - Compiler suppression directives (`@ts-ignore`, `@ts-nocheck` in comments): `-10.0 pts` per directive (cap `-20.0 pts`). (`@ts-expect-error` with an explanation is not penalized.)
      - Non-null assertion operators (`expr!`): `-2.0 pts` per occurrence (cap `-10.0 pts`).
    - **ECMAScript Hygiene**:
      - Legacy `var` declarations: `-3.0 pts` each (cap `-15.0 pts`).
      - Loose equality (`==`, `!=`): `-2.0 pts` each (cap `-10.0 pts`).
      - Empty `catch` block: `-10.0 pts`.
      - Lingering `debugger;` statement: `-10.0 pts`.
  - **Security & Boundary Hygiene (10%)**:
    - Dynamic code execution (`eval(...)`, `new Function(...)`): `-40.0 pts`.
    - String arguments to timers (`setTimeout("...", ...)`, `setInterval("...", ...)`): `-20.0 pts`.
    - Direct prototype mutation (`__proto__`, `Object.setPrototypeOf`): `-25.0 pts`.
    - `with` statement: `-30.0 pts`.
    - SQL/query execution calls (`query`, `execute`, `raw`, `$queryRawUnsafe`, `$executeRawUnsafe`) with string concatenation or template interpolation: `-40.0 pts`.
- **Missing Dependency Guard**: If `tree-sitter` or `tree-sitter-typescript` is missing when TypeScript files are targeted, halt immediately with exit code `2` and display copy-paste `uv` and `pip` installation commands in console or JSON format.
- **Discovery & Filtering**:
  - Automatically discover `.ts`, `.tsx`, `.mts`, `.cts` files.
  - Automatically skip ambient declaration files (`*.d.ts`, `*.d.mts`, `*.d.cts`) and minified/bundled files (`*.min.ts`, or lines $> 1000$ chars in the first 50 lines).
  - Support CLI `--lang typescript` (and alias `--lang ts`).
- **Test Suite Recognition**: Recognize `*.test.ts`, `*.spec.ts`, `*_test.ts`, `*.test.tsx`, `*.spec.tsx`, `*.test.mts`, `*.spec.mts`, `*.test.cts`, `*.spec.cts`, and files under `test/`, `tests/`, `__tests__/`. Extract `it(...)` and `test(...)` blocks with `is_test=True` and evaluate assertion counts (`0` assertions $\rightarrow -30.0$ pts; $>8$ assertions $\rightarrow -3.0$ pts per excess).

### Non-Goals
- Full cross-file type resolution or running the TypeScript compiler (`tsc`). Analysis is strictly per-file CST + repository Git history.
- Framework-specific profiles (e.g., Angular, NestJS, React, Next.js) — deferred to future `FrameworkProfile` extensions.
- Ambient declaration (`*.d.ts`) lint checking — declaration files contain no executable logic and are skipped during discovery.

### Anti-Goals
- No regex or heuristic fallback parser when `tree-sitter-typescript` is absent.
- No dependency on Node.js, npm, or external JS/TS runtimes.

---

## 3. Constraints

- **Python Version**: Python $\ge 3.11$ standard library.
- **Optional Native Dependencies**: Core Python analysis remains zero-dependency. TypeScript support is declared under `[project.optional-dependencies] typescript = ["tree-sitter>=0.23.0", "tree-sitter-typescript>=0.23.0"]`.
- **Self-Health Invariant**: All new and modified Python modules in `scripts/_code_health/` must maintain a composite score $\ge 90.0$ (Grade A), staying below the 350-LOC ideal file threshold.
- **Backward Compatibility**: 100% of existing Python, Java, and JavaScript unit tests and CLI outputs must remain unchanged.

---

## 4. Evaluated Approaches

### Approach 1: Dedicated `ts_parser.py` and `profiles_ts.py` Reusing Shared ECMAScript Helpers (Selected)
- **Mechanism**: Create `scripts/_code_health/ts_parser.py` using `tree-sitter-typescript` (`language_typescript()` for `.ts`/`.mts`/`.cts` and `language_tsx()` for `.tsx`) and `scripts/_code_health/profiles_ts.py` (`TypeScriptLanguageProfile` subclassing `JavaScriptLanguageProfile` or sharing common helpers).
- **Pros**: Keeps `js_parser.py` and `ts_parser.py` well under the 350-LOC threshold for Grade A self-health; cleanly isolates `tree-sitter-typescript` from `tree-sitter-javascript`; allows TypeScript-specific AST extraction (type annotations, return types, constructor parameter properties, `any`, `@ts-ignore`, non-null assertions) without cluttering JS parsing.
- **Cons**: Introduces two new modules in `scripts/_code_health/`.
- **Decision**: **Selected** (confirmed with user).

### Approach 2: Single Combined JS/TS Parser and Profile in `js_parser.py` and `profiles_js.py` (Rejected)
- **Mechanism**: Add TypeScript grammar and rule branches directly into `js_parser.py` and `profiles_js.py`.
- **Pros**: Fewer files in `scripts/_code_health/`.
- **Cons**: `js_parser.py` is already 419 LOC; adding TS grammar rules pushes it past 550 LOC, degrading its self-health score and coupling two optional parser libraries.
- **Decision**: **Rejected**.

---

## 5. Architectural & Technical Specification

### 5.1 Dependency & Packaging (`pyproject.toml`)
Add optional `typescript` dependency group:
```toml
typescript = [
    "tree-sitter>=0.23.0",
    "tree-sitter-typescript>=0.23.0",
]
```

### 5.2 Universal IR Model Extensions (`scripts/_code_health/ir_models.py`)
Extend `IRFunction` with backward-compatible defaults for TypeScript type-safety telemetry:
- `explicit_any_count: int = 0`
- `ts_ignore_count: int = 0`
- `non_null_assertion_count: int = 0`

### 5.3 TypeScript CST Parser (`scripts/_code_health/ts_parser.py`)
- `check_typescript_dependencies() -> tuple[Any, Any]`:
  - Imports `tree_sitter` and `tree_sitter_typescript`.
  - Raises `MissingNativeParserError("typescript", ["tree-sitter", "tree-sitter-typescript"])` on `ImportError`.
- `parse_typescript_file(file_path: Path, rel_path: str, is_test: bool) -> IRModule`:
  - Selects `tree_sitter_typescript.language_tsx()` when `file_path.suffix.lower() == ".tsx"`, otherwise `tree_sitter_typescript.language_typescript()`.
  - **Class & Abstract Class Extraction**: Handles `class_declaration` and `abstract_class_declaration` where the class identifier node is `type_identifier` (or `identifier`).
  - **Syntax Error Handling**: If `tree.root_node.has_error` is True, records a syntax error marker or delegates to module-level error handling on par with JS/Java.
  - **Parameter Extraction**:
    - Handles `required_parameter`, `optional_parameter`, and `rest_parameter` inside `formal_parameters`.
    - Extracts parameter name (`identifier` or destructuring pattern), `type_annotation` text (e.g., `: boolean` $\rightarrow$ `"bool"` normalized for boolean flag checks, `: any` $\rightarrow$ `"any"`, or raw type name), and `has_default` (`=` initializer present or `optional_parameter` `?`).
    - In `constructor`, parameters with `accessibility_modifier` (`public`, `private`, `protected`) or `readonly` are also recorded as `IRField` entries on the enclosing `IRClass` so LCOM4 tracks constructor parameter properties accurately.
  - **Return Type Extraction**:
    - Inspects `type_annotation` directly on the function/method/arrow node (outside `formal_parameters`).
    - Constructors (`name == "constructor"`) default to `return_type="void"`.
  - **TypeScript Smell & Escape-Hatch Scanning**:
    - `explicit_any_count`: Counts `predefined_type` nodes whose text is `"any"` across parameter annotations, return annotations, variable type annotations, `as_expression` (`x as any`), `type_assertion` (`<any>x`), and `type_arguments` (`Array<any>`).
    - `ts_ignore_count`: Scans `comment` nodes within the function (or module) for `@ts-ignore` or `@ts-nocheck`.
    - `non_null_assertion_count`: Counts `non_null_expression` (`expr!`) nodes inside the function body.
  - **SQL/Command String Concatenation**:
    - Marks `IRCall.has_string_concat = True` when a call's arguments include a `binary_expression` with `+` or a `template_string` containing `template_substitution` (`${...}`).
  - **Contract Declarations**:
    - `interface_declaration` and `type_alias_declaration` nodes at the module level are not emitted as behavioral `IRClass` units (preventing false missing-method or LCOM4 penalties), while still contributing to module effective LOC.

### 5.4 TypeScript Language Profile (`scripts/_code_health/profiles_ts.py` & `profiles.py`)
- `TypeScriptLanguageProfile(JavaScriptLanguageProfile)`:
  - `name = "typescript"`
  - `file_extensions = (".ts", ".tsx", ".mts", ".cts")`
  - **Function Evaluation**:
    - Inherits JS clean smells (`var`, loose equality `==`/`!=`, empty `catch`, `debugger;`) and security rules (`eval`, `new Function`, string timers, `__proto__`, `with`).
    - Overrides `_eval_parameter_typing`:
      - Skipped here because `UniversalIRScorer._score_source_clean_ir` already evaluates untyped parameters (`-5.0 pts` each, cap `-25.0 pts`) and missing return type (`-10.0 pts`) for non-JS profiles!
      - Wait: for arrow functions or methods with default parameter values (`x = 10`), `ts_parser.py` sets `type_annotation="inferred"` when `has_default=True` and no explicit `: type` is written, so `UniversalIRScorer` does not penalize defaulted parameters as untyped (while boolean default parameters get `type_annotation="bool"` so SRP flags boolean default flags!).
    - Adds `_eval_ts_type_safety(func: IRFunction) -> list[RulePenalty]`:
      - `func.explicit_any_count > 0`: `-5.0 pts` per `any` (cap `-20.0 pts`) in `clean` — `"Clean (TS): {n} explicit 'any' type usage(s) defeat type safety (-{pen:.1f} pts)"`.
      - `func.ts_ignore_count > 0`: `-10.0 pts` per `@ts-ignore`/`@ts-nocheck` (cap `-20.0 pts`) in `clean` — `"Clean (TS): {n} '@ts-ignore'/'@ts-nocheck' directive(s) suppress compiler checks (-{pen:.1f} pts)"`.
      - `func.non_null_assertion_count > 0`: `-2.0 pts` per `!` assertion (cap `-10.0 pts`) in `clean` — `"Clean (TS): {n} non-null assertion(s) ('!') bypass strict null checks (-{pen:.1f} pts)"`.
    - Adds SQL/query concatenation check in `_eval_dynamic_sinks`:
      - Calls matching SQL execution methods (`query`, `execute`, `raw`, `$queryRawUnsafe`, `$executeRawUnsafe`) with `has_string_concat=True` incur `-40.0 pts` in `security`.

### 5.5 Scorer, Discovery, and CLI Integration
- `scripts/_code_health/ir_scorer.py`:
  - In `_count_ir_asserts`: deduplicate `expect(...)` and chained matcher calls on the same line for both `"javascript"` and `"typescript"` (`profile.name in {"javascript", "typescript"}`).
  - In `score_function`: delegate exception handler and security call scoring to profile for `"typescript"` just like `"javascript"` (`self.profile.name in {"javascript", "typescript"}`), while letting `_score_source_clean_ir` run full parameter typing (`-5.0 pts`) and return type (`-10.0 pts`) checks for `"typescript"`.
- `scripts/_code_health/module_engine.py`:
  - Update `_GitLogAccumulator.record_block` to include `(".ts", ".tsx", ".mts", ".cts")`.
  - Update `is_test_file_path` to recognize `.test.ts`, `.spec.ts`, `_test.ts`, `.test.tsx`, `.spec.tsx`, `_test.tsx`, `.test.mts`, `.spec.mts`, `.test.cts`, `.spec.cts`, and `test_*.ts`.
  - Route `.ts`, `.tsx`, `.mts`, `.cts` to `self._analyze_typescript(...)` (or a unified `self._analyze_ir_module(...)` helper shared across Java, JS, and TS to reduce duplication).
- `scripts/_code_health/reporting.py`:
  - Update `_is_minified_or_bundled` (or add `_is_skipped_asset`) to skip `*.d.ts`, `*.d.mts`, `*.d.cts`, `*.min.ts`, and `.ts`/`.tsx`/`.mts`/`.cts` files with lines $> 1000$ chars in the first 50 lines.
  - Update `CodeHealthRunner._discover_files` to include `{".ts", ".tsx", ".mts", ".cts"}` when `lang_override` is `"typescript"` / `"ts"` or `None` (`auto`).
- `scripts/code_health.py`:
  - Add `"typescript"`, `"ts"` to `--lang` choices in `_build_arg_parser()`.

---

## 6. What Is Left to the Builder

- **Shared Helper Factoring**: The builder may extract small AST/CST utility functions (e.g., `_get_node_text`, `_find_first_child`, `_count_effective_js_loc`, `_has_doc_comment`, `_calc_js_lcom4`) from `js_parser.py` or import them into `ts_parser.py` so neither file exceeds 350 LOC.
- **Unified IR Module Analysis in `ModuleAnalyzer`**: `_analyze_java`, `_analyze_javascript`, and `_analyze_typescript` follow identical scoring patterns in `module_engine.py`; the builder may consolidate them into a single parameterized helper to keep `module_engine.py` concise and Grade A.
- **Sample Suite**: Create representative clean and smelly TypeScript sample files under `samples/typescript/` and unit tests in `tests/unit/test_typescript_health.py`.
