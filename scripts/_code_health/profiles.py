"""Language and framework profile definitions, registries, and AST converters."""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from _code_health.ast_engine import (
    ControlFlowVisitor,
    _classify_except_handler,
    call_name,
    compute_lcom4,
    count_effective_loc,
    has_exempt_base,
)
from _code_health.ir_models import (
    IRAnnotation,
    IRCall,
    IRClass,
    IRExceptHandler,
    IRField,
    IRFunction,
    IRModule,
    IRParam,
    RulePenalty,
)
from _code_health.models import (
    CONCERN_EXACT_MAP,
    CONCERN_SHORT_MAP,
    ENTRYPOINT_DECORATORS,
    AnalysisContext,
    RubricConfig,
)


@dataclass
class LanguageProfile:
    """Configuration and rule hooks for a target programming language."""

    name: str
    file_extensions: tuple[str, ...]
    frameworks: list[FrameworkProfile] = field(default_factory=list)

    def evaluate_function(self, func: IRFunction, parent: IRClass | None) -> list[RulePenalty]:
        penalties: list[RulePenalty] = []
        for fw in self.frameworks:
            penalties.extend(fw.evaluate_function(func, parent))
        return penalties

    def evaluate_class(self, cls: IRClass) -> list[RulePenalty]:
        penalties: list[RulePenalty] = []
        for fw in self.frameworks:
            penalties.extend(fw.evaluate_class(cls))
        return penalties

    def map_concern(self, cname: str) -> str | None:
        for fw in self.frameworks:
            c = fw.concern_map.get(cname) or fw.concern_map.get(cname.split(".")[-1])
            if c:
                return c
        return CONCERN_EXACT_MAP.get(cname) or CONCERN_SHORT_MAP.get(cname.split(".")[-1])

    def is_entrypoint_func(self, func: IRFunction) -> bool:
        names = {a.name.split(".")[-1] for a in func.annotations}
        fw_entrypoints = {ep for fw in self.frameworks for ep in fw.entrypoint_annotations}
        return bool(names & (ENTRYPOINT_DECORATORS | fw_entrypoints))

    def is_test_assert_call(self, cname: str) -> bool:
        for fw in self.frameworks:
            if fw.is_test_assert_call(cname):
                return True
        return cname in {"pytest.raises", "pytest.warns", "pytest.fail"} or cname.split(".")[-1].startswith("assert")


@dataclass
class FrameworkProfile:
    """Layered architectural rules and concern mappings for a specific framework."""

    name: str
    target_language: str
    concern_map: dict[str, str] = field(default_factory=dict)
    entrypoint_annotations: set[str] = field(default_factory=set)
    lcom4_exempt_annotations: set[str] = field(default_factory=set)

    def evaluate_function(self, func: IRFunction, parent: IRClass | None) -> list[RulePenalty]:
        return []

    def evaluate_class(self, cls: IRClass) -> list[RulePenalty]:
        return []

    def is_test_assert_call(self, call_name: str) -> bool:
        return False


PYTHON_PROFILE = LanguageProfile(name="python", file_extensions=(".py",))


def _python_func_to_ir(fn_node: ast.FunctionDef | ast.AsyncFunctionDef, lines: list[str], is_test: bool) -> IRFunction:
    cf = ControlFlowVisitor(is_test)
    cf.visit_block(fn_node.body, 0)
    loc = count_effective_loc(fn_node, lines)

    params: list[IRParam] = []
    defaults = [None] * (len(fn_node.args.args) - len(fn_node.args.defaults)) + list(fn_node.args.defaults)
    for arg, d in zip(fn_node.args.args, defaults):
        p_type = getattr(arg.annotation, "id", getattr(arg.annotation, "attr", None)) if arg.annotation else None
        params.append(IRParam(arg.arg, p_type, d is not None))

    calls: list[IRCall] = []
    for s in ast.walk(fn_node):
        if isinstance(s, ast.Call):
            calls.append(IRCall(call_name(s), getattr(s, "lineno", fn_node.lineno)))

    handlers: list[IRExceptHandler] = []
    for h in (n for n in ast.walk(fn_node) if isinstance(n, ast.ExceptHandler)):
        pen, msg = _classify_except_handler(h)
        handlers.append(IRExceptHandler(getattr(h.type, "id", None), is_broad=(pen > 0), is_empty=(pen == 10.0), lineno=h.lineno))

    decs = [IRAnnotation(getattr(d, "attr", getattr(d, "id", ""))) for d in fn_node.decorator_list]
    ret_type = getattr(fn_node.returns, "id", getattr(fn_node.returns, "attr", None)) if fn_node.returns else None
    has_doc = ast.get_docstring(fn_node) is not None

    return IRFunction(
        name=fn_node.name,
        qualname=fn_node.name,
        lineno=fn_node.lineno,
        end_lineno=getattr(fn_node, "end_lineno", fn_node.lineno),
        loc=loc,
        params=params,
        return_type=ret_type,
        max_nesting=cf.max_nesting,
        cyclomatic_complexity=cf.cc,
        cognitive_complexity=cf.cog,
        returns_count=cf.returns,
        calls=calls,
        accessed_fields=[],
        except_handlers=handlers,
        is_test=is_test,
        annotations=decs,
        has_docstring=has_doc,
    )


def python_ast_to_ir_module(tree: ast.Module, lines: list[str], rel_path: str, is_test: bool) -> IRModule:
    """Convert a Python ast.Module into a normalized IRModule."""
    classes: list[IRClass] = []
    for c_node in (n for n in tree.body if isinstance(n, ast.ClassDef)):
        methods = [_python_func_to_ir(m, lines, is_test) for m in c_node.body if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))]
        for m in methods:
            m.qualname = f"{c_node.name}.{m.name}"
        lcom4, self_attrs = compute_lcom4(c_node)
        loc = count_effective_loc(c_node, lines)
        fields = [IRField(a) for a in self_attrs]
        decs = [IRAnnotation(getattr(d, "attr", getattr(d, "id", ""))) for d in c_node.decorator_list]
        bases = [getattr(b, "id", getattr(b, "attr", "")) for b in c_node.bases]
        classes.append(
            IRClass(c_node.name, c_node.name, c_node.lineno, getattr(c_node, "end_lineno", c_node.lineno), loc, decs, bases, fields, methods, lcom4, ast.get_docstring(c_node) is not None)
        )

    functions = [_python_func_to_ir(f, lines, is_test) for f in tree.body if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef))]
    loc = count_effective_loc(tree, lines)
    return IRModule(
        file_path=rel_path,
        language="python",
        is_test=is_test,
        loc=loc,
        imports=[],
        classes=classes,
        functions=functions,
        has_docstring=ast.get_docstring(tree) is not None,
    )


def resolve_active_profiles(
    repo_root: Path, file_path: Path, lang_override: str | None = None, framework_override: str | None = None
) -> LanguageProfile:
    """Resolve active LanguageProfile and attached FrameworkProfiles for a given file."""
    ext = file_path.suffix.lower()
    lang = lang_override or ("java" if ext == ".java" else "python")
    if lang == "python":
        return PYTHON_PROFILE
    from _code_health.profiles_java import JAVA_PROFILE, SPRING_BOOT_FRAMEWORK
    if framework_override == "none":
        return LanguageProfile(name="java", file_extensions=(".java",), frameworks=[])
    return JAVA_PROFILE
