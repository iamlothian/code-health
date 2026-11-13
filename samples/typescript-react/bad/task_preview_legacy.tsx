// Legacy React component with conditional hook calls, array index keys, effect sprawl, and unsafe innerHTML sink.
import React, { useEffect, useState } from "react";

/** Render raw HTML previews using anti-patterns blocked by React code health rules. */
export function TaskPreviewLegacy({ enabled, items }: { readonly enabled: boolean; readonly items: readonly string[] }): React.JSX.Element {
  const [status, setStatus] = useState("idle");

  if (enabled) {
    useEffect(() => {
      setStatus("ready");
    }, [enabled]);
  }
  useEffect(() => {
    setStatus("synced");
  }, [items]);
  useEffect(() => {
    setStatus("logged");
  }, [status]);

  return (
    <section>
      <ul>
        {items.map((htmlSnippet, index) => (
          <li key={index} dangerouslySetInnerHTML={{ __html: htmlSnippet }} />
        ))}
      </ul>
    </section>
  );
}
