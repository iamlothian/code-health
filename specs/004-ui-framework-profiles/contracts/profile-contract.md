# Profile Contract: Web UI Framework Profiles

**Date**: 2026-11-12  
**Feature**: Web UI Framework Code Health Profiles (`004-ui-framework-profiles`)  
**Spec**: [spec.md](../spec.md)

---

## 1. Framework Isolation Contract

1. **Raw Language Profiles (`profiles_js.py`, `profiles_ts.py`)**:
   - Accept optional `frameworks: list[FrameworkProfile] | None = None` (default `[]`).
   - Never hardcode React, Next.js, or Angular rules or concern names.
   - Delegate to `self.frameworks` inside `evaluate_function` and `evaluate_class` (via `LanguageProfile`).
2. **CST Parsers (`js_parser.py`, `ts_parser.py`, `ecmascript_ui.py`)**:
   - Emit only generic language primitives (`IRAnnotation`, `IRCall.in_branch_or_loop`, `IRFunction.jsx_elements_count`, `IRFunction.dom_write_sinks`, `IRFunction.array_index_keys`, `IRModule.directives`, `IRModule.imports`).
   - Contain zero references to framework names or framework scoring thresholds.
3. **UI Framework Profiles (`profiles_ui.py`)**:
   - `ReactFrameworkProfile(FrameworkProfile)` (`name="react"`, `target_language="ecmascript"`) — implements `extra_concerns(func)` for `"render_ui"`, `requires_explicit_return_type(func)`, `evaluate_function`, and `UI_CONCERN_MAP`.
   - `NextJsFrameworkProfile(ReactFrameworkProfile)` (`name="nextjs"`, `target_language="ecmascript"`) — adds `evaluate_module(module)` emitting module-level `security` and `clean` penalties applied in `ModuleAnalyzer._score_ir_module` / `_blend_scores`.
   - `AngularFrameworkProfile(FrameworkProfile)` (`name="angular"`, `target_language="typescript"`) — implements `is_lcom4_exempt`, `requires_constructor_docstring`, `evaluate_class`, and `evaluate_function`.

---

## 2. Profile Resolver Contract (`scripts/_code_health/profiles.py`)

```python
def resolve_active_profiles(
    repo_root: Path,
    file_path: Path,
    lang_override: str | None = None,
    framework_override: str | None = None,
    imports: list[str] | None = None,
    has_jsx: bool = False,
) -> LanguageProfile:
    """Resolve active LanguageProfile and attached FrameworkProfiles for a target file."""
```

### Auto-Detection Precedence (`framework_override is None`)
- **If `framework_override == "none"`**: Returns raw `LanguageProfile` with `frameworks=[]`.
- **If `framework_override` is `"react"`, `"nextjs"`, or `"angular"`**: Attaches the requested `FrameworkProfile` directly (ignoring Angular if language is JavaScript? If explicitly forced on TS, attaches `ANGULAR_FRAMEWORK`).
- **Auto-detection (`framework_override is None`)**:
  - **TypeScript / JavaScript**:
    1. **Angular** (TypeScript only): `"@angular/core"` or `"@angular/"` in `imports`, OR (`"@angular/core"` in cached `package.json` deps AND file contains Angular signals/imports).
    2. **Next.js** (TS & JS): any import starting with `"next/"` or `"next"`, OR (`"next"` in cached `package.json` deps AND (file is under `app/` or `pages/` OR uses React/JSX/directive signals)).
    3. **React** (TS & JS): `"react"` or `"react-dom"` in `imports`, OR `has_jsx` is `True`, OR (`"react"` in cached `package.json` deps AND file imports/uses JSX or React hooks).
    4. Otherwise: `frameworks=[]` (pure TypeScript / pure JavaScript — prevents false positives on backend/utility files in monorepos).
