# Design: JavaScript Competitive Coding & Benchmark Baseline Samples

## 1. Intent & Context
The repository provides a multi-language code health analyzer evaluated across 5 core dimensions: Single Responsibility Principle (SRP), Size, Complexity, Clean Code, and Security.

To guarantee empirical accuracy, the repo maintains a catalog of functionally comparable **Good** and **Bad** sample baselines across supported languages (Python, Java, and JavaScript). Python currently features 4 paired scenarios, Java features 6 paired scenarios, whereas JavaScript only has 1 synthetic pair (`clean_math_service.js` vs. `smelly_legacy_script.js`).

This project adds 3 new paired scenarios (6 code files + sidecars) to the JavaScript catalog, sourced from canonical competitive programming datasets ([`TheAlgorithms/JavaScript`](https://github.com/TheAlgorithms/JavaScript)) and standard BDD/Jest test suites. This brings JavaScript to full parity with Python and Java across all 5 scorecard dimensions.

---

## 2. Goals, Non-Goals, & Anti-Goals

### Goals
1. Add 3 realistic paired scenarios (Good vs. Bad) to `samples/javascript/`:
   - **Scenario 2**: Graph Shortest-Path / Dijkstra (Algorithmic Complexity & Control Flow).
   - **Scenario 3**: Trie Prefix Tree (Data Structure OOP Cohesion & SRP / LCOM4).
   - **Scenario 4**: Algorithmic BDD Test Suite (Jest / Mocha Test Suite Hygiene & Assertion Density).
2. Ensure each scenario pairs a Good sample (Grade A, Score $\ge 90.0$) and a Bad sample (Grade C, D, or F, Score $< 80.0$) solving identical algorithmic problems.
3. Generate sidecar `<file>.expected.json` files capturing expected scores, LOC, AST counts, and required findings.
4. Register all 6 new samples in `samples/manifest.json`, expanding the verified catalog from 22 to 28 samples.
5. Update `tests/unit/test_language_scorecard_samples.py` to assert 28 samples and pass all automated comparison tests.
6. Update `samples/SCORECARD_BASELINES.md` summary table and detailed scenario scorecards with full deterministic output.
7. Maintain $\ge 95.0\%$ overall codebase health for `scripts/`.

### Non-Goals
- Modifying tree-sitter grammar bindings or analyzer rubric scoring formulas unless a parser deficiency is uncovered.
- Introducing npm dependencies or build steps; files must be pure standard ECMAScript compatible with the internal CST parser.

### Anti-Goals
- Artificial, non-functional code snippets that do not execute valid algorithmic logic.
- "Good" baseline samples that trigger clean code penalties or fail to achieve Grade A.
- "Bad" baseline samples that pass by accidentally evading dimension thresholds.

---

## 3. Approaches Considered

### Option 1 (Selected): 3 New Competitive & Research Scenarios (4 Scenarios Total)
Keep Scenario 1 (which specifically validates JavaScript security anti-patterns: `eval`, `Function`, `setTimeout(string)`, `with`, proto pollution) and add 3 competitive/research scenarios covering algorithmic complexity, OOP cohesion, and BDD test hygiene.
- *Pros*: Complete coverage across all 5 dimensions without discarding existing security baseline tests.
- *Trade-offs*: Total JavaScript catalog becomes 4 scenarios (8 sample files).

### Option 2: 4 Brand-New Competitive Coding Scenarios (Discarding Scenario 1)
Replace Scenario 1 entirely with 4 pure competitive algorithm pairs (Dijkstra, 0/1 Knapsack, Trie, and Solution Test Harness).
- *Pros*: 100% competitive algorithms across the entire JS sample directory.
- *Cons*: Loses the dedicated verification of dynamic code evaluation and JS-specific security hygiene rules.

**Decision**: The user selected **Option 1**.

---

## 4. Detailed Scenario Architecture

### Scenario 2: Graph Algorithm Complexity & Control Flow
- **Benchmark Source**: [`TheAlgorithms/JavaScript (Graphs/Dijkstra.js)`](https://github.com/TheAlgorithms/JavaScript/blob/master/Graphs/Dijkstra.js)
- **Problem**: Dijkstra Single-Source Shortest Path on a weighted adjacency graph.
- **Good Baseline (`samples/javascript/dijkstra_clean.js`)**:
  - Modular design: separate `minDistanceNode(distances, visited)` selector helper and `dijkstra(graph, startNode)` runner.
  - Low cyclomatic complexity ($CC \le 4$), low cognitive complexity ($Cog \le 3$), max nesting depth $\le 2$.
  - Clean JSDoc comments, modern `const`/`let`, default parameters.
  - Target: SRP 100.0 | Size 100.0 | Complexity 100.0 | Clean 100.0 | Security 100.0 -> **Composite 100.0 (Grade A)**.
- **Bad Baseline (`samples/javascript/dijkstra_branchy.js`)**:
  - Monolithic competitive script embedding nested while/for loops, deeply nested edge relaxation conditions (nesting depth $\ge 4$).
  - High cyclomatic complexity ($CC \ge 16$), cognitive complexity $\ge 18$, function LOC $\ge 50$.
  - Anti-patterns: `var`, loose equality (`==`), missing docstrings.
  - Target Dimension: `complexity`.
  - Target: SRP 100.0 | Size $\le 30.0$ | Complexity $\le 20.0$ | Clean $\le 70.0$ | Security 100.0 -> **Composite $\le 25.0$ (Grade F)**.

### Scenario 3: Data Structure OOP Cohesion & Class Size (SRP)
- **Benchmark Source**: [`TheAlgorithms/JavaScript (Data-Structures/Trie/Trie.js)`](https://github.com/TheAlgorithms/JavaScript/blob/master/Data-Structures/Trie/Trie.js) (LeetCode 208 Implement Trie).
- **Problem**: Prefix Tree (Trie) for string insertion, prefix matching, and word search.
- **Good Baseline (`samples/javascript/trie_clean.js`)**:
  - Two cohesive ES6 classes: `TrieNode` and `Trie`.
  - `TrieNode` manages character map and `isEndOfWord`.
  - `Trie` exposes cohesive methods: `insert(word)`, `search(word)`, `startsWith(prefix)`.
  - All methods share `this.root`. High cohesion: $LCOM4 = 1$, method count $\le 5$, class LOC $\le 50$.
  - Target: SRP 100.0 | Size 100.0 | Complexity 100.0 | Clean 100.0 | Security 100.0 -> **Composite 100.0 (Grade A)**.
- **Bad Baseline (`samples/javascript/trie_god_class.js`)**:
  - Bloated "God Class" `TrieGodClass` containing 12+ methods.
  - Mixes unrelated responsibilities: Trie operations (`insert`, `search`), file formatting/exporting (`dumpToJson`, `exportToCsv`), console debugging (`printAsciiTree`, `dumpStats`), and dictionary utilities (`filterAnagrams`, `calculateFrequencies`).
  - Disconnected field usage yielding $LCOM4 \ge 4$, methods $> 10$, class LOC $> 150$.
  - Target Dimension: `srp`.
  - Target: SRP $\le 10.0$ | Size $\le 80.0$ | Complexity 100.0 | Clean $\le 85.0$ | Security 100.0 -> **Composite $\le 40.0$ (Grade F)**.

### Scenario 4: BDD / Jest Unit Test Suite Hygiene
- **Benchmark Source**: Algorithmic test suites using Jest/Mocha BDD conventions (`describe`, `it`, `test`, `expect`).
- **Problem**: Unit test suite verifying Dijkstra graph algorithm correctness on various graph topologies.
- **Good Baseline (`samples/javascript/graph_algorithms.test.js`)**:
  - Structured `describe('Dijkstra Shortest Path', ...)` with 3 focused test cases:
    1. `test('computes correct shortest distances on simple DAG', ...)` (2 assertions)
    2. `test('handles disconnected vertices with Infinity distance', ...)` (2 assertions)
    3. `test('returns zero distance for source vertex to itself', ...)` (1 assertion)
  - Assertions per test $\le 4$ (within rubric threshold of 8).
  - Target: SRP 100.0 | Size 100.0 | Complexity 100.0 | Clean 100.0 | Security 100.0 -> **Composite 100.0 (Grade A)**.
- **Bad Baseline (`samples/javascript/graph_algorithms_bad.test.js`)**:
  - Overloaded test file with a single massive `test('exhaustive graph validation', ...)` containing $> 15$ assertions (`expect` calls).
  - Contains an empty test block `test('pending verification', () => {})` triggering empty test method penalty.
  - Excessive test file LOC.
  - Target Dimension: `clean`.
  - Target: SRP 100.0 | Size $\le 90.0$ | Complexity 100.0 | Clean $\le 65.0$ | Security 100.0 -> **Composite $\le 65.0$ (Grade D)**.

---

## 5. Verification Plan
1. **Automated Baseline Suite**:
   `pytest tests/unit/test_language_scorecard_samples.py -v` must execute all 28 samples (56 parameter instances + pairwise checks) with 100% pass rate.
2. **Catalog Consistency**:
   `samples/SCORECARD_BASELINES.md` must accurately reflect all 4 JavaScript scenarios in both the summary table and the detailed section.
3. **Full Repository Tests**:
   `pytest -v` must pass all unit and integration tests across Python, Java, and JavaScript.
4. **Self-Health Gate**:
   `python scripts/code_health.py scripts --fail-under 90.0` must verify overall score $\ge 95.0\%$ (Grade A).
