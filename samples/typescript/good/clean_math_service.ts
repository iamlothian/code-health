/**
 * Clean, strongly typed TypeScript arithmetic service for quickstart validation.
 */

/** Precision-aware four-function calculator. */
export class Calculator {
  private readonly precision: number;

  /** Initialize calculator with decimal precision. */
  constructor(precision: number = 2) {
    this.precision = precision;
  }

  /** Add two finite numbers and round to configured precision. */
  public add(a: number, b: number): number {
    return Number((a + b).toFixed(this.precision));
  }

  /** Subtract b from a and round to configured precision. */
  public subtract(a: number, b: number): number {
    return Number((a - b).toFixed(this.precision));
  }

  /** Multiply two numbers and round to configured precision. */
  public multiply(a: number, b: number): number {
    return Number((a * b).toFixed(this.precision));
  }

  /** Divide dividend by divisor with explicit zero guard. */
  public divide(a: number, b: number): number {
    if (b === 0) {
      throw new Error("Division by zero is undefined.");
    }
    return Number((a / b).toFixed(this.precision));
  }
}

/** Format a labeled numeric computation result for display. */
export function formatResult(label: string, value: number): string {
  return `${label}: ${value.toFixed(2)}`;
}
