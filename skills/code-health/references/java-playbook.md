# Java Refactoring Playbook

> **Profile:** `java` · **Detection:** `.java` files (native Tree-Sitter CST via `tree-sitter-java`) · **Force:** `--lang java --framework none` (or omit `--framework` for non-Spring projects)
> **Worked examples:** [good](../../../samples/java/good/) · [bad](../../../samples/java/bad/)

This reference provides targeted refactoring patterns to resolve deterministic code health penalties in standard Java code. For Spring Boot rules (`@Autowired`, `@RestController`, `@Transactional`, JPQL/JDBC SQL checks), also read the [Spring Boot Architectural Refactoring Playbook](java-spring-playbook.md).

---

## 1. Single Responsibility & Cohesion (SRP)

- **Finding: `SRP: LCOM4=X disconnected method groups`** (`-15.0 pts` per component over `1` when class has `> 2` methods)
  - *Cause:* Methods in a class touch disjoint subsets of fields (`this.field` / field identifiers) and do not call each other, signaling multiple unrelated responsibilities inside one class (see [`SinglyLinkedList.java`](../../../samples/java/bad/SinglyLinkedList.java)).
  - *Fix:* Split unrelated groups of fields and methods into cohesive collaborator classes or move stateless helpers into package-private utility classes.
  - *Exemptions:* Java `record` and `enum` declarations automatically score `LCOM4 = 1`.

- **Finding: `SRP: methods=X (>10)`** (`-4.0 pts` per method over `10`) and **`SRP: self attributes=X (>7)`** (`-4.0 pts` per field over `7`)
  - *Cause:* God class accumulating parsing, formatting, I/O helpers, and data structures in one class (see [`DivisibleByTwentyFiveGodClass.java`](../../../samples/java/bad/DivisibleByTwentyFiveGodClass.java) vs [`DivisibleByTwentyFiveClean.java`](../../../samples/java/good/DivisibleByTwentyFiveClean.java)).
  - *Fix:* Extract cohesive sub-components (e.g. a dedicated `ScannerReader`, `Node` helper, or domain value object) and delegate via composition.

- **Finding: `SRP: high external call fan-out=X (>6)`** (`-3.0 pts` per distinct call over `6`, capped at `-36.0 pts`)
  - *Cause:* Single method (often `main` or an orchestrator) invokes too many distinct external helpers or I/O APIs directly.
  - *Fix:* Group related setup, formatting, or validation calls into named helper methods or a service facade.

- **Finding: `SRP: boolean flag parameter with default value`** / **`SRP: mixes X concerns (...)`** (`-12.0 pts` per concern over `2`)
  - *Cause:* Method mixes multiple concern domains (e.g., `filesystem_io` like `Files.readString`/`Files.writeString` plus serialization or transport) in one unit.
  - *Fix:* Separate pure domain algorithms from I/O adapters and split boolean-branched behaviors into explicit methods.

---

## 2. Size & Readability

- **Finding: `Size: LOC=X (>25)`** (`-1.5 pts`/line for `26–50`, `-2.5 pts`/line above `50`; test files allow `<= 40` LOC)
  - *Cause:* Long monolithic method body (e.g., `SinglyLinkedList.swapNodes` or `DivisibleByTwentyFiveBranchy.main`).
  - *Fix:* Extract cohesive steps into private helper methods (compare [`DivisibleByTwentyFiveModular.java`](../../../samples/java/good/DivisibleByTwentyFiveModular.java) with [`DivisibleByTwentyFiveBranchy.java`](../../../samples/java/bad/DivisibleByTwentyFiveBranchy.java)).

- **Finding: `Size: class LOC=X (>200)`** (`-0.4 pts` per line over `200`) and **`Size: file LOC=X (>350)`** (`-0.15 pts`/line for `351–600`, `-0.25 pts`/line above `600`)
  - *Fix:* Move nested or auxiliary types (`Node`, `Iterator`, IO wrappers) into their own top-level package files.

- **Finding: `Size: params=X (>4)`** (`-6.0 pts` per parameter over `4`)
  - *Fix:* Introduce a parameter `record` or builder/request object to bundle related arguments.

- **Finding: `Size: nesting depth=X (>3)`** (`-10.0 pts` per level over `3`)
  - *Fix:* Invert conditions into early `return` / `continue` guard clauses and extract inner loop bodies:
    ```java
    // Before (nesting = 4)
    if (node != null) {
        if (node.isActive()) {
            for (Item item : node.items()) {
                if (item.isValid()) {
                    process(item);
                }
            }
        }
    }

    // After (nesting = 2)
    if (node == null || !node.isActive()) {
        return;
    }
    for (Item item : node.items()) {
        if (item.isValid()) {
            process(item);
        }
    }
    ```

