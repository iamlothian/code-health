from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import code_health as ch
from _code_health.models import RenderFilter, RubricConfig
from _code_health.reporting import CodeHealthRunner, ScorecardFormatter


def test_single_file_analyze_parity_and_cross_file_scorecards(tmp_path: Path, capsys) -> None:
    dup_body = "\n".join(f"    v{i} = items[{i}] * {i + 2}" for i in range(9))
    f1 = tmp_path / "src" / "a.py"
    f2 = tmp_path / "src" / "b.py"
    f1.parent.mkdir(parents=True)
    f1.write_text(
        '"""Module A."""\n\n'
        f'def fn1_alpha(items: list[int]) -> int:\n    """F1."""\n{dup_body}\n    return v8\n\n'
        f'def fn1_beta(items: list[int]) -> int:\n    """F2."""\n{dup_body}\n    return v8\n',
        encoding="utf-8",
    )
    f2.write_text(
        '"""Module B."""\n\n'
        f'def fn2_gamma(items: list[int]) -> int:\n    """F3."""\n{dup_body}\n    return v8\n',
        encoding="utf-8",
    )

    cfg = RubricConfig()
    solo = ch.analyze_file(f1, tmp_path, set(), cfg)
    batch_rep = CodeHealthRunner(tmp_path, cfg, git_mode="no-git").run([f1])
    batch = batch_rep.files[0]

    assert solo.scores == batch.scores
    assert solo.dry_score == batch.dry_score
    assert solo.duplicated_loc == batch.duplicated_loc
    assert solo.duplication_ratio == batch.duplication_ratio
    assert solo.duplicate_blocks == batch.duplicate_blocks
    assert solo.findings == batch.findings

    rep = CodeHealthRunner(tmp_path, cfg, git_mode="no-git").run([f1, f2])
    assert rep.dry.clone_groups_count >= 1
    assert rep.dry.cross_file_groups >= 1
    assert all(f.duplicated_loc > 0 and f.duplication_ratio > 0.0 and f.dry_score < 100.0 for f in rep.files)

    fmt = ScorecardFormatter(RenderFilter())
    console = fmt.render_console(rep)
    md = fmt.render_markdown(rep)
    assert "[DUPLICATE CODE & DRY SUMMARY]" in console
    assert "DRY-001" in console
    assert "## Duplicate Code & DRY Findings" in md
    assert "- **DRY / Duplication:**" in md

    rc = ch.main([str(f1.parent), "--no-git", "--format", "json"])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert payload["dry"]["clone_groups_count"] >= 1
    assert all("duplicated_loc" in item and "duplication_ratio" in item and "dry_score" in item for item in payload["files"])


