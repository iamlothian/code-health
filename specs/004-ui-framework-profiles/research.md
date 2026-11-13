# Research: Web UI Framework Code Health Profiles

**Date**: 2026-11-12  
**Feature**: Web UI Framework Code Health Profiles (`004-ui-framework-profiles`)  
**Spec**: [spec.md](./spec.md)

---

## 1. Modular Isolation: Language Primitives vs. Framework Concepts

### Decision
Parsers (`ts_parser.py`, `js_parser.py`) and the universal IR (`ir_models.py`) will record **only generic, language-level syntax facts** (`decorators`, `directives`, `imports`, `jsx_elements_count`, `in_branch_or_loop` on `IRCall`, generic attribute/DOM write records, and unwrapped HOC functions). All **framework semantics** (`useEffect`, `useState`, `dangerouslySetInnerHTML`, `HttpClient`, `.subscribe()`, `"use client"`, `next/headers`) will live exclusively in `scripts/_code_health/profiles_ui.py` (`ReactFrameworkProfile`, `NextJsFrameworkProfile`, `AngularFrameworkProfile`).

### Rationale
- Avoids polluting `IRFunction` with framework-specific fields (like `react_use_effect_count` or `angular_subscribe_count`).
- Ensures `--framework none` and non-UI TypeScript/JavaScript files execute pure language rules (`JavaScriptLanguageProfile` / `TypeScriptLanguageProfile`) with zero UI concern mappings or penalties.
- Matches the existing Java + `SpringBootFrameworkProfile` architecture in `profiles_java.py`.

### Alternatives Considered
- **Adding framework-named fields directly onto `IRFunction` and scanning React/Angular rules in `ts_parser.py`**: Rejected because it couples every parser to specific UI frameworks and violates IR language neutrality.

---

## 2. Empirical CST Verification (`tree-sitter-typescript` & `tree-sitter-javascript`)

Direct CST inspection on Python 3.12 verified the exact node types emitted by both grammars:

1. **JSX Parsing in JavaScript (`.jsx`)**:
   - `tree_sitter_javascript.language()` parses JSX elements (`jsx_element`, `jsx_self_closing_element`, `jsx_attribute`) and `"use client";` directives with `has_error == False` — zero new PyPI packages needed.
2. **Higher-Order Component Wrappers (`React.memo`, `React.forwardRef`)**:
   - In `export const Card = React.memo(({ title }) => ...)`, `variable_declarator` contains a `call_expression` whose `arguments` node holds the `arrow_function` / `function_expression` (sometimes nested twice, e.g. `memo(forwardRef(...))`).
   - Current `_extract_ts_var_funcs` and `_extract_var_funcs` only inspect direct children of `variable_declarator`, missing wrapped components completely. Unwrapping known wrapper callees (`memo`, `React.memo`, `forwardRef`, `React.forwardRef`) in a generic helper extracts these components cleanly.
3. **TypeScript Decorators (`@Component`, `@Injectable`, `@Input`, `@Output`)**:
   - Class decorators on `export class X` are children of `export_statement` (preceding `export`), while non-exported class decorators are direct children of `class_declaration`.
   - Field decorators are direct `decorator` children of `public_field_definition` / `field_definition`.
   - Method decorators are direct `decorator` children of `method_definition` (or preceding sibling inside `class_body` depending on TS grammar version — CST check confirms checking both `node.children` and immediate preceding `decorator` siblings handles both safely).
4. **DOM & JSX Sink Nodes**:
   - `dangerouslySetInnerHTML={{ __html: ... }}` emits `jsx_attribute` with `property_identifier == "dangerouslySetInnerHTML"`.
   - `el.innerHTML = val` / `el.outerHTML = val` emits `assignment_expression` with a `member_expression` LHS whose `property_identifier` is `innerHTML` / `outerHTML`.
   - `document.write(...)`, `el.insertAdjacentHTML(...)`, and Angular `sanitizer.bypassSecurityTrustHtml(...)` emit standard `call_expression` nodes already captured in `IRFunction.calls`.
