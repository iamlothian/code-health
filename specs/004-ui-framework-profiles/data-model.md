# Data Model: Web UI Framework Code Health Profiles

**Date**: 2026-11-12  
**Feature**: Web UI Framework Code Health Profiles (`004-ui-framework-profiles`)  
**Spec**: [spec.md](./spec.md)

---

## 1. Generic Intermediate Representation (IR) Extensions (`scripts/_code_health/ir_models.py`)

All IR additions represent **generic, framework-agnostic language syntax primitives** with backward-compatible defaults so existing Python, Java, JS, and pure TS pipelines remain unchanged:

### 1.1 `IRCall` Extension
```python
@dataclass(frozen=True)
class IRCall:
    name: str
    callee_symbol: str = ""
    lineno: int = 1
    has_string_concat: bool = False
    has_string_arg: bool = False
    in_branch_or_loop: bool = False  # True when call occurs inside conditional/loop or nested callback within a function body
```

- **Callback Propagation Rule**: When scanning a component/function body, calls *inside* a nested `arrow_function` or `function_expression` callback receive `in_branch_or_loop=True`, while the outer call (e.g., top-level `useEffect(() => { ... }, [])`) retains the enclosing statement's `in_branch_or_loop` state.

### 1.2 `IRFunction` Extensions
```python
@dataclass
class IRFunction:
    # ... existing fields ...
    # Generic UI / JSX / DOM syntax telemetry (backward-compatible defaults)
    jsx_elements_count: int = 0
    dom_write_sinks: list[tuple[str, int]] = field(default_factory=list)   # e.g. [("dangerouslySetInnerHTML", 24), ("innerHTML", 31)]
    array_index_keys: list[int] = field(default_factory=list)              # 1-based line numbers of JSX key={index} in .map
```

### 1.3 `IRModule` Extensions
```python
@dataclass
class IRModule:
    # ... existing fields ...
    directives: list[str] = field(default_factory=list)  # Top-level JS/TS directive prologues (e.g. "use client", "use server")
```

---

## 2. Profile & Framework Hook Extensions (`ir_models.py` & `ir_scorer.py`)

To keep `UniversalIRScorer` 100% framework-blind while supporting framework-specific exemptions and module-level boundary checks:

### 2.1 `FrameworkProfile` Hooks
```python
@dataclass
class FrameworkProfile:
    name: str
    target_language: str
    concern_map: dict[str, str] = field(default_factory=dict)
    entrypoint_annotations: set[str] = field(default_factory=set)
    lcom4_exempt_annotations: set[str] = field(default_factory=set)

    def evaluate_module(self, module: IRModule) -> list[RulePenalty]: ...
    def evaluate_function(self, func: IRFunction, parent: IRClass | None) -> list[RulePenalty]: ...
    def evaluate_class(self, cls: IRClass) -> list[RulePenalty]: ...
    def extra_concerns(self, func: IRFunction) -> set[str]: return set()
    def requires_explicit_return_type(self, func: IRFunction) -> bool: return True
    def requires_constructor_docstring(self, cls: IRClass | None) -> bool: return True
    def is_lcom4_exempt(self, cls: IRClass) -> bool: ...
    def is_test_assert_call(self, call_name: str) -> bool: return False
```

### 2.2 `LanguageProfile` & Scorer/Module Delegation
- `LanguageProfile` delegates `evaluate_module`, `extra_concerns`, `requires_explicit_return_type` (`all(...)`), `requires_constructor_docstring` (`all(...)`), and `is_lcom4_exempt` (`any(...)`) to its active `self.frameworks`.
- `TypeScriptLanguageProfile` and `JavaScriptLanguageProfile` accept `frameworks: list[FrameworkProfile] | None = None` in `__init__` (defaulting to `[]`) and invoke `super().evaluate_function(func, parent)` / `super().evaluate_class(cls)` so attached frameworks always execute.
- `UniversalIRScorer.score_function` merges `self.profile.extra_concerns(func)` with call-mapped concerns (`self.profile.map_concern(call.name)`).
- `UniversalIRScorer.score_class` skips LCOM4 penalties when `self.profile.is_lcom4_exempt(cls)` is `True`.
- `UniversalIRScorer._score_source_clean_ir` skips missing return-type penalty when `not profile.requires_explicit_return_type(func)` and skips missing docstring penalty on constructors when `not profile.requires_constructor_docstring(parent)`.
- `ModuleAnalyzer._score_ir_module` / `_blend_scores` applies module-level `evaluate_module(ir_mod)` penalties across all affected dimensions (`srp`, `size`, `clean`, and `security`—deducting `sec_pen` from `u_sec`) and records module findings on `FileReport`.

---

## 3. UI Concern Map & Framework Profiles (`scripts/_code_health/profiles_ui.py`)

