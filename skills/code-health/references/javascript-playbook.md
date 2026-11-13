# JavaScript / JSX Refactoring Playbook

> **Profile:** `javascript` · **Detection:** `.js`, `.jsx`, `.mjs`, `.cjs` files (native Tree-Sitter CST via `tree-sitter-javascript`; minified `*.min.*` / `*.bundle.js` and lines `> 1000` chars are skipped) · **Force:** `--lang javascript` (or `--lang js`)
> **Worked examples:** [good](../../../samples/javascript/good/) · [bad](../../../samples/javascript/bad/)

This reference provides targeted refactoring patterns for vanilla JavaScript and ECMAScript test suites. If JSX or React/Next.js imports are detected, also read the [React Refactoring Playbook](react-playbook.md) or [Next.js Refactoring Playbook](nextjs-playbook.md).

---

## 1. Single Responsibility & Cohesion (SRP)

- **Finding: `SRP: LCOM4=X disconnected method groups`** (`-15.0 pts` per group over `1` when class has `> 2` non-constructor methods)
  - *Cause:* A class bundles unrelated methods and `this.*` fields that never interact (see [`trie_god_class.js`](../../../samples/javascript/bad/trie_god_class.js) vs [`trie_clean.js`](../../../samples/javascript/good/trie_clean.js)).
  - *Fix:* Split unrelated capabilities (e.g., CSV parsing, logging, caching) into separate modules or focused classes grouped by shared state.

- **Finding: `SRP: methods=X (>10)`** / **`SRP: self attributes=X (>7)`** (`-4.0 pts` each above threshold)
  - *Fix:* Extract cohesive helper classes (such as `TrieNode` + `Trie` in [`trie_clean.js`](../../../samples/javascript/good/trie_clean.js)) or stateless module helpers.

- **Finding: `SRP: high external call fan-out=X (>6)`** (`-3.0 pts` per call over `6`, capped at `-36.0 pts`)
  - *Fix:* Delegate sub-workflows (e.g., distance initialization, neighbor relaxation) to small helper functions.

- **Finding: `SRP: mixes X concerns (...)`** (`-12.0 pts` per concern over `2`)
  - *Fix:* Keep pure algorithmic/domain functions separate from network, storage, DOM, or `console.*` I/O calls.

---

## 2. Size & Readability

- **Finding: `Size: LOC=X (>25)`** (`-1.5 pts`/line for `26–50`, `-2.5 pts`/line above `50`; tests allow `<= 40` LOC)
  - *Cause:* Monolithic functions handling initialization, scanning, and state updates inline (see [`dijkstra_branchy.js`](../../../samples/javascript/bad/dijkstra_branchy.js)).
  - *Fix:* Decompose into single-purpose functions (`initDistances`, `minDistanceNode`, `relaxNeighbors`, `dijkstra` in [`dijkstra_clean.js`](../../../samples/javascript/good/dijkstra_clean.js)).

- **Finding: `Size: params=X (>4)`** (`-6.0 pts` per parameter over `4`)
  - *Fix:* Accept an options object with destructuring and defaults (`function solve({ graph, start, target, weighted = true })`).

- **Finding: `Size: nesting depth=X (>3)`** (`-10.0 pts` per level over `3`)
  - *Fix:* Replace nested `if` blocks with guard clauses (`if (!visited.has(node)) continue;` or early `return`).

---

## 3. Complexity & Control Flow

- **Finding: `Complexity: CC=X (>5)`** (`-4.0 pts`/pt for `6–10`, `-7.0 pts`/pt above `10`), **`Complexity: cognitive=X (>8)`** (`-2.5 pts`/pt over `8`), and **`Complexity: returns=X (>3)`** (`-4.0 pts` per return over `3`)
  - *Cause:* Deeply nested loops/branches, `switch` chains, or multiple scattered `return` statements.
  - *Fix:* Extract inner loop logic into well-named helpers and replace branching ladders with object/Map dispatch tables.

---

## 4. Clean Code & Maintainability

- **Finding: `Clean: X legacy 'var' declaration(s) detected (prefer 'const' or 'let')`** (`-3.0 pts` each, capped at `-15.0 pts`)
  - *Cause:* Function-scoped `var` risks hoisting bugs and unintended mutation.
  - *Fix:* Replace `var` with `const` (default) or `let` (when reassigned).

- **Finding: `Clean: X loose equality comparison(s) (==/!=) trigger implicit type coercion (prefer ===/!==)`** (`-2.0 pts` each, capped at `-10.0 pts`)
  - *Cause:* `==` and `!=` silently coerce types (`"" == 0`, `null == undefined`).
  - *Fix:* Use strict equality (`===` and `!==`).

