"use client";

/**
 * Flawed Next.js App Router client module importing server-only modules and writing unsafe DOM HTML.
 */
import React from "react";
import { headers } from "next/headers";

/** Render raw audit banner inside a leaked client/server App Router component. */
export function DashboardUnsafePanel({ rawHtml }: { readonly rawHtml: string }): React.JSX.Element {
  const hostEl = document.getElementById("audit-banner");
  if (hostEl) {
    hostEl.innerHTML = rawHtml;
  }
  return <div data-source={String(Boolean(headers))} dangerouslySetInnerHTML={{ __html: rawHtml }} />;
}
