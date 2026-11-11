/**
 * Clean modular React 18 TSX task triage filter bar with strict prop contracts.
 */
import React from "react";

export type TaskStatus = "all" | "open" | "done";

export interface TaskItem {
  readonly id: string;
  readonly title: string;
  readonly done: boolean;
}

export interface TaskFilterProps {
  readonly query: string;
  readonly status: TaskStatus;
  readonly onQueryChange: (next: string) => void;
  readonly onStatusChange: (status: TaskStatus) => void;
}

/** Filter task rows matching a case-insensitive query and completion status. */
export function filterTasks(
  tasks: readonly TaskItem[],
  query: string,
  status: TaskStatus,
): TaskItem[] {
  const normalized = query.trim().toLowerCase();
  return tasks.filter((item) => {
    const matchesText = normalized === "" || item.title.toLowerCase().includes(normalized);
    const matchesStatus = status === "all" || (status === "done" ? item.done : !item.done);
    return matchesText && matchesStatus;
  });
}

/** Count open and completed tasks in a single pass. */
export function summarizeTasks(tasks: readonly TaskItem[]): { open: number; done: number } {
  let open = 0;
  let done = 0;
  for (const task of tasks) {
    if (task.done) {
      done += 1;
    } else {
      open += 1;
    }
  }
  return { open, done };
}

/** Render an accessible search input box for filtering tasks. */
function SearchInput({
  value,
  onChange,
}: {
  readonly value: string;
  readonly onChange: (next: string) => void;
}): React.JSX.Element {
  return (
    <input
      type="search"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder="Filter tasks..."
      aria-label="Filter tasks"
    />
  );
}

/** Render the task search box and completion status selector toolbar. */
export function TaskFilterBar({
  query,
  status,
  onQueryChange,
  onStatusChange,
}: TaskFilterProps): React.JSX.Element {
  return (
    <div className="task-filter-bar">
      <SearchInput value={query} onChange={onQueryChange} />
      <select
        value={status}
        onChange={(e) => onStatusChange(e.target.value as TaskStatus)}
        aria-label="Filter status"
      >
        <option value="all">All</option>
        <option value="open">Open</option>
        <option value="done">Done</option>
      </select>
    </div>
  );
}
