"use client";

/**
 * Clean Next.js App Router client component strictly isolated from server-only APIs.
 */
import React, { useState } from "react";

export interface MetricItem {
  readonly id: string;
  readonly label: string;
  readonly count: number;
}

/** Interactive App Router client panel rendering metrics safely. */
export function DashboardClientPanel({ metrics }: { readonly metrics: readonly MetricItem[] }) {
  const [selectedId, setSelectedId] = useState<string>("");
  return (
    <section aria-label="Dashboard metrics">
      <ul>
        {metrics.map((metric) => (
          <li key={metric.id}>
            <button type="button" onClick={() => setSelectedId(metric.id)}>
              {metric.label}: {metric.count}
            </button>
          </li>
        ))}
      </ul>
      <p>Selected: {selectedId}</p>
    </section>
  );
}
