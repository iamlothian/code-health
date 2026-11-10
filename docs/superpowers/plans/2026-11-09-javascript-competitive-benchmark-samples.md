# JavaScript Competitive Benchmark Baseline Samples Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add 3 paired competitive coding and research benchmark scenarios (6 JS sample files and sidecars) to the JavaScript code health baseline catalog.

**Architecture:** Each scenario pairs a clean, modular Good sample (Grade A) against a smelly, branchy, or monolithic Bad sample (Grade C/D/F) solving identical algorithmic logic. Samples are paired with sidecar `.expected.json` files, registered in `manifest.json`, validated by `test_language_scorecard_samples.py`, and documented in `SCORECARD_BASELINES.md`.

**Tech Stack:** JavaScript (ES6+), Python 3.12, tree-sitter, tree-sitter-javascript, pytest.

**Spec:** `docs/superpowers/specs/2026-11-09-javascript-competitive-benchmark-samples-design.md`

## Global Constraints

- Target directory: `samples/javascript/` for code and sidecars.
- Pure ECMAScript with standard syntax; no external npm runtime dependencies.
- Every Good sample must score $\ge 90.0$ (Grade A) with zero dimension penalties.
- Every Bad sample must score $< 80.0$ (Grade C, D, or F) and trigger target dimension penalties.
- Sidecar `<file>.js.expected.json` files must capture exact scores, LOC, AST counts, and `rendered_console` text.
- `samples/manifest.json` must be updated with all 6 new samples, bringing total sample count from 22 to 28.
- `tests/unit/test_language_scorecard_samples.py` must pass with all 28 samples (70 tests total).
- Overall repository code health for `scripts/` must remain $\ge 95.0\%$.

## Review Focus

- Unreachable/disconnected graph vertices: `dijkstra_clean.js` must handle disconnected nodes without runtime errors.
- Empty prefix in Trie: `trie_clean.js` must handle root/empty prefix lookup safely.
- Empty catch block detection: `dijkstra_branchy.js` and `trie_god_class.js` anti-patterns must trigger clean code penalties deterministically.
- Sidecar console drift: `rendered_console` in `.expected.json` must strictly match `ScorecardFormatter.render_console(report)`.
- Pairwise score dominance: In every scenario, Good sample composite and target dimension must strictly exceed Bad sample.

---

### Task 1: Scenario 2 — Graph Dijkstra Complexity & Control Flow

**Files:**
- Create: `samples/javascript/dijkstra_clean.js`
- Create: `samples/javascript/dijkstra_clean.js.expected.json`
- Create: `samples/javascript/dijkstra_branchy.js`
- Create: `samples/javascript/dijkstra_branchy.js.expected.json`

**Interfaces:**
- Consumes: None (independent sample files).
- Produces: Pair `javascript_dijkstra_clean` / `javascript_dijkstra_branchy` under pair_id `javascript_graph_complexity`.

- [ ] **Step 1: Write `samples/javascript/dijkstra_clean.js`**
  Implement modular Dijkstra algorithm with `minDistanceNode(distances = {}, visited = new Set())` and `dijkstra(graph = {}, startNode = '')`. JSDoc comments on all functions, `const`/`let`, $CC \le 4$, nesting $\le 2$.

- [ ] **Step 2: Write `samples/javascript/dijkstra_branchy.js`**
  Implement monolithic Dijkstra algorithm in a single function `dijkstra(graph, startNode)` with legacy `var`, loose equality `==`, nested while/for loops with nesting depth $\ge 4$, $CC \ge 16$, cognitive complexity $\ge 18$, and LOC $\ge 50$.

- [ ] **Step 3: Generate sidecar `.expected.json` files for both Dijkstra samples**
  Run `CodeHealthRunner` on both files to compute exact metrics, required findings, and rendered console text, and write `samples/javascript/dijkstra_clean.js.expected.json` and `samples/javascript/dijkstra_branchy.js.expected.json`.

- [ ] **Step 4: Verify Dijkstra scorecard baselines**
  Run:
  ```powershell
  .venv\Scripts\python.exe -c "from _code_health.reporting import CodeHealthRunner; from _code_health.models import RubricConfig; from pathlib import Path; r = CodeHealthRunner(Path('.'), RubricConfig(), git_mode='no-git', lang_override='javascript'); res = r.run([Path('samples/javascript/dijkstra_clean.js'), Path('samples/javascript/dijkstra_branchy.js')]); print('Good:', res.files[0].scores.composite, res.files[0].scores.grade); print('Bad:', res.files[1].scores.composite, res.files[1].scores.grade)"
  ```
  Expected: Good is 100.0 (Grade A), Bad is $\le 25.0$ (Grade F).

