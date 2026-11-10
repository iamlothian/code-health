# Data Model: TypeScript Language Profile

**Date**: 2026-11-09  
**Feature**: TypeScript Language Profile  
**Spec**: [spec.md](./spec.md)  

---

## 1. Intermediate Representation (IR) Extensions

The language-neutral `IRFunction` dataclass in `scripts/_code_health/ir_models.py` is extended with backward-compatible optional fields to capture TypeScript type safety and escape hatch telemetry without breaking existing Python, Java, or JavaScript analyzers.

```python
@dataclass
class IRFunction:
    # Existing core fields
    name: str
    qualname: str
    lineno: int
    end_lineno: int
    loc: int
    params: list[IRParam]
    return_type: str | None
    max_nesting: int
    cyclomatic_complexity: int
    cognitive_complexity: int
    returns_count: int
    calls: list[IRCall]
    accessed_fields: list[str]
    except_handlers: list[IRExceptHandler]
    is_test: bool
    annotations: list[IRAnnotation] = field(default_factory=list)
    modifiers: list[str] = field(default_factory=list)
    has_docstring: bool = True

    # JavaScript-specific rule tracking (backward-compatible defaults)
    var_declarations_count: int = 0
    loose_comparisons_count: int = 0
    has_proto_mutation: bool = False
    has_with_statement: bool = False
    has_debugger_statement: bool = False

    # TypeScript-specific rule tracking (backward-compatible defaults)
    explicit_any_count: int = 0
    ts_ignore_count: int = 0
    non_null_assertion_count: int = 0
```

### Parameter Representation (`IRParam`)

```python
@dataclass(frozen=True)
class IRParam:
    name: str
    type_annotation: str | None = None
    has_default: bool = False
    annotations: list[IRAnnotation] = field(default_factory=list)
```

- In TypeScript, `has_default=True` when a parameter has a default initializer (`param = value`) or is an optional parameter (`param?: string`).
- `type_annotation` captures the textual type representation (e.g., `: string` $\rightarrow$ `"string"`, `: boolean` $\rightarrow$ `"bool"`, `: any` $\rightarrow$ `"any"`).
- In constructors, parameters with access modifiers (`public`, `private`, `protected`) or `readonly` are also extracted as `IRField` entries on the enclosing `IRClass` to support accurate LCOM4 cohesion analysis.

---

## 2. TypeScript Language Profile

Defined in `scripts/_code_health/profiles_ts.py` and exported through `scripts/_code_health/profiles.py`.

```python
class TypeScriptLanguageProfile(JavaScriptLanguageProfile):
    """TypeScript language profile evaluating strict typing, escape hatches, anti-coercion, and security rules."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "typescript"
        self.file_extensions = (".ts", ".tsx", ".mts", ".cts")

    def evaluate_function(self, func: IRFunction, parent: IRClass | None) -> list[RulePenalty]:
        """Evaluate TS function-level rules (any, ts-ignore, non-null assertions, query injection, and JS smells)."""
        ...

    def evaluate_class(self, cls: IRClass) -> list[RulePenalty]:
        """Evaluate class-level rules."""
        ...

    def is_test_assert_call(self, call_name: str) -> bool:
        """Recognize standard TS/JS test assertion matchers (expect, assert, should, toBe, toEqual)."""
        ...
```

---

## 3. Rule Deduction Matrix

| Dimension | Rule | Condition | Penalty |
|:---|:---|:---|:---|
| **Clean Code** | Untyped Parameter | Parameter in non-test function has `type_annotation is None` and `not has_default` | `-5.0 pts` each (cap `-25.0 pts`) |
| **Clean Code** | Missing Return Type | Non-test, non-constructor function has `return_type is None` | `-10.0 pts` |
| **Clean Code** | Explicit `any` Usage | `func.explicit_any_count > 0` (`: any`, `as any`, `<any>x`, `Array<any>`) | `-5.0 pts` each (cap `-20.0 pts`) |
| **Clean Code** | Compiler Suppression | `func.ts_ignore_count > 0` (`@ts-ignore` or `@ts-nocheck` comments) | `-10.0 pts` each (cap `-20.0 pts`) |
| **Clean Code** | Non-Null Assertion | `func.non_null_assertion_count > 0` (`expr!`) | `-2.0 pts` each (cap `-10.0 pts`) |
| **Clean Code** | Missing Docstring | Public/exported class or function missing JSDoc/TSDoc block | `-5.0 pts` ($\le 10$ LOC), `-10.0 pts` ($> 10$ LOC), `-15.0 pts` (class) |
| **Clean Code** | Loose Equality (`==`/`!=`) | `func.loose_comparisons_count > 0` (implicit coercion smell) | `-2.0 pts` each (cap `-10.0 pts`) |
| **Clean Code** | Legacy `var` Declaration | `func.var_declarations_count > 0` | `-3.0 pts` each (cap `-15.0 pts`) |
| **Clean Code** | Empty `catch` Block | Swallowed exception in `catch` block | `-10.0 pts` |
| **Clean Code** | Debugger Statement | `func.has_debugger_statement` | `-10.0 pts` |
| **Clean Code** | Test Assertion Hygiene | Test function has 0 assertions | `-30.0 pts` |
| **Clean Code** | Excessive Assertions | Test function has $> 8$ assertions | `-3.0 pts` per excess (cap `-30.0 pts`) |
| **SRP** | Boolean Default Flag | Parameter with default boolean value (`flag: boolean = false` or `flag = false`) | `-6.0 pts` |
| **SRP** | LCOM4 Class Cohesion | Disconnected field access groups in class (`cls.lcom4 > 1`) | `-15.0 pts` per component $> 1$ |
| **Security** | Dynamic Execution | Invocation of `eval(...)` or `new Function(...)` | `-40.0 pts` |
| **Security** | Timer String Execution | `setTimeout` or `setInterval` with string literal argument | `-20.0 pts` |
| **Security** | Prototype Tampering | Direct mutation of `__proto__` or `Object.setPrototypeOf` | `-25.0 pts` |
| **Security** | With Statement | Use of `with (...)` statement | `-30.0 pts` |
| **Security** | SQL / Query Concatenation | Query method (`query`, `execute`, `raw`, `$queryRawUnsafe`, `$executeRawUnsafe`) with string concat or template interpolation | `-40.0 pts` |

---

## 4. Entity Lifecycle & Flow

```
+------------------------------------+
|  TypeScript File (.ts, .tsx, etc.) |
+-----------------+------------------+
                  |
                  | parse_typescript_file()
                  v
+------------------------------------+
|             IRModule               |
|  - loc, imports, is_test           |
|  - classes: list[IRClass]          |
|  - functions: list[IRFunction]     |
+-----------------+------------------+
                  |
                  | UniversalIRScorer + TypeScriptLanguageProfile
                  v
+------------------------------------+
|            FileReport              |
|  - SRP, Size, Comp, Clean, Sec     |
|  - Line-numbered findings          |
+------------------------------------+
```
