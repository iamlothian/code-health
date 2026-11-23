# Next.js Code Health Scorecard Baselines

This catalog provides functionally comparable, human-inspectable **Good** and **Bad** verbatim open-source Next.js App Router (`language: typescript`, `framework: nextjs`) code samples across 10 scenario pairs.

Each sample file `<filename>` has a matching `<filename>.expected.json` sidecar file verified against `CodeHealthRunner` (`lang_override="typescript"`, `framework_override="nextjs"`).

---

## Quick Summary Table

| Profile | Scenario | Quality | Sample File | Dataset Source | LOC | SRP | Size | Comp | Clean | Sec | Score | Grade |
| :--- | :--- | :---: | :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| `typescript (nextjs)` | 1. Next.js Client Navigation Component vs. Oversized Login Form (vercel/next-learn) | **GOOD** | [`good/app/nav_links.tsx`](good/app/nav_links.tsx) | [vercel/next-learn (dashboard/final-example/app/ui/dashboard/nav-links.tsx)](https://github.com/vercel/next-learn/blob/main/dashboard/final-example/app/ui/dashboard/nav-links.tsx) | 43 | 100.0 | 100.0 | 100.0 | 90.0 | 100.0 | **98.5** | **A** |
| `typescript (nextjs)` | 1. Next.js Client Navigation Component vs. Oversized Login Form (vercel/next-learn) | **BAD** | [`bad/app/login_form.tsx`](bad/app/login_form.tsx) | [vercel/next-learn (dashboard/final-example/app/ui/login-form.tsx)](https://github.com/vercel/next-learn/blob/main/dashboard/final-example/app/ui/login-form.tsx) | 86 | 100.0 | 2.5 | 100.0 | 90.0 | 100.0 | **7.5** | **F** |
| `typescript (nextjs)` | 2. Next.js Async Server Page vs. Monolithic Customers Table (vercel/next-learn) | **GOOD** | [`good/app/invoices_page.tsx`](good/app/invoices_page.tsx) | [vercel/next-learn (dashboard/final-example/app/dashboard/invoices/page.tsx)](https://github.com/vercel/next-learn/blob/main/dashboard/final-example/app/dashboard/invoices/page.tsx) | 40 | 100.0 | 95.5 | 100.0 | 90.0 | 100.0 | **97.4** | **A** |
| `typescript (nextjs)` | 2. Next.js Async Server Page vs. Monolithic Customers Table (vercel/next-learn) | **BAD** | [`bad/app/customers_table.tsx`](bad/app/customers_table.tsx) | [vercel/next-learn (dashboard/final-example/app/ui/customers/table.tsx)](https://github.com/vercel/next-learn/blob/main/dashboard/final-example/app/ui/customers/table.tsx) | 118 | 100.0 | 0.0 | 100.0 | 86.9 | 100.0 | **5.0** | **F** |
| `typescript (nextjs)` | 3. Next.js Error Boundary Component vs. Heavy Revenue Chart Render (vercel/next-learn) | **GOOD** | [`good/app/invoices_error.tsx`](good/app/invoices_error.tsx) | [vercel/next-learn (dashboard/final-example/app/dashboard/invoices/error.tsx)](https://github.com/vercel/next-learn/blob/main/dashboard/final-example/app/dashboard/invoices/error.tsx) | 26 | 100.0 | 100.0 | 100.0 | 90.0 | 100.0 | **98.5** | **A** |
| `typescript (nextjs)` | 3. Next.js Error Boundary Component vs. Heavy Revenue Chart Render (vercel/next-learn) | **BAD** | [`bad/app/revenue_chart.tsx`](bad/app/revenue_chart.tsx) | [vercel/next-learn (dashboard/final-example/app/ui/dashboard/revenue-chart.tsx)](https://github.com/vercel/next-learn/blob/main/dashboard/final-example/app/ui/dashboard/revenue-chart.tsx) | 48 | 100.0 | 71.5 | 100.0 | 90.0 | 100.0 | **76.5** | **C** |
| `typescript (nextjs)` | 4. Next.js Safe Product Description Component vs. Raw dangerouslySetInnerHTML Prose (vercel/commerce) | **GOOD** | [`good/app/product_description.tsx`](good/app/product_description.tsx) | [vercel/commerce (components/product/product-description.tsx)](https://github.com/vercel/commerce/blob/main/components/product/product-description.tsx) | 28 | 100.0 | 100.0 | 100.0 | 90.0 | 100.0 | **98.5** | **A** |
| `typescript (nextjs)` | 4. Next.js Safe Product Description Component vs. Raw dangerouslySetInnerHTML Prose (vercel/commerce) | **BAD** | [`bad/app/prose_html.tsx`](bad/app/prose_html.tsx) | [vercel/commerce (components/prose.tsx)](https://github.com/vercel/commerce/blob/main/components/prose.tsx) | 13 | 100.0 | 100.0 | 100.0 | 90.0 | 65.0 | **70.0** | **C** |
| `typescript (nextjs)` | 5. Next.js Safe Link Wrapper vs. dangerouslySetInnerHTML Markdown Preview (bulletproof-react) | **GOOD** | [`good/app/ui_link.tsx`](good/app/ui_link.tsx) | [alan2207/bulletproof-react (apps/nextjs-app/src/components/ui/link/link.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/nextjs-app/src/components/ui/link/link.tsx) | 18 | 100.0 | 100.0 | 100.0 | 90.0 | 100.0 | **98.5** | **A** |
| `typescript (nextjs)` | 5. Next.js Safe Link Wrapper vs. dangerouslySetInnerHTML Markdown Preview (bulletproof-react) | **BAD** | [`bad/app/md_preview.tsx`](bad/app/md_preview.tsx) | [alan2207/bulletproof-react (apps/nextjs-app/src/components/ui/md-preview/md-preview.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/nextjs-app/src/components/ui/md-preview/md-preview.tsx) | 15 | 100.0 | 100.0 | 100.0 | 95.0 | 65.0 | **70.0** | **C** |
| `typescript (nextjs)` | 6. Next.js App Router Dialog Story without Client Hook Leak vs. Missing 'use client' Directive (bulletproof-react) | **GOOD** | [`good/app/confirmation_dialog_stories.tsx`](good/app/confirmation_dialog_stories.tsx) | [alan2207/bulletproof-react (apps/nextjs-app/src/components/ui/dialog/confirmation-dialog/confirmation-dialog.stories.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/nextjs-app/src/components/ui/dialog/confirmation-dialog/confirmation-dialog.stories.tsx) | 26 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `typescript (nextjs)` | 6. Next.js App Router Dialog Story without Client Hook Leak vs. Missing 'use client' Directive (bulletproof-react) | **BAD** | [`bad/app/dialog_stories.tsx`](bad/app/dialog_stories.tsx) | [alan2207/bulletproof-react (apps/nextjs-app/src/components/ui/dialog/dialog.stories.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/nextjs-app/src/components/ui/dialog/dialog.stories.tsx) | 54 | 100.0 | 88.4 | 100.0 | 74.9 | 100.0 | **79.5** | **C** |
| `typescript (nextjs)` | 7. Next.js Focused Metadata Route (robots.ts) vs. High Fan-Out Sitemap Route (vercel/commerce) | **GOOD** | [`good/app/robots_route.ts`](good/app/robots_route.ts) | [vercel/commerce (app/robots.ts)](https://github.com/vercel/commerce/blob/main/app/robots.ts) | 12 | 100.0 | 100.0 | 100.0 | 80.0 | 100.0 | **97.0** | **A** |
| `typescript (nextjs)` | 7. Next.js Focused Metadata Route (robots.ts) vs. High Fan-Out Sitemap Route (vercel/commerce) | **BAD** | [`bad/app/sitemap_route.ts`](bad/app/sitemap_route.ts) | [vercel/commerce (app/sitemap.ts)](https://github.com/vercel/commerce/blob/main/app/sitemap.ts) | 42 | 73.0 | 86.5 | 100.0 | 84.9 | 100.0 | **78.0** | **C** |
| `typescript (nextjs)` | 8. Next.js Cart Trigger Leaf vs. Monolithic Branchy Cart Modal (vercel/commerce) | **GOOD** | [`good/app/open_cart.tsx`](good/app/open_cart.tsx) | [vercel/commerce (components/cart/open-cart.tsx)](https://github.com/vercel/commerce/blob/main/components/cart/open-cart.tsx) | 25 | 100.0 | 100.0 | 100.0 | 90.0 | 100.0 | **98.5** | **A** |
| `typescript (nextjs)` | 8. Next.js Cart Trigger Leaf vs. Monolithic Branchy Cart Modal (vercel/commerce) | **BAD** | [`bad/app/cart_modal.tsx`](bad/app/cart_modal.tsx) | [vercel/commerce (components/cart/modal.tsx)](https://github.com/vercel/commerce/blob/main/components/cart/modal.tsx) | 243 | 83.9 | 10.8 | 75.9 | 82.9 | 100.0 | **15.8** | **F** |
| `typescript (nextjs)` | 9. Next.js Discussions Container vs. Branchy Comments List Component (bulletproof-react) | **GOOD** | [`good/app/discussions_panel.tsx`](good/app/discussions_panel.tsx) | [alan2207/bulletproof-react (apps/nextjs-app/src/app/app/discussions/_components/discussions.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/nextjs-app/src/app/app/discussions/_components/discussions.tsx) | 25 | 100.0 | 100.0 | 100.0 | 90.0 | 100.0 | **98.5** | **A** |
| `typescript (nextjs)` | 9. Next.js Discussions Container vs. Branchy Comments List Component (bulletproof-react) | **BAD** | [`bad/app/comments_list.tsx`](bad/app/comments_list.tsx) | [alan2207/bulletproof-react (apps/nextjs-app/src/features/comments/components/comments-list.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/nextjs-app/src/features/comments/components/comments-list.tsx) | 81 | 91.0 | 20.0 | 84.0 | 90.0 | 100.0 | **25.0** | **F** |
| `typescript (nextjs)` | 10. Next.js Search Filter List Wrapper vs. High Fan-Out Filter Dropdown (vercel/commerce) | **GOOD** | [`good/app/filter_index.tsx`](good/app/filter_index.tsx) | [vercel/commerce (components/layout/search/filter/index.tsx)](https://github.com/vercel/commerce/blob/main/components/layout/search/filter/index.tsx) | 44 | 100.0 | 95.4 | 100.0 | 89.3 | 100.0 | **97.2** | **A** |
| `typescript (nextjs)` | 10. Next.js Search Filter List Wrapper vs. High Fan-Out Filter Dropdown (vercel/commerce) | **BAD** | [`bad/app/filter_dropdown.tsx`](bad/app/filter_dropdown.tsx) | [vercel/commerce (components/layout/search/filter/dropdown.tsx)](https://github.com/vercel/commerce/blob/main/components/layout/search/filter/dropdown.tsx) | 57 | 79.0 | 60.0 | 88.0 | 82.0 | 100.0 | **65.0** | **D** |

---

## Detailed Scenario Scorecards

### TYPESCRIPT (`--framework nextjs`) — 1. Next.js Client Navigation Component vs. Oversized Login Form (vercel/next-learn)

#### Good Baseline: [`good/app/nav_links.tsx`](good/app/nav_links.tsx) ([sidecar JSON](good/app/nav_links.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [vercel/next-learn (dashboard/final-example/app/ui/dashboard/nav-links.tsx)](https://github.com/vercel/next-learn/blob/main/dashboard/final-example/app/ui/dashboard/nav-links.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 98.5/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 98.5/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/good/app/nav_links.tsx src      43    - 100.0 100.0 100.0  90.0 100.0   98.5   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/good/app/nav_links.tsx:24    25   1    0   0   0   98.5   A
    - Clean: missing public docstring (-10.0 pts)
```

#### Bad Baseline: [`bad/app/login_form.tsx`](bad/app/login_form.tsx) ([sidecar JSON](bad/app/login_form.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [vercel/next-learn (dashboard/final-example/app/ui/login-form.tsx)](https://github.com/vercel/next-learn/blob/main/dashboard/final-example/app/ui/login-form.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 7.5/100 (Grade F)` — `SRP: 100.0` | `Size: 2.5` | `Complexity: 100.0` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 7.5/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 2.5 | Complexity: 100.0 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/bad/app/login_form.tsx src      86    - 100.0   2.5 100.0  90.0 100.0    7.5   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/bad/app/login_form.tsx:15    74   3    0   0   0    7.5   F
    - Size: LOC=74 (>25) (-97.5 pts)
    - Clean: missing public docstring (-10.0 pts)
```

---

### TYPESCRIPT (`--framework nextjs`) — 2. Next.js Async Server Page vs. Monolithic Customers Table (vercel/next-learn)

#### Good Baseline: [`good/app/invoices_page.tsx`](good/app/invoices_page.tsx) ([sidecar JSON](good/app/invoices_page.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [vercel/next-learn (dashboard/final-example/app/dashboard/invoices/page.tsx)](https://github.com/vercel/next-learn/blob/main/dashboard/final-example/app/dashboard/invoices/page.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 97.4/100 (Grade A)` — `SRP: 100.0` | `Size: 95.5` | `Complexity: 100.0` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 97.4/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 95.5 | Complexity: 100.0 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/good/app/invoices_page.tsx src      40    - 100.0  95.5 100.0  90.0 100.0   97.4   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/good/app/invoices_page.tsx   28   3    0   1   0   97.4   A
    - Size: LOC=28 (>25) (-4.5 pts)
    - Clean: missing public docstring (-10.0 pts)
```

#### Bad Baseline: [`bad/app/customers_table.tsx`](bad/app/customers_table.tsx) ([sidecar JSON](bad/app/customers_table.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [vercel/next-learn (dashboard/final-example/app/ui/customers/table.tsx)](https://github.com/vercel/next-learn/blob/main/dashboard/final-example/app/ui/customers/table.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 100.0` | `Size: 0.0` | `Complexity: 100.0` | `Clean: 86.9` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 0.0 | Complexity: 100.0 | Clean: 86.9 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/bad/app/customers_table.tsx src     118    - 100.0   0.0 100.0  86.9 100.0    5.0   F
    - Clean (DRY): DRY-001 (type3, 89.0%, 57 toks, 12 LOC) L29-40 in CustomersTable matches samples/typescript-nextjs/bad/app/customers_table.tsx:86-97 (CustomersTable) (-3.0 pts)
    - Clean (DRY): duplication_ratio=10.2% (>10.0%) (-0.1 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 12/118 (10.2%) | DRY Score: 96.9/100 | Clone Groups: 1 (T1: 0, T2: 0, T3: 1 | intra: 1, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type3   89.0% intra_file     12 samples/typescript-nextjs/bad/app/customers_table.tsx:L29-40, samples/typescript-nextjs/bad/app/customers_table.tsx:L86-97

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/bad/app/customers_table.ts  114   1    0   1   0    5.0   F
    - Size: LOC=114 (>25) (-100.0 pts)
    - Clean: missing public docstring (-10.0 pts)
```

---

### TYPESCRIPT (`--framework nextjs`) — 3. Next.js Error Boundary Component vs. Heavy Revenue Chart Render (vercel/next-learn)

#### Good Baseline: [`good/app/invoices_error.tsx`](good/app/invoices_error.tsx) ([sidecar JSON](good/app/invoices_error.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [vercel/next-learn (dashboard/final-example/app/dashboard/invoices/error.tsx)](https://github.com/vercel/next-learn/blob/main/dashboard/final-example/app/dashboard/invoices/error.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 98.5/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 98.5/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/good/app/invoices_error.tsx src      26    - 100.0 100.0 100.0  90.0 100.0   98.5   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/good/app/invoices_error.ts   24   1    0   1   0   98.5   A
    - Clean: missing public docstring (-10.0 pts)
```

#### Bad Baseline: [`bad/app/revenue_chart.tsx`](bad/app/revenue_chart.tsx) ([sidecar JSON](bad/app/revenue_chart.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [vercel/next-learn (dashboard/final-example/app/ui/dashboard/revenue-chart.tsx)](https://github.com/vercel/next-learn/blob/main/dashboard/final-example/app/ui/dashboard/revenue-chart.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 76.5/100 (Grade C)` — `SRP: 100.0` | `Size: 71.5` | `Complexity: 100.0` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 76.5/100 (Grade C) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 71.5 | Complexity: 100.0 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/bad/app/revenue_chart.tsx src      48    - 100.0  71.5 100.0  90.0 100.0   76.5   C

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/bad/app/revenue_chart.tsx:   44   3    1   0   1   76.5   C
    - Size: LOC=44 (>25) (-28.5 pts)
    - Clean: missing public docstring (-10.0 pts)
```

---

### TYPESCRIPT (`--framework nextjs`) — 4. Next.js Safe Product Description Component vs. Raw dangerouslySetInnerHTML Prose (vercel/commerce)

#### Good Baseline: [`good/app/product_description.tsx`](good/app/product_description.tsx) ([sidecar JSON](good/app/product_description.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [vercel/commerce (components/product/product-description.tsx)](https://github.com/vercel/commerce/blob/main/components/product/product-description.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 98.5/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 98.5/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/good/app/product_description.tsx src      28    - 100.0 100.0 100.0  90.0 100.0   98.5   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/good/app/product_descripti   23   2    1   1   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
```

#### Bad Baseline: [`bad/app/prose_html.tsx`](bad/app/prose_html.tsx) ([sidecar JSON](bad/app/prose_html.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [vercel/commerce (components/prose.tsx)](https://github.com/vercel/commerce/blob/main/components/prose.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 70.0/100 (Grade C)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 90.0` | `Security: 65.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 70.0/100 (Grade C) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 90.0 | Security: 65.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/bad/app/prose_html.tsx src      13    - 100.0 100.0 100.0  90.0  65.0   70.0   C

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/bad/app/prose_html.tsx:3 P   11   1    0   1   0   70.0   C
    - Clean: missing public docstring (-10.0 pts)
    - Security (Nextjs): unsafe XSS/DOM sink 'dangerouslySetInnerHTML' at L10 (-35.0 pts)
```

---

### TYPESCRIPT (`--framework nextjs`) — 5. Next.js Safe Link Wrapper vs. dangerouslySetInnerHTML Markdown Preview (bulletproof-react)

#### Good Baseline: [`good/app/ui_link.tsx`](good/app/ui_link.tsx) ([sidecar JSON](good/app/ui_link.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [alan2207/bulletproof-react (apps/nextjs-app/src/components/ui/link/link.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/nextjs-app/src/components/ui/link/link.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 98.5/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 98.5/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/good/app/ui_link.tsx src      18    - 100.0 100.0 100.0  90.0 100.0   98.5   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/good/app/ui_link.tsx:11 Li   11   1    0   1   0   98.5   A
    - Clean: missing public docstring (-10.0 pts)
```

#### Bad Baseline: [`bad/app/md_preview.tsx`](bad/app/md_preview.tsx) ([sidecar JSON](bad/app/md_preview.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [alan2207/bulletproof-react (apps/nextjs-app/src/components/ui/md-preview/md-preview.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/nextjs-app/src/components/ui/md-preview/md-preview.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 70.0/100 (Grade C)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 95.0` | `Security: 65.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 70.0/100 (Grade C) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 95.0 | Security: 65.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/bad/app/md_preview.tsx src      15    - 100.0 100.0 100.0  95.0  65.0   70.0   C

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/bad/app/md_preview.tsx:8 M   10   1    0   1   0   70.0   C
    - Clean: missing public docstring (-5.0 pts)
    - Security (Nextjs): unsafe XSS/DOM sink 'dangerouslySetInnerHTML' at L12 (-35.0 pts)
```

---

### TYPESCRIPT (`--framework nextjs`) — 6. Next.js App Router Dialog Story without Client Hook Leak vs. Missing 'use client' Directive (bulletproof-react)

#### Good Baseline: [`good/app/confirmation_dialog_stories.tsx`](good/app/confirmation_dialog_stories.tsx) ([sidecar JSON](good/app/confirmation_dialog_stories.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [alan2207/bulletproof-react (apps/nextjs-app/src/components/ui/dialog/confirmation-dialog/confirmation-dialog.stories.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/nextjs-app/src/components/ui/dialog/confirmation-dialog/confirmation-dialog.stories.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 0
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/good/app/confirmation_dialog_stories.tsx src      26    - 100.0 100.0 100.0 100.0 100.0  100.0   A
```

#### Bad Baseline: [`bad/app/dialog_stories.tsx`](bad/app/dialog_stories.tsx) ([sidecar JSON](bad/app/dialog_stories.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [alan2207/bulletproof-react (apps/nextjs-app/src/components/ui/dialog/dialog.stories.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/nextjs-app/src/components/ui/dialog/dialog.stories.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 79.5/100 (Grade C)` — `SRP: 100.0` | `Size: 88.4` | `Complexity: 100.0` | `Clean: 74.9` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 79.5/100 (Grade C) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 2
Dimensions -> SRP: 100.0 | Size: 88.4 | Complexity: 100.0 | Clean: 74.9 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/bad/app/dialog_stories.tsx src      54    - 100.0  88.4 100.0  74.9 100.0   79.5   C
    - Clean (Next.js): App Router module uses client hooks without 'use client' directive (-15.0 pts)

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/bad/app/dialog_stories.tsx   33   2    1   0   1   95.5   A
    - Size: LOC=33 (>25) (-12.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript-nextjs/bad/app/dialog_stories.tsx    1   1    0   0   0   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
```

---

### TYPESCRIPT (`--framework nextjs`) — 7. Next.js Focused Metadata Route (robots.ts) vs. High Fan-Out Sitemap Route (vercel/commerce)

#### Good Baseline: [`good/app/robots_route.ts`](good/app/robots_route.ts) ([sidecar JSON](good/app/robots_route.ts.expected.json))

- **Upstream Dataset / Benchmark:** [vercel/commerce (app/robots.ts)](https://github.com/vercel/commerce/blob/main/app/robots.ts) (`MIT`)
- **Expected Scorecard:** `Composite 97.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 80.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 97.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 80.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/good/app/robots_route.ts src      12    - 100.0 100.0 100.0  80.0 100.0   97.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/good/app/robots_route.ts:3   11   1    0   0   0   97.0   A
    - Clean: missing public docstring (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
```

#### Bad Baseline: [`bad/app/sitemap_route.ts`](bad/app/sitemap_route.ts) ([sidecar JSON](bad/app/sitemap_route.ts.expected.json))

- **Upstream Dataset / Benchmark:** [vercel/commerce (app/sitemap.ts)](https://github.com/vercel/commerce/blob/main/app/sitemap.ts) (`MIT`)
- **Expected Scorecard:** `Composite 78.0/100 (Grade C)` — `SRP: 73.0` | `Size: 86.5` | `Complexity: 100.0` | `Clean: 84.9` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 78.0/100 (Grade C) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 73.0 | Size: 86.5 | Complexity: 100.0 | Clean: 84.9 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/bad/app/sitemap_route.ts src      42    -  73.0  86.5 100.0  84.9 100.0   78.0   C
    - Clean (DRY): DRY-001 (type3, 98.0%, 48 toks, 7 LOC) L20-27 in sitemap matches samples/typescript-nextjs/bad/app/sitemap_route.ts:34-39 (sitemap) (-3.0 pts)
    - Clean (DRY): duplication_ratio=14.3% (>10.0%) (-2.1 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 6/42 (14.3%) | DRY Score: 94.9/100 | Clone Groups: 1 (T1: 0, T2: 0, T3: 1 | intra: 1, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type3   98.0% intra_file      7 samples/typescript-nextjs/bad/app/sitemap_route.ts:L20-27, samples/typescript-nextjs/bad/app/sitemap_route.ts:L34-39

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/bad/app/sitemap_route.ts:1   34   2    1   0   1   78.0   C
    - SRP: high external call fan-out=15 (>6) (-27.0 pts)
    - Size: LOC=34 (>25) (-13.5 pts)
    - Clean: missing public docstring (-10.0 pts)
```

---

### TYPESCRIPT (`--framework nextjs`) — 8. Next.js Cart Trigger Leaf vs. Monolithic Branchy Cart Modal (vercel/commerce)

#### Good Baseline: [`good/app/open_cart.tsx`](good/app/open_cart.tsx) ([sidecar JSON](good/app/open_cart.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [vercel/commerce (components/cart/open-cart.tsx)](https://github.com/vercel/commerce/blob/main/components/cart/open-cart.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 98.5/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 98.5/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/good/app/open_cart.tsx src      25    - 100.0 100.0 100.0  90.0 100.0   98.5   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/good/app/open_cart.tsx:4 O   23   2    1   1   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
```

#### Bad Baseline: [`bad/app/cart_modal.tsx`](bad/app/cart_modal.tsx) ([sidecar JSON](bad/app/cart_modal.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [vercel/commerce (components/cart/modal.tsx)](https://github.com/vercel/commerce/blob/main/components/cart/modal.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 15.8/100 (Grade F)` — `SRP: 83.9` | `Size: 10.8` | `Complexity: 75.9` | `Clean: 82.9` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 15.8/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 3
Dimensions -> SRP: 83.9 | Size: 10.8 | Complexity: 75.9 | Clean: 82.9 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/bad/app/cart_modal.tsx src     243    -  83.9  10.8  75.9  82.9 100.0   15.8   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/bad/app/cart_modal.tsx:24   199  11    7   0   2    5.0   F
    - SRP: high external call fan-out=12 (>6) (-18.0 pts)
    - Size: LOC=199 (>25) (-100.0 pts)
    - Complexity: CC=11 (>5) (-27.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Clean (React): array index used as JSX key at L121 (-8.0 pts)
samples/typescript-nextjs/bad/app/cart_modal.tsx:231   12   1    0   1   0   98.5   A
    - Clean: missing public docstring (-10.0 pts)
samples/typescript-nextjs/bad/app/cart_modal.tsx:244   12   2    1   0   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
```

---

### TYPESCRIPT (`--framework nextjs`) — 9. Next.js Discussions Container vs. Branchy Comments List Component (bulletproof-react)

#### Good Baseline: [`good/app/discussions_panel.tsx`](good/app/discussions_panel.tsx) ([sidecar JSON](good/app/discussions_panel.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [alan2207/bulletproof-react (apps/nextjs-app/src/app/app/discussions/_components/discussions.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/nextjs-app/src/app/app/discussions/_components/discussions.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 98.5/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 98.5/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/good/app/discussions_panel.tsx src      25    - 100.0 100.0 100.0  90.0 100.0   98.5   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/good/app/discussions_panel   19   1    0   0   0   98.5   A
    - Clean: missing public docstring (-10.0 pts)
```

#### Bad Baseline: [`bad/app/comments_list.tsx`](bad/app/comments_list.tsx) ([sidecar JSON](bad/app/comments_list.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [alan2207/bulletproof-react (apps/nextjs-app/src/features/comments/components/comments-list.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/nextjs-app/src/features/comments/components/comments-list.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 25.0/100 (Grade F)` — `SRP: 91.0` | `Size: 20.0` | `Complexity: 84.0` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 25.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 91.0 | Size: 20.0 | Complexity: 84.0 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/bad/app/comments_list.tsx src      81    -  91.0  20.0  84.0  90.0 100.0   25.0   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/bad/app/comments_list.tsx:   67   9    3   1   1   25.0   F
    - SRP: high external call fan-out=9 (>6) (-9.0 pts)
    - Size: LOC=67 (>25) (-80.0 pts)
    - Complexity: CC=9 (>5) (-16.0 pts)
    - Clean: missing public docstring (-10.0 pts)
```

---

### TYPESCRIPT (`--framework nextjs`) — 10. Next.js Search Filter List Wrapper vs. High Fan-Out Filter Dropdown (vercel/commerce)

#### Good Baseline: [`good/app/filter_index.tsx`](good/app/filter_index.tsx) ([sidecar JSON](good/app/filter_index.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [vercel/commerce (components/layout/search/filter/index.tsx)](https://github.com/vercel/commerce/blob/main/components/layout/search/filter/index.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 97.2/100 (Grade A)` — `SRP: 100.0` | `Size: 95.4` | `Complexity: 100.0` | `Clean: 89.3` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 97.2/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 2
Dimensions -> SRP: 100.0 | Size: 95.4 | Complexity: 100.0 | Clean: 89.3 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/good/app/filter_index.tsx src      44    - 100.0  95.4 100.0  89.3 100.0   97.2   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/good/app/filter_index.tsx:   29   2    1   1   1   97.0   A
    - Size: LOC=29 (>25) (-6.0 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript-nextjs/good/app/filter_index.tsx:    9   1    0   1   0   98.0   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean (React): array index used as JSX key at L13 (-8.0 pts)
```

#### Bad Baseline: [`bad/app/filter_dropdown.tsx`](bad/app/filter_dropdown.tsx) ([sidecar JSON](bad/app/filter_dropdown.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [vercel/commerce (components/layout/search/filter/dropdown.tsx)](https://github.com/vercel/commerce/blob/main/components/layout/search/filter/dropdown.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 65.0/100 (Grade D)` — `SRP: 79.0` | `Size: 60.0` | `Complexity: 88.0` | `Clean: 82.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 65.0/100 (Grade D) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 79.0 | Size: 60.0 | Complexity: 88.0 | Clean: 82.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/bad/app/filter_dropdown.tsx src      57    -  79.0  60.0  88.0  82.0 100.0   65.0   D

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-nextjs/bad/app/filter_dropdown.ts   51   8    2   1   1   65.0   D
    - SRP: high external call fan-out=13 (>6) (-21.0 pts)
    - Size: LOC=51 (>25) (-40.0 pts)
    - Complexity: CC=8 (>5) (-12.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Clean (React): array index used as JSX key at L58 (-8.0 pts)
```

