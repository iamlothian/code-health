# Research & Architectural Decisions: TypeScript Language Profile

**Date**: 2026-11-09  
**Feature**: TypeScript Language Profile  
**Spec**: [spec.md](./spec.md)  

---

## 1. Concrete Syntax Tree Parser Selection (`tree-sitter-typescript`)

### Decision
Use `tree-sitter` and `tree-sitter-typescript` (Python bindings) to parse TypeScript source files into Concrete Syntax Trees (CST):
- Files ending in `.tsx` are parsed using `tree_sitter_typescript.language_tsx()`.
- Files ending in `.ts`, `.mts`, and `.cts` are parsed using `tree_sitter_typescript.language_typescript()`.

### Rationale
- **Grammar Fidelity & JSX Support**: TypeScript includes advanced syntactic forms (generics, type arguments, union/intersection types, parameter properties, as-expressions, non-null assertions) and JSX syntax in `.tsx` files. Using the official `tree-sitter-typescript` grammar ensures 100% parse accuracy for modern TypeScript (TS 5.x / ES2024+).
- **Separation of TS and TSX Grammars**: `tree-sitter-typescript` provides two distinct language entrypoints. Pure TypeScript cannot parse `<Component />` unambiguously due to ambiguity with `<Type>` assertions, while TSX parses JSX element trees cleanly. Selecting the grammar by file extension guarantees error-free parsing across both standard modules and React/frontend components.
- **Architectural Parity & Standalone Execution**: Reuses the Tree-Sitter ecosystem already established in `py-code-health` for Java and JavaScript, avoiding any runtime dependency on Node.js, `npm`, or `tsc`.
- **Strict Parsing Policy**: Fallback regex or heuristic parsers are strictly prohibited. When `tree-sitter-typescript` is absent, the analyzer halts immediately with exit code `2`.

### Alternatives Considered
- **Subprocess `tsc --noEmit` or Node.js Language Service**: Invoking `tsc` via subprocess requires Node.js and introduces 1–3 second latency per file. Rejected per project constraints (zero Node.js dependency, sub-second execution).
- **Combined JS/TS Grammar in `tree-sitter-javascript`**: The JavaScript grammar fails on TypeScript type annotations and interface definitions. Rejected.

---

## 2. Dedicated Modular Architecture (`ts_parser.py` and `profiles_ts.py`)

### Decision
Implement TypeScript parsing in a dedicated `scripts/_code_health/ts_parser.py` and language rules in `scripts/_code_health/profiles_ts.py` (inheriting shared ECMAScript hygiene and security evaluations from `JavaScriptLanguageProfile`), rather than combining them into `js_parser.py`.

### Rationale
- **Code Health Dogfooding**: `js_parser.py` is currently 419 LOC. Adding TypeScript type annotations, return types, parameter properties, interfaces, and smell visitors would bloat `js_parser.py` past 550 LOC, violating the analyzer's own 350-LOC ideal file size threshold.
- **Dependency Isolation**: Isolates the dependency check for `tree-sitter-typescript` from `tree-sitter-javascript`. Users analyzing purely TypeScript need not install the JavaScript grammar wheel if they only have TypeScript installed.
- **Maintainability & Single Responsibility**: Separates TypeScript-specific AST extraction (types, generics, interfaces, compiler directives) from JavaScript CST transformations.

### Alternatives Considered
- **Single Combined JS/TS Module**: Rejected because it causes extreme file size bloat and couples optional dependencies.

---

## 3. Strict Typing and Type Safety Escape Hatch Rubric

### Decision
1. **Strict Signature Typing**:
   - Parameters in non-test functions lacking both type annotations and default initializers incur `-5.0 pts` each (capped at `-25.0 pts`) under Clean Code.
   - Missing explicit return type annotations on non-test, non-constructor functions incur `-10.0 pts` under Clean Code.
   - Missing public TSDoc/JSDoc comment blocks incur `-5.0 pts` (LOC $\le 10$) or `-10.0 pts` (LOC $> 10$) on functions, and `-15.0 pts` on classes.
2. **Type Safety Escape Hatches**:
   - Explicit `any` (`: any`, `as any`, `<any>x`, `Array<any>`): `-5.0 pts` per occurrence (capped at `-20.0 pts`) under Clean Code.
   - Compiler suppression directives (`@ts-ignore`, `@ts-nocheck`): `-10.0 pts` per directive (capped at `-20.0 pts`) under Clean Code. `@ts-expect-error` is permitted and not penalized.
   - Non-null assertion operators (`expr!`): `-2.0 pts` per occurrence (capped at `-10.0 pts`) under Clean Code.