def test_no_dry_flag_clean_console_custom_config_and_test_isolation(
    tmp_path: Path, capsys, monkeypatch: pytest.MonkeyPatch
) -> None:
    assert {"CloneGroup", "CloneLocation", "DrySummary"}.issubset(set(ch.__all__))

    dup_body = "\n".join(f"    step_{i} = payload[{i}] + {i + 1}" for i in range(9))
    src_file = tmp_path / "src" / "service.py"
    test_file = tmp_path / "tests" / "test_service.py"
    src_file.parent.mkdir(parents=True)
    test_file.parent.mkdir(parents=True)
    src_file.write_text(f'"""Svc."""\n\ndef run_a(payload):\n    """A."""\n{dup_body}\n    return step_8\n', encoding="utf-8")
    test_file.write_text(f'"""Test."""\n\ndef test_run_a(payload):\n{dup_body}\n    return step_8\n', encoding="utf-8")

    # src <-> tests partition isolation when both contain identical blocks.
    iso_rep = CodeHealthRunner(tmp_path, RubricConfig(), git_mode="no-git").run([src_file, test_file])
    assert iso_rep.dry.cross_file_groups == 0
    assert iso_rep.dry.clone_groups_count == 0
    fmt = ScorecardFormatter(RenderFilter())
    assert "[DUPLICATE CODE & DRY SUMMARY]" not in fmt.render_console(iso_rep)
    assert "## Duplicate Code & DRY Findings" not in fmt.render_markdown(iso_rep)

    # Plant cross-file src duplicate to verify --no-dry and config coercion.
    src_peer = tmp_path / "src" / "worker.py"
    src_peer.write_text(f'"""Wkr."""\n\ndef run_b(payload):\n    """B."""\n{dup_body}\n    return step_8\n', encoding="utf-8")

    no_dry_paths = ch.analyze_paths([src_file, src_peer], repo_root=tmp_path, use_git=False, use_dry=False)
    assert no_dry_paths.dry.clone_groups_count == 0
    assert all(f.dry_score == 100.0 and f.duplicated_loc == 0 for f in no_dry_paths.files)

    rc_no_dry = ch.main([str(src_file.parent), "--no-git", "--no-dry", "--format", "json"])
    payload_no_dry = json.loads(capsys.readouterr().out)
    assert rc_no_dry == 0
    assert payload_no_dry["dry"]["clone_groups_count"] == 0

    toml_cfg = tmp_path / "health.toml"
    toml_cfg.write_text('[tool.code_health]\ndry_exclude_globs = ["src/*.py"]\n', encoding="utf-8")
    loaded_toml = ch._load_custom_config(toml_cfg)
    assert isinstance(loaded_toml.dry_exclude_globs, tuple)
    assert loaded_toml.dry_exclude_globs == ("src/*.py",)

    json_cfg = tmp_path / "health.json"
    json_cfg.write_text(json.dumps({"dry_exclude_globs": ["worker.py"], "dry_min_tokens": 50}), encoding="utf-8")
    loaded_json = ch._load_custom_config(json_cfg)
    assert loaded_json.dry_exclude_globs == ("worker.py",)
    assert loaded_json.dry_min_tokens == 50

    monkeypatch.chdir(tmp_path)
    rc_cfg = ch.main([str(src_file.parent), "--no-git", "--config", str(toml_cfg), "--format", "json"])
    payload_cfg = json.loads(capsys.readouterr().out)
    assert rc_cfg == 0
    assert payload_cfg["dry"]["clone_groups_count"] == 0


