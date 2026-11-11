"""Unit tests for TypeScript and TSX code health analyzer."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
from typing import Any

_SCRIPTS_DIR = str(Path(__file__).resolve().parents[2] / "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import pytest  # noqa: E402
import code_health  # noqa: E402
import _code_health.ts_parser as ts_parser_mod  # noqa: E402
from _code_health.models import RubricConfig  # noqa: E402
from _code_health.module_engine import is_test_file_path  # noqa: E402
from _code_health.reporting import CodeHealthRunner  # noqa: E402
from _code_health.ts_parser import parse_typescript_file  # noqa: E402


def test_is_test_file_path_recognizes_typescript_conventions() -> None:
    # Test files
    assert is_test_file_path("src/components/button.test.ts") is True
    assert is_test_file_path("src/components/button.test.tsx") is True
    assert is_test_file_path("src/services/api.spec.ts") is True
    assert is_test_file_path("src/services/api.spec.tsx") is True
    assert is_test_file_path("tests/unit/calculator_test.ts") is True
    assert is_test_file_path("src/__tests__/utils.ts") is True
    assert is_test_file_path("test/integration.mts") is True
    assert is_test_file_path("test/config.spec.cts") is True

    # Source files
    assert is_test_file_path("src/components/button.ts") is False
    assert is_test_file_path("src/components/button.tsx") is False
    assert is_test_file_path("src/services/api.mts") is False
    assert is_test_file_path("lib/tools/runner.cts") is False


def test_typescript_file_discovery_and_ambient_skipping() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        src_dir = root / "src"
        src_dir.mkdir(parents=True)
        (src_dir / "index.ts").write_text("console.log('main');\n", encoding="utf-8")
        (src_dir / "component.tsx").write_text("export const C = () => <div />;\n", encoding="utf-8")
        (src_dir / "module.mts").write_text("export const x: number = 1;\n", encoding="utf-8")
        (src_dir / "config.cts").write_text("export = {};\n", encoding="utf-8")

        # Ambient declaration files (must be skipped)
        (src_dir / "globals.d.ts").write_text("declare const foo: string;\n", encoding="utf-8")
        (src_dir / "types.d.mts").write_text("declare module 'foo';\n", encoding="utf-8")
        (src_dir / "legacy.d.cts").write_text("declare var bar: number;\n", encoding="utf-8")

        # Minified and vendor files (must be skipped)
        (src_dir / "app.min.ts").write_text("const a=1;\n", encoding="utf-8")
        (src_dir / "huge_line.ts").write_text("const a: number = 1; " + "//" + "x" * 1200 + "\n", encoding="utf-8")

        vendor = root / "node_modules" / "pkg"
        vendor.mkdir(parents=True)
        (vendor / "vendor.ts").write_text("export const v = 1;\n", encoding="utf-8")

        # Run auto discovery
        runner = CodeHealthRunner(repo_root=root, git_mode="no-git")
        discovered = runner._discover_files([root])
        discovered_rel = [p.relative_to(root).as_posix() for p in discovered]

        # Valid source files discovered
        assert "src/index.ts" in discovered_rel
        assert "src/component.tsx" in discovered_rel
        assert "src/module.mts" in discovered_rel
        assert "src/config.cts" in discovered_rel

        # Ambient declarations, minified, and node_modules skipped
        assert "src/globals.d.ts" not in discovered_rel
        assert "src/types.d.mts" not in discovered_rel
        assert "src/legacy.d.cts" not in discovered_rel
        assert "src/app.min.ts" not in discovered_rel
        assert "src/huge_line.ts" not in discovered_rel
        assert "node_modules/pkg/vendor.ts" not in discovered_rel

        # Explicit --lang typescript flag
        runner_ts = CodeHealthRunner(repo_root=root, git_mode="no-git", lang_override="typescript")
        discovered_ts = runner_ts._discover_files([root])
        discovered_ts_rel = [p.relative_to(root).as_posix() for p in discovered_ts]
        assert "src/index.ts" in discovered_ts_rel
        assert "src/globals.d.ts" not in discovered_ts_rel


def test_tree_sitter_ts_parser_parses_classes_functions_and_tsx() -> None:
    code = """
    interface UserConfig {
        id: string;
        active: boolean;
    }

    type Point = { x: number; y: number };

    class DataService {
        constructor(private readonly baseUrl: string, public timeout: number = 5000) {}

        public async fetchData(endpoint: string): Promise<string> {
            return this.baseUrl + endpoint;
        }
    }

    export function calculateTax(amount: number = 100, rate: number = 0.05): number {
        if (amount <= 0) {
            return 0;
        }
        return amount * rate;
    }

    export const renderWidget = (title: string): string => title.toUpperCase();
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        ts_file = Path(tmp_dir) / "service.ts"
        ts_file.write_text(code, encoding="utf-8")

        mod = parse_typescript_file(ts_file, "src/service.ts", is_test=False)
        assert mod.language == "typescript"
        assert mod.file_path == "src/service.ts"
        assert mod.loc > 0

        # Classes
        assert len(mod.classes) == 1
        cls = mod.classes[0]
        assert cls.name == "DataService"
        field_names = [f.name for f in cls.fields]
        assert "baseUrl" in field_names
        assert "timeout" in field_names
        method_names = [m.name for m in cls.methods]
        assert "constructor" in method_names
        assert "fetchData" in method_names

        fetch_method = next(m for m in cls.methods if m.name == "fetchData")
        assert fetch_method.qualname == "DataService.fetchData"
        assert fetch_method.return_type is not None

        # Functions
        fn_names = [f.name for f in mod.functions]
        assert "calculateTax" in fn_names
        assert "renderWidget" in fn_names


