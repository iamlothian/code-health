"""Language and framework profile definitions, registries, and AST converters."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from _code_health.ast_engine import (
    ControlFlowVisitor,
    _classify_except_handler,
    call_name,
    compute_lcom4,
    count_effective_loc,
)
from _code_health.ir_models import (
    FrameworkProfile,
    IRAnnotation,
    IRCall,
    IRClass,
    IRExceptHandler,
    IRField,
    IRFunction,
    IRModule,
    IRParam,
    LanguageProfile,
    RulePenalty,
)
from _code_health.profiles_java import JAVA_PROFILE, SPRING_BOOT_FRAMEWORK
from _code_health.profiles_js import JAVASCRIPT_PROFILE

PYTHON_PROFILE = LanguageProfile(name="python", file_extensions=(".py",))


def _extract_py_params(fn_node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[IRParam]:
    defaults = [None] * (len(fn_node.args.args) - len(fn_node.args.defaults)) + list(fn_node.args.defaults)
    params: list[IRParam] = []
    for arg, d in zip(fn_node.args.args, defaults):
        p_type = getattr(arg.annotation, "id", getattr(arg.annotation, "attr", None)) if arg.annotation else None
        params.append(IRParam(arg.arg, p_type, d is not None))
    return params


def _extract_py_handlers(fn_node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[IRExceptHandler]:
    handlers: list[IRExceptHandler] = []
    for h in (n for n in ast.walk(fn_node) if isinstance(n, ast.ExceptHandler)):
        pen, _ = _classify_except_handler(h)
        handlers.append(IRExceptHandler(getattr(h.type, "id", None), is_broad=(pen > 0), is_empty=(pen == 10.0), lineno=h.lineno))
    return handlers


def _python_func_to_ir(fn_node: ast.FunctionDef | ast.AsyncFunctionDef, lines: list[str], is_test: bool) -> IRFunction:
    cf = ControlFlowVisitor(is_test)
    cf.visit_block(fn_node.body, 0)
    calls = [IRCall(call_name(s), getattr(s, "lineno", fn_node.lineno)) for s in ast.walk(fn_node) if isinstance(s, ast.Call)]
    decs = [IRAnnotation(getattr(d, "attr", getattr(d, "id", ""))) for d in fn_node.decorator_list]
    ret_type = getattr(fn_node.returns, "id", getattr(fn_node.returns, "attr", None)) if fn_node.returns else None

    return IRFunction(
        name=fn_node.name,
        qualname=fn_node.name,
        lineno=fn_node.lineno,
        end_lineno=getattr(fn_node, "end_lineno", fn_node.lineno),
        loc=count_effective_loc(fn_node, lines),
        params=_extract_py_params(fn_node),
        return_type=ret_type,
        max_nesting=cf.max_nesting,
        cyclomatic_complexity=cf.cc,
        cognitive_complexity=cf.cog,
        returns_count=cf.returns,
        calls=calls,
        accessed_fields=[],
        except_handlers=_extract_py_handlers(fn_node),
        is_test=is_test,
        annotations=decs,
        has_docstring=ast.get_docstring(fn_node) is not None,
    )


def _convert_py_class(c_node: ast.ClassDef, lines: list[str], is_test: bool) -> IRClass:
    methods = [_python_func_to_ir(m, lines, is_test) for m in c_node.body if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))]
    for m in methods:
        m.qualname = f"{c_node.name}.{m.name}"
    lcom4, self_attrs = compute_lcom4(c_node)
    fields = [IRField(a) for a in self_attrs]
    decs = [IRAnnotation(getattr(d, "attr", getattr(d, "id", ""))) for d in c_node.decorator_list]
    bases = [getattr(b, "id", getattr(b, "attr", "")) for b in c_node.bases]
    return IRClass(
        c_node.name, c_node.name, c_node.lineno, getattr(c_node, "end_lineno", c_node.lineno),
        count_effective_loc(c_node, lines), decs, bases, fields, methods, lcom4, ast.get_docstring(c_node) is not None,
    )


def python_ast_to_ir_module(tree: ast.Module, lines: list[str], rel_path: str, is_test: bool) -> IRModule:
    """Convert a Python ast.Module into a normalized IRModule."""
    classes = [_convert_py_class(c, lines, is_test) for c in tree.body if isinstance(c, ast.ClassDef)]
    functions = [_python_func_to_ir(f, lines, is_test) for f in tree.body if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef))]
    return IRModule(
        file_path=rel_path,
        language="python",
        is_test=is_test,
        loc=count_effective_loc(tree, lines),
        imports=[],
        classes=classes,
        functions=functions,
        has_docstring=ast.get_docstring(tree) is not None,
    )


def _is_spring_source(path: Path) -> bool:
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
        return "org.springframework" in content or "@SpringBootApplication" in content
    except OSError:
        return False


def _has_spring_build_descriptor(root: Path) -> bool:
    for name in ("pom.xml", "build.gradle", "build.gradle.kts"):
        target = root / name
        if target.is_file():
            text = target.read_text(encoding="utf-8", errors="replace")
            if "spring-boot" in text or "org.springframework" in text:
                return True
    return False


def resolve_active_profiles(
    repo_root: Path, file_path: Path, lang_override: str | None = None, framework_override: str | None = None
) -> LanguageProfile:
    """Resolve active LanguageProfile and attached FrameworkProfiles for a given file."""
    ext = file_path.suffix.lower()
    if lang_override in {"javascript", "js"} or (lang_override is None and ext in {".js", ".mjs", ".cjs"}):
        return JAVASCRIPT_PROFILE
    lang = lang_override or ("java" if ext == ".java" else "python")
    if lang == "python":
        return PYTHON_PROFILE
    if framework_override == "none":
        return LanguageProfile(name="java", file_extensions=(".java",), frameworks=[])
    if framework_override == "spring-boot":
        return JAVA_PROFILE

    is_spring = _is_spring_source(file_path) or _has_spring_build_descriptor(repo_root)
    frameworks = [SPRING_BOOT_FRAMEWORK] if is_spring else []
    return LanguageProfile(name="java", file_extensions=(".java",), frameworks=frameworks)
