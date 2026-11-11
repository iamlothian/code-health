/**
 * Generic bounded Least Recently Used (LRU) cache with cohesive eviction and hit-rate metrics.
 */

export interface CacheStats {
  readonly hits: number;
  readonly misses: number;
  readonly evictions: number;
  readonly size: number;
  readonly capacity: number;
}

/** Cohesive in-memory LRU cache backed by JavaScript Map insertion order. */
export class LRUCache<K, V> {
  private readonly store = new Map<K, V>();
  private hits = 0;
  private misses = 0;
  private evictions = 0;

  /** Initialize cache with a strictly positive entry capacity. */
  constructor(private readonly capacity: number = 128) {
    if (capacity < 1) {
      throw new RangeError("Cache capacity must be at least 1.");
    }
  }

  /** Retrieve a cached value and promote its key to most-recently used. */
  public get(key: K): V | undefined {
    if (!this.store.has(key)) {
      this.misses += 1;
      return undefined;
    }
    this.hits += 1;
    const value = this.store.get(key) as V;
    this.touchKey(key, value);
    return value;
  }

  /** Insert or update a key-value pair, evicting the oldest entry if full. */
  public put(key: K, value: V): void {
    if (this.store.has(key)) {
      this.touchKey(key, value);
      return;
    }
    if (this.store.size >= this.capacity) {
      this.evictLeastRecent();
    }
    this.store.set(key, value);
  }

  /** Inspect whether a key exists without altering recency order. */
  public has(key: K): boolean {
    return this.store.has(key);
  }

  /** Remove a specific key from the cache and return whether it existed. */
  public delete(key: K): boolean {
    return this.store.delete(key);
  }

  /** Clear all cached entries and reset lifetime telemetry counters. */
  public clear(): void {
    this.store.clear();
    this.hits = 0;
    this.misses = 0;
    this.evictions = 0;
  }

  /** Return a snapshot of current cache size and hit/miss statistics. */
  public getStats(): CacheStats {
    return {
      hits: this.hits,
      misses: this.misses,
      evictions: this.evictions,
      size: this.store.size,
      capacity: this.capacity,
    };
  }

  /** Promote an existing key to the tail (most-recently used) position. */
  private touchKey(key: K, value: V): void {
    this.store.delete(key);
    this.store.set(key, value);
  }

  /** Evict the oldest inserted key when cache capacity is reached. */
  private evictLeastRecent(): void {
    const oldest = this.store.keys().next();
    if (!oldest.done) {
      this.store.delete(oldest.value);
      this.evictions += 1;
    }
  }
}
