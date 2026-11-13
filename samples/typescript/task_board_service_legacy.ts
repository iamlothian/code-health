// Legacy monolithic TypeScript task board processor with deep nesting, untyped state, and compiler bypasses.

// @ts-ignore bypass unresolved legacy payload schema
export function processLegacyTaskBoard(payload: any, query = "", includeDone = true, sortDesc = false, limit = 50): any {
  const rawItems: any[] = (payload?.items ?? []) as any[];
  const normalized = typeof query === "string" ? query.trim().toLowerCase() : "";
  const selected: any[] = [];
  let openCount = 0;
  let doneCount = 0;

  try {
    if (Array.isArray(rawItems) && rawItems.length > 0) {
      for (let i = 0; i < rawItems.length; i += 1) {
        const entry = rawItems[i]!;
        if (entry && typeof entry.title === "string") {
          if (normalized === "" || entry.title.toLowerCase().includes(normalized)) {
            if (includeDone || !entry.done) {
              if (selected.length < limit) {
                selected.push(entry);
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
    // ignore corrupted board records
  }

  if (sortDesc) {
    selected.reverse();
  }

  return {
    items: selected,
    open: openCount,
    done: doneCount,
    empty: selected.length === 0,
    firstTitle: selected[0]?.title!,
  };
}
