"""Unit tests for Java AST extraction, LCOM4 cohesion, and multi-language discovery."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPTS_DIR = str(Path(__file__).resolve().parents[2] / "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import pytest
from _code_health.ir_scorer import UniversalIRScorer
from _code_health.models import RubricConfig
from _code_health.module_engine import is_test_file_path


def test_is_test_file_path_recognizes_java_conventions() -> None:
    assert is_test_file_path("src/test/java/com/example/UserServiceTest.java")
    assert is_test_file_path("src/test/java/com/example/OrderIT.java")
    assert is_test_file_path("test/com/example/AppTests.java")
    assert not is_test_file_path("src/main/java/com/example/UserService.java")
    assert not is_test_file_path("src/main/java/com/example/TestHelper.java")


def test_java_tree_sitter_parser_parses_clean_java_service(tmp_path: Path) -> None:
    tree_sitter = pytest.importorskip("tree_sitter")
    tree_sitter_java = pytest.importorskip("tree_sitter_java")
    from _code_health.java_parser import parse_java_file
    from _code_health.profiles_java import JAVA_PROFILE

    java_code = '''
package com.example.service;

import java.util.List;

/**
 * Clean cohesive user service.
 */
public class UserService {
    private final String prefix;

    public UserService(String prefix) {
        this.prefix = prefix;
    }

    /**
     * Format a username.
     */
    public String formatUser(String name) {
        if (name == null || name.isEmpty()) {
            return prefix + "Anonymous";
        }
        return prefix + name.trim();
    }
}
'''
    f = tmp_path / "UserService.java"
    f.write_text(java_code, encoding="utf-8")

    ir_mod = parse_java_file(f, "com/example/service/UserService.java", is_test=False)
    assert ir_mod.language == "java"
    assert len(ir_mod.classes) == 1
    cls = ir_mod.classes[0]
    assert cls.name == "UserService"
    assert len(cls.fields) == 1
    assert cls.fields[0].name == "prefix"

    scorer = UniversalIRScorer(RubricConfig(), JAVA_PROFILE)
    cls_rep = scorer.score_class(cls, "UserService.java", is_test=False)
    assert cls_rep.scores.grade == "A"
    assert cls_rep.scores.composite >= 90.0
    assert cls_rep.lcom4 == 1


def test_java_lcom4_detects_disconnected_components_with_implicit_field_refs(tmp_path: Path) -> None:
    pytest.importorskip("tree_sitter_java")
    from _code_health.java_parser import parse_java_file
    from _code_health.profiles_java import JAVA_PROFILE

    code = '''
public class GodService {
    private String name;
    private int counter;

    public String getName() {
        return name;
    }

    public void updateName(String val) {
        name = val;
    }

    public int getCounter() {
        return counter;
    }

    public void increment() {
        counter++;
    }
}
'''
    f = tmp_path / "GodService.java"
    f.write_text(code, encoding="utf-8")

    ir_mod = parse_java_file(f, "GodService.java", is_test=False)
    cls = ir_mod.classes[0]
    assert cls.lcom4 == 2  # {getName, updateName} and {getCounter, increment} are disconnected


def test_cli_mixed_python_and_java_project(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    pytest.importorskip("tree_sitter_java")
    from code_health import main

    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "app.py").write_text('"""App."""\ndef run() -> int:\n    """Run."""\n    return 42\n', encoding="utf-8")
    (src_dir / "Greeter.java").write_text('public class Greeter {\n    public String hello() {\n        return "hi";\n    }\n}\n', encoding="utf-8")

    rc = main([str(src_dir), "--no-git"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "app.py" in out
    assert "Greeter.java" in out
    assert "Score:" in out


def test_missing_java_dependencies_halts_with_exit_code_2(tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    import json
    from code_health import main
    import _code_health.java_parser as jp

    def fake_check():
        from _code_health.ir_models import MissingNativeParserError
        raise MissingNativeParserError("java", ["tree-sitter", "tree-sitter-java"])

    monkeypatch.setattr(jp, "check_java_dependencies", fake_check)

    f = tmp_path / "MyClass.java"
    f.write_text("public class MyClass {}", encoding="utf-8")

    # 1. Console mode exit code 2
    rc = main([str(f), "--no-git"])
    captured = capsys.readouterr()
    assert rc == 2
    err_text = captured.err or captured.out
    assert "Native Java AST parser ('tree-sitter-java') is not installed" in err_text
    assert "uv run --with tree-sitter" in err_text

    # 2. JSON mode exit code 2 with structured error payload
    rc_json = main([str(f), "--format", "json", "--no-git"])
    out_json = capsys.readouterr().out
    assert rc_json == 2
    data = json.loads(out_json)
    assert data["status"] == "missing_native_parser"
    assert "tree-sitter-java" in data["missing_packages"]


def test_pure_python_unaffected_when_java_parser_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from code_health import main
    import _code_health.java_parser as jp

    def fake_check():
        from _code_health.ir_models import MissingNativeParserError
        raise MissingNativeParserError("java", ["tree-sitter", "tree-sitter-java"])

    monkeypatch.setattr(jp, "check_java_dependencies", fake_check)

    py_file = tmp_path / "app.py"
    py_file.write_text('"""App."""\ndef run() -> int:\n    return 1\n', encoding="utf-8")
    rc = main([str(py_file), "--no-git"])
    assert rc == 0


