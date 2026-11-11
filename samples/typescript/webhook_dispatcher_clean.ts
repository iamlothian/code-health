/**
 * Typed async webhook dispatcher demonstrating interface contracts, arrow handlers, and shallow early returns.
 */

export type WebhookTopic = "invoice.paid" | "refund.created";

export interface WebhookEvent<TPayload = Record<string, string | number>> {
  readonly id: string;
  readonly topic: WebhookTopic;
  readonly signature: string;
  readonly payload: TPayload;
}

export interface DispatchOutcome {
  readonly accepted: boolean;
  readonly eventId: string;
  readonly reason: string;
}

export type SignatureVerifier = (payload: string, signature: string) => boolean;

/** Verify HMAC-style webhook signature prefix cleanly using typed arrow assignment. */
export const verifyWebhookSignature: SignatureVerifier = (
  payload: string,
  signature: string,
): boolean => {
  return payload.length > 0 && signature.startsWith("sha256=");
};

/** Registry of strongly typed async handlers keyed by domain action. */
export const webhookHandlers = {
  /** Acknowledge a paid invoice webhook event. */
  async handleInvoicePaid(event: WebhookEvent): Promise<DispatchOutcome> {
    const amount = Number(event.payload.amount ?? 0);
    if (amount <= 0) {
      return { accepted: false, eventId: event.id, reason: "invalid_amount" };
    }
    return { accepted: true, eventId: event.id, reason: "invoice_recorded" };
  },

  /** Acknowledge a refund creation webhook event. */
  async handleRefundCreated(event: WebhookEvent): Promise<DispatchOutcome> {
    const reference = String(event.payload.refundId ?? "");
    if (!reference) {
      return { accepted: false, eventId: event.id, reason: "missing_refund_id" };
    }
    return { accepted: true, eventId: event.id, reason: "refund_recorded" };
  },
};

/** Dispatch a verified webhook event to the matching domain handler. */
export async function dispatchWebhook(
  rawBody: string,
  event: WebhookEvent,
): Promise<DispatchOutcome> {
  if (!verifyWebhookSignature(rawBody, event.signature)) {
    return { accepted: false, eventId: event.id, reason: "invalid_signature" };
  }
  if (event.topic === "invoice.paid") {
    return webhookHandlers.handleInvoicePaid(event);
  }
  return webhookHandlers.handleRefundCreated(event);
}
