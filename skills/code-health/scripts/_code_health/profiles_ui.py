"""Web UI framework code health profiles (React, Next.js, Angular)."""

from __future__ import annotations

from pathlib import Path

from _code_health.ir_models import FrameworkProfile, IRClass, IRFunction, IRModule, RulePenalty

UI_CONCERN_MAP: dict[str, str] = {
    "fetch": "network_io",
    "window.fetch": "network_io",
    "axios": "network_io",
    "axios.get": "network_io",
    "axios.post": "network_io",
    "axios.put": "network_io",
    "axios.delete": "network_io",
    "HttpClient": "network_io",
    "localStorage.getItem": "storage_io",
    "localStorage.setItem": "storage_io",
    "localStorage.removeItem": "storage_io",
    "sessionStorage.getItem": "storage_io",
    "sessionStorage.setItem": "storage_io",
    "document.getElementById": "dom_mutation",
    "document.querySelector": "dom_mutation",
    "document.querySelectorAll": "dom_mutation",
    "document.createElement": "dom_mutation",
    "window.open": "dom_mutation",
    "console.log": "presentation",
    "console.warn": "presentation",
    "console.error": "presentation",
    "console.info": "presentation",
}

_ANGULAR_SANITIZER_BYPASSES = frozenset({
    "bypassSecurityTrustHtml",
    "bypassSecurityTrustScript",
    "bypassSecurityTrustUrl",
    "bypassSecurityTrustResourceUrl",
})
_ANGULAR_LCOM4_EXEMPT = frozenset({"Component", "Directive", "Pipe", "NgModule"})
_ANGULAR_DI_ANNOTATIONS = frozenset({"Component", "Directive", "Injectable", "Pipe", "NgModule"})
_ANGULAR_UI_ANNOTATIONS = frozenset({"Component", "Directive"})
_ANGULAR_TEARDOWN_CALLS = frozenset({"takeUntilDestroyed", "takeUntil"})
_SERVER_ONLY_IMPORTS = frozenset({"fs", "child_process", "server-only", "next/headers"})
_SERVER_IMPORT_PREFIXES = ("node:", "fs/", "next/headers/")
_NEXT_CLIENT_HOOKS = frozenset({"useState", "useEffect", "useReducer", "useRef", "useContext"})


def _is_hook_identifier(name: str) -> bool:
    short = name.split(".")[-1]
    return short.startswith("use") and len(short) > 3 and short[3].isupper()


def _is_custom_hook_func(func: IRFunction) -> bool:
    return _is_hook_identifier(func.name) and func.jsx_elements_count == 0


def _is_custom_hook_module(file_path: str) -> bool:
    return _is_hook_identifier(Path(file_path).stem)


def _eval_react_hooks(func: IRFunction) -> list[RulePenalty]:
    penalties: list[RulePenalty] = []
    applied = 0.0
    for call in func.calls:
        if call.in_branch_or_loop and _is_hook_identifier(call.name) and applied < 50.0:
            pts = min(25.0, 50.0 - applied)
            applied += pts
            penalties.append(
                RulePenalty(
                    "clean",
                    pts,
                    f"Clean (React): Rules of Hooks violation calling '{call.name}' in branch/loop at L{call.lineno} (-{pts:.1f} pts)",
                    call.lineno,
                )
            )
    return penalties


def _eval_react_sprawl(func: IRFunction) -> list[RulePenalty]:
    if _is_custom_hook_func(func):
        return []
    shorts = [c.name.split(".")[-1] for c in func.calls]
    eff_cnt = sum(s in {"useEffect", "useLayoutEffect"} for s in shorts)
    state_cnt = sum(s == "useState" for s in shorts)
    penalties: list[RulePenalty] = []
    if eff_cnt > 2:
        pts = min(24.0, (eff_cnt - 2) * 8.0)
        penalties.append(RulePenalty("srp", pts, f"SRP (React): effect sprawl with {eff_cnt} useEffect/useLayoutEffect calls (>2) (-{pts:.1f} pts)", func.lineno))
    if state_cnt > 5:
        pts = min(20.0, (state_cnt - 5) * 5.0)
        penalties.append(RulePenalty("srp", pts, f"SRP (React): state sprawl with {state_cnt} useState calls (>5) (-{pts:.1f} pts)", func.lineno))
    return penalties


