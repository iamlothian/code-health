# Python Code Health Scorecard Baselines

This catalog provides 10 functionally comparable, verbatim real-world **Good** and **Bad** Python code health baseline scenario pairs (`--language python --framework auto`) from [`TheAlgorithms/Python`](https://github.com/TheAlgorithms/Python), [`PyCQA/bandit`](https://github.com/PyCQA/bandit), and [`pallets/click`](https://github.com/pallets/click).

Each sample file `<filename>` has a matching `<filename>.expected.json` sidecar file and is listed in [`manifest.json`](manifest.json).

---

## Quick Summary Table

| Profile | Scenario | Quality | Sample File | Dataset Source | LOC | SRP | Size | Comp | Clean | Sec | Score | Grade |
| :--- | :--- | :---: | :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| `python (auto)` | 1. Shortest-Path Graph Algorithm Complexity & Decomposition (TheAlgorithms/Python graphs/) | **GOOD** | [`good/bellman_ford.py`](good/bellman_ford.py) | [TheAlgorithms/Python (graphs/bellman_ford.py)](https://github.com/TheAlgorithms/Python/blob/master/graphs/bellman_ford.py) | 56 | 100.0 | 100.0 | 97.8 | 86.9 | 100.0 | **97.6** | **A** |
| `python (auto)` | 1. Shortest-Path Graph Algorithm Complexity & Decomposition (TheAlgorithms/Python graphs/) | **BAD** | [`bad/a_star.py`](bad/a_star.py) | [TheAlgorithms/Python (graphs/a_star.py)](https://github.com/TheAlgorithms/Python/blob/master/graphs/a_star.py) | 118 | 100.0 | 14.0 | 10.5 | 90.0 | 100.0 | **15.5** | **F** |
| `python (auto)` | 2. Binary Tree Data Structure OOP Design (TheAlgorithms/Python binary_tree/) | **GOOD** | [`good/fenwick_tree.py`](good/fenwick_tree.py) | [TheAlgorithms/Python (data_structures/binary_tree/fenwick_tree.py)](https://github.com/TheAlgorithms/Python/blob/master/data_structures/binary_tree/fenwick_tree.py) | 202 | 96.0 | 100.0 | 96.6 | 85.1 | 100.0 | **95.9** | **A** |
| `python (auto)` | 2. Binary Tree Data Structure OOP Design (TheAlgorithms/Python binary_tree/) | **BAD** | [`bad/red_black_tree.py`](bad/red_black_tree.py) | [TheAlgorithms/Python (data_structures/binary_tree/red_black_tree.py)](https://github.com/TheAlgorithms/Python/blob/master/data_structures/binary_tree/red_black_tree.py) | 613 | 49.1 | 0.0 | 25.4 | 65.5 | 100.0 | **5.0** | **F** |
| `python (auto)` | 3. Serialization & I/O Security Hygiene (PyCQA/bandit examples/, 19 LOC) | **GOOD** | [`good/urlopen.py`](good/urlopen.py) | [PyCQA/bandit (examples/urlopen.py)](https://github.com/PyCQA/bandit/blob/main/examples/urlopen.py) | 19 | 100.0 | 100.0 | 100.0 | 80.0 | 100.0 | **97.0** | **A** |
| `python (auto)` | 3. Serialization & I/O Security Hygiene (PyCQA/bandit examples/, 19 LOC) | **BAD** | [`bad/yaml_load.py`](bad/yaml_load.py) | [PyCQA/bandit (examples/yaml_load.py)](https://github.com/PyCQA/bandit/blob/main/examples/yaml_load.py) | 19 | 100.0 | 100.0 | 100.0 | 75.0 | 60.0 | **65.0** | **D** |
| `python (auto)` | 4. CLI Command & Option Test Suite Hygiene (pallets/click tests/) | **GOOD** | [`good/test_info_dict.py`](good/test_info_dict.py) | [pallets/click (tests/test_info_dict.py)](https://github.com/pallets/click/blob/main/tests/test_info_dict.py) | 322 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `python (auto)` | 4. CLI Command & Option Test Suite Hygiene (pallets/click tests/) | **BAD** | [`bad/test_commands.py`](bad/test_commands.py) | [pallets/click (tests/test_commands.py)](https://github.com/pallets/click/blob/main/tests/test_commands.py) | 544 | 100.0 | 68.9 | 100.0 | 92.8 | 100.0 | **73.9** | **C** |
| `python (auto)` | 5. Sorting Algorithm Function Size & Decomposition (TheAlgorithms/Python sorts/) | **GOOD** | [`good/pigeon_sort.py`](good/pigeon_sort.py) | [TheAlgorithms/Python (sorts/pigeon_sort.py)](https://github.com/TheAlgorithms/Python/blob/master/sorts/pigeon_sort.py) | 35 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `python (auto)` | 5. Sorting Algorithm Function Size & Decomposition (TheAlgorithms/Python sorts/) | **BAD** | [`bad/merge_insertion_sort.py`](bad/merge_insertion_sort.py) | [TheAlgorithms/Python (sorts/merge_insertion_sort.py)](https://github.com/TheAlgorithms/Python/blob/master/sorts/merge_insertion_sort.py) | 158 | 100.0 | 25.2 | 67.9 | 99.8 | 100.0 | **30.2** | **F** |
| `python (auto)` | 6. Safe Analyzer Plugin vs. Unsafe Subprocess & YAML Deserialization (PyCQA/bandit) | **GOOD** | [`good/pytorch_load.py`](good/pytorch_load.py) | [PyCQA/bandit (bandit/plugins/pytorch_load.py)](https://github.com/PyCQA/bandit/blob/main/bandit/plugins/pytorch_load.py) | 28 | 100.0 | 100.0 | 96.0 | 85.0 | 100.0 | **97.0** | **A** |
| `python (auto)` | 6. Safe Analyzer Plugin vs. Unsafe Subprocess & YAML Deserialization (PyCQA/bandit) | **BAD** | [`bad/new_candidates-all.py`](bad/new_candidates-all.py) | [PyCQA/bandit (examples/new_candidates-all.py)](https://github.com/PyCQA/bandit/blob/main/examples/new_candidates-all.py) | 12 | 100.0 | 100.0 | 100.0 | 75.0 | 20.0 | **25.0** | **F** |
| `python (auto)` | 7. Linked Data Structure Class Cohesion & Method Count (TheAlgorithms/Python data_structures/) | **GOOD** | [`good/flatten_binarytree_to_linkedlist.py`](good/flatten_binarytree_to_linkedlist.py) | [TheAlgorithms/Python (data_structures/binary_tree/flatten_binarytree_to_linkedlist.py)](https://github.com/TheAlgorithms/Python/blob/master/data_structures/binary_tree/flatten_binarytree_to_linkedlist.py) | 96 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `python (auto)` | 7. Linked Data Structure Class Cohesion & Method Count (TheAlgorithms/Python data_structures/) | **BAD** | [`bad/sorted_linked_list.py`](bad/sorted_linked_list.py) | [TheAlgorithms/Python (data_structures/linked_list/sorted_linked_list.py)](https://github.com/TheAlgorithms/Python/blob/master/data_structures/linked_list/sorted_linked_list.py) | 274 | 62.5 | 86.2 | 82.4 | 90.0 | 100.0 | **67.5** | **D** |
| `python (auto)` | 8. Stack Expression Notation Conversion Complexity (TheAlgorithms/Python data_structures/stacks/) | **GOOD** | [`good/postfix_to_infix_conversion.py`](good/postfix_to_infix_conversion.py) | [TheAlgorithms/Python (data_structures/stacks/postfix_to_infix_conversion.py)](https://github.com/TheAlgorithms/Python/blob/master/data_structures/stacks/postfix_to_infix_conversion.py) | 39 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `python (auto)` | 8. Stack Expression Notation Conversion Complexity (TheAlgorithms/Python data_structures/stacks/) | **BAD** | [`bad/infix_to_postfix_conversion.py`](bad/infix_to_postfix_conversion.py) | [TheAlgorithms/Python (data_structures/stacks/infix_to_postfix_conversion.py)](https://github.com/TheAlgorithms/Python/blob/master/data_structures/stacks/infix_to_postfix_conversion.py) | 91 | 89.3 | 79.0 | 10.5 | 96.0 | 100.0 | **15.5** | **F** |
| `python (auto)` | 9. Dynamic Programming Type Annotations & Documentation Hygiene (TheAlgorithms/Python dynamic_programming/) | **GOOD** | [`good/trapped_water.py`](good/trapped_water.py) | [TheAlgorithms/Python (dynamic_programming/trapped_water.py)](https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/trapped_water.py) | 38 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `python (auto)` | 9. Dynamic Programming Type Annotations & Documentation Hygiene (TheAlgorithms/Python dynamic_programming/) | **BAD** | [`bad/floyd_warshall.py`](bad/floyd_warshall.py) | [TheAlgorithms/Python (dynamic_programming/floyd_warshall.py)](https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/floyd_warshall.py) | 72 | 100.0 | 100.0 | 100.0 | 61.0 | 100.0 | **66.0** | **D** |
| `python (auto)` | 10. Click Command Chain Test Hygiene vs. Duplicated & Oversized Basic Tests (pallets/click tests/) | **GOOD** | [`good/test_chain.py`](good/test_chain.py) | [pallets/click (tests/test_chain.py)](https://github.com/pallets/click/blob/main/tests/test_chain.py) | 187 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `python (auto)` | 10. Click Command Chain Test Hygiene vs. Duplicated & Oversized Basic Tests (pallets/click tests/) | **BAD** | [`bad/test_basic.py`](bad/test_basic.py) | [pallets/click (tests/test_basic.py)](https://github.com/pallets/click/blob/main/tests/test_basic.py) | 761 | 100.0 | 21.9 | 100.0 | 72.8 | 100.0 | **26.9** | **F** |

---

## Detailed Scenario Scorecards

### PYTHON (`--framework auto`) — 1. Shortest-Path Graph Algorithm Complexity & Decomposition (TheAlgorithms/Python graphs/)

#### Good Baseline: [`good/bellman_ford.py`](good/bellman_ford.py) ([sidecar JSON](good/bellman_ford.py.expected.json))

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

#### Bad Baseline: [`bad/a_star.py`](bad/a_star.py) ([sidecar JSON](bad/a_star.py.expected.json))

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

#### Good Baseline: [`good/fenwick_tree.py`](good/fenwick_tree.py) ([sidecar JSON](good/fenwick_tree.py.expected.json))

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

#### Bad Baseline: [`bad/red_black_tree.py`](bad/red_black_tree.py) ([sidecar JSON](bad/red_black_tree.py.expected.json))

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

#### Good Baseline: [`good/urlopen.py`](good/urlopen.py) ([sidecar JSON](good/urlopen.py.expected.json))

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

#### Bad Baseline: [`bad/yaml_load.py`](bad/yaml_load.py) ([sidecar JSON](bad/yaml_load.py.expected.json))

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

#### Good Baseline: [`good/test_info_dict.py`](good/test_info_dict.py) ([sidecar JSON](good/test_info_dict.py.expected.json))

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

#### Bad Baseline: [`bad/test_commands.py`](bad/test_commands.py) ([sidecar JSON](bad/test_commands.py.expected.json))

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

### PYTHON (`--framework auto`) — 5. Sorting Algorithm Function Size & Decomposition (TheAlgorithms/Python sorts/)

#### Good Baseline: [`good/pigeon_sort.py`](good/pigeon_sort.py) ([sidecar JSON](good/pigeon_sort.py.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Python (sorts/pigeon_sort.py)](https://github.com/TheAlgorithms/Python/blob/master/sorts/pigeon_sort.py) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/pigeon_sort.py             src      35    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/pigeon_sort.py:16 pigeon_sort      17   5    5   1   2  100.0   A
```

#### Bad Baseline: [`bad/merge_insertion_sort.py`](bad/merge_insertion_sort.py) ([sidecar JSON](bad/merge_insertion_sort.py.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Python (sorts/merge_insertion_sort.py)](https://github.com/TheAlgorithms/Python/blob/master/sorts/merge_insertion_sort.py) (`MIT`)
- **Expected Scorecard:** `Composite 30.2/100 (Grade F)` — `SRP: 100.0` | `Size: 25.2` | `Complexity: 67.9` | `Clean: 99.8` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 30.2/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 5
Dimensions -> SRP: 100.0 | Size: 25.2 | Complexity: 67.9 | Clean: 99.8 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/merge_insertion_sort.py     src     158    - 100.0  25.2  67.9  99.8 100.0   30.2   F

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/merge_insertion_sort.py:19 Comp     2    1     1    1   97.8   A
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/merge_insertion_sort.py:70 merge_   92  10   17   1   3    5.0   F
    - Size: LOC=92 (>25) (-100.0 pts)
    - Complexity: CC=10 (>5) (-20.0 pts)
    - Complexity: cognitive=17 (>8) (-22.5 pts)
samples/python/bad/merge_insertion_sort.py:23 binary   15   5    9   2   3   99.5   A
    - Complexity: cognitive=9 (>8) (-2.5 pts)
samples/python/bad/merge_insertion_sort.py:20 Compar    1   1    0   0   0  100.0   A
samples/python/bad/merge_insertion_sort.py:44 merge     8   4    5   2   2  100.0   A
samples/python/bad/merge_insertion_sort.py:58 sortli    6   2    1   1   1  100.0   A
```

### PYTHON (`--framework auto`) — 6. Safe Analyzer Plugin vs. Unsafe Subprocess & YAML Deserialization (PyCQA/bandit)

#### Good Baseline: [`good/pytorch_load.py`](good/pytorch_load.py) ([sidecar JSON](good/pytorch_load.py.expected.json))

- **Upstream Dataset / Benchmark:** [PyCQA/bandit (bandit/plugins/pytorch_load.py)](https://github.com/PyCQA/bandit/blob/main/bandit/plugins/pytorch_load.py) (`Apache-2.0`)
- **Expected Scorecard:** `Composite 97.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 96.0` | `Clean: 85.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 97.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 96.0 | Clean: 85.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/pytorch_load.py            src      28    - 100.0 100.0  96.0  85.0 100.0   97.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/pytorch_load.py:52 pytorch_load    16   6    6   1   2   97.0   A
    - Complexity: CC=6 (>5) (-4.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
    - Clean: 1 untyped param(s) (context) (-5.0 pts)
```

#### Bad Baseline: [`bad/new_candidates-all.py`](bad/new_candidates-all.py) ([sidecar JSON](bad/new_candidates-all.py.expected.json))

- **Upstream Dataset / Benchmark:** [PyCQA/bandit (examples/new_candidates-all.py)](https://github.com/PyCQA/bandit/blob/main/examples/new_candidates-all.py) (`Apache-2.0`)
- **Expected Scorecard:** `Composite 25.0/100 (Grade F)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 75.0` | `Security: 20.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 25.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 3
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 75.0 | Security: 20.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/new_candidates-all.py       src      12    - 100.0 100.0 100.0  75.0  20.0   25.0   F
    - Clean: missing module docstring (-10.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/new_candidates-all.py:4 subproces    3   1    0   0   0   25.0   F
    - Clean: missing return type annotation (-10.0 pts)
    - Clean: missing public docstring (-5.0 pts)
    - Security: subprocess call with shell=True at L7 (-40.0 pts)
    - Security: subprocess call with shell=True at L9 (-40.0 pts)
samples/python/bad/new_candidates-all.py:11 yaml_loa    4   1    0   0   0   25.0   F
    - Clean: missing return type annotation (-10.0 pts)
    - Clean: missing public docstring (-5.0 pts)
    - Security: unsafe yaml.load() without SafeLoader at L15 (-40.0 pts)
    - Security: unsafe yaml.load() without SafeLoader at L17 (-40.0 pts)
samples/python/bad/new_candidates-all.py:19 xml_sax_    3   1    0   0   0   97.8   A
    - Clean: missing return type annotation (-10.0 pts)
    - Clean: missing public docstring (-5.0 pts)
```

### PYTHON (`--framework auto`) — 7. Linked Data Structure Class Cohesion & Method Count (TheAlgorithms/Python data_structures/)

#### Good Baseline: [`good/flatten_binarytree_to_linkedlist.py`](good/flatten_binarytree_to_linkedlist.py) ([sidecar JSON](good/flatten_binarytree_to_linkedlist.py.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Python (data_structures/binary_tree/flatten_binarytree_to_linkedlist.py)](https://github.com/TheAlgorithms/Python/blob/master/data_structures/binary_tree/flatten_binarytree_to_linkedlist.py) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 4
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/flatten_binarytree_to_linkedlist.py src      96    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/flatten_binarytree_to_linkedli     5    1     1    1  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/flatten_binarytree_to_linkedlist    4   1    0   1   0  100.0   A
samples/python/good/flatten_binarytree_to_linkedlist    8   1    0   0   0  100.0   A
samples/python/good/flatten_binarytree_to_linkedlist   12   3    2   1   1  100.0   A
samples/python/good/flatten_binarytree_to_linkedlist    8   3    3   1   2  100.0   A
```

#### Bad Baseline: [`bad/sorted_linked_list.py`](bad/sorted_linked_list.py) ([sidecar JSON](bad/sorted_linked_list.py.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Python (data_structures/linked_list/sorted_linked_list.py)](https://github.com/TheAlgorithms/Python/blob/master/data_structures/linked_list/sorted_linked_list.py) (`MIT`)
- **Expected Scorecard:** `Composite 67.5/100 (Grade D)` — `SRP: 62.5` | `Size: 86.2` | `Complexity: 82.4` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 67.5/100 (Grade D) | Files: 1 (src: 1, test: 0) | Classes: 2 | Functions/Methods: 12
Dimensions -> SRP: 62.5 | Size: 86.2 | Complexity: 82.4 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/sorted_linked_list.py       src     274    -  62.5  86.2  82.4  90.0 100.0   67.5   D
    - Clean: missing module docstring (-10.0 pts)

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/sorted_linked_list.py:24 Sorted   233   12     3   34   67.0   D
    - SRP: LCOM4=3 disconnected method groups (-30.0 pts)
    - SRP: methods=12 (>10) (-8.0 pts)
    - Size: class LOC=233 (>200) (-13.2 pts)
    - Complexity: total class CC=34 (>25) (-13.5 pts)
samples/python/bad/sorted_linked_list.py:8 Node        3    0     0    0  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/sorted_linked_list.py:113 SortedL   18   8   14   1   4   74.0   C
    - Size: nesting depth=4 (>3) (-10.0 pts)
    - Complexity: CC=8 (>5) (-12.0 pts)
    - Complexity: cognitive=14 (>8) (-15.0 pts)
    - Complexity: returns=4 (>3) (-4.0 pts)
samples/python/bad/sorted_linked_list.py:80 SortedLi   17   7   13   1   3   95.9   A
    - Complexity: CC=7 (>5) (-8.0 pts)
    - Complexity: cognitive=13 (>8) (-12.5 pts)
samples/python/bad/sorted_linked_list.py:27 SortedLi    3   1    0   0   0  100.0   A
samples/python/bad/sorted_linked_list.py:37 SortedLi    5   2    1   0   1  100.0   A
samples/python/bad/sorted_linked_list.py:52 SortedLi    2   1    0   0   0  100.0   A
samples/python/bad/sorted_linked_list.py:68 SortedLi    2   1    0   1   0  100.0   A
samples/python/bad/sorted_linked_list.py:160 SortedL    2   1    0   1   0  100.0   A
samples/python/bad/sorted_linked_list.py:184 SortedL    2   1    0   0   0  100.0   A
samples/python/bad/sorted_linked_list.py:203 SortedL    2   2    1   0   0  100.0   A
samples/python/bad/sorted_linked_list.py:222 SortedL    2   2    1   0   0  100.0   A
samples/python/bad/sorted_linked_list.py:242 SortedL    7   4    5   0   2  100.0   A
samples/python/bad/sorted_linked_list.py:267 SortedL   12   4    6   1   2  100.0   A
```

### PYTHON (`--framework auto`) — 8. Stack Expression Notation Conversion Complexity (TheAlgorithms/Python data_structures/stacks/)

#### Good Baseline: [`good/postfix_to_infix_conversion.py`](good/postfix_to_infix_conversion.py) ([sidecar JSON](good/postfix_to_infix_conversion.py.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Python (data_structures/stacks/postfix_to_infix_conversion.py)](https://github.com/TheAlgorithms/Python/blob/master/data_structures/stacks/postfix_to_infix_conversion.py) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/postfix_to_infix_conversion.py src      39    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/postfix_to_infix_conversion.py:7   13   5    6   1   2  100.0   A
```

#### Bad Baseline: [`bad/infix_to_postfix_conversion.py`](bad/infix_to_postfix_conversion.py) ([sidecar JSON](bad/infix_to_postfix_conversion.py.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Python (data_structures/stacks/infix_to_postfix_conversion.py)](https://github.com/TheAlgorithms/Python/blob/master/data_structures/stacks/infix_to_postfix_conversion.py) (`MIT`)
- **Expected Scorecard:** `Composite 15.5/100 (Grade F)` — `SRP: 89.3` | `Size: 79.0` | `Complexity: 10.5` | `Clean: 96.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 15.5/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 3
Dimensions -> SRP: 89.3 | Size: 79.0 | Complexity: 10.5 | Clean: 96.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/infix_to_postfix_conversion.py src      91    -  89.3  79.0  10.5  96.0 100.0   15.5   F
    - Clean: 1 mid-file/late import(s) (-4.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/infix_to_postfix_conversion.py:45   34  15   36   1   4    5.0   F
    - SRP: high external call fan-out=10 (>6) (-12.0 pts)
    - Size: LOC=34 (>25) (-13.5 pts)
    - Size: nesting depth=4 (>3) (-10.0 pts)
    - Complexity: CC=15 (>5) (-55.0 pts)
    - Complexity: cognitive=36 (>8) (-70.0 pts)
samples/python/bad/infix_to_postfix_conversion.py:28    2   1    0   1   0  100.0   A
samples/python/bad/infix_to_postfix_conversion.py:37    2   1    0   1   0  100.0   A
```

### PYTHON (`--framework auto`) — 9. Dynamic Programming Type Annotations & Documentation Hygiene (TheAlgorithms/Python dynamic_programming/)

#### Good Baseline: [`good/trapped_water.py`](good/trapped_water.py) ([sidecar JSON](good/trapped_water.py.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Python (dynamic_programming/trapped_water.py)](https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/trapped_water.py) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/trapped_water.py           src      38    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/trapped_water.py:16 trapped_rain   18   5    4   1   1  100.0   A
```

#### Bad Baseline: [`bad/floyd_warshall.py`](bad/floyd_warshall.py) ([sidecar JSON](bad/floyd_warshall.py.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/Python (dynamic_programming/floyd_warshall.py)](https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/floyd_warshall.py) (`MIT`)
- **Expected Scorecard:** `Composite 66.0/100 (Grade D)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 61.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 66.0/100 (Grade D) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 4
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 61.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/floyd_warshall.py           src      72    - 100.0 100.0 100.0  61.0 100.0   66.0   D
    - Clean: missing module docstring (-10.0 pts)
    - Clean: 1 mid-file/late import(s) (-4.0 pts)

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/floyd_warshall.py:4 Graph          49    4     1    7   96.2   A
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/floyd_warshall.py:45 Graph.show_m    2   1    0   2   0   97.0   A
    - Clean: missing return type annotation (-10.0 pts)
    - Clean: 2 untyped param(s) (u, v) (-10.0 pts)
samples/python/bad/floyd_warshall.py:14 Graph.add_ed    2   1    0   3   0   97.8   A
    - Clean: 3 untyped param(s) (u, v, w) (-15.0 pts)
samples/python/bad/floyd_warshall.py:5 Graph.__init_    8   1    0   1   0   99.2   A
    - Clean: 1 untyped param(s) (n) (-5.0 pts)
samples/python/bad/floyd_warshall.py:26 Graph.floyd_    5   4    6   0   3  100.0   A
```

### PYTHON (`--framework auto`) — 10. Click Command Chain Test Hygiene vs. Duplicated & Oversized Basic Tests (pallets/click tests/)

#### Good Baseline: [`good/test_chain.py`](good/test_chain.py) ([sidecar JSON](good/test_chain.py.expected.json))

- **Upstream Dataset / Benchmark:** [pallets/click (tests/test_chain.py)](https://github.com/pallets/click/blob/main/tests/test_chain.py) (`BSD-3-Clause`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 0, test: 1) | Classes: 0 | Functions/Methods: 10
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/test_chain.py              test    187    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/python/good/test_chain.py:8 debug               5   1    0   0   0  100.0   A
samples/python/good/test_chain.py:15 test_basic_chai   17   1    0   1   0  100.0   A
samples/python/good/test_chain.py:47 test_chaining_h   16   1    0   3   0  100.0   A
samples/python/good/test_chain.py:68 test_chaining_w   15   1    0   1   0  100.0   A
samples/python/good/test_chain.py:89 test_no_command    9   1    0   3   0  100.0   A
samples/python/good/test_chain.py:107 test_chaining_   15   1    0   1   0  100.0   A
samples/python/good/test_chain.py:135 test_pipeline    27   1    0   4   0  100.0   A
samples/python/good/test_chain.py:170 test_args_and_   16   1    0   1   0  100.0   A
samples/python/good/test_chain.py:192 test_group_arg   21   1    0   1   0  100.0   A
samples/python/good/test_chain.py:222 test_group_cha   19   1    0   1   0  100.0   A
```

#### Bad Baseline: [`bad/test_basic.py`](bad/test_basic.py) ([sidecar JSON](bad/test_basic.py.expected.json))

- **Upstream Dataset / Benchmark:** [pallets/click (tests/test_basic.py)](https://github.com/pallets/click/blob/main/tests/test_basic.py) (`BSD-3-Clause`)
- **Expected Scorecard:** `Composite 26.9/100 (Grade F)` — `SRP: 100.0` | `Size: 21.9` | `Complexity: 100.0` | `Clean: 72.8` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 26.9/100 (Grade F) | Files: 1 (src: 0, test: 1) | Classes: 0 | Functions/Methods: 42
Dimensions -> SRP: 100.0 | Size: 21.9 | Complexity: 100.0 | Clean: 72.8 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/test_basic.py               test    761    - 100.0  21.9 100.0  72.8 100.0   26.9   F
    - Size: file LOC=761 (>350) (-77.8 pts)
    - Clean: 3 mid-file/late import(s) (-12.0 pts)
    - Clean: 3 duplicate code block(s) detected (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/python/bad/test_basic.py:46 test_param_named   17   1    0   5   0   98.5   A
    - Size: params=5 (>4) (-6.0 pts)
samples/python/bad/test_basic.py:969 test_cast_multi    9   2    2   5   1   98.5   A
    - Size: params=5 (>4) (-6.0 pts)
samples/python/bad/test_basic.py:137 test_basic_grou   21   1    0   1   0   99.1   A
    - Clean (Test): 10 assertions in single test (>8) (-6.0 pts)
samples/python/bad/test_basic.py:12 test_basic_funct   15   1    0   1   0  100.0   A
samples/python/bad/test_basic.py:71 test_param_squat    8   1    0   1   0  100.0   A
samples/python/bad/test_basic.py:88 test_option_reus   12   1    0   1   0  100.0   A
samples/python/bad/test_basic.py:109 test_repr         13   1    0   0   0  100.0   A
samples/python/bad/test_basic.py:127 test_return_val    7   1    0   0   0  100.0   A
samples/python/bad/test_basic.py:163 test_group_comm    7   1    0   1   0  100.0   A
samples/python/bad/test_basic.py:175 test_group_from    7   1    0   1   0  100.0   A
samples/python/bad/test_basic.py:197 test_string_opt   11   2    2   3   1  100.0   A
samples/python/bad/test_basic.py:220 test_int_option   11   2    2   3   1  100.0   A
samples/python/bad/test_basic.py:246 test_uuid_optio   13   2    2   3   1  100.0   A
samples/python/bad/test_basic.py:271 test_float_opti   11   2    2   3   1  100.0   A
samples/python/bad/test_basic.py:303 test_boolean_sw    7   1    0   4   0  100.0   A
samples/python/bad/test_basic.py:325 test_boolean_fl    7   1    0   4   0  100.0   A
samples/python/bad/test_basic.py:342 test_boolean_co    9   1    0   3   0  100.0   A
samples/python/bad/test_basic.py:390 test_flag_value    8   1    0   4   0  100.0   A
samples/python/bad/test_basic.py:410 test_file_optio   16   1    0   2   0  100.0   A
samples/python/bad/test_basic.py:431 test_file_lazy_   30   1    0   2   0  100.0   A
samples/python/bad/test_basic.py:471 test_path_optio   32   1    0   2   0  100.0   A
samples/python/bad/test_basic.py:515 test_choice_opt   16   1    0   1   0  100.0   A
samples/python/bad/test_basic.py:536 test_choice_arg   16   1    0   1   0  100.0   A
samples/python/bad/test_basic.py:557 test_choice_arg   21   1    0   1   0  100.0   A
samples/python/bad/test_basic.py:584 test_choice_arg   24   1    0   1   0  100.0   A
samples/python/bad/test_basic.py:615 test_choice_arg   22   1    0   1   0  100.0   A
samples/python/bad/test_basic.py:643 test_choice_arg   15   1    0   1   0  100.0   A
samples/python/bad/test_basic.py:670 test_datetime_a    8   1    0   1   0  100.0   A
samples/python/bad/test_basic.py:683 test_datetime_o   21   1    0   1   0  100.0   A
samples/python/bad/test_basic.py:710 test_datetime_o    8   1    0   1   0  100.0   A
samples/python/bad/test_basic.py:721 test_required_o    8   1    0   1   0  100.0   A
samples/python/bad/test_basic.py:732 test_evaluation   38   1    0   1   0  100.0   A
samples/python/bad/test_basic.py:775 test_hidden_opt    8   1    0   1   0  100.0   A
samples/python/bad/test_basic.py:786 test_hidden_com   10   1    0   1   0  100.0   A
samples/python/bad/test_basic.py:800 test_hidden_gro   14   1    0   1   0  100.0   A
samples/python/bad/test_basic.py:819 test_summary_li   14   1    0   1   0  100.0   A
samples/python/bad/test_basic.py:838 test_help_inval   15   1    0   1   0  100.0   A
samples/python/bad/test_basic.py:855 test_version_op   19   1    0   2   0  100.0   A
samples/python/bad/test_basic.py:885 test_version_op   20   1    0   2   0  100.0   A
samples/python/bad/test_basic.py:914 test_version_op   13   1    0   2   0  100.0   A
samples/python/bad/test_basic.py:935 test_custom_ver    8   1    0   2   0  100.0   A
samples/python/bad/test_basic.py:946 test_custom_ver    8   1    0   1   0  100.0   A
```