- [ ] **Step 5: Commit**
  ```bash
  git add samples/javascript/dijkstra*
  git commit -m "feat(samples): add scenario 2 Dijkstra graph complexity baseline"
  ```

---

### Task 2: Scenario 3 — Trie Prefix Tree OOP Cohesion & SRP

**Files:**
- Create: `samples/javascript/trie_clean.js`
- Create: `samples/javascript/trie_clean.js.expected.json`
- Create: `samples/javascript/trie_god_class.js`
- Create: `samples/javascript/trie_god_class.js.expected.json`

**Interfaces:**
- Consumes: None.
- Produces: Pair `javascript_trie_clean` / `javascript_trie_god_class` under pair_id `javascript_trie_srp`.

- [ ] **Step 1: Write `samples/javascript/trie_clean.js`**
  Implement cohesive ES6 classes `TrieNode` and `Trie`. Methods: `constructor`, `insert(word = '')`, `search(word = '')`, `startsWith(prefix = '')`. All methods use `this.root`. $LCOM4 = 1$, methods $\le 5$, class LOC $\le 50$, JSDoc on all methods.

- [ ] **Step 2: Write `samples/javascript/trie_god_class.js`**
  Implement `TrieGodClass` with 12+ methods mixing Trie operations (`insert`, `search`) with disconnected responsibilities: file dumping (`dumpToJson`, `exportToCsv`), console formatting (`printAsciiTree`, `dumpStats`), anagram generation (`filterAnagrams`), frequency counters (`calculateFrequencies`). Disconnected field groups produce $LCOM4 \ge 4$, methods $> 10$, class LOC $> 150$.

- [ ] **Step 3: Generate sidecar `.expected.json` files for both Trie samples**
  Run `CodeHealthRunner` on both files to compute exact metrics, required findings, and rendered console text, and write `samples/javascript/trie_clean.js.expected.json` and `samples/javascript/trie_god_class.js.expected.json`.

- [ ] **Step 4: Verify Trie scorecard baselines**
  Run:
  ```powershell
  .venv\Scripts\python.exe -c "from _code_health.reporting import CodeHealthRunner; from _code_health.models import RubricConfig; from pathlib import Path; r = CodeHealthRunner(Path('.'), RubricConfig(), git_mode='no-git', lang_override='javascript'); res = r.run([Path('samples/javascript/trie_clean.js'), Path('samples/javascript/trie_god_class.js')]); print('Good:', res.files[0].scores.composite, res.files[0].scores.grade); print('Bad:', res.files[1].scores.composite, res.files[1].scores.grade)"
  ```
  Expected: Good is 100.0 (Grade A), Bad is $\le 40.0$ (Grade F).

- [ ] **Step 5: Commit**
  ```bash
  git add samples/javascript/trie*
  git commit -m "feat(samples): add scenario 3 Trie OOP cohesion baseline"
  ```

---

### Task 3: Scenario 4 — BDD / Jest Unit Test Hygiene

**Files:**
- Create: `samples/javascript/graph_algorithms.test.js`
- Create: `samples/javascript/graph_algorithms.test.js.expected.json`
- Create: `samples/javascript/graph_algorithms_bad.test.js`
- Create: `samples/javascript/graph_algorithms_bad.test.js.expected.json`

**Interfaces:**
- Consumes: None.
- Produces: Pair `javascript_test_hygiene_good` / `javascript_test_hygiene_bad` under pair_id `javascript_test_hygiene`.

- [ ] **Step 1: Write `samples/javascript/graph_algorithms.test.js`**
  Implement BDD Jest/Mocha test suite: `describe('Dijkstra Algorithm', ...)` with 3 focused test cases (`test(...)` or `it(...)`), each having 1 to 3 `expect(...).toEqual(...)` assertions ($\le 4$ assertions per test, well within rubric limit of 8).

- [ ] **Step 2: Write `samples/javascript/graph_algorithms_bad.test.js`**
  Implement bloated test suite with a single `test('exhaustive graph validation', ...)` containing $> 15$ assertions (`expect` calls), plus an empty test block `test('placeholder verification', () => {})` that triggers the empty test penalty.

- [ ] **Step 3: Generate sidecar `.expected.json` files for both test samples**
  Run `CodeHealthRunner` on both files to compute exact metrics, required findings, and rendered console text, and write `samples/javascript/graph_algorithms.test.js.expected.json` and `samples/javascript/graph_algorithms_bad.test.js.expected.json`.