def _build_polyglot_sources(ext: str) -> tuple[str, str, str, str]:
    """Build deterministic alpha/beta source modules with Type-1/2/3 and intra/cross clones."""
    if ext == ".py":
        alpha = '''"""Alpha Python module with intra-file Type-1, cross-file Type-1/2/3, and boilerplate."""


def guard_loop_alpha_one(limit: int, seed: int) -> int:
    """First intra-file Type-1 occurrence with repeated audit boilerplate."""
    acc = limit * 2 + seed
    idx = 0
    audit_trace("guard", "enter", limit)
    while idx < limit:
        step = (idx * 3 + acc) % 97
        if step > 10:
            acc = acc + step + 5
        audit_trace("guard", "step", step)
        idx = idx + 1
    audit_trace("guard", "exit", acc)
    return acc


def guard_loop_alpha_two(limit: int, seed: int) -> int:
    """Second intra-file Type-1 occurrence with identical body."""
    acc = limit * 2 + seed
    idx = 0
    audit_trace("guard", "enter", limit)
    while idx < limit:
        step = (idx * 3 + acc) % 97
        if step > 10:
            acc = acc + step + 5
        audit_trace("guard", "step", step)
        idx = idx + 1
    audit_trace("guard", "exit", acc)
    return acc


def sync_ledger_alpha(seed: int) -> int:
    """Cross-file Type-1 baseline with retry telemetry boilerplate."""
    retry = 0
    score = seed - 10
    emit_metric("ledger", "start", score)
    for slot in range(seed):
        delta = score - slot * 2
        if delta <= 0:
            retry = retry + 3
            score = score + 11
        emit_metric("ledger", "iter", retry)
    emit_metric("ledger", "done", score)
    return score - retry


def route_payload(items: list[int], weight: int) -> int:
    """Cross-file Type-2 baseline with distinct identifiers and literals."""
    bucket = weight * 13 + 7
    span = len(items)
    floor = bucket - 41
    ceil = bucket + 19
    if span > 3:
        tag = "alpha-low"
        floor = floor + items[0] * 3
    elif span == 3:
        tag = "alpha-mid"
        ceil = ceil + items[1] + 88
    else:
        tag = "alpha-high"
        bucket = bucket + floor + ceil
    record_alpha(tag, bucket + ceil)
    return bucket + floor - ceil


def reconcile_alpha(first_v: int, second_v: int, factor: int) -> int:
    """Cross-file Type-3 baseline segmented below Type-1/2 thresholds."""
    acc_a = (first_v << 2) + 9
    acc_b = (second_v >> 1) + 5
    acc_c = acc_a ^ acc_b
    mask_a = acc_c & 255
    mask_b = (mask_a * factor) + 12
    mask_c = (acc_b + factor) | 4
    total_x = mask_b + mask_c
    final_c = (total_x * 3) + factor
    return final_c + total_x
'''
        beta = '''"""Beta Python module completing cross-file Type-1, Type-2, and Type-3 pairs."""


def sync_ledger_beta(seed: int) -> int:
    """Cross-file Type-1 twin matching sync_ledger_alpha."""
    retry = 0
    score = seed - 10
    emit_metric("ledger", "start", score)
    for slot in range(seed):
        delta = score - slot * 2
        if delta <= 0:
            retry = retry + 3
            score = score + 11
        emit_metric("ledger", "iter", retry)
    emit_metric("ledger", "done", score)
    return score - retry


def dispatch_envelope(records: list[int], scale: int) -> int:
    """Cross-file Type-2 twin with renamed variables and modified literals."""
    slot = scale * 29 + 11
    width = len(records)
    lower = slot - 53
    upper = slot + 23
    if width > 6:
        label = "beta-low"
        lower = lower + records[2] * 6
    elif width == 6:
        label = "beta-mid"
        upper = upper + records[4] + 95
    else:
        label = "beta-high"
        slot = slot + lower + upper
    write_beta(label, slot + upper)
    return slot + lower - upper


def reconcile_beta(first_v: int, second_v: int, factor: int) -> int:
    """Cross-file Type-3 twin with three scattered 1-line gaps."""
    acc_a = (first_v << 2) + 9
    acc_b = (second_v >> 1) + 5
    chk_a = acc_a ^ 17
    acc_c = acc_a ^ acc_b
    mask_a = acc_c & 255
    chk_b = mask_a + 31
    mask_b = (mask_a * factor) + 12
    mask_c = (acc_b + factor) | 4
    chk_c = mask_c ^ 19
    total_x = mask_b + mask_c
    final_c = (total_x * 3) + factor
    return final_c + total_x
'''
        return ("alpha.py", alpha, "beta.py", beta)

    if ext == ".java":
        alpha = '''package com.example.dry;

/** Alpha Java service for DRY polyglot tests. */
public class AlphaService {
    /** First intra-file Type-1 occurrence. */
    public int guardLoopAlphaOne(int limit, int seed) {
        int acc = limit * 2 + seed;
        int idx = 0;
        auditTrace("guard", "enter", limit);
        while (idx < limit) {
            int step = (idx * 3 + acc) % 97;
            if (step > 10) {
                acc = acc + step + 5;
            }
            auditTrace("guard", "step", step);
            idx = idx + 1;
        }
        auditTrace("guard", "exit", acc);
        return acc;
    }

    /** Second intra-file Type-1 occurrence. */
    public int guardLoopAlphaTwo(int limit, int seed) {
        int acc = limit * 2 + seed;
        int idx = 0;
        auditTrace("guard", "enter", limit);
        while (idx < limit) {
            int step = (idx * 3 + acc) % 97;
            if (step > 10) {
                acc = acc + step + 5;
            }
            auditTrace("guard", "step", step);
            idx = idx + 1;
        }
        auditTrace("guard", "exit", acc);
        return acc;
    }

    /** Cross-file Type-1 baseline. */
    public int syncLedgerAlpha(int seed) {
        int retry = 0;
        int score = seed - 10;
        emitMetric("ledger", "start", score);
        for (int slot = 0; slot < seed; slot++) {
            int delta = score - slot * 2;
            if (delta <= 0) {
                retry = retry + 3;
                score = score + 11;
            }
            emitMetric("ledger", "iter", retry);
        }
        emitMetric("ledger", "done", score);
        return score - retry;
    }

    /** Cross-file Type-2 baseline. */
    public int routePayload(int[] items, int weight) {
        int bucket = weight * 13 + 7;
        int span = items.length;
        int floor = bucket - 41;
        int ceil = bucket + 19;
        if (span > 3) {
            String tag = "alpha-low";
            floor = floor + items[0] * 3;
            recordAlpha(tag, floor);
        } else if (span == 3) {
            String tag = "alpha-mid";
            ceil = ceil + items[1] + 88;
            recordAlpha(tag, ceil);
        } else {
            String tag = "alpha-high";
            bucket = bucket + floor + ceil;
            recordAlpha(tag, bucket);
        }
        return bucket + floor - ceil;
    }

    /** Cross-file Type-3 baseline. */
    public int reconcileAlpha(int firstV, int secondV, int factor) {
        int accA = (firstV << 2) + 9;
        int accB = (secondV >> 1) + 5;
        int accC = accA ^ accB;
        int maskA = accC & 255;
        int maskB = (maskA * factor) + 12;
        int maskC = (accB + factor) | 4;
        int totalX = maskB + maskC;
        int finalC = (totalX * 3) + factor;
        return finalC + totalX;
    }
}
'''
        beta = '''package com.example.dry;

/** Beta Java service completing cross-file clones. */
public class BetaService {
    /** Cross-file Type-1 twin. */
    public int syncLedgerBeta(int seed) {
        int retry = 0;
        int score = seed - 10;
        emitMetric("ledger", "start", score);
        for (int slot = 0; slot < seed; slot++) {
            int delta = score - slot * 2;
            if (delta <= 0) {
                retry = retry + 3;
                score = score + 11;
            }
            emitMetric("ledger", "iter", retry);
        }
        emitMetric("ledger", "done", score);
        return score - retry;
    }

    /** Cross-file Type-2 twin with renamed identifiers and literals. */
    public int dispatchEnvelope(int[] records, int scale) {
        int slot = scale * 29 + 11;
        int width = records.length;
        int lower = slot - 53;
        int upper = slot + 23;
        if (width > 6) {
            String label = "beta-low";
            lower = lower + records[2] * 6;
            writeBeta(label, lower);
        } else if (width == 6) {
            String label = "beta-mid";
            upper = upper + records[4] + 95;
            writeBeta(label, upper);
        } else {
            String label = "beta-high";
            slot = slot + lower + upper;
            writeBeta(label, slot);
        }
        return slot + lower - upper;
    }

    /** Cross-file Type-3 twin with three scattered 1-line gaps. */
    public int reconcileBeta(int firstV, int secondV, int factor) {
        int accA = (firstV << 2) + 9;
        int accB = (secondV >> 1) + 5;
        int chkA = accA ^ 17;
        int accC = accA ^ accB;
        int maskA = accC & 255;
        int chkB = maskA + 31;
        int maskB = (maskA * factor) + 12;
        int maskC = (accB + factor) | 4;
        int chkC = maskC ^ 19;
        int totalX = maskB + maskC;
        int finalC = (totalX * 3) + factor;
        return finalC + totalX;
    }
}
'''
        return ("AlphaService.java", alpha, "BetaService.java", beta)

    if ext == ".js":
        alpha = '''/** First intra-file Type-1 occurrence. */
export function guardLoopAlphaOne(limit, seed) {
  let acc = limit * 2 + seed;
  let idx = 0;
  auditTrace("guard", "enter", limit);
  while (idx < limit) {
    const step = (idx * 3 + acc) % 97;
    if (step > 10) {
      acc = acc + step + 5;
    }
    auditTrace("guard", "step", step);
    idx = idx + 1;
  }
  auditTrace("guard", "exit", acc);
  return acc;
}

/** Second intra-file Type-1 occurrence. */
export function guardLoopAlphaTwo(limit, seed) {
  let acc = limit * 2 + seed;
  let idx = 0;
  auditTrace("guard", "enter", limit);
  while (idx < limit) {
    const step = (idx * 3 + acc) % 97;
    if (step > 10) {
      acc = acc + step + 5;
    }
    auditTrace("guard", "step", step);
    idx = idx + 1;
  }
  auditTrace("guard", "exit", acc);
  return acc;
}

/** Cross-file Type-1 baseline. */
export function syncLedgerAlpha(seed) {
  let retry = 0;
  let score = seed - 10;
  emitMetric("ledger", "start", score);
  for (let slot = 0; slot < seed; slot++) {
    const delta = score - slot * 2;
    if (delta <= 0) {
      retry = retry + 3;
      score = score + 11;
    }
    emitMetric("ledger", "iter", retry);
  }
  emitMetric("ledger", "done", score);
  return score - retry;
}

/** Cross-file Type-2 baseline. */
export function routePayload(items, weight) {
  let bucket = weight * 13 + 7;
  const span = items.length;
  let floor = bucket - 41;
  let ceil = bucket + 19;
  if (span > 3) {
    const tag = "alpha-low";
    floor = floor + items[0] * 3;
    recordAlpha(tag, floor);
  } else if (span === 3) {
    const tag = "alpha-mid";
    ceil = ceil + items[1] + 88;
    recordAlpha(tag, ceil);
  } else {
    const tag = "alpha-high";
    bucket = bucket + floor + ceil;
    recordAlpha(tag, bucket);
  }
  return bucket + floor - ceil;
}

/** Cross-file Type-3 baseline. */
export function reconcileAlpha(firstV, secondV, factor) {
  const accA = (firstV << 2) + 9;
  const accB = (secondV >> 1) + 5;
  const accC = accA ^ accB;
  const maskA = accC & 255;
  const maskB = (maskA * factor) + 12;
  const maskC = (accB + factor) | 4;
  const totalX = maskB + maskC;
  const finalC = (totalX * 3) + factor;
  return finalC + totalX;
}
'''
        beta = '''/** Cross-file Type-1 twin. */
export function syncLedgerBeta(seed) {
  let retry = 0;
  let score = seed - 10;
  emitMetric("ledger", "start", score);
  for (let slot = 0; slot < seed; slot++) {
    const delta = score - slot * 2;
    if (delta <= 0) {
      retry = retry + 3;
      score = score + 11;
    }
    emitMetric("ledger", "iter", retry);
  }
  emitMetric("ledger", "done", score);
  return score - retry;
}

/** Cross-file Type-2 twin with renamed identifiers and literals. */
export function dispatchEnvelope(records, scale) {
  let slot = scale * 29 + 11;
  const width = records.length;
  let lower = slot - 53;
  let upper = slot + 23;
  if (width > 6) {
    const label = "beta-low";
    lower = lower + records[2] * 6;
    writeBeta(label, lower);
  } else if (width === 6) {
    const label = "beta-mid";
    upper = upper + records[4] + 95;
    writeBeta(label, upper);
  } else {
    const label = "beta-high";
    slot = slot + lower + upper;
    writeBeta(label, slot);
  }
  return slot + lower - upper;
}

/** Cross-file Type-3 twin with three scattered 1-line gaps. */
export function reconcileBeta(firstV, secondV, factor) {
  const accA = (firstV << 2) + 9;
  const accB = (secondV >> 1) + 5;
  const chkA = accA ^ 17;
  const accC = accA ^ accB;
  const maskA = accC & 255;
  const chkB = maskA + 31;
  const maskB = (maskA * factor) + 12;
  const maskC = (accB + factor) | 4;
  const chkC = maskC ^ 19;
  const totalX = maskB + maskC;
  const finalC = (totalX * 3) + factor;
  return finalC + totalX;
}
'''
        return ("alpha.js", alpha, "beta.js", beta)

    alpha = '''export interface MetricsNote {
  code: string;
}

/** First intra-file Type-1 occurrence. */
export function guardLoopAlphaOne(limit: number, seed: number): number {
  let acc = limit * 2 + seed;
  let idx = 0;
  auditTrace("guard", "enter", limit);
  while (idx < limit) {
    const step = (idx * 3 + acc) % 97;
    if (step > 10) {
      acc = acc + step + 5;
    }
    auditTrace("guard", "step", step);
    idx = idx + 1;
  }
  auditTrace("guard", "exit", acc);
  return acc;
}

/** Second intra-file Type-1 occurrence. */
export function guardLoopAlphaTwo(limit: number, seed: number): number {
  let acc = limit * 2 + seed;
  let idx = 0;
  auditTrace("guard", "enter", limit);
  while (idx < limit) {
    const step = (idx * 3 + acc) % 97;
    if (step > 10) {
      acc = acc + step + 5;
    }
    auditTrace("guard", "step", step);
    idx = idx + 1;
  }
  auditTrace("guard", "exit", acc);
  return acc;
}

/** Cross-file Type-1 baseline. */
export function syncLedgerAlpha(seed: number): number {
  let retry = 0;
  let score = seed - 10;
  emitMetric("ledger", "start", score);
  for (let slot = 0; slot < seed; slot++) {
    const delta = score - slot * 2;
    if (delta <= 0) {
      retry = retry + 3;
      score = score + 11;
    }
    emitMetric("ledger", "iter", retry);
  }
  emitMetric("ledger", "done", score);
  return score - retry;
}

/** Cross-file Type-2 baseline. */
export function routePayload(items: number[], weight: number): number {
  let bucket = weight * 13 + 7;
  const span = items.length;
  let floor = bucket - 41;
  let ceil = bucket + 19;
  if (span > 3) {
    const tag = "alpha-low";
    floor = floor + items[0] * 3;
    recordAlpha(tag, floor);
  } else if (span === 3) {
    const tag = "alpha-mid";
    ceil = ceil + items[1] + 88;
    recordAlpha(tag, ceil);
  } else {
    const tag = "alpha-high";
    bucket = bucket + floor + ceil;
    recordAlpha(tag, bucket);
  }
  return bucket + floor - ceil;
}

/** Cross-file Type-3 baseline. */
export function reconcileAlpha(firstV: number, secondV: number, factor: number): number {
  const accA = (firstV << 2) + 9;
  const accB = (secondV >> 1) + 5;
  const accC = accA ^ accB;
  const maskA = accC & 255;
  const maskB = (maskA * factor) + 12;
  const maskC = (accB + factor) | 4;
  const totalX = maskB + maskC;
  const finalC = (totalX * 3) + factor;
  return finalC + totalX;
}
'''
    beta = '''/** Cross-file Type-1 twin. */
export function syncLedgerBeta(seed: number): number {
  let retry = 0;
  let score = seed - 10;
  emitMetric("ledger", "start", score);
  for (let slot = 0; slot < seed; slot++) {
    const delta = score - slot * 2;
    if (delta <= 0) {
      retry = retry + 3;
      score = score + 11;
    }
    emitMetric("ledger", "iter", retry);
  }
  emitMetric("ledger", "done", score);
  return score - retry;
}

/** Cross-file Type-2 twin with renamed identifiers and literals. */
export function dispatchEnvelope(records: number[], scale: number): number {
  let slot = scale * 29 + 11;
  const width = records.length;
  let lower = slot - 53;
  let upper = slot + 23;
  if (width > 6) {
    const label = "beta-low";
    lower = lower + records[2] * 6;
    writeBeta(label, lower);
  } else if (width === 6) {
    const label = "beta-mid";
    upper = upper + records[4] + 95;
    writeBeta(label, upper);
  } else {
    const label = "beta-high";
    slot = slot + lower + upper;
    writeBeta(label, slot);
  }
  return slot + lower - upper;
}

/** Cross-file Type-3 twin with three scattered 1-line gaps. */
export function reconcileBeta(firstV: number, secondV: number, factor: number): number {
  const accA = (firstV << 2) + 9;
  const accB = (secondV >> 1) + 5;
  const chkA = accA ^ 17;
  const accC = accA ^ accB;
  const maskA = accC & 255;
  const chkB = maskA + 31;
  const maskB = (maskA * factor) + 12;
  const maskC = (accB + factor) | 4;
  const chkC = maskC ^ 19;
  const totalX = maskB + maskC;
  const finalC = (totalX * 3) + factor;
  return finalC + totalX;
}
'''
    return ("alpha.ts", alpha, "beta.ts", beta)