def test_tree_sitter_tsx_parser_parses_jsx_components() -> None:
    code = """
    export const Button = (props: { label: string }): string => {
        return <button className="btn">{props.label}</button>;
    };
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        tsx_file = Path(tmp_dir) / "button.tsx"
        tsx_file.write_text(code, encoding="utf-8")

        mod = parse_typescript_file(tsx_file, "src/button.tsx", is_test=False)
        assert mod.language == "typescript"
        assert len(mod.functions) == 1
        assert mod.functions[0].name == "Button"


def test_tree_sitter_ts_parser_absorbs_inline_callbacks_into_parent() -> None:
    code = """
    export function processItems(items: number[] = []): number {
        return items
            .map((x: number): number => x * 2)
            .filter((x: number): boolean => x > 10)
            .reduce((acc: number, curr: number): number => acc + curr, 0);
    }
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        ts_file = Path(tmp_dir) / "process.ts"
        ts_file.write_text(code, encoding="utf-8")

        mod = parse_typescript_file(ts_file, "src/process.ts", is_test=False)
        # Inline arrow callbacks should be absorbed into processItems
        assert len(mod.functions) == 1
        assert mod.functions[0].name == "processItems"


def test_cli_lang_typescript_flag_and_multilang_scan(capsys: pytest.CaptureFixture[str]) -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        src_dir = root / "src"
        src_dir.mkdir(parents=True)

        # Python file
        (src_dir / "calc.py").write_text(
            'def add(a: int, b: int) -> int:\n    """Add two numbers."""\n    return a + b\n',
            encoding="utf-8",
        )
        # TypeScript file
        (src_dir / "service.ts").write_text(
            '/** Math service. */\nexport class MathService {\n    /** Add two numbers. */\n    public add(a: number = 0, b: number = 0): number {\n        return a + b;\n    }\n}\n',
            encoding="utf-8",
        )

        exit_code = code_health.main([str(src_dir), "--no-git", "--format", "json", "--lang", "typescript"])
        assert exit_code == 0
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        # In --lang typescript mode, only service.ts should be analyzed
        assert data["files_count"] == 1
        assert data["files"][0]["file_path"].endswith("service.ts")
        assert data["files"][0]["scores"]["grade"] == "A"


def test_missing_native_typescript_parser_exits_code_2_console(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    monkeypatch.setitem(sys.modules, "tree_sitter_typescript", None)

    ts_file = tmp_path / "app.ts"
    ts_file.write_text("export const x: number = 1;\n", encoding="utf-8")

    rc = code_health.main([str(ts_file), "--no-git"])
    assert rc == 2
    captured = capsys.readouterr()
    assert "[WARNING] Native Typescript AST parser ('tree-sitter-typescript') is not installed." in captured.err
    assert "uv run --with tree-sitter --with tree-sitter-typescript" in captured.err
    assert "uv pip install 'tree-sitter>=0.23.0' 'tree-sitter-typescript>=0.23.0'" in captured.err
    assert "pip install tree-sitter tree-sitter-typescript" in captured.err


def test_missing_native_typescript_parser_exits_code_2_json(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    monkeypatch.setitem(sys.modules, "tree_sitter_typescript", None)

    ts_file = tmp_path / "app.ts"
    ts_file.write_text("export const x: number = 1;\n", encoding="utf-8")

    rc = code_health.main([str(ts_file), "--format", "json", "--no-git"])
    assert rc == 2
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["status"] == "missing_native_parser"
    assert payload["language"] == "typescript"
    assert "tree-sitter-typescript" in payload["missing_packages"]
    assert "uv_ephemeral" in payload["install_commands"]
    assert "uv_project" in payload["install_commands"]
    assert "pip" in payload["install_commands"]


def test_python_java_js_runs_never_trigger_missing_ts_parser(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def mock_check() -> tuple[Any, Any]:
        raise AssertionError("TS parser should never be invoked for non-TS files!")

    monkeypatch.setattr(ts_parser_mod, "check_typescript_dependencies", mock_check)

    # 1. Pure Python run
    py_file = tmp_path / "app.py"
    py_file.write_text("def run() -> int:\n    '''Doc.'''\n    return 1\n", encoding="utf-8")
    assert code_health.main([str(py_file), "--no-git"]) == 0

    # 2. Pure Java run
    java_file = tmp_path / "App.java"
    java_file.write_text("public class App {\n    /** Greet. */\n    public String greet() { return \"hi\"; }\n}\n", encoding="utf-8")
    assert code_health.main([str(java_file), "--no-git"]) == 0

    # 3. Pure JavaScript run
    js_file = tmp_path / "app.js"
    js_file.write_text("/** Greet. */\nexport function greet(name = 'world') { return name; }\n", encoding="utf-8")
    assert code_health.main([str(js_file), "--no-git"]) == 0