- [ ] **Step 4: Verify test hygiene scorecard baselines**
  Run:
  ```powershell
  .venv\Scripts\python.exe -c "from _code_health.reporting import CodeHealthRunner; from _code_health.models import RubricConfig; from pathlib import Path; r = CodeHealthRunner(Path('.'), RubricConfig(), git_mode='no-git', lang_override='javascript'); res = r.run([Path('samples/javascript/graph_algorithms.test.js'), Path('samples/javascript/graph_algorithms_bad.test.js')]); print('Good:', res.files[0].scores.composite, res.files[0].scores.grade); print('Bad:', res.files[1].scores.composite, res.files[1].scores.grade)"
  ```
  Expected: Good is 100.0 (Grade A), Bad is $\le 65.0$ (Grade D).

- [ ] **Step 5: Commit**
  ```bash
  git add samples/javascript/graph_algorithms*.test.js*
  git commit -m "feat(samples): add scenario 4 BDD unit test hygiene baseline"
  ```

---

### Task 4: Manifest & Automated Verification

**Files:**
- Modify: `samples/manifest.json`
- Modify: `tests/unit/test_language_scorecard_samples.py`

**Interfaces:**
- Consumes: All 6 new samples and sidecar JSON files from Tasks 1-3.
- Produces: 28 total validated samples in `samples/manifest.json`.

- [ ] **Step 1: Register all 6 new samples in `samples/manifest.json`**
  Add entries for:
  - `javascript_dijkstra_clean` (Good, 100.0, Grade A, Scenario: `2. Graph Dijkstra Shortest Path Algorithm Complexity & Control Flow`)
  - `javascript_dijkstra_branchy` (Bad, Grade F, Scenario: `2. Graph Dijkstra Shortest Path Algorithm Complexity & Control Flow`)
  - `javascript_trie_clean` (Good, 100.0, Grade A, Scenario: `3. Trie Prefix Tree Data Structure OOP Cohesion & Class Size`)
  - `javascript_trie_god_class` (Bad, Grade F, Scenario: `3. Trie Prefix Tree Data Structure OOP Cohesion & Class Size`)
  - `javascript_test_hygiene_good` (Good, 100.0, Grade A, Scenario: `4. BDD Algorithmic Test Suite Hygiene & Assertion Density`)
  - `javascript_test_hygiene_bad` (Bad, Grade D, Scenario: `4. BDD Algorithmic Test Suite Hygiene & Assertion Density`)

- [ ] **Step 2: Update sample count assertion in `tests/unit/test_language_scorecard_samples.py`**
  Change `assert len(samples) == 22` to `assert len(samples) == 28`.

- [ ] **Step 3: Run the baseline test suite**
  Run: `.venv\Scripts\pytest.exe tests/unit/test_language_scorecard_samples.py -v`
  Expected: 70 passed in ~2s (28 baseline match tests + 28 findings tests + 14 scenario pairwise tests).

- [ ] **Step 4: Commit**
  ```bash
  git add samples/manifest.json tests/unit/test_language_scorecard_samples.py
  git commit -m "feat(samples): register 6 new JavaScript baseline samples in manifest"
  ```

---

### Task 5: Catalog Update & Self-Health Verification

**Files:**
- Modify: `samples/SCORECARD_BASELINES.md`

**Interfaces:**
- Consumes: Exact scorecard results and console rendering from Tasks 1-4.
- Produces: Complete human-readable catalog with all 4 JavaScript scenarios.

- [ ] **Step 1: Add summary table rows to `samples/SCORECARD_BASELINES.md`**
  Insert the 6 new sample rows under `javascript (none)` in `## Quick Summary Table`.

- [ ] **Step 2: Add detailed scenario scorecard sections to `samples/SCORECARD_BASELINES.md`**
  Add full scenario sections with ```` ```text ```` code blocks for Scenarios 2, 3, and 4 matching the exact console output.

- [ ] **Step 3: Run full repo test suite**
  Run: `.venv\Scripts\pytest.exe -v`
  Expected: 112 passed, 0 failures.

- [ ] **Step 4: Run repo code health check**
  Run: `.venv\Scripts\python.exe scripts/code_health.py scripts --fail-under 90.0`
  Expected: Overall score $\ge 95.0\%$ (Grade A).

- [ ] **Step 5: Commit**
  ```bash
  git add samples/SCORECARD_BASELINES.md
  git commit -m "docs(samples): update SCORECARD_BASELINES.md with JavaScript scenarios 2-4"
  ```
