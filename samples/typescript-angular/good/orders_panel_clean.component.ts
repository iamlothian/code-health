/**
 * Clean Angular component delegating HTTP to an injected service and cleaning up via takeUntilDestroyed.
 */
import { Component, DestroyRef, inject, OnInit } from "@angular/core";
import { takeUntilDestroyed } from "@angular/core/rxjs-interop";

export interface OrderRecord {
  readonly id: string;
  readonly label: string;
}

export interface OrdersFacade {
  streamOrders: () => {
    pipe: (op: unknown) => { subscribe: (fn: (rows: OrderRecord[]) => void) => void };
  };
}

/** Clean standalone Angular orders view with compliant DI and RxJS lifecycle hygiene. */
@Component({ selector: "app-orders-panel", template: "<section></section>" })
export class OrdersPanelComponent implements OnInit {
  private readonly destroyRef = inject(DestroyRef);
  orders: OrderRecord[] = [];
  selectedOrderId = "";

  constructor(private readonly ordersFacade: OrdersFacade) {}

  /** Subscribe to order updates bound to DestroyRef lifetime. */
  ngOnInit(): void {
    this.ordersFacade
      .streamOrders()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe((rows: OrderRecord[]) => {
        this.orders = rows;
      });
  }

  /** Record user selection without direct DOM access. */
  onSelectOrder(orderId: string): string {
    this.selectedOrderId = orderId;
    return this.selectedOrderId;
  }

  /** Format display title safely. */
  formatOrderLabel(label: string): string {
    return label.trim();
  }
}