@pytest.mark.parametrize("ext", [".py", ".java", ".js", ".ts"])
def test_polyglot_type1_type2_type3_and_cross_cutting_boilerplate_detection(tmp_path: Path, ext: str) -> None:
    if ext == ".java":
        pytest.importorskip("tree_sitter_java")
    elif ext == ".js":
        pytest.importorskip("tree_sitter_javascript")
    elif ext == ".ts":
        pytest.importorskip("tree_sitter_typescript")

    src_dir = tmp_path / "src"
    src_dir.mkdir(parents=True)
    alpha_name, alpha_code, beta_name, beta_code = _build_polyglot_sources(ext)
    (src_dir / alpha_name).write_text(alpha_code, encoding="utf-8")
    (src_dir / beta_name).write_text(beta_code, encoding="utf-8")

    report = CodeHealthRunner(repo_root=tmp_path, git_mode="no-git").run([src_dir])

    assert report.files_count == 2
    assert report.dry.type1_groups >= 1
    assert report.dry.type2_groups >= 1
    assert report.dry.type3_groups >= 1
    assert report.dry.intra_file_groups >= 1
    assert report.dry.cross_file_groups >= 1
    assert all(len(g.occurrences) >= 2 for g in report.dry.clone_groups)


def test_polyglot_ecmascript_bucket_empty_init_and_broken_ts_resilience(tmp_path: Path) -> None:
    pytest.importorskip("tree_sitter_java")
    pytest.importorskip("tree_sitter_javascript")
    pytest.importorskip("tree_sitter_typescript")

    src_dir = tmp_path / "src"
    src_dir.mkdir(parents=True)

    # Empty package marker and syntax-invalid TypeScript file must never crash analysis
    (src_dir / "__init__.py").write_text("", encoding="utf-8")
    (src_dir / "broken.ts").write_text("export function brokenSyntax(x: number { if (x > 0 {{{ return ;; ", encoding="utf-8")
    (src_dir / "helper.py").write_text('"""Helper."""\n\n\ndef greet(name: str) -> str:\n    """Greet."""\n    return f"hi {name}"\n', encoding="utf-8")
    (src_dir / "Service.java").write_text(
        '/** Service. */\npublic class Service {\n    /** Compute. */\n    public int calc(int v) { return v + 1; }\n}\n',
        encoding="utf-8",
    )

    # Shared ecmascript bucket: .js and .tsx sharing identical algorithmic structure
    (src_dir / "cart_utils.js").write_text(
        '''/** Calculate adjusted basket score. */
export function normalizeBasketItems(rows, taxRate) {
  let acc = rows.length * 10 + taxRate;
  let idx = 0;
  auditCart("start", acc);
  while (idx < rows.length) {
    const val = (rows[idx] * 3 + acc) % 97;
    if (val > 12) {
      acc = acc + val + 7;
    }
    auditCart("row", val);
    idx = idx + 1;
  }
  auditCart("done", acc);
  return acc;
}
''',
        encoding="utf-8",
    )
    (src_dir / "CartPanel.tsx").write_text(
        '''/** Render summary and normalize order entries. */
export function CartBadge({ count }: { count: number }) {
  return <span>{count}</span>;
}

/** Twin algorithm inside .tsx to prove shared ecmascript JS<->TS detection. */
export function normalizeOrderItems(entries: number[], rate: number): number {
  let total = entries.length * 20 + rate;
  let cursor = 0;
  auditOrder("start", total);
  while (cursor < entries.length) {
    const itemVal = (entries[cursor] * 5 + total) % 83;
    if (itemVal > 18) {
      total = total + itemVal + 9;
    }
    auditOrder("row", itemVal);
    cursor = cursor + 1;
  }
  auditOrder("done", total);
  return total;
}
''',
        encoding="utf-8",
    )

    report = CodeHealthRunner(repo_root=tmp_path, git_mode="no-git").run([src_dir])

    file_scores = {Path(f.file_path).name: f.scores.composite for f in report.files}
    assert file_scores["__init__.py"] == 100.0
    assert "helper.py" in file_scores and "Service.java" in file_scores
    assert report.dry.clone_groups_count >= 1
    assert report.dry.cross_file_groups >= 1
    assert any(
        {Path(occ.file_path).suffix for occ in group.occurrences} == {".js", ".tsx"}
        for group in report.dry.clone_groups
    )


