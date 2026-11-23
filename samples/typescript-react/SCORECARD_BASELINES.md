# React Code Health Scorecard Baselines

This catalog provides 10 functionally comparable, human-inspectable **Good** and **Bad** verbatim real-world TypeScript/React TSX sample pairs (20 files) from `alan2207/bulletproof-react`, `shadcn-ui/ui`, and `TanStack/table`, verified with `--language typescript --framework react`.

Each sample file `<filename>` has a matching `<filename>.expected.json` sidecar file and is listed in [`manifest.json`](manifest.json).

---

## Quick Summary Table

| Profile | Scenario | Quality | Sample File | Dataset Source | LOC | SRP | Size | Comp | Clean | Sec | Score | Grade |
| :--- | :--- | :---: | :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| `typescript (react)` | 3. React Feature Component Decomposition vs. Profile Update Form (bulletproof-react) | **GOOD** | [`good/delete_discussion.tsx`](good/delete_discussion.tsx) | [alan2207/bulletproof-react (features/discussions/components/delete-discussion.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/react-vite/src/features/discussions/components/delete-discussion.tsx) | 48 | 100.0 | 79.0 | 100.0 | 90.0 | 100.0 | **93.2** | **A** |
| `typescript (react)` | 3. React Feature Component Decomposition vs. Profile Update Form (bulletproof-react) | **BAD** | [`bad/update_profile.tsx`](bad/update_profile.tsx) | [alan2207/bulletproof-react (features/users/components/update-profile.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/react-vite/src/features/users/components/update-profile.tsx) | 86 | 100.0 | 0.0 | 100.0 | 86.8 | 100.0 | **5.0** | **F** |
| `typescript (react)` | 4. React Safe UI Link Wrapper vs. Unsanitized Markdown Preview XSS (bulletproof-react) | **GOOD** | [`good/link.tsx`](good/link.tsx) | [alan2207/bulletproof-react (components/ui/link/link.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/react-vite/src/components/ui/link/link.tsx) | 12 | 100.0 | 100.0 | 100.0 | 95.0 | 100.0 | **99.2** | **A** |
| `typescript (react)` | 4. React Safe UI Link Wrapper vs. Unsanitized Markdown Preview XSS (bulletproof-react) | **BAD** | [`bad/md_preview.tsx`](bad/md_preview.tsx) | [alan2207/bulletproof-react (components/ui/md-preview/md-preview.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/react-vite/src/components/ui/md-preview/md-preview.tsx) | 16 | 100.0 | 100.0 | 100.0 | 95.0 | 65.0 | **70.0** | **C** |
| `typescript (react)` | 5. React Feature View Composition vs. Large Comments List Render (bulletproof-react) | **GOOD** | [`good/discussion_view.tsx`](good/discussion_view.tsx) | [alan2207/bulletproof-react (features/discussions/components/discussion-view.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/react-vite/src/features/discussions/components/discussion-view.tsx) | 45 | 100.0 | 77.5 | 100.0 | 90.0 | 100.0 | **92.9** | **A** |
| `typescript (react)` | 5. React Feature View Composition vs. Large Comments List Render (bulletproof-react) | **BAD** | [`bad/comments_list.tsx`](bad/comments_list.tsx) | [alan2207/bulletproof-react (features/comments/components/comments-list.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/react-vite/src/features/comments/components/comments-list.tsx) | 83 | 97.0 | 12.5 | 92.0 | 90.0 | 100.0 | **17.5** | **F** |
| `typescript (react)` | 4. React Focused Media Query Hook vs. Layout Hook & Effect Sprawl (shadcn-ui/ui) | **GOOD** | [`good/use_media_query.tsx`](good/use_media_query.tsx) | [shadcn-ui/ui (apps/v4/hooks/use-media-query.tsx)](https://github.com/shadcn-ui/ui/blob/main/apps/v4/hooks/use-media-query.tsx) | 14 | 100.0 | 100.0 | 100.0 | 80.0 | 100.0 | **97.0** | **A** |
| `typescript (react)` | 4. React Focused Media Query Hook vs. Layout Hook & Effect Sprawl (shadcn-ui/ui) | **BAD** | [`bad/use_layout.tsx`](bad/use_layout.tsx) | [shadcn-ui/ui (apps/v4/hooks/use-layout.tsx)](https://github.com/shadcn-ui/ui/blob/main/apps/v4/hooks/use-layout.tsx) | 134 | 63.0 | 15.9 | 15.9 | 89.1 | 100.0 | **20.9** | **F** |
| `typescript (react)` | 5. React Composable Table Header Controls vs. Branchy Column Header (TanStack/table) | **GOOD** | [`good/header_components.tsx`](good/header_components.tsx) | [TanStack/table (examples/react/composable-tables/src/components/header-components.tsx)](https://github.com/TanStack/table/blob/main/examples/react/composable-tables/src/components/header-components.tsx) | 49 | 98.5 | 100.0 | 100.0 | 100.0 | 100.0 | **99.5** | **A** |
| `typescript (react)` | 5. React Composable Table Header Controls vs. Branchy Column Header (TanStack/table) | **BAD** | [`bad/data_table_column_header.tsx`](bad/data_table_column_header.tsx) | [TanStack/table (examples/react/kitchen-sink-shadcn-radix/src/components/data-table/data-table-column-header.tsx)](https://github.com/TanStack/table/blob/main/examples/react/kitchen-sink-shadcn-radix/src/components/data-table/data-table-column-header.tsx) | 153 | 76.0 | 0.0 | 0.0 | 90.0 | 100.0 | **5.0** | **F** |
| `typescript (react)` | 6. React Focused Button Primitive vs. Branchy Font Picker Component (shadcn-ui/ui) | **GOOD** | [`good/button.tsx`](good/button.tsx) | [shadcn-ui/ui (apps/v4/registry/bases/radix/ui/button.tsx)](https://github.com/shadcn-ui/ui/blob/main/apps/v4/registry/bases/radix/ui/button.tsx) | 55 | 100.0 | 100.0 | 100.0 | 90.0 | 100.0 | **98.5** | **A** |
| `typescript (react)` | 6. React Focused Button Primitive vs. Branchy Font Picker Component (shadcn-ui/ui) | **BAD** | [`bad/font_picker.tsx`](bad/font_picker.tsx) | [shadcn-ui/ui (apps/v4/app/(app)/(typeset)/components/font-picker.tsx)](https://github.com/shadcn-ui/ui/blob/main/apps/v4/app/(app)/(typeset)/components/font-picker.tsx) | 132 | 88.0 | 0.0 | 0.0 | 90.0 | 100.0 | **5.0** | **F** |
| `typescript (react)` | 7. React Sidebar Menu Rendering vs. Array Index JSX Keys (shadcn-ui/ui) | **GOOD** | [`good/sidebar_menu.tsx`](good/sidebar_menu.tsx) | [shadcn-ui/ui (apps/v4/examples/radix/sidebar-menu.tsx)](https://github.com/shadcn-ui/ui/blob/main/apps/v4/examples/radix/sidebar-menu.tsx) | 73 | 100.0 | 97.0 | 100.0 | 90.0 | 100.0 | **97.8** | **A** |
| `typescript (react)` | 7. React Sidebar Menu Rendering vs. Array Index JSX Keys (shadcn-ui/ui) | **BAD** | [`bad/nav_actions.tsx`](bad/nav_actions.tsx) | [shadcn-ui/ui (apps/v4/registry/new-york-v4/blocks/sidebar-10/components/nav-actions.tsx)](https://github.com/shadcn-ui/ui/blob/main/apps/v4/registry/new-york-v4/blocks/sidebar-10/components/nav-actions.tsx) | 147 | 100.0 | 60.0 | 100.0 | 68.5 | 100.0 | **65.0** | **D** |
| `typescript (react)` | 8. React Composable Cell Components vs. Conditional Hook Call (TanStack/table) | **GOOD** | [`good/cell_components.tsx`](good/cell_components.tsx) | [TanStack/table (examples/react/composable-tables/src/components/cell-components.tsx)](https://github.com/TanStack/table/blob/main/examples/react/composable-tables/src/components/cell-components.tsx) | 91 | 100.0 | 96.2 | 100.0 | 90.4 | 100.0 | **97.6** | **A** |
| `typescript (react)` | 8. React Composable Cell Components vs. Conditional Hook Call (TanStack/table) | **BAD** | [`bad/material_react_table.tsx`](bad/material_react_table.tsx) | [TanStack/table (examples/react/material-react-table/src/material-react-table/components/MaterialReactTable.tsx)](https://github.com/TanStack/table/blob/main/examples/react/material-react-table/src/material-react-table/components/MaterialReactTable.tsx) | 37 | 100.0 | 100.0 | 100.0 | 66.4 | 100.0 | **71.4** | **C** |
| `typescript (react)` | 9. React Safe Copy Button vs. Chart Code Viewer dangerouslySetInnerHTML (shadcn-ui/ui) | **GOOD** | [`good/copy_button.tsx`](good/copy_button.tsx) | [shadcn-ui/ui (apps/v4/components/copy-button.tsx)](https://github.com/shadcn-ui/ui/blob/main/apps/v4/components/copy-button.tsx) | 104 | 97.8 | 77.1 | 96.8 | 85.3 | 100.0 | **90.8** | **A** |
| `typescript (react)` | 9. React Safe Copy Button vs. Chart Code Viewer dangerouslySetInnerHTML (shadcn-ui/ui) | **BAD** | [`bad/chart_code_viewer.tsx`](bad/chart_code_viewer.tsx) | [shadcn-ui/ui (apps/v4/components/chart-code-viewer.tsx)](https://github.com/shadcn-ui/ui/blob/main/apps/v4/components/chart-code-viewer.tsx) | 114 | 100.0 | 0.0 | 100.0 | 90.0 | 65.0 | **5.0** | **F** |
| `typescript (react)` | 10. React Component RTL Test Hygiene vs. Bloated Multi-Assertion Adapter Test | **GOOD** | [`good/dialog.test.tsx`](good/dialog.test.tsx) | [alan2207/bulletproof-react (apps/react-vite/src/components/ui/dialog/__tests__/dialog.test.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/react-vite/src/components/ui/dialog/__tests__/dialog.test.tsx) | 56 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | **100.0** | **A** |
| `typescript (react)` | 10. React Component RTL Test Hygiene vs. Bloated Multi-Assertion Adapter Test | **BAD** | [`bad/adapter_reactivity.test.tsx`](bad/adapter_reactivity.test.tsx) | [TanStack/table (packages/react-table/tests/adapterReactivity.test.tsx)](https://github.com/TanStack/table/blob/main/packages/react-table/tests/adapterReactivity.test.tsx) | 508 | 100.0 | 29.5 | 99.0 | 75.0 | 100.0 | **34.5** | **F** |

---

## Detailed Scenario Scorecards

### TYPESCRIPT (`--framework react`) — 3. React Feature Component Decomposition vs. Profile Update Form (bulletproof-react)

#### Good Baseline: [`good/delete_discussion.tsx`](good/delete_discussion.tsx) ([sidecar JSON](good/delete_discussion.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [alan2207/bulletproof-react (features/discussions/components/delete-discussion.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/react-vite/src/features/discussions/components/delete-discussion.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 93.2/100 (Grade A)` — `SRP: 100.0` | `Size: 79.0` | `Complexity: 100.0` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 93.2/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 79.0 | Complexity: 100.0 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/good/delete_discussion.tsx src      48    - 100.0  79.0 100.0  90.0 100.0   93.2   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/good/delete_discussion.tsx:   39   1    0   1   0   93.2   A
    - Size: LOC=39 (>25) (-21.0 pts)
    - Clean: missing public docstring (-10.0 pts)
```

#### Bad Baseline: [`bad/update_profile.tsx`](bad/update_profile.tsx) ([sidecar JSON](bad/update_profile.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [alan2207/bulletproof-react (features/users/components/update-profile.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/react-vite/src/features/users/components/update-profile.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 100.0` | `Size: 0.0` | `Complexity: 100.0` | `Clean: 86.8` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 0.0 | Complexity: 100.0 | Clean: 86.8 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/bad/update_profile.tsx src      86    - 100.0   0.0 100.0  86.8 100.0    5.0   F
    - Clean (DRY): DRY-001 (type3, 100.0%, 46 toks, 9 LOC) L65-73 in UpdateProfile matches samples/typescript-react/bad/update_profile.tsx:76-85 (UpdateProfile) (-3.0 pts)
    - Clean (DRY): duplication_ratio=10.5% (>10.0%) (-0.2 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 9/86 (10.5%) | DRY Score: 96.8/100 | Clone Groups: 1 (T1: 0, T2: 0, T3: 1 | intra: 1, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type3  100.0% intra_file      9 samples/typescript-react/bad/update_profile.tsx:L65-73, samples/typescript-react/bad/update_profile.tsx:L76-85

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/bad/update_profile.tsx:13 U   77   5    0   0   0    5.0   F
    - Size: LOC=77 (>25) (-100.0 pts)
    - Clean: missing public docstring (-10.0 pts)
```

---

### TYPESCRIPT (`--framework react`) — 4. React Safe UI Link Wrapper vs. Unsanitized Markdown Preview XSS (bulletproof-react)

#### Good Baseline: [`good/link.tsx`](good/link.tsx) ([sidecar JSON](good/link.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [alan2207/bulletproof-react (components/ui/link/link.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/react-vite/src/components/ui/link/link.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 99.2/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 95.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 99.2/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 95.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/good/link.tsx         src      12    - 100.0 100.0 100.0  95.0 100.0   99.2   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/good/link.tsx:5 Link          10   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

#### Bad Baseline: [`bad/md_preview.tsx`](bad/md_preview.tsx) ([sidecar JSON](bad/md_preview.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [alan2207/bulletproof-react (components/ui/md-preview/md-preview.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/react-vite/src/components/ui/md-preview/md-preview.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 70.0/100 (Grade C)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 95.0` | `Security: 65.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 70.0/100 (Grade C) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 95.0 | Security: 65.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/bad/md_preview.tsx    src      16    - 100.0 100.0 100.0  95.0  65.0   70.0   C

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/bad/md_preview.tsx:10 MDPre   10   1    0   1   0   70.0   C
    - Clean: missing public docstring (-5.0 pts)
    - Security (React): unsafe XSS/DOM sink 'dangerouslySetInnerHTML' at L14 (-35.0 pts)
```

---

### TYPESCRIPT (`--framework react`) — 5. React Feature View Composition vs. Large Comments List Render (bulletproof-react)

#### Good Baseline: [`good/discussion_view.tsx`](good/discussion_view.tsx) ([sidecar JSON](good/discussion_view.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [alan2207/bulletproof-react (features/discussions/components/discussion-view.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/react-vite/src/features/discussions/components/discussion-view.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 92.9/100 (Grade A)` — `SRP: 100.0` | `Size: 77.5` | `Complexity: 100.0` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 92.9/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 77.5 | Complexity: 100.0 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/good/discussion_view.tsx src      45    - 100.0  77.5 100.0  90.0 100.0   92.9   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/good/discussion_view.tsx:8    40   4    2   1   1   92.9   A
    - Size: LOC=40 (>25) (-22.5 pts)
    - Clean: missing public docstring (-10.0 pts)
```

#### Bad Baseline: [`bad/comments_list.tsx`](bad/comments_list.tsx) ([sidecar JSON](bad/comments_list.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [alan2207/bulletproof-react (features/comments/components/comments-list.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/react-vite/src/features/comments/components/comments-list.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 17.5/100 (Grade F)` — `SRP: 97.0` | `Size: 12.5` | `Complexity: 92.0` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 17.5/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 97.0 | Size: 12.5 | Complexity: 92.0 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/bad/comments_list.tsx src      83    -  97.0  12.5  92.0  90.0 100.0   17.5   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/bad/comments_list.tsx:19 Co   70   7    3   1   1   17.5   F
    - SRP: high external call fan-out=7 (>6) (-3.0 pts)
    - Size: LOC=70 (>25) (-87.5 pts)
    - Complexity: CC=7 (>5) (-8.0 pts)
    - Clean: missing public docstring (-10.0 pts)
```

---

### TYPESCRIPT (`--framework react`) — 4. React Focused Media Query Hook vs. Layout Hook & Effect Sprawl (shadcn-ui/ui)

#### Good Baseline: [`good/use_media_query.tsx`](good/use_media_query.tsx) ([sidecar JSON](good/use_media_query.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [shadcn-ui/ui (apps/v4/hooks/use-media-query.tsx)](https://github.com/shadcn-ui/ui/blob/main/apps/v4/hooks/use-media-query.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 97.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 80.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 97.0/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 80.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/good/use_media_query.tsx src      14    - 100.0 100.0 100.0  80.0 100.0   97.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/good/use_media_query.tsx:3    13   1    0   1   0   97.0   A
    - Clean: missing public docstring (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
```

#### Bad Baseline: [`bad/use_layout.tsx`](bad/use_layout.tsx) ([sidecar JSON](bad/use_layout.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [shadcn-ui/ui (apps/v4/hooks/use-layout.tsx)](https://github.com/shadcn-ui/ui/blob/main/apps/v4/hooks/use-layout.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 20.9/100 (Grade F)` — `SRP: 63.0` | `Size: 15.9` | `Complexity: 15.9` | `Clean: 89.1` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 20.9/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 4
Dimensions -> SRP: 63.0 | Size: 15.9 | Complexity: 15.9 | Clean: 89.1 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/bad/use_layout.tsx    src     134    -  63.0  15.9  15.9  89.1 100.0   20.9   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/bad/use_layout.tsx:43 Layou   95  20   22   1   3    5.0   F
    - SRP: high external call fan-out=21 (>6) (-36.0 pts)
    - Size: LOC=95 (>25) (-100.0 pts)
    - Complexity: CC=20 (>5) (-90.0 pts)
    - Complexity: cognitive=22 (>8) (-35.0 pts)
    - Complexity: returns=9 (>3) (-24.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - SRP (React): effect sprawl with 3 useEffect/useLayoutEffect calls (>2) (-8.0 pts)
samples/typescript-react/bad/use_layout.tsx:27 saveT    6   2    1   2   1   96.2   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
    - Clean: empty catch block swallows exception (-10.0 pts)
samples/typescript-react/bad/use_layout.tsx:35 useLa    7   2    1   0   1   97.8   A
    - Clean: missing public docstring (-5.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-react/bad/use_layout.tsx:155 Layo    5   2    1   1   1   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

---

### TYPESCRIPT (`--framework react`) — 5. React Composable Table Header Controls vs. Branchy Column Header (TanStack/table)

#### Good Baseline: [`good/header_components.tsx`](good/header_components.tsx) ([sidecar JSON](good/header_components.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [TanStack/table (examples/react/composable-tables/src/components/header-components.tsx)](https://github.com/TanStack/table/blob/main/examples/react/composable-tables/src/components/header-components.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 99.5/100 (Grade A)` — `SRP: 98.5` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 99.5/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 4
Dimensions -> SRP: 98.5 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/good/header_components.tsx src      49    -  98.5 100.0 100.0 100.0 100.0   99.5   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/good/header_components.tsx:   23   3    1   0   1   99.1   A
    - SRP: high external call fan-out=7 (>6) (-3.0 pts)
samples/typescript-react/good/header_components.tsx:    8   3    2   0   1  100.0   A
samples/typescript-react/good/header_components.tsx:    4   1    0   0   0  100.0   A
samples/typescript-react/good/header_components.tsx:   12   3    2   0   1  100.0   A
```

#### Bad Baseline: [`bad/data_table_column_header.tsx`](bad/data_table_column_header.tsx) ([sidecar JSON](bad/data_table_column_header.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [TanStack/table (examples/react/kitchen-sink-shadcn-radix/src/components/data-table/data-table-column-header.tsx)](https://github.com/TanStack/table/blob/main/examples/react/kitchen-sink-shadcn-radix/src/components/data-table/data-table-column-header.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 76.0` | `Size: 0.0` | `Complexity: 0.0` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 76.0 | Size: 0.0 | Complexity: 0.0 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/bad/data_table_column_header.tsx src     153    -  76.0   0.0   0.0  90.0 100.0    5.0   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/bad/data_table_column_heade  131  22   11   1   1    5.0   F
    - SRP: high external call fan-out=14 (>6) (-24.0 pts)
    - Size: LOC=131 (>25) (-100.0 pts)
    - Complexity: CC=22 (>5) (-100.0 pts)
    - Complexity: cognitive=11 (>8) (-7.5 pts)
    - Clean: missing public docstring (-10.0 pts)
```

---

### TYPESCRIPT (`--framework react`) — 6. React Focused Button Primitive vs. Branchy Font Picker Component (shadcn-ui/ui)

#### Good Baseline: [`good/button.tsx`](good/button.tsx) ([sidecar JSON](good/button.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [shadcn-ui/ui (apps/v4/registry/bases/radix/ui/button.tsx)](https://github.com/shadcn-ui/ui/blob/main/apps/v4/registry/bases/radix/ui/button.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 98.5/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 98.5/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/good/button.tsx       src      55    - 100.0 100.0 100.0  90.0 100.0   98.5   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/good/button.tsx:36 Button     21   2    1   1   1   98.5   A
    - Clean: missing public docstring (-10.0 pts)
```

#### Bad Baseline: [`bad/font_picker.tsx`](bad/font_picker.tsx) ([sidecar JSON](bad/font_picker.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [shadcn-ui/ui (apps/v4/app/(app)/(typeset)/components/font-picker.tsx)](https://github.com/shadcn-ui/ui/blob/main/apps/v4/app/(app)/(typeset)/components/font-picker.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 88.0` | `Size: 0.0` | `Complexity: 0.0` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 88.0 | Size: 0.0 | Complexity: 0.0 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/bad/font_picker.tsx   src     132    -  88.0   0.0   0.0  90.0 100.0    5.0   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/bad/font_picker.tsx:21 Font  114  19   21   1   3    5.0   F
    - SRP: high external call fan-out=10 (>6) (-12.0 pts)
    - Size: LOC=114 (>25) (-100.0 pts)
    - Complexity: CC=19 (>5) (-83.0 pts)
    - Complexity: cognitive=21 (>8) (-32.5 pts)
    - Clean: missing public docstring (-10.0 pts)
```

---

### TYPESCRIPT (`--framework react`) — 7. React Sidebar Menu Rendering vs. Array Index JSX Keys (shadcn-ui/ui)

#### Good Baseline: [`good/sidebar_menu.tsx`](good/sidebar_menu.tsx) ([sidecar JSON](good/sidebar_menu.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [shadcn-ui/ui (apps/v4/examples/radix/sidebar-menu.tsx)](https://github.com/shadcn-ui/ui/blob/main/apps/v4/examples/radix/sidebar-menu.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 97.8/100 (Grade A)` — `SRP: 100.0` | `Size: 97.0` | `Complexity: 100.0` | `Clean: 90.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 97.8/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 97.0 | Complexity: 100.0 | Clean: 90.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/good/sidebar_menu.tsx src      73    - 100.0  97.0 100.0  90.0 100.0   97.8   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/good/sidebar_menu.tsx:51 Ap   27   1    0   0   0   97.8   A
    - Size: LOC=27 (>25) (-3.0 pts)
    - Clean: missing public docstring (-10.0 pts)
```

#### Bad Baseline: [`bad/nav_actions.tsx`](bad/nav_actions.tsx) ([sidecar JSON](bad/nav_actions.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [shadcn-ui/ui (apps/v4/registry/new-york-v4/blocks/sidebar-10/components/nav-actions.tsx)](https://github.com/shadcn-ui/ui/blob/main/apps/v4/registry/new-york-v4/blocks/sidebar-10/components/nav-actions.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 65.0/100 (Grade D)` — `SRP: 100.0` | `Size: 60.0` | `Complexity: 100.0` | `Clean: 68.5` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 65.0/100 (Grade D) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 60.0 | Complexity: 100.0 | Clean: 68.5 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/bad/nav_actions.tsx   src     147    - 100.0  60.0 100.0  68.5 100.0   65.0   D
    - Clean (DRY): DRY-001 (type3, 83.1%, 58 toks, 22 LOC) L50-71 in <module> matches samples/typescript-react/bad/nav_actions.tsx:72-93 (<module>) (-3.0 pts)
    - Clean (DRY): duplication_ratio=15.0% (>10.0%) (-2.5 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 22/147 (15.0%) | DRY Score: 94.5/100 | Clone Groups: 1 (T1: 0, T2: 0, T3: 1 | intra: 1, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type3   83.1% intra_file     22 samples/typescript-react/bad/nav_actions.tsx:L50-71, samples/typescript-react/bad/nav_actions.tsx:L72-93

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/bad/nav_actions.tsx:101 Nav   51   1    0   0   0   65.0   D
    - Size: LOC=51 (>25) (-40.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Clean (React): array index used as JSX key at L133 (-16.0 pts)
```

---

### TYPESCRIPT (`--framework react`) — 8. React Composable Cell Components vs. Conditional Hook Call (TanStack/table)

#### Good Baseline: [`good/cell_components.tsx`](good/cell_components.tsx) ([sidecar JSON](good/cell_components.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [TanStack/table (examples/react/composable-tables/src/components/cell-components.tsx)](https://github.com/TanStack/table/blob/main/examples/react/composable-tables/src/components/cell-components.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 97.6/100 (Grade A)` — `SRP: 100.0` | `Size: 96.2` | `Complexity: 100.0` | `Clean: 90.4` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 97.6/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 8
Dimensions -> SRP: 100.0 | Size: 96.2 | Complexity: 100.0 | Clean: 90.4 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/good/cell_components.tsx src      91    - 100.0  96.2 100.0  90.4 100.0   97.6   A
    - Clean (DRY): DRY-001 (type2, 36 toks, 7 LOC) L92-98 in RowActionsCell matches samples/typescript-react/good/cell_components.tsx:100-106 (RowActionsCell) (-4.0 pts)
    - Clean (DRY): DRY-002 (type2, 41 toks, 5 LOC) L57-61 in StatusCell matches samples/typescript-react/good/cell_components.tsx:132-136 (CategoryCell) (-4.0 pts)
    - Clean (DRY): duplication_ratio=13.2% (>10.0%) (-1.6 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 12/91 (13.2%) | DRY Score: 90.4/100 | Clone Groups: 2 (T1: 0, T2: 2, T3: 0 | intra: 2, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type2  100.0% intra_file      7 samples/typescript-react/good/cell_components.tsx:L92-98, samples/typescript-react/good/cell_components.tsx:L100-106
DRY-002  type2  100.0% intra_file      5 samples/typescript-react/good/cell_components.tsx:L57-61, samples/typescript-react/good/cell_components.tsx:L132-136

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/good/cell_components.tsx:79   32   1    0   0   0   97.4   A
    - Size: LOC=32 (>25) (-10.5 pts)
samples/typescript-react/good/cell_components.tsx:19   17   1    0   0   0  100.0   A
samples/typescript-react/good/cell_components.tsx:41    4   1    0   0   0  100.0   A
samples/typescript-react/good/cell_components.tsx:49    4   1    0   0   0  100.0   A
samples/typescript-react/good/cell_components.tsx:57    5   1    0   0   0  100.0   A
samples/typescript-react/good/cell_components.tsx:66    9   1    0   0   0  100.0   A
samples/typescript-react/good/cell_components.tsx:11   12   1    0   0   0  100.0   A
samples/typescript-react/good/cell_components.tsx:13    5   1    0   0   0  100.0   A
```

#### Bad Baseline: [`bad/material_react_table.tsx`](bad/material_react_table.tsx) ([sidecar JSON](bad/material_react_table.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [TanStack/table (examples/react/material-react-table/src/material-react-table/components/MaterialReactTable.tsx)](https://github.com/TanStack/table/blob/main/examples/react/material-react-table/src/material-react-table/components/MaterialReactTable.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 71.4/100 (Grade C)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 66.4` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 71.4/100 (Grade C) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 2
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 66.4 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/bad/material_react_table.tsx src      37    - 100.0 100.0 100.0  66.4 100.0   71.4   C

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/bad/material_react_table.ts   18   2    1   1   1   65.0   D
    - Clean: missing public docstring (-10.0 pts)
    - Clean (React): Rules of Hooks violation calling 'useMaterialReactTable' in branch/loop at L32 (-25.0 pts)
    - Clean (TS): 1 explicit 'any' type usage(s) defeat type safety (-5.0 pts)
samples/typescript-react/bad/material_react_table.ts    4   1    0   1   0   99.2   A
    - Clean: missing public docstring (-5.0 pts)
```

---

### TYPESCRIPT (`--framework react`) — 9. React Safe Copy Button vs. Chart Code Viewer dangerouslySetInnerHTML (shadcn-ui/ui)

#### Good Baseline: [`good/copy_button.tsx`](good/copy_button.tsx) ([sidecar JSON](good/copy_button.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [shadcn-ui/ui (apps/v4/components/copy-button.tsx)](https://github.com/shadcn-ui/ui/blob/main/apps/v4/components/copy-button.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 90.8/100 (Grade A)` — `SRP: 97.8` | `Size: 77.1` | `Complexity: 96.8` | `Clean: 85.3` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 90.8/100 (Grade A) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 3
Dimensions -> SRP: 97.8 | Size: 77.1 | Complexity: 96.8 | Clean: 85.3 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/good/copy_button.tsx  src     104    -  97.8  77.1  96.8  85.3 100.0   90.8   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/good/copy_button.tsx:67 Cop   52   5    4   1   1   62.5   D
    - SRP: high external call fan-out=7 (>6) (-3.0 pts)
    - Size: LOC=52 (>25) (-42.5 pts)
    - Clean: missing public docstring (-10.0 pts)
samples/typescript-react/good/copy_button.tsx:34 cop   26   7    7   2   2   94.2   A
    - Size: LOC=26 (>25) (-1.5 pts)
    - Complexity: CC=7 (>5) (-8.0 pts)
    - Complexity: returns=4 (>3) (-4.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
samples/typescript-react/good/copy_button.tsx:10 leg   20   2    1   1   1   96.1   A
    - SRP: high external call fan-out=7 (>6) (-3.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Clean: missing return type annotation (-10.0 pts)
```

#### Bad Baseline: [`bad/chart_code_viewer.tsx`](bad/chart_code_viewer.tsx) ([sidecar JSON](bad/chart_code_viewer.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [shadcn-ui/ui (apps/v4/components/chart-code-viewer.tsx)](https://github.com/shadcn-ui/ui/blob/main/apps/v4/components/chart-code-viewer.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 5.0/100 (Grade F)` — `SRP: 100.0` | `Size: 0.0` | `Complexity: 100.0` | `Clean: 90.0` | `Security: 65.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 5.0/100 (Grade F) | Files: 1 (src: 1, test: 0) | Classes: 0 | Functions/Methods: 1
Dimensions -> SRP: 100.0 | Size: 0.0 | Complexity: 100.0 | Clean: 90.0 | Security: 65.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/bad/chart_code_viewer.tsx src     114    - 100.0   0.0 100.0  90.0  65.0    5.0   F

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/bad/chart_code_viewer.tsx:2   90   3    1   1   1    5.0   F
    - Size: LOC=90 (>25) (-100.0 pts)
    - Clean: missing public docstring (-10.0 pts)
    - Security (React): unsafe XSS/DOM sink 'dangerouslySetInnerHTML' at L72 (-35.0 pts)
```

---

### TYPESCRIPT (`--framework react`) — 10. React Component RTL Test Hygiene vs. Bloated Multi-Assertion Adapter Test

#### Good Baseline: [`good/dialog.test.tsx`](good/dialog.test.tsx) ([sidecar JSON](good/dialog.test.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [alan2207/bulletproof-react (apps/react-vite/src/components/ui/dialog/__tests__/dialog.test.tsx)](https://github.com/alan2207/bulletproof-react/blob/master/apps/react-vite/src/components/ui/dialog/__tests__/dialog.test.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 100.0/100 (Grade A)` — `SRP: 100.0` | `Size: 100.0` | `Complexity: 100.0` | `Clean: 100.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 100.0/100 (Grade A) | Files: 1 (src: 0, test: 1) | Classes: 0 | Functions/Methods: 2
Dimensions -> SRP: 100.0 | Size: 100.0 | Complexity: 100.0 | Clean: 100.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/good/dialog.test.tsx  test     56    - 100.0 100.0 100.0 100.0 100.0  100.0   A

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/good/dialog.test.tsx:20 Tes   31   2    1   0   1  100.0   A
samples/typescript-react/good/dialog.test.tsx:54 tes   10   1    0   0   0  100.0   A
```

#### Bad Baseline: [`bad/adapter_reactivity.test.tsx`](bad/adapter_reactivity.test.tsx) ([sidecar JSON](bad/adapter_reactivity.test.tsx.expected.json))

- **Upstream Dataset / Benchmark:** [TanStack/table (packages/react-table/tests/adapterReactivity.test.tsx)](https://github.com/TanStack/table/blob/main/packages/react-table/tests/adapterReactivity.test.tsx) (`MIT`)
- **Expected Scorecard:** `Composite 34.5/100 (Grade F)` — `SRP: 100.0` | `Size: 29.5` | `Complexity: 99.0` | `Clean: 75.0` | `Security: 100.0`

```text
================================================================================================
CODE HEALTH SCORECARD | Score: 34.5/100 (Grade F) | Files: 1 (src: 0, test: 1) | Classes: 0 | Functions/Methods: 10
Dimensions -> SRP: 100.0 | Size: 29.5 | Complexity: 99.0 | Clean: 75.0 | Security: 100.0
================================================================================================

[FILES SCORECARD]
File                                           Kind    LOC  Git   SRP  Size  Comp   Cln   Sec  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/bad/adapter_reactivity.test.tsx test    508    - 100.0  29.5  99.0  75.0 100.0   34.5   F
    - Size: file LOC=508 (>350) (-23.7 pts)
    - Clean (DRY): DRY-001 (type3, 81.3%, 79 toks, 12 LOC) L192-207 in test: updates the paginated row model without invalidating the core row model matches samples/typescript-react/bad/adapter_reactivity.test.tsx:257-272 (test: bridges external atoms through both Subscribe source overloads), samples/typescript-react/bad/adapter_reactivity.test.tsx:550-561 (test: refreshes data, columns, and table options together on the next render) (-6.0 pts)
    - Clean (DRY): DRY-002 (type3, 85.9%, 64 toks, 16 LOC) L221-237 in test: bridges external atoms through both Subscribe source overloads matches samples/typescript-react/bad/adapter_reactivity.test.tsx:292-305 (test: isolates Subscribe render cycles to each selected dependency) (-3.0 pts)
    - Clean (DRY): DRY-003 (type3, 86.8%, 65 toks, 9 LOC) L200-210 in test: updates the paginated row model without invalidating the core row model matches samples/typescript-react/bad/adapter_reactivity.test.tsx:364-374 (test: isolates Subscribe render cycles to each selected dependency), samples/typescript-react/bad/adapter_reactivity.test.tsx:379-389 (test: isolates Subscribe render cycles to each selected dependency) (-6.0 pts)
    - Clean (DRY): DRY-004 (type3, 95.7%, 69 toks, 13 LOC) L284-297 in test: isolates Subscribe render cycles to each selected dependency matches samples/typescript-react/bad/adapter_reactivity.test.tsx:403-415 (test: stops root and isolated React observers after unmount) (-3.0 pts)
    - Clean (DRY): DRY-005 (type3, 90.1%, 59 toks, 8 LOC) L351-360 in test: isolates Subscribe render cycles to each selected dependency matches samples/typescript-react/bad/adapter_reactivity.test.tsx:363-372 (test: isolates Subscribe render cycles to each selected dependency) (-3.0 pts)

[DUPLICATE CODE & DRY SUMMARY]
Duplicated LOC: 66/508 (13.0%) | DRY Score: 79.0/100 | Clone Groups: 5 (T1: 0, T2: 0, T3: 5 | intra: 5, cross: 0)
ID       Type      Sim Scope         LOC Locations
------------------------------------------------------------------------------------------------
DRY-001  type3   81.3% intra_file     12 samples/typescript-react/bad/adapter_reactivity.test.tsx:L192-207, samples/typescript-react/bad/adapter_reactivity.test.tsx:L257-272, samples/typescript-react/bad/adapter_reactivity.test.tsx:L550-561
DRY-002  type3   85.9% intra_file     16 samples/typescript-react/bad/adapter_reactivity.test.tsx:L221-237, samples/typescript-react/bad/adapter_reactivity.test.tsx:L292-305
DRY-003  type3   86.8% intra_file      9 samples/typescript-react/bad/adapter_reactivity.test.tsx:L200-210, samples/typescript-react/bad/adapter_reactivity.test.tsx:L364-374, samples/typescript-react/bad/adapter_reactivity.test.tsx:L379-389
DRY-004  type3   95.7% intra_file     13 samples/typescript-react/bad/adapter_reactivity.test.tsx:L284-297, samples/typescript-react/bad/adapter_reactivity.test.tsx:L403-415
DRY-005  type3   90.1% intra_file      8 samples/typescript-react/bad/adapter_reactivity.test.tsx:L351-360, samples/typescript-react/bad/adapter_reactivity.test.tsx:L363-372

[FUNCTIONS & METHODS SCORECARD]
Symbol (file:line)                                    LOC  CC  Cog Prm Nst  Score Grd
------------------------------------------------------------------------------------------------
samples/typescript-react/bad/adapter_reactivity.test  106   1    0   0   0    8.0   F
    - Size: LOC=106 (>40) (-97.0 pts)
    - Complexity: returns=4 (>3) (-4.0 pts)
    - Clean (Test): 26 assertions in single test (>8) (-30.0 pts)
samples/typescript-react/bad/adapter_reactivity.test   92   5    4   0   1   36.0   F
    - Size: LOC=92 (>40) (-69.0 pts)
    - Clean (Test): 11 assertions in single test (>8) (-9.0 pts)
    - Clean (TS): 3 non-null assertion(s) ('!') bypass strict null checks (-6.0 pts)
samples/typescript-react/bad/adapter_reactivity.test   57   1    0   0   0   94.1   A
    - Size: LOC=57 (>40) (-17.0 pts)
    - Clean (Test): 9 assertions in single test (>8) (-3.0 pts)
    - Clean (TS): 4 non-null assertion(s) ('!') bypass strict null checks (-8.0 pts)
samples/typescript-react/bad/adapter_reactivity.test   62   1    0   0   0   94.2   A
    - Size: LOC=62 (>40) (-22.0 pts)
    - Clean (TS): 1 non-null assertion(s) ('!') bypass strict null checks (-2.0 pts)
samples/typescript-react/bad/adapter_reactivity.test   57   1    0   0   0   95.8   A
    - Size: LOC=57 (>40) (-17.0 pts)
samples/typescript-react/bad/adapter_reactivity.test   54   1    0   0   0   96.5   A
    - Size: LOC=54 (>40) (-14.0 pts)
samples/typescript-react/bad/adapter_reactivity.test    4   1    0   0   0   99.7   A
    - Clean (TS): 1 non-null assertion(s) ('!') bypass strict null checks (-2.0 pts)
samples/typescript-react/bad/adapter_reactivity.test    4   1    0   1   0  100.0   A
samples/typescript-react/bad/adapter_reactivity.test    3   1    0   1   0  100.0   A
samples/typescript-react/bad/adapter_reactivity.test    3   1    0   1   0  100.0   A
```
