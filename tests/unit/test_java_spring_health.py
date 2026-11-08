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


def test_spring_boot_antipatterns_detected_with_exact_penalties(tmp_path: Path) -> None:
    pytest.importorskip("tree_sitter_java")
    from _code_health.java_parser import parse_java_file
    from _code_health.ir_scorer import UniversalIRScorer
    from _code_health.profiles_java import JAVA_PROFILE

    code = '''
package com.example.controller;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.transaction.annotation.Transactional;

@RestController
public class BadOrderController {
    @Autowired
    private OrderRepository orderRepository;

    @Transactional
    @GetMapping("/orders")
    public List<Order> listOrders(String filter) {
        String sql = "SELECT * FROM orders WHERE status = '" + filter + "'";
        return jdbcTemplate.query(sql);
    }
}
'''
    f = tmp_path / "BadOrderController.java"
    f.write_text(code, encoding="utf-8")

    ir_mod = parse_java_file(f, "BadOrderController.java", is_test=False)
    scorer = UniversalIRScorer(RubricConfig(), JAVA_PROFILE)
    cls = ir_mod.classes[0]
    rep = scorer.score_class(cls, "BadOrderController.java", is_test=False)

    findings = rep.findings + [f for m in rep.methods for f in m.findings]
    assert any("field injection detected on 'orderRepository'" in f for f in findings)
    assert any("directly injects orderRepository" in f for f in findings)
    assert any("@Transactional should not be placed on web controllers" in f for f in findings)
    assert any("potential SQL/JPQL injection" in f for f in findings)
    assert rep.scores.srp < 85.0
    assert rep.scores.security < 70.0


def test_spring_boot_web_entrypoint_relaxes_parameter_count(tmp_path: Path) -> None:
    pytest.importorskip("tree_sitter_java")
    from _code_health.java_parser import parse_java_file
    from _code_health.ir_scorer import UniversalIRScorer
    from _code_health.profiles_java import JAVA_PROFILE

    code = '''
package com.example.controller;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.PostMapping;

@RestController
public class SearchController {
    /**
     * Search endpoint with 5 parameters.
     */
    @PostMapping("/search")
    public String search(String q, int page, int size, String sort, boolean active) {
        return q;
    }
}
'''
    f = tmp_path / "SearchController.java"
    f.write_text(code, encoding="utf-8")

    ir_mod = parse_java_file(f, "SearchController.java", is_test=False)
    scorer = UniversalIRScorer(RubricConfig(), JAVA_PROFILE)
    cls = ir_mod.classes[0]
    m_rep = scorer.score_function(cls.methods[0], "SearchController.java", is_test=False, parent=cls)
    assert not any("params=" in f for f in m_rep.findings)
    assert m_rep.scores.size == 100.0


def test_spring_boot_workspace_auto_detection(tmp_path: Path) -> None:
    from _code_health.profiles import resolve_active_profiles

    # 1. Detected from file content
    f1 = tmp_path / "App.java"
    f1.write_text("import org.springframework.boot.SpringApplication;\npublic class App {}", encoding="utf-8")
    p1 = resolve_active_profiles(tmp_path, f1)
    assert any(fw.name == "spring-boot" for fw in p1.frameworks)

    # 2. Detected from pom.xml
    pom = tmp_path / "pom.xml"
    pom.write_text("<project><artifactId>spring-boot-starter-web</artifactId></project>", encoding="utf-8")
    f2 = tmp_path / "Plain.java"
    f2.write_text("public class Plain {}", encoding="utf-8")
    p2 = resolve_active_profiles(tmp_path, f2)
    assert any(fw.name == "spring-boot" for fw in p2.frameworks)

    # 3. Explicit override --framework none
    p3 = resolve_active_profiles(tmp_path, f2, framework_override="none")
    assert not any(fw.name == "spring-boot" for fw in p3.frameworks)


def test_spring_boot_transactional_on_private_method_penalized(tmp_path: Path) -> None:
    pytest.importorskip("tree_sitter_java")
    from _code_health.java_parser import parse_java_file
    from _code_health.ir_scorer import UniversalIRScorer
    from _code_health.profiles_java import JAVA_PROFILE

    code = '''
package com.example.service;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class OrderService {
    @Transactional
    private void internalProcess() {
        // do work
    }
}
'''
    f = tmp_path / "OrderService.java"
    f.write_text(code, encoding="utf-8")

    ir_mod = parse_java_file(f, "OrderService.java", is_test=False)
    scorer = UniversalIRScorer(RubricConfig(), JAVA_PROFILE)
    cls = ir_mod.classes[0]
    m_rep = scorer.score_function(cls.methods[0], "OrderService.java", is_test=False, parent=cls)
    assert any("@Transactional on private method has no effect" in f for f in m_rep.findings)
    assert m_rep.scores.srp <= 85.0