def test_determinism_and_100_file_memory_speed_budget(tmp_path: Path) -> None:
    import gc
    import time
    import tracemalloc
    from dataclasses import asdict

    assign_ops = ("=", "+=", "-=", "*=", "/=", "//=", "%=", "**=", "&=", "|=", "^=", ">>=", "<<=")
    bin_ops = ("+", "-", "*", "/", "//", "%", "**", "<<", ">>", "&", "|", "^", "@")

    def make_unique_fn(file_idx: int, fn_idx: int, pair_start: int) -> str:
        lines = [
            f"def compute_f{file_idx}_{fn_idx}(a: int, b: int) -> int:",
            '    """Generated unique benchmark function."""',
            "    x = a",
        ]
        for p in range(13):
            m = pair_start + p
            a0, b0 = assign_ops[m % 13], bin_ops[(m // 13) % 13]
            a1, b1 = assign_ops[(m // 169) % 13], bin_ops[(m // 2197) % 13]
            lines.append(f"    x {a0} a {b0} {p + 1}")
            lines.append(f"    x {a1} b {b1} a")
        lines.append("    return x")
        return "\n".join(lines)

    _, py_alpha, _, py_beta = _build_polyglot_sources(".py")
    planted_t1_a = "def sync_ledger_alpha" + py_alpha.split("def sync_ledger_alpha")[1].split("def route_payload")[0]
    planted_t1_b = "def sync_ledger_beta" + py_beta.split("def sync_ledger_beta")[1].split("def dispatch_envelope")[0]
    planted_t2_a = "def route_payload" + py_alpha.split("def route_payload")[1].split("def reconcile_alpha")[0]
    planted_t2_b = "def dispatch_envelope" + py_beta.split("def dispatch_envelope")[1].split("def reconcile_beta")[0]
    planted_t3_a = "def reconcile_alpha" + py_alpha.split("def reconcile_alpha")[1]
    planted_t3_b = "def reconcile_beta" + py_beta.split("def reconcile_beta")[1]
    planted_by_idx = {
        0: planted_t1_a,
        1: planted_t1_b,
        2: planted_t2_a,
        3: planted_t2_b,
        4: planted_t3_a,
        5: planted_t3_b,
    }

    corpus_dir = tmp_path / "src"
    corpus_dir.mkdir(parents=True)
    pair_cursor = 0
    for file_idx in range(100):
        parts = [f'"""Benchmark module {file_idx}."""']
        if file_idx in planted_by_idx:
            parts.append(planted_by_idx[file_idx].strip())
        for fn_idx in range(5):
            parts.append(make_unique_fn(file_idx, fn_idx, pair_cursor))
            pair_cursor += 13
        (corpus_dir / f"mod_{file_idx:03d}.py").write_text("\n\n\n".join(parts) + "\n", encoding="utf-8")

    t0 = time.perf_counter()
    rep1 = CodeHealthRunner(repo_root=tmp_path, git_mode="no-git").run([corpus_dir])
    elapsed = time.perf_counter() - t0

    gc.collect()
    tracemalloc.start()
    rep2 = CodeHealthRunner(repo_root=tmp_path, git_mode="no-git").run([corpus_dir])
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    assert rep1.files_count == 100
    assert rep1.dry.total_loc >= 14000
    assert rep1.dry.type1_groups >= 1
    assert rep1.dry.type2_groups >= 1
    assert rep1.dry.type3_groups >= 1
    assert elapsed < 2.5, f"100-file benchmark took {elapsed:.3f}s (budget < 2.5s)"
    assert peak_bytes < 25 * 1024 * 1024, f"Peak memory {peak_bytes / (1024 * 1024):.2f} MB (budget < 25 MB)"
    assert asdict(rep1) == asdict(rep2)


def test_skill_scripts_mirror_matches_repo_scripts_byte_for_byte() -> None:
    repo = Path(__file__).resolve().parents[2]
    src_root = repo / "scripts"
    dst_root = repo / "skills" / "code-health" / "scripts"
    src_files = {p.relative_to(src_root).as_posix(): p.read_bytes() for p in sorted(src_root.rglob("*.py"))}
    dst_files = {p.relative_to(dst_root).as_posix(): p.read_bytes() for p in sorted(dst_root.rglob("*.py"))}
    assert src_files == dst_files
