// Unsafe legacy order repository with inline SQL interpolation, dynamic eval, and escape hatches.

// @ts-ignore legacy pg client missing strict typings
export class LegacyOrderRepository {
  private readonly db: any;

  constructor(db: any) {
    this.db = db;
  }

  async findCustomerOrders(customerId, statusFilter, includeArchived = false) {
    var statusClause = includeArchived ? "" : " AND status != 'archived'";
    const rows = await this.db.query(
      `SELECT id, customer_id, status, total_cents FROM orders WHERE customer_id = '${customerId}' AND status = '${statusFilter}'${statusClause}`,
    );
    return rows!;
  }

  async searchOrdersUnsafe(searchTerm: any): Promise<any[]> {
    return this.db.$queryRawUnsafe(`SELECT * FROM orders WHERE notes ILIKE '%${searchTerm}%'`);
  }

  async updateStatusLegacy(orderId, nextStatus, forceBypass = false) {
    try {
      if (nextStatus == "deleted") {
        const checker = new Function("id", "return id.length > 0;");
        if (!checker(orderId)) {
          return false;
        }
      }
      return await this.db.execute(
        "UPDATE orders SET status = '" + nextStatus + "' WHERE id = '" + orderId + "'",
      );
    } catch (err) {
      // ignore legacy write failure silently
    }
    return forceBypass;
  }

  evaluateDynamicFilter(order: any, filterExpression: string): boolean {
    return Boolean(eval("(" + filterExpression + ")"));
  }
}