### 3.1 Shared Web UI Concern Map (`UI_CONCERN_MAP`)
| Call / Symbol Pattern | Concern Category |
|:---|:---|
| `fetch`, `window.fetch`, `axios`, `axios.get`, `axios.post`, `axios.put`, `axios.delete`, `HttpClient` | `network_io` |
| `localStorage.getItem`, `localStorage.setItem`, `localStorage.removeItem`, `sessionStorage.getItem`, `sessionStorage.setItem` | `storage_io` |
| `document.getElementById`, `document.querySelector`, `document.querySelectorAll`, `document.createElement`, `window.open` | `dom_mutation` |
| `console.log`, `console.warn`, `console.error`, `console.info` | `presentation` |
| `jsx_elements_count > 0` (component function renders JSX) | `render_ui` |

### 3.2 Rule Deduction Matrix

#### Custom Hook Predicates (Shared by React & Next.js)
- **Custom Hook Function**: `func.name.startswith("use") and len(func.name) > 3 and func.name[3].isupper()` and `func.jsx_elements_count == 0` (exempt from component-level `useEffect`/`useState` sprawl and JSX return-type exemption).
- **Custom Hook Module**: `Path(module.file_path).stem` matches `use[A-Z]*` (exempt from Next.js `app/` missing `"use client"` check).

#### React (`ReactFrameworkProfile`, `name="react"`)
| Dimension | Rule | Condition | Penalty |
|:---|:---|:---|:---|
| **Security** | Browser / JSX XSS Sink | `dangerouslySetInnerHTML`, `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write` | `-35.0 pts` per sink (cap `-70.0`) |
| **Clean** | Rules of Hooks Violation | `use[A-Z]*` call with `in_branch_or_loop=True` inside component/hook | `-25.0 pts` per violation (cap `-50.0`) |
| **Clean** | Array Index as JSX `key` | `len(func.array_index_keys) > 0` | `-8.0 pts` each (cap `-24.0`) |
| **Clean** | Inferred JSX Return Type | `func.jsx_elements_count > 0` and PascalCase component name (`func.name[:1].isupper()`) | **Exempt** from `-10.0 pts` missing return type |
| **SRP** | Effect Sprawl | `useEffect` + `useLayoutEffect` count `> 2` in a non-hook component | `-8.0 pts` per excess (cap `-24.0`) |
| **SRP** | State Sprawl | `useState` count `> 5` in a non-hook component | `-5.0 pts` per excess (cap `-20.0`) |
| **SRP** | UI Concern Mixing | `> 2` concerns across `UI_CONCERN_MAP` + `render_ui` | `-12.0 pts` per extra concern (via `UniversalIRScorer`) |

#### Next.js (`NextJsFrameworkProfile(ReactFrameworkProfile)`, `name="nextjs"`)
Inherits all `ReactFrameworkProfile` rules, plus module-level boundary checks in `evaluate_module(module)`:
| Dimension | Rule | Condition | Penalty |
|:---|:---|:---|:---|
| **Security** | Server Import in Client Module | `"use client"` in `module.directives` AND import matches server-only (`fs`, `node:*`, `child_process`, `next/headers`, `server-only`) | `-30.0 pts` (module Security) |
| **Clean** | Missing `"use client"` in App Router | Path under `app/` (not `pages/`), NOT a `use*` hook file, `"use client"` absent, AND calls client hooks (`useState`, `useEffect`, `useReducer`, `useRef`, `useContext`) | `-15.0 pts` (module Clean) |

#### Angular (`AngularFrameworkProfile`, `name="angular"`)
| Dimension | Rule | Condition | Penalty |
|:---|:---|:---|:---|
| **Security** | Sanitizer Bypass / DOM Sink | Calls `bypassSecurityTrustHtml`, `bypassSecurityTrustScript`, `bypassSecurityTrustUrl`, `bypassSecurityTrustResourceUrl`, or DOM sinks (`innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`) | `-35.0 pts` per sink (cap `-70.0`) |
| **SRP** | Controller/Component Layering | Class with `@Component` or `@Directive` injects `HttpClient` (constructor param type/name or `inject(HttpClient)` call) | `-20.0 pts` |
| **Clean** | Unmanaged RxJS Subscription | `@Component` / `@Directive` method calls `.subscribe(...)` without `takeUntilDestroyed`, `takeUntil`, `DestroyRef`, or `unsubscribe` in class | `-15.0 pts` |
| **Clean** | DI Constructor Exemption | `func.name == "constructor"` inside `@Component`/`@Directive`/`@Injectable`/`@Pipe` | **Exempt** from `-5.0 pts` missing docstring |
| **SRP** | Template-Bound LCOM4 Exemption | Class decorated with `@Component`, `@Directive`, `@Pipe`, or `@NgModule` | **Exempt** from LCOM4 split penalty |
