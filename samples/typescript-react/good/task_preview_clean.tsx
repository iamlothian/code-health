/**
 * Clean React 18 TSX preview card using top-level custom hook and safe JSX rendering.
 */
import React, { useMemo, useState } from "react";

export interface PreviewTask {
  readonly id: string;
  readonly title: string;
  readonly summary: string;
}

/** Return true when a task title contains the normalized search term. */
function titleMatches(task: PreviewTask, normalizedQuery: string): boolean {
  return normalizedQuery === "" || task.title.toLowerCase().includes(normalizedQuery);
}

/** Custom hook maintaining query state and memoized matching task slice. */
export function useFilteredPreview(tasks: readonly PreviewTask[]): {
  readonly query: string;
  readonly setQuery: (next: string) => void;
  readonly visible: readonly PreviewTask[];
} {
  const [query, setQuery] = useState("");
  const visible = useMemo(() => {
    const normalized = query.trim().toLowerCase();
    return tasks.filter((item) => titleMatches(item, normalized));
  }, [tasks, query]);
  return { query, setQuery, visible };
}

/** Render escaped task cards with stable item ID keys. */
export function TaskPreviewPanel({ tasks }: { readonly tasks: readonly PreviewTask[] }) {
  const { query, setQuery, visible } = useFilteredPreview(tasks);
  return (
    <section className="task-preview">
      <input
        type="search"
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        aria-label="Filter preview tasks"
      />
      <ul>
        {visible.map((task) => (
          <li key={task.id}>
            <h3>{task.title}</h3>
            <p>{task.summary}</p>
          </li>
        ))}
      </ul>
    </section>
  );
}
