# Data Model: Vanilla JavaScript (ECMAScript) Language Profile

**Date**: 2026-11-09  
**Feature**: Vanilla JavaScript (ECMAScript) Language Profile  
**Spec**: [spec.md](./spec.md)  

---

## 1. Intermediate Representation (IR) Extensions

The language-neutral `IRFunction` dataclass in `scripts/_code_health/ir_models.py` is extended with backward-compatible fields to capture JavaScript-specific language constructs without breaking Python or Java analyzers.

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
- In JavaScript, `has_default=True` when a parameter has a default initializer (`param = defaultValue`).
- `type_annotation` is populated from JSDoc `@param {type}` if present, or set to `"inferred"` when `has_default=True`.

---

## 2. JavaScript Language Profile

Defined in `scripts/_code_health/profiles_js.py` and exported through `scripts/_code_health/profiles.py`.

```python
class JavaScriptLanguageProfile(LanguageProfile):
    """ECMAScript language profile evaluating code health, anti-coercion, and security rules."""

    def __init__(self) -> None:
        super().__init__(
            name="javascript",
            file_extensions=(".js", ".mjs", ".cjs"),
            frameworks=[],
        )

    def evaluate_function(self, func: IRFunction, parent: IRClass | None) -> list[RulePenalty]:
        """Evaluate JS function-level rules (var, loose equality, with, debugger, timers, proto, new Function)."""
        ...

    def evaluate_class(self, cls: IRClass) -> list[RulePenalty]:
        """Evaluate class-level rules."""
        ...

    def is_test_assert_call(self, call_name: str) -> bool:
        """Recognize standard JS test assertion matchers (expect, assert, should, toBe, toEqual)."""
        ...

    def map_concern(self, call_name: str) -> str | None:
        """Map standard calls to concern buckets."""
        ...
```

### Rule Deduction Matrix

| Dimension | Rule | Condition | Penalty |
|:---|:---|:---|:---|
| **Clean Code** | Untyped Parameter | Parameter in non-test function has `type_annotation is None` and `not has_default` | `-2.0 pts` each (cap `-10.0 pts`) |
| **Clean Code** | Missing Docstring | Exported / top-level function or class without JSDoc block | `-5.0 pts` ($\le 10$ LOC) or `-10.0 pts` ($> 10$ LOC) |
| **Clean Code** | Loose Equality (`==`/`!=`) | `func.loose_comparisons_count > 0` (implicit coercion smell) | `-2.0 pts` each (cap `-10.0 pts`) |
| **Clean Code** | Legacy `var` Declaration | `func.var_declarations_count > 0` | `-3.0 pts` each (cap `-15.0 pts`) |
| **Clean Code** | Empty `catch` Block | `any(h.is_empty for h in func.except_handlers)` | `-10.0 pts` |
| **Clean Code** | Debugger Statement | `func.has_debugger_statement` | `-10.0 pts` |
| **Clean Code** | Test Assertion Hygiene | Test function has 0 assertions | `-30.0 pts` |
| **Clean Code** | Test Assertion Overcrowding | Test function has $> 8$ assertions | `-3.0 pts` each (cap `-30.0 pts`) |
| **Security** | Dynamic Code Evaluation | Call to `eval(...)` or `new Function(...)` | `-40.0 pts` |
| **Security** | Timer String Execution | `setTimeout` or `setInterval` with string literal first argument | `-20.0 pts` |
| **Security** | Prototype Mutation | Assignment or access to `__proto__` | `-25.0 pts` |
| **Security** | `with` Statement | `func.has_with_statement` | `-30.0 pts` |

---

## 3. Tree-Sitter CST Node Mapping Table

The parser in `scripts/_code_health/js_parser.py` maps Tree-Sitter JavaScript CST nodes to normalized IR models:

| JavaScript CST Node Type | IR Target | Description / Extraction Logic |
|:---|:---|:---|
| `program` | `IRModule` | Root CST node representing the file. Computes effective LOC. |
| `class_declaration`, `class` | `IRClass` | ES6 class definition. Extracts name, bases (`extends`), fields, and methods. |
| `field_definition` | `IRField` | Public/private class fields (`this.x`, `#privateField`). |
| `method_definition` | `IRFunction` | Instance or static class method. `qualname` formatted as `ClassName.methodName`. |
| `function_declaration` | `IRFunction` | Top-level or nested function declaration. `qualname` formatted as `funcName`. |
| `variable_declarator` + `arrow_function` | `IRFunction` | Function assigned to variable (`const f = () => {}`). `qualname` set to variable name. |
| `pair` with method in object literal | `IRFunction` | Method inside object literal (`const obj = { m() {} }`). `qualname` set to `obj.m`. |
| `call_expression` (`it`, `test`) | `IRFunction` | BDD test block. Extracts callback argument with `is_test=True` and `name="test: " + title`. |
| `formal_parameters` | `list[IRParam]` | Function arguments. Detects `assignment_pattern` for `has_default=True`. |
| `call_expression` | `IRCall` | Function/method invocation. Checks string concat and string literals in timer calls. |
| `catch_clause` | `IRExceptHandler` | Exception catch block. Checks whether statement block is empty. |
| `member_expression` (`this.x`) | `accessed_fields` | Tracks property access on `this` for LCOM4 connected components. |
| `with_statement` | `has_with_statement` | Sets flag on enclosing `IRFunction`. |
| `debugger_statement` | `has_debugger_statement`| Sets flag on enclosing `IRFunction`. |
| `binary_expression` (`==`, `!=`) | `loose_comparisons`| Increments count on enclosing `IRFunction`. |
| `variable_declaration` (`var`) | `var_declarations` | Increments count on enclosing `IRFunction`. |

---

## 4. Entity Lifecycle & Data Flow

```
1. File Discovery (reporting.py)
   ├── Discovers *.js, *.mjs, *.cjs
   ├── Skips *.min.js and files with lines > 1,000 chars
   └── Filters out node_modules, dist, build, .next, .nuxt

2. Dispatcher (module_engine.py)
   ├── Checks tree-sitter & tree-sitter-javascript dependencies (ParserGuard)
   │   └── If missing: raises MissingNativeParserError -> halts with exit code 2
   └── Invokes parse_javascript_file(path, rel_path, is_test)

3. CST Parsing & Normalization (js_parser.py)
   ├── Builds Tree-Sitter CST
   ├── Extracts classes, methods, and functions (absorbing inline callbacks)
   ├── Computes CC (branch count) and Cognitive Complexity (nesting penalty)
   └── Returns normalized IRModule

4. Scoring (ir_scorer.py with JavaScriptLanguageProfile)
   ├── UniversalIRScorer scores IRModule, IRClass, and IRFunction units
   ├── Evaluates Clean Code anti-coercion (==, var, empty catch, JSDoc inference)
   ├── Evaluates Security rules (eval, new Function, __proto__, with, timers)
   └── Blends unit scores with module LOC and Git stats into FileReport

5. Output Generation (reporting.py / code_health.py)
   └── Formats FileReports into Console, Markdown, or JSON scorecards
```
