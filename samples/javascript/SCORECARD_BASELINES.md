# JavaScript Code Health Scorecard Baselines

This catalog provides 10 functionally comparable **Good** and **Bad** verbatim real-world Vanilla JavaScript (`--lang javascript`, `--framework auto`) code sample pairs (20 files total) sourced directly from [`TheAlgorithms/JavaScript`](https://github.com/TheAlgorithms/JavaScript) and [`trekhleb/javascript-algorithms`](https://github.com/trekhleb/javascript-algorithms).

Each sample file `<filename>` has a matching `<filename>.expected.json` sidecar file and is indexed in [`manifest.json`](manifest.json).

---

## Quick Summary Table

| Profile | Scenario | Quality | Sample File | Dataset Source | LOC | SRP | Size | Comp | Clean | Sec | Score | Grade |
| :--- | :--- | :---: | :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| `javascript (auto)` | 1. Sorting Algorithm Documentation & Clean Hygiene (MergeSort vs. BubbleSort) | **GOOD** | [`good/MergeSort.js`](good/MergeSort.js) | [TheAlgorithms/JavaScript (Sorts/MergeSort.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Sorts/MergeSort.js) | 20 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `javascript (auto)` | 1. Sorting Algorithm Documentation & Clean Hygiene (MergeSort vs. BubbleSort) | **BAD** | [`bad/BubbleSort.js`](bad/BubbleSort.js) | [trekhleb/javascript-algorithms (src/algorithms/sorting/bubble-sort/BubbleSort.js)](https://github.com/trekhleb/javascript-algorithms/blob/master/src/algorithms/sorting/bubble-sort/BubbleSort.js) | 22 | 100.0 | 100.0 | 100.0 | 73.0 | 100.0 | **78.0** | **C** |
| `javascript (auto)` | 2. String Matching & Pattern Search Complexity (Rabin-Karp vs. Regex Matching) | **GOOD** | [`good/rabinKarp.js`](good/rabinKarp.js) | [trekhleb/javascript-algorithms (src/algorithms/string/rabin-karp/rabinKarp.js)](https://github.com/trekhleb/javascript-algorithms/blob/master/src/algorithms/string/rabin-karp/rabinKarp.js) | 23 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `javascript (auto)` | 2. String Matching & Pattern Search Complexity (Rabin-Karp vs. Regex Matching) | **BAD** | [`bad/regularExpressionMatching.js`](bad/regularExpressionMatching.js) | [trekhleb/javascript-algorithms (src/algorithms/string/regular-expression-matching/regularExpressionMatching.js)](https://github.com/trekhleb/javascript-algorithms/blob/master/src/algorithms/string/regular-expression-matching/regularExpressionMatching.js) | 48 | 100.0 | 48.5 | 21.5 | 100.0 | 100.0 | **26.5** | **F** |
| `javascript (auto)` | 3. Binary Heap Priority Queue OOP Cohesion & Method Count | **GOOD** | [`good/BinaryHeap.js`](good/BinaryHeap.js) | [TheAlgorithms/JavaScript (Data-Structures/Heap/BinaryHeap.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Data-Structures/Heap/BinaryHeap.js) | 66 | 100.0 | 100.0 | 99.6 | 100.0 | 100.0 | **99.9** | **A** |
| `javascript (auto)` | 3. Binary Heap Priority Queue OOP Cohesion & Method Count | **BAD** | [`bad/Heap.js`](bad/Heap.js) | [trekhleb/javascript-algorithms (src/data-structures/heap/Heap.js)](https://github.com/trekhleb/javascript-algorithms/blob/master/src/data-structures/heap/Heap.js) | 142 | 55.4 | 100.0 | 78.8 | 100.0 | 100.0 | **60.4** | **D** |
| `javascript (auto)` | 4. Range-Query Tree OOP Cohesion (FenwickTree vs. SegmentTree) | **GOOD** | [`good/FenwickTree.js`](good/FenwickTree.js) | [TheAlgorithms/JavaScript (Trees/FenwickTree.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Trees/FenwickTree.js) | 27 | 100.0 | 100.0 | 100.0 | 90.7 | 100.0 | **98.6** | **A** |
| `javascript (auto)` | 4. Range-Query Tree OOP Cohesion (FenwickTree vs. SegmentTree) | **BAD** | [`bad/SegmentTree.js`](bad/SegmentTree.js) | [TheAlgorithms/JavaScript (Data-Structures/Tree/SegmentTree.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Data-Structures/Tree/SegmentTree.js) | 42 | 70.0 | 100.0 | 100.0 | 90.8 | 100.0 | **75.0** | **C** |
| `javascript (auto)` | 5. Cipher Encoding Helper Decomposition vs. Monolithic Encoder | **GOOD** | [`good/AffineCipher.js`](good/AffineCipher.js) | [TheAlgorithms/JavaScript (Ciphers/AffineCipher.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Ciphers/AffineCipher.js) | 51 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `javascript (auto)` | 5. Cipher Encoding Helper Decomposition vs. Monolithic Encoder | **BAD** | [`bad/MorseCode.js`](bad/MorseCode.js) | [TheAlgorithms/JavaScript (Ciphers/MorseCode.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Ciphers/MorseCode.js) | 76 | 82.0 | 0.0 | 100.0 | 100.0 | 100.0 | **5.0** | **F** |
| `javascript (auto)` | 6. Sorting Algorithm Decomposition vs. Monolithic IntroSort | **GOOD** | [`good/QuickSortRecursive.js`](good/QuickSortRecursive.js) | [TheAlgorithms/JavaScript (Sorts/QuickSortRecursive.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Sorts/QuickSortRecursive.js) | 30 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `javascript (auto)` | 6. Sorting Algorithm Decomposition vs. Monolithic IntroSort | **BAD** | [`bad/IntroSort.js`](bad/IntroSort.js) | [TheAlgorithms/JavaScript (Sorts/IntroSort.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Sorts/IntroSort.js) | 182 | 85.0 | 28.3 | 28.7 | 100.0 | 100.0 | **33.3** | **F** |
| `javascript (auto)` | 7. Graph Traversal Concern Separation & External Call Fan-Out | **GOOD** | [`good/depthFirstSearch.js`](good/depthFirstSearch.js) | [trekhleb/javascript-algorithms (src/algorithms/graph/depth-first-search/depthFirstSearch.js)](https://github.com/trekhleb/javascript-algorithms/blob/master/src/algorithms/graph/depth-first-search/depthFirstSearch.js) | 33 | 100.0 | 100.0 | 97.6 | 100.0 | 100.0 | **99.5** | **A** |
| `javascript (auto)` | 7. Graph Traversal Concern Separation & External Call Fan-Out | **BAD** | [`bad/eulerianPath.js`](bad/eulerianPath.js) | [trekhleb/javascript-algorithms (src/algorithms/graph/eulerian-path/eulerianPath.js)](https://github.com/trekhleb/javascript-algorithms/blob/master/src/algorithms/graph/eulerian-path/eulerianPath.js) | 52 | 67.0 | 60.0 | 79.0 | 100.0 | 100.0 | **65.0** | **D** |
| `javascript (auto)` | 8. Numerical Math Algorithm Cyclomatic & Cognitive Complexity | **GOOD** | [`good/FigurateNumber.js`](good/FigurateNumber.js) | [TheAlgorithms/JavaScript (Maths/FigurateNumber.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Maths/FigurateNumber.js) | 41 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `javascript (auto)` | 8. Numerical Math Algorithm Cyclomatic & Cognitive Complexity | **BAD** | [`bad/SimpsonIntegration.js`](bad/SimpsonIntegration.js) | [TheAlgorithms/JavaScript (Maths/SimpsonIntegration.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Maths/SimpsonIntegration.js) | 38 | 100.0 | 82.0 | 39.5 | 92.0 | 100.0 | **44.5** | **F** |
| `javascript (auto)` | 9. BDD Unit Test Assertion Density & Hygiene (Knapsack Suite) | **GOOD** | [`good/Knapsack.test.js`](good/Knapsack.test.js) | [trekhleb/javascript-algorithms (src/algorithms/sets/knapsack-problem/__test__/Knapsack.test.js)](https://github.com/trekhleb/javascript-algorithms/blob/master/src/algorithms/sets/knapsack-problem/__test__/Knapsack.test.js) | 127 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `javascript (auto)` | 9. BDD Unit Test Assertion Density & Hygiene (Knapsack Suite) | **BAD** | [`bad/KnapsackItem.test.js`](bad/KnapsackItem.test.js) | [trekhleb/javascript-algorithms (src/algorithms/sets/knapsack-problem/__test__/KnapsackItem.test.js)](https://github.com/trekhleb/javascript-algorithms/blob/master/src/algorithms/sets/knapsack-problem/__test__/KnapsackItem.test.js) | 29 | 100.0 | 100.0 | 100.0 | 70.0 | 100.0 | **75.0** | **C** |
| `javascript (auto)` | 10. Graph Algorithm Test Suite Decomposition & Test Function Size | **GOOD** | [`good/articulationPoints.test.js`](good/articulationPoints.test.js) | [trekhleb/javascript-algorithms (src/algorithms/graph/articulation-points/__test__/articulationPoints.test.js)](https://github.com/trekhleb/javascript-algorithms/blob/master/src/algorithms/graph/articulation-points/__test__/articulationPoints.test.js) | 190 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `javascript (auto)` | 10. Graph Algorithm Test Suite Decomposition & Test Function Size | **BAD** | [`bad/breadthFirstSearch.test.js`](bad/breadthFirstSearch.test.js) | [trekhleb/javascript-algorithms (src/algorithms/graph/breadth-first-search/__test__/breadthFirstSearch.test.js)](https://github.com/trekhleb/javascript-algorithms/blob/master/src/algorithms/graph/breadth-first-search/__test__/breadthFirstSearch.test.js) | 146 | 100.0 | 70.0 | 100.0 | 100.0 | 100.0 | **75.0** | **C** |

---

## Detailed Scenario Scorecards

### JAVASCRIPT (`--lang javascript`) — 1. Sorting Algorithm Documentation & Clean Hygiene (MergeSort vs. BubbleSort)

#### Good Baseline: [`good/MergeSort.js`](good/MergeSort.js) ([sidecar JSON](good/MergeSort.js.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/JavaScript (Sorts/MergeSort.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Sorts/MergeSort.js) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 2
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/MergeSort.js           src      20    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/MergeSort.js:18 merge          13   4    3   2   2  100.0   A
samples/javascript/good/MergeSort.js:40 mergeSort       7   2    1   1   1  100.0   A
```

#### Bad Baseline: [`bad/BubbleSort.js`](bad/BubbleSort.js) ([sidecar JSON](bad/BubbleSort.js.expected.json))

- **Upstream Dataset / Benchmark:** [trekhleb/javascript-algorithms (src/algorithms/sorting/bubble-sort/BubbleSort.js)](https://github.com/trekhleb/javascript-algorithms/blob/master/src/algorithms/sorting/bubble-sort/BubbleSort.js) (`MIT`)
- **Expected Scorecard:** `Composite 78.0/100 (Grade C)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 73.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 78.0/100 (Grade C) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 73.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/BubbleSort.js           src      22    - 100.0 100.0 100.0  73.0 100.0   78.0   C

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/BubbleSort.js:3 BubbleSort     21    1     1    5   78.0   C
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/BubbleSort.js:4 BubbleSort.so   19   5    8   1   3   98.2   A
    - Clean: missing public docstring (-10.0 pts)
    - Clean: 1 unannotated parameter(s) without default values (originalArray) (-2.0 pts)
```

---

### JAVASCRIPT (`--lang javascript`) — 2. String Matching & Pattern Search Complexity (Rabin-Karp vs. Regex Matching)

#### Good Baseline: [`good/rabinKarp.js`](good/rabinKarp.js) ([sidecar JSON](good/rabinKarp.js.expected.json))

- **Upstream Dataset / Benchmark:** [trekhleb/javascript-algorithms (src/algorithms/string/rabin-karp/rabinKarp.js)](https://github.com/trekhleb/javascript-algorithms/blob/master/src/algorithms/string/rabin-karp/rabinKarp.js) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/rabinKarp.js           src      23    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/rabinKarp.js:8 rabinKarp       22   5    5   2   2  100.0   A
```

#### Bad Baseline: [`bad/regularExpressionMatching.js`](bad/regularExpressionMatching.js) ([sidecar JSON](bad/regularExpressionMatching.js.expected.json))

- **Upstream Dataset / Benchmark:** [trekhleb/javascript-algorithms (src/algorithms/string/regular-expression-matching/regularExpressionMatching.js)](https://github.com/trekhleb/javascript-algorithms/blob/master/src/algorithms/string/regular-expression-matching/regularExpressionMatching.js) (`MIT`)
- **Expected Scorecard:** `Composite 26.5/100 (Grade F)` — `SRP: 100.0` | `Size: 48.5` | `Complexity: 21.5` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 26.5/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 48.5 | Complexity: 21.5 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/regularExpressionMatching.js src      48    - 100.0  48.5  21.5 100.0 100.0   26.5   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/regularExpressionMatching.js:   46  13   23   2   5   26.5   F
    - Size: LOC=46 (>25) (-31.5 pts)
    - Size: nesting depth=5 (>3) (-20.0 pts)
    - Complexity: CC=13 (>5) (-41.0 pts)
    - Complexity: cognitive=23 (>8) (-37.5 pts)
```

---

### JAVASCRIPT (`--lang javascript`) — 3. Binary Heap Priority Queue OOP Cohesion & Method Count

#### Good Baseline: [`good/BinaryHeap.js`](good/BinaryHeap.js) ([sidecar JSON](good/BinaryHeap.js.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/JavaScript (Data-Structures/Heap/BinaryHeap.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Data-Structures/Heap/BinaryHeap.js) (`MIT`)
- **Expected Scorecard:** `Composite 99.9/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 99.6` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 99.9/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 11
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 99.6 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/BinaryHeap.js          src      66    - 100.0 100.0  99.6 100.0 100.0   99.9   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/BinaryHeap.js:8 BinaryHeap    63    9     1   17   99.9   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/BinaryHeap.js:76 BinaryHeap.   18   6    7   1   2   99.2   A
    - Complexity: CC=6 (>5) (-4.0 pts)
samples/javascript/good/BinaryHeap.js:14 BinaryHeap.    4   1    0   1   0  100.0   A
samples/javascript/good/BinaryHeap.js:32 BinaryHeap.    4   1    0   1   0  100.0   A
samples/javascript/good/BinaryHeap.js:41 BinaryHeap.    3   1    0   0   0  100.0   A
samples/javascript/good/BinaryHeap.js:49 BinaryHeap.    3   1    0   0   0  100.0   A
samples/javascript/good/BinaryHeap.js:58 BinaryHeap.   11   3    1   1   1  100.0   A
samples/javascript/good/BinaryHeap.js:101 BinaryHeap    3   1    0   0   0  100.0   A
samples/javascript/good/BinaryHeap.js:109 BinaryHeap    9   2    1   0   1  100.0   A
samples/javascript/good/BinaryHeap.js:127 BinaryHeap    6   1    0   2   0  100.0   A
samples/javascript/good/BinaryHeap.js:141 minHeapCom    1   1    0   2   0  100.0   A
samples/javascript/good/BinaryHeap.js:149 maxHeapCom    1   1    0   2   0  100.0   A
```

#### Bad Baseline: [`bad/Heap.js`](bad/Heap.js) ([sidecar JSON](bad/Heap.js.expected.json))

- **Upstream Dataset / Benchmark:** [trekhleb/javascript-algorithms (src/data-structures/heap/Heap.js)](https://github.com/trekhleb/javascript-algorithms/blob/master/src/data-structures/heap/Heap.js) (`MIT`)
- **Expected Scorecard:** `Composite 60.4/100 (Grade D)` — `SRP: 55.4` | `Size: 100.0` | `Complexity: 78.8` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 60.4/100 (Grade D) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 21
Dimensions -> SRP: 55.4 | Size: 100.0 | Complexity: 78.8 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/Heap.js                 src     142    -  55.4 100.0  78.8 100.0 100.0   60.4   D

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/Heap.js:6 Heap                141   21     1   39   60.4   D
    - SRP: methods=21 (>10) (-44.0 pts)
    - Complexity: total class CC=39 (>25) (-21.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/Heap.js:150 Heap.remove         24   6    6   2   3   97.4   A
    - SRP: high external call fan-out=8 (>6) (-6.0 pts)
    - Complexity: CC=6 (>5) (-4.0 pts)
samples/javascript/bad/Heap.js:241 Heap.heapifyDown    22   5    5   1   2   98.2   A
    - SRP: high external call fan-out=8 (>6) (-6.0 pts)
samples/javascript/bad/Heap.js:11 Heap.constructor      7   2    1   1   1  100.0   A
samples/javascript/bad/Heap.js:25 Heap.getLeftChildI    3   1    0   1   0  100.0   A
samples/javascript/bad/Heap.js:33 Heap.getRightChild    3   1    0   1   0  100.0   A
samples/javascript/bad/Heap.js:41 Heap.getParentInde    3   1    0   1   0  100.0   A
samples/javascript/bad/Heap.js:49 Heap.hasParent        3   1    0   1   0  100.0   A
samples/javascript/bad/Heap.js:57 Heap.hasLeftChild     3   1    0   1   0  100.0   A
samples/javascript/bad/Heap.js:65 Heap.hasRightChild    3   1    0   1   0  100.0   A
samples/javascript/bad/Heap.js:73 Heap.leftChild        3   1    0   1   0  100.0   A
samples/javascript/bad/Heap.js:81 Heap.rightChild       3   1    0   1   0  100.0   A
samples/javascript/bad/Heap.js:89 Heap.parent           3   1    0   1   0  100.0   A
samples/javascript/bad/Heap.js:97 Heap.swap             5   1    0   2   0  100.0   A
samples/javascript/bad/Heap.js:106 Heap.peek            6   2    1   0   1  100.0   A
samples/javascript/bad/Heap.js:117 Heap.poll           12   3    2   0   1  100.0   A
samples/javascript/bad/Heap.js:139 Heap.add             5   1    0   1   0  100.0   A
samples/javascript/bad/Heap.js:194 Heap.find            9   3    3   2   2  100.0   A
samples/javascript/bad/Heap.js:209 Heap.isEmpty         3   1    0   0   0  100.0   A
samples/javascript/bad/Heap.js:216 Heap.toString        3   1    0   0   0  100.0   A
samples/javascript/bad/Heap.js:223 Heap.heapifyUp      10   4    1   1   1  100.0   A
samples/javascript/bad/Heap.js:280 Heap.pairIsInCorr    6   1    0   2   0  100.0   A
```

---

### JAVASCRIPT (`--lang javascript`) — 4. Range-Query Tree OOP Cohesion (FenwickTree vs. SegmentTree)

#### Good Baseline: [`good/FenwickTree.js`](good/FenwickTree.js) ([sidecar JSON](good/FenwickTree.js.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/JavaScript (Trees/FenwickTree.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Trees/FenwickTree.js) (`MIT`)
- **Expected Scorecard:** `Composite 98.6/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 90.7` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 98.6/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 3
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 90.7 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/FenwickTree.js         src      27    - 100.0 100.0 100.0  90.7 100.0   98.6   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/FenwickTree.js:7 FenwickTr    26    3     1    7   98.6   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/FenwickTree.js:17 FenwickTre    7   2    1   4   1   98.0   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 4 unannotated parameter(s) without default values (feneickArray, n, index) (-8.0 pts)
samples/javascript/good/FenwickTree.js:25 FenwickTre    9   2    1   2   1   98.7   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 2 unannotated parameter(s) without default values (feneickArray, index) (-4.0 pts)
samples/javascript/good/FenwickTree.js:8 FenwickTree    8   3    2   3   1   99.1   A
    - Clean: 3 unannotated parameter(s) without default values (feneickArray, array, n) (-6.0 pts)
```

#### Bad Baseline: [`bad/SegmentTree.js`](bad/SegmentTree.js) ([sidecar JSON](bad/SegmentTree.js.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/JavaScript (Data-Structures/Tree/SegmentTree.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Data-Structures/Tree/SegmentTree.js) (`MIT`)
- **Expected Scorecard:** `Composite 75.0/100 (Grade C)` — `SRP: 70.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 90.8` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 75.0/100 (Grade C) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 4
Dimensions -> SRP: 70.0 | Size: 100.0 | Complexity: 100.0 | Clean: 90.8 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/SegmentTree.js          src      42    -  70.0 100.0 100.0  90.8 100.0   75.0   C

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/SegmentTree.js:13 SegmentTr    41    4     3   10   75.0   C
    - SRP: LCOM4=3 disconnected method groups (-30.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/SegmentTree.js:68 SegmentTree   14   4    5   2   2   97.9   A
    - Clean: missing public docstring (-10.0 pts)
    - Clean: 2 unannotated parameter(s) without default values (left, right) (-4.0 pts)
samples/javascript/bad/SegmentTree.js:48 SegmentTree    8   2    1   2   1   98.7   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 2 unannotated parameter(s) without default values (index, value) (-4.0 pts)
samples/javascript/bad/SegmentTree.js:16 SegmentTree    6   1    0   1   0   99.0   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 1 unannotated parameter(s) without default values (arr) (-2.0 pts)
samples/javascript/bad/SegmentTree.js:31 SegmentTree    9   3    2   1   1   99.0   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 1 unannotated parameter(s) without default values (arr) (-2.0 pts)
```

---

### JAVASCRIPT (`--lang javascript`) — 5. Cipher Encoding Helper Decomposition vs. Monolithic Encoder

#### Good Baseline: [`good/AffineCipher.js`](good/AffineCipher.js) ([sidecar JSON](good/AffineCipher.js.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/JavaScript (Ciphers/AffineCipher.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Ciphers/AffineCipher.js) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 6
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/AffineCipher.js        src      51    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/AffineCipher.js:16 mod          3   1    0   2   0  100.0   A
samples/javascript/good/AffineCipher.js:26 inverseMo    5   3    3   2   2  100.0   A
samples/javascript/good/AffineCipher.js:39 isCorrect   12   5    3   3   1  100.0   A
samples/javascript/good/AffineCipher.js:60 findCharI    3   1    0   1   0  100.0   A
samples/javascript/good/AffineCipher.js:72 encrypt     11   4    6   3   3  100.0   A
samples/javascript/good/AffineCipher.js:91 decrypt     14   4    6   3   3  100.0   A
```

#### Bad Baseline: [`bad/MorseCode.js`](bad/MorseCode.js) ([sidecar JSON](bad/MorseCode.js.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/JavaScript (Ciphers/MorseCode.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Ciphers/MorseCode.js) (`MIT`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 82.0` | `Size: 0.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 82.0 | Size: 0.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/MorseCode.js            src      76    -  82.0   0.0 100.0 100.0 100.0    5.0   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/MorseCode.js:11 morse           75   3    3   3   2    5.0   F
    - SRP: high external call fan-out=12 (>6) (-18.0 pts)
    - Size: LOC=75 (>25) (-100.0 pts)
```

---

### JAVASCRIPT (`--lang javascript`) — 6. Sorting Algorithm Decomposition vs. Monolithic IntroSort

#### Good Baseline: [`good/QuickSortRecursive.js`](good/QuickSortRecursive.js) ([sidecar JSON](good/QuickSortRecursive.js.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/JavaScript (Sorts/QuickSortRecursive.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Sorts/QuickSortRecursive.js) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 2
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/QuickSortRecursive.js  src      30    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/QuickSortRecursive.js:24 qui   11   3    2   3   1  100.0   A
samples/javascript/good/QuickSortRecursive.js:45 par   18   3    3   3   2  100.0   A
```

#### Bad Baseline: [`bad/IntroSort.js`](bad/IntroSort.js) ([sidecar JSON](bad/IntroSort.js.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/JavaScript (Sorts/IntroSort.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Sorts/IntroSort.js) (`MIT`)
- **Expected Scorecard:** `Composite 33.3/100 (Grade F)` — `SRP: 85.0` | `Size: 28.3` | `Complexity: 28.7` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 33.3/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 3
Dimensions -> SRP: 85.0 | Size: 28.3 | Complexity: 28.7 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/IntroSort.js            src     182    -  85.0  28.3  28.7 100.0 100.0   33.3   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/IntroSort.js:18 introsort      129  34   34   2   2    5.0   F
    - SRP: high external call fan-out=13 (>6) (-21.0 pts)
    - Size: LOC=129 (>25) (-100.0 pts)
    - Complexity: CC=34 (>5) (-100.0 pts)
    - Complexity: cognitive=34 (>8) (-65.0 pts)
    - Complexity: returns=16 (>3) (-52.0 pts)
samples/javascript/bad/IntroSort.js:250 demo1          26   5    5   0   2   99.6   A
    - Size: LOC=26 (>25) (-1.5 pts)
samples/javascript/bad/IntroSort.js:282 demo2          26   5    5   0   2   99.6   A
    - Size: LOC=26 (>25) (-1.5 pts)
```

---

### JAVASCRIPT (`--lang javascript`) — 7. Graph Traversal Concern Separation & External Call Fan-Out

#### Good Baseline: [`good/depthFirstSearch.js`](good/depthFirstSearch.js) ([sidecar JSON](good/depthFirstSearch.js.expected.json))

- **Upstream Dataset / Benchmark:** [trekhleb/javascript-algorithms (src/algorithms/graph/depth-first-search/depthFirstSearch.js)](https://github.com/trekhleb/javascript-algorithms/blob/master/src/algorithms/graph/depth-first-search/depthFirstSearch.js) (`MIT`)
- **Expected Scorecard:** `Composite 99.5/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 97.6` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 99.5/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 3
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 97.6 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/depthFirstSearch.js    src      33    - 100.0 100.0  97.6 100.0 100.0   99.5   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/depthFirstSearch.js:17 initC   20   5    1   1   1   99.2   A
    - Complexity: returns=4 (>3) (-4.0 pts)
samples/javascript/good/depthFirstSearch.js:48 depth    9   2    1   4   1  100.0   A
samples/javascript/good/depthFirstSearch.js:65 depth    4   1    0   3   0  100.0   A
```

#### Bad Baseline: [`bad/eulerianPath.js`](bad/eulerianPath.js) ([sidecar JSON](bad/eulerianPath.js.expected.json))

- **Upstream Dataset / Benchmark:** [trekhleb/javascript-algorithms (src/algorithms/graph/eulerian-path/eulerianPath.js)](https://github.com/trekhleb/javascript-algorithms/blob/master/src/algorithms/graph/eulerian-path/eulerianPath.js) (`MIT`)
- **Expected Scorecard:** `Composite 65.0/100 (Grade D)` — `SRP: 67.0` | `Size: 60.0` | `Complexity: 79.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 65.0/100 (Grade D) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 67.0 | Size: 60.0 | Complexity: 79.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/eulerianPath.js         src      52    -  67.0  60.0  79.0 100.0 100.0   65.0   D

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/eulerianPath.js:9 eulerianPat   51   9   10   1   2   65.0   D
    - SRP: high external call fan-out=17 (>6) (-33.0 pts)
    - Size: LOC=51 (>25) (-40.0 pts)
    - Complexity: CC=9 (>5) (-16.0 pts)
    - Complexity: cognitive=10 (>8) (-5.0 pts)
```

---

### JAVASCRIPT (`--lang javascript`) — 8. Numerical Math Algorithm Cyclomatic & Cognitive Complexity

#### Good Baseline: [`good/FigurateNumber.js`](good/FigurateNumber.js) ([sidecar JSON](good/FigurateNumber.js.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/JavaScript (Maths/FigurateNumber.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Maths/FigurateNumber.js) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 4
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/FigurateNumber.js      src      41    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/FigurateNumber.js:18 isTrian   10   4    6   1   3  100.0   A
samples/javascript/good/FigurateNumber.js:34 isTetra   10   4    6   1   3  100.0   A
samples/javascript/good/FigurateNumber.js:49 isPenta   10   4    6   1   3  100.0   A
samples/javascript/good/FigurateNumber.js:65 checkAl    7   1    0   1   0  100.0   A
```

#### Bad Baseline: [`bad/SimpsonIntegration.js`](bad/SimpsonIntegration.js) ([sidecar JSON](bad/SimpsonIntegration.js.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/JavaScript (Maths/SimpsonIntegration.js)](https://github.com/TheAlgorithms/JavaScript/blob/master/Maths/SimpsonIntegration.js) (`MIT`)
- **Expected Scorecard:** `Composite 44.5/100 (Grade F)` — `SRP: 100.0` | `Size: 82.0` | `Complexity: 39.5` | `Clean: 92.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 44.5/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 82.0 | Complexity: 39.5 | Clean: 92.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/SimpsonIntegration.js   src      38    - 100.0  82.0  39.5  92.0 100.0   44.5   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/SimpsonIntegration.js:24 inte   37  14   13   4   3   44.5   F
    - Size: LOC=37 (>25) (-18.0 pts)
    - Complexity: CC=14 (>5) (-48.0 pts)
    - Complexity: cognitive=13 (>8) (-12.5 pts)
    - Clean: 4 unannotated parameter(s) without default values (N, a, b) (-8.0 pts)
```

---

### JAVASCRIPT (`--lang javascript`) — 9. BDD Unit Test Assertion Density & Hygiene (Knapsack Suite)

#### Good Baseline: [`good/Knapsack.test.js`](good/Knapsack.test.js) ([sidecar JSON](good/Knapsack.test.js.expected.json))

- **Upstream Dataset / Benchmark:** [trekhleb/javascript-algorithms (src/algorithms/sets/knapsack-problem/__test__/Knapsack.test.js)](https://github.com/trekhleb/javascript-algorithms/blob/master/src/algorithms/sets/knapsack-problem/__test__/Knapsack.test.js) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 0, test: 1) | Classes: 0 | Functions/Methods: 7
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/Knapsack.test.js       test    127    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/Knapsack.test.js:5 test: sho   16   1    0   0   0  100.0   A
samples/javascript/good/Knapsack.test.js:26 test: sh   16   1    0   0   0  100.0   A
samples/javascript/good/Knapsack.test.js:47 test: sh   14   1    0   0   0  100.0   A
samples/javascript/good/Knapsack.test.js:66 test: sh   19   1    0   0   0  100.0   A
samples/javascript/good/Knapsack.test.js:90 test: sh   20   1    0   0   0  100.0   A
samples/javascript/good/Knapsack.test.js:115 test: s   18   1    0   0   0  100.0   A
samples/javascript/good/Knapsack.test.js:138 test: s   20   1    0   0   0  100.0   A
```

#### Bad Baseline: [`bad/KnapsackItem.test.js`](bad/KnapsackItem.test.js) ([sidecar JSON](bad/KnapsackItem.test.js.expected.json))

- **Upstream Dataset / Benchmark:** [trekhleb/javascript-algorithms (src/algorithms/sets/knapsack-problem/__test__/KnapsackItem.test.js)](https://github.com/trekhleb/javascript-algorithms/blob/master/src/algorithms/sets/knapsack-problem/__test__/KnapsackItem.test.js) (`MIT`)
- **Expected Scorecard:** `Composite 75.0/100 (Grade C)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 70.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 75.0/100 (Grade C) | Files: 1 (src: 0, test: 1) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 70.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/KnapsackItem.test.js    test     29    - 100.0 100.0 100.0  70.0 100.0   75.0   C

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/KnapsackItem.test.js:4 test:    26   1    0   0   0   75.0   C
    - Clean (Test): 21 assertions in single test (>8) (-30.0 pts)
```

---

### JAVASCRIPT (`--lang javascript`) — 10. Graph Algorithm Test Suite Decomposition & Test Function Size

#### Good Baseline: [`good/articulationPoints.test.js`](good/articulationPoints.test.js) ([sidecar JSON](good/articulationPoints.test.js.expected.json))

- **Upstream Dataset / Benchmark:** [trekhleb/javascript-algorithms (src/algorithms/graph/articulation-points/__test__/articulationPoints.test.js)](https://github.com/trekhleb/javascript-algorithms/blob/master/src/algorithms/graph/articulation-points/__test__/articulationPoints.test.js) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 0, test: 1) | Classes: 0 | Functions/Methods: 7
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/articulationPoints.test.js test    190    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/good/articulationPoints.test.js:7   18   1    0   0   0  100.0   A
samples/javascript/good/articulationPoints.test.js:3   19   1    0   0   0  100.0   A
samples/javascript/good/articulationPoints.test.js:5   22   1    0   0   0  100.0   A
samples/javascript/good/articulationPoints.test.js:8   36   1    0   0   0  100.0   A
samples/javascript/good/articulationPoints.test.js:1   36   1    0   0   0  100.0   A
samples/javascript/good/articulationPoints.test.js:1   23   1    0   0   0  100.0   A
samples/javascript/good/articulationPoints.test.js:1   30   1    0   0   0  100.0   A
```

#### Bad Baseline: [`bad/breadthFirstSearch.test.js`](bad/breadthFirstSearch.test.js) ([sidecar JSON](bad/breadthFirstSearch.test.js.expected.json))

- **Upstream Dataset / Benchmark:** [trekhleb/javascript-algorithms (src/algorithms/graph/breadth-first-search/__test__/breadthFirstSearch.test.js)](https://github.com/trekhleb/javascript-algorithms/blob/master/src/algorithms/graph/breadth-first-search/__test__/breadthFirstSearch.test.js) (`MIT`)
- **Expected Scorecard:** `Composite 75.0/100 (Grade C)` — `SRP: 100.0` | `Size: 70.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 75.0/100 (Grade C) | Files: 1 (src: 0, test: 1) | Classes: 0 | Functions/Methods: 2
Dimensions -> SRP: 100.0 | Size: 70.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/breadthFirstSearch.test.js test    146    - 100.0  70.0 100.0 100.0 100.0   75.0   C

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/javascript/bad/breadthFirstSearch.test.js:7    70   3    2   0   1   75.0   C
    - Size: LOC=70 (>40) (-30.0 pts)
samples/javascript/bad/breadthFirstSearch.test.js:92   70   4    2   0   1   75.0   C
    - Size: LOC=70 (>40) (-30.0 pts)
```