3. **Boolean Default Flags**:
   - Boolean parameters with default values (`flag: boolean = false` or `flag = false`) incur `-6.0 pts` under Single Responsibility (SRP), matching Python rubric parity.
4. **ECMAScript Hygiene**:
   - Inherits deductions for legacy `var` (`-3.0 pts`), loose equality `==`/`!=` (`-2.0 pts`), empty `catch` blocks (`-10.0 pts`), and lingering `debugger;` statements (`-10.0 pts`).

### Rationale
In TypeScript, writing untyped parameters, using `any`, suppressing compiler checks via `@ts-ignore`, or bypassing strict null checks with `!` undermines the type safety guarantees of the language. These rules align directly with `typescript-eslint/recommended-type-checked`, `strictTypeChecked`, and Google TypeScript Style Guide conventions.

### Alternatives Considered
- **Treating `any` as a standard untyped parameter**: `any` explicitly tells the compiler to silence type checks, which is a deliberate code smell distinct from omitted types. Penalizing it explicitly surfaces type-safety degradation.
- **Penalizing `@ts-expect-error`**: Modern TypeScript conventions recommend `@ts-expect-error` over `@ts-ignore` because `@ts-expect-error` fails compilation if the suppressed error is fixed, whereas `@ts-ignore` silently lingers. Therefore, only `@ts-ignore` and `@ts-nocheck` are penalized.

---

## 4. Pure Contracts (Interfaces & Type Aliases) vs. Behavioral Classes

### Decision
Module-level `interface_declaration` and `type_alias_declaration` nodes contribute to module effective LOC, but are **not** emitted as behavioral `IRClass` unit scorecards.

### Rationale
Interfaces and type aliases in TypeScript are compile-time type definitions that contain no runtime executable methods. If emitted as `IRClass` units, they would trigger false-positive penalties for having 0 methods, 0 attributes, or disconnected LCOM4 components. Treating them as structural contracts matches how Python `Protocol` and `TypedDict` are handled in `has_exempt_base()`.

### Alternatives Considered
- **Emitting `IRClass` with LCOM4 exemptions**: Unnecessarily clutters the Classes Scorecard with empty data types.

---

## 5. Constructor Parameter Properties and LCOM4 Cohesion

### Decision
Extract constructor parameters that declare accessibility modifiers (`public`, `private`, `protected`) or `readonly` as `IRField` entries on the enclosing `IRClass`.

### Rationale
In TypeScript, `constructor(private readonly repo: Repository, public count = 0)` automatically creates and initializes instance fields. Methods referencing `this.repo` or `this.count` are utilizing these fields. If parameter properties were not recognized as class fields, LCOM4 analysis would erroneously report that methods do not access class attributes, resulting in artificial cohesion penalties.

---

## 6. Ambient Declarations and Bundled Asset Skipping

### Decision
1. **Ambient Declaration Files**: Automatically exclude `*.d.ts`, `*.d.mts`, and `*.d.cts` files during directory discovery.
2. **Minified / Bundled Files**: Skip `*.min.ts` and files with lines exceeding 1,000 characters within the first 50 lines.

### Rationale
`*.d.ts` declaration files contain only ambient type definitions for third-party libraries or build outputs; they contain no runtime code. Minified bundles contain artificial LOC and complexity spikes that distort repository health.

---

## 7. Security and Operational Hygiene Rules

### Decision
Enforce deterministic AST checks for dangerous ECMAScript and database constructs:
- Dynamic code evaluation (`eval`, `new Function`): `-40.0 pts` (Security)
- Direct prototype mutation (`__proto__`, `Object.setPrototypeOf`): `-25.0 pts` (Security)
- String timers (`setTimeout("...", delay)`): `-20.0 pts` (Security)
- `with` statement: `-30.0 pts` (Security)
- SQL/query string concatenation/template literal interpolation in query calls (`query`, `execute`, `raw`, `$queryRawUnsafe`, `$executeRawUnsafe`): `-40.0 pts` (Security)

### Rationale
Surfaces critical security vulnerabilities (SQL injection, code injection, prototype pollution) during local development and CI quality gates.
