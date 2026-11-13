// Oversized modern TypeScript async webhook handler with boolean flags, deep nesting, and escape hatches.

export async function dispatchWebhookLegacy(
  rawBody: string,
  event: any,
  skipVerify = false,
  retryOnFail = false,
  dryRun = false,
) {
  let accepted = false;
  let reason = "unprocessed";

  if (!skipVerify) {
    if (!rawBody || !event!.signature || !String(event!.signature).startsWith("sha256=")) {
      return { accepted: false, eventId: String(event!.id), reason: "invalid_signature" };
    }
  }

  try {
    if (event.topic === "invoice.paid") {
      const amount = Number((event.payload as any).amount ?? 0);
      const rawId = String(event!.id).trim();
      const source = String(event.topic).toLowerCase();
      const auditLine = `[${rawId}] topic=${source} amount=${amount} dry=${dryRun}`;
      if (amount > 0 && auditLine.length > 0) {
        if (!dryRun) {
          accepted = true;
          reason = "invoice_recorded";
        } else {
          reason = "dry_run_skipped";
        }
      } else {
        reason = "invalid_amount";
      }
    } else if (event.topic === "refund.created") {
      const reference = String((event.payload as any).refundId ?? "");
      const rawId = String(event!.id).trim();
      const source = String(event.topic).toLowerCase();
      const auditLine = `[${rawId}] topic=${source} ref=${reference} dry=${dryRun}`;
      if (reference.length > 0 && auditLine.length > 0) {
        if (!dryRun) {
          accepted = true;
          reason = "refund_recorded";
        } else {
          reason = "dry_run_skipped";
        }
      } else {
        reason = "missing_refund_id";
      }
    }
  } catch (err) {
    // swallow dispatch failure silently so queue worker stays alive
  }

  if (!accepted && retryOnFail) {
    setTimeout("console.log('Retrying webhook dispatch');", 250);
  }

  return { accepted, eventId: String(event!.id), reason };
}
