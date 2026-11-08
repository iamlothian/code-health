"""Unit tests for the standalone deterministic Code Health Analyzer (scripts/code_health.py)."""

from __future__ import annotations

import ast
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any


def _load_code_health():
    script_path = Path(__file__).resolve().parents[2] / "scripts" / "code_health.py"
    spec = importlib.util.spec_from_file_location("code_health", script_path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_clean_small_function_scores_grade_a() -> None:
    ch = _load_code_health()
    code = '''
def calculate_discount(price: float, rate: float) -> float:
    """Compute discounted price."""
    if rate <= 0:
        return price
    return price * (1.0 - rate)
'''
    tree = ast.parse(code)
    fn_node = tree.body[0]
    assert isinstance(fn_node, ast.FunctionDef)
    report = ch.analyze_function_node(
        fn_node,
        code.splitlines(),
        "src/pricing.py",
        is_test=False,
        config=ch.RubricConfig(),
    )
    assert report.scores.grade == "A"
    assert report.scores.composite >= 95.0
    assert report.cyclomatic_complexity == 2
    assert report.findings == []


def test_bloated_complex_function_penalizes_srp_size_complexity_clean_security() -> None:
    ch = _load_code_health()
    body_lines = ["def mega_handler(raw_path, flag=True, a=1, b=2, c=3, d=4):"]
    body_lines.append("    p = Path(raw_path)")
    body_lines.append('    p.write_text("dirty")')
    body_lines.append('    subprocess.run("git checkout " + raw_path, shell=True)')
    body_lines.append("    data = yaml.load(p.read_text())")
    body_lines.append("    console.print(data)")
    for i in range(55):
        body_lines.append(f"    if a == {i}:")
        body_lines.append("        if b > 0:")
        body_lines.append("            if c > 0:")
        body_lines.append("                if d > 0:")
        body_lines.append(f"                    print({i})")
    body_lines.append("    try:")
    body_lines.append("        pass")
    body_lines.append("    except Exception:")
    body_lines.append("        pass")
    code = "\n".join(body_lines)
    tree = ast.parse(code)
    fn_node = tree.body[0]
    assert isinstance(fn_node, ast.FunctionDef)
    report = ch.analyze_function_node(
        fn_node,
        code.splitlines(),
        "src/handler.py",
        is_test=False,
        config=ch.RubricConfig(),
    )
    assert report.scores.srp < 70.0
    assert report.scores.size < 50.0
    assert report.scores.complexity < 50.0
    assert report.scores.clean < 70.0
    assert report.scores.security < 60.0
    assert any("LOC=" in f for f in report.findings)
    assert any("shell=True" in f or "yaml.load" in f for f in report.findings)


def test_cli_decorated_entrypoint_exempts_boolean_defaults_and_allows_6_params() -> None:
    ch = _load_code_health()
    code = '''
@app.command("run")
def run_cmd(a: str, b: str, c: str, d: str, e: bool = False, f: bool = True) -> None:
    """CLI entrypoint."""
    return None
'''
    tree = ast.parse(code)
    fn_node = tree.body[0]
    assert isinstance(fn_node, ast.FunctionDef)
    report = ch.analyze_function_node(
        fn_node,
        code.splitlines(),
        "src/cli.py",
        is_test=False,
        config=ch.RubricConfig(),
    )
    assert report.scores.size == 100.0
    assert not any("bool default" in f for f in report.findings)


def test_lcom4_cohesive_vs_disconnected_class() -> None:
    ch = _load_code_health()
    cohesive_code = "\n".join([
        "class CohesiveService:",
        '    """Single responsibility service."""',
        "    def __init__(self, db: str) -> None:",
        "        self.db = db",
        "    def fetch(self, key: str) -> str:",
        '        """Fetch item."""',
        '        return f"{self.db}:{key}"',
        "    def save(self, key: str, val: str) -> str:",
        '        """Save item."""',
        "        return self.fetch(key) + val",
    ])
    disconnected_code = "\n".join([
        "class DisconnectedGodClass:",
        '    """Does two unrelated things."""',
        "    def a1(self) -> int:",
        '        """Group A1."""',
        "        return self.x + 1",
        "    def a2(self) -> int:",
        '        """Group A2."""',
        "        return self.x + 2",
        "    def b1(self) -> str:",
        '        """Group B1."""',
        "        return self.y.strip()",
        "    def b2(self) -> str:",
        '        """Group B2."""',
        "        return self.y.lower()",
    ])
    c_node = ast.parse(cohesive_code).body[0]
    d_node = ast.parse(disconnected_code).body[0]
    assert isinstance(c_node, ast.ClassDef) and isinstance(d_node, ast.ClassDef)
    c_rep = ch.analyze_class_node(c_node, cohesive_code.splitlines(), "src/svc.py", False, ch.RubricConfig())
    d_rep = ch.analyze_class_node(d_node, disconnected_code.splitlines(), "src/god.py", False, ch.RubricConfig())
    assert c_rep.lcom4 == 1 and c_rep.scores.grade == "A"
    assert d_rep.lcom4 == 2 and d_rep.scores.srp < c_rep.scores.srp
    assert any("LCOM4=2" in f for f in d_rep.findings)


def test_pydantic_model_and_small_class_exempt_from_lcom4() -> None:
    ch = _load_code_health()
    model_code = '''
class UserModel(BaseModel):
    """Pydantic model with validator methods."""
    name: str
    def v1(self) -> str:
        """Validator 1."""
        return "a"
    def v2(self) -> str:
        """Validator 2."""
        return "b"
    def v3(self) -> str:
        """Validator 3."""
        return "c"
'''
    m_node = ast.parse(model_code).body[0]
    assert isinstance(m_node, ast.ClassDef)
    m_rep = ch.analyze_class_node(
        m_node, model_code.splitlines(), "src/models.py", False, ch.RubricConfig()
    )
    assert m_rep.lcom4 == 1
    assert m_rep.scores.grade == "A"


def test_empty_init_py_scores_100(tmp_path: Path) -> None:
    ch = _load_code_health()
    init_file = tmp_path / "src" / "pkg" / "__init__.py"
    init_file.parent.mkdir(parents=True)
    init_file.write_text('"""Package."""\n', encoding="utf-8")
    rep = ch.analyze_file(init_file, tmp_path, {"pkg"}, ch.RubricConfig(), git_stats=None)
    assert rep.scores.composite == 100.0
    assert rep.scores.grade == "A"


def test_cli_single_file_and_folder_and_json_output(tmp_path: Path, capsys: Any) -> None:
    ch = _load_code_health()
    pkg = tmp_path / "sample_pkg"
    pkg.mkdir()
    f1 = pkg / "mod.py"
    f1.write_text(
        '"""Sample module."""\n\ndef add(a: int, b: int) -> int:\n    """Add."""\n    return a + b\n',
        encoding="utf-8",
    )
    # 1. Single file console mode
    rc = ch.main([str(f1), "--no-git"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "mod.py" in out
    assert "add" in out

    # 2. Folder JSON mode + --json-out + --markdown-out
    json_out = tmp_path / "scorecard.json"
    md_out = tmp_path / "report.md"
    rc2 = ch.main(
        [
            str(pkg),
            "--no-git",
            "--format",
            "json",
            "--json-out",
            str(json_out),
            "--markdown-out",
            str(md_out),
        ]
    )
    out2 = capsys.readouterr().out
    data = json.loads(out2)
    assert rc2 == 0 and data["files_count"] == 1
    assert json_out.is_file() and md_out.is_file()
    assert "mod.py" in md_out.read_text(encoding="utf-8")

    # 3. --fail-under gate returns non-zero when threshold exceeds score
    rc3 = ch.main([str(f1), "--no-git", "--fail-under", "101.0"])
    assert rc3 == 1


