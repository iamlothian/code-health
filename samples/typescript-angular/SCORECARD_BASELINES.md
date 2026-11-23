# Angular Code Health Scorecard Baselines

This catalog provides functionally comparable, verbatim real-world **Good** and **Bad** TypeScript/Angular code samples for the `typescript (--framework angular)` profile across 10 scenarios from [`realworld-apps/angular-realworld-example-app`](https://github.com/realworld-apps/angular-realworld-example-app) and [`OWASP juice-shop/juice-shop`](https://github.com/juice-shop/juice-shop).

Each sample file `<filename>` has a matching `<filename>.expected.json` sidecar file verified against `CodeHealthRunner` and [`manifest.json`](manifest.json).

---

## Quick Summary Table

| Profile | Scenario | Quality | Sample File | Dataset Source | LOC | SRP | Size | Comp | Clean | Sec | Score | Grade |
| :--- | :--- | :---: | :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| `typescript (angular)` | 1. Angular Layout Component vs. OWASP Juice Shop Search XSS & Leak | **GOOD** | [`good/header.component.ts`](good/header.component.ts) | [realworld-apps/angular-realworld-example-app (src/app/core/layout/header.component.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/core/layout/header.component.ts) | 16 | 100.0 | 100.0 | 100.0 | 85.0 | 100.0 | **97.8** | **A** |
| `typescript (angular)` | 1. Angular Layout Component vs. OWASP Juice Shop Search XSS & Leak | **BAD** | [`bad/search_result.component.ts`](bad/search_result.component.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/search-result/search-result.component.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/search-result/search-result.component.ts) | 186 | 36.1 | 96.5 | 98.1 | 64.5 | 65.0 | **41.1** | **F** |
| `typescript (angular)` | 2. Angular Article Preview Component vs. OWASP Juice Shop Complaint Form | **GOOD** | [`good/article_preview.component.ts`](good/article_preview.component.ts) | [realworld-apps/angular-realworld-example-app (src/app/features/article/components/article-preview.component.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/features/article/components/article-preview.component.ts) | 45 | 100.0 | 100.0 | 100.0 | 80.0 | 100.0 | **97.0** | **A** |
| `typescript (angular)` | 2. Angular Article Preview Component vs. OWASP Juice Shop Complaint Form | **BAD** | [`bad/complaint.component.ts`](bad/complaint.component.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/complaint/complaint.component.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/complaint/complaint.component.ts) | 102 | 80.0 | 100.0 | 100.0 | 52.0 | 100.0 | **57.0** | **F** |
| `typescript (angular)` | 3. Angular Favorite Button Component vs. OWASP Juice Shop Score Board | **GOOD** | [`good/favorite_button.component.ts`](good/favorite_button.component.ts) | [realworld-apps/angular-realworld-example-app (src/app/features/article/components/favorite-button.component.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/features/article/components/favorite-button.component.ts) | 73 | 95.5 | 98.5 | 100.0 | 80.0 | 100.0 | **95.3** | **A** |
| `typescript (angular)` | 3. Angular Favorite Button Component vs. OWASP Juice Shop Score Board | **BAD** | [`bad/score_board.component.ts`](bad/score_board.component.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/score-board/score-board.component.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/score-board/score-board.component.ts) | 217 | 29.0 | 98.6 | 79.0 | 65.4 | 65.0 | **34.0** | **F** |
| `typescript (angular)` | 4. Angular Articles Service vs. OWASP Juice Shop WebSocket Chat Service Complexity | **GOOD** | [`good/articles.service.ts`](good/articles.service.ts) | [realworld-apps/angular-realworld-example-app (src/app/features/article/services/articles.service.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/features/article/services/articles.service.ts) | 42 | 100.0 | 100.0 | 100.0 | 79.4 | 100.0 | **96.9** | **A** |
| `typescript (angular)` | 4. Angular Articles Service vs. OWASP Juice Shop WebSocket Chat Service Complexity | **BAD** | [`bad/chat.service.ts`](bad/chat.service.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/Services/chat.service.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/Services/chat.service.ts) | 88 | 88.0 | 12.5 | 0.0 | 75.0 | 100.0 | **5.0** | **F** |
| `typescript (angular)` | 5. Angular Article Comment Component vs. OWASP Juice Shop Monolithic Product Component | **GOOD** | [`good/article_comment.component.ts`](good/article_comment.component.ts) | [realworld-apps/angular-realworld-example-app (src/app/features/article/components/article-comment.component.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/features/article/components/article-comment.component.ts) | 48 | 100.0 | 100.0 | 100.0 | 85.0 | 100.0 | **97.8** | **A** |
| `typescript (angular)` | 5. Angular Article Comment Component vs. OWASP Juice Shop Monolithic Product Component | **BAD** | [`bad/product.component.ts`](bad/product.component.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/product/product.component.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/product/product.component.ts) | 201 | 74.0 | 50.0 | 96.0 | 33.8 | 100.0 | **38.8** | **F** |
| `typescript (angular)` | 6. Angular Auth Component Hygiene vs. OWASP Juice Shop OAuth Component | **GOOD** | [`good/auth.component.ts`](good/auth.component.ts) | [realworld-apps/angular-realworld-example-app (src/app/core/auth/auth.component.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/core/auth/auth.component.ts) | 80 | 89.0 | 100.0 | 100.0 | 77.7 | 100.0 | **93.4** | **A** |
| `typescript (angular)` | 6. Angular Auth Component Hygiene vs. OWASP Juice Shop OAuth Component | **BAD** | [`bad/oauth.component.ts`](bad/oauth.component.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/oauth/oauth.component.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/oauth/oauth.component.ts) | 70 | 89.5 | 100.0 | 100.0 | 45.5 | 100.0 | **50.5** | **F** |
| `typescript (angular)` | 7. Angular Settings Component vs. OWASP Juice Shop Administration XSS Sinks | **GOOD** | [`good/settings.component.ts`](good/settings.component.ts) | [realworld-apps/angular-realworld-example-app (src/app/features/settings/settings.component.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/features/settings/settings.component.ts) | 71 | 99.2 | 100.0 | 100.0 | 77.5 | 100.0 | **96.4** | **A** |
| `typescript (angular)` | 7. Angular Settings Component vs. OWASP Juice Shop Administration XSS Sinks | **BAD** | [`bad/administration.component.ts`](bad/administration.component.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/administration/administration.component.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/administration/administration.component.ts) | 123 | 64.0 | 100.0 | 100.0 | 50.3 | 65.0 | **55.3** | **F** |
| `typescript (angular)` | 8. Angular Cohesive Comments Service vs. OWASP Juice Shop Disconnected Storage Service | **GOOD** | [`good/comments.service.ts`](good/comments.service.ts) | [realworld-apps/angular-realworld-example-app (src/app/features/article/services/comments.service.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/features/article/services/comments.service.ts) | 22 | 100.0 | 100.0 | 100.0 | 81.2 | 100.0 | **97.2** | **A** |
| `typescript (angular)` | 8. Angular Cohesive Comments Service vs. OWASP Juice Shop Disconnected Storage Service | **BAD** | [`bad/conversation_storage.service.ts`](bad/conversation_storage.service.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/Services/conversation-storage.service.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/Services/conversation-storage.service.ts) | 42 | 55.0 | 100.0 | 100.0 | 80.0 | 100.0 | **60.0** | **D** |
| `typescript (angular)` | 9. OWASP Juice Shop Score Board Query Param Helpers vs. Challenge Filtering Complexity | **GOOD** | [`good/query_params_converters.ts`](good/query_params_converters.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/score-board/filter-settings/query-params-converters.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/score-board/filter-settings/query-params-converters.ts) | 37 | 95.7 | 100.0 | 92.0 | 82.9 | 100.0 | **94.5** | **A** |
| `typescript (angular)` | 9. OWASP Juice Shop Score Board Query Param Helpers vs. Challenge Filtering Complexity | **BAD** | [`bad/challenge_filtering.ts`](bad/challenge_filtering.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/score-board/helpers/challenge-filtering.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/score-board/helpers/challenge-filtering.ts) | 98 | 69.7 | 15.8 | 15.2 | 86.0 | 100.0 | **20.2** | **F** |
| `typescript (angular)` | 10. Angular User Service Spec vs. OWASP Juice Shop Oversized Navbar Spec | **GOOD** | [`good/user.service.spec.ts`](good/user.service.spec.ts) | [realworld-apps/angular-realworld-example-app (src/app/core/auth/services/user.service.spec.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/core/auth/services/user.service.spec.ts) | 325 | 100.0 | 100.0 | 100.0 | 75.0 | 100.0 | **96.2** | **A** |
| `typescript (angular)` | 10. Angular User Service Spec vs. OWASP Juice Shop Oversized Navbar Spec | **BAD** | [`bad/navbar.component.spec.ts`](bad/navbar.component.spec.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/navbar/navbar.component.spec.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/navbar/navbar.component.spec.ts) | 519 | 100.0 | 74.7 | 100.0 | 94.3 | 100.0 | **79.5** | **C** |

---

## Detailed Scenario Scorecards

### TYPESCRIPT (`--framework angular`) — 1. Angular Layout Component vs. OWASP Juice Shop Search XSS & Leak

#### Good Baseline: [`good/header.component.ts`](good/header.component.ts) ([sidecar JSON](good/header.component.ts.expected.json))

- **Upstream Dataset / Benchmark:** [realworld-apps/angular-realworld-example-app (src/app/core/layout/header.component.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/core/layout/header.component.ts) (`MIT`)
- **Expected Scorecard:** `Composite 97.8/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 85.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 97.8/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 0
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 85.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/header.component.ts src      16    - 100.0 100.0 100.0  85.0 100.0   97.8   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/header.component.t     5    0     1    0   97.8   A
    - Clean: missing class docstring (-15.0 pts)
```

#### Bad Baseline: [`bad/search_result.component.ts`](bad/search_result.component.ts) ([sidecar JSON](bad/search_result.component.ts.expected.json))

- **Upstream Dataset / Benchmark:** [OWASP juice-shop/juice-shop (frontend/src/app/search-result/search-result.component.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/search-result/search-result.component.ts) (`MIT`)
- **Expected Scorecard:** `Composite 41.1/100 (Grade F)` — `SRP: 36.1` | `Size: 96.5` | `Complexity: 98.1` | `Clean: 64.5` | `Security: 65.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 41.1/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 10
Dimensions -> SRP: 36.1 | Size: 96.5 | Complexity: 98.1 | Clean: 64.5 | Security: 65.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/search_result.component.ts src     186    -  36.1  96.5  98.1  64.5  65.0   41.1   F
    - Clean (DRY): DRY-001 (type2, 40 toks, 5 LOC) L37-41 in <module> matches samples/typescript-angular/bad/search_result.component.ts:42-46 (<module>) (-4.0 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 5/186 (2.7%) | DRY Score: 96.0/100 | Clone Groups: 1 (T1: 0, T2: 1, T3: 0 | intra: 1, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type2  100.0% intra_file      5 samples/typescript-angular/bad/search_result.component.ts:L37-41, samples/typescript-angular/bad/search_result.component.ts:L42-46

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/search_result.compo   160   10     3   26   41.1   F
    - SRP: self attributes=22 (>7) (-60.0 pts)
    - Complexity: total class CC=26 (>25) (-1.5 pts)
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/search_result.compone    5   2    1   1   1   70.0   C
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
    - Security (Angular): unsafe XSS/DOM sink 'bypassSecurityTrustHtml' at L113 (-35.0 pts)
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
samples/typescript-angular/bad/search_result.compone   25   4    5   0   2   70.0   C
    - SRP: high external call fan-out=8 (>6) (-6.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
    - Security (Angular): unsafe XSS/DOM sink 'bypassSecurityTrustHtml' at L146 (-35.0 pts)
samples/typescript-angular/bad/search_result.compone   48   6    5   0   2   70.5   C
    - SRP: high external call fan-out=17 (>6) (-33.0 pts)
    - Size: LOC=48 (>25) (-34.5 pts)
    - Complexity: CC=6 (>5) (-4.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-angular/bad/search_result.compone   14   5    4   0   1   97.0   A
    - Clean: missing public docstring (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-angular/bad/search_result.compone   15   2    1   1   1   97.0   A
    - Clean: missing public docstring (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-angular/bad/search_result.compone   10   2    1   0   1   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-angular/bad/search_result.compone    7   2    1   0   1   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-angular/bad/search_result.compone    6   1    0   1   0   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-angular/bad/search_result.compone    3   1    0   0   0   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-angular/bad/search_result.compone    3   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

---

### TYPESCRIPT (`--framework angular`) — 2. Angular Article Preview Component vs. OWASP Juice Shop Complaint Form

#### Good Baseline: [`good/article_preview.component.ts`](good/article_preview.component.ts) ([sidecar JSON](good/article_preview.component.ts.expected.json))

- **Upstream Dataset / Benchmark:** [realworld-apps/angular-realworld-example-app (src/app/features/article/components/article-preview.component.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/features/article/components/article-preview.component.ts) (`MIT`)
- **Expected Scorecard:** `Composite 97.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 80.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 97.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 2
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 80.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/article_preview.component.ts src      45    - 100.0 100.0 100.0  80.0 100.0   97.0   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/article_preview.co    14    2     1    3   97.0   A
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/article_preview.comp    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript-angular/good/article_preview.comp    7   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

#### Bad Baseline: [`bad/complaint.component.ts`](bad/complaint.component.ts) ([sidecar JSON](bad/complaint.component.ts.expected.json))

- **Upstream Dataset / Benchmark:** [OWASP juice-shop/juice-shop (frontend/src/app/complaint/complaint.component.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/complaint/complaint.component.ts) (`MIT`)
- **Expected Scorecard:** `Composite 57.0/100 (Grade F)` — `SRP: 80.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 52.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 57.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 5
Dimensions -> SRP: 80.0 | Size: 100.0 | Complexity: 100.0 | Clean: 52.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/complaint.component.ts src     102    -  80.0 100.0 100.0  52.0 100.0   57.0   F

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/complaint.component    80    5     1    6   57.0   F
    - SRP: self attributes=12 (>7) (-20.0 pts)
    - Clean: missing class docstring (-15.0 pts)
    - Clean (Angular): unmanaged .subscribe() at L71 without takeUntilDestroyed/takeUntil/DestroyRef/ngOnDestroy (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/complaint.component.t   14   1    0   0   0   96.2   A
    - Clean: missing public docstring (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
samples/typescript-angular/bad/complaint.component.t   19   1    0   0   0   96.2   A
    - Clean: missing public docstring (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
samples/typescript-angular/bad/complaint.component.t    8   2    1   0   1   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-angular/bad/complaint.component.t    6   1    0   0   0   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-angular/bad/complaint.component.t   14   1    0   0   0   98.5   A
    - Clean: missing public docstring (-10.0 pts)
```

---

### TYPESCRIPT (`--framework angular`) — 3. Angular Favorite Button Component vs. OWASP Juice Shop Score Board

#### Good Baseline: [`good/favorite_button.component.ts`](good/favorite_button.component.ts) ([sidecar JSON](good/favorite_button.component.ts.expected.json))

- **Upstream Dataset / Benchmark:** [realworld-apps/angular-realworld-example-app (src/app/features/article/components/favorite-button.component.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/features/article/components/favorite-button.component.ts) (`MIT`)
- **Expected Scorecard:** `Composite 95.3/100 (Grade A)` — `SRP: 95.5` | `Size: 98.5` | `Complexity: 100.0` | `Clean: 80.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 95.3/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 2
Dimensions -> SRP: 95.5 | Size: 98.5 | Complexity: 100.0 | Clean: 80.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/favorite_button.component.ts src      73    -  95.5  98.5 100.0  80.0 100.0   95.3   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/favorite_button.co    38    2     1    4   95.3   A
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/favorite_button.comp   27   3    2   0   1   95.0   A
    - SRP: high external call fan-out=9 (>6) (-9.0 pts)
    - Size: LOC=27 (>25) (-3.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript-angular/good/favorite_button.comp    5   1    0   3   0  100.0   A
```

#### Bad Baseline: [`bad/score_board.component.ts`](bad/score_board.component.ts) ([sidecar JSON](bad/score_board.component.ts.expected.json))

- **Upstream Dataset / Benchmark:** [OWASP juice-shop/juice-shop (frontend/src/app/score-board/score-board.component.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/score-board/score-board.component.ts) (`MIT`)
- **Expected Scorecard:** `Composite 34.0/100 (Grade F)` — `SRP: 29.0` | `Size: 98.6` | `Complexity: 79.0` | `Clean: 65.4` | `Security: 65.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 34.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 12
Dimensions -> SRP: 29.0 | Size: 98.6 | Complexity: 79.0 | Clean: 65.4 | Security: 65.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/score_board.component.ts src     217    -  29.0  98.6  79.0  65.4  65.0   34.0   F
    - Clean (DRY): DRY-001 (type2, 101 toks, 16 LOC) L186-201 in ScoreBoardComponent.checkTagHighlight matches samples/typescript-angular/bad/score_board.component.ts:203-218 (ScoreBoardComponent.checkTagHighlight) (-4.0 pts)
    - Clean (DRY): DRY-002 (type3, 96.1%, 44 toks, 8 LOC) L134-142 in ScoreBoardComponent.onChallengeSolvedWebsocket matches samples/typescript-angular/bad/score_board.component.ts:154-162 (ScoreBoardComponent.onCodeChallengeSolvedWebsocket) (-3.0 pts)
    - Clean (DRY): duplication_ratio=11.1% (>10.0%) (-0.5 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 24/217 (11.1%) | DRY Score: 92.5/100 | Clone Groups: 2 (T1: 0, T2: 1, T3: 1 | intra: 2, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type2  100.0% intra_file     16 samples/typescript-angular/bad/score_board.component.ts:L186-201, samples/typescript-angular/bad/score_board.component.ts:L203-218
DRY-002  type3   96.1% intra_file      8 samples/typescript-angular/bad/score_board.component.ts:L134-142, samples/typescript-angular/bad/score_board.component.ts:L154-162

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/score_board.compone   175   12     3   36   34.0   F
    - SRP: methods=12 (>10) (-8.0 pts)
    - SRP: self attributes=22 (>7) (-60.0 pts)
    - Complexity: total class CC=36 (>25) (-16.5 pts)
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/score_board.component   36  12   16   0   3   51.0   F
    - Size: LOC=36 (>25) (-16.5 pts)
    - Complexity: CC=12 (>5) (-34.0 pts)
    - Complexity: cognitive=16 (>8) (-20.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript-angular/bad/score_board.component   25   5    1   0   1   70.0   C
    - SRP: high external call fan-out=17 (>6) (-33.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Security (Angular): unsafe XSS/DOM sink 'bypassSecurityTrustHtml' at L103 (-35.0 pts)
samples/typescript-angular/bad/score_board.component   16   3    2   1   1   97.0   A
    - Clean: missing public docstring (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-angular/bad/score_board.component   16   3    2   1   1   97.0   A
    - Clean: missing public docstring (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-angular/bad/score_board.component    5   1    0   1   0   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-angular/bad/score_board.component    5   1    0   0   0   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-angular/bad/score_board.component    4   1    0   1   0   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-angular/bad/score_board.component    9   2    0   2   0   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-angular/bad/score_board.component   10   1    0   0   0   98.3   A
    - SRP: high external call fan-out=7 (>6) (-3.0 pts)
    - Clean: missing public docstring (-5.0 pts)
samples/typescript-angular/bad/score_board.component   13   4    3   0   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/typescript-angular/bad/score_board.component    9   2    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript-angular/bad/score_board.component    3   1    0   2   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

---

### TYPESCRIPT (`--framework angular`) — 4. Angular Articles Service vs. OWASP Juice Shop WebSocket Chat Service Complexity

#### Good Baseline: [`good/articles.service.ts`](good/articles.service.ts) ([sidecar JSON](good/articles.service.ts.expected.json))

- **Upstream Dataset / Benchmark:** [realworld-apps/angular-realworld-example-app (src/app/features/article/services/articles.service.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/features/article/services/articles.service.ts) (`MIT`)
- **Expected Scorecard:** `Composite 96.9/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 79.4` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 96.9/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 8
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 79.4 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/articles.service.ts src      42    - 100.0 100.0 100.0  79.4 100.0   96.9   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/articles.service.t    35    8     1    9   96.9   A
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/articles.service.ts:   10   2    1   1   1   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean (TS): 1 '@ts-ignore'/'@ts-nocheck' directive(s) suppress compiler checks (-10.0 pts)
samples/typescript-angular/good/articles.service.ts:    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript-angular/good/articles.service.ts:    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript-angular/good/articles.service.ts:    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript-angular/good/articles.service.ts:    7   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript-angular/good/articles.service.ts:    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript-angular/good/articles.service.ts:    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript-angular/good/articles.service.ts:    1   1    0   1   0  100.0   A
```

#### Bad Baseline: [`bad/chat.service.ts`](bad/chat.service.ts) ([sidecar JSON](bad/chat.service.ts.expected.json))

- **Upstream Dataset / Benchmark:** [OWASP juice-shop/juice-shop (frontend/src/app/Services/chat.service.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/Services/chat.service.ts) (`MIT`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 88.0` | `Size: 12.5` | `Complexity: 0.0` | `Clean: 75.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 1
Dimensions -> SRP: 88.0 | Size: 12.5 | Complexity: 0.0 | Clean: 75.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/chat.service.ts src      88    -  88.0  12.5   0.0  75.0 100.0    5.0   F

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/chat.service.ts:26     71    1     1   18    5.0   F
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/chat.service.ts:31 Ch   66  18   34   1   4    5.0   F
    - SRP: high external call fan-out=10 (>6) (-12.0 pts)
    - Size: LOC=66 (>25) (-77.5 pts)
    - Size: nesting depth=4 (>3) (-10.0 pts)
    - Complexity: CC=18 (>5) (-76.0 pts)
    - Complexity: cognitive=34 (>8) (-65.0 pts)
    - Clean: missing public docstring (-10.0 pts)
```

---

### TYPESCRIPT (`--framework angular`) — 5. Angular Article Comment Component vs. OWASP Juice Shop Monolithic Product Component

#### Good Baseline: [`good/article_comment.component.ts`](good/article_comment.component.ts) ([sidecar JSON](good/article_comment.component.ts.expected.json))

- **Upstream Dataset / Benchmark:** [realworld-apps/angular-realworld-example-app (src/app/features/article/components/article-comment.component.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/features/article/components/article-comment.component.ts) (`MIT`)
- **Expected Scorecard:** `Composite 97.8/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 85.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 97.8/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 0
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 85.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/article_comment.component.ts src      48    - 100.0 100.0 100.0  85.0 100.0   97.8   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/article_comment.co     7    0     1    0   97.8   A
    - Clean: missing class docstring (-15.0 pts)
```

#### Bad Baseline: [`bad/product.component.ts`](bad/product.component.ts) ([sidecar JSON](bad/product.component.ts.expected.json))

- **Upstream Dataset / Benchmark:** [OWASP juice-shop/juice-shop (frontend/src/app/product/product.component.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/product/product.component.ts) (`MIT`)
- **Expected Scorecard:** `Composite 38.8/100 (Grade F)` — `SRP: 74.0` | `Size: 50.0` | `Complexity: 96.0` | `Clean: 33.8` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 38.8/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 2
Dimensions -> SRP: 74.0 | Size: 50.0 | Complexity: 96.0 | Clean: 33.8 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/product.component.ts src     201    -  74.0  50.0  96.0  33.8 100.0   38.8   F
    - Clean (DRY): DRY-001 (type3, 80.0%, 104 toks, 10 LOC) L76-85 in ProductComponent.addToBasket matches samples/typescript-angular/bad/product.component.ts:119-146 (ProductComponent.addToBasket), samples/typescript-angular/bad/product.component.ts:173-197 (ProductComponent.addToBasket) (-6.0 pts)
    - Clean (DRY): duplication_ratio=26.4% (>10.0%) (-8.2 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 53/201 (26.4%) | DRY Score: 85.8/100 | Clone Groups: 1 (T1: 0, T2: 0, T3: 1 | intra: 1, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type3   80.0% intra_file     28 samples/typescript-angular/bad/product.component.ts:L76-85, samples/typescript-angular/bad/product.component.ts:L119-146, samples/typescript-angular/bad/product.component.ts:L173-197

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/product.component.t   180    2     1    8   53.0   F
    - SRP: self attributes=9 (>7) (-8.0 pts)
    - Clean: missing class docstring (-15.0 pts)
    - Clean (Angular): unmanaged .subscribe() at L76 without takeUntilDestroyed/takeUntil/DestroyRef/ngOnDestroy (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/product.component.ts:  149   7    8   1   2    5.0   F
    - SRP: high external call fan-out=31 (>6) (-36.0 pts)
    - Size: LOC=149 (>25) (-100.0 pts)
    - Complexity: CC=7 (>5) (-8.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
    - Clean: 2 loose equality comparison(s) (==/!=) trigger implicit type coercion (prefer ===/!==) (-4.0 pts)
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
samples/typescript-angular/bad/product.component.ts:    9   1    0   1   0   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
```

---

### TYPESCRIPT (`--framework angular`) — 6. Angular Auth Component Hygiene vs. OWASP Juice Shop OAuth Component

#### Good Baseline: [`good/auth.component.ts`](good/auth.component.ts) ([sidecar JSON](good/auth.component.ts.expected.json))

- **Upstream Dataset / Benchmark:** [realworld-apps/angular-realworld-example-app (src/app/core/auth/auth.component.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/core/auth/auth.component.ts) (`MIT`)
- **Expected Scorecard:** `Composite 93.4/100 (Grade A)` — `SRP: 89.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 77.7` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 93.4/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 3
Dimensions -> SRP: 89.0 | Size: 100.0 | Complexity: 100.0 | Clean: 77.7 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/auth.component.ts src      80    -  89.0 100.0 100.0  77.7 100.0   93.4   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/auth.component.ts:    62    3     1    7   93.4   A
    - SRP: self attributes=9 (>7) (-8.0 pts)
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/auth.component.ts:60   25   3    2   0   1   95.8   A
    - SRP: high external call fan-out=9 (>6) (-9.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript-angular/good/auth.component.ts:46   13   3    2   0   1   98.2   A
    - Clean: missing public docstring (-10.0 pts)
    - Clean (TS): 1 non-null assertion(s) ('!') bypass strict null checks (-2.0 pts)
samples/typescript-angular/good/auth.component.ts:29   16   1    0   3   0  100.0   A
```

#### Bad Baseline: [`bad/oauth.component.ts`](bad/oauth.component.ts) ([sidecar JSON](bad/oauth.component.ts.expected.json))

- **Upstream Dataset / Benchmark:** [OWASP juice-shop/juice-shop (frontend/src/app/oauth/oauth.component.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/oauth/oauth.component.ts) (`MIT`)
- **Expected Scorecard:** `Composite 50.5/100 (Grade F)` — `SRP: 89.5` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 45.5` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 50.5/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 4
Dimensions -> SRP: 89.5 | Size: 100.0 | Complexity: 100.0 | Clean: 45.5 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/oauth.component.ts src      70    -  89.5 100.0 100.0  45.5 100.0   50.5   F
    - Clean (DRY): DRY-001 (type1, 42 toks, 8 LOC) L37-44 in OAuthComponent.ngOnInit matches samples/typescript-angular/bad/oauth.component.ts:55-62 (OAuthComponent.login) (-5.0 pts)
    - Clean (DRY): duplication_ratio=11.4% (>10.0%) (-0.7 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 8/70 (11.4%) | DRY Score: 94.3/100 | Clone Groups: 1 (T1: 1, T2: 0, T3: 0 | intra: 1, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type1  100.0% intra_file      8 samples/typescript-angular/bad/oauth.component.ts:L37-44, samples/typescript-angular/bad/oauth.component.ts:L55-62

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/oauth.component.ts:    57    4     1    5   56.2   F
    - Clean: missing class docstring (-15.0 pts)
    - Clean (Angular): unmanaged .subscribe() at L29 without takeUntilDestroyed/takeUntil/DestroyRef/ngOnDestroy (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/oauth.component.ts:46   17   1    0   1   0   90.0   A
    - SRP: high external call fan-out=13 (>6) (-21.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
samples/typescript-angular/bad/oauth.component.ts:28   17   1    0   0   0   91.5   A
    - SRP: high external call fan-out=13 (>6) (-21.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
samples/typescript-angular/bad/oauth.component.ts:71   10   2    1   0   1   97.0   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
samples/typescript-angular/bad/oauth.component.ts:64    6   1    0   1   0   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
```

---

### TYPESCRIPT (`--framework angular`) — 7. Angular Settings Component vs. OWASP Juice Shop Administration XSS Sinks

#### Good Baseline: [`good/settings.component.ts`](good/settings.component.ts) ([sidecar JSON](good/settings.component.ts.expected.json))

- **Upstream Dataset / Benchmark:** [realworld-apps/angular-realworld-example-app (src/app/features/settings/settings.component.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/features/settings/settings.component.ts) (`MIT`)
- **Expected Scorecard:** `Composite 96.4/100 (Grade A)` — `SRP: 99.2` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 77.5` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 96.4/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 4
Dimensions -> SRP: 99.2 | Size: 100.0 | Complexity: 100.0 | Clean: 77.5 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/settings.component.ts src      71    -  99.2 100.0 100.0  77.5 100.0   96.4   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/settings.component    50    4     1    8   96.4   A
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/settings.component.t   17   2    1   0   1   96.1   A
    - SRP: high external call fan-out=7 (>6) (-3.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-angular/good/settings.component.t   10   4    1   0   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript-angular/good/settings.component.t    3   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript-angular/good/settings.component.t    4   1    0   2   0  100.0   A
```

#### Bad Baseline: [`bad/administration.component.ts`](bad/administration.component.ts) ([sidecar JSON](bad/administration.component.ts.expected.json))

- **Upstream Dataset / Benchmark:** [OWASP juice-shop/juice-shop (frontend/src/app/administration/administration.component.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/administration/administration.component.ts) (`MIT`)
- **Expected Scorecard:** `Composite 55.3/100 (Grade F)` — `SRP: 64.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 50.3` | `Security: 65.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 55.3/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 9
Dimensions -> SRP: 64.0 | Size: 100.0 | Complexity: 100.0 | Clean: 50.3 | Security: 65.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/administration.component.ts src     123    -  64.0 100.0 100.0  50.3  65.0   55.3   F
    - Clean (DRY): DRY-001 (type3, 76.1%, 129 toks, 18 LOC) L68-85 in AdministrationComponent.findAllUsers matches samples/typescript-angular/bad/administration.component.ts:92-103 (AdministrationComponent.findAllFeedbacks) (-3.0 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 12/123 (9.8%) | DRY Score: 97.0/100 | Clone Groups: 1 (T1: 0, T2: 0, T3: 1 | intra: 1, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type3   76.1% intra_file     18 samples/typescript-angular/bad/administration.component.ts:L68-85, samples/typescript-angular/bad/administration.component.ts:L92-103

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/administration.comp    97    9     3   13   58.3   F
    - SRP: self attributes=16 (>7) (-36.0 pts)
    - Clean: missing class docstring (-15.0 pts)
    - Clean (Angular): unmanaged .subscribe() at L69 without takeUntilDestroyed/takeUntil/DestroyRef/ngOnDestroy (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/administration.compon   18   3    3   0   2   70.0   C
    - Clean: missing public docstring (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
    - Security (Angular): unsafe XSS/DOM sink 'bypassSecurityTrustHtml' at L74 (-35.0 pts)
samples/typescript-angular/bad/administration.compon   17   2    1   0   1   70.0   C
    - Clean: missing public docstring (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
    - Security (Angular): unsafe XSS/DOM sink 'bypassSecurityTrustHtml' at L92 (-35.0 pts)
samples/typescript-angular/bad/administration.compon    6   1    0   1   0   97.0   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
samples/typescript-angular/bad/administration.compon   11   1    0   1   0   97.0   A
    - Clean: missing public docstring (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-angular/bad/administration.compon    8   1    0   2   0   97.0   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
samples/typescript-angular/bad/administration.compon    7   1    0   1   0   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-angular/bad/administration.compon    3   1    0   1   0   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-angular/bad/administration.compon    4   2    0   1   0   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-angular/bad/administration.compon    5   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

---

### TYPESCRIPT (`--framework angular`) — 8. Angular Cohesive Comments Service vs. OWASP Juice Shop Disconnected Storage Service

#### Good Baseline: [`good/comments.service.ts`](good/comments.service.ts) ([sidecar JSON](good/comments.service.ts.expected.json))

- **Upstream Dataset / Benchmark:** [realworld-apps/angular-realworld-example-app (src/app/features/article/services/comments.service.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/features/article/services/comments.service.ts) (`MIT`)
- **Expected Scorecard:** `Composite 97.2/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 81.2` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 97.2/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 4
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 81.2 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/comments.service.ts src      22    - 100.0 100.0 100.0  81.2 100.0   97.2   A

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/comments.service.t    16    4     1    4   97.2   A
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/comments.service.ts:    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript-angular/good/comments.service.ts:    7   1    0   2   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript-angular/good/comments.service.ts:    3   1    0   2   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript-angular/good/comments.service.ts:    1   1    0   1   0  100.0   A
```

#### Bad Baseline: [`bad/conversation_storage.service.ts`](bad/conversation_storage.service.ts) ([sidecar JSON](bad/conversation_storage.service.ts.expected.json))

- **Upstream Dataset / Benchmark:** [OWASP juice-shop/juice-shop (frontend/src/app/Services/conversation-storage.service.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/Services/conversation-storage.service.ts) (`MIT`)
- **Expected Scorecard:** `Composite 60.0/100 (Grade D)` — `SRP: 55.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 80.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 60.0/100 (Grade D) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 7
Dimensions -> SRP: 55.0 | Size: 100.0 | Complexity: 100.0 | Clean: 80.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/conversation_storage.service.ts src      42    -  55.0 100.0 100.0  80.0 100.0   60.0   D

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/conversation_storag    36    7     4   10   60.0   D
    - SRP: LCOM4=4 disconnected method groups (-45.0 pts)
    - Clean: missing class docstring (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/conversation_storage.    5   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript-angular/bad/conversation_storage.    3   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript-angular/bad/conversation_storage.    6   2    1   0   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript-angular/bad/conversation_storage.    3   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript-angular/bad/conversation_storage.   10   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript-angular/bad/conversation_storage.    4   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
samples/typescript-angular/bad/conversation_storage.    3   1    0   0   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

---

### TYPESCRIPT (`--framework angular`) — 9. OWASP Juice Shop Score Board Query Param Helpers vs. Challenge Filtering Complexity

#### Good Baseline: [`good/query_params_converters.ts`](good/query_params_converters.ts) ([sidecar JSON](good/query_params_converters.ts.expected.json))

- **Upstream Dataset / Benchmark:** [OWASP juice-shop/juice-shop (frontend/src/app/score-board/filter-settings/query-params-converters.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/score-board/filter-settings/query-params-converters.ts) (`MIT`)
- **Expected Scorecard:** `Composite 94.5/100 (Grade A)` — `SRP: 95.7` | `Size: 100.0` | `Complexity: 92.0` | `Clean: 82.9` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 94.5/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 2
Dimensions -> SRP: 95.7 | Size: 100.0 | Complexity: 92.0 | Clean: 82.9 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/query_params_converters.ts src      37    -  95.7 100.0  92.0  82.9 100.0   94.5   A
    - Clean (DRY): DRY-001 (type2, 36 toks, 7 LOC) L6-12 in fromQueryParams matches samples/typescript-angular/good/query_params_converters.ts:17-23 (fromQueryParams) (-4.0 pts)
    - Clean (DRY): duplication_ratio=18.9% (>10.0%) (-4.5 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 7/37 (18.9%) | DRY Score: 91.5/100 | Clone Groups: 1 (T1: 0, T2: 1, T3: 0 | intra: 1, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type2  100.0% intra_file      7 samples/typescript-angular/good/query_params_converters.ts:L6-12, samples/typescript-angular/good/query_params_converters.ts:L17-23

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/query_params_convert   25   7    6   1   1   95.1   A
    - SRP: high external call fan-out=8 (>6) (-6.0 pts)
    - Complexity: CC=7 (>5) (-8.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript-angular/good/query_params_convert   10   7    1   1   1   97.7   A
    - Complexity: CC=7 (>5) (-8.0 pts)
    - Clean: missing public docstring (-5.0 pts)
```

#### Bad Baseline: [`bad/challenge_filtering.ts`](bad/challenge_filtering.ts) ([sidecar JSON](bad/challenge_filtering.ts.expected.json))

- **Upstream Dataset / Benchmark:** [OWASP juice-shop/juice-shop (frontend/src/app/score-board/helpers/challenge-filtering.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/score-board/helpers/challenge-filtering.ts) (`MIT`)
- **Expected Scorecard:** `Composite 20.2/100 (Grade F)` — `SRP: 69.7` | `Size: 15.8` | `Complexity: 15.2` | `Clean: 86.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 20.2/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 2
Dimensions -> SRP: 69.7 | Size: 15.8 | Complexity: 15.2 | Clean: 86.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/challenge_filtering.ts src      98    -  69.7  15.8  15.2  86.0 100.0   20.2   F
    - Clean (DRY): DRY-001 (type2, 35 toks, 6 LOC) L13-18 in filterChallenges matches samples/typescript-angular/bad/challenge_filtering.ts:20-25 (filterChallenges) (-4.0 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 6/98 (6.1%) | DRY Score: 96.0/100 | Clone Groups: 1 (T1: 0, T2: 1, T3: 0 | intra: 1, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type2  100.0% intra_file      6 samples/typescript-angular/bad/challenge_filtering.ts:L13-18, samples/typescript-angular/bad/challenge_filtering.ts:L20-25

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/challenge_filtering.t   80  15   12   2   2    5.0   F
    - SRP: high external call fan-out=23 (>6) (-36.0 pts)
    - Size: LOC=80 (>25) (-100.0 pts)
    - Complexity: CC=15 (>5) (-55.0 pts)
    - Complexity: cognitive=12 (>8) (-10.0 pts)
    - Complexity: returns=20 (>3) (-68.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript-angular/bad/challenge_filtering.t   15   5    6   1   2   97.7   A
    - Complexity: returns=4 (>3) (-4.0 pts)
    - Clean: missing public docstring (-10.0 pts)
```

---

### TYPESCRIPT (`--framework angular`) — 10. Angular User Service Spec vs. OWASP Juice Shop Oversized Navbar Spec

#### Good Baseline: [`good/user.service.spec.ts`](good/user.service.spec.ts) ([sidecar JSON](good/user.service.spec.ts.expected.json))

- **Upstream Dataset / Benchmark:** [realworld-apps/angular-realworld-example-app (src/app/core/auth/services/user.service.spec.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/core/auth/services/user.service.spec.ts) (`MIT`)
- **Expected Scorecard:** `Composite 96.2/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 75.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 96.2/100 (Grade A) | Files: 1 (src: 0, test: 1) | Classes: 0 | Functions/Methods: 28
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 75.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/user.service.spec.ts test    325    - 100.0 100.0 100.0  75.0 100.0   96.2   A
    - Clean (DRY): DRY-001 (type3, 72.4%, 97 toks, 11 LOC) L65-75 in test: should emit distinct values only matches samples/typescript-angular/good/user.service.spec.ts:84-92 (test: should emit true when user is authenticated), samples/typescript-angular/good/user.service.spec.ts:194-206 (test: should clear currentUser), samples/typescript-angular/good/user.service.spec.ts:294-302 (test: should update currentUser subject) (+1 more) (-12.0 pts)
    - Clean (DRY): DRY-002 (type3, 71.4%, 101 toks, 11 LOC) L117-127 in test: should update currentUser after successful login matches samples/typescript-angular/good/user.service.spec.ts:264-276 (test: should update currentUser with new values), samples/typescript-angular/good/user.service.spec.ts:329-340 (test: should handle complete authentication flow) (-6.0 pts)
    - Clean (DRY): DRY-003 (type3, 84.6%, 92 toks, 8 LOC) L132-139 in test: should handle login error matches samples/typescript-angular/good/user.service.spec.ts:169-180 (test: should handle registration error), samples/typescript-angular/good/user.service.spec.ts:278-285 (test: should handle update error) (-6.0 pts)
    - Clean (DRY): DRY-004 (type3, 82.9%, 88 toks, 8 LOC) L99-106 in test: should send POST request to /users/login matches samples/typescript-angular/good/user.service.spec.ts:146-153 (test: should send POST request to /users), samples/typescript-angular/good/user.service.spec.ts:252-259 (test: should send PUT request to /user) (-6.0 pts)
    - Clean (DRY): DRY-005 (type3, 93.8%, 81 toks, 8 LOC) L108-115 in test: should call setAuth with returned user matches samples/typescript-angular/good/user.service.spec.ts:156-167 (test: should call setAuth with returned user) (-3.0 pts)
    - Clean (DRY): duplication_ratio=35.1% (>15.0%) (-10.0 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 114/325 (35.1%) | DRY Score: 75.0/100 | Clone Groups: 5 (T1: 0, T2: 0, T3: 5 | intra: 5, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type3   72.4% intra_file     12 samples/typescript-angular/good/user.service.spec.ts:L65-75, samples/typescript-angular/good/user.service.spec.ts:L84-92, samples/typescript-angular/good/user.service.spec.ts:L194-206 (+2 more)
DRY-002  type3   71.4% intra_file     13 samples/typescript-angular/good/user.service.spec.ts:L117-127, samples/typescript-angular/good/user.service.spec.ts:L264-276, samples/typescript-angular/good/user.service.spec.ts:L329-340
DRY-003  type3   84.6% intra_file     12 samples/typescript-angular/good/user.service.spec.ts:L132-139, samples/typescript-angular/good/user.service.spec.ts:L169-180, samples/typescript-angular/good/user.service.spec.ts:L278-285
DRY-004  type3   82.9% intra_file      8 samples/typescript-angular/good/user.service.spec.ts:L99-106, samples/typescript-angular/good/user.service.spec.ts:L146-153, samples/typescript-angular/good/user.service.spec.ts:L252-259
DRY-005  type3   93.8% intra_file     12 samples/typescript-angular/good/user.service.spec.ts:L108-115, samples/typescript-angular/good/user.service.spec.ts:L156-167

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/user.service.spec.ts    3   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts    4   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts   11   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts    4   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts   12   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts    8   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts    8   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts   14   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts    8   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts   12   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts   12   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts   12   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts    4   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts    4   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts   12   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts    6   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts    7   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts   12   2    1   0   1  100.0   A
samples/typescript-angular/good/user.service.spec.ts    8   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts   11   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts   15   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts    8   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts    4   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts   11   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts    4   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts   12   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts   16   1    0   0   0  100.0   A
samples/typescript-angular/good/user.service.spec.ts   16   1    0   0   0  100.0   A
```

#### Bad Baseline: [`bad/navbar.component.spec.ts`](bad/navbar.component.spec.ts) ([sidecar JSON](bad/navbar.component.spec.ts.expected.json))

- **Upstream Dataset / Benchmark:** [OWASP juice-shop/juice-shop (frontend/src/app/navbar/navbar.component.spec.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/navbar/navbar.component.spec.ts) (`MIT`)
- **Expected Scorecard:** `Composite 79.5/100 (Grade C)` — `SRP: 100.0` | `Size: 74.7` | `Complexity: 100.0` | `Clean: 94.3` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 79.5/100 (Grade C) | Files: 1 (src: 0, test: 1) | Classes: 1 | Functions/Methods: 56
Dimensions -> SRP: 100.0 | Size: 74.7 | Complexity: 100.0 | Clean: 94.3 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/navbar.component.spec.ts test    519    - 100.0  74.7 100.0  94.3 100.0   79.5   C
    - Size: file LOC=519 (>350) (-25.3 pts)
    - Clean (DRY): DRY-001 (type2, 71 toks, 9 LOC) L560-569 in test: should navigate to the profile page via window.location.replace matches samples/typescript-angular/bad/navbar.component.spec.ts:571-579 (test: should navigate to the data erasure page via window.location.replace) (-4.0 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 9/519 (1.7%) | DRY Score: 96.0/100 | Clone Groups: 1 (T1: 0, T2: 1, T3: 0 | intra: 1, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type2  100.0% intra_file      9 samples/typescript-angular/bad/navbar.component.spec.ts:L560-569, samples/typescript-angular/bad/navbar.component.spec.ts:L571-579

[CLASSES SCORECARD]
Class (file:line)                                    LOC  Mth LCOM4   CC  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/navbar.component.sp     5    1     1    1   99.2   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/navbar.component.spec    9   1    0   0   0   97.8   A
    - Clean (TS): 3 explicit 'any' type usage(s) defeat type safety (-15.0 pts)
samples/typescript-angular/bad/navbar.component.spec    9   1    0   0   0   97.8   A
    - Clean (TS): 3 explicit 'any' type usage(s) defeat type safety (-15.0 pts)
samples/typescript-angular/bad/navbar.component.spec    3   1    0   2   0   99.2   A
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
samples/typescript-angular/bad/navbar.component.spec    5   1    0   0   0   99.2   A
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
samples/typescript-angular/bad/navbar.component.spec    8   1    0   0   0   99.2   A
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
samples/typescript-angular/bad/navbar.component.spec    7   1    0   0   0   99.2   A
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
samples/typescript-angular/bad/navbar.component.spec    7   1    0   0   0   99.2   A
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
samples/typescript-angular/bad/navbar.component.spec    7   1    0   0   0   99.2   A
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
samples/typescript-angular/bad/navbar.component.spec   10   2    1   0   1   99.2   A
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
samples/typescript-angular/bad/navbar.component.spec   10   2    1   0   1   99.2   A
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
samples/typescript-angular/bad/navbar.component.spec    3   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    5   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    5   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    6   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    6   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    5   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    5   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    6   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    7   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    6   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    5   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    5   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    6   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    5   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    5   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    5   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    5   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    5   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    4   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    5   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    5   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    5   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    4   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    4   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    5   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    7   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    6   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    6   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    6   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec   21   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    7   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    6   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    6   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    6   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    6   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    6   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    5   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    5   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    6   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    5   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    7   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    4   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    4   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    4   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    5   1    0   0   0  100.0   A
samples/typescript-angular/bad/navbar.component.spec    7   1    0   0   0  100.0   A
```