---

## 3. Complexity & Control Flow

- **Finding: `Complexity: CC=X (>5)`** (`-4.0 pts`/pt for `6–10`, `-7.0 pts`/pt above `10`) and **`Complexity: cognitive=X (>8)`** (`-2.5 pts`/pt over `8`)
  - *Cause:* Deeply nested `if`/`else` chains, large `switch` blocks, or multi-condition boolean expressions.
  - *Fix:* Replace branching chains with `Map`-based dispatch, Java `switch` expressions, or small predicate helpers; extract nested loops into dedicated methods.

- **Finding: `Complexity: returns=X (>3)`** (`-4.0 pts` per return over `3`)
  - *Fix:* Consolidate trailing branches or move input validation into a helper so the core method has `<= 3` exit points.

- **Finding: `Complexity: total class CC=X (>25)`** (`-1.5 pts` per point over `25`)
  - *Cause:* Too many branchy methods accumulated in one class.
  - *Fix:* Decompose responsibilities into smaller collaborator classes so each class stays `<= 25` total CC.

---

## 4. Clean Code & Maintainability

- **Finding: `Clean: missing class docstring`** (`-15.0 pts`) and **`Clean: missing public docstring`** (`-5.0 pts` if method `<= 10` LOC, `-10.0 pts` if `> 10` LOC)
  - *Cause:* Public class, constructor, or method lacks a Javadoc (`/** ... */`) block within 3 lines above its declaration (note: Java private methods still trigger if their method name does not start with `_`; check scorecard output on public/package methods).
  - *Fix:* Add concise Javadoc comments above the class and each public method:
    ```java
    /** Computes the count of valid 25-divisible substitutions. */
    public static int countValidPatterns(String mask) { ... }
    ```

- **Finding: `Clean: swallowed broad except Exception at L<n> (-10.0 pts)`**
  - *Cause:* A `catch` block catching `Exception` or `Throwable` with an empty body (`{}`).
  - *Fix:* Catch the specific checked/runtime exception type and handle, log, or rethrow it with context:
    ```java
    // Before
    try {
        parseConfig(path);
    } catch (Exception e) {
    }

    // After
    try {
        parseConfig(path);
    } catch (IOException e) {
        throw new UncheckedIOException("Failed to load config: " + path, e);
    }
    ```

- **Finding: `Clean (DRY): DRY-XXX (type1|type2|type3, N toks, M LOC) L<start>-<end> in <symbol> matches <peer>:<start>-<end> (<peer_symbol>)`**
  - *Cause:* Duplicated validation, traversal, symmetric left/right branches, or repeated JUnit test bodies across methods or classes ($\ge 35$ tokens / $\ge 5$ lines in source; $\ge 55$ tokens / $\ge 8$ lines in tests).
  - *Fix:* Extract package-private or static utility helpers, parameterize symmetric operations (e.g., passing a direction/comparator enum or `Function` strategy), and convert repeated `@Test` methods into JUnit 5 `@ParameterizedTest` with `@MethodSource` / `@CsvSource`.

---

## 5. Security & Operational Hygiene

- **Finding: `Security: unsafe <call>() at L<n> (-40.0 pts)`**
  - *Cause:* Direct invocation of unsafe dynamic evaluation/deserialization primitives.
  - *Fix:* Replace dynamic evaluation with safe typed parsers, allowlisted schemas, or parameterized APIs.

---

## 6. Test Hygiene

Test files (`*Test.java`, `*Tests.java`, `*IT.java`, or paths inside `test/` / `tests/`) are exempt from SRP and Security checks and allow `<= 40` LOC per test method, while enforcing assertion hygiene on `test*` / `should*` / `@Test` / `@ParameterizedTest` / `@RepeatedTest` methods:

- **Finding: `Clean (Test): test has 0 assertions (-30.0 pts)`**
  - *Fix:* Add explicit JUnit 5 (`assertEquals`, `assertTrue`, `assertThrows`, `assertAll`) or AssertJ (`assertThat(...)`) assertions in the test body rather than relying on "did not throw".
- **Finding: `Clean (Test): X assertions in single test (>8)`** (`-3.0 pts` per assertion over `8`, capped at `-30.0 pts`)
  - *Fix:* Split large multi-scenario test methods into focused per-behavior `@Test` cases or `@ParameterizedTest` variants.