5. **Array-Index JSX `key` Detection**:
   - Inside `items.map((item, idx) => <li key={idx} ... />)`: `call_expression` callee ends with `.map`, callback `arrow_function` / `function_expression` has `len(params) >= 2`, and a `jsx_attribute` named `key` contains an `identifier` matching the 2nd parameter name (`idx`). This gives high precision without false positives on `key={item.id}`.
6. **Conditional / Looped Hook Calls**:
   - Tracking `in_branch_or_loop: bool` (when a call occurs inside `if_statement`, `for_*`, `while_*`, `do_statement`, `switch_statement`, `ternary_expression`, `try_statement`, OR inside a nested function/callback inside an enclosing component function) enables accurate Rules of Hooks detection without false-flagging top-level hooks inside a component.

---

## 3. Shared ECMAScript UI CST Helper (`ecmascript_ui.py`)

### Decision
Extract shared generic CST extraction primitives (`extract_decorators`, `extract_directives`, `unwrap_wrapper_callable`, `scan_jsx_and_dom_sinks`, `collect_array_index_keys`) into `scripts/_code_health/ecmascript_ui.py`, imported by both `ts_parser.py` and `js_parser.py`.

### Rationale
- `js_parser.py` is currently 419 LOC (above the 350-LOC Grade A file threshold). Factoring shared ECMAScript CST helpers keeps `js_parser.py`, `ts_parser.py`, and `ecmascript_ui.py` all under 350 LOC while avoiding logic duplication across JS and TS.

---

## 4. Framework Auto-Detection & Polyglot Isolation

### Decision
Cache `package.json` dependency inspection per `repo_root` (`functools.lru_cache` keyed by resolved `repo_root` path and mtime/existence, gracefully ignoring malformed JSON) and combine it with per-file `IRModule.imports` and `file_path` context:
- **Angular** (`angular`): `"@angular/core"` in file imports OR (`"@angular/core"` in `package.json` and file is `.ts` with Angular decorators/imports). Never attaches to `.js`/`.jsx`.
- **Next.js** (`nextjs`): `"next/"` import in file OR (`"next"` in `package.json` and file is `.ts`/`.tsx`/`.js`/`.jsx` UI/app module, excluding clearly non-UI backend scripts unless `package.json` declares `next` and file uses React/JSX/App Router paths).
- **React** (`react`): `"react"` / `"react-dom"` import in file OR JSX syntax (`jsx_elements_count > 0`) OR (`"react"` in `package.json` and file uses React hooks/JSX).
- **Explicit Overrides**: `--framework react|nextjs|angular|none` always takes precedence over auto-detection.

### Rationale
- Prevents false positives on pure Node/backend TypeScript utility files inside a monorepo that happens to have `"react"` in root `package.json`, while still detecting frameworks cleanly in single-file snippets without `package.json`.

---

## 5. Baseline Relocation (`samples/typescript/` vs `samples/typescript-react/`)

### Decision
Move `samples/typescript/task_board_legacy.tsx` and `samples/typescript/task_filter_bar.tsx` into `samples/typescript-react/` (updating their baselines for React-aware scoring under `framework: "auto"`) and replace Scenario 5 in `samples/typescript/` with a pure, framework-free TypeScript pair (e.g., `order_pipeline_clean.ts` vs. `order_pipeline_legacy.ts` or pure generic TSX/DOM-free TypeScript). Add new Good/Bad pairs for React Hooks/XSS (`samples/typescript-react/`), Next.js App Router (`samples/typescript-nextjs/`), and Angular (`samples/typescript-angular/`).

### Rationale
- Resolves Q2 cleanly: pure TypeScript baselines stay 100% framework-free, while the moved TSX files and new pairs test real React, Next.js, and Angular scoring end-to-end.
