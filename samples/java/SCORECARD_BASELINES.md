# Java Code Health Scorecard Baselines

This catalog provides functionally comparable, human-inspectable **Good** and **Bad** verbatim real-world Java (`--framework none`) code samples across 10 scenarios (20 files total) from [`deepmind/code_contests`](https://huggingface.co/datasets/deepmind/code_contests) and [`TheAlgorithms/Java`](https://github.com/TheAlgorithms/Java).

Each scenario pairs a **Good** and **Bad** file solving the **same problem or performing comparable domain functionality**. Each `<filename>` has a matching `<filename>.expected.json` sidecar and is indexed in [`manifest.json`](manifest.json).

---

## Quick Summary Table

| Profile | Scenario | Quality | Sample File | Dataset Source | LOC | SRP | Size | Comp | Clean | Sec | Score | Grade |
| :--- | :--- | :---: | :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| `java (none)` | 1. Competitive Programming Contest Class Structure (Same Problem: Codeforces 1575D) | **GOOD** | [`good/DivisibleByTwentyFiveClean.java`](good/DivisibleByTwentyFiveClean.java) | [DeepMind code_contests (test split, Problem 1575_D. Divisible by Twenty-Five, Solution #57)](https://huggingface.co/datasets/deepmind/code_contests) | 132 | 100.0 | 100.0 | 100.0 | 75.0 | 100.0 | **96.2** | **A** |
| `java (none)` | 1. Competitive Programming Contest Class Structure (Same Problem: Codeforces 1575D) | **BAD** | [`bad/DivisibleByTwentyFiveGodClass.java`](bad/DivisibleByTwentyFiveGodClass.java) | [DeepMind code_contests (test split, Problem 1575_D. Divisible by Twenty-Five, Solution #45)](https://huggingface.co/datasets/deepmind/code_contests) | 611 | 0.0 | 0.0 | 0.0 | 59.1 | 100.0 | **5.0** | **F** |
| `java (none)` | 2. Method Complexity & Control Flow (Same Problem: Codeforces 1575D) | **GOOD** | [`good/DivisibleByTwentyFiveModular.java`](good/DivisibleByTwentyFiveModular.java) | [DeepMind code_contests (test split, Problem 1575_D. Divisible by Twenty-Five, Solution #46)](https://huggingface.co/datasets/deepmind/code_contests) | 79 | 100.0 | 96.5 | 93.3 | 76.7 | 100.0 | **94.3** | **A** |
| `java (none)` | 2. Method Complexity & Control Flow (Same Problem: Codeforces 1575D) | **BAD** | [`bad/DivisibleByTwentyFiveBranchy.java`](bad/DivisibleByTwentyFiveBranchy.java) | [DeepMind code_contests (test split, Problem 1575_D. Divisible by Twenty-Five, Solution #32)](https://huggingface.co/datasets/deepmind/code_contests) | 42 | 100.0 | 79.0 | 39.5 | 75.0 | 100.0 | **44.5** | **F** |
| `java (none)` | 3. Linked List Data Structure Cohesion & Method Count (TheAlgorithms/Java lists/, ~250 LOC) | **GOOD** | [`good/DoublyLinkedList.java`](good/DoublyLinkedList.java) | [TheAlgorithms/Java (src/main/java/com/thealgorithms/datastructures/lists/DoublyLinkedList.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/datastructures/lists/DoublyLinkedList.java) | 234 | 96.6 | 99.2 | 93.1 | 77.4 | 100.0 | **94.0** | **A** |
| `java (none)` | 3. Linked List Data Structure Cohesion & Method Count (TheAlgorithms/Java lists/, ~250 LOC) | **BAD** | [`bad/SinglyLinkedList.java`](bad/SinglyLinkedList.java) | [TheAlgorithms/Java (src/main/java/com/thealgorithms/datastructures/lists/SinglyLinkedList.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/datastructures/lists/SinglyLinkedList.java) | 281 | 15.7 | 66.7 | 50.2 | 98.9 | 100.0 | **20.7** | **F** |
| `java (none)` | 4. Block & Classical Cipher Implementation Size (TheAlgorithms/Java ciphers/) | **GOOD** | [`good/AffineCipher.java`](good/AffineCipher.java) | [TheAlgorithms/Java (src/main/java/com/thealgorithms/ciphers/AffineCipher.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/ciphers/AffineCipher.java) | 37 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `java (none)` | 4. Block & Classical Cipher Implementation Size (TheAlgorithms/Java ciphers/) | **BAD** | [`bad/Blowfish.java`](bad/Blowfish.java) | [TheAlgorithms/Java (src/main/java/com/thealgorithms/ciphers/Blowfish.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/ciphers/Blowfish.java) | 1149 | 99.0 | 0.0 | 100.0 | 63.9 | 100.0 | **5.0** | **F** |
| `java (none)` | 5. Ring & Sliding Window Buffer Cohesion & Attribute Count (TheAlgorithms/Java buffers/) | **GOOD** | [`good/CircularBuffer.java`](good/CircularBuffer.java) | [TheAlgorithms/Java (src/main/java/com/thealgorithms/datastructures/buffers/CircularBuffer.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/datastructures/buffers/CircularBuffer.java) | 55 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `java (none)` | 5. Ring & Sliding Window Buffer Cohesion & Attribute Count (TheAlgorithms/Java buffers/) | **BAD** | [`bad/SlidingWindowAggregator.java`](bad/SlidingWindowAggregator.java) | [TheAlgorithms/Java (src/main/java/com/thealgorithms/datastructures/buffers/SlidingWindowAggregator.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/datastructures/buffers/SlidingWindowAggregator.java) | 177 | 8.9 | 100.0 | 83.5 | 99.0 | 100.0 | **13.9** | **F** |
| `java (none)` | 6. Graph Traversal & Path Complexity (TheAlgorithms/Java graph/) | **GOOD** | [`good/TarjanBridges.java`](good/TarjanBridges.java) | [TheAlgorithms/Java (src/main/java/com/thealgorithms/graph/TarjanBridges.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/graph/TarjanBridges.java) | 57 | 100.0 | 100.0 | 98.0 | 100.0 | 100.0 | **99.6** | **A** |
| `java (none)` | 6. Graph Traversal & Path Complexity (TheAlgorithms/Java graph/) | **BAD** | [`bad/HierholzerEulerianPath.java`](bad/HierholzerEulerianPath.java) | [TheAlgorithms/Java (src/main/java/com/thealgorithms/graph/HierholzerEulerianPath.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/graph/HierholzerEulerianPath.java) | 188 | 97.0 | 92.5 | 47.7 | 94.3 | 100.0 | **52.7** | **F** |
| `java (none)` | 7. Mathematical Utility Javadocs & Cohesion (TheAlgorithms/Java maths/) | **GOOD** | [`good/ChineseRemainderTheorem.java`](good/ChineseRemainderTheorem.java) | [TheAlgorithms/Java (src/main/java/com/thealgorithms/maths/ChineseRemainderTheorem.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/maths/ChineseRemainderTheorem.java) | 42 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `java (none)` | 7. Mathematical Utility Javadocs & Cohesion (TheAlgorithms/Java maths/) | **BAD** | [`bad/DistanceFormula.java`](bad/DistanceFormula.java) | [TheAlgorithms/Java (src/main/java/com/thealgorithms/maths/DistanceFormula.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/maths/DistanceFormula.java) | 35 | 70.0 | 100.0 | 100.0 | 71.4 | 100.0 | **75.0** | **C** |
| `java (none)` | 8. String Algorithm Single-Responsibility Cohesion (TheAlgorithms/Java strings/) | **GOOD** | [`good/PermuteString.java`](good/PermuteString.java) | [TheAlgorithms/Java (src/main/java/com/thealgorithms/strings/PermuteString.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/strings/PermuteString.java) | 27 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `java (none)` | 8. String Algorithm Single-Responsibility Cohesion (TheAlgorithms/Java strings/) | **BAD** | [`bad/Anagrams.java`](bad/Anagrams.java) | [TheAlgorithms/Java (src/main/java/com/thealgorithms/strings/Anagrams.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/strings/Anagrams.java) | 87 | 31.5 | 100.0 | 100.0 | 68.2 | 100.0 | **36.5** | **F** |
| `java (none)` | 9. Binary Search Tree Implementation Size & Complexity (TheAlgorithms/Java trees/) | **GOOD** | [`good/BSTRecursive.java`](good/BSTRecursive.java) | [TheAlgorithms/Java (src/main/java/com/thealgorithms/datastructures/trees/BSTRecursive.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/datastructures/trees/BSTRecursive.java) | 73 | 100.0 | 99.2 | 98.0 | 96.4 | 100.0 | **98.9** | **A** |
| `java (none)` | 9. Binary Search Tree Implementation Size & Complexity (TheAlgorithms/Java trees/) | **BAD** | [`bad/RedBlackBST.java`](bad/RedBlackBST.java) | [TheAlgorithms/Java (src/main/java/com/thealgorithms/datastructures/trees/RedBlackBST.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/datastructures/trees/RedBlackBST.java) | 308 | 87.8 | 49.4 | 43.8 | 71.0 | 100.0 | **48.8** | **F** |
| `java (none)` | 10. JUnit 5 Sorting Test Suite Assertion Hygiene (TheAlgorithms/Java sorts/ tests) | **GOOD** | [`good/BubbleSortTest.java`](good/BubbleSortTest.java) | [TheAlgorithms/Java (src/test/java/com/thealgorithms/sorts/BubbleSortTest.java)](https://github.com/TheAlgorithms/Java/blob/master/src/test/java/com/thealgorithms/sorts/BubbleSortTest.java) | 148 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `java (none)` | 10. JUnit 5 Sorting Test Suite Assertion Hygiene (TheAlgorithms/Java sorts/ tests) | **BAD** | [`bad/InsertionSortTest.java`](bad/InsertionSortTest.java) | [TheAlgorithms/Java (src/test/java/com/thealgorithms/sorts/InsertionSortTest.java)](https://github.com/TheAlgorithms/Java/blob/master/src/test/java/com/thealgorithms/sorts/InsertionSortTest.java) | 160 | 60.0 | 100.0 | 100.0 | 89.5 | 100.0 | **65.0** | **D** |

---

## Detailed Scenario Scorecards

### JAVA (`--framework none`) — 1. Competitive Programming Contest Class Structure (Same Problem: Codeforces 1575D)

#### Good Baseline: [`good/DivisibleByTwentyFiveClean.java`](good/DivisibleByTwentyFiveClean.java) ([sidecar JSON](good/DivisibleByTwentyFiveClean.java.expected.json))

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

#### Bad Baseline: [`bad/DivisibleByTwentyFiveGodClass.java`](bad/DivisibleByTwentyFiveGodClass.java) ([sidecar JSON](bad/DivisibleByTwentyFiveGodClass.java.expected.json))

- **Upstream Dataset / Benchmark:** [DeepMind code_contests (test split, Problem 1575_D. Divisible by Twenty-Five, Solution #45)](https://huggingface.co/datasets/deepmind/code_contests) (`CC-BY-4.0`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 0.0` | `Size: 0.0` | `Complexity: 0.0` | `Clean: 59.1` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 69
Dimensions -> SRP: 0.0 | Size: 0.0 | Complexity: 0.0 | Clean: 59.1 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/DivisibleByTwentyFiveGodClass.java src     611    -   0.0   0.0   0.0  59.1 100.0    5.0   F
    - Size: file LOC=611 (>350) (-40.2 pts)
    - Clean (DRY): DRY-001 (type1, 90 toks, 14 LOC) L631-645 in Main.prime matches samples/java/bad/DivisibleByTwentyFiveGodClass.java:646-660 (Main.prime) (-5.0 pts)
    - Clean (DRY): DRY-002 (type2, 39 toks, 6 LOC) L364-369 in Main.max matches samples/java/bad/DivisibleByTwentyFiveGodClass.java:371-376 (Main.min), samples/java/bad/DivisibleByTwentyFiveGodClass.java:378-383 (Main.max), samples/java/bad/DivisibleByTwentyFiveGodClass.java:385-390 (Main.min) (-12.0 pts)
    - Clean (DRY): DRY-003 (type1, 55 toks, 11 LOC) L608-618 in Main.hash matches samples/java/bad/DivisibleByTwentyFiveGodClass.java:620-630 (Main.tree) (-5.0 pts)
    - Clean (DRY): DRY-004 (type3, 88.7%, 53 toks, 11 LOC) L502-515 in Main.power matches samples/java/bad/DivisibleByTwentyFiveGodClass.java:523-535 (Main.power) (-3.0 pts)
    - Clean (DRY): DRY-005 (type1, 94 toks, 9 LOC) L433-441 in Main.fill matches samples/java/bad/DivisibleByTwentyFiveGodClass.java:456-464 (Main.fill) (-5.0 pts)
    - Clean (DRY): DRY-006 (type3, 73.8%, 35 toks, 6 LOC) L283-288 in Main.input matches samples/java/bad/DivisibleByTwentyFiveGodClass.java:290-295 (Main.inputL), samples/java/bad/DivisibleByTwentyFiveGodClass.java:297-302 (Main.inputS) (-6.0 pts)
    - Clean (DRY): DRY-007 (type3, 87.0%, 60 toks, 8 LOC) L232-239 in Main.upper matches samples/java/bad/DivisibleByTwentyFiveGodClass.java:249-256 (Main.lower) (-3.0 pts)
    - Clean (DRY): DRY-008 (type1, 75 toks, 7 LOC) L405-411 in Main.suffix matches samples/java/bad/DivisibleByTwentyFiveGodClass.java:412-418 (Main.suffix) (-5.0 pts)
    - Clean (DRY): DRY-009 (type1, 65 toks, 7 LOC) L391-397 in Main.prefix matches samples/java/bad/DivisibleByTwentyFiveGodClass.java:398-404 (Main.prefix) (-5.0 pts)
    - Clean (DRY): DRY-010 (type1, 65 toks, 7 LOC) L426-432 in Main.fill matches samples/java/bad/DivisibleByTwentyFiveGodClass.java:449-455 (Main.fill) (-5.0 pts)
    - Clean (DRY): DRY-011 (type3, 84.9%, 59 toks, 7 LOC) L319-326 in Main.reverse matches samples/java/bad/DivisibleByTwentyFiveGodClass.java:329-336 (Main.reverse) (-3.0 pts)
    - Clean (DRY): DRY-012 (type1, 53 toks, 7 LOC) L78-84 in Main.go matches samples/java/bad/DivisibleByTwentyFiveGodClass.java:91-97 (Main.go) (-5.0 pts)
    - Clean (DRY): DRY-013 (type3, 98.8%, 47 toks, 7 LOC) L577-583 in Main.sort matches samples/java/bad/DivisibleByTwentyFiveGodClass.java:588-594 (Main.sort) (-3.0 pts)
    - Clean (DRY): DRY-014 (type2, 40 toks, 6 LOC) L199-204 in Main.sum matches samples/java/bad/DivisibleByTwentyFiveGodClass.java:210-215 (Main.sum1) (-4.0 pts)
    - Clean (DRY): DRY-015 (type3, 71.1%, 38 toks, 6 LOC) L269-274 in Main.copy matches samples/java/bad/DivisibleByTwentyFiveGodClass.java:276-281 (Main.copy) (-3.0 pts)
    - Clean (DRY): duplication_ratio=22.3% (>10.0%) (-6.1 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 136/611 (22.3%) | DRY Score: 65.0/100 | Clone Groups: 15 (T1: 7, T2: 2, T3: 6 | intra: 15, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type1  100.0% intra_file     14 samples/java/bad/DivisibleByTwentyFiveGodClass.java:L631-645, samples/java/bad/DivisibleByTwentyFiveGodClass.java:L646-660
DRY-002  type2  100.0% intra_file      6 samples/java/bad/DivisibleByTwentyFiveGodClass.java:L364-369, samples/java/bad/DivisibleByTwentyFiveGodClass.java:L371-376, samples/java/bad/DivisibleByTwentyFiveGodClass.java:L378-383 (+1 more)
DRY-003  type1  100.0% intra_file     11 samples/java/bad/DivisibleByTwentyFiveGodClass.java:L608-618, samples/java/bad/DivisibleByTwentyFiveGodClass.java:L620-630
DRY-004  type3   88.7% intra_file     11 samples/java/bad/DivisibleByTwentyFiveGodClass.java:L502-515, samples/java/bad/DivisibleByTwentyFiveGodClass.java:L523-535
DRY-005  type1  100.0% intra_file      9 samples/java/bad/DivisibleByTwentyFiveGodClass.java:L433-441, samples/java/bad/DivisibleByTwentyFiveGodClass.java:L456-464
DRY-006  type3   73.8% intra_file      6 samples/java/bad/DivisibleByTwentyFiveGodClass.java:L283-288, samples/java/bad/DivisibleByTwentyFiveGodClass.java:L290-295, samples/java/bad/DivisibleByTwentyFiveGodClass.java:L297-302
DRY-007  type3   87.0% intra_file      8 samples/java/bad/DivisibleByTwentyFiveGodClass.java:L232-239, samples/java/bad/DivisibleByTwentyFiveGodClass.java:L249-256
DRY-008  type1  100.0% intra_file      7 samples/java/bad/DivisibleByTwentyFiveGodClass.java:L405-411, samples/java/bad/DivisibleByTwentyFiveGodClass.java:L412-418
DRY-009  type1  100.0% intra_file      7 samples/java/bad/DivisibleByTwentyFiveGodClass.java:L391-397, samples/java/bad/DivisibleByTwentyFiveGodClass.java:L398-404
DRY-010  type1  100.0% intra_file      7 samples/java/bad/DivisibleByTwentyFiveGodClass.java:L426-432, samples/java/bad/DivisibleByTwentyFiveGodClass.java:L449-455
DRY-011  type3   84.9% intra_file      7 samples/java/bad/DivisibleByTwentyFiveGodClass.java:L319-326, samples/java/bad/DivisibleByTwentyFiveGodClass.java:L329-336
DRY-012  type1  100.0% intra_file      7 samples/java/bad/DivisibleByTwentyFiveGodClass.java:L78-84, samples/java/bad/DivisibleByTwentyFiveGodClass.java:L91-97
DRY-013  type3   98.8% intra_file      7 samples/java/bad/DivisibleByTwentyFiveGodClass.java:L577-583, samples/java/bad/DivisibleByTwentyFiveGodClass.java:L588-594
DRY-014  type2  100.0% intra_file      6 samples/java/bad/DivisibleByTwentyFiveGodClass.java:L199-204, samples/java/bad/DivisibleByTwentyFiveGodClass.java:L210-215
DRY-015  type3   71.1% intra_file      6 samples/java/bad/DivisibleByTwentyFiveGodClass.java:L269-274, samples/java/bad/DivisibleByTwentyFiveGodClass.java:L276-281

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

#### Good Baseline: [`good/DivisibleByTwentyFiveModular.java`](good/DivisibleByTwentyFiveModular.java) ([sidecar JSON](good/DivisibleByTwentyFiveModular.java.expected.json))

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

#### Bad Baseline: [`bad/DivisibleByTwentyFiveBranchy.java`](bad/DivisibleByTwentyFiveBranchy.java) ([sidecar JSON](bad/DivisibleByTwentyFiveBranchy.java.expected.json))

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

#### Good Baseline: [`good/DoublyLinkedList.java`](good/DoublyLinkedList.java) ([sidecar JSON](good/DoublyLinkedList.java.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Java (src/main/java/com/thealgorithms/datastructures/lists/DoublyLinkedList.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/datastructures/lists/DoublyLinkedList.java) (`MIT`)
- **Expected Scorecard:** `Composite 94.0/100 (Grade A)` — `SRP: 96.6` | `Size: 99.2` | `Complexity: 93.1` | `Clean: 77.4` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 94.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 3 | Functions/Methods: 19
Dimensions -> SRP: 96.6 | Size: 99.2 | Complexity: 93.1 | Clean: 77.4 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/DoublyLinkedList.java        src     234    -  96.6  99.2  93.1  77.4 100.0   94.0   A
    - Clean (DRY): DRY-001 (type3, 86.8%, 76 toks, 11 LOC) L131-143 in Link.main matches samples/java/good/DoublyLinkedList.java:148-153 (Link.main) (-3.0 pts)
    - Clean (DRY): DRY-002 (type2, 45 toks, 11 LOC) L260-272 in LinkOperations.deleteHead matches samples/java/good/DoublyLinkedList.java:279-290 (LinkOperations.deleteTail) (-4.0 pts)
    - Clean (DRY): DRY-003 (type2, 47 toks, 10 LOC) L309-318 in LinkOperations.delete matches samples/java/good/DoublyLinkedList.java:351-360 (LinkOperations.deleteNode) (-4.0 pts)
    - Clean (DRY): DRY-004 (type3, 78.4%, 51 toks, 8 LOC) L140-150 in Link.main matches samples/java/good/DoublyLinkedList.java:155-163 (Link.main) (-3.0 pts)
    - Clean (DRY): DRY-005 (type2, 40 toks, 8 LOC) L66-73 in DoublyLinkedList.display matches samples/java/good/DoublyLinkedList.java:78-85 (DoublyLinkedList.displayBackwards) (-4.0 pts)
    - Clean (DRY): duplication_ratio=17.9% (>10.0%) (-4.0 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 42/234 (17.9%) | DRY Score: 78.0/100 | Clone Groups: 5 (T1: 0, T2: 3, T3: 2 | intra: 5, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type3   86.8% intra_file     11 samples/java/good/DoublyLinkedList.java:L131-143, samples/java/good/DoublyLinkedList.java:L148-153
DRY-002  type2  100.0% intra_file     11 samples/java/good/DoublyLinkedList.java:L260-272, samples/java/good/DoublyLinkedList.java:L279-290
DRY-003  type2  100.0% intra_file     10 samples/java/good/DoublyLinkedList.java:L309-318, samples/java/good/DoublyLinkedList.java:L351-360
DRY-004  type3   78.4% intra_file      8 samples/java/good/DoublyLinkedList.java:L140-150, samples/java/good/DoublyLinkedList.java:L155-163
DRY-005  type2  100.0% intra_file      8 samples/java/good/DoublyLinkedList.java:L66-73, samples/java/good/DoublyLinkedList.java:L78-85

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

#### Bad Baseline: [`bad/SinglyLinkedList.java`](bad/SinglyLinkedList.java) ([sidecar JSON](bad/SinglyLinkedList.java.expected.json))

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

### JAVA (`--framework none`) — 4. Block & Classical Cipher Implementation Size (TheAlgorithms/Java ciphers/)

#### Good Baseline: [`good/AffineCipher.java`](good/AffineCipher.java) ([sidecar JSON](good/AffineCipher.java.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Java (src/main/java/com/thealgorithms/ciphers/AffineCipher.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/ciphers/AffineCipher.java) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 3
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/AffineCipher.java            src      37    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/AffineCipher.java:21 AffineCiphe    37    3     1    9  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/AffineCipher.java:22 AffineCipher.    2   1    0   0   0  100.0   A
samples/java/good/AffineCipher.java:35 AffineCipher.   11   3    2   1   1  100.0   A
samples/java/good/AffineCipher.java:58 AffineCipher.   20   5    4   1   1  100.0   A
```

#### Bad Baseline: [`bad/Blowfish.java`](bad/Blowfish.java) ([sidecar JSON](bad/Blowfish.java.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Java (src/main/java/com/thealgorithms/ciphers/Blowfish.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/ciphers/Blowfish.java) (`MIT`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 99.0` | `Size: 0.0` | `Complexity: 100.0` | `Clean: 63.9` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 9
Dimensions -> SRP: 99.0 | Size: 0.0 | Complexity: 100.0 | Clean: 63.9 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/Blowfish.java                 src    1149    -  99.0   0.0 100.0  63.9 100.0    5.0   F
    - Size: file LOC=1149 (>350) (-100.0 pts)
    - Clean (DRY): DRY-001 (type2, 1030 toks, 516 LOC) L15-530 in <module> matches samples/java/bad/Blowfish.java:531-1046 (<module>) (-4.0 pts)
    - Clean (DRY): DRY-002 (type2, 50 toks, 25 LOC) L16-40 in <module> matches samples/java/bad/Blowfish.java:41-65 (<module>), samples/java/bad/Blowfish.java:66-90 (<module>) (-8.0 pts)
    - Clean (DRY): DRY-003 (type3, 94.7%, 66 toks, 9 LOC) L1209-1219 in Blowfish.encrypt matches samples/java/bad/Blowfish.java:1233-1243 (Blowfish.decrypt) (-3.0 pts)
    - Clean (DRY): duplication_ratio=50.0% (>10.0%) (-20.0 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 575/1149 (50.0%) | DRY Score: 65.0/100 | Clone Groups: 3 (T1: 0, T2: 2, T3: 1 | intra: 3, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type2  100.0% intra_file    516 samples/java/bad/Blowfish.java:L15-530, samples/java/bad/Blowfish.java:L531-1046
DRY-002  type2  100.0% intra_file     25 samples/java/bad/Blowfish.java:L16-40, samples/java/bad/Blowfish.java:L41-65, samples/java/bad/Blowfish.java:L66-90
DRY-003  type3   94.7% intra_file      9 samples/java/bad/Blowfish.java:L1209-1219, samples/java/bad/Blowfish.java:L1233-1243

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/Blowfish.java:11 Blowfish          1149    9     1   16    5.0   F
    - Size: class LOC=1149 (>200) (-100.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/Blowfish.java:1080 Blowfish.hexToBi   14   2    1   1   1   98.2   A
    - SRP: high external call fan-out=8 (>6) (-6.0 pts)
samples/java/bad/Blowfish.java:1121 Blowfish.xor       10   2    1   2   1   99.1   A
    - SRP: high external call fan-out=7 (>6) (-3.0 pts)
samples/java/bad/Blowfish.java:1170 Blowfish.keyGene    7   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/Blowfish.java:1181 Blowfish.round     10   1    0   2   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/Blowfish.java:1104 Blowfish.binToHe    8   2    1   1   1  100.0   A
samples/java/bad/Blowfish.java:1140 Blowfish.addBin     9   1    0   2   0  100.0   A
samples/java/bad/Blowfish.java:1155 Blowfish.f         12   2    1   1   1  100.0   A
samples/java/bad/Blowfish.java:1205 Blowfish.encrypt   11   2    1   2   1  100.0   A
samples/java/bad/Blowfish.java:1229 Blowfish.decrypt   11   2    1   2   1  100.0   A
```

### JAVA (`--framework none`) — 5. Ring & Sliding Window Buffer Cohesion & Attribute Count (TheAlgorithms/Java buffers/)

#### Good Baseline: [`good/CircularBuffer.java`](good/CircularBuffer.java) ([sidecar JSON](good/CircularBuffer.java.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Java (src/main/java/com/thealgorithms/datastructures/buffers/CircularBuffer.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/datastructures/buffers/CircularBuffer.java) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 5
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/CircularBuffer.java          src      55    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/CircularBuffer.java:13 CircularB    55    5     1    8  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/CircularBuffer.java:26 CircularBuf    8   1    0   1   0  100.0   A
samples/java/good/CircularBuffer.java:42 CircularBuf    3   1    0   0   0  100.0   A
samples/java/good/CircularBuffer.java:52 CircularBuf    3   1    0   0   0  100.0   A
samples/java/good/CircularBuffer.java:62 CircularBuf    8   2    1   0   1  100.0   A
samples/java/good/CircularBuffer.java:80 CircularBuf   13   3    2   1   1  100.0   A
```

#### Bad Baseline: [`bad/SlidingWindowAggregator.java`](bad/SlidingWindowAggregator.java) ([sidecar JSON](bad/SlidingWindowAggregator.java.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Java (src/main/java/com/thealgorithms/datastructures/buffers/SlidingWindowAggregator.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/datastructures/buffers/SlidingWindowAggregator.java) (`MIT`)
- **Expected Scorecard:** `Composite 13.9/100 (Grade F)` — `SRP: 8.9` | `Size: 100.0` | `Complexity: 83.5` | `Clean: 99.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 13.9/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 26
Dimensions -> SRP: 8.9 | Size: 100.0 | Complexity: 83.5 | Clean: 99.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/SlidingWindowAggregator.java  src     177    -   8.9 100.0  83.5  99.0 100.0   13.9   F

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/SlidingWindowAggregator.java:92 S   177   26     2   36   13.9   F
    - SRP: LCOM4=2 disconnected method groups (-15.0 pts)
    - SRP: methods=26 (>10) (-64.0 pts)
    - SRP: self attributes=10 (>7) (-12.0 pts)
    - Complexity: total class CC=36 (>25) (-16.5 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/SlidingWindowAggregator.java:205 Sl   12   1    0   1   0   99.1   A
    - SRP: high external call fan-out=7 (>6) (-3.0 pts)
samples/java/bad/SlidingWindowAggregator.java:387 Sl    4   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/SlidingWindowAggregator.java:409 Sl    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/SlidingWindowAggregator.java:413 Sl    4   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/SlidingWindowAggregator.java:418 Sl    4   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/SlidingWindowAggregator.java:423 Sl    3   1    0   2   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/SlidingWindowAggregator.java:130 Sl   10   1    0   3   0  100.0   A
samples/java/bad/SlidingWindowAggregator.java:149 Sl    3   1    0   2   0  100.0   A
samples/java/bad/SlidingWindowAggregator.java:159 Sl    3   1    0   1   0  100.0   A
samples/java/bad/SlidingWindowAggregator.java:170 Sl    3   1    0   1   0  100.0   A
samples/java/bad/SlidingWindowAggregator.java:182 Sl    3   1    0   2   0  100.0   A
samples/java/bad/SlidingWindowAggregator.java:194 Sl    3   1    0   2   0  100.0   A
samples/java/bad/SlidingWindowAggregator.java:226 Sl    6   2    1   1   1  100.0   A
samples/java/bad/SlidingWindowAggregator.java:239 Sl   15   3    2   0   1  100.0   A
samples/java/bad/SlidingWindowAggregator.java:263 Sl   10   3    2   0   1  100.0   A
samples/java/bad/SlidingWindowAggregator.java:281 Sl    6   2    1   1   1  100.0   A
samples/java/bad/SlidingWindowAggregator.java:294 Sl    6   2    1   0   1  100.0   A
samples/java/bad/SlidingWindowAggregator.java:307 Sl    6   2    1   0   1  100.0   A
samples/java/bad/SlidingWindowAggregator.java:319 Sl    3   1    0   0   0  100.0   A
samples/java/bad/SlidingWindowAggregator.java:328 Sl    3   1    0   0   0  100.0   A
samples/java/bad/SlidingWindowAggregator.java:337 Sl    3   1    0   0   0  100.0   A
samples/java/bad/SlidingWindowAggregator.java:346 Sl    3   1    0   0   0  100.0   A
samples/java/bad/SlidingWindowAggregator.java:353 Sl    9   1    0   0   0  100.0   A
samples/java/bad/SlidingWindowAggregator.java:369 Sl    7   2    1   0   1  100.0   A
samples/java/bad/SlidingWindowAggregator.java:382 Sl    4   1    0   0   0  100.0   A
samples/java/bad/SlidingWindowAggregator.java:397 Sl   11   2    1   0   1  100.0   A
```

### JAVA (`--framework none`) — 6. Graph Traversal & Path Complexity (TheAlgorithms/Java graph/)

#### Good Baseline: [`good/TarjanBridges.java`](good/TarjanBridges.java) ([sidecar JSON](good/TarjanBridges.java.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Java (src/main/java/com/thealgorithms/graph/TarjanBridges.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/graph/TarjanBridges.java) (`MIT`)
- **Expected Scorecard:** `Composite 99.6/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 98.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 99.6/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 2
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 98.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/TarjanBridges.java           src      57    - 100.0 100.0  98.0 100.0 100.0   99.6   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/TarjanBridges.java:29 TarjanBrid    57    2     1    7   99.6   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/TarjanBridges.java:52 TarjanBridge   19   6    5   2   1   99.2   A
    - Complexity: CC=6 (>5) (-4.0 pts)
samples/java/good/TarjanBridges.java:31 TarjanBridge    3   1    0   0   0  100.0   A
```

#### Bad Baseline: [`bad/HierholzerEulerianPath.java`](bad/HierholzerEulerianPath.java) ([sidecar JSON](bad/HierholzerEulerianPath.java.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Java (src/main/java/com/thealgorithms/graph/HierholzerEulerianPath.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/graph/HierholzerEulerianPath.java) (`MIT`)
- **Expected Scorecard:** `Composite 52.7/100 (Grade F)` — `SRP: 97.0` | `Size: 92.5` | `Complexity: 47.7` | `Clean: 94.3` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 52.7/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 7
Dimensions -> SRP: 97.0 | Size: 92.5 | Complexity: 47.7 | Clean: 94.3 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/HierholzerEulerianPath.java   src     188    -  97.0  92.5  47.7  94.3 100.0   52.7   F

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/HierholzerEulerianPath.java:38 Hi   188    7     1   48   52.7   F
    - Complexity: total class CC=48 (>25) (-34.5 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/HierholzerEulerianPath.java:207 Hie   49  15   14   3   1   35.0   F
    - Size: LOC=49 (>25) (-36.0 pts)
    - Complexity: CC=15 (>5) (-55.0 pts)
    - Complexity: cognitive=14 (>8) (-15.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/HierholzerEulerianPath.java:269 Hie   32  10    9   4   1   92.9   A
    - Size: LOC=32 (>25) (-10.5 pts)
    - Complexity: CC=10 (>5) (-20.0 pts)
    - Complexity: cognitive=9 (>8) (-2.5 pts)
samples/java/bad/HierholzerEulerianPath.java:151 Hie   29   9    8   2   1   93.8   A
    - Size: LOC=29 (>25) (-6.0 pts)
    - Complexity: CC=9 (>5) (-16.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/HierholzerEulerianPath.java:184 Hie   19   4    3   2   1   94.0   A
    - SRP: high external call fan-out=11 (>6) (-15.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/HierholzerEulerianPath.java:105 Hie   24   6    5   0   1   95.0   A
    - SRP: high external call fan-out=8 (>6) (-6.0 pts)
    - Complexity: CC=6 (>5) (-4.0 pts)
    - Complexity: returns=6 (>3) (-12.0 pts)
samples/java/bad/HierholzerEulerianPath.java:139 Hie   11   3    2   2   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/HierholzerEulerianPath.java:95 Hier    3   1    0   1   0  100.0   A
```

### JAVA (`--framework none`) — 7. Mathematical Utility Javadocs & Cohesion (TheAlgorithms/Java maths/)

#### Good Baseline: [`good/ChineseRemainderTheorem.java`](good/ChineseRemainderTheorem.java) ([sidecar JSON](good/ChineseRemainderTheorem.java.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Java (src/main/java/com/thealgorithms/maths/ChineseRemainderTheorem.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/maths/ChineseRemainderTheorem.java) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 3
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/ChineseRemainderTheorem.java src      42    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/ChineseRemainderTheorem.java:13     42    3     1    9  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/ChineseRemainderTheorem.java:14 Ch    2   1    0   0   0  100.0   A
samples/java/good/ChineseRemainderTheorem.java:23 Ch   17   4    3   2   1  100.0   A
samples/java/good/ChineseRemainderTheorem.java:55 Ch   21   4    3   2   1  100.0   A
```

#### Bad Baseline: [`bad/DistanceFormula.java`](bad/DistanceFormula.java) ([sidecar JSON](bad/DistanceFormula.java.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Java (src/main/java/com/thealgorithms/maths/DistanceFormula.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/maths/DistanceFormula.java) (`MIT`)
- **Expected Scorecard:** `Composite 75.0/100 (Grade C)` — `SRP: 70.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 71.4` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 75.0/100 (Grade C) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 5
Dimensions -> SRP: 70.0 | Size: 100.0 | Complexity: 100.0 | Clean: 71.4 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/DistanceFormula.java          src      35    -  70.0 100.0 100.0  71.4 100.0   75.0   C
    - Clean (DRY): DRY-001 (type2, 43 toks, 6 LOC) L18-25 in DistanceFormula.hammingDistance matches samples/java/bad/DistanceFormula.java:33-40 (DistanceFormula.minkowskiDistance) (-4.0 pts)
    - Clean (DRY): duplication_ratio=17.1% (>10.0%) (-3.6 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 6/35 (17.1%) | DRY Score: 92.4/100 | Clone Groups: 1 (T1: 0, T2: 1, T3: 0 | intra: 1, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type2  100.0% intra_file      6 samples/java/bad/DistanceFormula.java:L18-25, samples/java/bad/DistanceFormula.java:L33-40

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/DistanceFormula.java:3 DistanceFo    35    5     3    9   75.0   C
    - SRP: LCOM4=3 disconnected method groups (-30.0 pts)
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/DistanceFormula.java:31 DistanceFor   13   3    2   3   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/DistanceFormula.java:4 DistanceForm    2   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DistanceFormula.java:7 DistanceForm    5   1    0   4   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DistanceFormula.java:13 DistanceFor    3   1    0   4   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/DistanceFormula.java:17 DistanceFor   10   3    2   2   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

### JAVA (`--framework none`) — 8. String Algorithm Single-Responsibility Cohesion (TheAlgorithms/Java strings/)

#### Good Baseline: [`good/PermuteString.java`](good/PermuteString.java) ([sidecar JSON](good/PermuteString.java.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Java (src/main/java/com/thealgorithms/strings/PermuteString.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/strings/PermuteString.java) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 4
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/PermuteString.java           src      27    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/PermuteString.java:29 PermuteStr    27    4     1    6  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/PermuteString.java:30 PermuteStrin    2   1    0   0   0  100.0   A
samples/java/good/PermuteString.java:45 PermuteStrin    5   1    0   1   0  100.0   A
samples/java/good/PermuteString.java:59 PermuteStrin   11   3    2   4   1  100.0   A
samples/java/good/PermuteString.java:82 PermuteStrin    7   1    0   3   0  100.0   A
```

#### Bad Baseline: [`bad/Anagrams.java`](bad/Anagrams.java) ([sidecar JSON](bad/Anagrams.java.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Java (src/main/java/com/thealgorithms/strings/Anagrams.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/strings/Anagrams.java) (`MIT`)
- **Expected Scorecard:** `Composite 36.5/100 (Grade F)` — `SRP: 31.5` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 68.2` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 36.5/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 6
Dimensions -> SRP: 31.5 | Size: 100.0 | Complexity: 100.0 | Clean: 68.2 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/Anagrams.java                 src      87    -  31.5 100.0 100.0  68.2 100.0   36.5   F
    - Clean (DRY): DRY-001 (type2, 142 toks, 18 LOC) L76-93 in Anagrams.areAnagramsByCountingCharsSingleArray matches samples/java/bad/Anagrams.java:133-150 (Anagrams.areAnagramsBySingleFreqArray) (-4.0 pts)
    - Clean (DRY): DRY-002 (type1, 60 toks, 6 LOC) L26-31 in Anagrams.areAnagramsBySorting matches samples/java/bad/Anagrams.java:76-82 (Anagrams.areAnagramsByCountingCharsSingleArray), samples/java/bad/Anagrams.java:104-109 (Anagrams.areAnagramsUsingHashMap), samples/java/bad/Anagrams.java:133-139 (Anagrams.areAnagramsBySingleFreqArray) (-15.0 pts)
    - Clean (DRY): duplication_ratio=35.6% (>10.0%) (-12.8 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 31/87 (35.6%) | DRY Score: 68.2/100 | Clone Groups: 2 (T1: 1, T2: 1, T3: 0 | intra: 2, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type2  100.0% intra_file     18 samples/java/bad/Anagrams.java:L76-93, samples/java/bad/Anagrams.java:L133-150
DRY-002  type1  100.0% intra_file      7 samples/java/bad/Anagrams.java:L26-31, samples/java/bad/Anagrams.java:L76-82, samples/java/bad/Anagrams.java:L104-109 (+1 more)

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/Anagrams.java:13 Anagrams            87    6     5   23   36.5   F
    - SRP: LCOM4=5 disconnected method groups (-60.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/Anagrams.java:104 Anagrams.areAnagr   18   5    4   2   1   78.0   C
    - SRP: high external call fan-out=15 (>6) (-27.0 pts)
samples/java/bad/Anagrams.java:26 Anagrams.areAnagra   12   2    1   2   1   96.4   A
    - SRP: high external call fan-out=10 (>6) (-12.0 pts)
samples/java/bad/Anagrams.java:76 Anagrams.areAnagra   18   5    4   2   1   98.2   A
    - SRP: high external call fan-out=8 (>6) (-6.0 pts)
samples/java/bad/Anagrams.java:133 Anagrams.areAnagr   18   5    4   2   1   98.2   A
    - SRP: high external call fan-out=8 (>6) (-6.0 pts)
samples/java/bad/Anagrams.java:14 Anagrams.Anagrams     2   1    0   0   0  100.0   A
samples/java/bad/Anagrams.java:48 Anagrams.areAnagra   17   5    4   2   1  100.0   A
```

### JAVA (`--framework none`) — 9. Binary Search Tree Implementation Size & Complexity (TheAlgorithms/Java trees/)

#### Good Baseline: [`good/BSTRecursive.java`](good/BSTRecursive.java) ([sidecar JSON](good/BSTRecursive.java.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Java (src/main/java/com/thealgorithms/datastructures/trees/BSTRecursive.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/datastructures/trees/BSTRecursive.java) (`MIT`)
- **Expected Scorecard:** `Composite 98.9/100 (Grade A)` — `SRP: 100.0` | `Size: 99.2` | `Complexity: 98.0` | `Clean: 96.4` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 98.9/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 8
Dimensions -> SRP: 100.0 | Size: 99.2 | Complexity: 98.0 | Clean: 96.4 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/BSTRecursive.java            src      73    - 100.0  99.2  98.0  96.4 100.0   98.9   A
    - Clean (DRY): DRY-001 (type3, 90.8%, 51 toks, 6 LOC) L49-54 in BSTRecursive.delete matches samples/java/good/BSTRecursive.java:88-93 (BSTRecursive.insert) (-3.0 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 6/73 (8.2%) | DRY Score: 97.0/100 | Clone Groups: 1 (T1: 0, T2: 0, T3: 1 | intra: 1, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type3   90.8% intra_file      6 samples/java/good/BSTRecursive.java:L49-54, samples/java/good/BSTRecursive.java:L88-93

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/BSTRecursive.java:22 BSTRecursiv    73    8     1   22   99.3   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/BSTRecursive.java:47 BSTRecursive.   29   8    7   2   1   96.1   A
    - Size: LOC=29 (>25) (-6.0 pts)
    - Complexity: CC=8 (>5) (-12.0 pts)
samples/java/good/BSTRecursive.java:36 BSTRecursive.    3   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/good/BSTRecursive.java:104 BSTRecursive   11   4    3   2   1   99.2   A
    - Complexity: returns=4 (>3) (-4.0 pts)
samples/java/good/BSTRecursive.java:32 BSTRecursive.    3   1    0   0   0  100.0   A
samples/java/good/BSTRecursive.java:86 BSTRecursive.   10   4    3   2   1  100.0   A
samples/java/good/BSTRecursive.java:122 BSTRecursive    3   1    0   1   0  100.0   A
samples/java/good/BSTRecursive.java:131 BSTRecursive    3   1    0   1   0  100.0   A
samples/java/good/BSTRecursive.java:140 BSTRecursive    8   2    1   1   1  100.0   A
```

#### Bad Baseline: [`bad/RedBlackBST.java`](bad/RedBlackBST.java) ([sidecar JSON](bad/RedBlackBST.java.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Java (src/main/java/com/thealgorithms/datastructures/trees/RedBlackBST.java)](https://github.com/TheAlgorithms/Java/blob/master/src/main/java/com/thealgorithms/datastructures/trees/RedBlackBST.java) (`MIT`)
- **Expected Scorecard:** `Composite 48.8/100 (Grade F)` — `SRP: 87.8` | `Size: 49.4` | `Complexity: 43.8` | `Clean: 71.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 48.8/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 13
Dimensions -> SRP: 87.8 | Size: 49.4 | Complexity: 43.8 | Clean: 71.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/RedBlackBST.java              src     308    -  87.8  49.4  43.8  71.0 100.0   48.8   F
    - Clean (DRY): DRY-001 (type3, 92.5%, 161 toks, 24 LOC) L137-160 in RedBlackBST.rotateLeft matches samples/java/bad/RedBlackBST.java:162-186 (RedBlackBST.rotateRight) (-3.0 pts)
    - Clean (DRY): DRY-002 (type2, 78 toks, 12 LOC) L142-153 in RedBlackBST.rotateLeft matches samples/java/bad/RedBlackBST.java:167-179 (RedBlackBST.rotateRight) (-4.0 pts)
    - Clean (DRY): DRY-003 (type2, 57 toks, 9 LOC) L100-109 in RedBlackBST.fixTree matches samples/java/bad/RedBlackBST.java:117-125 (RedBlackBST.fixTree) (-4.0 pts)
    - Clean (DRY): DRY-004 (type2, 36 toks, 8 LOC) L153-160 in RedBlackBST.rotateLeft matches samples/java/bad/RedBlackBST.java:179-186 (RedBlackBST.rotateRight) (-4.0 pts)
    - Clean (DRY): DRY-005 (type2, 40 toks, 6 LOC) L300-307 in RedBlackBST.insertDemo matches samples/java/bad/RedBlackBST.java:319-324 (RedBlackBST.deleteDemo) (-4.0 pts)
    - Clean (DRY): duplication_ratio=13.0% (>10.0%) (-1.5 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 40/308 (13.0%) | DRY Score: 79.5/100 | Clone Groups: 5 (T1: 0, T2: 4, T3: 1 | intra: 5, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type3   92.5% intra_file     24 samples/java/bad/RedBlackBST.java:L137-160, samples/java/bad/RedBlackBST.java:L162-186
DRY-002  type2  100.0% intra_file     12 samples/java/bad/RedBlackBST.java:L142-153, samples/java/bad/RedBlackBST.java:L167-179
DRY-003  type2  100.0% intra_file      9 samples/java/bad/RedBlackBST.java:L100-109, samples/java/bad/RedBlackBST.java:L117-125
DRY-004  type2  100.0% intra_file      8 samples/java/bad/RedBlackBST.java:L153-160, samples/java/bad/RedBlackBST.java:L179-186
DRY-005  type2  100.0% intra_file      6 samples/java/bad/RedBlackBST.java:L300-307, samples/java/bad/RedBlackBST.java:L319-324

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/RedBlackBST.java:8 RedBlackBST      308   13     1   59   48.8   F
    - SRP: methods=13 (>10) (-12.0 pts)
    - Size: class LOC=308 (>200) (-43.2 pts)
    - Complexity: total class CC=59 (>25) (-51.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/RedBlackBST.java:243 RedBlackBST.de   56  11   10   1   1   52.5   F
    - Size: LOC=56 (>25) (-52.5 pts)
    - Complexity: CC=11 (>5) (-27.0 pts)
    - Complexity: cognitive=10 (>8) (-5.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/RedBlackBST.java:96 RedBlackBST.fix   39   7    6   1   1   91.7   A
    - Size: LOC=39 (>25) (-21.0 pts)
    - Complexity: CC=7 (>5) (-8.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/RedBlackBST.java:206 RedBlackBST.de   35   6    5   1   1   94.0   A
    - Size: LOC=35 (>25) (-15.0 pts)
    - Complexity: CC=6 (>5) (-4.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/RedBlackBST.java:65 RedBlackBST.ins   30   7    6   1   1   95.0   A
    - Size: LOC=30 (>25) (-7.5 pts)
    - Complexity: CC=7 (>5) (-8.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/RedBlackBST.java:47 RedBlackBST.fin   17   7    6   2   1   95.3   A
    - Complexity: CC=7 (>5) (-8.0 pts)
    - Complexity: returns=5 (>3) (-8.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/RedBlackBST.java:319 RedBlackBST.de   19   2    1   0   1   97.6   A
    - SRP: high external call fan-out=7 (>6) (-3.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/RedBlackBST.java:137 RedBlackBST.ro   24   4    3   1   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/RedBlackBST.java:162 RedBlackBST.ro   24   4    3   1   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/RedBlackBST.java:300 RedBlackBST.in   16   2    1   0   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/java/bad/RedBlackBST.java:29 RedBlackBST.pri    8   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/RedBlackBST.java:38 RedBlackBST.pri    8   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/RedBlackBST.java:188 RedBlackBST.tr   10   3    2   2   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/java/bad/RedBlackBST.java:199 RedBlackBST.tr    6   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

### JAVA (`--framework none`) — 10. JUnit 5 Sorting Test Suite Assertion Hygiene (TheAlgorithms/Java sorts/ tests)

#### Good Baseline: [`good/BubbleSortTest.java`](good/BubbleSortTest.java) ([sidecar JSON](good/BubbleSortTest.java.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Java (src/test/java/com/thealgorithms/sorts/BubbleSortTest.java)](https://github.com/TheAlgorithms/Java/blob/master/src/test/java/com/thealgorithms/sorts/BubbleSortTest.java) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 0, test: 1) | Classes: 1 | Functions/Methods: 10
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/BubbleSortTest.java          test    148    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/BubbleSortTest.java:12 BubbleSor   148   10     1   10  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java/good/BubbleSortTest.java:16 BubbleSortT    7   1    0   0   0  100.0   A
samples/java/good/BubbleSortTest.java:24 BubbleSortT    7   1    0   0   0  100.0   A
samples/java/good/BubbleSortTest.java:32 BubbleSortT    7   1    0   0   0  100.0   A
samples/java/good/BubbleSortTest.java:40 BubbleSortT   19   1    0   0   0  100.0   A
samples/java/good/BubbleSortTest.java:60 BubbleSortT   35   1    0   0   0  100.0   A
samples/java/good/BubbleSortTest.java:96 BubbleSortT    7   1    0   0   0  100.0   A
samples/java/good/BubbleSortTest.java:104 BubbleSort    7   1    0   0   0  100.0   A
samples/java/good/BubbleSortTest.java:112 BubbleSort    7   1    0   0   0  100.0   A
samples/java/good/BubbleSortTest.java:120 BubbleSort    7   1    0   0   0  100.0   A
samples/java/good/BubbleSortTest.java:163 BubbleSort   15   1    0   0   0  100.0   A
```

#### Bad Baseline: [`bad/InsertionSortTest.java`](bad/InsertionSortTest.java) ([sidecar JSON](bad/InsertionSortTest.java.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Java (src/test/java/com/thealgorithms/sorts/InsertionSortTest.java)](https://github.com/TheAlgorithms/Java/blob/master/src/test/java/com/thealgorithms/sorts/InsertionSortTest.java) (`MIT`)
- **Expected Scorecard:** `Composite 65.0/100 (Grade D)` — `SRP: 60.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 89.5` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 65.0/100 (Grade D) | Files: 1 (src: 0, test: 1) | Classes: 1 | Functions/Methods: 20
Dimensions -> SRP: 60.0 | Size: 100.0 | Complexity: 100.0 | Clean: 89.5 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/InsertionSortTest.java        test    160    -  60.0 100.0 100.0  89.5 100.0   65.0   D

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/InsertionSortTest.java:11 Inserti   160   20     1   20   65.0   D
    - SRP: methods=20 (>10) (-40.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/java/bad/InsertionSortTest.java:19 Insertion    5   1    0   0   0   75.0   C
    - Clean (Test): test has 0 assertions (-30.0 pts)
samples/java/bad/InsertionSortTest.java:33 Insertion    5   1    0   0   0   75.0   C
    - Clean (Test): test has 0 assertions (-30.0 pts)
samples/java/bad/InsertionSortTest.java:47 Insertion    5   1    0   0   0   75.0   C
    - Clean (Test): test has 0 assertions (-30.0 pts)
samples/java/bad/InsertionSortTest.java:61 Insertion    5   1    0   0   0   75.0   C
    - Clean (Test): test has 0 assertions (-30.0 pts)
samples/java/bad/InsertionSortTest.java:75 Insertion    5   1    0   0   0   75.0   C
    - Clean (Test): test has 0 assertions (-30.0 pts)
samples/java/bad/InsertionSortTest.java:89 Insertion    5   1    0   0   0   75.0   C
    - Clean (Test): test has 0 assertions (-30.0 pts)
samples/java/bad/InsertionSortTest.java:103 Insertio    5   1    0   0   0   75.0   C
    - Clean (Test): test has 0 assertions (-30.0 pts)
samples/java/bad/InsertionSortTest.java:14 Insertion    4   1    0   0   0  100.0   A
samples/java/bad/InsertionSortTest.java:25 Insertion    7   1    0   1   0  100.0   A
samples/java/bad/InsertionSortTest.java:39 Insertion    7   1    0   1   0  100.0   A
samples/java/bad/InsertionSortTest.java:53 Insertion    7   1    0   1   0  100.0   A
samples/java/bad/InsertionSortTest.java:67 Insertion    7   1    0   1   0  100.0   A
samples/java/bad/InsertionSortTest.java:81 Insertion    7   1    0   1   0  100.0   A
samples/java/bad/InsertionSortTest.java:95 Insertion    7   1    0   1   0  100.0   A
samples/java/bad/InsertionSortTest.java:109 Insertio    6   1    0   1   0  100.0   A
samples/java/bad/InsertionSortTest.java:116 Insertio    7   1    0   0   0  100.0   A
samples/java/bad/InsertionSortTest.java:124 Insertio    7   1    0   0   0  100.0   A
samples/java/bad/InsertionSortTest.java:132 Insertio    7   1    0   0   0  100.0   A
samples/java/bad/InsertionSortTest.java:140 Insertio    7   1    0   0   0  100.0   A
samples/java/bad/InsertionSortTest.java:183 Insertio   15   1    0   0   0  100.0   A
```
