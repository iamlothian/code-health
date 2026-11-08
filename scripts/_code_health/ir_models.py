"""Language-neutral Intermediate Representation (IR) data models for Code Health Analyzer."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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
