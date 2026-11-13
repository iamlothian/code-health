/**
 * Pure framework-free TypeScript task board filtering and summary domain service.
 */

export type WorkItemStatus = "all" | "open" | "done";

export interface WorkItem {
  readonly id: string;
  readonly title: string;
  readonly priority: number;
  readonly done: boolean;
}

export interface WorkBoardSummary {
  readonly total: number;
  readonly open: number;
  readonly done: number;
}

/** Check whether a work item matches a normalized search query and status filter. */
export function matchesWorkItem(item: WorkItem, normalizedQuery: string, status: WorkItemStatus): boolean {
  const matchesText = normalizedQuery === "" || item.title.toLowerCase().includes(normalizedQuery);
  const matchesStatus = status === "all" || (status === "done" ? item.done : !item.done);
  return matchesText && matchesStatus;
}

/** Filter and sort work items using strict TypeScript contracts and shallow helpers. */
export function filterWorkItems(
  items: readonly WorkItem[],
  query: string,
  status: WorkItemStatus,
): WorkItem[] {
  const normalized = query.trim().toLowerCase();
  return items
    .filter((item) => matchesWorkItem(item, normalized, status))
    .sort((left, right) => right.priority - left.priority);
}

/** Summarize open, done, and total counts for a slice of work items. */
export function summarizeWorkBoard(items: readonly WorkItem[]): WorkBoardSummary {
  let open = 0;
  let done = 0;
  for (const item of items) {
    if (item.done) {
      done += 1;
    } else {
      open += 1;
    }
  }
  return { total: items.length, open, done };
}