def _eval_react_index_keys(func: IRFunction) -> list[RulePenalty]:
    if not func.array_index_keys:
        return []
    pts = min(24.0, len(func.array_index_keys) * 8.0)
    line = func.array_index_keys[0]
    return [RulePenalty("clean", pts, f"Clean (React): array index used as JSX key at L{line} (-{pts:.1f} pts)", line)]


def _eval_xss_sink_list(sinks: list[tuple[str, int]], label: str) -> list[RulePenalty]:
    """Build capped Security penalties for browser/framework DOM XSS sinks."""
    if not sinks:
        return []
    penalties: list[RulePenalty] = []
    applied = 0.0
    for sink_name, line in sinks:
        if applied >= 70.0:
            break
        pts = min(35.0, 70.0 - applied)
        applied += pts
        penalties.append(
            RulePenalty(
                "security",
                pts,
                f"Security ({label}): unsafe XSS/DOM sink '{sink_name}' at L{line} (-{pts:.1f} pts)",
                line,
            )
        )
    return penalties


class ReactFrameworkProfile(FrameworkProfile):
    """Code health rules and UI concerns for React TS/JS components and hooks."""

    def __init__(self, name: str = "react") -> None:
        super().__init__(name=name, target_language="ecmascript", concern_map=UI_CONCERN_MAP)

    def extra_concerns(self, func: IRFunction) -> set[str]:
        """Contribute 'render_ui' concern when a function returns or constructs JSX."""
        return {"render_ui"} if func.jsx_elements_count > 0 else set()

    def requires_explicit_return_type(self, func: IRFunction) -> bool:
        """Exempt PascalCase JSX-returning UI components from missing return type penalties."""
        is_component = bool(func.name) and func.name[0].isupper() and func.jsx_elements_count > 0
        return not (is_component and not _is_custom_hook_func(func))

    def evaluate_function(self, func: IRFunction, parent: IRClass | None) -> list[RulePenalty]:
        """Evaluate React security, hook hygiene, and rendering rules on a function."""
        if func.is_test:
            return []
        label = self.name.title()
        return (
            _eval_xss_sink_list(func.dom_write_sinks, label)
            + _eval_react_hooks(func)
            + _eval_react_sprawl(func)
            + _eval_react_index_keys(func)
        )


class NextJsFrameworkProfile(ReactFrameworkProfile):
    """Code health rules for Next.js App Router and Pages Router modules."""

    def __init__(self) -> None:
        super().__init__(name="nextjs")

    def evaluate_module(self, module: IRModule) -> list[RulePenalty]:
        """Enforce App Router 'use client' boundaries and block server imports in client modules."""
        if module.is_test:
            return []
        penalties: list[RulePenalty] = []
        has_use_client = "use client" in module.directives
        if has_use_client:
            bad_imps = [i for i in module.imports if i in _SERVER_ONLY_IMPORTS or i.startswith(_SERVER_IMPORT_PREFIXES)]
            if bad_imps:
                penalties.append(RulePenalty("security", 30.0, f"Security (Next.js): server-only import '{bad_imps[0]}' inside 'use client' module (-30.0 pts)", 1))
        parts = module.file_path.replace("\\", "/").split("/")
        if "app" in parts and "pages" not in parts and not has_use_client and not _is_custom_hook_module(module.file_path):
            all_funcs = list(module.functions) + [m for c in module.classes for m in c.methods]
            if any(c.name.split(".")[-1] in _NEXT_CLIENT_HOOKS for fn in all_funcs for c in fn.calls):
                penalties.append(RulePenalty("clean", 15.0, "Clean (Next.js): App Router module uses client hooks without 'use client' directive (-15.0 pts)", 1))
        return penalties


