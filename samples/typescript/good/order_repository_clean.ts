/**
 * Parameterized PostgreSQL customer order repository using typed DTOs and explicit interfaces.
 */

export type OrderStatus = "pending" | "paid" | "shipped" | "cancelled";

export interface OrderRecord {
  readonly id: string;
  readonly customerId: string;
  readonly status: OrderStatus;
  readonly totalCents: number;
  readonly createdAtIso: string;
}

export interface QueryResult<T> {
  readonly rows: readonly T[];
}

export interface DatabaseClient {
  query<T>(sql: string, params: readonly unknown[]): Promise<QueryResult<T>>;
}

/** Handles strongly typed, parameterized persistence operations for customer orders. */
export class OrderRepository {
  /** Construct repository with an injected SQL query client. */
  constructor(private readonly db: DatabaseClient) {}

  /** Fetch all orders belonging to a specific customer sorted by newest first. */
  public async findByCustomer(customerId: string): Promise<readonly OrderRecord[]> {
    const sql =
      "SELECT id, customer_id, status, total_cents, created_at_iso " +
      "FROM orders WHERE customer_id = $1 ORDER BY created_at_iso DESC";
    const result = await this.db.query<OrderRecord>(sql, [customerId]);
    return result.rows;
  }

  /** Search customer orders matching a status and optional note substring safely. */
  public async searchCustomerOrders(
    customerId: string,
    status: OrderStatus,
    noteQuery: string,
  ): Promise<readonly OrderRecord[]> {
    const sql =
      "SELECT id, customer_id, status, total_cents, created_at_iso " +
      "FROM orders WHERE customer_id = $1 AND status = $2 AND notes ILIKE $3";
    const result = await this.db.query<OrderRecord>(sql, [customerId, status, `%${noteQuery}%`]);
    return result.rows;
  }

  /** Update an order status safely with bound SQL parameters. */
  public async updateStatus(orderId: string, nextStatus: OrderStatus): Promise<boolean> {
    if (!orderId.trim()) {
      throw new Error("Order ID must not be empty.");
    }
    const sql = "UPDATE orders SET status = $1 WHERE id = $2 RETURNING id";
    const result = await this.db.query<{ id: string }>(sql, [nextStatus, orderId]);
    return result.rows.length > 0;
  }
}

/** Compute total paid or shipped order value in cents for reporting. */
export function sumPaidCents(orders: readonly OrderRecord[]): number {
  let total = 0;
  for (const order of orders) {
    if (order.status === "paid" || order.status === "shipped") {
      total += order.totalCents;
    }
  }
  return total;
}
