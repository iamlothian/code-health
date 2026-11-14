# Angular Code Health Scorecard Baselines

This catalog provides functionally comparable, verbatim real-world **Good** and **Bad** TypeScript/Angular code samples for the `typescript (--framework angular)` profile across 10 scenarios from [`realworld-apps/angular-realworld-example-app`](https://github.com/realworld-apps/angular-realworld-example-app) and [`OWASP juice-shop/juice-shop`](https://github.com/juice-shop/juice-shop).

Each sample file `<filename>` has a matching `<filename>.expected.json` sidecar file verified against `CodeHealthRunner` and [`manifest.json`](manifest.json).

---

## Quick Summary Table

| Profile | Scenario | Quality | Sample File | Dataset Source | LOC | SRP | Size | Comp | Clean | Sec | Score | Grade |
| :--- | :--- | :---: | :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| `typescript (angular)` | 1. Angular Layout Component vs. OWASP Juice Shop Search XSS & Leak | **GOOD** | [`good/header.component.ts`](good/header.component.ts) | [realworld-apps/angular-realworld-example-app (src/app/core/layout/header.component.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/core/layout/header.component.ts) | 16 | 100.0 | 100.0 | 100.0 | 85.0 | 100.0 | **97.8** | **A** |
| `typescript (angular)` | 1. Angular Layout Component vs. OWASP Juice Shop Search XSS & Leak | **BAD** | [`bad/search_result.component.ts`](bad/search_result.component.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/search-result/search-result.component.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/search-result/search-result.component.ts) | 186 | 36.1 | 96.5 | 98.1 | 68.5 | 65.0 | **41.1** | **F** |
| `typescript (angular)` | 2. Angular Article Preview Component vs. OWASP Juice Shop Complaint Form | **GOOD** | [`good/article_preview.component.ts`](good/article_preview.component.ts) | [realworld-apps/angular-realworld-example-app (src/app/features/article/components/article-preview.component.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/features/article/components/article-preview.component.ts) | 45 | 100.0 | 100.0 | 100.0 | 80.0 | 100.0 | **97.0** | **A** |
| `typescript (angular)` | 2. Angular Article Preview Component vs. OWASP Juice Shop Complaint Form | **BAD** | [`bad/complaint.component.ts`](bad/complaint.component.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/complaint/complaint.component.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/complaint/complaint.component.ts) | 102 | 80.0 | 100.0 | 100.0 | 52.0 | 100.0 | **57.0** | **F** |
| `typescript (angular)` | 3. Angular Favorite Button Component vs. OWASP Juice Shop Score Board | **GOOD** | [`good/favorite_button.component.ts`](good/favorite_button.component.ts) | [realworld-apps/angular-realworld-example-app (src/app/features/article/components/favorite-button.component.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/features/article/components/favorite-button.component.ts) | 73 | 95.5 | 98.5 | 100.0 | 80.0 | 100.0 | **95.3** | **A** |
| `typescript (angular)` | 3. Angular Favorite Button Component vs. OWASP Juice Shop Score Board | **BAD** | [`bad/score_board.component.ts`](bad/score_board.component.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/score-board/score-board.component.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/score-board/score-board.component.ts) | 217 | 29.0 | 98.6 | 79.0 | 72.9 | 65.0 | **34.0** | **F** |
| `typescript (angular)` | 4. Angular Articles Service vs. OWASP Juice Shop WebSocket Chat Service Complexity | **GOOD** | [`good/articles.service.ts`](good/articles.service.ts) | [realworld-apps/angular-realworld-example-app (src/app/features/article/services/articles.service.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/features/article/services/articles.service.ts) | 42 | 100.0 | 100.0 | 100.0 | 79.4 | 100.0 | **96.9** | **A** |
| `typescript (angular)` | 4. Angular Articles Service vs. OWASP Juice Shop WebSocket Chat Service Complexity | **BAD** | [`bad/chat.service.ts`](bad/chat.service.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/Services/chat.service.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/Services/chat.service.ts) | 88 | 88.0 | 12.5 | 0.0 | 75.0 | 100.0 | **5.0** | **F** |
| `typescript (angular)` | 5. Angular Article Comment Component vs. OWASP Juice Shop Monolithic Product Component | **GOOD** | [`good/article_comment.component.ts`](good/article_comment.component.ts) | [realworld-apps/angular-realworld-example-app (src/app/features/article/components/article-comment.component.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/features/article/components/article-comment.component.ts) | 48 | 100.0 | 100.0 | 100.0 | 85.0 | 100.0 | **97.8** | **A** |
| `typescript (angular)` | 5. Angular Article Comment Component vs. OWASP Juice Shop Monolithic Product Component | **BAD** | [`bad/product.component.ts`](bad/product.component.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/product/product.component.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/product/product.component.ts) | 201 | 74.0 | 50.0 | 96.0 | 48.0 | 100.0 | **53.0** | **F** |
| `typescript (angular)` | 6. Angular Auth Component Hygiene vs. OWASP Juice Shop OAuth Component | **GOOD** | [`good/auth.component.ts`](good/auth.component.ts) | [realworld-apps/angular-realworld-example-app (src/app/core/auth/auth.component.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/core/auth/auth.component.ts) | 80 | 89.0 | 100.0 | 100.0 | 77.7 | 100.0 | **93.4** | **A** |
| `typescript (angular)` | 6. Angular Auth Component Hygiene vs. OWASP Juice Shop OAuth Component | **BAD** | [`bad/oauth.component.ts`](bad/oauth.component.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/oauth/oauth.component.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/oauth/oauth.component.ts) | 70 | 89.5 | 100.0 | 100.0 | 51.2 | 100.0 | **56.2** | **F** |
| `typescript (angular)` | 7. Angular Settings Component vs. OWASP Juice Shop Administration XSS Sinks | **GOOD** | [`good/settings.component.ts`](good/settings.component.ts) | [realworld-apps/angular-realworld-example-app (src/app/features/settings/settings.component.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/features/settings/settings.component.ts) | 71 | 99.2 | 100.0 | 100.0 | 77.5 | 100.0 | **96.4** | **A** |
| `typescript (angular)` | 7. Angular Settings Component vs. OWASP Juice Shop Administration XSS Sinks | **BAD** | [`bad/administration.component.ts`](bad/administration.component.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/administration/administration.component.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/administration/administration.component.ts) | 123 | 64.0 | 100.0 | 100.0 | 53.3 | 65.0 | **58.3** | **F** |
| `typescript (angular)` | 8. Angular Cohesive Comments Service vs. OWASP Juice Shop Disconnected Storage Service | **GOOD** | [`good/comments.service.ts`](good/comments.service.ts) | [realworld-apps/angular-realworld-example-app (src/app/features/article/services/comments.service.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/features/article/services/comments.service.ts) | 22 | 100.0 | 100.0 | 100.0 | 81.2 | 100.0 | **97.2** | **A** |
| `typescript (angular)` | 8. Angular Cohesive Comments Service vs. OWASP Juice Shop Disconnected Storage Service | **BAD** | [`bad/conversation_storage.service.ts`](bad/conversation_storage.service.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/Services/conversation-storage.service.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/Services/conversation-storage.service.ts) | 42 | 55.0 | 100.0 | 100.0 | 80.0 | 100.0 | **60.0** | **D** |
| `typescript (angular)` | 9. OWASP Juice Shop Score Board Query Param Helpers vs. Challenge Filtering Complexity | **GOOD** | [`good/query_params_converters.ts`](good/query_params_converters.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/score-board/filter-settings/query-params-converters.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/score-board/filter-settings/query-params-converters.ts) | 37 | 95.7 | 100.0 | 92.0 | 91.4 | 100.0 | **95.8** | **A** |
| `typescript (angular)` | 9. OWASP Juice Shop Score Board Query Param Helpers vs. Challenge Filtering Complexity | **BAD** | [`bad/challenge_filtering.ts`](bad/challenge_filtering.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/score-board/helpers/challenge-filtering.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/score-board/helpers/challenge-filtering.ts) | 98 | 69.7 | 15.8 | 15.2 | 90.0 | 100.0 | **20.2** | **F** |
| `typescript (angular)` | 10. Angular User Service Spec vs. OWASP Juice Shop Oversized Navbar Spec | **GOOD** | [`good/user.service.spec.ts`](good/user.service.spec.ts) | [realworld-apps/angular-realworld-example-app (src/app/core/auth/services/user.service.spec.ts)](https://github.com/realworld-apps/angular-realworld-example-app/blob/main/src/app/core/auth/services/user.service.spec.ts) | 325 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `typescript (angular)` | 10. Angular User Service Spec vs. OWASP Juice Shop Oversized Navbar Spec | **BAD** | [`bad/navbar.component.spec.ts`](bad/navbar.component.spec.ts) | [OWASP juice-shop/juice-shop (frontend/src/app/navbar/navbar.component.spec.ts)](https://github.com/juice-shop/juice-shop/blob/master/frontend/src/app/navbar/navbar.component.spec.ts) | 519 | 100.0 | 74.7 | 100.0 | 98.3 | 100.0 | **79.5** | **C** |

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
- **Expected Scorecard:** `Composite 41.1/100 (Grade F)` — `SRP: 36.1` | `Size: 96.5` | `Complexity: 98.1` | `Clean: 68.5` | `Security: 65.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 41.1/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 10
Dimensions -> SRP: 36.1 | Size: 96.5 | Complexity: 98.1 | Clean: 68.5 | Security: 65.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/search_result.component.ts src     186    -  36.1  96.5  98.1  68.5  65.0   41.1   F

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
- **Expected Scorecard:** `Composite 34.0/100 (Grade F)` — `SRP: 29.0` | `Size: 98.6` | `Complexity: 79.0` | `Clean: 72.9` | `Security: 65.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 34.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 12
Dimensions -> SRP: 29.0 | Size: 98.6 | Complexity: 79.0 | Clean: 72.9 | Security: 65.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/score_board.component.ts src     217    -  29.0  98.6  79.0  72.9  65.0   34.0   F

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
- **Expected Scorecard:** `Composite 53.0/100 (Grade F)` — `SRP: 74.0` | `Size: 50.0` | `Complexity: 96.0` | `Clean: 48.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 53.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 2
Dimensions -> SRP: 74.0 | Size: 50.0 | Complexity: 96.0 | Clean: 48.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/product.component.ts src     201    -  74.0  50.0  96.0  48.0 100.0   53.0   F

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
- **Expected Scorecard:** `Composite 56.2/100 (Grade F)` — `SRP: 89.5` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 51.2` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 56.2/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 4
Dimensions -> SRP: 89.5 | Size: 100.0 | Complexity: 100.0 | Clean: 51.2 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/oauth.component.ts src      70    -  89.5 100.0 100.0  51.2 100.0   56.2   F

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
- **Expected Scorecard:** `Composite 58.3/100 (Grade F)` — `SRP: 64.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 53.3` | `Security: 65.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 58.3/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 1 | Functions/Methods: 9
Dimensions -> SRP: 64.0 | Size: 100.0 | Complexity: 100.0 | Clean: 53.3 | Security: 65.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/administration.component.ts src     123    -  64.0 100.0 100.0  53.3  65.0   58.3   F

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
- **Expected Scorecard:** `Composite 95.8/100 (Grade A)` — `SRP: 95.7` | `Size: 100.0` | `Complexity: 92.0` | `Clean: 91.4` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 95.8/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 2
Dimensions -> SRP: 95.7 | Size: 100.0 | Complexity: 92.0 | Clean: 91.4 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/query_params_converters.ts src      37    -  95.7 100.0  92.0  91.4 100.0   95.8   A

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
- **Expected Scorecard:** `Composite 20.2/100 (Grade F)` — `SRP: 69.7` | `Size: 15.8` | `Complexity: 15.2` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 20.2/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 2
Dimensions -> SRP: 69.7 | Size: 15.8 | Complexity: 15.2 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/challenge_filtering.ts src      98    -  69.7  15.8  15.2  90.0 100.0   20.2   F

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
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 0, test: 1) | Classes: 0 | Functions/Methods: 28
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/good/user.service.spec.ts test    325    - 100.0 100.0 100.0 100.0 100.0  100.0   A

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
- **Expected Scorecard:** `Composite 79.5/100 (Grade C)` — `SRP: 100.0` | `Size: 74.7` | `Complexity: 100.0` | `Clean: 98.3` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 79.5/100 (Grade C) | Files: 1 (src: 0, test: 1) | Classes: 1 | Functions/Methods: 56
Dimensions -> SRP: 100.0 | Size: 74.7 | Complexity: 100.0 | Clean: 98.3 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-angular/bad/navbar.component.spec.ts test    519    - 100.0  74.7 100.0  98.3 100.0   79.5   C
    - Size: file LOC=519 (>350) (-25.3 pts)

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
