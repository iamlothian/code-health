"""Unit tests for Unified Intermediate Representation (IR) and Universal Scorer."""

from __future__ import annotations

import ast
from pathlib import Path
import sys

_SCRIPTS_DIR = str(Path(__file__).resolve().parents[2] / "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import pytest
from _code_health.ir_models import (
    IRAnnotation,
    IRCall,
    IRClass,
    IRExceptHandler,
    IRField,
    IRFunction,
    IRModule,
    IRParam,
    MissingNativeParserError,
    RulePenalty,
)
from _code_health.ir_scorer import UniversalIRScorer
from _code_health.models import RubricConfig
from _code_health.profiles import PYTHON_PROFILE, resolve_active_profiles


def test_ir_module_creation_and_attributes() -> None:
    func = IRFunction(
        name="do_work",
        qualname="Worker.do_work",
        lineno=10,
        end_lineno=25,
        loc=15,
        params=[IRParam("item", "str", False, [])],
        return_type="bool",
        max_nesting=1,
        cyclomatic_complexity=2,
        cognitive_complexity=1,
        returns_count=1,
        calls=[IRCall("print", "print", 12)],
        accessed_fields=["logger"],
        except_handlers=[],
        is_test=False,
    )
    cls = IRClass(
        name="Worker",
        qualname="Worker",
        lineno=5,
        end_lineno=30,
        loc=25,
        annotations=[],
        base_types=[],
        fields=[IRField("logger", "Logger", [], 6)],
        methods=[func],
        lcom4=1,
    )
    mod = IRModule(
        file_path="src/worker.py",
        language="python",
        is_test=False,
        loc=35,
        imports=["logging"],
        classes=[cls],
        functions=[],
        parser_backend="native",
    )
    assert mod.file_path == "src/worker.py"
    assert mod.classes[0].methods[0].name == "do_work"
    assert mod.classes[0].fields[0].name == "logger"


def test_missing_native_parser_error_formatting() -> None:
    err = MissingNativeParserError(
        language="java",
        missing_packages=["tree-sitter", "tree-sitter-java"],
    )
    msg = str(err)
    assert "tree-sitter-java" in msg
    assert "uv run --with tree-sitter" in msg
    assert "pip install" in msg


def test_universal_ir_scorer_scores_clean_ir_function_grade_a() -> None:
    func = IRFunction(
        name="add",
        qualname="add",
        lineno=1,
        end_lineno=5,
        loc=4,
        params=[IRParam("a", "int", False, []), IRParam("b", "int", False, [])],
        return_type="int",
        max_nesting=0,
        cyclomatic_complexity=1,
        cognitive_complexity=0,
        returns_count=1,
        calls=[],
        accessed_fields=[],
        except_handlers=[],
        is_test=False,
    )
    scorer = UniversalIRScorer(RubricConfig(), PYTHON_PROFILE)
    rep = scorer.score_function(func, "src/math.py", is_test=False)
    assert rep.scores.grade == "A"
    assert rep.scores.composite >= 95.0
    assert rep.findings == []


def test_python_ast_to_ir_adapter_matches_legacy_ast_engine() -> None:
    from _code_health.ast_engine import UnitScorer
    from _code_health.models import AnalysisContext
    from _code_health.profiles import python_ast_to_ir_module

    source = '''
def greet(name: str) -> str:
    """Return greeting."""
    if not name:
        return "Hello World"
    return f"Hello {name}"
'''
    tree = ast.parse(source)
    ctx = AnalysisContext(source.splitlines(), "src/greet.py", is_test=False, config=RubricConfig())
    legacy_scorer = UnitScorer(ctx)
    legacy_rep = legacy_scorer.analyze_function(tree.body[0])

    ir_mod = python_ast_to_ir_module(tree, source.splitlines(), "src/greet.py", is_test=False)
    assert len(ir_mod.functions) == 1
    ir_func = ir_mod.functions[0]
    assert ir_func.loc == legacy_rep.loc
    assert ir_func.cyclomatic_complexity == legacy_rep.cyclomatic_complexity
    assert ir_func.cognitive_complexity == legacy_rep.cognitive_complexity

    ir_scorer = UniversalIRScorer(RubricConfig(), PYTHON_PROFILE)
    ir_rep = ir_scorer.score_function(ir_func, "src/greet.py", is_test=False)
    assert ir_rep.scores.composite == legacy_rep.scores.composite
    assert ir_rep.scores.grade == legacy_rep.scores.grade


def test_ir_function_javascript_rule_fields_and_defaults() -> None:
    func = IRFunction(
        name="calculate",
        qualname="calculate",
        lineno=1,
        end_lineno=5,
        loc=4,
        params=[],
        return_type=None,
        max_nesting=1,
        cyclomatic_complexity=1,
        cognitive_complexity=0,
        returns_count=1,
        calls=[],
        accessed_fields=[],
        except_handlers=[],
        is_test=False,
    )
    # Check default values
    assert func.var_declarations_count == 0
    assert func.loose_comparisons_count == 0
    assert func.has_proto_mutation is False
    assert func.has_with_statement is False
    assert func.has_debugger_statement is False

    # Check customized values
    js_func = IRFunction(
        name="legacy",
        qualname="legacy",
        lineno=1,
        end_lineno=10,
        loc=8,
        params=[],
        return_type=None,
        max_nesting=1,
        cyclomatic_complexity=2,
        cognitive_complexity=1,
        returns_count=1,
        calls=[IRCall("setTimeout", "setTimeout", 5, has_string_arg=True)],
        accessed_fields=[],
        except_handlers=[],
        is_test=False,
        var_declarations_count=2,
        loose_comparisons_count=1,
        has_proto_mutation=True,
        has_with_statement=True,
        has_debugger_statement=True,
    )
    assert js_func.var_declarations_count == 2
    assert js_func.loose_comparisons_count == 1
    assert js_func.has_proto_mutation is True
    assert js_func.has_with_statement is True
    assert js_func.has_debugger_statement is True
    assert js_func.calls[0].has_string_arg is True


def test_ir_function_typescript_rule_fields_and_defaults() -> None:
    func = IRFunction(
        name="processData",
        qualname="processData",
        lineno=1,
        end_lineno=5,
        loc=4,
        params=[],
        return_type=None,
        max_nesting=1,
        cyclomatic_complexity=1,
        cognitive_complexity=0,
        returns_count=1,
        calls=[],
        accessed_fields=[],
        except_handlers=[],
        is_test=False,
    )
    # Check default values
    assert func.explicit_any_count == 0
    assert func.ts_ignore_count == 0
    assert func.non_null_assertion_count == 0

    # Check customized values
    ts_func = IRFunction(
        name="escapeHatch",
        qualname="escapeHatch",
        lineno=1,
        end_lineno=10,
        loc=8,
        params=[],
        return_type=None,
        max_nesting=1,
        cyclomatic_complexity=1,
        cognitive_complexity=0,
        returns_count=1,
        calls=[],
        accessed_fields=[],
        except_handlers=[],
        is_test=False,
        explicit_any_count=3,
        ts_ignore_count=1,
        non_null_assertion_count=2,
    )
    assert ts_func.explicit_any_count == 3
    assert ts_func.ts_ignore_count == 1
    assert ts_func.non_null_assertion_count == 2


def test_ir_ui_primitives_and_framework_hooks_defaults_and_delegation() -> None:
    from _code_health.ir_models import FrameworkProfile, LanguageProfile
    from _code_health.module_engine import ModuleAnalyzer

    call_default = IRCall("fetch", "fetch", 4)
    assert call_default.in_branch_or_loop is False
    call_branch = IRCall("useState", "useState", 5, in_branch_or_loop=True)
    assert call_branch.in_branch_or_loop is True

    func = IRFunction(
        name="UserCard",
        qualname="UserCard",
        lineno=1,
        end_lineno=8,
        loc=7,
        params=[IRParam("props", "Props", False, [])],
        return_type=None,
        max_nesting=0,
        cyclomatic_complexity=1,
        cognitive_complexity=0,
        returns_count=1,
        calls=[],
        accessed_fields=[],
        except_handlers=[],
        is_test=False,
    )
    assert func.jsx_elements_count == 0
    assert func.dom_write_sinks == []
    assert func.array_index_keys == []

    mod = IRModule(
        file_path="app/page.tsx",
        language="typescript",
        is_test=False,
        loc=10,
        imports=[],
        classes=[],
        functions=[],
    )
    assert mod.directives == []

    class _MockUIFramework(FrameworkProfile):
        def __init__(self) -> None:
            super().__init__(name="mock_ui", target_language="typescript")

        def evaluate_module(self, module: IRModule) -> list[RulePenalty]:
            return [RulePenalty("security", 30.0, "Security: mock module issue", 1)]

        def extra_concerns(self, fn: IRFunction) -> set[str]:
            return {"render_ui"} if fn.jsx_elements_count > 0 else set()

        def requires_explicit_return_type(self, fn: IRFunction) -> bool:
            return fn.jsx_elements_count == 0

        def requires_constructor_docstring(self, cls: IRClass | None) -> bool:
            return cls is None

        def is_lcom4_exempt(self, cls: IRClass) -> bool:
            return True

    base_fw = FrameworkProfile(name="base", target_language="typescript")
    assert base_fw.evaluate_module(mod) == []
    assert base_fw.extra_concerns(func) == set()
    assert base_fw.requires_explicit_return_type(func) is True
    assert base_fw.requires_constructor_docstring(None) is True
    assert base_fw.is_lcom4_exempt(IRClass("C", "C", 1, 5, 4, [], [], [], [])) is False

    fw = _MockUIFramework()
    profile = LanguageProfile("typescript", (".ts", ".tsx"), frameworks=[fw])
    jsx_fn = IRFunction(
        name="UserCard",
        qualname="UserCard",
        lineno=1,
        end_lineno=6,
        loc=5,
        params=[IRParam("props", "Props", False, [])],
        return_type=None,
        max_nesting=0,
        cyclomatic_complexity=1,
        cognitive_complexity=0,
        returns_count=1,
        calls=[],
        accessed_fields=[],
        except_handlers=[],
        is_test=False,
        jsx_elements_count=2,
    )
    scorer = UniversalIRScorer(RubricConfig(), profile)
    fn_rep = scorer.score_function(jsx_fn, "src/UserCard.tsx", is_test=False)
    assert "render_ui" in fn_rep.concerns
    assert not any("missing return type annotation" in f for f in fn_rep.findings)

    ctor = IRFunction(
        name="constructor",
        qualname="Widget.constructor",
        lineno=4,
        end_lineno=6,
        loc=2,
        params=[],
        return_type="void",
        max_nesting=0,
        cyclomatic_complexity=1,
        cognitive_complexity=0,
        returns_count=0,
        calls=[],
        accessed_fields=[],
        except_handlers=[],
        is_test=False,
        has_docstring=False,
    )
    cls = IRClass(
        name="Widget",
        qualname="Widget",
        lineno=1,
        end_lineno=20,
        loc=18,
        annotations=[],
        base_types=[],
        fields=[],
        methods=[ctor, jsx_fn, func],
        lcom4=3,
    )
    cls_rep = scorer.score_class(cls, "src/Widget.tsx", is_test=False)
    assert not any("LCOM4" in f for f in cls_rep.findings)
    assert not any("missing public docstring" in f for f in cls_rep.methods[0].findings)

    analyzer = ModuleAnalyzer(Path("."), set(), RubricConfig(), None)
    blended = analyzer._blend_scores((100.0, 100.0, 100.0, 70.0), [], [fn_rep])
    assert blended.security == 70.0