- **Finding: `Clean: empty catch block swallows exception (-10.0 pts)`**
  - *Cause:* `catch (err) {}` hides failures silently.
  - *Fix:* Log, recover explicitly, or rethrow the error:
    ```javascript
    // Before
    try { return JSON.parse(raw); } catch (e) {}

    // After
    try {
      return JSON.parse(raw);
    } catch (error) {
      throw new Error(`Invalid JSON payload: ${error.message}`, { cause: error });
    }
    ```

- **Finding: `Clean: debugger statement detected (-10.0 pts)`**
  - *Fix:* Remove leftover `debugger;` statements before committing.

- **Finding: `Clean: X unannotated parameter(s) without default values (...)`** (`-2.0 pts` each, capped at `-10.0 pts` on non-test functions)
  - *Cause:* Parameters lack both a default value (`param = default`) and a JSDoc `@param {type}` tag.
  - *Fix:* Add JSDoc `@param {type} name` annotations or meaningful default values (see [`clean_math_service.js`](../../../samples/javascript/good/clean_math_service.js)):
    ```javascript
    /**
     * Add two numbers.
     * @param {number} left
     * @param {number} right
     * @returns {number}
     */
    add(left, right) {
      return left + right;
    }
    ```

- **Finding: `Clean: missing class docstring`** (`-15.0 pts`) and **`Clean: missing public docstring`** (`-5.0 pts` if `<= 10` LOC, `-10.0 pts` if `> 10` LOC)
  - *Fix:* Add a JSDoc `/** ... */` block immediately above classes, exported functions, and public methods (not `_private` helpers).

---

## 5. Security & Boundary Hygiene

All five rules below are demonstrated in [`smelly_legacy_script.js`](../../../samples/javascript/bad/smelly_legacy_script.js):

- **Finding: `Security: dynamic code execution via eval (-40.0 pts)`** / **`Security: dynamic code execution via new Function (-40.0 pts)`**
  - *Cause:* `eval(...)`, `window.eval(...)`, `globalThis.eval(...)`, or `new Function(...)` executes arbitrary strings as code.
  - *Fix:* Replace with `JSON.parse(...)`, structured expression evaluators, or static lookup maps.

- **Finding: `Security: string argument to setTimeout causes implicit code evaluation (-20.0 pts)`** (also `setInterval`)
  - *Cause:* Passing a string literal/template (`setTimeout("run()", 100)`) triggers implicit `eval`.
  - *Fix:* Pass a function reference or arrow callback (`setTimeout(() => run(), 100)`).

- **Finding: `Security: direct prototype mutation via '__proto__' (-25.0 pts)`**
  - *Cause:* Assigning `obj.__proto__ = ...` or calling `Object.setPrototypeOf(...)` risks prototype pollution and severe V8 deoptimization.
  - *Fix:* Use `Object.create(proto)` at construction time, `Object.assign({}, source)` with explicit allowlisted keys, or `Map`/`Set` for dynamic dictionaries.

- **Finding: `Security: 'with' statement obscures lexical scope and risks prototype pollution (-30.0 pts)`**
  - *Cause:* `with (obj) { ... }` dynamically alters lexical scope resolution and is forbidden in strict mode.
  - *Fix:* Use destructuring (`const { a, b } = obj;`) or explicit property access.

---

## 6. Test Hygiene

Test functions (`it(...)`, `test(...)`, `it.only(...)`, `test.skip(...)`, etc. inside `*.test.js`, `*.spec.js`, `_test.js`, `*.test.jsx`, `*.test.mjs`, `*.test.cjs`, or `tests/` / `test/` / `__tests__/`) are exempt from SRP, Security, and parameter-annotation checks, and allow `<= 40` LOC per test. Recognized assertions include Node `assert` (`assert`, `assertEquals`, `strictEqual`, `deepStrictEqual`, `ok`), Jest/Vitest (`expect`, `toBe`, `toEqual`, `toStrictEqual`, `toThrow`, `toBeTruthy`, `toBeFalsy`, `toHaveLength`), and Chai (`should`, `equal`).

- **Finding: `Clean (Test): test has 0 assertions (-30.0 pts)`**
  - *Fix:* Add explicit `assert.*` or `expect(...).*` checks directly inside each `it`/`test` block (compare [`graph_algorithms_bad.test.js`](../../../samples/javascript/bad/graph_algorithms_bad.test.js) with [`graph_algorithms.test.js`](../../../samples/javascript/good/graph_algorithms.test.js)).
- **Finding: `Clean (Test): X assertions in single test (>8)`** (`-3.0 pts` per assertion over `8`, capped at `-30.0 pts`)
  - *Fix:* Split monolithic tests into focused `it(...)` / `test(...)` cases covering one behavior each (`<= 8` assertions per test).

