# Next.js Refactoring Playbook

**Profile:** `nextjs`  
**Detection:** Imports from `next` or `next/*`, or `package.json` listing `"next"` for files under `app/` or `pages/` routes or containing JSX / `react` imports / `'use client'` or `'use server'` directives  
**Force:** `--framework nextjs`  
**Builds on:** [React Playbook](react-playbook.md)  
**Worked examples:**  
- Clean: [product_description.tsx](../../../samples/typescript-nextjs/good/app/product_description.tsx), [confirmation_dialog_stories.tsx](../../../samples/typescript-nextjs/good/app/confirmation_dialog_stories.tsx), [nav_links.tsx](../../../samples/typescript-nextjs/good/app/nav_links.tsx), [invoices_page.tsx](../../../samples/typescript-nextjs/good/app/invoices_page.tsx), [invoices_error.tsx](../../../samples/typescript-nextjs/good/app/invoices_error.tsx)  
- Flagged: [prose_html.tsx](../../../samples/typescript-nextjs/bad/app/prose_html.tsx), [dialog_stories.tsx](../../../samples/typescript-nextjs/bad/app/dialog_stories.tsx), [cart_modal.tsx](../../../samples/typescript-nextjs/bad/app/cart_modal.tsx), [login_form.tsx](../../../samples/typescript-nextjs/bad/app/login_form.tsx), [customers_table.tsx](../../../samples/typescript-nextjs/bad/app/customers_table.tsx), [revenue_chart.tsx](../../../samples/typescript-nextjs/bad/app/revenue_chart.tsx)

---

## Profile Scope & Finding Names

`nextjs` inherits every rule and exemption from `react` (Rules of Hooks, effect/state sprawl, array index keys, XSS sinks, UI concern buckets, and PascalCase JSX component return-type exemptions) and adds App Router client/server boundary checks.

> [!NOTE]
> Function-level XSS findings emit `Security (Nextjs): unsafe XSS/DOM sink '...'` (without the dot), whereas module-level App Router findings emit `Clean (Next.js): ...` and `Security (Next.js): ...`.

---

## 1. App Router Client Hooks Without `'use client'`

**Finding:** `Clean (Next.js): App Router module uses client hooks without 'use client' directive (-15.0 pts)`

Triggers on App Router modules (path contains `app` and not `pages`) whose filename stem is not a custom hook (`use[A-Z]*`), that call `useState`, `useEffect`, `useReducer`, `useRef`, or `useContext` without a top-level `'use client'` directive.

**Fix — Push Client Leaves Down, Don't Blanket-Mark `page.tsx`:**
Keep `app/**/page.tsx` as a Server Component that loads data and passes plain serializable props to small `'use client'` interactive leaf components.

```tsx
// Before: app/dashboard/page.tsx uses useState directly with no directive (-15.0 pts)
import { useState } from 'react';

export default function DashboardPage() {
  const [filter, setFilter] = useState('all');
  return <section>{filter}</section>;
}

// After: Server Component page delegates interactive controls to a Client Leaf
// app/dashboard/page.tsx (Server Component — 0 hooks)
export default async function DashboardPage() {
  const summary = await loadDashboardSummary();
  return <DashboardFilterView initialSummary={summary} />;
}

// app/dashboard/dashboard-filter-view.tsx
'use client';
import { useState } from 'react';

/** Renders interactive filter controls for the dashboard summary. */
export function DashboardFilterView({ initialSummary }: DashboardProps) {
  const [filter, setFilter] = useState('all');
  return <section>{initialSummary.total} ({filter})</section>;
}
```

---

## 2. Server-Only Import Inside `'use client'` Module

**Finding:** `Security (Next.js): server-only import '{bad_imps[0]}' inside 'use client' module (-30.0 pts)`

Blocked server-only imports in `'use client'` modules:
`fs`, `child_process`, `server-only`, `next/headers`, `node:*`, `fs/*`, `next/headers/*`.

Importing server secrets, headers/cookies helpers, or Node APIs inside a client bundle either crashes the Next.js build or leaks server-only code to the browser.

```tsx
// Before (-30.0 pts Security (Next.js))
'use client';
import { cookies } from 'next/headers';
import { useState } from 'react';

export default function DashboardUnsafe() {
  const [tab, setTab] = useState('overview');
  const session = cookies().get('session');
  return <div>{tab}: {session?.value}</div>;
}

// After: read cookies() / headers() / fs on the server, pass safe strings to Client Component
// app/dashboard_page_clean.tsx (Server Component)
import { cookies } from 'next/headers';
import { DashboardTabs } from './dashboard_tabs';

/** Loads user session theme on the server and renders interactive dashboard tabs. */
export default async function DashboardPageClean(): Promise<JSX.Element> {
  const cookieStore = await cookies();
  const activeTab = cookieStore.get('tab')?.value ?? 'overview';
  return <DashboardTabs initialTab={activeTab} />;
}
```

---

## 3. Unsafe XSS / DOM Sinks

**Finding:** `Security (Nextjs): unsafe XSS/DOM sink '{sink_name}' at L{line} (-{pts:.1f} pts)` (`-35.0 pts` per occurrence, capped at `-70.0 pts`)

Applies to `dangerouslySetInnerHTML`, `innerHTML`, `outerHTML`, `document.write`, `document.writeln`, and `insertAdjacentHTML`. Render typed JSX elements or server-sanitized plain text instead of raw HTML strings.

---

## 4. Inherited React & TypeScript Patterns in Next.js
- Split heavy table/chart/form route modules (`login_form.tsx`, `customers_table.tsx`, `revenue_chart.tsx`) by extracting formatting helpers and Server Action / API fetch functions out of UI components so `render_ui` does not mix with `network_io` or `storage_io`.
- Remember JSDoc comments (`/** ... */`) on exported helpers/hooks and explicit parameter/return types on non-JSX TypeScript helpers (`TypeScript Playbook`).
- **Finding: `Clean (DRY): DRY-XXX (type1|type2|type3, ...)`:** Deduplicate repeated Server Action validation, data-fetching wrappers, and shared Client Component leaf patterns into focused server utilities (`lib/`) or reusable UI components while respecting `'use client'` / `'use server'` boundaries.

