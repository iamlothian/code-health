"""Edge-case and code-review regression tests for TypeScript health analyzer."""

from __future__ import annotations

import json
from pathlib import Path
import sys

_SCRIPTS_DIR = str(Path(__file__).resolve().parents[2] / "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import pytest  # noqa: E402
import code_health  # noqa: E402
from _code_health.ir_scorer import UniversalIRScorer  # noqa: E402
from _code_health.models import RubricConfig  # noqa: E402
from _code_health.module_engine import _parse_git_log_output, is_test_file_path  # noqa: E402
from _code_health.profiles_ts import TYPESCRIPT_PROFILE  # noqa: E402
from _code_health.reporting import CodeHealthRunner  # noqa: E402
from _code_health.ts_parser import parse_typescript_file  # noqa: E402


def test_malformed_typescript_scores_zero_grade_f(tmp_path: Path) -> None:
    (tmp_path / "broken.ts").write_text("export function broken(x: number {\n  return ;;;\n}\n", encoding="utf-8")
    (tmp_path / "ok.ts").write_text("/** Add. */\nexport function add(a: number, b: number): number { return a + b; }\n", encoding="utf-8")
    report = CodeHealthRunner(repo_root=tmp_path, git_mode="no-git").run([tmp_path])
    by_name = {Path(f.file_path).name: f for f in report.files}
    assert by_name["broken.ts"].scores.composite == 0.0
    assert by_name["broken.ts"].scores.grade == "F"
    assert any("Syntax: parse error at L" in f for f in by_name["broken.ts"].findings)
    assert by_name["ok.ts"].scores.composite == 100.0


def test_object_literal_methods_qualname_extraction(tmp_path: Path) -> None:
    ts_file = tmp_path / "api.ts"
    ts_file.write_text(
        """export const api = {
  /** Fetch endpoint. */
  fetchData(ep: string): string { return ep; },
  /** Save id. */
  save: (id: string): void => {},
  /** Compute helper. */
  compute: function(flag: boolean): number { return flag ? 1 : 0; },
};
""",
        encoding="utf-8",
    )
    mod = parse_typescript_file(ts_file, "api.ts", is_test=False)
    assert [f.qualname for f in mod.functions] == ["api.fetchData", "api.save", "api.compute"]
    scorer = UniversalIRScorer(RubricConfig(), TYPESCRIPT_PROFILE)
    assert all(scorer.score_function(f, "api.ts", is_test=False).scores.composite >= 90.0 for f in mod.functions)


def test_ts_setter_accessor_no_missing_return_penalty(tmp_path: Path) -> None:
    ts_file = tmp_path / "box.ts"
    ts_file.write_text(
        """/** Box class. */
export class Box {
  private val: number = 0;
  /** Set value. */
  set value(v: number) { this.val = v; }
  /** Get value. */
  get value(): number { return this.val; }
}
""",
        encoding="utf-8",
    )
    mod = parse_typescript_file(ts_file, "box.ts", is_test=False)
    scorer = UniversalIRScorer(RubricConfig(), TYPESCRIPT_PROFILE)
    setter = next(m for m in mod.classes[0].methods if m.lineno == 5)
    assert setter.return_type == "void"
    assert scorer.score_function(setter, "box.ts", is_test=False, parent=mod.classes[0]).scores.clean == 100.0


def test_ts_optional_boolean_without_default_no_srp_penalty(tmp_path: Path) -> None:
    ts_file = tmp_path / "flags.ts"
    ts_file.write_text(
        """/** Opt flag. */
export function renderOpt(flag?: boolean): string { return flag ? "y" : "n"; }
/** Default flag. */
export function renderDefault(flag: boolean = false): string { return flag ? "y" : "n"; }
""",
        encoding="utf-8",
    )
    mod = parse_typescript_file(ts_file, "flags.ts", is_test=False)
    scorer = UniversalIRScorer(RubricConfig(), TYPESCRIPT_PROFILE)
    r_opt = scorer.score_function(mod.functions[0], "flags.ts", is_test=False)
    r_def = scorer.score_function(mod.functions[1], "flags.ts", is_test=False)
    assert mod.functions[0].params[0].has_default is False
    assert r_opt.scores.srp == 100.0
    assert r_def.scores.srp == 94.0


def test_abstract_class_and_abstract_method_signatures(tmp_path: Path) -> None:
    ts_file = tmp_path / "worker.ts"
    ts_file.write_text(
        """/** Base worker. */
export abstract class Worker {
  protected count: number = 0;
  /** Run task. */
  abstract run(id: string): void;
  /** Increment counter. */
  public tick(): void { this.count += 1; }
  /** Reset counter. */
  public reset(): void { this.count = 0; }
}
""",
        encoding="utf-8",
    )
    mod = parse_typescript_file(ts_file, "worker.ts", is_test=False)
    cls = mod.classes[0]
    assert [m.qualname for m in cls.methods] == ["Worker.run", "Worker.tick", "Worker.reset"]
    assert cls.lcom4 == 1
    scorer = UniversalIRScorer(RubricConfig(), TYPESCRIPT_PROFILE)
    assert scorer.score_class(cls, "worker.ts", is_test=False).scores.clean == 100.0


def test_ctor_param_properties_cst_accuracy(tmp_path: Path) -> None:
    ts_file = tmp_path / "ctor.ts"
    ts_file.write_text(
        """/** Service. */
export class Service {
  /** Init. */
  constructor(
    public readonly count: number,
    private
    label: string,
    is_public = true
  ) {}
  /** Read a. */
  getCount(): number { return this.count; }
  /** Read b. */
  getLabel(): string { return this.label; }
  /** Pair. */
  summary(): string { return `${this.label}:${this.count}`; }
}
""",
        encoding="utf-8",
    )
    mod = parse_typescript_file(ts_file, "ctor.ts", is_test=False)
    field_names = {f.name for f in mod.classes[0].fields}
    assert field_names == {"count", "label"}
    assert "is_public" not in field_names
    assert mod.classes[0].lcom4 == 1


def test_exported_generator_and_field_ts_ignore(tmp_path: Path) -> None:
    (tmp_path / "gen.ts").write_text(
        """/** Exported generator. */
export function* ids(): Generator<number> { yield 1; }
/** Class with suppressed field. */
export class Holder {
  // @ts-ignore suppressing legacy type mismatch
  private raw: string = 123 as unknown as string;
  /** Get raw. */
  public getRaw(): string { return this.raw; }
}
""",
        encoding="utf-8",
    )
    report = CodeHealthRunner(repo_root=tmp_path, git_mode="no-git").run([tmp_path])
    f_rep = report.files[0]
    assert [fn.name for fn in f_rep.functions] == ["ids"]
    assert any("'@ts-ignore'/'@ts-nocheck'" in msg for msg in f_rep.findings)
    assert f_rep.scores.clean == 90.0


def test_empty_comment_only_and_cli_lang_ts_alias(capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    (tmp_path / "empty.ts").write_text("// License header only\n/* Copyright */\n", encoding="utf-8")
    (tmp_path / "mod.mts").write_text("/** Ping. */\nexport function ping(): string { return 'pong'; }\n", encoding="utf-8")
    (tmp_path / "ignored.py").write_text("def x(): pass\n", encoding="utf-8")
    (tmp_path / "coverage").mkdir()
    (tmp_path / "coverage" / "cov.ts").write_text("export var bad = 1;\n", encoding="utf-8")

    rc = code_health.main([str(tmp_path), "--no-git", "--format", "json", "--lang", "ts"])
    assert rc == 0
    data = json.loads(capsys.readouterr().out)
    names = sorted(Path(f["file_path"]).name for f in data["files"])
    assert names == ["empty.ts", "mod.mts"]
    assert all(f["scores"]["composite"] == 100.0 for f in data["files"])


def test_git_churn_ts_mts_cts_and_test_patterns() -> None:
    log_out = (
        "COMMIT:abc|dev|feat: update ts module\n"
        "src/app.ts\nsrc/types.d.ts\nsrc/widget.tsx\nsrc/mod.mts\nsrc/legacy.cts\n"
        "COMMIT:def|dev|fix: adjust app\nsrc/app.ts\n"
    )
    stats = _parse_git_log_output(log_out)
    assert stats["src/app.ts"].commits == 2
    assert stats["src/app.ts"].feat_commits == 1
    assert "src/types.d.ts" not in stats
    assert "src/mod.mts" in stats and "src/legacy.cts" in stats
    assert is_test_file_path("src/a_test.mts") is True and is_test_file_path("src/b_test.cts") is True
    assert TYPESCRIPT_PROFILE.is_test_assert_call("to.equal") is True


def test_async_arrow_generic_any_and_typed_var_arrow(tmp_path: Path) -> None:
    ts_file = tmp_path / "arrows.ts"
    ts_file.write_text(
        """const inc = async x => x + 1;
/** Generic identity. */
export function wrap<T extends any>(v: T): T { return v; }
/** Typed arrow variable. */
export const addFn: (a: number) => number = (a) => a + 1;
""",
        encoding="utf-8",
    )
    mod = parse_typescript_file(ts_file, "arrows.ts", is_test=False)
    scorer = UniversalIRScorer(RubricConfig(), TYPESCRIPT_PROFILE)
    r_inc = scorer.score_function(mod.functions[0], "arrows.ts", is_test=False)
    r_wrap = scorer.score_function(mod.functions[1], "arrows.ts", is_test=False)
    r_add = scorer.score_function(mod.functions[2], "arrows.ts", is_test=False)
    assert mod.functions[0].params[0].name == "x" and r_inc.scores.clean < 90.0
    assert mod.functions[1].explicit_any_count == 1 and r_wrap.scores.clean == 95.0
    assert r_add.scores.clean == 100.0


def test_minified_skip_stderr_notice(capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    (tmp_path / "bundle.min.ts").write_text("export const a=1;\n", encoding="utf-8")
    (tmp_path / "clean.ts").write_text("/** Ok. */\nexport function ok(): number { return 1; }\n", encoding="utf-8")
    rc = code_health.main([str(tmp_path), "--no-git", "--format", "json"])
    assert rc == 0
    cap = capsys.readouterr()
    assert "Skipped minified asset:" in cap.err and "bundle.min.ts" in cap.err
    assert json.loads(cap.out)["files_count"] == 1
