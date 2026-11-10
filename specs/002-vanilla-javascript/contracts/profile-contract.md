# Profile Contract: JavaScript Language Profile

**Date**: 2026-11-09  
**Feature**: Vanilla JavaScript (ECMAScript) Language Profile  
**Spec**: [spec.md](../spec.md)  

---

## 1. Profile Definition Interface

`JavaScriptLanguageProfile` adheres to the `BaseProfileProtocol` defined in `scripts/_code_health/ir_scorer.py`:

```python
class BaseProfileProtocol(Protocol):
    name: str

    def evaluate_function(self, func: IRFunction, parent: IRClass | None) -> list[RulePenalty]:
        """Evaluate architectural and clean code violations for a function or method."""
        ...

    def evaluate_class(self, cls: IRClass) -> list[RulePenalty]:
        """Evaluate architectural violations for a class or record."""
        ...

    def map_concern(self, call_name: str) -> str | None:
        """Map a function/method call name to an operational concern category."""
        ...

    def is_entrypoint_func(self, func: IRFunction) -> bool:
        """Check if function is an external entrypoint with relaxed parameters."""
        ...

    def is_test_assert_call(self, call_name: str) -> bool:
        """Determine if a function/method call represents a test assertion."""
        ...
```

---

## 2. Behavioral Contract: `evaluate_function`

Given an `IRFunction`:
1. **Legacy `var` check**:
   - If `func.var_declarations_count > 0`:
     - Deduct `min(15.0, func.var_declarations_count * 3.0)` from Clean Code.
     - Finding: `Clean: {count} legacy 'var' declaration(s) detected (prefer 'const' or 'let') (-{pen:.1f} pts)`.
2. **Loose Equality check**:
   - If `func.loose_comparisons_count > 0`:
     - Deduct `min(10.0, func.loose_comparisons_count * 2.0)` from Clean Code.
     - Finding: `Clean: {count} loose equality comparison(s) (==/!=) trigger implicit type coercion (prefer ===/!==) (-{pen:.1f} pts)`.
3. **Empty catch blocks**:
   - For each `h` in `func.except_handlers` where `h.is_empty`:
     - Deduct `10.0` from Clean Code.
     - Finding: `Clean: empty catch block swallows exception (-10.0 pts)`.
4. **Debugger statements**:
   - If `func.has_debugger_statement`:
     - Deduct `10.0` from Clean Code.
     - Finding: `Clean: debugger statement detected (-10.0 pts)`.
5. **Dynamic evaluation (Security)**:
   - For each call matching `eval` or `Function` / `new Function`:
     - Deduct `40.0` from Security.
     - Finding: `Security: dynamic code execution via {call.name} (-40.0 pts)`.
6. **Timer string execution (Security)**:
   - For each call to `setTimeout` or `setInterval` where `call.has_string_arg`:
     - Deduct `20.0` from Security.
     - Finding: `Security: string argument to {call.name} causes implicit code evaluation (-20.0 pts)`.
7. **Prototype mutation (Security)**:
   - If `func.has_proto_mutation`:
     - Deduct `25.0` from Security.
     - Finding: `Security: direct prototype mutation via '__proto__' (-25.0 pts)`.
8. **`with` statement (Security & Operational Hygiene)**:
   - If `func.has_with_statement`:
     - Deduct `30.0` from Security.
     - Finding: `Security: 'with' statement obscures lexical scope and risks prototype pollution (-30.0 pts)`.

---

## 3. Behavioral Contract: `is_test_assert_call`

Returns `True` if `call_name` represents an assertion in common JavaScript test suites:
- Node.js `assert`: `assert`, `assert.strictEqual`, `assert.deepStrictEqual`, `assert.ok`, `assert.throws`
- Jest / Jasmine / Vitest: `expect`, `toBe`, `toEqual`, `toStrictEqual`, `toThrow`, `toBeTruthy`, `toBeFalsy`, `toHaveLength`
- Chai / Mocha: `should`, `expect`, `to.equal`, `to.be.true`, `to.be.false`
