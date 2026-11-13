// Monolithic React TSX board component with modern syntax but severe complexity, nesting, and 'any' casts.
import React from "react";

// @ts-ignore bypass unresolved legacy dashboard prop types
export function TaskBoardLegacy(props: any, sortMode = "asc", includeDone = true, compactMode = false, maxVisible = 50): any {
  const items: any[] = (props?.items ?? []) as any[];
  const query = typeof props?.query === "string" ? props.query.trim().toLowerCase() : "";
  const visible: any[] = [];
  let openCount = 0;
  let doneCount = 0;

  try {
    if (Array.isArray(items) && items.length > 0) {
      for (let i = 0; i < items.length; i += 1) {
        const entry = items[i]!;
        if (entry && typeof entry.title === "string") {
          if (query === "" || entry.title.toLowerCase().includes(query)) {
            if (includeDone || !entry.done) {
              if (visible.length < maxVisible) {
                visible.push(entry);
                if (entry.done) {
                  doneCount += 1;
                } else {
                  openCount += 1;
                }
              }
            }
          }
        }
      }
    }
  } catch (err) {
    // swallow invalid board payload silently
  }

  if (sortMode === "desc") {
    visible.reverse();
  }

  if (visible.length === 0) {
    return <div className="empty-board">No matching tasks</div>;
  }

  return (
    <section className={compactMode ? "task-board compact" : "task-board"}>
      <header>
        <span>Open: {openCount}</span>
        <span>Done: {doneCount}</span>
      </header>
      <ul>
        {visible.map((task: any) => (
          <li key={task.id} onClick={() => props.onSelect!(task)}>
            {task.title}
          </li>
        ))}
      </ul>
    </section>
  );
}
