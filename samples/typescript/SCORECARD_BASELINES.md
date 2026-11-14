# TypeScript Code Health Scorecard Baselines

This catalog provides functionally comparable, human-inspectable **Good** and **Bad** pure TypeScript (`framework: auto`, no JSX/UI framework imports) code samples verbatim from established open-source repositories ([`TheAlgorithms/TypeScript`](https://github.com/TheAlgorithms/TypeScript), [`colinhacks/zod`](https://github.com/colinhacks/zod), and [`sindresorhus/ky`](https://github.com/sindresorhus/ky)).

Each sample file `<filename>` has a matching `<filename>.expected.json` sidecar file verified against `CodeHealthRunner` (`lang_override="typescript"`, `framework_override=None`).

---

## Quick Summary Table

| Profile | Scenario | Quality | Sample File | Dataset Source | LOC | SRP | Size | Comp | Clean | Sec | Score | Grade |
| :--- | :--- | :---: | :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| `typescript (auto)` | 1. Graph Shortest-Path Algorithm Complexity & Control Flow (TheAlgorithms/TypeScript) | **GOOD** | [`good/floyd_warshall.ts`](good/floyd_warshall.ts) | [TheAlgorithms/TypeScript (graph/floyd_warshall.ts)](https://github.com/TheAlgorithms/TypeScript/blob/master/graph/floyd_warshall.ts) | 20 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `typescript (auto)` | 1. Graph Shortest-Path Algorithm Complexity & Control Flow (TheAlgorithms/TypeScript) | **BAD** | [`bad/bellman_ford.ts`](bad/bellman_ford.ts) | [TheAlgorithms/TypeScript (graph/bellman_ford.ts)](https://github.com/TheAlgorithms/TypeScript/blob/master/graph/bellman_ford.ts) | 25 | 100.0 | 90.0 | 68.0 | 100.0 | 100.0 | **73.0** | **C** |
| `typescript (auto)` | 2. Graph Traversal Function Size & Nesting (TheAlgorithms/TypeScript) | **GOOD** | [`good/bipartite_graph.ts`](good/bipartite_graph.ts) | [TheAlgorithms/TypeScript (graph/bipartite_graph.ts)](https://github.com/TheAlgorithms/TypeScript/blob/master/graph/bipartite_graph.ts) | 27 | 100.0 | 100.0 | 100.0 | 93.7 | 100.0 | **99.1** | **A** |
| `typescript (auto)` | 2. Graph Traversal Function Size & Nesting (TheAlgorithms/TypeScript) | **BAD** | [`bad/edmonds_karp.ts`](bad/edmonds_karp.ts) | [TheAlgorithms/TypeScript (graph/edmonds_karp.ts)](https://github.com/TheAlgorithms/TypeScript/blob/master/graph/edmonds_karp.ts) | 68 | 79.0 | 0.0 | 14.0 | 90.0 | 100.0 | **5.0** | **F** |
| `typescript (auto)` | 3. Matrix & Combinatorial Math Complexity (TheAlgorithms/TypeScript) | **GOOD** | [`good/pascals_triangle.ts`](good/pascals_triangle.ts) | [TheAlgorithms/TypeScript (maths/pascals_triangle.ts)](https://github.com/TheAlgorithms/TypeScript/blob/master/maths/pascals_triangle.ts) | 20 | 100.0 | 100.0 | 96.0 | 100.0 | 100.0 | **99.2** | **A** |
| `typescript (auto)` | 3. Matrix & Combinatorial Math Complexity (TheAlgorithms/TypeScript) | **BAD** | [`bad/gaussian_elimination.ts`](bad/gaussian_elimination.ts) | [TheAlgorithms/TypeScript (maths/gaussian_elimination.ts)](https://github.com/TheAlgorithms/TypeScript/blob/master/maths/gaussian_elimination.ts) | 39 | 100.0 | 79.0 | 52.5 | 100.0 | 100.0 | **57.5** | **F** |
| `typescript (auto)` | 4. Schema Contract vs. Legacy Error Class Prototype & Cohesion (colinhacks/zod) | **GOOD** | [`good/zod_standard_schema.ts`](good/zod_standard_schema.ts) | [colinhacks/zod (packages/zod/src/v4/core/standard-schema.ts)](https://github.com/colinhacks/zod/blob/main/packages/zod/src/v4/core/standard-schema.ts) | 78 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `typescript (auto)` | 4. Schema Contract vs. Legacy Error Class Prototype & Cohesion (colinhacks/zod) | **BAD** | [`bad/zod_error_legacy.ts`](bad/zod_error_legacy.ts) | [colinhacks/zod (packages/zod/src/v3/ZodError.ts)](https://github.com/colinhacks/zod/blob/main/packages/zod/src/v3/ZodError.ts) | 287 | 56.2 | 90.0 | 87.8 | 68.5 | 75.0 | **61.2** | **D** |
| `typescript (auto)` | 5. JSON Schema Contract Size vs. Monolithic AST Visitor (colinhacks/zod) | **GOOD** | [`good/zod_json_schema.ts`](good/zod_json_schema.ts) | [colinhacks/zod (packages/zod/src/v4/core/json-schema.ts)](https://github.com/colinhacks/zod/blob/main/packages/zod/src/v4/core/json-schema.ts) | 99 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `typescript (auto)` | 5. JSON Schema Contract Size vs. Monolithic AST Visitor (colinhacks/zod) | **BAD** | [`bad/zod_visit.ts`](bad/zod_visit.ts) | [colinhacks/zod (packages/zod/src/v4/core/visit.ts)](https://github.com/colinhacks/zod/blob/main/packages/zod/src/v4/core/visit.ts) | 168 | 85.0 | 0.0 | 0.0 | 93.0 | 100.0 | **5.0** | **F** |
| `typescript (auto)` | 6. Schema Definition Typing Hygiene vs. Registry Escape Hatches (colinhacks/zod) | **GOOD** | [`good/zod_zsf.ts`](good/zod_zsf.ts) | [colinhacks/zod (packages/zod/src/v4/core/zsf.ts)](https://github.com/colinhacks/zod/blob/main/packages/zod/src/v4/core/zsf.ts) | 82 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `typescript (auto)` | 6. Schema Definition Typing Hygiene vs. Registry Escape Hatches (colinhacks/zod) | **BAD** | [`bad/zod_registries.ts`](bad/zod_registries.ts) | [colinhacks/zod (packages/zod/src/v4/core/registries.ts)](https://github.com/colinhacks/zod/blob/main/packages/zod/src/v4/core/registries.ts) | 80 | 100.0 | 100.0 | 100.0 | 73.3 | 100.0 | **78.3** | **C** |
| `typescript (auto)` | 7. HTTP Client Constants Cohesion vs. Monolithic Ky Class SRP (sindresorhus/ky) | **GOOD** | [`good/ky_constants.ts`](good/ky_constants.ts) | [sindresorhus/ky (source/core/constants.ts)](https://github.com/sindresorhus/ky/blob/main/source/core/constants.ts) | 95 | 100.0 | 100.0 | 100.0 | 95.5 | 100.0 | **99.3** | **A** |
| `typescript (auto)` | 7. HTTP Client Constants Cohesion vs. Monolithic Ky Class SRP (sindresorhus/ky) | **BAD** | [`bad/ky_client.ts`](bad/ky_client.ts) | [sindresorhus/ky (source/core/Ky.ts)](https://github.com/sindresorhus/ky/blob/main/source/core/Ky.ts) | 1006 | 22.4 | 0.0 | 15.2 | 79.6 | 100.0 | **5.0** | **F** |
| `typescript (auto)` | 8. HTTP Type Guards vs. Branchy Network Error Classifier (sindresorhus/ky) | **GOOD** | [`good/ky_type_guards.ts`](good/ky_type_guards.ts) | [sindresorhus/ky (source/utils/type-guards.ts)](https://github.com/sindresorhus/ky/blob/main/source/utils/type-guards.ts) | 26 | 100.0 | 100.0 | 100.0 | 97.2 | 100.0 | **99.6** | **A** |
| `typescript (auto)` | 8. HTTP Type Guards vs. Branchy Network Error Classifier (sindresorhus/ky) | **BAD** | [`bad/ky_is_network_error.ts`](bad/ky_is_network_error.ts) | [sindresorhus/ky (source/utils/is-network-error.ts)](https://github.com/sindresorhus/ky/blob/main/source/utils/is-network-error.ts) | 32 | 100.0 | 100.0 | 51.0 | 90.0 | 100.0 | **56.0** | **F** |
| `typescript (auto)` | 9. Request Option Helpers vs. High-Complexity Retry Option Normalizer (sindresorhus/ky) | **GOOD** | [`good/ky_options.ts`](good/ky_options.ts) | [sindresorhus/ky (source/utils/options.ts)](https://github.com/sindresorhus/ky/blob/main/source/utils/options.ts) | 40 | 100.0 | 100.0 | 86.4 | 90.0 | 100.0 | **95.8** | **A** |
| `typescript (auto)` | 9. Request Option Helpers vs. High-Complexity Retry Option Normalizer (sindresorhus/ky) | **BAD** | [`bad/ky_normalize.ts`](bad/ky_normalize.ts) | [sindresorhus/ky (source/utils/normalize.ts)](https://github.com/sindresorhus/ky/blob/main/source/utils/normalize.ts) | 73 | 86.4 | 67.3 | 9.3 | 90.4 | 100.0 | **14.3** | **F** |
| `typescript (auto)` | 10. Vitest Schema Validation Suite vs. Oversized First-Party Switch Test (colinhacks/zod) | **GOOD** | [`good/zod_validations.test.ts`](good/zod_validations.test.ts) | [colinhacks/zod (packages/zod/src/v4/classic/tests/validations.test.ts)](https://github.com/colinhacks/zod/blob/main/packages/zod/src/v4/classic/tests/validations.test.ts) | 254 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `typescript (auto)` | 10. Vitest Schema Validation Suite vs. Oversized First-Party Switch Test (colinhacks/zod) | **BAD** | [`bad/zod_firstparty.test.ts`](bad/zod_firstparty.test.ts) | [colinhacks/zod (packages/zod/src/v3/tests/firstparty.test.ts)](https://github.com/colinhacks/zod/blob/main/packages/zod/src/v3/tests/firstparty.test.ts) | 83 | 100.0 | 55.0 | 0.0 | 60.0 | 100.0 | **5.0** | **F** |

---

## Detailed Scenario Scorecards

### TYPESCRIPT (`--lang typescript`) — 1. Graph Shortest-Path Algorithm Complexity & Control Flow (TheAlgorithms/TypeScript)

#### Good Baseline: [`good/floyd_warshall.ts`](good/floyd_warshall.ts) ([sidecar JSON](good/floyd_warshall.ts.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/TypeScript (graph/floyd_warshall.ts)](https://github.com/TheAlgorithms/TypeScript/blob/master/graph/floyd_warshall.ts) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/good/floyd_warshall.ts      src      20    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/good/floyd_warshall.ts:11 floydWa   20   5    8   1   3  100.0   A
```

#### Bad Baseline: [`bad/bellman_ford.ts`](bad/bellman_ford.ts) ([sidecar JSON](bad/bellman_ford.ts.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/TypeScript (graph/bellman_ford.ts)](https://github.com/TheAlgorithms/TypeScript/blob/master/graph/bellman_ford.ts) (`MIT`)
- **Expected Scorecard:** `Composite 73.0/100 (Grade C)` — `SRP: 100.0` | `Size: 90.0` | `Complexity: 68.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 73.0/100 (Grade C) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 90.0 | Complexity: 68.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/bellman_ford.ts         src      25    - 100.0  90.0  68.0 100.0 100.0   73.0   C

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/bellman_ford.ts:12 bellmanFor   25   8   16   2   4   73.0   C
    - Size: nesting depth=4 (>3) (-10.0 pts)
    - Complexity: CC=8 (>5) (-12.0 pts)
    - Complexity: cognitive=16 (>8) (-20.0 pts)
```

---

### TYPESCRIPT (`--lang typescript`) — 2. Graph Traversal Function Size & Nesting (TheAlgorithms/TypeScript)

#### Good Baseline: [`good/bipartite_graph.ts`](good/bipartite_graph.ts) ([sidecar JSON](good/bipartite_graph.ts.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/TypeScript (graph/bipartite_graph.ts)](https://github.com/TheAlgorithms/TypeScript/blob/master/graph/bipartite_graph.ts) (`MIT`)
- **Expected Scorecard:** `Composite 99.1/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 93.7` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 99.1/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 2
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 93.7 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/good/bipartite_graph.ts     src      27    - 100.0 100.0 100.0  93.7 100.0   99.1   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/good/bipartite_graph.ts:1 dfs       17   4    4   4   2   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/good/bipartite_graph.ts:33 isBipa   10   4    3   1   2  100.0   A
```

#### Bad Baseline: [`bad/edmonds_karp.ts`](bad/edmonds_karp.ts) ([sidecar JSON](bad/edmonds_karp.ts.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/TypeScript (graph/edmonds_karp.ts)](https://github.com/TheAlgorithms/TypeScript/blob/master/graph/edmonds_karp.ts) (`MIT`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 79.0` | `Size: 0.0` | `Complexity: 14.0` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 79.0 | Size: 0.0 | Complexity: 14.0 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/edmonds_karp.ts         src      68    -  79.0   0.0  14.0  90.0 100.0    5.0   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/edmonds_karp.ts:15 edmondsKar   67  13   26   3   5    5.0   F
    - SRP: high external call fan-out=13 (>6) (-21.0 pts)
    - Size: LOC=67 (>25) (-80.0 pts)
    - Size: nesting depth=5 (>3) (-20.0 pts)
    - Complexity: CC=13 (>5) (-41.0 pts)
    - Complexity: cognitive=26 (>8) (-45.0 pts)
    - Clean (TS): 5 non-null assertion(s) ('!') bypass strict null checks (-10.0 pts)
```

---

### TYPESCRIPT (`--lang typescript`) — 3. Matrix & Combinatorial Math Complexity (TheAlgorithms/TypeScript)

#### Good Baseline: [`good/pascals_triangle.ts`](good/pascals_triangle.ts) ([sidecar JSON](good/pascals_triangle.ts.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/TypeScript (maths/pascals_triangle.ts)](https://github.com/TheAlgorithms/TypeScript/blob/master/maths/pascals_triangle.ts) (`MIT`)
- **Expected Scorecard:** `Composite 99.2/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 96.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 99.2/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 96.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/good/pascals_triangle.ts    src      20    - 100.0 100.0  96.0 100.0 100.0   99.2   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/good/pascals_triangle.ts:17 pasca   20   6    8   1   3   99.2   A
    - Complexity: CC=6 (>5) (-4.0 pts)
```

#### Bad Baseline: [`bad/gaussian_elimination.ts`](bad/gaussian_elimination.ts) ([sidecar JSON](bad/gaussian_elimination.ts.expected.json))

- **Upstream Dataset / Benchmark:** [TheAlgorithms/TypeScript (maths/gaussian_elimination.ts)](https://github.com/TheAlgorithms/TypeScript/blob/master/maths/gaussian_elimination.ts) (`MIT`)
- **Expected Scorecard:** `Composite 57.5/100 (Grade F)` — `SRP: 100.0` | `Size: 79.0` | `Complexity: 52.5` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 57.5/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 79.0 | Complexity: 52.5 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/gaussian_elimination.ts src      39    - 100.0  79.0  52.5 100.0 100.0   57.5   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/gaussian_elimination.ts:7 gau   39  10   19   1   3   57.5   F
    - Size: LOC=39 (>25) (-21.0 pts)
    - Complexity: CC=10 (>5) (-20.0 pts)
    - Complexity: cognitive=19 (>8) (-27.5 pts)
```

---

### TYPESCRIPT (`--lang typescript`) — 4. Schema Contract vs. Legacy Error Class Prototype & Cohesion (colinhacks/zod)

#### Good Baseline: [`good/zod_standard_schema.ts`](good/zod_standard_schema.ts) ([sidecar JSON](good/zod_standard_schema.ts.expected.json))

- **Upstream Dataset / Benchmark:** [colinhacks/zod (packages/zod/src/v4/core/standard-schema.ts)](https://github.com/colinhacks/zod/blob/main/packages/zod/src/v4/core/standard-schema.ts) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 0
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/good/zod_standard_schema.ts src      78    - 100.0 100.0 100.0 100.0 100.0  100.0   A
```

#### Bad Baseline: [`bad/zod_error_legacy.ts`](bad/zod_error_legacy.ts) ([sidecar JSON](bad/zod_error_legacy.ts.expected.json))

- **Upstream Dataset / Benchmark:** [colinhacks/zod (packages/zod/src/v3/ZodError.ts)](https://github.com/colinhacks/zod/blob/main/packages/zod/src/v3/ZodError.ts) (`MIT`)
- **Expected Scorecard:** `Composite 61.2/100 (Grade D)` — `SRP: 56.2` | `Size: 90.0` | `Complexity: 87.8` | `Clean: 68.5` | `Security: 75.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 61.2/100 (Grade D) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 10
Dimensions -> SRP: 56.2 | Size: 90.0 | Complexity: 87.8 | Clean: 68.5 | Security: 75.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/zod_error_legacy.ts     src     287    -  56.2  90.0  87.8  68.5  75.0   61.2   D

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/zod_error_legacy.ts:194 Zod   114    9     4   26   59.7   F
    - SRP: LCOM4=4 disconnected method groups (-45.0 pts)
    - Complexity: total class CC=26 (>25) (-1.5 pts)
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/zod_error_legacy.ts:217 ZodEr   52  13   58   1   8    5.0   F
    - SRP: high external call fan-out=7 (>6) (-3.0 pts)
    - Size: LOC=52 (>25) (-42.5 pts)
    - Size: nesting depth=8 (>3) (-50.0 pts)
    - Complexity: CC=13 (>5) (-41.0 pts)
    - Complexity: cognitive=58 (>8) (-100.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
    - Clean (TS): 5 explicit 'any' type usage(s) defeat type safety (-20.0 pts)
    - Clean (TS): 1 non-null assertion(s) ('!') bypass strict null checks (-2.0 pts)
samples/typescript/bad/zod_error_legacy.ts:308 ZodEr   14   4    3   1   2   78.0   C
    - Clean: missing public docstring (-10.0 pts)
    - Clean (TS): 3 explicit 'any' type usage(s) defeat type safety (-15.0 pts)
    - Clean (TS): 1 non-null assertion(s) ('!') bypass strict null checks (-2.0 pts)
samples/typescript/bad/zod_error_legacy.ts:201 ZodEr   11   2    1   1   1   95.2   A
    - Clean: missing public docstring (-10.0 pts)
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
    - Security: direct prototype mutation via '__proto__' (-25.0 pts)
samples/typescript/bad/zod_error_legacy.ts:175 quote    4   1    0   1   0   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript/bad/zod_error_legacy.ts:197 ZodEr    3   1    0   0   0   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript/bad/zod_error_legacy.ts:287 ZodEr    3   1    0   0   0   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript/bad/zod_error_legacy.ts:290 ZodEr    3   1    0   0   0   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript/bad/zod_error_legacy.ts:323 ZodEr    3   1    0   0   0   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript/bad/zod_error_legacy.ts:281 ZodEr    5   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/zod_error_legacy.ts:294 ZodEr    3   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

---

### TYPESCRIPT (`--lang typescript`) — 5. JSON Schema Contract Size vs. Monolithic AST Visitor (colinhacks/zod)

#### Good Baseline: [`good/zod_json_schema.ts`](good/zod_json_schema.ts) ([sidecar JSON](good/zod_json_schema.ts.expected.json))

- **Upstream Dataset / Benchmark:** [colinhacks/zod (packages/zod/src/v4/core/json-schema.ts)](https://github.com/colinhacks/zod/blob/main/packages/zod/src/v4/core/json-schema.ts) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 0
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/good/zod_json_schema.ts     src      99    - 100.0 100.0 100.0 100.0 100.0  100.0   A
```

#### Bad Baseline: [`bad/zod_visit.ts`](bad/zod_visit.ts) ([sidecar JSON](bad/zod_visit.ts.expected.json))

- **Upstream Dataset / Benchmark:** [colinhacks/zod (packages/zod/src/v4/core/visit.ts)](https://github.com/colinhacks/zod/blob/main/packages/zod/src/v4/core/visit.ts) (`MIT`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 85.0` | `Size: 0.0` | `Complexity: 0.0` | `Clean: 93.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 85.0 | Size: 0.0 | Complexity: 0.0 | Clean: 93.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/zod_visit.ts            src     168    -  85.0   0.0   0.0  93.0 100.0    5.0   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/zod_visit.ts:28 visit          155  69   50   2   3    5.0   F
    - SRP: high external call fan-out=11 (>6) (-15.0 pts)
    - Size: LOC=155 (>25) (-100.0 pts)
    - Complexity: CC=69 (>5) (-100.0 pts)
    - Complexity: cognitive=50 (>8) (-100.0 pts)
    - Complexity: returns=18 (>3) (-60.0 pts)
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
    - Clean (TS): 1 non-null assertion(s) ('!') bypass strict null checks (-2.0 pts)
```

---

### TYPESCRIPT (`--lang typescript`) — 6. Schema Definition Typing Hygiene vs. Registry Escape Hatches (colinhacks/zod)

#### Good Baseline: [`good/zod_zsf.ts`](good/zod_zsf.ts) ([sidecar JSON](good/zod_zsf.ts.expected.json))

- **Upstream Dataset / Benchmark:** [colinhacks/zod (packages/zod/src/v4/core/zsf.ts)](https://github.com/colinhacks/zod/blob/main/packages/zod/src/v4/core/zsf.ts) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 0
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/good/zod_zsf.ts             src      82    - 100.0 100.0 100.0 100.0 100.0  100.0   A
```

#### Bad Baseline: [`bad/zod_registries.ts`](bad/zod_registries.ts) ([sidecar JSON](bad/zod_registries.ts.expected.json))

- **Upstream Dataset / Benchmark:** [colinhacks/zod (packages/zod/src/v4/core/registries.ts)](https://github.com/colinhacks/zod/blob/main/packages/zod/src/v4/core/registries.ts) (`MIT`)
- **Expected Scorecard:** `Composite 78.3/100 (Grade C)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 73.3` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 78.3/100 (Grade C) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 6
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 73.3 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/zod_registries.ts       src      80    - 100.0 100.0 100.0  73.3 100.0   78.3   C

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/zod_registries.ts:27 $ZodRe    43    5     1   14   76.8   C
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/zod_registries.ts:33 $ZodRegi   11   4    1   2   1   96.4   A
    - Clean: missing public docstring (-10.0 pts)
    - Clean (TS): 2 explicit 'any' type usage(s) defeat type safety (-10.0 pts)
    - Clean (TS): 2 non-null assertion(s) ('!') bypass strict null checks (-4.0 pts)
samples/typescript/bad/zod_registries.ts:60 $ZodRegi   10   4    3   1   2   97.0   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean (TS): 3 explicit 'any' type usage(s) defeat type safety (-15.0 pts)
samples/typescript/bad/zod_registries.ts:51 $ZodRegi    8   4    1   1   1   98.2   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
    - Clean (TS): 1 non-null assertion(s) ('!') bypass strict null checks (-2.0 pts)
samples/typescript/bad/zod_registries.ts:45 $ZodRegi    5   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/zod_registries.ts:74 $ZodRegi    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/zod_registries.ts:90 registry    3   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

---

### TYPESCRIPT (`--lang typescript`) — 7. HTTP Client Constants Cohesion vs. Monolithic Ky Class SRP (sindresorhus/ky)

#### Good Baseline: [`good/ky_constants.ts`](good/ky_constants.ts) ([sidecar JSON](good/ky_constants.ts.expected.json))

- **Upstream Dataset / Benchmark:** [sindresorhus/ky (source/core/constants.ts)](https://github.com/sindresorhus/ky/blob/main/source/core/constants.ts) (`MIT`)
- **Expected Scorecard:** `Composite 99.3/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 95.5` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 99.3/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 6
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 95.5 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/good/ky_constants.ts        src      95    - 100.0 100.0 100.0  95.5 100.0   99.3   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/good/ky_constants.ts:162 RetryM     9    2     1    2   99.6   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/good/ky_constants.ts:40 validate     1   1    0   0   0   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript/good/ky_constants.ts:263 retry       1   1    0   1   0   98.5   A
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript/good/ky_constants.ts:58 getSuppor    3   2    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/good/ky_constants.ts:170 RetryMar    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/good/ky_constants.ts:175 isRetryM    2   2    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/good/ky_constants.ts:164 RetryMar    3   1    0   0   0  100.0   A
```

#### Bad Baseline: [`bad/ky_client.ts`](bad/ky_client.ts) ([sidecar JSON](bad/ky_client.ts.expected.json))

- **Upstream Dataset / Benchmark:** [sindresorhus/ky (source/core/Ky.ts)](https://github.com/sindresorhus/ky/blob/main/source/core/Ky.ts) (`MIT`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 22.4` | `Size: 0.0` | `Complexity: 15.2` | `Clean: 79.6` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 49
Dimensions -> SRP: 22.4 | Size: 0.0 | Complexity: 15.2 | Clean: 79.6 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/ky_client.ts            src    1006    -  22.4   0.0  15.2  79.6 100.0    5.0   F
    - Size: file LOC=1006 (>350) (-100.0 pts)

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/ky_client.ts:348 Ky           735   32     1  214    5.0   F
    - SRP: methods=32 (>10) (-88.0 pts)
    - Size: class LOC=735 (>200) (-100.0 pts)
    - Complexity: total class CC=214 (>25) (-100.0 pts)
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/ky_client.ts:349 Ky.create      62  19   26   2   4    5.0   F
    - SRP: high external call fan-out=16 (>6) (-30.0 pts)
    - Size: LOC=62 (>25) (-67.5 pts)
    - Size: nesting depth=4 (>3) (-10.0 pts)
    - Complexity: CC=19 (>5) (-83.0 pts)
    - Complexity: cognitive=26 (>8) (-45.0 pts)
    - Complexity: returns=7 (>3) (-16.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
samples/typescript/bad/ky_client.ts:458 Ky.construct   99  40   21   2   3    5.0   F
    - SRP: high external call fan-out=21 (>6) (-36.0 pts)
    - Size: LOC=99 (>25) (-100.0 pts)
    - Complexity: CC=40 (>5) (-100.0 pts)
    - Complexity: cognitive=21 (>8) (-32.5 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:688 Ky.<method>    53  21   22   1   3    5.0   F
    - SRP: high external call fan-out=17 (>6) (-33.0 pts)
    - Size: LOC=53 (>25) (-45.0 pts)
    - Complexity: CC=21 (>5) (-97.0 pts)
    - Complexity: cognitive=22 (>8) (-35.0 pts)
    - Complexity: returns=6 (>3) (-12.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript/bad/ky_client.ts:1125 Ky.<method>   61  15   21   1   4   17.5   F
    - SRP: high external call fan-out=22 (>6) (-36.0 pts)
    - Size: LOC=61 (>25) (-65.0 pts)
    - Size: nesting depth=4 (>3) (-10.0 pts)
    - Complexity: CC=15 (>5) (-55.0 pts)
    - Complexity: cognitive=21 (>8) (-32.5 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:931 Ky.<method>    60  12   23   1   4   21.5   F
    - SRP: high external call fan-out=14 (>6) (-24.0 pts)
    - Size: LOC=60 (>25) (-62.5 pts)
    - Size: nesting depth=4 (>3) (-10.0 pts)
    - Complexity: CC=12 (>5) (-34.0 pts)
    - Complexity: cognitive=23 (>8) (-37.5 pts)
    - Complexity: returns=6 (>3) (-12.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:590 Ky.<method>    48  14   21   0   4   24.5   F
    - SRP: high external call fan-out=17 (>6) (-33.0 pts)
    - Size: LOC=48 (>25) (-34.5 pts)
    - Size: nesting depth=4 (>3) (-10.0 pts)
    - Complexity: CC=14 (>5) (-48.0 pts)
    - Complexity: cognitive=21 (>8) (-32.5 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:136 readResponse   48  12   18   2   3   30.0   F
    - SRP: high external call fan-out=14 (>6) (-24.0 pts)
    - Size: LOC=48 (>25) (-34.5 pts)
    - Complexity: CC=12 (>5) (-34.0 pts)
    - Complexity: cognitive=18 (>8) (-25.0 pts)
    - Complexity: returns=7 (>3) (-16.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:280 applySearchP   26  11   21   2   4   45.5   F
    - Size: LOC=26 (>25) (-1.5 pts)
    - Size: nesting depth=4 (>3) (-10.0 pts)
    - Complexity: CC=11 (>5) (-27.0 pts)
    - Complexity: cognitive=21 (>8) (-32.5 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:881 Ky.<method>    35  10   16   2   4   65.0   D
    - SRP: high external call fan-out=8 (>6) (-6.0 pts)
    - Size: LOC=35 (>25) (-15.0 pts)
    - Size: nesting depth=4 (>3) (-10.0 pts)
    - Complexity: CC=10 (>5) (-20.0 pts)
    - Complexity: cognitive=16 (>8) (-20.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:1218 Ky.<method>   41   9   15   0   3   71.5   C
    - SRP: high external call fan-out=15 (>6) (-27.0 pts)
    - Size: LOC=41 (>25) (-24.0 pts)
    - Complexity: CC=9 (>5) (-16.0 pts)
    - Complexity: cognitive=15 (>8) (-17.5 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:1065 Ky.<method>   36   7   13   1   3   85.8   B
    - SRP: high external call fan-out=11 (>6) (-15.0 pts)
    - Size: LOC=36 (>25) (-16.5 pts)
    - Complexity: CC=7 (>5) (-8.0 pts)
    - Complexity: cognitive=13 (>8) (-12.5 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:814 Ky.<method>    28   7    5   1   1   88.8   B
    - SRP: high external call fan-out=12 (>6) (-18.0 pts)
    - Size: LOC=28 (>25) (-4.5 pts)
    - Complexity: CC=7 (>5) (-8.0 pts)
    - Complexity: returns=5 (>3) (-8.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:765 Ky.<method>    11   3    1   1   1   95.8   A
    - SRP: high external call fan-out=9 (>6) (-9.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:113 isJsonConten   14   7    3   1   1   96.1   A
    - Complexity: CC=7 (>5) (-8.0 pts)
    - Complexity: returns=4 (>3) (-4.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:1041 Ky.<method>   19   5    8   0   3   96.7   A
    - SRP: high external call fan-out=8 (>6) (-6.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:1330 Ky.<method>    8   2    1   2   1   97.5   A
    - SRP: boolean flag parameter with default value (-6.0 pts)
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/ky_client.ts:1287 Ky.<method>   16   4    4   1   2   97.6   A
    - SRP: high external call fan-out=7 (>6) (-3.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:221 validateCall   11   6    4   1   2   97.7   A
    - Complexity: CC=6 (>5) (-4.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:246 resolveInput   20   6    7   3   2   97.7   A
    - Complexity: CC=6 (>5) (-4.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:329 validateJson   14   6    3   2   1   97.7   A
    - Complexity: CC=6 (>5) (-4.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:665 Ky.<method>    16   6    7   2   3   97.7   A
    - Complexity: CC=6 (>5) (-4.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:101 createTextDe   10   4    3   1   2   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: empty catch block swallows exception (-10.0 pts)
samples/typescript/bad/ky_client.ts:218 withAttemptD    1   1    0   1   0   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript/bad/ky_client.ts:70 raceWithTimeo   11   1    0   2   0   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:202 validateTime   11   4    3   2   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:312 cloneInitHoo   11   2    0   1   0   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:783 Ky.<method>    21   5    5   2   2   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:855 Ky.<method>    11   3    2   1   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:1307 Ky.<method>   19   2    1   0   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_client.ts:1013 Ky.<method>    5   2    1   0   1   98.7   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean (TS): 2 non-null assertion(s) ('!') bypass strict null checks (-4.0 pts)
samples/typescript/bad/ky_client.ts:66 getCurrentTim    1   2    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/ky_client.ts:83 cancelReturne    5   3    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/ky_client.ts:90 releaseWhenSe    5   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/ky_client.ts:239 isAbsoluteIn    2   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/ky_client.ts:242 normalizeInp    2   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/ky_client.ts:273 deleteSearch    5   2    1   2   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/ky_client.ts:869 Ky.<method>     8   4    3   0   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/ky_client.ts:1008 Ky.<method>    4   2    1   3   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/ky_client.ts:1020 Ky.<method>    9   3    3   1   2   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/ky_client.ts:1031 Ky.<method>    3   2    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/ky_client.ts:1035 Ky.<method>    5   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/ky_client.ts:1117 Ky.<method>    7   2    1   0   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/ky_client.ts:1277 Ky.<method>    3   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/ky_client.ts:1282 Ky.<method>    3   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/ky_client.ts:1342 Ky.<method>   10   3    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/ky_client.ts:1355 Ky.<method>    3   2    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/ky_client.ts:1359 Ky.<method>    4   1    0   2   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/ky_client.ts:1364 Ky.<method>    4   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/ky_client.ts:1369 Ky.<method>    6   4    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

---

### TYPESCRIPT (`--lang typescript`) — 8. HTTP Type Guards vs. Branchy Network Error Classifier (sindresorhus/ky)

#### Good Baseline: [`good/ky_type_guards.ts`](good/ky_type_guards.ts) ([sidecar JSON](good/ky_type_guards.ts.expected.json))

- **Upstream Dataset / Benchmark:** [sindresorhus/ky (source/utils/type-guards.ts)](https://github.com/sindresorhus/ky/blob/main/source/utils/type-guards.ts) (`MIT`)
- **Expected Scorecard:** `Composite 99.6/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 97.2` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 99.6/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 7
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 97.2 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/good/ky_type_guards.ts      src      26    - 100.0 100.0 100.0  97.2 100.0   99.6   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/good/ky_type_guards.ts:9 isErrorT    2   3    0   2   0   97.0   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean (TS): 3 explicit 'any' type usage(s) defeat type safety (-15.0 pts)
samples/typescript/good/ky_type_guards.ts:36 isKyErr    3   1    0   1   0   99.2   A
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
samples/typescript/good/ky_type_guards.ts:59 isHTTPE    3   1    0   1   0  100.0   A
samples/typescript/good/ky_type_guards.ts:81 isNetwo    3   1    0   1   0  100.0   A
samples/typescript/good/ky_type_guards.ts:103 isTime    3   1    0   1   0  100.0   A
samples/typescript/good/ky_type_guards.ts:130 isForc    3   1    0   1   0  100.0   A
samples/typescript/good/ky_type_guards.ts:153 isResp    3   1    0   1   0  100.0   A
```

#### Bad Baseline: [`bad/ky_is_network_error.ts`](bad/ky_is_network_error.ts) ([sidecar JSON](bad/ky_is_network_error.ts.expected.json))

- **Upstream Dataset / Benchmark:** [sindresorhus/ky (source/utils/is-network-error.ts)](https://github.com/sindresorhus/ky/blob/main/source/utils/is-network-error.ts) (`MIT`)
- **Expected Scorecard:** `Composite 56.0/100 (Grade F)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 51.0` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 56.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 51.0 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/ky_is_network_error.ts  src      32    - 100.0 100.0  51.0  90.0 100.0   56.0   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/ky_is_network_error.ts:15 isR   21  13    4   1   1   56.0   F
    - Complexity: CC=13 (>5) (-41.0 pts)
    - Complexity: returns=5 (>3) (-8.0 pts)
    - Clean: missing public docstring (-10.0 pts)
```

---

### TYPESCRIPT (`--lang typescript`) — 9. Request Option Helpers vs. High-Complexity Retry Option Normalizer (sindresorhus/ky)

#### Good Baseline: [`good/ky_options.ts`](good/ky_options.ts) ([sidecar JSON](good/ky_options.ts.expected.json))

- **Upstream Dataset / Benchmark:** [sindresorhus/ky (source/utils/options.ts)](https://github.com/sindresorhus/ky/blob/main/source/utils/options.ts) (`MIT`)
- **Expected Scorecard:** `Composite 95.8/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 86.4` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 95.8/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 2
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 86.4 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/good/ky_options.ts          src      40    - 100.0 100.0  86.4  90.0 100.0   95.8   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/good/ky_options.ts:32 hasSearchPa   21   8    6   1   1   93.7   A
    - Complexity: CC=8 (>5) (-12.0 pts)
    - Complexity: returns=6 (>3) (-12.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/good/ky_options.ts:5 findUnknownO   16   4    3   1   2   98.5   A
    - Clean: missing public docstring (-10.0 pts)
```

#### Bad Baseline: [`bad/ky_normalize.ts`](bad/ky_normalize.ts) ([sidecar JSON](bad/ky_normalize.ts.expected.json))

- **Upstream Dataset / Benchmark:** [sindresorhus/ky (source/utils/normalize.ts)](https://github.com/sindresorhus/ky/blob/main/source/utils/normalize.ts) (`MIT`)
- **Expected Scorecard:** `Composite 14.3/100 (Grade F)` — `SRP: 86.4` | `Size: 67.3` | `Complexity: 9.3` | `Clean: 90.4` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 14.3/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 4
Dimensions -> SRP: 86.4 | Size: 67.3 | Complexity: 9.3 | Clean: 90.4 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/ky_normalize.ts         src      73    -  86.4  67.3   9.3  90.4 100.0   14.3   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/ky_normalize.ts:37 normalizeR   49  19   20   1   3    5.0   F
    - SRP: high external call fan-out=11 (>6) (-15.0 pts)
    - Size: LOC=49 (>25) (-36.0 pts)
    - Complexity: CC=19 (>5) (-83.0 pts)
    - Complexity: cognitive=20 (>8) (-30.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript/bad/ky_normalize.ts:32 defaultRet    1   1    0   1   0   97.0   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: 1 untyped param(s) (attemptCount) (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript/bad/ky_normalize.ts:6 normalizeRe    2   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript/bad/ky_normalize.ts:14 normalizeR    2   2    1   1   1  100.0   A
```

---

### TYPESCRIPT (`--lang typescript`) — 10. Vitest Schema Validation Suite vs. Oversized First-Party Switch Test (colinhacks/zod)

#### Good Baseline: [`good/zod_validations.test.ts`](good/zod_validations.test.ts) ([sidecar JSON](good/zod_validations.test.ts.expected.json))

- **Upstream Dataset / Benchmark:** [colinhacks/zod (packages/zod/src/v4/classic/tests/validations.test.ts)](https://github.com/colinhacks/zod/blob/main/packages/zod/src/v4/classic/tests/validations.test.ts) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 0, test: 1) | Classes: 0 | Functions/Methods: 13
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/good/zod_validations.test.ts test    254    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/good/zod_validations.test.ts:5 te   36   3    2   0   1  100.0   A
samples/typescript/good/zod_validations.test.ts:45 t   18   2    1   0   1  100.0   A
samples/typescript/good/zod_validations.test.ts:65 t   18   2    1   0   1  100.0   A
samples/typescript/good/zod_validations.test.ts:85 t   18   2    1   0   1  100.0   A
samples/typescript/good/zod_validations.test.ts:105    18   2    1   0   1  100.0   A
samples/typescript/good/zod_validations.test.ts:125    18   2    1   0   1  100.0   A
samples/typescript/good/zod_validations.test.ts:145    18   2    1   0   1  100.0   A
samples/typescript/good/zod_validations.test.ts:165    18   2    1   0   1  100.0   A
samples/typescript/good/zod_validations.test.ts:185    18   2    1   0   1  100.0   A
samples/typescript/good/zod_validations.test.ts:205    18   2    1   0   1  100.0   A
samples/typescript/good/zod_validations.test.ts:225    18   2    1   0   1  100.0   A
samples/typescript/good/zod_validations.test.ts:245    18   2    1   0   1  100.0   A
samples/typescript/good/zod_validations.test.ts:265    18   2    1   0   1  100.0   A
```

#### Bad Baseline: [`bad/zod_firstparty.test.ts`](bad/zod_firstparty.test.ts) ([sidecar JSON](bad/zod_firstparty.test.ts.expected.json))

- **Upstream Dataset / Benchmark:** [colinhacks/zod (packages/zod/src/v3/tests/firstparty.test.ts)](https://github.com/colinhacks/zod/blob/main/packages/zod/src/v3/tests/firstparty.test.ts) (`MIT`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 100.0` | `Size: 55.0` | `Complexity: 0.0` | `Clean: 60.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 0, test: 1) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 55.0 | Complexity: 0.0 | Clean: 60.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/zod_firstparty.test.ts  test     83    - 100.0  55.0   0.0  60.0 100.0    5.0   F
    - Clean (TS): 1 '@ts-ignore'/'@ts-nocheck' directive(s) suppress compiler checks (-10.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript/bad/zod_firstparty.test.ts:7 test   80  37    1   0   1    5.0   F
    - Size: LOC=80 (>40) (-45.0 pts)
    - Complexity: CC=37 (>5) (-100.0 pts)
    - Clean (Test): test has 0 assertions (-30.0 pts)
```

---