def test_java_test_assertion_recognition_junit_and_assertj(tmp_path: Path) -> None:
    pytest.importorskip("tree_sitter_java")
    from _code_health.java_parser import parse_java_file
    from _code_health.ir_scorer import UniversalIRScorer
    from _code_health.profiles_java import JAVA_PROFILE

    code = '''
package com.example.service;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.assertj.core.api.Assertions.assertThat;

public class OrderServiceTest {
    @Test
    void testWithAssertEquals() {
        assertEquals(1, 1);
    }

    @Test
    void testWithAssertThat() {
        assertThat("hello").isEqualTo("hello");
    }
}
'''
    f = tmp_path / "OrderServiceTest.java"
    f.write_text(code, encoding="utf-8")

    ir_mod = parse_java_file(f, "src/test/java/OrderServiceTest.java", is_test=True)
    scorer = UniversalIRScorer(RubricConfig(), JAVA_PROFILE)
    cls = ir_mod.classes[0]
    methods = {m.name: scorer.score_function(m, "src/test/java/OrderServiceTest.java", is_test=True, parent=cls) for m in cls.methods}

    assert not any("0 assertions" in f for f in methods["testWithAssertEquals"].findings)
    assert methods["testWithAssertEquals"].scores.clean == 100.0
    assert not any("0 assertions" in f for f in methods["testWithAssertThat"].findings)
    assert methods["testWithAssertThat"].scores.clean == 100.0


def test_java_test_assertion_mockmvc_and_empty_test_penalized(tmp_path: Path) -> None:
    pytest.importorskip("tree_sitter_java")
    from _code_health.java_parser import parse_java_file
    from _code_health.ir_scorer import UniversalIRScorer
    from _code_health.profiles_java import JAVA_PROFILE

    code = '''
package com.example.service;

import org.junit.jupiter.api.Test;
import org.springframework.test.web.servlet.MockMvc;

public class ControllerTest {
    @Test
    void testWithMockMvc(MockMvc mockMvc) throws Exception {
        mockMvc.perform(get("/orders")).andExpect(status().isOk());
    }

    @Test
    void testWithNoAssertions() {
        int x = 1 + 1;
    }

    void helperMethodWithoutAssertions() {
        int y = 2 + 2;
    }
}
'''
    f = tmp_path / "ControllerTest.java"
    f.write_text(code, encoding="utf-8")

    ir_mod = parse_java_file(f, "src/test/java/ControllerTest.java", is_test=True)
    scorer = UniversalIRScorer(RubricConfig(), JAVA_PROFILE)
    cls = ir_mod.classes[0]
    methods = {m.name: scorer.score_function(m, "src/test/java/ControllerTest.java", is_test=True, parent=cls) for m in cls.methods}

    assert not any("0 assertions" in f for f in methods["testWithMockMvc"].findings)
    assert methods["testWithMockMvc"].scores.clean == 100.0
    assert any("test has 0 assertions" in f for f in methods["testWithNoAssertions"].findings)
    assert methods["testWithNoAssertions"].scores.clean < 100.0
    assert not any("test has 0 assertions" in f for f in methods["helperMethodWithoutAssertions"].findings)


def test_java_fail_under_gate_cli_exit_code(tmp_path: Path) -> None:
    pytest.importorskip("tree_sitter_java")
    from code_health import main

    code = '''
package com.example.service;

public class SampleService {
    public String greet(String name) {
        return "Hello " + name;
    }
}
'''
    f = tmp_path / "SampleService.java"
    f.write_text(code, encoding="utf-8")

    # When fail-under is impossibly high (99.9), CLI returns exit code 1
    rc_fail = main([str(f), "--fail-under", "99.9", "--no-git"])
    assert rc_fail == 1

    # When fail-under is reasonable (50.0), CLI returns exit code 0
    rc_pass = main([str(f), "--fail-under", "50.0", "--no-git"])
    assert rc_pass == 0


def test_cli_lang_and_framework_overrides(tmp_path: Path) -> None:
    pytest.importorskip("tree_sitter_java")
    from code_health import main
    import io
    from contextlib import redirect_stdout
    import json

    py_file = tmp_path / "app.py"
    py_file.write_text("def hello() -> str:\n    '''Doc.'''\n    return 'hello'\n", encoding="utf-8")

    java_file = tmp_path / "App.java"
    java_file.write_text("public class App {\n    /** Greet. */\n    public String greet() { return \"hi\"; }\n}\n", encoding="utf-8")

    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = main([str(tmp_path), "--lang", "python", "--format", "json", "--no-git"])
    assert rc == 0
    data = json.loads(buf.getvalue())
    scanned_files = [f["file_path"] for f in data["files"]]
    assert any(f.endswith(".py") for f in scanned_files)
    assert not any(f.endswith(".java") for f in scanned_files)

    buf2 = io.StringIO()
    with redirect_stdout(buf2):
        rc2 = main([str(tmp_path), "--lang", "java", "--framework", "none", "--format", "json", "--no-git"])
    assert rc2 == 0
    data2 = json.loads(buf2.getvalue())
    scanned_files2 = [f["file_path"] for f in data2["files"]]
    assert any(f.endswith(".java") for f in scanned_files2)
    assert not any(f.endswith(".py") for f in scanned_files2)