def _annotation_names(cls: IRClass) -> set[str]:
    return {ann.name for ann in cls.annotations}


def _injects_type(cls: IRClass, type_token: str) -> bool:
    if any(f.type_annotation and type_token in f.type_annotation for f in cls.fields):
        return True
    return any(
        p.type_annotation and type_token in p.type_annotation
        for m in cls.methods
        if m.name == "constructor"
        for p in m.params
    )


def _has_subscription_teardown(cls: IRClass) -> bool:
    if _injects_type(cls, "DestroyRef"):
        return True
    calls = [c.name.split(".")[-1] for m in cls.methods for c in m.calls]
    if any(name in _ANGULAR_TEARDOWN_CALLS for name in calls):
        return True
    has_destroy = any(m.name == "ngOnDestroy" for m in cls.methods)
    return has_destroy and "unsubscribe" in calls


def _first_unmanaged_subscribe(cls: IRClass) -> int | None:
    sub_line = next(
        (c.lineno for m in cls.methods for c in m.calls if c.name.split(".")[-1] == "subscribe"),
        None,
    )
    if sub_line is None or _has_subscription_teardown(cls):
        return None
    return sub_line


class AngularFrameworkProfile(FrameworkProfile):
    """Code health rules for Angular TypeScript components, directives, and services."""

    def __init__(self) -> None:
        super().__init__(
            name="angular",
            target_language="typescript",
            concern_map=UI_CONCERN_MAP,
            entrypoint_annotations={"HostListener"},
            lcom4_exempt_annotations=set(_ANGULAR_LCOM4_EXEMPT),
        )

    def requires_constructor_docstring(self, cls: IRClass | None) -> bool:
        """Exempt Angular DI constructors in decorated components and services from docstring penalties."""
        return not (cls is not None and bool(_annotation_names(cls) & _ANGULAR_DI_ANNOTATIONS))

    def evaluate_class(self, cls: IRClass) -> list[RulePenalty]:
        """Enforce Angular component HttpClient layering and RxJS subscription lifecycle rules."""
        if not (_annotation_names(cls) & _ANGULAR_UI_ANNOTATIONS):
            return []
        penalties: list[RulePenalty] = []
        if _injects_type(cls, "HttpClient"):
            penalties.append(
                RulePenalty(
                    "srp",
                    20.0,
                    "SRP (Angular): @Component/@Directive injects HttpClient directly instead of a service (-20.0 pts)",
                    cls.lineno,
                )
            )
        sub_line = _first_unmanaged_subscribe(cls)
        if sub_line is not None:
            penalties.append(
                RulePenalty(
                    "clean",
                    15.0,
                    f"Clean (Angular): unmanaged .subscribe() at L{sub_line} without takeUntilDestroyed/takeUntil/DestroyRef/ngOnDestroy (-15.0 pts)",
                    sub_line,
                )
            )
        return penalties

    def evaluate_function(self, func: IRFunction, parent: IRClass | None) -> list[RulePenalty]:
        """Evaluate Angular sanitizer bypasses and DOM XSS sinks."""
        if func.is_test:
            return []
        bypass_sinks = [
            (c.name.split(".")[-1], c.lineno)
            for c in func.calls
            if c.name.split(".")[-1] in _ANGULAR_SANITIZER_BYPASSES
        ]
        return _eval_xss_sink_list(list(func.dom_write_sinks) + bypass_sinks, "Angular")


REACT_FRAMEWORK = ReactFrameworkProfile()
NEXTJS_FRAMEWORK = NextJsFrameworkProfile()
ANGULAR_FRAMEWORK = AngularFrameworkProfile()
