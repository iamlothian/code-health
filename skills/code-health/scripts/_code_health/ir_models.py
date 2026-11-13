"""Language-neutral Intermediate Representation (IR) data models for Code Health Analyzer."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from _code_health.models import CONCERN_EXACT_MAP, CONCERN_SHORT_MAP, ENTRYPOINT_DECORATORS


@dataclass(frozen=True)
class RulePenalty:
    """Individual rule violation penalty applied to a dimension."""

    dimension: str
    penalty_points: float
    finding: str
    lineno: int = 1


@dataclass(frozen=True)
class IRAnnotation:
    """Annotation or decorator declaration attached to a class, function, or field."""

    name: str
    args: dict[str, Any] = field(default_factory=dict)
    lineno: int = 1


@dataclass(frozen=True)
class IRParam:
    """Function or method parameter representation."""

    name: str
    type_annotation: str | None = None
    has_default: bool = False
    annotations: list[IRAnnotation] = field(default_factory=list)


@dataclass(frozen=True)
class IRField:
    """Class field or attribute declaration."""

    name: str
    type_annotation: str | None = None
    annotations: list[IRAnnotation] = field(default_factory=list)
    lineno: int = 1


@dataclass(frozen=True)
class IRCall:
    """Function or method call expression."""

    name: str
    callee_symbol: str = ""
    lineno: int = 1
    has_string_concat: bool = False
    has_string_arg: bool = False
    in_branch_or_loop: bool = False


@dataclass(frozen=True)
class IRExceptHandler:
    """Catch block or exception handler representation."""

    exception_type: str | None = None
    is_empty: bool = False
    is_broad: bool = False
    lineno: int = 1


@dataclass
class IRFunction:
    """Language-neutral representation of a function or method."""

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

    # Generic UI / JSX / DOM syntax telemetry (backward-compatible defaults)
    jsx_elements_count: int = 0
    dom_write_sinks: list[tuple[str, int]] = field(default_factory=list)
    array_index_keys: list[int] = field(default_factory=list)


@dataclass
class IRClass:
    """Language-neutral representation of a class, record, or interface."""

    name: str
    qualname: str
    lineno: int
    end_lineno: int
    loc: int
    annotations: list[IRAnnotation]
    base_types: list[str]
    fields: list[IRField]
    methods: list[IRFunction]
    lcom4: int = 1
    has_docstring: bool = True


@dataclass
class IRModule:
    """Language-neutral representation of a source or test file."""

    file_path: str
    language: str
    is_test: bool
    loc: int
    imports: list[str]
    classes: list[IRClass]
    functions: list[IRFunction]
    parser_backend: str = "native"
    has_docstring: bool = True
    duplicate_blocks: int = 0
    mid_file_imports: int = 0
    ts_ignore_count: int = 0
    syntax_errors: list[int] = field(default_factory=list)
    directives: list[str] = field(default_factory=list)


class MissingNativeParserError(RuntimeError):
    """Raised when native grammar wheels (e.g. tree-sitter-java) are missing."""

    def __init__(self, language: str, missing_packages: list[str]) -> None:
        self.language = language
        self.missing_packages = missing_packages
        self.install_commands = {
            "uv_ephemeral": f"uv run --with {missing_packages[0]} --with {missing_packages[-1]} python scripts/code_health.py",
            "uv_project": f"uv pip install '{missing_packages[0]}>=0.23.0' '{missing_packages[-1]}>=0.23.0'",
            "pip": f"pip install 'py-code-health[{language}]'",
        }
        pkgs_str = " ".join(missing_packages)
        super().__init__(
            f"[WARNING] Native {language.title()} AST parser ('{missing_packages[-1]}') is not installed.\n"
            f"To analyze {language.title()} files, install the native parser dependencies:\n"
            f"  • uv (ephemeral): uv run --with {missing_packages[0]} --with {missing_packages[-1]} python scripts/code_health.py <paths>\n"
            f"  • uv (project):   uv pip install 'tree-sitter>=0.23.0' '{missing_packages[-1]}>=0.23.0'\n"
            f"  • pip:            pip install {pkgs_str}\n"
        )


@dataclass
class FrameworkProfile:
    """Layered architectural rules and concern mappings for a specific framework."""

    name: str
    target_language: str
    concern_map: dict[str, str] = field(default_factory=dict)
    entrypoint_annotations: set[str] = field(default_factory=set)
    lcom4_exempt_annotations: set[str] = field(default_factory=set)

    def evaluate_module(self, module: IRModule) -> list[RulePenalty]:
        """Evaluate architectural or boundary rules for a module."""
        return []

    def evaluate_function(self, func: IRFunction, parent: IRClass | None) -> list[RulePenalty]:
        """Evaluate architectural rule violations for a function or method."""
        return []

    def evaluate_class(self, cls: IRClass) -> list[RulePenalty]:
        """Evaluate architectural rule violations for a class or record."""
        return []

    def extra_concerns(self, func: IRFunction) -> set[str]:
        """Return framework-specific operational concerns derived from generic IR telemetry."""
        return set()

    def requires_explicit_return_type(self, func: IRFunction) -> bool:
        """Return False to exempt qualifying functions (e.g. JSX components) from missing-return-type checks."""
        return True

    def requires_constructor_docstring(self, cls: IRClass | None) -> bool:
        """Return False to exempt DI/framework constructors from missing-docstring penalties."""
        return True

    def is_lcom4_exempt(self, cls: IRClass) -> bool:
        """Return True when a class is exempt from LCOM4 cohesion split penalties."""
        ann_names = {a.name.split(".")[-1] for a in cls.annotations}
        return bool(ann_names & self.lcom4_exempt_annotations)

    def is_test_assert_call(self, call_name: str) -> bool:
        """Determine if a function/method call represents an assertion."""
        return False


@dataclass
class LanguageProfile:
    """Configuration and rule hooks for a target programming language."""

    name: str
    file_extensions: tuple[str, ...]
    frameworks: list[FrameworkProfile] = field(default_factory=list)

    def evaluate_module(self, module: IRModule) -> list[RulePenalty]:
        """Evaluate framework penalties across the entire module."""
        penalties: list[RulePenalty] = []
        for fw in self.frameworks:
            penalties.extend(fw.evaluate_module(module))
        return penalties

    def evaluate_function(self, func: IRFunction, parent: IRClass | None) -> list[RulePenalty]:
        """Evaluate framework and language penalties on a function or method."""
        penalties: list[RulePenalty] = []
        for fw in self.frameworks:
            penalties.extend(fw.evaluate_function(func, parent))
        return penalties

    def evaluate_class(self, cls: IRClass) -> list[RulePenalty]:
        """Evaluate framework and language penalties on a class or record."""
        penalties: list[RulePenalty] = []
        for fw in self.frameworks:
            penalties.extend(fw.evaluate_class(cls))
        return penalties

    def extra_concerns(self, func: IRFunction) -> set[str]:
        """Collect non-call operational concerns contributed by attached frameworks."""
        concerns: set[str] = set()
        for fw in self.frameworks:
            concerns.update(fw.extra_concerns(func))
        return concerns

    def requires_explicit_return_type(self, func: IRFunction) -> bool:
        """Return True unless an active framework exempts this function's return annotation."""
        return all(fw.requires_explicit_return_type(func) for fw in self.frameworks)

    def requires_constructor_docstring(self, cls: IRClass | None) -> bool:
        """Return True unless an active framework exempts constructors on cls from docstrings."""
        return all(fw.requires_constructor_docstring(cls) for fw in self.frameworks)

    def is_lcom4_exempt(self, cls: IRClass) -> bool:
        """Return True if any active framework exempts cls from LCOM4 penalties."""
        return any(fw.is_lcom4_exempt(cls) for fw in self.frameworks)

    def map_concern(self, cname: str) -> str | None:
        """Map a function/call name to an operational concern category."""
        for fw in self.frameworks:
            c = fw.concern_map.get(cname) or fw.concern_map.get(cname.split(".")[-1])
            if c:
                return c
        return CONCERN_EXACT_MAP.get(cname) or CONCERN_SHORT_MAP.get(cname.split(".")[-1])

    def is_entrypoint_func(self, func: IRFunction) -> bool:
        """Check if function is an entrypoint (web, CLI, scheduled job)."""
        names = {a.name.split(".")[-1] for a in func.annotations}
        fw_entrypoints = {ep for fw in self.frameworks for ep in fw.entrypoint_annotations}
        return bool(names & (ENTRYPOINT_DECORATORS | fw_entrypoints))

    def is_test_assert_call(self, cname: str) -> bool:
        """Determine if a call name matches a test assertion idiom."""
        for fw in self.frameworks:
            if fw.is_test_assert_call(cname):
                return True
        return cname in {"pytest.raises", "pytest.warns", "pytest.fail"} or cname.split(".")[-1].startswith("assert")
