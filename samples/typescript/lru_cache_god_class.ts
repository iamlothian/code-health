// Uncohesive cache god class mixing storage, telemetry, CSV export, audit logging, and config mutation.

// @ts-ignore legacy map polyfill compatibility
export class LegacyCacheManager {
  private store: Map<string, any>;
  private auditEvents: string[];
  private maxSize: number;
  private hitCount: number;
  private missCount: number;
  private lastExportTimestamp: number;
  private debugLabel: string;

  constructor(maxSize: number = 128) {
    this.store = new Map<string, any>();
    this.auditEvents = [];
    this.maxSize = maxSize;
    this.hitCount = 0;
    this.missCount = 0;
    this.lastExportTimestamp = 0;
    this.debugLabel = "default";
  }

  set label(value: string) {
    this.debugLabel = value;
  }

  get(key): any {
    if (!this.store.has(key)) {
      this.missCount += 1;
      return undefined;
    }
    this.hitCount += 1;
    const val = this.store.get(key)!;
    this.store.delete(key);
    this.store.set(key, val);
    return val;
  }

  put(key, value: any): void {
    if (this.store.has(key)) {
      this.store.delete(key);
      this.store.set(key, value);
      return;
    }
    if (this.store.size >= this.maxSize) {
      const oldest = this.store.keys().next().value!;
      this.store.delete(oldest);
    }
    this.store.set(key, value);
  }

  has(key): boolean {
    return this.store.has(key);
  }

  delete(key): boolean {
    return this.store.delete(key);
  }

  clearStore(): void {
    this.store.clear();
  }

  recordAuditEvent(message): void {
    this.auditEvents.push(String(message));
  }

  drainAuditEvents(): string[] {
    const copy = this.auditEvents.slice();
    this.auditEvents = [];
    return copy;
  }

  exportCountersCsv(): string {
    this.lastExportTimestamp = Date.now();
    return `${this.hitCount},${this.missCount},${this.lastExportTimestamp}`;
  }

  resetCounters(): void {
    this.hitCount = 0;
    this.missCount = 0;
  }

  getHitRatio(): number {
    const total = this.hitCount + this.missCount;
    return total == 0 ? 0 : this.hitCount / total;
  }

  formatDebugBanner(prefix): string {
    return `[${prefix}:${this.debugLabel}]`;
  }

  computeHealthStatus(): string {
    const ratio = this.hitCount + this.missCount;
    if (ratio == 0) {
      return "COLD";
    }
    return "ACTIVE";
  }

  serializeLastExportIso(): string {
    return new Date(this.lastExportTimestamp).toISOString();
  }
}
