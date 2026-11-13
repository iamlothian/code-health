# React Refactoring Playbook

**Profile:** `react`  
**Detection:** `.jsx`/`.tsx` files with JSX syntax or `react` / `react-dom` imports, or `package.json` listing `"react"` in modules with `'use client'` / `'use server'` directives  
**Force:** `--framework react`  
**Builds on:** [TypeScript Playbook](typescript-playbook.md) (for `.tsx`) and [JavaScript Playbook](javascript-playbook.md) (for `.jsx`)  
**Worked examples:**  
- Clean: [task_preview_clean.tsx](../../../samples/typescript-react/good/task_preview_clean.tsx), [task_filter_bar.tsx](../../../samples/typescript-react/good/task_filter_bar.tsx), [delete_discussion.tsx](../../../samples/typescript-react/good/delete_discussion.tsx), [link.tsx](../../../samples/typescript-react/good/link.tsx), [discussion_view.tsx](../../../samples/typescript-react/good/discussion_view.tsx)  
- Flagged: [task_preview_legacy.tsx](../../../samples/typescript-react/bad/task_preview_legacy.tsx), [task_board_legacy.tsx](../../../samples/typescript-react/bad/task_board_legacy.tsx), [update_profile.tsx](../../../samples/typescript-react/bad/update_profile.tsx), [md_preview.tsx](../../../samples/typescript-react/bad/md_preview.tsx), [comments_list.tsx](../../../samples/typescript-react/bad/comments_list.tsx)

---

## Profile-Specific Rules & Exemptions

### UI Concern Buckets (`SRP`)
Alongside base TypeScript/JavaScript heuristics, the React profile maps UI-specific calls and adds `render_ui` whenever a function renders JSX (`jsx_elements_count > 0`):
- `network_io`: `fetch`, `window.fetch`, `axios*`, `HttpClient`
- `storage_io`: `localStorage.*`, `sessionStorage.*`
- `dom_mutation`: `document.getElementById`, `document.querySelector`, `document.querySelectorAll`, `document.createElement`, `window.open`
- `presentation`: `console.log`, `console.warn`, `console.error`, `console.info`
- `render_ui`: any non-zero JSX element count in the function body

Mixing `network_io` / `storage_io` / `dom_mutation` inside a JSX-rendering component produces `SRP: mixes N distinct I/O concerns ...` penalties.

### React Exemptions
- **Component return types:** PascalCase JSX-returning UI components (`name[0].isupper()` and `jsx_elements_count > 0`, excluding custom hooks `use[A-Z]*`) are **exempt** from `Clean: missing return type annotation`. Returning `JSX.Element` explicitly is still fine, just not penalized if omitted.
- **Custom hooks (`use[A-Z]*` without JSX):** Functions named `use[A-Z]*` with `jsx_elements_count == 0` are **exempt** from React's `effect sprawl` and `state sprawl` penalties so you can extract side effects and state out of components into dedicated hooks.

---

## 1. Rules of Hooks Violation

**Finding:** `Clean (React): Rules of Hooks violation calling '{call.name}' in branch/loop at L{call.lineno} (-{pts:.1f} pts)` (`-25.0 pts` per violation, capped at `-50.0 pts`)

Hooks (`use[A-Z]*`) must run unconditionally in the exact same order on every render. Calling `useState`, `useEffect`, or a custom hook inside an `if`, ternary, `for`, or `while` triggers this penalty.

```tsx
// Before (-25.0 pts Clean)
function TaskDetail({ id }: { id: string }) {
  if (!id) {
    return null;
  }
  const [task, setTask] = useState<Task | null>(null); // conditional hook after early return!
  return <div>{task?.title}</div>;
}

// After (0 pts)
function TaskDetail({ id }: { id: string }) {
  const [task, setTask] = useState<Task | null>(null);
  if (!id) {
    return null;
  }
  return <div>{task?.title}</div>;
}
```

---

## 2. Effect & State Sprawl (`useEffect` / `useState`)

**Findings:**
- `SRP (React): effect sprawl with {eff_cnt} useEffect/useLayoutEffect calls (>2) (-{pts:.1f} pts)` (`-8.0 pts` per excess effect over 2, capped at `-24.0 pts`)
- `SRP (React): state sprawl with {state_cnt} useState calls (>5) (-{pts:.1f} pts)` (`-5.0 pts` per excess `useState` over 5, capped at `-20.0 pts`)

**Fix:**
1. Extract cohesive data-fetching and synchronization effects into a custom hook (`useTaskBoard`, `useTaskFilter`) returning domain state and handlers.
2. Replace groups of related `useState` flags (`loading`, `error`, `data`, `filter`, `sort`, `selectedId`) with `useReducer` or a custom hook.
3. Derive computed values during render instead of storing mirror state synchronized via `useEffect`.

```tsx
// Before: component mixes 3 useEffect + 7 useState + fetch + localStorage + JSX
function TaskBoard() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState("all");
  const [sort, setSort] = useState("date");
  const [selectedId, setSelectedId] = useState(null);
  useEffect(() => { /* fetch tasks */ }, []);
  useEffect(() => { /* sync localStorage */ }, [filter]);
  useEffect(() => { /* document title */ }, [tasks]);
  return <main>{/* ... */}</main>;
}

// After: custom hook owns I/O & effects; component renders UI cleanly
function useTaskBoardData(): TaskBoardState {
  const [state, dispatch] = useReducer(taskBoardReducer, INITIAL_STATE);
  useEffect(() => { /* load tasks */ }, []);
  useEffect(() => { /* persist filter */ }, [state.filter]);
  return state;
}

/** Renders the task board header and task list. */
export function TaskBoard() {
  const { tasks, loading, error, filter, dispatch } = useTaskBoardData();
  return <main>{/* pure JSX presentation */}</main>;
}
```

---

## 3. Array Index Used as JSX `key`

**Finding:** `Clean (React): array index used as JSX key at L{line} (-{pts:.1f} pts)` (`-8.0 pts` per occurrence, capped at `-24.0 pts`)

Using the `.map((item, idx) => <Row key={idx} />)` index breaks reconciliation when lists are sorted, filtered, or inserted into. Always key by a stable domain ID (`item.id`).

```tsx
// Before (-8.0 pts)
{items.map((item, index) => (
  <CommentRow key={index} comment={item} />
))}

// After (0 pts)
{items.map((item) => (
  <CommentRow key={item.id} comment={item} />
))}
```

---

## 4. Unsafe XSS / DOM Sinks

**Finding:** `Security (React): unsafe XSS/DOM sink '{sink_name}' at L{line} (-{pts:.1f} pts)` (`-35.0 pts` per occurrence, capped at `-70.0 pts`)

Flagged sinks: `dangerouslySetInnerHTML`, `innerHTML`, `outerHTML`, `document.write`, `document.writeln`, `insertAdjacentHTML`.

**Fix:** Render structured JSX nodes (`{comment.body}`), use a safe Markdown-to-React component library without raw HTML injection, or replace imperative `innerHTML` mutations with declarative JSX children. See [md_preview.tsx](../../../samples/typescript-react/bad/md_preview.tsx) vs. [discussion_view.tsx](../../../samples/typescript-react/good/discussion_view.tsx).

