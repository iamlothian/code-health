# TypeScript / TSX Refactoring Playbook

> **Profile:** `typescript` · **Detection:** `.ts`, `.tsx`, `.mts`, `.cts` files (native Tree-Sitter CST via `tree-sitter-typescript`; `.d.ts`/`.d.mts`/`.d.cts` and minified bundles are skipped) · **Force:** `--lang typescript` (or `--lang ts`)
> **Builds on:** [JavaScript / JSX Refactoring Playbook](javascript-playbook.md) — all ECMAScript clean-code (`var`, `==`/`!=`, empty `catch`, `debugger`) and security (`eval`, `new Function`, string `setTimeout`/`setInterval`, `__proto__`/`setPrototypeOf`, `with`) rules apply here as well.
> **Worked examples:** [good](../../../samples/typescript/good/) · [bad](../../../samples/typescript/bad/)

This reference covers TypeScript-specific type-safety, contract, SQL injection, and test hygiene findings. If React, Next.js, or Angular files are analyzed, also read the matching UI framework playbook.

---

## 1. Single Responsibility & Cohesion (SRP)

- **Finding: `SRP: LCOM4=X disconnected method groups`** (`-15.0 pts` per group over `1` when class has `> 2` concrete non-constructor methods)
  - *Cause:* A class bundles unrelated methods touching disjoint `this.*` fields or constructor parameter properties (`private readonly ...`) — see [`zod_error_legacy.ts`](../../../samples/typescript/bad/zod_error_legacy.ts) vs [`zod_standard_schema.ts`](../../../samples/typescript/good/zod_standard_schema.ts).
  - *Fix:* Extract unrelated concerns (e.g., logging, serialization, metrics) into dedicated injected services or module functions.

- **Finding: `SRP: boolean flag parameter with default value`** (`-6.0 pts` per boolean default parameter)
  - *Cause:* Passing `includeArchived = false` or `dryRun = true` branches a single function into two distinct behaviors.
  - *Fix:* Split into explicit functions (`findActiveOrders` / `findAllOrders`) or accept a typed filter/strategy parameter object.

- **Finding: `SRP: high external call fan-out=X (>6)`** / **`SRP: methods=X (>10)`** / **`SRP: self attributes=X (>7)`**
  - *Fix:* Decompose large services into cohesive helper modules and typed interfaces (compare [`ky_constants.ts`](../../../samples/typescript/good/ky_constants.ts) vs. [`ky_client.ts`](../../../samples/typescript/bad/ky_client.ts)).

---

## 2. Size & Readability

- **Finding: `Size: LOC=X (>25)`** / **`Size: params=X (>4)`** / **`Size: nesting depth=X (>3)`**
  - *Cause:* Long multi-stage pipelines with deeply nested `if`/`for`/`try` blocks (see [`edmonds_karp.ts`](../../../samples/typescript/bad/edmonds_karp.ts)).
  - *Fix:* Extract pure helper steps with explicit input/output interfaces, replace >4 positional parameters with a `readonly` options `interface`, and flatten nesting with guard clauses (`if (!node) return;`). Compare [`floyd_warshall.ts`](../../../samples/typescript/good/floyd_warshall.ts).

---

## 3. Complexity & Control Flow

- **Finding: `Complexity: CC=X (>5)`** / **`Complexity: cognitive=X (>8)`** / **`Complexity: returns=X (>3)`**
  - *Fix:* Extract inner loop predicates, replace `if/else if` ladders with `Record<Key, Handler>` dispatch maps, and consolidate early-exit branches.

---

## 4. Clean Code & Type Safety

- **Finding: `Clean (TS): X explicit 'any' type usage(s) defeat type safety`** (`-5.0 pts` each, capped at `-20.0 pts`)
  - *Cause:* Using `: any`, `as any`, or `any[]` disables compile-time type checking (see [`zod_registries.ts`](../../../samples/typescript/bad/zod_registries.ts)).
  - *Fix:* Replace `any` with `unknown` + type guards, discriminated unions, generics (`<T>`), or concrete `interface`/`type` definitions:
    ```typescript
    // Before
    function parsePayload(raw: any): any {
      return raw.items;
    }

    // After
    interface Payload { readonly items: readonly string[]; }
    function parsePayload(raw: unknown): readonly string[] {
      if (typeof raw !== "object" || raw === null || !("items" in raw)) {
        throw new TypeError("Expected object with items");
      }
      return (raw as Payload).items;
    }
    ```

