"""Unit tests for Vanilla JavaScript (ECMAScript) code health analyzer."""

from __future__ import annotations

from pathlib import Path
import sys
import tempfile

_SCRIPTS_DIR = str(Path(__file__).resolve().parents[2] / "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import pytest
from _code_health.models import RubricConfig
from _code_health.module_engine import is_test_file_path


def test_is_test_file_path_recognizes_javascript_conventions() -> None:
    # Test files
    assert is_test_file_path("src/components/button.test.js") is True
    assert is_test_file_path("src/services/api.spec.js") is True
    assert is_test_file_path("tests/unit/calculator_test.js") is True
    assert is_test_file_path("src/__tests__/utils.js") is True
    assert is_test_file_path("test/integration.mjs") is True

    # Source files
    assert is_test_file_path("src/components/button.js") is False
    assert is_test_file_path("src/services/api.mjs") is False
    assert is_test_file_path("lib/tools/runner.cjs") is False


def test_javascript_file_discovery_and_minified_skipping() -> None:
    from _code_health.reporting import CodeHealthRunner

    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        src_dir = root / "src"
        src_dir.mkdir(parents=True)
        (src_dir / "index.js").write_text("console.log('main');\n", encoding="utf-8")
        (src_dir / "module.mjs").write_text("export const x = 1;\n", encoding="utf-8")
        (src_dir / "config.cjs").write_text("module.exports = {};\n", encoding="utf-8")

        # Vendor and ignored directories
        vendor = root / "node_modules" / "pkg"
        vendor.mkdir(parents=True)
        (vendor / "vendor.js").write_text("var vendor = true;\n", encoding="utf-8")

        dist = root / "dist"
        dist.mkdir(parents=True)
        (dist / "bundle.js").write_text("var bundle = true;\n", encoding="utf-8")

        # Minified files
        (src_dir / "app.min.js").write_text("var minified = 1;\n", encoding="utf-8")
        (src_dir / "huge_line.js").write_text("var a = 1; " + "//" + "x" * 1200 + "\n", encoding="utf-8")

        runner = CodeHealthRunner(repo_root=root, git_mode="no-git")
        discovered = runner._discover_files([root])
        discovered_rel = [p.relative_to(root).as_posix() for p in discovered]

        # Valid source files discovered
        assert "src/index.js" in discovered_rel
        assert "src/module.mjs" in discovered_rel
        assert "src/config.cjs" in discovered_rel

        # Ignored and minified files skipped
        assert "node_modules/pkg/vendor.js" not in discovered_rel
        assert "dist/bundle.js" not in discovered_rel
        assert "src/app.min.js" not in discovered_rel
        assert "src/huge_line.js" not in discovered_rel


def test_tree_sitter_js_parser_parses_clean_es6_classes_and_functions() -> None:
    from _code_health.js_parser import parse_javascript_file

    code = """
    class Calculator {
        constructor() {
            this.total = 0;
        }

        add(value = 0) {
            this.total += value;
            return this.total;
        }
    }

    function calculateDiscount(price = 100, rate = 0.1) {
        if (price <= 0) {
            return 0;
        }
        return price * (1 - rate);
    }

    const multiply = (a = 1, b = 1) => a * b;

    const api = {
        fetchData(endpoint = "/api") {
            return endpoint;
        }
    };
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        js_file = Path(tmp_dir) / "service.js"
        js_file.write_text(code, encoding="utf-8")

        mod = parse_javascript_file(js_file, "src/service.js", is_test=False)
        assert mod.language == "javascript"
        assert mod.file_path == "src/service.js"
        assert mod.loc > 0

        # Classes
        assert len(mod.classes) == 1
        cls = mod.classes[0]
        assert cls.name == "Calculator"
        assert cls.qualname == "Calculator"
        assert "total" in [f.name for f in cls.fields]
        method_names = [m.name for m in cls.methods]
        assert "constructor" in method_names
        assert "add" in method_names
        add_method = next(m for m in cls.methods if m.name == "add")
        assert add_method.qualname == "Calculator.add"
        assert add_method.params[0].name == "value"
        assert add_method.params[0].has_default is True

        # Functions
        func_qualnames = [f.qualname for f in mod.functions]
        assert "calculateDiscount" in func_qualnames
        assert "multiply" in func_qualnames
        assert "api.fetchData" in func_qualnames

        calc_func = next(f for f in mod.functions if f.name == "calculateDiscount")
        assert len(calc_func.params) == 2
        assert calc_func.params[0].has_default is True
        assert calc_func.params[1].has_default is True
        assert calc_func.cyclomatic_complexity >= 2  # if branch


def test_tree_sitter_js_parser_absorbs_inline_callbacks_into_parent() -> None:
    from _code_health.js_parser import parse_javascript_file

    code = """
    function transformList(items = []) {
        return items
            .map(x => x * 2)
            .filter(x => x > 10)
            .reduce((acc, curr) => acc + curr, 0);
    }
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        js_file = Path(tmp_dir) / "transform.js"
        js_file.write_text(code, encoding="utf-8")

        mod = parse_javascript_file(js_file, "src/transform.js", is_test=False)
        # Should only have transformList, NOT 3 separate anonymous functions
        assert len(mod.functions) == 1
        fn = mod.functions[0]
        assert fn.name == "transformList"
        assert fn.loc >= 5

def test_cli_lang_javascript_flag_and_multilang_scan(capsys: pytest.CaptureFixture[str]) -> None:
    import json
    import code_health

    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        js_file = root / "math.js"
        js_file.write_text("export function add(a = 1, b = 2) { return a + b; }\n", encoding="utf-8")
        py_file = root / "service.py"
        py_file.write_text("def run() -> int:\n    return 42\n", encoding="utf-8")

        # Test --lang javascript
        ret = code_health.main([str(js_file), "--lang", "javascript", "--no-git"])
        assert ret == 0
        captured = capsys.readouterr()
        assert "CODE HEALTH SCORECARD" in captured.out
        assert "math.js" in captured.out

        # Test --lang js with --format json
        ret_json = code_health.main([str(js_file), "--lang", "js", "--format", "json", "--no-git"])
        assert ret_json == 0
        captured_json = capsys.readouterr()
        data = json.loads(captured_json.out)
        assert data["files_count"] == 1
        assert data["files"][0]["file_path"].endswith("math.js")

        # Test multi-language directory scan
        ret_dir = code_health.main([str(root), "--format", "json", "--no-git"])
        assert ret_dir == 0
        captured_dir = capsys.readouterr()
        dir_data = json.loads(captured_dir.out)
        assert dir_data["files_count"] == 2
        file_paths = [f["file_path"] for f in dir_data["files"]]
        assert any(p.endswith("math.js") for p in file_paths)
        assert any(p.endswith("service.py") for p in file_paths)


def test_missing_native_javascript_parser_exits_code_2_console(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    from typing import Any
    import code_health
    from _code_health.ir_models import MissingNativeParserError
    import _code_health.js_parser

    def mock_check() -> tuple[Any, Any]:
        raise MissingNativeParserError("javascript", ["tree-sitter", "tree-sitter-javascript"])

    monkeypatch.setattr(_code_health.js_parser, "check_javascript_dependencies", mock_check)

    js_file = tmp_path / "app.js"
    js_file.write_text("console.log('hi');\n", encoding="utf-8")

    rc = code_health.main([str(js_file), "--no-git"])
    assert rc == 2
    captured = capsys.readouterr()
    assert "[WARNING] Native Javascript AST parser ('tree-sitter-javascript') is not installed." in captured.err
    assert "uv run --with tree-sitter --with tree-sitter-javascript" in captured.err
    assert "uv pip install 'tree-sitter>=0.23.0' 'tree-sitter-javascript>=0.23.0'" in captured.err
    assert "pip install tree-sitter tree-sitter-javascript" in captured.err


def test_missing_native_javascript_parser_exits_code_2_json(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    from typing import Any
    import json
    import code_health
    from _code_health.ir_models import MissingNativeParserError
    import _code_health.js_parser

    def mock_check() -> tuple[Any, Any]:
        raise MissingNativeParserError("javascript", ["tree-sitter", "tree-sitter-javascript"])

    monkeypatch.setattr(_code_health.js_parser, "check_javascript_dependencies", mock_check)

    js_file = tmp_path / "app.js"
    js_file.write_text("console.log('hi');\n", encoding="utf-8")

    rc = code_health.main([str(js_file), "--format", "json", "--no-git"])
    assert rc == 2
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["status"] == "missing_native_parser"
    assert payload["language"] == "javascript"
    assert "tree-sitter-javascript" in payload["missing_packages"]
    assert "uv_ephemeral" in payload["install_commands"]
    assert "uv_project" in payload["install_commands"]
    assert "pip" in payload["install_commands"]


def test_python_and_java_runs_never_trigger_missing_js_parser(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    from typing import Any
    import code_health
    import _code_health.js_parser

    def mock_check() -> tuple[Any, Any]:
        raise AssertionError("JS parser should never be invoked for non-JS files!")

    monkeypatch.setattr(_code_health.js_parser, "check_javascript_dependencies", mock_check)

    # 1. Pure Python run
    py_file = tmp_path / "app.py"
    py_file.write_text("def run() -> int:\n    '''Doc.'''\n    return 1\n", encoding="utf-8")
    rc_py = code_health.main([str(py_file), "--no-git"])
    assert rc_py == 0

    # 2. Pure Java run
    java_file = tmp_path / "App.java"
    java_file.write_text("public class App {\n    /** Greet. */\n    public String greet() { return \"hi\"; }\n}\n", encoding="utf-8")
    rc_java = code_health.main([str(java_file), "--no-git"])
    assert rc_java == 0


def test_parameter_defaults_and_jsdoc_inferred_as_typed_with_zero_penalty(tmp_path: Path) -> None:
    from _code_health.js_parser import parse_javascript_file
    from _code_health.profiles_js import JAVASCRIPT_PROFILE
    from _code_health.ir_scorer import UniversalIRScorer

    code = """
    /**
     * Calculate tax with JSDoc type annotations.
     * @param {number} amount
     * @param {number} rate
     */
    function calculateTax(amount, rate) {
        return amount * rate;
    }

    /**
     * Greet user with parameter default values.
     */
    function greet(name = "friend", greeting = "Hello") {
        return `${greeting}, ${name}!`;
    }
    """
    f = tmp_path / "typed.js"
    f.write_text(code, encoding="utf-8")

    mod = parse_javascript_file(f, "typed.js", is_test=False)
    scorer = UniversalIRScorer(RubricConfig(), JAVASCRIPT_PROFILE)

    for fn in mod.functions:
        rep = scorer.score_function(fn, "typed.js", is_test=False)
        untyped_findings = [f for f in rep.findings if "unannotated parameter" in f or "untyped param" in f]
        assert not untyped_findings, f"Unexpected parameter typing findings in {fn.name}: {untyped_findings}"
        assert rep.scores.clean == 100.0


def test_untyped_undefaulted_parameters_penalized(tmp_path: Path) -> None:
    from _code_health.js_parser import parse_javascript_file
    from _code_health.profiles_js import JAVASCRIPT_PROFILE
    from _code_health.ir_scorer import UniversalIRScorer

    code = """
    /**
     * Process 3 untyped, undefaulted parameters.
     */
    function processThree(a, b, c) {
        return a + b + c;
    }

    /**
     * Process 6 untyped, undefaulted parameters (capped at -10).
     */
    function processSix(a, b, c, d, e, f) {
        return a + b + c + d + e + f;
    }
    """
    f = tmp_path / "untyped.js"
    f.write_text(code, encoding="utf-8")

    mod = parse_javascript_file(f, "untyped.js", is_test=False)
    scorer = UniversalIRScorer(RubricConfig(), JAVASCRIPT_PROFILE)

    fn3 = next(fn for fn in mod.functions if fn.name == "processThree")
    rep3 = scorer.score_function(fn3, "untyped.js", is_test=False)
    assert any("3 unannotated parameter(s) without default values" in f for f in rep3.findings)
    assert rep3.scores.clean == 94.0  # 100 - 3 * 2.0 = 94.0

    fn6 = next(fn for fn in mod.functions if fn.name == "processSix")
    rep6 = scorer.score_function(fn6, "untyped.js", is_test=False)
    assert any("6 unannotated parameter(s) without default values" in f for f in rep6.findings)
    assert rep6.scores.clean == 90.0  # 100 - min(10.0, 6 * 2.0) = 90.0


def test_loose_equality_legacy_var_and_empty_catch_penalties(tmp_path: Path) -> None:
    from _code_health.js_parser import parse_javascript_file
    from _code_health.profiles_js import JAVASCRIPT_PROFILE
    from _code_health.ir_scorer import UniversalIRScorer

    code = """
    /**
     * Smelly function with var, loose equality, and empty catch.
     */
    function smelly(x, y) {
        var a = 1;
        var b = 2;
        if (x == y || a != b) {
            console.log(a);
        }
        try {
            doSomething();
        } catch (e) {
        }
        return x;
    }
    """
    f = tmp_path / "smelly.js"
    f.write_text(code, encoding="utf-8")

    mod = parse_javascript_file(f, "smelly.js", is_test=False)
    scorer = UniversalIRScorer(RubricConfig(), JAVASCRIPT_PROFILE)

    fn = mod.functions[0]
    rep = scorer.score_function(fn, "smelly.js", is_test=False)

    findings = rep.findings
    assert any("2 legacy 'var' declaration(s) detected" in f for f in findings)
    assert any("2 loose equality comparison(s)" in f for f in findings)
    assert any("empty catch block swallows exception" in f for f in findings)
    assert any("2 unannotated parameter(s) without default values" in f for f in findings)

    # 100 - var(6.0) - loose_eq(4.0) - empty_catch(10.0) - untyped(4.0) = 76.0
    assert rep.scores.clean == 76.0


def test_dynamic_eval_and_new_function_security_penalties(tmp_path: Path) -> None:
    from _code_health.js_parser import parse_javascript_file
    from _code_health.profiles_js import JAVASCRIPT_PROFILE
    from _code_health.ir_scorer import UniversalIRScorer

    code = """
    /**
     * Executes dynamically.
     */
    function runEval(input = "1 + 1") {
        return eval(input);
    }

    /**
     * Creates function constructor.
     */
    function runNewFunction(body = "return 1;") {
        const fn = new Function(body);
        return fn();
    }
    """
    f = tmp_path / "dynamic.js"
    f.write_text(code, encoding="utf-8")

    mod = parse_javascript_file(f, "dynamic.js", is_test=False)
    scorer = UniversalIRScorer(RubricConfig(), JAVASCRIPT_PROFILE)

    fn_eval = next(fn for fn in mod.functions if fn.name == "runEval")
    rep_eval = scorer.score_function(fn_eval, "dynamic.js", is_test=False)
    assert any("dynamic code execution via eval (-40.0 pts)" in f for f in rep_eval.findings)
    assert rep_eval.scores.security == 60.0

    fn_new = next(fn for fn in mod.functions if fn.name == "runNewFunction")
    rep_new = scorer.score_function(fn_new, "dynamic.js", is_test=False)
    assert any("dynamic code execution via new Function (-40.0 pts)" in f for f in rep_new.findings)
    assert rep_new.scores.security == 60.0


def test_timer_string_and_proto_mutation_security_penalties(tmp_path: Path) -> None:
    from _code_health.js_parser import parse_javascript_file
    from _code_health.profiles_js import JAVASCRIPT_PROFILE
    from _code_health.ir_scorer import UniversalIRScorer

    code = """
    /**
     * Timer with string argument and proto mutation.
     */
    function scheduleWork(obj = {}) {
        setTimeout("doAlert()", 1000);
        setInterval("doTick()", 2000);
        obj.__proto__ = { admin: true };
        return obj;
    }
    """
    f = tmp_path / "timers_proto.js"
    f.write_text(code, encoding="utf-8")

    mod = parse_javascript_file(f, "timers_proto.js", is_test=False)
    scorer = UniversalIRScorer(RubricConfig(), JAVASCRIPT_PROFILE)

    fn = mod.functions[0]
    rep = scorer.score_function(fn, "timers_proto.js", is_test=False)

    findings = rep.findings
    assert any("string argument to setTimeout causes implicit code evaluation (-20.0 pts)" in f for f in findings)
    assert any("string argument to setInterval causes implicit code evaluation (-20.0 pts)" in f for f in findings)
    assert any("direct prototype mutation via '__proto__' (-25.0 pts)" in f for f in findings)

    # 100 - setTimeout(20) - setInterval(20) - proto(25) = 35.0
    assert rep.scores.security == 35.0


def test_with_statement_and_debugger_penalties(tmp_path: Path) -> None:
    from _code_health.js_parser import parse_javascript_file
    from _code_health.profiles_js import JAVASCRIPT_PROFILE
    from _code_health.ir_scorer import UniversalIRScorer

    code = """
    /**
     * Function with with-statement and debugger statement.
     */
    function debugAndScope(obj = {}) {
        debugger;
        with (obj) {
            console.log(msg);
        }
    }
    """
    f = tmp_path / "with_debug.js"
    f.write_text(code, encoding="utf-8")

    mod = parse_javascript_file(f, "with_debug.js", is_test=False)
    scorer = UniversalIRScorer(RubricConfig(), JAVASCRIPT_PROFILE)

    fn = mod.functions[0]
    rep = scorer.score_function(fn, "with_debug.js", is_test=False)

    findings = rep.findings
    assert any("debugger statement detected (-10.0 pts)" in f for f in findings)
    assert any("'with' statement obscures lexical scope" in f for f in findings)

    assert rep.scores.clean == 90.0  # 100 - 10.0 = 90.0
    assert rep.scores.security == 70.0  # 100 - 30.0 = 70.0


def test_bdd_test_block_extraction_and_test_flag(tmp_path: Path) -> None:
    from _code_health.js_parser import parse_javascript_file

    code = """
    describe("MathService", () => {
        it("should add numbers correctly", () => {
            expect(1 + 2).toBe(3);
        });

        test("should multiply numbers correctly", () => {
            assert.strictEqual(2 * 3, 6);
        });
    });
    """
    f = tmp_path / "math.test.js"
    f.write_text(code, encoding="utf-8")

    mod = parse_javascript_file(f, "src/__tests__/math.test.js", is_test=True)
    assert mod.is_test is True
    assert len(mod.functions) == 2

    fn_add = next(fn for fn in mod.functions if "add numbers" in fn.name)
    assert fn_add.name == "test: should add numbers correctly"
    assert fn_add.qualname == "test: should add numbers correctly"
    assert fn_add.is_test is True

    fn_mul = next(fn for fn in mod.functions if "multiply numbers" in fn.name)
    assert fn_mul.name == "test: should multiply numbers correctly"
    assert fn_mul.qualname == "test: should multiply numbers correctly"
    assert fn_mul.is_test is True


def test_assertion_matcher_recognition_and_assertion_hygiene(tmp_path: Path) -> None:
    from _code_health.js_parser import parse_javascript_file
    from _code_health.profiles_js import JAVASCRIPT_PROFILE
    from _code_health.ir_scorer import UniversalIRScorer

    code = """
    describe("TestSuite", () => {
        it("has zero assertions", () => {
            const x = 1;
            console.log(x);
        });

        it("has normal assertion count (Node assert, Jest expect, Chai should)", () => {
            expect(1).toBe(1);
            expect(2).toEqual(2);
            assert.strictEqual(3, 3);
            assert.ok(true);
        });

        it("has excessive assertions (>8)", () => {
            expect(1).toBe(1);
            expect(2).toBe(2);
            expect(3).toBe(3);
            expect(4).toBe(4);
            expect(5).toBe(5);
            expect(6).toBe(6);
            expect(7).toBe(7);
            expect(8).toBe(8);
            expect(9).toBe(9);
            expect(10).toBe(10);
        });
    });
    """
    f = tmp_path / "assertions.test.js"
    f.write_text(code, encoding="utf-8")

    mod = parse_javascript_file(f, "test/assertions.test.js", is_test=True)
    scorer = UniversalIRScorer(RubricConfig(), JAVASCRIPT_PROFILE)

    # 1. Zero assertions: flagged with -30 pts Clean (Test)
    fn_zero = next(fn for fn in mod.functions if "zero assertions" in fn.name)
    rep_zero = scorer.score_function(fn_zero, "test/assertions.test.js", is_test=True)
    assert any("Clean (Test): test has 0 assertions" in f for f in rep_zero.findings)
    assert rep_zero.scores.clean == 70.0  # 100 - 30 = 70.0

    # 2. Normal assertions (4 assertions): 100 Clean score, zero findings
    fn_normal = next(fn for fn in mod.functions if "normal assertion count" in fn.name)
    rep_normal = scorer.score_function(fn_normal, "test/assertions.test.js", is_test=True)
    assert not rep_normal.findings
    assert rep_normal.scores.clean == 100.0

    # 3. Excessive assertions (10 assertions): flagged for >8 assertions (-6.0 pts)
    fn_excess = next(fn for fn in mod.functions if "excessive assertions" in fn.name)
    rep_excess = scorer.score_function(fn_excess, "test/assertions.test.js", is_test=True)
    assert any("Clean (Test): 10 assertions in single test (>8)" in f for f in rep_excess.findings)
    assert rep_excess.scores.clean == 94.0  # 100 - (10 - 8) * 3.0 = 94.0
