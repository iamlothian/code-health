# Multi-Language Code Health Scorecard Baselines

This catalog provides functionally comparable, human-inspectable **Good** and **Bad** code samples across every supported language and framework profile (**Python**, **Java**, **Java Spring Boot**, **Vanilla JavaScript**, and **TypeScript / TSX**).

Each scenario pairs a **Good** and **Bad** file solving the **same problem or performing comparable domain functionality** from public competitive programming datasets ([`deepmind/code_contests`](https://huggingface.co/datasets/deepmind/code_contests)) and established open-source benchmarks ([`TheAlgorithms/Python`](https://github.com/TheAlgorithms/Python), [`TheAlgorithms/Java`](https://github.com/TheAlgorithms/Java), [`spring-projects/spring-petclinic`](https://github.com/spring-projects/spring-petclinic), [`spring-petclinic-microservices`](https://github.com/spring-petclinic/spring-petclinic-microservices), [`OWASP WebGoat`](https://github.com/WebGoat/WebGoat), [`PyCQA/bandit`](https://github.com/PyCQA/bandit), [`pallets/click`](https://github.com/pallets/click), and [MDN Web Docs JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)).

Each sample file `<filename>` has a matching `<filename>.expected.json` sidecar file and is continuously verified by `tests/unit/test_language_scorecard_samples.py`.

---

## Quick Summary Table

| Profile | Scenario | Quality | Sample File | Dataset Source | LOC | SRP | Size | Comp | Clean | Sec | Score | Grade |
| :--- | :--- | :---: | :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| `python (auto)` | 1. Shortest-Path Graph Algorithm Complexity & Decomposition (TheAlgorithms/Python graphs/) | **GOOD** | [`python/good/bellman_ford.py`](python/good/bellman_ford.py) | [TheAlgorithms/Python (graphs/bellman_ford.py)](https://github.com/TheAlgorithms/Python/blob/master/graphs/bellman_ford.py) | 56 | 100.0 | 100.0 | 97.8 | 86.9 | 100.0 | **97.6** | **A** |
| `python (auto)` | 1. Shortest-Path Graph Algorithm Complexity & Decomposition (TheAlgorithms/Python graphs/) | **BAD** | [`python/bad/a_star.py`](python/bad/a_star.py) | [TheAlgorithms/Python (graphs/a_star.py)](https://github.com/TheAlgorithms/Python/blob/master/graphs/a_star.py) | 118 | 100.0 | 14.0 | 10.5 | 90.0 | 100.0 | **15.5** | **F** |
| `python (auto)` | 2. Binary Tree Data Structure OOP Design (TheAlgorithms/Python binary_tree/) | **GOOD** | [`python/good/fenwick_tree.py`](python/good/fenwick_tree.py) | [TheAlgorithms/Python (data_structures/binary_tree/fenwick_tree.py)](https://github.com/TheAlgorithms/Python/blob/master/data_structures/binary_tree/fenwick_tree.py) | 202 | 96.0 | 100.0 | 96.6 | 85.1 | 100.0 | **95.9** | **A** |
| `python (auto)` | 2. Binary Tree Data Structure OOP Design (TheAlgorithms/Python binary_tree/) | **BAD** | [`python/bad/red_black_tree.py`](python/bad/red_black_tree.py) | [TheAlgorithms/Python (data_structures/binary_tree/red_black_tree.py)](https://github.com/TheAlgorithms/Python/blob/master/data_structures/binary_tree/red_black_tree.py) | 613 | 49.1 | 0.0 | 25.4 | 65.5 | 100.0 | **5.0** | **F** |
| `python (auto)` | 3. Serialization & I/O Security Hygiene (PyCQA/bandit examples/, 19 LOC) | **GOOD** | [`python/good/urlopen.py`](python/good/urlopen.py) | [PyCQA/bandit (examples/urlopen.py)](https://github.com/PyCQA/bandit/blob/main/examples/urlopen.py) | 19 | 100.0 | 100.0 | 100.0 | 80.0 | 100.0 | **97.0** | **A** |
| `python (auto)` | 3. Serialization & I/O Security Hygiene (PyCQA/bandit examples/, 19 LOC) | **BAD** | [`python/bad/yaml_load.py`](python/bad/yaml_load.py) | [PyCQA/bandit (examples/yaml_load.py)](https://github.com/PyCQA/bandit/blob/main/examples/yaml_load.py) | 19 | 100.0 | 100.0 | 100.0 | 75.0 | 60.0 | **65.0** | **D** |
| `python (auto)` | 4. CLI Command & Option Test Suite Hygiene (pallets/click tests/) | **GOOD** | [`python/good/test_info_dict.py`](python/good/test_info_dict.py) | [pallets/click (tests/test_info_dict.py)](https://github.com/pallets/click/blob/main/tests/test_info_dict.py) | 322 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `python (auto)` | 4. CLI Command & Option Test Suite Hygiene (pallets/click tests/) | **BAD** | [`python/bad/test_commands.py`](python/bad/test_commands.py) | [pallets/click (tests/test_commands.py)](https://github.com/pallets/click/blob/main/tests/test_commands.py) | 544 | 100.0 | 68.9 | 100.0 | 92.8 | 100.0 | **73.9** | **C** |
| `java (none)` | 1. Competitive Programming Contest Class Structure (Same Problem: Codeforces 1575D) | **GOOD** | [`java/good/DivisibleByTwentyFiveClean.java`](java/good/DivisibleByTwentyFiveClean.java) | [DeepMind code_contests (test split, Problem 1575_D. Divisible by Twenty-Five, Solution #57)](https://huggingface.co/datasets/deepmind/code_contests) | 132 | 100.0 | 100.0 | 100.0 | 75.0 | 100.0 | **96.2** | **A** |
| `java (none)` | 1. Competitive Programming Contest Class Structure (Same Problem: Codeforces 1575D) | **BAD** | [`java/bad/DivisibleByTwentyFiveGodClass.java`](java/bad/DivisibleByTwentyFiveGodClass.java) | [DeepMind code_contests (test split, Problem 1575_D. Divisible by Twenty-Five, Solution #45)](https://huggingface.co/datasets/deepmind/code_contests) | 611 | 0.0 | 0.0 | 0.0 | 94.1 | 100.0 | **5.0** | **F** |
| `java (none)` | 2. Method Complexity & Control Flow (Same Problem: Codeforces 1575D) | **GOOD** | [`java/good/DivisibleByTwentyFiveModular.java`](java/good/DivisibleByTwentyFiveModular.java) | [DeepMind code_contests (test split, Problem 1575_D. Divisible by Twenty-Five, Solution #46)](https://huggingface.co/datasets/deepmind/code_contests) | 79 | 100.0 | 96.5 | 93.3 | 76.7 | 100.0 | **94.3** | **A** |
| `java (none)` | 2. Method Complexity & Control Flow (Same Problem: Codeforces 1575D) | **BAD** | [`java/bad/DivisibleByTwentyFiveBranchy.java`](java/bad/DivisibleByTwentyFiveBranchy.java) | [DeepMind code_contests (test split, Problem 1575_D. Divisible by Twenty-Five, Solution #32)](https://huggingface.co/datasets/deepmind/code_contests) | 42 | 100.0 | 79.0 | 39.5 | 75.0 | 100.0 | **44.5** | **F** |
| `java (none)` | 3. Linked List Data Structure Cohesion & Method Count (TheAlgorithms/Java lists/, ~250 LOC) | **GOOD** | [`java/good/DoublyLinkedList.java`](java/good/DoublyLinkedList.java) | [TheAlgorithms/Java (src/main/java/com/thealgorithms/datastructures/lists/DoublyLinkedList.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/datastructures/lists/DoublyLinkedList.java) | 234 | 96.6 | 99.2 | 93.1 | 99.4 | 100.0 | **97.3** | **A** |
| `java (none)` | 3. Linked List Data Structure Cohesion & Method Count (TheAlgorithms/Java lists/, ~250 LOC) | **BAD** | [`java/bad/SinglyLinkedList.java`](java/bad/SinglyLinkedList.java) | [TheAlgorithms/Java (src/main/java/com/thealgorithms/datastructures/lists/SinglyLinkedList.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/datastructures/lists/SinglyLinkedList.java) | 281 | 15.7 | 66.7 | 50.2 | 98.9 | 100.0 | **20.7** | **F** |
| `java (spring-boot)` | 1. Multi-Endpoint PetClinic REST Controller Layering (spring-petclinic-microservices, ~44 LOC) | **GOOD** | [`java-spring/good/ApiGatewayController.java`](java-spring/good/ApiGatewayController.java) | [spring-petclinic/spring-petclinic-microservices (boundary/web/ApiGatewayController.java)](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/spring-petclinic-api-gateway/src/main/java/org/springframework/samples/petclinic/api/boundary/web/ApiGatewayController.java) | 40 | 94.0 | 100.0 | 100.0 | 92.5 | 100.0 | **97.1** | **A** |
| `java (spring-boot)` | 1. Multi-Endpoint PetClinic REST Controller Layering (spring-petclinic-microservices, ~44 LOC) | **BAD** | [`java-spring/bad/PetResource.java`](java-spring/bad/PetResource.java) | [spring-petclinic/spring-petclinic-microservices (customers/web/PetResource.java)](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/spring-petclinic-customers-service/src/main/java/org/springframework/samples/petclinic/customers/web/PetResource.java) | 48 | 58.7 | 100.0 | 100.0 | 94.3 | 100.0 | **63.7** | **D** |
| `java (spring-boot)` | 2. JDBC SQL Query Endpoint: Parameterized vs String Concatenation (OWASP WebGoat sqlinjection/) | **GOOD** | [`java-spring/good/Servers.java`](java-spring/good/Servers.java) | [OWASP WebGoat (sqlinjection/mitigation/Servers.java)](https://github.com/WebGoat/WebGoat/blob/main/src/main/java/org/owasp/webgoat/lessons/sqlinjection/mitigation/Servers.java) | 46 | 100.0 | 98.5 | 100.0 | 77.5 | 100.0 | **96.2** | **A** |
| `java (spring-boot)` | 2. JDBC SQL Query Endpoint: Parameterized vs String Concatenation (OWASP WebGoat sqlinjection/) | **BAD** | [`java-spring/bad/SqlInjectionLesson8.java`](java-spring/bad/SqlInjectionLesson8.java) | [OWASP WebGoat (sqlinjection/introduction/SqlInjectionLesson8.java)](https://github.com/WebGoat/WebGoat/blob/main/src/main/java/org/owasp/webgoat/lessons/sqlinjection/introduction/SqlInjectionLesson8.java) | 104 | 90.4 | 94.0 | 97.6 | 77.0 | 60.0 | **65.0** | **D** |
| `java (spring-boot)` | 3. Spring Boot @WebMvcTest Controller Test Suite Hygiene (spring-petclinic owner/, ~208 LOC) | **GOOD** | [`java-spring/good/PetControllerTests.java`](java-spring/good/PetControllerTests.java) | [spring-projects/spring-petclinic (owner/PetControllerTests.java)](https://github.com/spring-projects/spring-petclinic/blob/main/src/test/java/org/springframework/samples/petclinic/owner/PetControllerTests.java) | 193 | 100.0 | 100.0 | 100.0 | 92.0 | 100.0 | **98.8** | **A** |
| `java (spring-boot)` | 3. Spring Boot @WebMvcTest Controller Test Suite Hygiene (spring-petclinic owner/, ~208 LOC) | **BAD** | [`java-spring/bad/OwnerControllerTests.java`](java-spring/bad/OwnerControllerTests.java) | [spring-projects/spring-petclinic (owner/OwnerControllerTests.java)](https://github.com/spring-projects/spring-petclinic/blob/main/src/test/java/org/springframework/samples/petclinic/owner/OwnerControllerTests.java) | 224 | 60.0 | 90.4 | 100.0 | 91.8 | 100.0 | **65.0** | **D** |
| `javascript (none)` | 1. Modern ECMAScript Arithmetic Service vs. Legacy Smelly Script | **GOOD** | [`javascript/clean_math_service.js`](javascript/clean_math_service.js) | [Custom JavaScript Benchmark](https://developer.mozilla.org/en-US/docs/Web/JavaScript) | 21 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `javascript (none)` | 1. Modern ECMAScript Arithmetic Service vs. Legacy Smelly Script | **BAD** | [`javascript/smelly_legacy_script.js`](javascript/smelly_legacy_script.js) | [Custom JavaScript Benchmark](https://developer.mozilla.org/en-US/docs/Web/JavaScript) | 19 | 100.0 | 100.0 | 100.0 | 53.0 | 0.0 | **5.0** | **F** |
| `javascript (none)` | 2. Graph Dijkstra Shortest Path Algorithm Complexity & Control Flow | **GOOD** | [`javascript/dijkstra_clean.js`](javascript/dijkstra_clean.js) | [TheAlgorithms/JavaScript (Graphs/Dijkstra.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Graphs/Dijkstra.js) | 41 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `javascript (none)` | 2. Graph Dijkstra Shortest Path Algorithm Complexity & Control Flow | **BAD** | [`javascript/dijkstra_branchy.js`](javascript/dijkstra_branchy.js) | [TheAlgorithms/JavaScript (Graphs/Dijkstra.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Graphs/Dijkstra.js) | 79 | 100.0 | 0.0 | 0.0 | 55.0 | 100.0 | **5.0** | **F** |
| `javascript (none)` | 3. Trie Prefix Tree Data Structure OOP Cohesion & Class Size | **GOOD** | [`javascript/trie_clean.js`](javascript/trie_clean.js) | [TheAlgorithms/JavaScript (Data-Structures/Trie/Trie.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Data-Structures/Trie/Trie.js) | 42 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `javascript (none)` | 3. Trie Prefix Tree Data Structure OOP Cohesion & Class Size | **BAD** | [`javascript/trie_god_class.js`](javascript/trie_god_class.js) | [TheAlgorithms/JavaScript (Data-Structures/Trie/Trie.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Data-Structures/Trie/Trie.js) | 92 | 0.0 | 100.0 | 100.0 | 78.0 | 100.0 | **5.0** | **F** |
| `javascript (none)` | 4. BDD Algorithmic Test Suite Hygiene & Assertion Density | **GOOD** | [`javascript/graph_algorithms.test.js`](javascript/graph_algorithms.test.js) | [TheAlgorithms/JavaScript (test suites)](https://github.com/TheAlgorithms/JavaScript) | 33 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `javascript (none)` | 4. BDD Algorithmic Test Suite Hygiene & Assertion Density | **BAD** | [`javascript/graph_algorithms_bad.test.js`](javascript/graph_algorithms_bad.test.js) | [TheAlgorithms/JavaScript (test suites)](https://github.com/TheAlgorithms/JavaScript) | 41 | 100.0 | 100.0 | 100.0 | 70.0 | 100.0 | **75.0** | **C** |
| `typescript (auto)` | 1. Strictly Typed TypeScript Arithmetic Service vs. Legacy Escape-Hatch Script | **GOOD** | [`typescript/clean_math_service.ts`](typescript/clean_math_service.ts) | [Custom TypeScript Benchmark](https://www.typescriptlang.org/docs/) | 24 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `typescript (auto)` | 1. Strictly Typed TypeScript Arithmetic Service vs. Legacy Escape-Hatch Script | **BAD** | [`typescript/smelly_legacy_script.ts`](typescript/smelly_legacy_script.ts) | [Custom TypeScript Benchmark](https://www.typescriptlang.org/docs/) | 19 | 94.0 | 100.0 | 100.0 | 21.0 | 0.0 | **5.0** | **F** |
| `typescript (auto)` | 2. Graph Shortest-Path Algorithmic Complexity (Decomposed Typed Dijkstra vs. Monolith) | **GOOD** | [`typescript/dijkstra_clean.ts`](typescript/dijkstra_clean.ts) | [Custom TypeScript Benchmark (modeled after TheAlgorithms Dijkstra)](https://github.com/TheAlgorithms/TypeScript) | 88 | 100.0 | 100.0 | 99.0 | 100.0 | 100.0 | **99.8** | **A** |
| `typescript (auto)` | 2. Graph Shortest-Path Algorithmic Complexity (Decomposed Typed Dijkstra vs. Monolith) | **BAD** | [`typescript/dijkstra_branchy.ts`](typescript/dijkstra_branchy.ts) | [Custom TypeScript Benchmark (Legacy Branchy Shortest Path)](https://github.com/TheAlgorithms/TypeScript) | 81 | 82.0 | 0.0 | 0.0 | 8.0 | 100.0 | **5.0** | **F** |
| `typescript (auto)` | 3. OOP Cache Cohesion & Parameter Properties (Cohesive LRUCache vs. God Class) | **GOOD** | [`typescript/lru_cache_clean.ts`](typescript/lru_cache_clean.ts) | [Custom TypeScript Benchmark](https://www.typescriptlang.org/docs/handbook/2/classes.html) | 70 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `typescript (auto)` | 3. OOP Cache Cohesion & Parameter Properties (Cohesive LRUCache vs. God Class) | **BAD** | [`typescript/lru_cache_god_class.ts`](typescript/lru_cache_god_class.ts) | [Custom TypeScript Benchmark](https://www.typescriptlang.org/docs/handbook/2/classes.html) | 86 | 50.0 | 100.0 | 100.0 | 65.8 | 100.0 | **55.0** | **F** |
| `typescript (auto)` | 4. Backend Repository Security & SQL Injection (Parameterized Queries vs. Unsafe Interpolation) | **GOOD** | [`typescript/order_repository_clean.ts`](typescript/order_repository_clean.ts) | [Custom TypeScript Benchmark](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) | 52 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `typescript (auto)` | 4. Backend Repository Security & SQL Injection (Parameterized Queries vs. Unsafe Interpolation) | **BAD** | [`typescript/order_repository_unsafe.ts`](typescript/order_repository_unsafe.ts) | [Custom TypeScript Benchmark](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) | 34 | 82.6 | 100.0 | 100.0 | 53.6 | 20.0 | **25.0** | **F** |
| `typescript (auto)` | 5. React 18 TSX Component Decomposition & Props Hygiene vs. Monolithic TSX Board | **GOOD** | [`typescript/task_filter_bar.tsx`](typescript/task_filter_bar.tsx) | [Custom TypeScript/React TSX Benchmark](https://react.dev/learn/typescript) | 75 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `typescript (auto)` | 5. React 18 TSX Component Decomposition & Props Hygiene vs. Monolithic TSX Board | **BAD** | [`typescript/task_board_legacy.tsx`](typescript/task_board_legacy.tsx) | [Custom TypeScript/React TSX Benchmark](https://react.dev/learn/typescript) | 51 | 79.0 | 6.5 | 0.0 | 46.0 | 100.0 | **5.0** | **F** |
| `typescript (auto)` | 6. Async Webhook Dispatcher Size & Contract Clarity vs. Oversized Monolithic Handler | **GOOD** | [`typescript/webhook_dispatcher_clean.ts`](typescript/webhook_dispatcher_clean.ts) | [Custom TypeScript Benchmark](https://www.typescriptlang.org/docs/) | 47 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `typescript (auto)` | 6. Async Webhook Dispatcher Size & Contract Clarity vs. Oversized Monolithic Handler | **BAD** | [`typescript/webhook_dispatcher_smelly.ts`](typescript/webhook_dispatcher_smelly.ts) | [Custom TypeScript Benchmark](https://www.typescriptlang.org/docs/) | 53 | 82.0 | 29.0 | 0.0 | 45.0 | 80.0 | **5.0** | **F** |
| `typescript (auto)` | 7. Jest/Vitest TypeScript BDD Test Suite Assertion Density & Type Safety | **GOOD** | [`typescript/dijkstra.test.ts`](typescript/dijkstra.test.ts) | [Custom TypeScript Test Benchmark](https://vitest.dev/) | 31 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `typescript (auto)` | 7. Jest/Vitest TypeScript BDD Test Suite Assertion Density & Type Safety | **BAD** | [`typescript/dijkstra_bad.test.ts`](typescript/dijkstra_bad.test.ts) | [Custom TypeScript Test Benchmark](https://vitest.dev/) | 28 | 100.0 | 100.0 | 100.0 | 61.8 | 100.0 | **66.8** | **D** |

---

## Detailed Scenario Scorecards

### PYTHON (`--framework auto`) — 1. Shortest-Path Graph Algorithm Complexity & Decomposition (TheAlgorithms/Python graphs/)

#### Good Baseline: [`python/good/bellman_ford.py`](python/good/bellman_ford.py) ([sidecar JSON](python/good/bellman_ford.py.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Python (graphs/bellman_ford.py)](https://github.com/TheAlgorithms/Python/blob/master/graphs/bellman_ford.py) (`MIT`)
- **Expected Scorecard:** `Composite 97.6/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 97.8` | `Clean: 86.9` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 97.6/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 3
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 97.8 | Clean: 86.9 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/bellman_ford.py            src      56    - 100.0 100.0  97.8  86.9 100.0   97.6   A
    - Clean: missing module docstring (-10.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/bellman_ford.py:4 print_distance    4   2    1   2   1   98.5   A
    - Clean: 1 untyped param(s) (src) (-5.0 pts)
    - Clean: missing public docstring (-5.0 pts)
samples/python/good/bellman_ford.py:10 check_negativ    8   4    4   3   2   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/python/good/bellman_ford.py:20 bellman_ford    14   6    8   4   3   99.2   A
    - Complexity: CC=6 (>5) (-4.0 pts)
```

#### Bad Baseline: [`python/bad/a_star.py`](python/bad/a_star.py) ([sidecar JSON](python/bad/a_star.py.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Python (graphs/a_star.py)](https://github.com/TheAlgorithms/Python/blob/master/graphs/a_star.py) (`MIT`)
- **Expected Scorecard:** `Composite 15.5/100 (Grade F)` — `SRP: 100.0` | `Size: 14.0` | `Complexity: 10.5` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 15.5/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 14.0 | Complexity: 10.5 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/a_star.py                   src     118    - 100.0  14.0  10.5  90.0 100.0   15.5   F
    - Clean: missing module docstring (-10.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/a_star.py:12 search                 63  16   19   5   4   15.5   F
    - Size: LOC=63 (>25) (-70.0 pts)
    - Size: params=5 (>4) (-6.0 pts)
    - Size: nesting depth=4 (>3) (-10.0 pts)
    - Complexity: CC=16 (>5) (-62.0 pts)
    - Complexity: cognitive=19 (>8) (-27.5 pts)
```

### PYTHON (`--framework auto`) — 2. Binary Tree Data Structure OOP Design (TheAlgorithms/Python binary_tree/)

#### Good Baseline: [`python/good/fenwick_tree.py`](python/good/fenwick_tree.py) ([sidecar JSON](python/good/fenwick_tree.py.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Python (data_structures/binary_tree/fenwick_tree.py)](https://github.com/TheAlgorithms/Python/blob/master/data_structures/binary_tree/fenwick_tree.py) (`MIT`)
- **Expected Scorecard:** `Composite 95.9/100 (Grade A)` — `SRP: 96.0` | `Size: 100.0` | `Complexity: 96.6` | `Clean: 85.1` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 95.9/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 11
Dimensions -> SRP: 96.0 | Size: 100.0 | Complexity: 96.6 | Clean: 85.1 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/fenwick_tree.py            src     202    -  96.0 100.0  96.6  85.1 100.0   95.9   A
    - Clean: missing module docstring (-10.0 pts)
    - Clean: 1 mid-file/late import(s) (-4.0 pts)

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/fenwick_tree.py:4 FenwickTree    194   11     1   27   98.0   A
    - SRP: methods=11 (>10) (-4.0 pts)
    - Complexity: total class CC=27 (>25) (-3.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/fenwick_tree.py:73 FenwickTree.n    2   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/python/good/fenwick_tree.py:77 FenwickTree.p    2   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/python/good/fenwick_tree.py:198 FenwickTree.   14   6    6   1   2   99.2   A
    - Complexity: CC=6 (>5) (-4.0 pts)
samples/python/good/fenwick_tree.py:11 FenwickTree._    8   4    5   2   1  100.0   A
samples/python/good/fenwick_tree.py:28 FenwickTree.i    7   3    3   1   2  100.0   A
samples/python/good/fenwick_tree.py:53 FenwickTree.g    7   3    3   0   2  100.0   A
samples/python/good/fenwick_tree.py:80 FenwickTree.a    7   3    2   2   1  100.0   A
samples/python/good/fenwick_tree.py:107 FenwickTree.    2   1    0   2   0  100.0   A
samples/python/good/fenwick_tree.py:129 FenwickTree.    9   3    2   1   1  100.0   A
samples/python/good/fenwick_tree.py:156 FenwickTree.    2   1    0   2   0  100.0   A
samples/python/good/fenwick_tree.py:178 FenwickTree.    2   1    0   1   0  100.0   A
```

#### Bad Baseline: [`python/bad/red_black_tree.py`](python/bad/red_black_tree.py) ([sidecar JSON](python/bad/red_black_tree.py.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Python (data_structures/binary_tree/red_black_tree.py)](https://github.com/TheAlgorithms/Python/blob/master/data_structures/binary_tree/red_black_tree.py) (`MIT`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 49.1` | `Size: 0.0` | `Complexity: 25.4` | `Clean: 65.5` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 40
Dimensions -> SRP: 49.1 | Size: 0.0 | Complexity: 25.4 | Clean: 65.5 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/red_black_tree.py           src     613    -  49.1   0.0  25.4  65.5 100.0    5.0   F
    - Size: file LOC=613 (>350) (-40.8 pts)
    - Clean: missing module docstring (-10.0 pts)
    - Clean: 1 mid-file/late import(s) (-4.0 pts)
    - Clean: 4 duplicate code block(s) detected (-20.0 pts)

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/red_black_tree.py:6 RedBlackTre   427   27     1  160    5.0   F
    - SRP: methods=27 (>10) (-68.0 pts)
    - Size: class LOC=427 (>200) (-90.8 pts)
    - Complexity: total class CC=160 (>25) (-100.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/red_black_tree.py:112 RedBlackTre   34  17   49   0   4    5.0   F
    - Size: LOC=34 (>25) (-13.5 pts)
    - Size: nesting depth=4 (>3) (-10.0 pts)
    - Complexity: CC=17 (>5) (-69.0 pts)
    - Complexity: cognitive=49 (>8) (-100.0 pts)
samples/python/bad/red_black_tree.py:150 RedBlackTre   39  19   54   1   5    5.0   F
    - Size: LOC=39 (>25) (-21.0 pts)
    - Size: nesting depth=5 (>3) (-20.0 pts)
    - Complexity: CC=19 (>5) (-83.0 pts)
    - Complexity: cognitive=54 (>8) (-100.0 pts)
samples/python/bad/red_black_tree.py:205 RedBlackTre   71  31   22   0   2    5.0   F
    - Size: LOC=71 (>25) (-90.0 pts)
    - Complexity: CC=31 (>5) (-100.0 pts)
    - Complexity: cognitive=22 (>8) (-35.0 pts)
samples/python/bad/red_black_tree.py:367 RedBlackTre   14   7   13   1   3   76.5   C
    - Complexity: CC=7 (>5) (-8.0 pts)
    - Complexity: cognitive=13 (>8) (-12.5 pts)
    - Complexity: returns=5 (>3) (-8.0 pts)
samples/python/bad/red_black_tree.py:384 RedBlackTre   14   7   13   1   3   76.5   C
    - Complexity: CC=7 (>5) (-8.0 pts)
    - Complexity: cognitive=13 (>8) (-12.5 pts)
    - Complexity: returns=5 (>3) (-8.0 pts)
samples/python/bad/red_black_tree.py:688 pytests        8   8    0   0   0   95.9   A
    - SRP: high external call fan-out=7 (>6) (-3.0 pts)
    - Complexity: CC=8 (>5) (-12.0 pts)
    - Clean: missing public docstring (-5.0 pts)
samples/python/bad/red_black_tree.py:698 main          12   1    0   0   0   96.4   A
    - SRP: high external call fan-out=10 (>6) (-12.0 pts)
samples/python/bad/red_black_tree.py:350 RedBlackTre   12   6   10   1   2   96.6   A
    - Complexity: CC=6 (>5) (-4.0 pts)
    - Complexity: cognitive=10 (>8) (-5.0 pts)
    - Complexity: returns=5 (>3) (-8.0 pts)
samples/python/bad/red_black_tree.py:87 RedBlackTree   18   7   11   1   2   96.9   A
    - Complexity: CC=7 (>5) (-8.0 pts)
    - Complexity: cognitive=11 (>8) (-7.5 pts)
samples/python/bad/red_black_tree.py:321 RedBlackTre   10   7    5   0   1   97.6   A
    - Complexity: CC=7 (>5) (-8.0 pts)
    - Complexity: returns=4 (>3) (-4.0 pts)
samples/python/bad/red_black_tree.py:487 RedBlackTre   13   7    6   0   1   98.4   A
    - Complexity: CC=7 (>5) (-8.0 pts)
samples/python/bad/red_black_tree.py:20 RedBlackTree   13   1    0   5   0   98.5   A
    - Size: params=5 (>4) (-6.0 pts)
samples/python/bad/red_black_tree.py:526 test_rotati   28   2    1   0   1   98.9   A
    - Size: LOC=28 (>25) (-4.5 pts)
samples/python/bad/red_black_tree.py:278 RedBlackTre   11   4    3   0   1   99.2   A
    - Complexity: returns=4 (>3) (-4.0 pts)
samples/python/bad/red_black_tree.py:311 RedBlackTre    6   6    5   0   1   99.2   A
    - Complexity: CC=6 (>5) (-4.0 pts)
samples/python/bad/red_black_tree.py:466 RedBlackTre    6   3    2   0   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/python/bad/red_black_tree.py:473 RedBlackTre    6   3    2   0   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/python/bad/red_black_tree.py:480 RedBlackTre    6   3    2   0   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/python/bad/red_black_tree.py:684 print_resul    2   2    1   2   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/python/bad/red_black_tree.py:43 RedBlackTree   17   5    6   0   2  100.0   A
samples/python/bad/red_black_tree.py:65 RedBlackTree   17   5    6   0   2  100.0   A
samples/python/bad/red_black_tree.py:343 RedBlackTre    2   1    0   1   0  100.0   A
samples/python/bad/red_black_tree.py:402 RedBlackTre    5   2    2   0   1  100.0   A
samples/python/bad/red_black_tree.py:412 RedBlackTre    5   2    2   0   1  100.0   A
samples/python/bad/red_black_tree.py:423 RedBlackTre    5   2    2   0   1  100.0   A
samples/python/bad/red_black_tree.py:431 RedBlackTre    7   3    4   0   1  100.0   A
samples/python/bad/red_black_tree.py:440 RedBlackTre    4   2    1   0   1  100.0   A
samples/python/bad/red_black_tree.py:446 RedBlackTre    4   2    1   0   1  100.0   A
samples/python/bad/red_black_tree.py:452 RedBlackTre    2   1    0   0   0  100.0   A
samples/python/bad/red_black_tree.py:455 RedBlackTre    7   3    2   0   1  100.0   A
samples/python/bad/red_black_tree.py:502 RedBlackTre    7   4    4   1   1  100.0   A
samples/python/bad/red_black_tree.py:512 color          5   2    2   1   1  100.0   A
samples/python/bad/red_black_tree.py:560 test_insert    5   2    1   0   1  100.0   A
samples/python/bad/red_black_tree.py:570 test_insert   16   1    0   0   0  100.0   A
samples/python/bad/red_black_tree.py:591 test_insert   11   2    1   0   1  100.0   A
samples/python/bad/red_black_tree.py:607 test_insert   17   2    1   0   1  100.0   A
samples/python/bad/red_black_tree.py:629 test_floor_   13   4    4   0   2  100.0   A
samples/python/bad/red_black_tree.py:645 test_min_ma    9   2    1   0   0  100.0   A
samples/python/bad/red_black_tree.py:657 test_tree_t   13   3    2   0   1  100.0   A
samples/python/bad/red_black_tree.py:673 test_tree_c    8   3    2   0   1  100.0   A
```

### PYTHON (`--framework auto`) — 3. Serialization & I/O Security Hygiene (PyCQA/bandit examples/, 19 LOC)

#### Good Baseline: [`python/good/urlopen.py`](python/good/urlopen.py) ([sidecar JSON](python/good/urlopen.py.expected.json))

- **Upstream Dataset / Benchmark:** [PyCQA/bandit (examples/urlopen.py)](https://github.com/PyCQA/bandit/blob/main/examples/urlopen.py) (`Apache-2.0`)
- **Expected Scorecard:** `Composite 97.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 80.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 97.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 80.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/urlopen.py                 src      19    - 100.0 100.0 100.0  80.0 100.0   97.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/urlopen.py:15 test_urlopen         17   1    0   0   0   97.0   A
    - Clean: missing return type annotation (-10.0 pts)
    - Clean: missing public docstring (-10.0 pts)
```

#### Bad Baseline: [`python/bad/yaml_load.py`](python/bad/yaml_load.py) ([sidecar JSON](python/bad/yaml_load.py.expected.json))

- **Upstream Dataset / Benchmark:** [PyCQA/bandit (examples/yaml_load.py)](https://github.com/PyCQA/bandit/blob/main/examples/yaml_load.py) (`Apache-2.0`)
- **Expected Scorecard:** `Composite 65.0/100 (Grade D)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 75.0` | `Security: 60.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 65.0/100 (Grade D) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 2
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 75.0 | Security: 60.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/yaml_load.py                src      19    - 100.0 100.0 100.0  75.0  60.0   65.0   D
    - Clean: missing module docstring (-10.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/yaml_load.py:7 test_yaml_load        8   2    1   0   1   65.0   D
    - Clean: missing return type annotation (-10.0 pts)
    - Clean: missing public docstring (-5.0 pts)
    - Security: unsafe yaml.load() without SafeLoader at L9 (-40.0 pts)
samples/python/bad/yaml_load.py:18 test_json_load       2   1    0   0   0   97.8   A
    - Clean: missing return type annotation (-10.0 pts)
    - Clean: missing public docstring (-5.0 pts)
```

### PYTHON (`--framework auto`) — 4. CLI Command & Option Test Suite Hygiene (pallets/click tests/)

#### Good Baseline: [`python/good/test_info_dict.py`](python/good/test_info_dict.py) ([sidecar JSON](python/good/test_info_dict.py.expected.json))

- **Upstream Dataset / Benchmark:** [pallets/click (tests/test_info_dict.py)](https://github.com/pallets/click/blob/main/tests/test_info_dict.py) (`BSD-3-Clause`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 0, test: 1) | Classes: 0 | Functions/Methods: 8
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/test_info_dict.py          test    322    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/test_info_dict.py:212 test_param    3   1    0   2   0  100.0   A
samples/python/good/test_info_dict.py:253 test_comma    4   1    0   2   0  100.0   A
samples/python/good/test_info_dict.py:259 test_conte   11   1    0   0   0  100.0   A
samples/python/good/test_info_dict.py:272 test_param    4   1    0   0   0  100.0   A
samples/python/good/test_info_dict.py:300 test_param    2   1    0   3   0  100.0   A
samples/python/good/test_info_dict.py:321 test_param    3   1    0   4   0  100.0   A
samples/python/good/test_info_dict.py:327 test_argum    5   1    0   0   0  100.0   A
samples/python/good/test_info_dict.py:334 test_comma   11   2    0   0   0  100.0   A
```

#### Bad Baseline: [`python/bad/test_commands.py`](python/bad/test_commands.py) ([sidecar JSON](python/bad/test_commands.py.expected.json))

- **Upstream Dataset / Benchmark:** [pallets/click (tests/test_commands.py)](https://github.com/pallets/click/blob/main/tests/test_commands.py) (`BSD-3-Clause`)
- **Expected Scorecard:** `Composite 73.9/100 (Grade C)` — `SRP: 100.0` | `Size: 68.9` | `Complexity: 100.0` | `Clean: 92.8` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 73.9/100 (Grade C) | Files: 1 (src: 0, test: 1) | Classes: 0 | Functions/Methods: 28
Dimensions -> SRP: 100.0 | Size: 68.9 | Complexity: 100.0 | Clean: 92.8 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/test_commands.py            test    544    - 100.0  68.9 100.0  92.8 100.0   73.9   C
    - Size: file LOC=544 (>350) (-29.1 pts)
    - Clean: 1 mid-file/late import(s) (-4.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/test_commands.py:469 test_help_pa   43   2    1   1   1   75.0   C
    - Size: LOC=43 (>40) (-3.0 pts)
    - Clean (Test): 24 assertions in single test (>8) (-30.0 pts)
samples/python/bad/test_commands.py:144 test_custom_   53   1    0   1   0   96.8   A
    - Size: LOC=53 (>40) (-13.0 pts)
samples/python/bad/test_commands.py:8 test_other_com   12   1    0   1   0  100.0   A
samples/python/bad/test_commands.py:24 test_other_co   15   1    0   1   0  100.0   A
samples/python/bad/test_commands.py:44 test_forwarde   17   1    0   1   0  100.0   A
samples/python/bad/test_commands.py:66 test_auto_sho   26   1    0   1   0  100.0   A
samples/python/bad/test_commands.py:98 test_command_    4   1    0   1   0  100.0   A
samples/python/bad/test_commands.py:104 test_default   11   1    0   1   0  100.0   A
samples/python/bad/test_commands.py:129 test_group_w   11   1    0   4   0  100.0   A
samples/python/bad/test_commands.py:210 test_object_   16   2    1   1   1  100.0   A
samples/python/bad/test_commands.py:262 test_other_c   12   1    0   3   0  100.0   A
samples/python/bad/test_commands.py:279 test_invoked   18   1    0   1   0  100.0   A
samples/python/bad/test_commands.py:311 test_subcomm   12   1    0   4   0  100.0   A
samples/python/bad/test_commands.py:329 test_aliased   14   1    0   1   0  100.0   A
samples/python/bad/test_commands.py:349 test_group_a    6   1    0   1   0  100.0   A
samples/python/bad/test_commands.py:401 test_iter_pa   17   1    0   3   0  100.0   A
samples/python/bad/test_commands.py:462 test_get_hel    4   1    0   3   0  100.0   A
samples/python/bad/test_commands.py:536 test_unproce   13   1    0   1   0  100.0   A
samples/python/bad/test_commands.py:554 test_depreca    8   2    1   3   1  100.0   A
samples/python/bad/test_commands.py:568 test_depreca    7   1    0   3   0  100.0   A
samples/python/bad/test_commands.py:582 test_depreca   10   1    0   2   0  100.0   A
samples/python/bad/test_commands.py:603 test_depreca    8   2    1   2   1  100.0   A
samples/python/bad/test_commands.py:615 test_command    9   1    0   0   0  100.0   A
samples/python/bad/test_commands.py:628 test_group_p   16   1    0   0   0  100.0   A
samples/python/bad/test_commands.py:650 test_group_i   18   1    0   1   0  100.0   A
samples/python/bad/test_commands.py:675 test_abort_e    8   1    0   2   0  100.0   A
samples/python/bad/test_commands.py:686 test_unknown    4   1    0   1   0  100.0   A
samples/python/bad/test_commands.py:699 test_suggest   13   1    0   3   0  100.0   A
```

### JAVA (`--framework none`) — 1. Competitive Programming Contest Class Structure (Same Problem: Codeforces 1575D)

#### Good Baseline: [`java/good/DivisibleByTwentyFiveClean.java`](java/good/DivisibleByTwentyFiveClean.java) ([sidecar JSON](java/good/DivisibleByTwentyFiveClean.java.expected.json))

- **Upstream Dataset / Benchmark:** [DeepMind code_contests (test split, Problem 1575_D. Divisible by Twenty-Five, Solution #57)](https://huggingface.co/datasets/deepmind/code_contests) (`CC-BY-4.0`)
- **Expected Scorecard:** `Composite 96.2/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 75.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 96.2/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 75.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/DivisibleByTwentyFiveClean.java src     132    - 100.0 100.0 100.0  75.0 100.0   96.2   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/DivisibleByTwentyFiveClean.java:   132    1     1    2   96.2   A
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/DivisibleByTwentyFiveClean.java:9    11   2    1   1   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
```

#### Bad Baseline: [`java/bad/DivisibleByTwentyFiveGodClass.java`](java/bad/DivisibleByTwentyFiveGodClass.java) ([sidecar JSON](java/bad/DivisibleByTwentyFiveGodClass.java.expected.json))

- **Upstream Dataset / Benchmark:** [DeepMind code_contests (test split, Problem 1575_D. Divisible by Twenty-Five, Solution #45)](https://huggingface.co/datasets/deepmind/code_contests) (`CC-BY-4.0`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 0.0` | `Size: 0.0` | `Complexity: 0.0` | `Clean: 94.1` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 69
Dimensions -> SRP: 0.0 | Size: 0.0 | Complexity: 0.0 | Clean: 94.1 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/DivisibleByTwentyFiveGodClass.java src     611    -   0.0   0.0   0.0  94.1 100.0    5.0   F
    - Size: file LOC=611 (>350) (-40.2 pts)

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/DivisibleByTwentyFiveGodClass.jav   611   69    14  162    5.0   F
    - SRP: LCOM4=14 disconnected method groups (-100.0 pts)
    - SRP: methods=69 (>10) (-100.0 pts)
    - SRP: self attributes=8 (>7) (-4.0 pts)
    - Size: class LOC=611 (>200) (-100.0 pts)
    - Complexity: total class CC=162 (>25) (-100.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/DivisibleByTwentyFiveGodClass.java:   37  11   10   4   1   69.0   D
    - Size: LOC=37 (>25) (-18.0 pts)
    - Complexity: CC=11 (>5) (-27.0 pts)
    - Complexity: cognitive=10 (>8) (-5.0 pts)
    - Complexity: returns=4 (>3) (-4.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:   14   6    5   1   1   96.1   A
    - Complexity: CC=6 (>5) (-4.0 pts)
    - Complexity: returns=5 (>3) (-8.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:   14   6    5   1   1   96.1   A
    - Complexity: CC=6 (>5) (-4.0 pts)
    - Complexity: returns=5 (>3) (-8.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:   26   6    5   1   1   97.3   A
    - Size: LOC=26 (>25) (-1.5 pts)
    - Complexity: CC=6 (>5) (-4.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:   17   3    2   4   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:   17   3    2   4   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:   16   5    4   3   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:   15   5    4   2   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:   11   2    1   1   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:   11   2    1   1   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:   12   3    2   1   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:   12   3    2   1   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:   12   3    2   1   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    5   2    1   2   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    4   2    1   2   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    6   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    4   2    1   2   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    6   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    8   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    7   3    2   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    7   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    7   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    7   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    7   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    7   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    7   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    7   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    9   3    2   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    9   3    2   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    6   2    1   2   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    9   3    2   2   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:   10   3    2   2   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    7   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    7   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    7   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    7   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    7   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    7   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    7   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    7   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    4   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    7   3    2   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    9   4    3   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    4   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    7   3    2   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    9   4    3   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    3   1    0   2   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    3   1    0   3   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    3   1    0   4   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    3   1    0   2   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    3   1    0   3   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    3   1    0   4   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    3   1    0   2   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    3   1    0   3   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    3   1    0   4   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    3   1    0   2   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    3   1    0   3   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    3   1    0   4   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    6   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    6   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    5   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    3   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    3   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    3   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    6   2    1   2   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DivisibleByTwentyFiveGodClass.java:    6   2    1   2   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

### JAVA (`--framework none`) — 2. Method Complexity & Control Flow (Same Problem: Codeforces 1575D)

#### Good Baseline: [`java/good/DivisibleByTwentyFiveModular.java`](java/good/DivisibleByTwentyFiveModular.java) ([sidecar JSON](java/good/DivisibleByTwentyFiveModular.java.expected.json))

- **Upstream Dataset / Benchmark:** [DeepMind code_contests (test split, Problem 1575_D. Divisible by Twenty-Five, Solution #46)](https://huggingface.co/datasets/deepmind/code_contests) (`CC-BY-4.0`)
- **Expected Scorecard:** `Composite 94.3/100 (Grade A)` — `SRP: 100.0` | `Size: 96.5` | `Complexity: 93.3` | `Clean: 76.7` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 94.3/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 3
Dimensions -> SRP: 100.0 | Size: 96.5 | Complexity: 93.3 | Clean: 76.7 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/DivisibleByTwentyFiveModular.java src      79    - 100.0  96.5  93.3  76.7 100.0   94.3   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/DivisibleByTwentyFiveModular.jav    79    3     1   14   94.3   A
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/DivisibleByTwentyFiveModular.java:   28   9    8   5   1   91.9   A
    - Size: LOC=28 (>25) (-4.5 pts)
    - Size: params=5 (>4) (-6.0 pts)
    - Complexity: CC=9 (>5) (-16.0 pts)
    - Complexity: returns=4 (>3) (-4.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java/good/DivisibleByTwentyFiveModular.java:   16   4    3   2   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java/good/DivisibleByTwentyFiveModular.java:    8   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

#### Bad Baseline: [`java/bad/DivisibleByTwentyFiveBranchy.java`](java/bad/DivisibleByTwentyFiveBranchy.java) ([sidecar JSON](java/bad/DivisibleByTwentyFiveBranchy.java.expected.json))

- **Upstream Dataset / Benchmark:** [DeepMind code_contests (test split, Problem 1575_D. Divisible by Twenty-Five, Solution #32)](https://huggingface.co/datasets/deepmind/code_contests) (`CC-BY-4.0`)
- **Expected Scorecard:** `Composite 44.5/100 (Grade F)` — `SRP: 100.0` | `Size: 79.0` | `Complexity: 39.5` | `Clean: 75.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 44.5/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 79.0 | Complexity: 39.5 | Clean: 75.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/DivisibleByTwentyFiveBranchy.java src      42    - 100.0  79.0  39.5  75.0 100.0   44.5   F

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/DivisibleByTwentyFiveBranchy.java    42    1     1   14   44.5   F
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/DivisibleByTwentyFiveBranchy.java:6   39  14   13   1   1   44.5   F
    - Size: LOC=39 (>25) (-21.0 pts)
    - Complexity: CC=14 (>5) (-48.0 pts)
    - Complexity: cognitive=13 (>8) (-12.5 pts)
    - Clean: missing public docstring (-10.0 pts)
```

### JAVA (`--framework none`) — 3. Linked List Data Structure Cohesion & Method Count (TheAlgorithms/Java lists/, ~250 LOC)

#### Good Baseline: [`java/good/DoublyLinkedList.java`](java/good/DoublyLinkedList.java) ([sidecar JSON](java/good/DoublyLinkedList.java.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Java (src/main/java/com/thealgorithms/datastructures/lists/DoublyLinkedList.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/datastructures/lists/DoublyLinkedList.java) (`MIT`)
- **Expected Scorecard:** `Composite 97.3/100 (Grade A)` — `SRP: 96.6` | `Size: 99.2` | `Complexity: 93.1` | `Clean: 99.4` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 97.3/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 3 | Functions/Methods: 19
Dimensions -> SRP: 96.6 | Size: 99.2 | Complexity: 93.1 | Clean: 99.4 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/DoublyLinkedList.java        src     234    -  96.6  99.2  93.1  99.4 100.0   97.3   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/DoublyLinkedList.java:172 LinkOp   154   11     1   32   96.6   A
    - SRP: methods=11 (>10) (-4.0 pts)
    - Complexity: total class CC=32 (>25) (-10.5 pts)
samples/java/good/DoublyLinkedList.java:93 Link       44    3     1    3   97.8   A
samples/java/good/DoublyLinkedList.java:16 DoublyL    36    5     1    7  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/DoublyLinkedList.java:129 Link.mai   33   1    0   1   0   93.4   A
    - SRP: high external call fan-out=10 (>6) (-12.0 pts)
    - Size: LOC=33 (>25) (-12.0 pts)
samples/java/good/DoublyLinkedList.java:362 LinkOper   13   4    3   1   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java/good/DoublyLinkedList.java:34 DoublyLin    4   1    0   0   0  100.0   A
samples/java/good/DoublyLinkedList.java:45 DoublyLin    8   1    0   1   0  100.0   A
samples/java/good/DoublyLinkedList.java:59 DoublyLin    3   1    0   0   0  100.0   A
samples/java/good/DoublyLinkedList.java:66 DoublyLin    8   2    1   0   1  100.0   A
samples/java/good/DoublyLinkedList.java:78 DoublyLin    8   2    1   0   1  100.0   A
samples/java/good/DoublyLinkedList.java:113 Link.Lin    3   1    0   1   0  100.0   A
samples/java/good/DoublyLinkedList.java:120 Link.dis    3   1    0   0   0  100.0   A
samples/java/good/DoublyLinkedList.java:193 LinkOper   11   2    1   2   1  100.0   A
samples/java/good/DoublyLinkedList.java:210 LinkOper   13   2    1   2   1  100.0   A
samples/java/good/DoublyLinkedList.java:230 LinkOper   23   5    4   3   1  100.0   A
samples/java/good/DoublyLinkedList.java:260 LinkOper   11   2    1   0   1  100.0   A
samples/java/good/DoublyLinkedList.java:279 LinkOper   11   2    1   0   1  100.0   A
samples/java/good/DoublyLinkedList.java:298 LinkOper   19   5    4   1   1  100.0   A
samples/java/good/DoublyLinkedList.java:325 LinkOper   18   4    3   2   1  100.0   A
samples/java/good/DoublyLinkedList.java:350 LinkOper   11   3    2   1   1  100.0   A
samples/java/good/DoublyLinkedList.java:379 LinkOper   14   2    1   0   1  100.0   A
samples/java/good/DoublyLinkedList.java:405 LinkOper    5   1    0   0   0  100.0   A
```

#### Bad Baseline: [`java/bad/SinglyLinkedList.java`](java/bad/SinglyLinkedList.java) ([sidecar JSON](java/bad/SinglyLinkedList.java.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Java (src/main/java/com/thealgorithms/datastructures/lists/SinglyLinkedList.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/datastructures/lists/SinglyLinkedList.java) (`MIT`)
- **Expected Scorecard:** `Composite 20.7/100 (Grade F)` — `SRP: 15.7` | `Size: 66.7` | `Complexity: 50.2` | `Clean: 98.9` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 20.7/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 27
Dimensions -> SRP: 15.7 | Size: 66.7 | Complexity: 50.2 | Clean: 98.9 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/SinglyLinkedList.java         src     281    -  15.7  66.7  50.2  98.9 100.0   20.7   F

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/SinglyLinkedList.java:10 SinglyLi   281   27     2   58   20.7   F
    - SRP: LCOM4=2 disconnected method groups (-15.0 pts)
    - SRP: methods=27 (>10) (-68.0 pts)
    - Size: class LOC=281 (>200) (-32.4 pts)
    - Complexity: total class CC=58 (>25) (-49.5 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/SinglyLinkedList.java:402 SinglyLin   34   2    1   1   0   69.0   D
    - SRP: high external call fan-out=19 (>6) (-36.0 pts)
    - Size: LOC=34 (>25) (-13.5 pts)
samples/java/bad/SinglyLinkedList.java:81 SinglyLink   33   7    6   2   1   95.4   A
    - Size: LOC=33 (>25) (-12.0 pts)
    - Complexity: CC=7 (>5) (-8.0 pts)
samples/java/bad/SinglyLinkedList.java:251 SinglyLin   15   4    3   0   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/SinglyLinkedList.java:275 SinglyLin   11   3    2   0   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/SinglyLinkedList.java:242 SinglyLin    8   2    1   0   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/SinglyLinkedList.java:449 SinglyLin    4   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/SinglyLinkedList.java:25 SinglyLink    4   1    0   0   0  100.0   A
samples/java/bad/SinglyLinkedList.java:36 SinglyLink    4   1    0   2   0  100.0   A
samples/java/bad/SinglyLinkedList.java:46 SinglyLink   12   3    2   0   1  100.0   A
samples/java/bad/SinglyLinkedList.java:64 SinglyLink   12   3    2   0   1  100.0   A
samples/java/bad/SinglyLinkedList.java:129 SinglyLin   15   3    2   1   1  100.0   A
samples/java/bad/SinglyLinkedList.java:152 SinglyLin   10   2    1   1   1  100.0   A
samples/java/bad/SinglyLinkedList.java:169 SinglyLin    8   2    1   0   1  100.0   A
samples/java/bad/SinglyLinkedList.java:183 SinglyLin    3   1    0   0   0  100.0   A
samples/java/bad/SinglyLinkedList.java:192 SinglyLin    3   1    0   0   0  100.0   A
samples/java/bad/SinglyLinkedList.java:201 SinglyLin    3   1    0   0   0  100.0   A
samples/java/bad/SinglyLinkedList.java:209 SinglyLin    3   1    0   1   0  100.0   A
samples/java/bad/SinglyLinkedList.java:218 SinglyLin    7   2    1   0   1  100.0   A
samples/java/bad/SinglyLinkedList.java:233 SinglyLin    8   3    2   1   1  100.0   A
samples/java/bad/SinglyLinkedList.java:292 SinglyLin    3   1    0   1   0  100.0   A
samples/java/bad/SinglyLinkedList.java:301 SinglyLin    3   1    0   1   0  100.0   A
samples/java/bad/SinglyLinkedList.java:311 SinglyLin   22   4    3   2   1  100.0   A
samples/java/bad/SinglyLinkedList.java:340 SinglyLin    3   1    0   0   0  100.0   A
samples/java/bad/SinglyLinkedList.java:347 SinglyLin    3   1    0   0   0  100.0   A
samples/java/bad/SinglyLinkedList.java:354 SinglyLin   14   3    2   1   1  100.0   A
samples/java/bad/SinglyLinkedList.java:377 SinglyLin    8   2    1   1   1  100.0   A
samples/java/bad/SinglyLinkedList.java:393 SinglyLin    5   2    1   3   1  100.0   A
```

### JAVA (`--framework spring-boot`) — 1. Multi-Endpoint PetClinic REST Controller Layering (spring-petclinic-microservices, ~44 LOC)

#### Good Baseline: [`java-spring/good/ApiGatewayController.java`](java-spring/good/ApiGatewayController.java) ([sidecar JSON](java-spring/good/ApiGatewayController.java.expected.json))

- **Upstream Dataset / Benchmark:** [spring-petclinic/spring-petclinic-microservices (boundary/web/ApiGatewayController.java)](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/spring-petclinic-api-gateway/src/main/java/org/springframework/samples/petclinic/api/boundary/web/ApiGatewayController.java) (`Apache-2.0`)
- **Expected Scorecard:** `Composite 97.1/100 (Grade A)` — `SRP: 94.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 92.5` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 97.1/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 4
Dimensions -> SRP: 94.0 | Size: 100.0 | Complexity: 100.0 | Clean: 92.5 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/ApiGatewayController.java src      40    -  94.0 100.0 100.0  92.5 100.0   97.1   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/ApiGatewayController.java    40    4     1    4   97.1   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/ApiGatewayController.java:5   12   1    0   1   0   94.9   A
    - SRP: high external call fan-out=10 (>6) (-12.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/good/ApiGatewayController.java:6   11   1    0   1   0   94.9   A
    - SRP: high external call fan-out=10 (>6) (-12.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/good/ApiGatewayController.java:4    7   1    0   3   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/good/ApiGatewayController.java:8    3   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

#### Bad Baseline: [`java-spring/bad/PetResource.java`](java-spring/bad/PetResource.java) ([sidecar JSON](java-spring/bad/PetResource.java.expected.json))

- **Upstream Dataset / Benchmark:** [spring-petclinic/spring-petclinic-microservices (customers/web/PetResource.java)](https://github.com/spring-petclinic/spring-petclinic-microservices/blob/master/spring-petclinic-customers-service/src/main/java/org/springframework/samples/petclinic/customers/web/PetResource.java) (`Apache-2.0`)
- **Expected Scorecard:** `Composite 63.7/100 (Grade D)` — `SRP: 58.7` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 94.3` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 63.7/100 (Grade D) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 7
Dimensions -> SRP: 58.7 | Size: 100.0 | Complexity: 100.0 | Clean: 94.3 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/PetResource.java       src      48    -  58.7 100.0 100.0  94.3 100.0   63.7   D

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/PetResource.java:36 PetRes    48    7     1    7   63.7   D
    - SRP (Spring): @RestController directly injects petRepository (-20.0 pts)
    - SRP (Spring): @RestController directly injects ownerRepository (-20.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/PetResource.java:77 PetResou    8   1    0   2   0   96.5   A
    - SRP: high external call fan-out=9 (>6) (-9.0 pts)
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/bad/PetResource.java:55 PetResou   11   1    0   2   0   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/bad/PetResource.java:45 PetResou    4   1    0   2   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/bad/PetResource.java:50 PetResou    4   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/bad/PetResource.java:69 PetResou    6   1    0   2   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/bad/PetResource.java:89 PetResou    4   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/bad/PetResource.java:96 PetResou    4   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

### JAVA (`--framework spring-boot`) — 2. JDBC SQL Query Endpoint: Parameterized vs String Concatenation (OWASP WebGoat sqlinjection/)

#### Good Baseline: [`java-spring/good/Servers.java`](java-spring/good/Servers.java) ([sidecar JSON](java-spring/good/Servers.java.expected.json))

- **Upstream Dataset / Benchmark:** [OWASP WebGoat (sqlinjection/mitigation/Servers.java)](https://github.com/WebGoat/WebGoat/blob/main/src/main/java/org/owasp/webgoat/lessons/sqlinjection/mitigation/Servers.java) (`GPL-2.0`)
- **Expected Scorecard:** `Composite 96.2/100 (Grade A)` — `SRP: 100.0` | `Size: 98.5` | `Complexity: 100.0` | `Clean: 77.5` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 96.2/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 2
Dimensions -> SRP: 100.0 | Size: 98.5 | Complexity: 100.0 | Clean: 77.5 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/Servers.java          src      46    - 100.0  98.5 100.0  77.5 100.0   96.2   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/Servers.java:20 Servers      46    2     1    3   96.2   A
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/Servers.java:43 Servers.sor   27   2    1   1   1   97.8   A
    - Size: LOC=27 (>25) (-3.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/good/Servers.java:39 Servers.Ser    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

#### Bad Baseline: [`java-spring/bad/SqlInjectionLesson8.java`](java-spring/bad/SqlInjectionLesson8.java) ([sidecar JSON](java-spring/bad/SqlInjectionLesson8.java.expected.json))

- **Upstream Dataset / Benchmark:** [OWASP WebGoat (sqlinjection/introduction/SqlInjectionLesson8.java)](https://github.com/WebGoat/WebGoat/blob/main/src/main/java/org/owasp/webgoat/lessons/sqlinjection/introduction/SqlInjectionLesson8.java) (`GPL-2.0`)
- **Expected Scorecard:** `Composite 65.0/100 (Grade D)` — `SRP: 90.4` | `Size: 94.0` | `Complexity: 97.6` | `Clean: 77.0` | `Security: 60.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 65.0/100 (Grade D) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 5
Dimensions -> SRP: 90.4 | Size: 94.0 | Complexity: 97.6 | Clean: 77.0 | Security: 60.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/SqlInjectionLesson8.java src     104    -  90.4  94.0  97.6  77.0  60.0   65.0   D

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/SqlInjectionLesson8.java:2   104    5     1   14   65.0   D
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/SqlInjectionLesson8.java:47    44   5    4   2   1   65.0   D
    - SRP: high external call fan-out=25 (>6) (-36.0 pts)
    - Size: LOC=44 (>25) (-28.5 pts)
    - Complexity: returns=6 (>3) (-12.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Security (Spring): potential SQL/JPQL injection in statement.executeQuery via string concatenation (-40.0 pts)
samples/java-spring/bad/SqlInjectionLesson8.java:131   14   2    1   2   0   65.0   D
    - SRP: high external call fan-out=8 (>6) (-6.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Security (Spring): potential SQL/JPQL injection in statement.executeUpdate via string concatenation (-40.0 pts)
samples/java-spring/bad/SqlInjectionLesson8.java:100   26   5    4   1   1   96.3   A
    - SRP: high external call fan-out=8 (>6) (-6.0 pts)
    - Size: LOC=26 (>25) (-1.5 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java-spring/bad/SqlInjectionLesson8.java:37     3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java-spring/bad/SqlInjectionLesson8.java:41     5   1    0   2   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

### JAVA (`--framework spring-boot`) — 3. Spring Boot @WebMvcTest Controller Test Suite Hygiene (spring-petclinic owner/, ~208 LOC)

#### Good Baseline: [`java-spring/good/PetControllerTests.java`](java-spring/good/PetControllerTests.java) ([sidecar JSON](java-spring/good/PetControllerTests.java.expected.json))

- **Upstream Dataset / Benchmark:** [spring-projects/spring-petclinic (owner/PetControllerTests.java)](https://github.com/spring-projects/spring-petclinic/blob/main/src/test/java/org/springframework/samples/petclinic/owner/PetControllerTests.java) (`Apache-2.0`)
- **Expected Scorecard:** `Composite 98.8/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 92.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 98.8/100 (Grade A) | Files: 1 (src: 0, test: 1) | Classes: 1 | Functions/Methods: 5
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 92.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/PetControllerTests.java test    193    - 100.0 100.0 100.0  92.0 100.0   98.8   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/PetControllerTests.java:5   193    5     1    5   98.8   A
    - Clean (Spring): @Autowired field injection detected on 'mockMvc' (-8.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/good/PetControllerTests.java:70    17   1    0   0   0  100.0   A
samples/java-spring/good/PetControllerTests.java:89     7   1    0   0   0  100.0   A
samples/java-spring/good/PetControllerTests.java:97     9   1    0   0   0  100.0   A
samples/java-spring/good/PetControllerTests.java:191    9   1    0   0   0  100.0   A
samples/java-spring/good/PetControllerTests.java:201    8   1    0   0   0  100.0   A
```

#### Bad Baseline: [`java-spring/bad/OwnerControllerTests.java`](java-spring/bad/OwnerControllerTests.java) ([sidecar JSON](java-spring/bad/OwnerControllerTests.java.expected.json))

- **Upstream Dataset / Benchmark:** [spring-projects/spring-petclinic (owner/OwnerControllerTests.java)](https://github.com/spring-projects/spring-petclinic/blob/main/src/test/java/org/springframework/samples/petclinic/owner/OwnerControllerTests.java) (`Apache-2.0`)
- **Expected Scorecard:** `Composite 65.0/100 (Grade D)` — `SRP: 60.0` | `Size: 90.4` | `Complexity: 100.0` | `Clean: 91.8` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 65.0/100 (Grade D) | Files: 1 (src: 0, test: 1) | Classes: 1 | Functions/Methods: 20
Dimensions -> SRP: 60.0 | Size: 90.4 | Complexity: 100.0 | Clean: 91.8 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/OwnerControllerTests.java test    224    -  60.0  90.4 100.0  91.8 100.0   65.0   D

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/OwnerControllerTests.java:   224   20     1   22   65.0   D
    - SRP: methods=20 (>10) (-40.0 pts)
    - Size: class LOC=224 (>200) (-9.6 pts)
    - Clean (Spring): @Autowired field injection detected on 'mockMvc' (-8.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java-spring/bad/OwnerControllerTests.java:28   14   1    0   0   0   99.5   A
    - Clean (Test): 9 assertions in single test (>8) (-3.0 pts)
samples/java-spring/bad/OwnerControllerTests.java:73   18   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:92   10   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:10    7   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:11   10   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:12   10   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:13   14   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:15   14   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:16    7   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:17    6   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:18    8   2    1   0   1  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:19    8   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:19   11   2    1   0   1  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:21    9   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:22   10   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:23   12   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:25   11   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:26    6   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:26   13   1    0   0   0  100.0   A
samples/java-spring/bad/OwnerControllerTests.java:29   16   1    0   0   0  100.0   A
```

---

### JAVASCRIPT (`--lang javascript`) — 1. Modern ECMAScript Arithmetic Service vs. Legacy Smelly Script

#### Good Baseline: [`javascript/clean_math_service.js`](javascript/clean_math_service.js) ([sidecar JSON](javascript/clean_math_service.js.expected.json))

- **Upstream Dataset / Benchmark:** [Custom JavaScript Benchmark](https://developer.mozilla.org/en-US/docs/Web/JavaScript) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 5
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/clean_math_service.js       src      21    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/clean_math_service.js:4 MathSer    20    5     1    6  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/clean_math_service.js:5 MathServi    3   1    0   1   0  100.0   A
samples/javascript/clean_math_service.js:14 MathServ    3   1    0   2   0  100.0   A
samples/javascript/clean_math_service.js:23 MathServ    3   1    0   2   0  100.0   A
samples/javascript/clean_math_service.js:32 MathServ    3   1    0   2   0  100.0   A
samples/javascript/clean_math_service.js:41 MathServ    6   2    1   2   1  100.0   A
```

#### Bad Baseline: [`javascript/smelly_legacy_script.js`](javascript/smelly_legacy_script.js) ([sidecar JSON](javascript/smelly_legacy_script.js.expected.json))

- **Upstream Dataset / Benchmark:** [Custom JavaScript Benchmark](https://developer.mozilla.org/en-US/docs/Web/JavaScript) (`MIT`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 53.0` | `Security: 0.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 53.0 | Security: 0.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/smelly_legacy_script.js     src      19    - 100.0 100.0 100.0  53.0   0.0    5.0   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/smelly_legacy_script.js:3 process   18   4    5   2   3    5.0   F
    - Clean: missing public docstring (-10.0 pts)
    - Clean: 3 legacy 'var' declaration(s) detected (prefer 'const' or 'let') (-9.0 pts)
    - Clean: 2 loose equality comparison(s) (==/!=) trigger implicit type coercion (prefer ===/!==) (-4.0 pts)
    - Clean: empty catch block swallows exception (-10.0 pts)
    - Clean: debugger statement detected (-10.0 pts)
    - Clean: 2 unannotated parameter(s) without default values (input, role) (-4.0 pts)
    - Security: dynamic code execution via eval (-40.0 pts)
    - Security: dynamic code execution via new Function (-40.0 pts)
    - Security: string argument to setTimeout causes implicit code evaluation (-20.0 pts)
    - Security: 'with' statement obscures lexical scope and risks prototype pollution (-30.0 pts)
```
---

### JAVASCRIPT (`--lang javascript`) — 2. Graph Dijkstra Shortest Path Algorithm Complexity & Control Flow

#### Good Baseline: [`javascript/dijkstra_clean.js`](javascript/dijkstra_clean.js) ([sidecar JSON](javascript/dijkstra_clean.js.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/JavaScript (Graphs/Dijkstra.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Graphs/Dijkstra.js) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 4
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/dijkstra_clean.js           src      41    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/dijkstra_clean.js:8 initDistances    8   2    1   2   1  100.0   A
samples/javascript/dijkstra_clean.js:24 minDistanceN   12   4    3   2   2  100.0   A
samples/javascript/dijkstra_clean.js:45 relaxNeighbo    8   3    3   3   2  100.0   A
samples/javascript/dijkstra_clean.js:61 dijkstra       12   2    1   2   1  100.0   A
```

#### Bad Baseline: [`javascript/dijkstra_branchy.js`](javascript/dijkstra_branchy.js) ([sidecar JSON](javascript/dijkstra_branchy.js.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/JavaScript (Graphs/Dijkstra.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Graphs/Dijkstra.js) (`MIT`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 100.0` | `Size: 0.0` | `Complexity: 0.0` | `Clean: 55.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 0.0 | Complexity: 0.0 | Clean: 55.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/dijkstra_branchy.js         src      79    - 100.0   0.0   0.0  55.0 100.0    5.0   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/dijkstra_branchy.js:1 dijkstra      78  29   73   7   8    5.0   F
    - Size: LOC=78 (>25) (-100.0 pts)
    - Size: params=7 (>4) (-18.0 pts)
    - Size: nesting depth=8 (>3) (-50.0 pts)
    - Complexity: CC=29 (>5) (-100.0 pts)
    - Complexity: cognitive=73 (>8) (-100.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Clean: 14 legacy 'var' declaration(s) detected (prefer 'const' or 'let') (-15.0 pts)
    - Clean: 19 loose equality comparison(s) (==/!=) trigger implicit type coercion (prefer ===/!==) (-10.0 pts)
    - Clean: 7 unannotated parameter(s) without default values (graph, startNode, destNode) (-10.0 pts)
```

---

### JAVASCRIPT (`--lang javascript`) — 3. Trie Prefix Tree Data Structure OOP Cohesion & Class Size

#### Good Baseline: [`javascript/trie_clean.js`](javascript/trie_clean.js) ([sidecar JSON](javascript/trie_clean.js.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/JavaScript (Data-Structures/Trie/Trie.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Data-Structures/Trie/Trie.js) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 2 | Functions/Methods: 5
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/trie_clean.js               src      42    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/trie_clean.js:4 TrieNode            6    1     1    1  100.0   A
samples/javascript/trie_clean.js:17 Trie              35    4     1   10  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/trie_clean.js:8 TrieNode.construc    4   1    0   0   0  100.0   A
samples/javascript/trie_clean.js:21 Trie.constructor    3   1    0   0   0  100.0   A
samples/javascript/trie_clean.js:30 Trie.insert        10   3    3   1   2  100.0   A
samples/javascript/trie_clean.js:47 Trie.search        10   3    3   1   2  100.0   A
samples/javascript/trie_clean.js:64 Trie.startsWith    10   3    3   1   2  100.0   A
```

#### Bad Baseline: [`javascript/trie_god_class.js`](javascript/trie_god_class.js) ([sidecar JSON](javascript/trie_god_class.js.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/JavaScript (Data-Structures/Trie/Trie.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Data-Structures/Trie/Trie.js) (`MIT`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 0.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 78.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 16
Dimensions -> SRP: 0.0 | Size: 100.0 | Complexity: 100.0 | Clean: 78.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/trie_god_class.js           src      92    -   0.0 100.0 100.0  78.0 100.0    5.0   F

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/trie_god_class.js:1 TrieGodClas    91   16     6   25    5.0   F
    - SRP: LCOM4=6 disconnected method groups (-75.0 pts)
    - SRP: methods=16 (>10) (-24.0 pts)
    - SRP: self attributes=8 (>7) (-4.0 pts)
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/trie_god_class.js:13 TrieGodClass   11   3    3   1   2   98.2   A
    - Clean: missing public docstring (-10.0 pts)
    - Clean: 1 unannotated parameter(s) without default values (word) (-2.0 pts)
samples/javascript/trie_god_class.js:25 TrieGodClass   11   3    3   1   2   98.2   A
    - Clean: missing public docstring (-10.0 pts)
    - Clean: 1 unannotated parameter(s) without default values (word) (-2.0 pts)
samples/javascript/trie_god_class.js:37 TrieGodClass    3   1    0   1   0   99.0   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 1 unannotated parameter(s) without default values (path) (-2.0 pts)
samples/javascript/trie_god_class.js:41 TrieGodClass    3   1    0   1   0   99.0   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 1 unannotated parameter(s) without default values (delim) (-2.0 pts)
samples/javascript/trie_god_class.js:49 TrieGodClass    7   2    1   1   1   99.0   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 1 unannotated parameter(s) without default values (records) (-2.0 pts)
samples/javascript/trie_god_class.js:57 TrieGodClass    4   1    0   1   0   99.0   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 1 unannotated parameter(s) without default values (msg) (-2.0 pts)
samples/javascript/trie_god_class.js:70 TrieGodClass    3   1    0   1   0   99.0   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 1 unannotated parameter(s) without default values (ms) (-2.0 pts)
samples/javascript/trie_god_class.js:85 TrieGodClass    3   1    0   1   0   99.0   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 1 unannotated parameter(s) without default values (key) (-2.0 pts)
samples/javascript/trie_god_class.js:89 TrieGodClass    3   1    0   1   0   99.0   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 1 unannotated parameter(s) without default values (word) (-2.0 pts)
samples/javascript/trie_god_class.js:93 TrieGodClass    3   1    0   1   0   99.0   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 1 unannotated parameter(s) without default values (word) (-2.0 pts)
samples/javascript/trie_god_class.js:97 TrieGodClass    9   3    3   1   2   99.0   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 1 unannotated parameter(s) without default values (tokens) (-2.0 pts)
samples/javascript/trie_god_class.js:2 TrieGodClass.   10   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/javascript/trie_god_class.js:45 TrieGodClass    3   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/javascript/trie_god_class.js:62 TrieGodClass    3   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/javascript/trie_god_class.js:66 TrieGodClass    3   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/javascript/trie_god_class.js:74 TrieGodClass   10   3    2   0   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

---

### JAVASCRIPT (`--lang javascript`) — 4. BDD Algorithmic Test Suite Hygiene & Assertion Density

#### Good Baseline: [`javascript/graph_algorithms.test.js`](javascript/graph_algorithms.test.js) ([sidecar JSON](javascript/graph_algorithms.test.js.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/JavaScript (test suites)](https://github.com/TheAlgorithms/JavaScript) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 0, test: 1) | Classes: 0 | Functions/Methods: 3
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/graph_algorithms.test.js    test     33    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/graph_algorithms.test.js:4 test:    11   1    0   0   0  100.0   A
samples/javascript/graph_algorithms.test.js:16 test:   10   1    0   0   0  100.0   A
samples/javascript/graph_algorithms.test.js:27 test:    9   1    0   0   0  100.0   A
```

#### Bad Baseline: [`javascript/graph_algorithms_bad.test.js`](javascript/graph_algorithms_bad.test.js) ([sidecar JSON](javascript/graph_algorithms_bad.test.js.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/JavaScript (test suites)](https://github.com/TheAlgorithms/JavaScript) (`MIT`)
- **Expected Scorecard:** `Composite 75.0/100 (Grade C)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 70.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 75.0/100 (Grade C) | Files: 1 (src: 0, test: 1) | Classes: 0 | Functions/Methods: 2
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 70.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/graph_algorithms_bad.test.js test     41    - 100.0 100.0 100.0  70.0 100.0   75.0   C

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/graph_algorithms_bad.test.js:4 te   35   1    0   0   0   75.0   C
    - Clean (Test): 19 assertions in single test (>8) (-30.0 pts)
samples/javascript/graph_algorithms_bad.test.js:46 t    3   1    0   0   0   75.0   C
    - Clean (Test): test has 0 assertions (-30.0 pts)
```

---

### TYPESCRIPT (`--lang typescript`) — 1. Strictly Typed TypeScript Arithmetic Service vs. Legacy Escape-Hatch Script

#### Good Baseline: [`typescript/clean_math_service.ts`](typescript/clean_math_service.ts) ([sidecar JSON](typescript/clean_math_service.ts.expected.json))

- **Upstream Dataset / Benchmark:** [Custom TypeScript Benchmark](https://www.typescriptlang.org/docs/) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 6
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/clean_math_service.ts       src      24    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/clean_math_service.ts:6 Calcula    21    5     1    6  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/clean_math_service.ts:10 Calculat    3   1    0   1   0  100.0   A
samples/typescript/clean_math_service.ts:15 Calculat    3   1    0   2   0  100.0   A
samples/typescript/clean_math_service.ts:20 Calculat    3   1    0   2   0  100.0   A
samples/typescript/clean_math_service.ts:25 Calculat    3   1    0   2   0  100.0   A
samples/typescript/clean_math_service.ts:30 Calculat    6   2    1   2   1  100.0   A
samples/typescript/clean_math_service.ts:39 formatRe    3   1    0   2   0  100.0   A
```

#### Bad Baseline: [`typescript/smelly_legacy_script.ts`](typescript/smelly_legacy_script.ts) ([sidecar JSON](typescript/smelly_legacy_script.ts.expected.json))

- **Upstream Dataset / Benchmark:** [Custom TypeScript Benchmark](https://www.typescriptlang.org/docs/) (`MIT`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 94.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 21.0` | `Security: 0.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 94.0 | Size: 100.0 | Complexity: 100.0 | Clean: 21.0 | Security: 0.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/smelly_legacy_script.ts     src      19    -  94.0 100.0 100.0  21.0   0.0    5.0   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/smelly_legacy_script.ts:4 process   19   5    6   3   3    5.0   F
    - SRP: boolean flag parameter with default value (-6.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Clean: 1 untyped param(s) (rawInput) (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
    - Clean: 2 legacy 'var' declaration(s) detected (prefer 'const' or 'let') (-6.0 pts)
    - Clean: 2 loose equality comparison(s) (==/!=) trigger implicit type coercion (prefer ===/!==) (-4.0 pts)
    - Clean: empty catch block swallows exception (-10.0 pts)
    - Clean: debugger statement detected (-10.0 pts)
    - Clean (TS): 2 explicit 'any' type usage(s) defeat type safety (-10.0 pts)
    - Clean (TS): 1 '@ts-ignore'/'@ts-nocheck' directive(s) suppress compiler checks (-10.0 pts)
    - Clean (TS): 2 non-null assertion(s) ('!') bypass strict null checks (-4.0 pts)
    - Security: dynamic code execution via eval (-40.0 pts)
    - Security: dynamic code execution via new Function (-40.0 pts)
    - Security: string argument to setTimeout causes implicit code evaluation (-20.0 pts)
    - Security: direct prototype mutation via '__proto__' (-25.0 pts)
    - Security: 'with' statement obscures lexical scope and risks prototype pollution (-30.0 pts)
```


---

### TYPESCRIPT (`--lang typescript`) — 2. Graph Shortest-Path Algorithmic Complexity (Decomposed Typed Dijkstra vs. Monolith)

#### Good Baseline: [`typescript/dijkstra_clean.ts`](typescript/dijkstra_clean.ts) ([sidecar JSON](typescript/dijkstra_clean.ts.expected.json))

- **Upstream Dataset / Benchmark:** [Custom TypeScript Benchmark (modeled after TheAlgorithms Dijkstra)](https://github.com/TheAlgorithms/TypeScript) (`MIT`)
- **Expected Scorecard:** `Composite 99.8/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 99.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 99.8/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 5
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 99.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/dijkstra_clean.ts           src      88    - 100.0 100.0  99.0 100.0 100.0   99.8   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/dijkstra_clean.ts:87 findShortest   20   6    4   3   2   99.2   A
    - Complexity: CC=6 (>5) (-4.0 pts)
samples/typescript/dijkstra_clean.ts:16 initializeDi   15   3    2   2   1  100.0   A
samples/typescript/dijkstra_clean.ts:34 findNearestU   15   4    3   2   2  100.0   A
samples/typescript/dijkstra_clean.ts:52 relaxNeighbo   19   5    5   4   2  100.0   A
samples/typescript/dijkstra_clean.ts:73 reconstructP   12   3    1   2   1  100.0   A
```

#### Bad Baseline: [`typescript/dijkstra_branchy.ts`](typescript/dijkstra_branchy.ts) ([sidecar JSON](typescript/dijkstra_branchy.ts.expected.json))

- **Upstream Dataset / Benchmark:** [Custom TypeScript Benchmark (Legacy Branchy Shortest Path)](https://github.com/TheAlgorithms/TypeScript) (`MIT`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 82.0` | `Size: 0.0` | `Complexity: 0.0` | `Clean: 8.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 82.0 | Size: 0.0 | Complexity: 0.0 | Clean: 8.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/dijkstra_branchy.ts         src      81    -  82.0   0.0   0.0   8.0 100.0    5.0   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/dijkstra_branchy.ts:4 findShortes   81  28   86   7  10    5.0   F
    - SRP: boolean flag parameter with default value (-18.0 pts)
    - Size: LOC=81 (>25) (-100.0 pts)
    - Size: params=7 (>4) (-18.0 pts)
    - Size: nesting depth=10 (>3) (-70.0 pts)
    - Complexity: CC=28 (>5) (-100.0 pts)
    - Complexity: cognitive=86 (>8) (-100.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Clean: 3 untyped param(s) (graph, startNode, targetNode) (-15.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
    - Clean: 15 legacy 'var' declaration(s) detected (prefer 'const' or 'let') (-15.0 pts)
    - Clean: 17 loose equality comparison(s) (==/!=) trigger implicit type coercion (prefer ===/!==) (-10.0 pts)
    - Clean (TS): 4 explicit 'any' type usage(s) defeat type safety (-20.0 pts)
    - Clean (TS): 1 '@ts-ignore'/'@ts-nocheck' directive(s) suppress compiler checks (-10.0 pts)
    - Clean (TS): 1 non-null assertion(s) ('!') bypass strict null checks (-2.0 pts)
```


---

### TYPESCRIPT (`--lang typescript`) — 3. OOP Cache Cohesion & Parameter Properties (Cohesive LRUCache vs. God Class)

#### Good Baseline: [`typescript/lru_cache_clean.ts`](typescript/lru_cache_clean.ts) ([sidecar JSON](typescript/lru_cache_clean.ts.expected.json))

- **Upstream Dataset / Benchmark:** [Custom TypeScript Benchmark](https://www.typescriptlang.org/docs/handbook/2/classes.html) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 9
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/lru_cache_clean.ts          src      70    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/lru_cache_clean.ts:14 LRUCache     63    9     1   14  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/lru_cache_clean.ts:21 LRUCache.co    5   2    1   1   1  100.0   A
samples/typescript/lru_cache_clean.ts:28 LRUCache.ge   10   2    1   1   1  100.0   A
samples/typescript/lru_cache_clean.ts:40 LRUCache.pu   10   3    2   2   1  100.0   A
samples/typescript/lru_cache_clean.ts:52 LRUCache.ha    3   1    0   1   0  100.0   A
samples/typescript/lru_cache_clean.ts:57 LRUCache.de    3   1    0   1   0  100.0   A
samples/typescript/lru_cache_clean.ts:62 LRUCache.cl    6   1    0   0   0  100.0   A
samples/typescript/lru_cache_clean.ts:70 LRUCache.ge    9   1    0   0   0  100.0   A
samples/typescript/lru_cache_clean.ts:81 LRUCache.to    4   1    0   2   0  100.0   A
samples/typescript/lru_cache_clean.ts:87 LRUCache.ev    7   2    1   0   1  100.0   A
```

#### Bad Baseline: [`typescript/lru_cache_god_class.ts`](typescript/lru_cache_god_class.ts) ([sidecar JSON](typescript/lru_cache_god_class.ts.expected.json))

- **Upstream Dataset / Benchmark:** [Custom TypeScript Benchmark](https://www.typescriptlang.org/docs/handbook/2/classes.html) (`MIT`)
- **Expected Scorecard:** `Composite 55.0/100 (Grade F)` — `SRP: 50.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 65.8` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 55.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 15
Dimensions -> SRP: 50.0 | Size: 100.0 | Complexity: 100.0 | Clean: 65.8 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/lru_cache_god_class.ts      src      86    -  50.0 100.0 100.0  65.8 100.0   55.0   F
    - Clean (TS): 1 '@ts-ignore'/'@ts-nocheck' directive(s) suppress compiler checks (-10.0 pts)

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/lru_cache_god_class.ts:4 Legacy    86   15     3   20   55.0   F
    - SRP: LCOM4=3 disconnected method groups (-30.0 pts)
    - SRP: methods=15 (>10) (-20.0 pts)
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/lru_cache_god_class.ts:27 LegacyC   11   2    1   1   1   96.7   A
    - Clean: missing public docstring (-10.0 pts)
    - Clean: 1 untyped param(s) (key) (-5.0 pts)
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
    - Clean (TS): 1 non-null assertion(s) ('!') bypass strict null checks (-2.0 pts)
samples/typescript/lru_cache_god_class.ts:39 LegacyC   12   3    2   2   1   96.7   A
    - Clean: missing public docstring (-10.0 pts)
    - Clean: 1 untyped param(s) (key) (-5.0 pts)
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
    - Clean (TS): 1 non-null assertion(s) ('!') bypass strict null checks (-2.0 pts)
samples/typescript/lru_cache_god_class.ts:13 LegacyC    9   1    0   1   0   98.5   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
samples/typescript/lru_cache_god_class.ts:52 LegacyC    3   1    0   1   0   98.5   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 1 untyped param(s) (key) (-5.0 pts)
samples/typescript/lru_cache_god_class.ts:56 LegacyC    3   1    0   1   0   98.5   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 1 untyped param(s) (key) (-5.0 pts)
samples/typescript/lru_cache_god_class.ts:64 LegacyC    3   1    0   1   0   98.5   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 1 untyped param(s) (message) (-5.0 pts)
samples/typescript/lru_cache_god_class.ts:89 LegacyC    3   1    0   1   0   98.5   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 1 untyped param(s) (prefix) (-5.0 pts)
samples/typescript/lru_cache_god_class.ts:84 LegacyC    4   2    1   0   1   99.0   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 1 loose equality comparison(s) (==/!=) trigger implicit type coercion (prefer ===/!==) (-2.0 pts)
samples/typescript/lru_cache_god_class.ts:93 LegacyC    7   2    1   0   1   99.0   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 1 loose equality comparison(s) (==/!=) trigger implicit type coercion (prefer ===/!==) (-2.0 pts)
samples/typescript/lru_cache_god_class.ts:23 LegacyC    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/lru_cache_god_class.ts:60 LegacyC    3   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/lru_cache_god_class.ts:68 LegacyC    5   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/lru_cache_god_class.ts:74 LegacyC    4   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/lru_cache_god_class.ts:79 LegacyC    4   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/lru_cache_god_class.ts:101 Legacy    3   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```


---

### TYPESCRIPT (`--lang typescript`) — 4. Backend Repository Security & SQL Injection (Parameterized Queries vs. Unsafe Interpolation)

#### Good Baseline: [`typescript/order_repository_clean.ts`](typescript/order_repository_clean.ts) ([sidecar JSON](typescript/order_repository_clean.ts.expected.json))

- **Upstream Dataset / Benchmark:** [Custom TypeScript Benchmark](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 5
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/order_repository_clean.ts   src      52    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/order_repository_clean.ts:24 Or    29    4     1    5  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/order_repository_clean.ts:26 Orde    1   1    0   1   0  100.0   A
samples/typescript/order_repository_clean.ts:29 Orde    7   1    0   1   0  100.0   A
samples/typescript/order_repository_clean.ts:38 Orde   11   1    0   3   0  100.0   A
samples/typescript/order_repository_clean.ts:51 Orde    8   2    1   2   1  100.0   A
samples/typescript/order_repository_clean.ts:62 sumP    9   4    3   1   2  100.0   A
```

#### Bad Baseline: [`typescript/order_repository_unsafe.ts`](typescript/order_repository_unsafe.ts) ([sidecar JSON](typescript/order_repository_unsafe.ts.expected.json))

- **Upstream Dataset / Benchmark:** [Custom TypeScript Benchmark](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) (`MIT`)
- **Expected Scorecard:** `Composite 25.0/100 (Grade F)` — `SRP: 82.6` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 53.6` | `Security: 20.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 25.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 5
Dimensions -> SRP: 82.6 | Size: 100.0 | Complexity: 100.0 | Clean: 53.6 | Security: 20.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/order_repository_unsafe.ts  src      34    -  82.6 100.0 100.0  53.6  20.0   25.0   F
    - Clean (TS): 1 '@ts-ignore'/'@ts-nocheck' directive(s) suppress compiler checks (-10.0 pts)

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/order_repository_unsafe.ts:4 Le    34    5     2    9   25.0   F
    - SRP: LCOM4=2 disconnected method groups (-15.0 pts)
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/order_repository_unsafe.ts:23 Leg   15   4    6   3   3   25.0   F
    - SRP: boolean flag parameter with default value (-6.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Clean: 2 untyped param(s) (orderId, nextStatus) (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
    - Clean: 1 loose equality comparison(s) (==/!=) trigger implicit type coercion (prefer ===/!==) (-2.0 pts)
    - Clean: empty catch block swallows exception (-10.0 pts)
    - Security: dynamic code execution via new Function (-40.0 pts)
    - Security (TS): potential SQL/query injection in this.db.execute via string concatenation (-40.0 pts)
samples/typescript/order_repository_unsafe.ts:11 Leg    7   2    1   3   1   65.0   D
    - SRP: boolean flag parameter with default value (-6.0 pts)
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 2 untyped param(s) (customerId, statusFilter) (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
    - Clean: 1 legacy 'var' declaration(s) detected (prefer 'const' or 'let') (-3.0 pts)
    - Clean (TS): 1 non-null assertion(s) ('!') bypass strict null checks (-2.0 pts)
    - Security (TS): potential SQL/query injection in this.db.query via string concatenation (-40.0 pts)
samples/typescript/order_repository_unsafe.ts:19 Leg    3   1    0   1   0   65.0   D
    - Clean: missing public docstring (-5.0 pts)
    - Clean (TS): 2 explicit 'any' type usage(s) defeat type safety (-10.0 pts)
    - Security (TS): potential SQL/query injection in this.db.$queryRawUnsafe via string concatenation (-40.0 pts)
samples/typescript/order_repository_unsafe.ts:40 Leg    3   1    0   2   0   65.0   D
    - Clean: missing public docstring (-5.0 pts)
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
    - Security: dynamic code execution via eval (-40.0 pts)
samples/typescript/order_repository_unsafe.ts:7 Lega    3   1    0   1   0   98.5   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
```


---

### TYPESCRIPT (`--lang typescript`) — 5. React 18 TSX Component Decomposition & Props Hygiene vs. Monolithic TSX Board

#### Good Baseline: [`typescript/task_filter_bar.tsx`](typescript/task_filter_bar.tsx) ([sidecar JSON](typescript/task_filter_bar.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [Custom TypeScript/React TSX Benchmark](https://react.dev/learn/typescript) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 4
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/task_filter_bar.tsx         src      75    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/task_filter_bar.tsx:22 filterTask   12   5    1   3   1  100.0   A
samples/typescript/task_filter_bar.tsx:36 summarizeT   12   3    3   1   2  100.0   A
samples/typescript/task_filter_bar.tsx:50 SearchInpu   17   1    0   1   0  100.0   A
samples/typescript/task_filter_bar.tsx:69 TaskFilter   21   1    0   1   0  100.0   A
```

#### Bad Baseline: [`typescript/task_board_legacy.tsx`](typescript/task_board_legacy.tsx) ([sidecar JSON](typescript/task_board_legacy.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [Custom TypeScript/React TSX Benchmark](https://react.dev/learn/typescript) (`MIT`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 79.0` | `Size: 6.5` | `Complexity: 0.0` | `Clean: 46.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 79.0 | Size: 6.5 | Complexity: 0.0 | Clean: 46.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/task_board_legacy.tsx       src      51    -  79.0   6.5   0.0  46.0 100.0    5.0   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/task_board_legacy.tsx:5 TaskBoard   50  18   40   5   8    5.0   F
    - SRP: high external call fan-out=9 (>6) (-9.0 pts)
    - SRP: boolean flag parameter with default value (-12.0 pts)
    - Size: LOC=50 (>25) (-37.5 pts)
    - Size: params=5 (>4) (-6.0 pts)
    - Size: nesting depth=8 (>3) (-50.0 pts)
    - Complexity: CC=18 (>5) (-76.0 pts)
    - Complexity: cognitive=40 (>8) (-80.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Clean: empty catch block swallows exception (-10.0 pts)
    - Clean (TS): 6 explicit 'any' type usage(s) defeat type safety (-20.0 pts)
    - Clean (TS): 1 '@ts-ignore'/'@ts-nocheck' directive(s) suppress compiler checks (-10.0 pts)
    - Clean (TS): 2 non-null assertion(s) ('!') bypass strict null checks (-4.0 pts)
```


---

### TYPESCRIPT (`--lang typescript`) — 6. Async Webhook Dispatcher Size & Contract Clarity vs. Oversized Monolithic Handler

#### Good Baseline: [`typescript/webhook_dispatcher_clean.ts`](typescript/webhook_dispatcher_clean.ts) ([sidecar JSON](typescript/webhook_dispatcher_clean.ts.expected.json))

- **Upstream Dataset / Benchmark:** [Custom TypeScript Benchmark](https://www.typescriptlang.org/docs/) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 4
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/webhook_dispatcher_clean.ts src      47    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/webhook_dispatcher_clean.ts:23 ve    6   2    0   2   0  100.0   A
samples/typescript/webhook_dispatcher_clean.ts:33 we    7   3    1   1   1  100.0   A
samples/typescript/webhook_dispatcher_clean.ts:42 we    7   3    1   1   1  100.0   A
samples/typescript/webhook_dispatcher_clean.ts:52 di   12   3    2   2   1  100.0   A
```

#### Bad Baseline: [`typescript/webhook_dispatcher_smelly.ts`](typescript/webhook_dispatcher_smelly.ts) ([sidecar JSON](typescript/webhook_dispatcher_smelly.ts.expected.json))

- **Upstream Dataset / Benchmark:** [Custom TypeScript Benchmark](https://www.typescriptlang.org/docs/) (`MIT`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 82.0` | `Size: 29.0` | `Complexity: 0.0` | `Clean: 45.0` | `Security: 80.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 82.0 | Size: 29.0 | Complexity: 0.0 | Clean: 45.0 | Security: 80.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/webhook_dispatcher_smelly.ts src      53    -  82.0  29.0   0.0  45.0  80.0    5.0   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/webhook_dispatcher_smelly.ts:3 di   53  18   26   5   5    5.0   F
    - SRP: boolean flag parameter with default value (-18.0 pts)
    - Size: LOC=53 (>25) (-45.0 pts)
    - Size: params=5 (>4) (-6.0 pts)
    - Size: nesting depth=5 (>3) (-20.0 pts)
    - Complexity: CC=18 (>5) (-76.0 pts)
    - Complexity: cognitive=26 (>8) (-45.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
    - Clean: empty catch block swallows exception (-10.0 pts)
    - Clean (TS): 3 explicit 'any' type usage(s) defeat type safety (-15.0 pts)
    - Clean (TS): 6 non-null assertion(s) ('!') bypass strict null checks (-10.0 pts)
    - Security: string argument to setTimeout causes implicit code evaluation (-20.0 pts)
```


---

### TYPESCRIPT (`--lang typescript`) — 7. Jest/Vitest TypeScript BDD Test Suite Assertion Density & Type Safety

#### Good Baseline: [`typescript/dijkstra.test.ts`](typescript/dijkstra.test.ts) ([sidecar JSON](typescript/dijkstra.test.ts.expected.json))

- **Upstream Dataset / Benchmark:** [Custom TypeScript Test Benchmark](https://vitest.dev/) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 0, test: 1) | Classes: 0 | Functions/Methods: 3
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/dijkstra.test.ts            test     31    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/dijkstra.test.ts:7 test: computes   11   1    0   0   0  100.0   A
samples/typescript/dijkstra.test.ts:19 test: returns   10   1    0   0   0  100.0   A
samples/typescript/dijkstra.test.ts:30 test: rejects    7   1    0   0   0  100.0   A
```

#### Bad Baseline: [`typescript/dijkstra_bad.test.ts`](typescript/dijkstra_bad.test.ts) ([sidecar JSON](typescript/dijkstra_bad.test.ts.expected.json))

- **Upstream Dataset / Benchmark:** [Custom TypeScript Test Benchmark](https://vitest.dev/) (`MIT`)
- **Expected Scorecard:** `Composite 66.8/100 (Grade D)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 61.8` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 66.8/100 (Grade D) | Files: 1 (src: 0, test: 1) | Classes: 0 | Functions/Methods: 2
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 61.8 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/dijkstra_bad.test.ts        test     28    - 100.0 100.0 100.0  61.8 100.0   66.8   D
    - Clean (TS): 1 '@ts-ignore'/'@ts-nocheck' directive(s) suppress compiler checks (-10.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/dijkstra_bad.test.ts:32 test: pla    3   1    0   0   0   75.0   C
    - Clean (Test): test has 0 assertions (-30.0 pts)
samples/typescript/dijkstra_bad.test.ts:5 test: vali   22   1    0   0   0   77.0   C
    - Clean (Test): 10 assertions in single test (>8) (-6.0 pts)
    - Clean (TS): 5 explicit 'any' type usage(s) defeat type safety (-20.0 pts)
    - Clean (TS): 1 non-null assertion(s) ('!') bypass strict null checks (-2.0 pts)
```