- **Finding: `Clean (TS): X '@ts-ignore'/'@ts-nocheck' directive(s) suppress compiler checks`** (`-10.0 pts` each, capped at `-20.0 pts`, evaluated both per-function and at module scope)
  - *Cause:* Compiler-suppression directives mask real type mismatches.
  - *Fix:* Fix the underlying type mismatch (narrowing, overloads, or module declaration types). Only use `@ts-expect-error` with an explanatory comment in rare test edge cases where intentional type errors are asserted.

- **Finding: `Clean (TS): X non-null assertion(s) ('!') bypass strict null checks`** (`-2.0 pts` each, capped at `-10.0 pts`)
  - *Cause:* Postfix `value!.prop` can throw `TypeError` at runtime if the value is `null` or `undefined`.
  - *Fix:* Use optional chaining (`?.`), nullish coalescing (`??`), or an explicit guard (`if (!value) throw new Error(...)`).

- **Finding: `Clean: X untyped param(s) (...)`** (`-5.0 pts` each, capped at `-25.0 pts`) and **`Clean: missing return type annotation (-10.0 pts)`**
  - *Cause:* Non-test functions/methods lack explicit TypeScript parameter or return type annotations (`constructor`, `set` accessors, and PascalCase JSX-returning React components are exempt from return types; parameter defaults or optional `param?: T` count as inferred for parameters).
  - *Fix:* Annotate every parameter and return type (`function sum(values: readonly number[]): number`). See [`zod_zsf.ts`](../../../samples/typescript/good/zod_zsf.ts).

- **Finding: `Clean: missing class docstring`** (`-15.0 pts`) and **`Clean: missing public docstring`** (`-5.0 pts` if `<= 10` LOC, `-10.0 pts` if `> 10` LOC)
  - *Fix:* Add JSDoc (`/** ... */`) above public classes, exported functions, and public methods (including above decorators like `@Component` or `@Injectable`).

---

## 5. Security & Boundary Hygiene

- **Finding: `Security (TS): potential SQL/query injection in <call> via string concatenation (-40.0 pts)`**
  - *Cause:* Calling `query`, `execute`, `raw`, `$queryRawUnsafe`, or `$executeRawUnsafe` with a `+`-concatenated string or interpolated template literal (`` `SELECT * FROM orders WHERE id = ${id}` ``).
  - *Fix:* Pass parameterized placeholders or tagged templates (e.g., Prisma `$queryRaw` tagged template or `$1`/`?` bound parameters):
    ```typescript
    // Before (SQL injection risk)
    return this.db.$queryRawUnsafe(`SELECT * FROM orders WHERE customer_id = '${customerId}'`);

    // After (Parameterized query)
    return this.db.query("SELECT * FROM orders WHERE customer_id = $1", [customerId]);
    ```

---

## 6. Test Hygiene

Test files (`*.test.{ts,tsx,mts,cts}`, `*.spec.{ts,tsx,mts,cts}`, `*_test.*`, `test_*.*`, or inside `tests/` / `test/` / `__tests__/`) support Jest, Vitest, Mocha, Node `assert`, and Testing Library matchers (`toBeDefined`, `toBeUndefined`, `toBeNull`, `toContain`, `toMatch`, `toMatchObject`, `toHaveBeenCalled`, `toHaveBeenCalledWith`, `toHaveBeenCalledTimes`, `toHaveProperty`, `toBeInstanceOf`, `toBeGreaterThan`, `toBeLessThan`, `toBeInTheDocument`, plus all JS matchers).

- **Finding: `Clean (Test): test has 0 assertions (-30.0 pts)`** / **`Clean (Test): X assertions in single test (>8)`** (`-3.0 pts` per assertion over `8`, capped at `-30.0 pts`)
  - *Fix:* Keep each `it`/`test` block focused with `1–8` explicit typed `expect(...)` assertions and avoid `any` or `@ts-ignore` in test files (compare [`zod_firstparty.test.ts`](../../../samples/typescript/bad/zod_firstparty.test.ts) with [`zod_validations.test.ts`](../../../samples/typescript/good/zod_validations.test.ts)).

