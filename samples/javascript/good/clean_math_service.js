/**
 * High-performance arithmetic utility service written in modern ECMAScript.
 */
class MathService {
  constructor(precision = 2) {
    this.precision = precision;
  }

  /**
   * Sum two numbers with default fallbacks.
   * @param {number} a
   * @param {number} b
   */
  add(a = 0, b = 0) {
    return Number((a + b).toFixed(this.precision));
  }

  /**
   * Subtract subtrahend from minuend.
   * @param {number} a
   * @param {number} b
   */
  subtract(a = 0, b = 0) {
    return Number((a - b).toFixed(this.precision));
  }

  /**
   * Multiply two factors.
   * @param {number} a
   * @param {number} b
   */
  multiply(a = 1, b = 1) {
    return Number((a * b).toFixed(this.precision));
  }

  /**
   * Divide dividend by divisor safely.
   * @param {number} a
   * @param {number} b
   */
  divide(a = 0, b = 1) {
    if (b === 0) {
      throw new Error("Division by zero is undefined.");
    }
    return Number((a / b).toFixed(this.precision));
  }
}

module.exports = { MathService };
