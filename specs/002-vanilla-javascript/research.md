# Research & Architectural Decisions: Vanilla JavaScript (ECMAScript) Profile

**Date**: 2026-11-09  
**Feature**: Vanilla JavaScript (ECMAScript) Language Profile  
**Spec**: [spec.md](./spec.md)  

---

## 1. Concrete Syntax Tree Parser Selection

### Decision
Use `tree-sitter` and `tree-sitter-javascript` (Python bindings) to parse `.js`, `.mjs`, and `.cjs` source files into Concrete Syntax Trees (CST).

### Rationale
- **AST Fidelity**: JavaScript syntax contains complex constructs (nested arrow functions, object literal methods, destructuring, template literals, async generators, optional chaining, and nullish coalescing) that cannot be reliably analyzed via regular expressions or heuristics.
- **Architectural Parity**: Java support in `py-code-health` already uses `tree-sitter` and `tree-sitter-java`. Reusing the Tree-Sitter ecosystem ensures consistent CST traversal, performance, and error handling.
- **Zero Node.js Dependency**: Avoids requiring a Node.js binary, npm packages, or external subprocess IPC on the host machine.
- **Strict Parsing Policy**: Per project constitution and spec requirements, fallback/heuristic parsers are prohibited to guarantee 100% metric accuracy. If `tree-sitter-javascript` is missing, the tool halts immediately with exit code `2`.

### Alternatives Considered
- **External Node.js / Acorn / Espree Bridge**: Calling `node -e "..."` to generate ESTree AST JSON. Rejected due to subprocess overhead and introducing a hard runtime dependency on Node.js.
- **Python-based Regex / Heuristic Tokenizer**: Zero external dependencies, but fails to accurately determine cognitive complexity, nesting levels, or distinguish class field accesses for LCOM4. Rejected per anti-goals.

---

## 2. Unit Boundary Extraction & Parent Scope Absorption

### Decision
Extract only top-level function declarations, class/object methods, and functions assigned to named variables (`const handler = () => {}`) as discrete `IRFunction` unit scorecards. Inline callbacks (such as those passed to `.map()`, `.filter()`, `.reduce()`, event listeners, or IIFEs) are absorbed into their enclosing parent function.

### Rationale
- JavaScript codebases heavily utilize inline anonymous callbacks (`array.map(x => x.id)`). If every 1-line callback was extracted as an independent `IRFunction`, scorecards would be flooded with dozens of trivial `<anonymous:line>` entries, skewing function counts and generating false warnings for missing docstrings.
- By absorbing inline callbacks into the enclosing parent function, their cyclomatic complexity, cognitive nesting penalties, and LOC are accurately credited to the parent function where the logical complexity resides.

### Alternatives Considered
- **Extract Every Function/Closure**: Creates severe report clutter and false-positive docstring penalties for short callbacks.
- **LOC Threshold Extraction**: Arbitrary boundary ($>5$ LOC) that creates inconsistent scorecard symbol listings.

---

## 3. Type Reasoning, Anti-Coercion, and Clean Code Rubric

### Decision
1. **Type Reasoning**: Parameters with default values (e.g. `param = "default"`) or JSDoc `@param {type}` tags are counted as typed. Parameters in non-test functions lacking both defaults and JSDoc incur a small Clean Code deduction (`-2.0 pts` each, capped at `-10.0 pts`).
2. **Anti-Coercion**: Loose equality operators (`==` and `!=`) trigger implicit type coercion that obscures reasoning; each occurrence is penalized `-2.0 pts` (capped at `-10.0 pts`) under Clean Code.
3. **Legacy Idioms**: `var` declarations incur `-3.0 pts` (cap `-15.0 pts`) under Clean Code, recommending `const` or `let`.
4. **Empty Catch Blocks**: Swallowed exceptions in `catch` blocks deduct `-10.0 pts` under Clean Code.

### Rationale
Vanilla ECMAScript lacks native type syntax. Forcing JSDoc `{type}` annotations on every function would inappropriately cap clean vanilla JS code at Grade C/D. Recognizing parameter defaults as inferred types rewards self-documenting code, while penalizing loose equality directly discourages unexpected type coercion.

### Alternatives Considered
- **Mandatory JSDoc**: Penalizing every unannotated JS parameter with the standard Python/Java `-5.0 pt` penalty would unfairly penalize idiomatic vanilla JS.
- **Complete Exemption from Typing**: Ignores the user's principle that code readers need to be able to reason about parameter types and object structures.

---

## 4. Missing Dependency Behavior (Parser Guard)

### Decision
When analyzing JavaScript files without `tree-sitter` or `tree-sitter-javascript` installed:
- Print a clear, actionable warning banner to `stderr` (or a structured JSON payload in `--format json` mode).
- Provide copy-paste installation commands for `uv` (`uv pip install tree-sitter tree-sitter-javascript`) and `pip` (`pip install tree-sitter tree-sitter-javascript`).
- Terminate process execution with exit code `2`.
- Pure Python and Java analysis must run without triggering JavaScript parser checks.

### Rationale
Matches the exact contract established in `MissingNativeParserError` and Java's `check_java_dependencies()`. Guarantees zero silent failures or degraded heuristic metrics.

---

## 5. Minified & Bundled Asset Detection

### Decision
Automatically identify and skip pre-bundled or minified JavaScript files during directory scans:
- Match standard minified filename patterns: `*.min.js`.
- Inspect the first 50 lines: if any line exceeds 1,000 characters, classify as a bundled/minified asset.
- Emit an informative log message (`"Skipped minified asset: <path>"`) and exclude the file from composite codebase scoring.

### Rationale
Checking in bundled or minified assets is common in web projects. Attempting to parse a 50,000-character single-line bundle creates extreme LOC and cognitive complexity anomalies that distort repository health scores.

---

## 6. Security and Operational Hygiene Rules

### Decision
Enforce deterministic AST checks for core ECMAScript security and operational smells:
- Dynamic execution (`eval(...)`, `new Function(...)`): `-40.0 pts` (Security)
- Direct prototype mutation (`__proto__`): `-25.0 pts` (Security)
- Timer string execution (`setTimeout("string", ...)`): `-20.0 pts` (Security)
- `with (...)` statements: `-30.0 pts` (Security & Operational Hygiene)
- `debugger;` statements: `-10.0 pts` (Clean Code & Operational Hygiene)

### Rationale
These language constructs represent high-risk attack vectors (code injection, prototype pollution, scope corruption) or unhygienic debug remnants that should never appear in production codebases.
