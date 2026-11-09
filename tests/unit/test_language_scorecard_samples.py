"""Automated baseline verification for multi-language good and bad code health samples."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
import sys
from typing import Any

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCRIPTS_DIR = str(_REPO_ROOT / "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from _code_health.models import RenderFilter, RubricConfig  # noqa: E402
from _code_health.reporting import CodeHealthRunner, ScorecardFormatter  # noqa: E402

_MANIFEST_PATH = _REPO_ROOT / "samples" / "manifest.json"


def _load_manifest_samples() -> list[dict[str, Any]]:
    """Load all sample definitions from samples/manifest.json."""
    data = json.loads(_MANIFEST_PATH.read_text(encoding="utf-8"))
    return list(data["samples"])


def _load_scenario_pairs() -> list[tuple[str, dict[str, Any], dict[str, Any]]]:
    """Group manifest samples into (pair_id, good_entry, bad_entry) tuples."""
    by_pair: dict[str, dict[str, dict[str, Any]]] = {}
    for entry in _load_manifest_samples():
        by_pair.setdefault(entry["pair_id"], {})[entry["quality"]] = entry
    return [(pid, pair["good"], pair["bad"]) for pid, pair in by_pair.items()]


def _collect_all_findings(file_rep: Any) -> list[str]:
    """Collect module, class, method, and function findings for a FileReport."""
    items = list(file_rep.findings)
    for cls in file_rep.classes:
        items.extend(f"[Class {cls.name}] {x}" for x in cls.findings)
        for method in cls.methods:
            items.extend(f"[Method {method.qualname}] {x}" for x in method.findings)
    for func in file_rep.functions:
        items.extend(f"[Func {func.qualname}] {x}" for x in func.findings)
    return items


def _run_sample_analysis(entry: dict[str, Any]) -> tuple[Any, str]:
    """Execute CodeHealthRunner on a single sample entry and return (FileReport, console_text)."""
    if entry["language"] == "java":
        pytest.importorskip("tree_sitter_java")
    fw = None if entry["framework"] == "auto" else entry["framework"]
    runner = CodeHealthRunner(
        repo_root=_REPO_ROOT,
        config=RubricConfig(),
        git_mode="no-git",
        lang_override=entry["language"],
        framework_override=fw,
    )
    sample_file = _REPO_ROOT / entry["file_path"]
    report = runner.run([sample_file])
    console = ScorecardFormatter(RenderFilter(show_all_funcs=True)).render_console(report)
    return report.files[0], console


def test_samples_manifest_and_catalog_exist() -> None:
    """Verify the top-level samples manifest and human-readable baseline catalog exist."""
    catalog_path = _REPO_ROOT / "samples" / "SCORECARD_BASELINES.md"
    assert _MANIFEST_PATH.is_file()
    assert catalog_path.is_file()
    samples = _load_manifest_samples()
    assert len(samples) == 20
    catalog_text = catalog_path.read_text(encoding="utf-8")
    assert "# Multi-Language Code Health Scorecard Baselines" in catalog_text


@pytest.mark.parametrize("entry", _load_manifest_samples(), ids=lambda e: e["id"])
def test_sample_file_matches_expected_scorecard_baseline(entry: dict[str, Any]) -> None:
    """Verify each sample file matches its sidecar .expected.json and deterministic scorecard."""
    sample_file = _REPO_ROOT / entry["file_path"]
    sidecar_file = sample_file.with_name(sample_file.name + ".expected.json")
    assert sample_file.is_file()
    assert sidecar_file.is_file()

    sidecar_data = json.loads(sidecar_file.read_text(encoding="utf-8"))
    assert sidecar_data["expected"]["scores"] == entry["expected"]["scores"]

    file_rep, console = _run_sample_analysis(entry)
    assert file_rep.loc == entry["expected"]["loc"]
    assert asdict(file_rep.scores) == entry["expected"]["scores"]
    assert console == entry["expected"]["rendered_console"]


@pytest.mark.parametrize("entry", _load_manifest_samples(), ids=lambda e: e["id"])
def test_sample_file_triggers_expected_findings(entry: dict[str, Any]) -> None:
    """Verify bad samples trigger required findings and 100-score good samples have none."""
    file_rep, _ = _run_sample_analysis(entry)
    findings = _collect_all_findings(file_rep)
    joined = "\n".join(findings)
    for req in entry["expected"]["required_findings"]:
        assert req in joined
    if entry["expected"]["scores"]["composite"] == 100.0:
        assert findings == []


@pytest.mark.parametrize(
    ("pair_id", "good_entry", "bad_entry"),
    _load_scenario_pairs(),
    ids=lambda val: val if isinstance(val, str) else "",
)
def test_good_sample_strictly_outscores_bad_sample_in_each_scenario(
    pair_id: str, good_entry: dict[str, Any], bad_entry: dict[str, Any]
) -> None:
    """Verify the good baseline sample strictly beats the bad sample on composite and target dimension."""
    good_rep, _ = _run_sample_analysis(good_entry)
    bad_rep, _ = _run_sample_analysis(bad_entry)
    target_dim = good_entry["target_dimension"]

    assert pair_id == bad_entry["pair_id"]
    assert good_rep.scores.composite > bad_rep.scores.composite
    assert getattr(good_rep.scores, target_dim) > getattr(bad_rep.scores, target_dim)
    assert good_rep.scores.grade == "A"
    assert bad_rep.scores.grade in {"C", "D", "F"}
    assert bad_rep.scores.composite < 80.0
