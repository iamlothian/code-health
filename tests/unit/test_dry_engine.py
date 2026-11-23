from __future__ import annotations

import ast
import sys
import time
from array import array
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from _code_health.dry_models import (
    BlockSpan,
    FileDryMetrics,
    FileTokenStream,
    PyTokenMeta,
    RawCloneMatch,
)
from _code_health.dry_scoring import apply_dry_metrics, cluster_and_score_clones
from _code_health.dry_tokens import (
    KIND_IDENT,
    KIND_LITERAL,
    KIND_STRUCT,
    TOK_ID,
    TOK_NUM,
    TokenInterner,
    extract_python_tokens,
)
from _code_health.dry_engine import (
    DryAnalyzer,
    PyTokenMeta as FacadePyTokenMeta,
    TokenInterner as FacadeTokenInterner,
    apply_dry_metrics as facade_apply_dry_metrics,
    extract_python_tokens as facade_extract_python_tokens,
)
from _code_health.dry_type3 import detect_block_type3_clones
from _code_health.models import (
    DimensionScores,
    FileReport,
    GitFileStats,
    RubricConfig,
)


def _make_stream(
    file_path: str,
    length: int = 80,
    *,
    is_test: bool = False,
    language: str = "python",
    loc: int | None = None,
) -> FileTokenStream:
    file_loc = loc if loc is not None else max(10, (length // 4) + 1)
    exact = array("I", [100 + (i % 13) for i in range(length)])
    norm = array("I", [100 + (i % 13) for i in range(length)])
    lines = array("I", [1 + (i // 4) for i in range(length)])
    kinds = array("B", [KIND_IDENT if i % 3 == 1 else KIND_STRUCT for i in range(length)])
    stmts = array("I", list(range(0, length, 8)))
    blocks = (
        BlockSpan(
            symbol="process_batch",
            start_tok=0,
            end_tok=length,
            start_line=1,
            end_line=int(lines[-1]),
            loc=file_loc,
            stmt_count=len(stmts),
        ),
    )
    return FileTokenStream(
        file_path=file_path,
        language=language,
        is_test=is_test,
        loc=file_loc,
        exact_ids=exact,
        norm_ids=norm,
        lines=lines,
        tok_kinds=kinds,
        stmt_starts=stmts,
        blocks=blocks,
    )


def _make_clean_report(file_path: str, *, is_test: bool = False, loc: int = 40) -> FileReport:
    cfg = RubricConfig()
    return FileReport(
        file_path=file_path,
        is_test=is_test,
        loc=loc,
        internal_imports=1,
        duplicate_blocks=0,
        mid_file_imports=0,
        git=GitFileStats(),
        scores=DimensionScores.from_raw((100.0, 100.0, 100.0, 100.0, 100.0), cfg),
    )


def _py_stream(path: str, src: str, symbol: str = "fn", *, is_test: bool = False) -> FileTokenStream:
    interner = _py_stream._interner
    lines = src.splitlines()
    loc = len(lines)
    meta = PyTokenMeta(
        rel_path=path,
        is_test=is_test,
        loc=loc,
        block_bounds=((symbol, 1, loc, loc),),
    )
    stream = extract_python_tokens(ast.parse(src), src, meta, interner)
    assert stream is not None
    return stream


_py_stream._interner = TokenInterner()


def test_cluster_union_find_subsumption_and_interval_merge() -> None:
    cfg = RubricConfig()
    streams = [
        _make_stream("src/a.py", length=80, loc=20),
        _make_stream("src/b.py", length=80, loc=20),
        _make_stream("src/c.py", length=80, loc=20),
    ]
    # Type-1 between a and b, overlapping Type-3 on same pair (must be subsumed),
    # plus Type-2 linking b and c -> consolidates {a, b, c} into DRY-001.
    matches = [
        RawCloneMatch(0, 0, 40, 1, 0, 40, "type1", 1.0),
        RawCloneMatch(0, 2, 38, 1, 2, 38, "type3", 0.85),
        RawCloneMatch(1, 0, 40, 2, 0, 40, "type2", 1.0),
        # Overlapping match within a and b lines to verify interval-merged duplicated_loc <= loc.
        RawCloneMatch(0, 20, 76, 1, 20, 76, "type1", 1.0),
    ]

    per_file, summary = cluster_and_score_clones(streams, matches, cfg)

    assert summary.clone_groups_count >= 1
    first = summary.clone_groups[0]
    assert first.group_id == "DRY-001"
    assert first.scope == "cross_file"
    assert len(first.occurrences) == 3
    assert {occ.file_path for occ in first.occurrences} == {"src/a.py", "src/b.py", "src/c.py"}
    assert all(occ.symbol == "process_batch" for occ in first.occurrences)

    for path in ("src/a.py", "src/b.py", "src/c.py"):
        fdm = per_file[path]
        assert fdm.duplicated_loc <= 20
        assert 0.0 <= fdm.duplication_ratio <= 100.0
    # Subsumed Type-3 overlap between a and b must not inflate summary type3 count.
    assert summary.type3_groups == 0


def test_severity_weights_worst_dimension_ceiling_and_test_cap() -> None:
    cfg = RubricConfig()
    src_s = _make_stream("src/heavy.py", length=80, loc=25)
    src_p = _make_stream("src/peer.py", length=80, loc=25)

    # Compare single duplicate block severity weights: type1 (-5) vs type2 (-4) vs type3 (-3).
    p_t1, _ = cluster_and_score_clones(
        [_make_stream("src/s1.py", 60, loc=100), _make_stream("src/s2.py", 60, loc=100)],
        [RawCloneMatch(0, 0, 40, 1, 0, 40, "type1", 1.0)],
        cfg,
    )
    p_t2, _ = cluster_and_score_clones(
        [_make_stream("src/s1.py", 60, loc=100), _make_stream("src/s2.py", 60, loc=100)],
        [RawCloneMatch(0, 0, 40, 1, 0, 40, "type2", 1.0)],
        cfg,
    )
    p_t3, _ = cluster_and_score_clones(
        [_make_stream("src/s1.py", 60, loc=100), _make_stream("src/s2.py", 60, loc=100)],
        [RawCloneMatch(0, 0, 40, 1, 0, 40, "type3", 0.80)],
        cfg,
    )
    assert p_t1["src/s1.py"].dry_penalty == pytest.approx(5.0)
    assert p_t2["src/s1.py"].dry_penalty == pytest.approx(4.0)
    assert p_t3["src/s1.py"].dry_penalty == pytest.approx(3.0)

    # Heavy duplication pushes Clean Code < 75.0 -> triggers worst-dimension composite ceiling <= 79.5.
    heavy_matches = [RawCloneMatch(0, 0, 80, 1, 0, 80, "type1", 1.0)]
    heavy_dry, _ = cluster_and_score_clones([src_s, src_p], heavy_matches, cfg)
    assert heavy_dry["src/heavy.py"].dry_penalty == pytest.approx(35.0)
    updated_src = apply_dry_metrics(_make_clean_report("src/heavy.py", loc=25), heavy_dry["src/heavy.py"], cfg)
    assert updated_src.scores.clean < 75.0
    assert updated_src.scores.composite <= 79.5

    # Test files cap DRY penalty at 25.0 pts instead of 35.0 pts.
    test_a = _make_stream("tests/test_a.py", length=120, is_test=True, loc=30)
    test_b = _make_stream("tests/test_b.py", length=120, is_test=True, loc=30)
    test_dry, _ = cluster_and_score_clones(
        [test_a, test_b],
        [RawCloneMatch(0, 0, 120, 1, 0, 120, "type1", 1.0)],
        cfg,
    )
    assert test_dry["tests/test_a.py"].dry_penalty == pytest.approx(25.0)
    updated_test = apply_dry_metrics(
        _make_clean_report("tests/test_a.py", is_test=True, loc=30),
        test_dry["tests/test_a.py"],
        cfg,
    )
    assert updated_test.scores.clean == pytest.approx(75.0)


def test_winnowing_type1_and_type2_detection_across_files() -> None:
    cfg = RubricConfig()
    analyzer = DryAnalyzer(cfg)
    _py_stream._interner = TokenInterner()

    src_a = '''
def sync_orders(orders, client, repo):
    """Sync orders with upstream retry handling."""
    synced = []
    # Fetch pending batch
    for order in orders:
        if order.status == "pending" and order.total > 0:
            payload = {"id": order.id, "total": order.total}
            response = client.send(payload)
            repo.save(response)
            synced.append(order.id)
    return synced
'''
    src_b_type1 = '''
def sync_orders(orders, client, repo):
    """Different docstring that must be ignored for Type-1."""
    synced = []
    # Totally different comment
    for order in orders:
        if order.status == "pending" and order.total > 0:
            payload = {"id": order.id, "total": order.total}
            response = client.send(payload)
            repo.save(response)
            synced.append(order.id)
    return synced
'''
    src_c_type2 = '''
def sync_invoices(invoices, gateway, store):
    exported = []
    for invoice in invoices:
        if invoice.status == "queued" and invoice.total > 10:
            body = {"id": invoice.id, "total": invoice.total}
            reply = gateway.send(body)
            store.save(reply)
            exported.append(invoice.id)
    return exported
'''

    streams = [
        _py_stream("src/a.py", src_a, "sync_orders"),
        _py_stream("src/b.py", src_b_type1, "sync_orders"),
        _py_stream("src/c.py", src_c_type2, "sync_invoices"),
    ]
    per_file, summary = analyzer.analyze(streams)

    assert summary.clone_groups_count == 1
    group = summary.clone_groups[0]
    assert group.group_id == "DRY-001"
    assert len(group.occurrences) == 3
    assert any("DRY-001" in f and f.startswith("Clean (DRY):") for f in per_file["src/a.py"].findings)


def test_type2_rejects_non_bijective_identifier_collision() -> None:
    cfg = RubricConfig()
    analyzer = DryAnalyzer(cfg)

    # Identical structural normalized tokens (len=42), but stream_b collapses
    # two distinct identifiers (var_x=501, var_y=502) into a single identifier (601, 601).
    def _build_bijection_probe(path: str, ident_pair: tuple[int, int]) -> FileTokenStream:
        pattern_norm = [10, TOK_ID, 11, TOK_ID, 12, TOK_NUM] * 7  # 42 tokens
        pattern_kinds = [KIND_STRUCT, KIND_IDENT, KIND_STRUCT, KIND_IDENT, KIND_STRUCT, KIND_LITERAL] * 7
        exact = []
        for idx, k in enumerate(pattern_kinds):
            if k == KIND_IDENT:
                exact.append(ident_pair[0] if (idx % 6 == 1) else ident_pair[1])
            elif k == KIND_LITERAL:
                exact.append(900)
            else:
                exact.append(pattern_norm[idx])
        lines = array("I", [1 + (i // 6) for i in range(len(pattern_norm))])
        return FileTokenStream(
            file_path=path,
            language="python",
            is_test=False,
            loc=8,
            exact_ids=array("I", exact),
            norm_ids=array("I", pattern_norm),
            lines=lines,
            tok_kinds=array("B", pattern_kinds),
            stmt_starts=array("I", list(range(0, 42, 6))),
            blocks=(BlockSpan("probe", 0, 42, 1, 7, 7, 7),),
        )

    s_a = _build_bijection_probe("src/alpha.py", (501, 502))
    s_b = _build_bijection_probe("src/beta.py", (601, 601))
    _, summary = analyzer.analyze([s_a, s_b])

    assert summary.type1_groups == 0
    assert summary.type2_groups == 0


def test_triple_back_to_back_intra_file_clones_and_pathological_85_branches() -> None:
    cfg = RubricConfig()
    analyzer = DryAnalyzer(cfg)
    _py_stream._interner = TokenInterner()

    fn_block = (
        "    total = base_val * item.tax_rate\n"
        "    adjusted = total - discount.amount\n"
        "    if adjusted > threshold and item.active:\n"
        "        audit.record(item.id, adjusted, 'ok')\n"
        "        cache[item.key] = adjusted\n"
        "        ledger.append((item.key, adjusted))\n"
        "    return cache.get(item.key, 0)\n\n"
    )
    multi_fn_src = (
        "def run_first(item, base_val, discount, threshold, audit, cache, ledger):\n" + fn_block
        + "def run_second(item, base_val, discount, threshold, audit, cache, ledger):\n" + fn_block
        + "def run_third(item, base_val, discount, threshold, audit, cache, ledger):\n" + fn_block
    )
    lines = multi_fn_src.splitlines()
    blocks = (
        BlockSpan("run_first", 0, 0, 1, 9, 9, 7),
        BlockSpan("run_second", 0, 0, 10, 18, 9, 7),
        BlockSpan("run_third", 0, 0, 19, 27, 9, 7),
    )
    s_triple = extract_python_tokens(
        ast.parse(multi_fn_src),
        multi_fn_src,
        PyTokenMeta(
            rel_path="src/triple.py",
            is_test=False,
            loc=len(lines),
            block_bounds=tuple((b.symbol, b.start_line, b.end_line, b.loc) for b in blocks),
        ),
        _py_stream._interner,
    )
    assert s_triple is not None
    per_file, summary = analyzer.analyze([s_triple])

    assert summary.clone_groups_count == 1
    grp = summary.clone_groups[0]
    assert len(grp.occurrences) == 3
    assert per_file["src/triple.py"].duplicate_blocks == 2
    assert per_file["src/triple.py"].duplicated_loc <= len(lines)

    # Pathological 85-branch file must complete < 0.5s under MAX_BUCKET=64.
    branches = []
    for idx in range(85):
        kw = "if" if idx == 0 else "elif"
        branches.append(
            f"    {kw} code == {idx}:\n"
            "        record.status = 'matched'\n"
            "        record.score = base_score + bonus\n"
            "        registry.emit(record.id, record.status, record.score)\n"
            "        metrics.increment(record.category, 1)\n"
            "        return record.score\n"
        )
    patho_src = "def dispatch_many(code, record, base_score, bonus, registry, metrics):\n" + "".join(branches)
    patho_meta = PyTokenMeta("src/patho.py", False, len(patho_src.splitlines()), (("dispatch_many", 1, len(patho_src.splitlines()), len(patho_src.splitlines())),))
    s_patho = extract_python_tokens(ast.parse(patho_src), patho_src, patho_meta, _py_stream._interner)
    assert s_patho is not None

    t0 = time.perf_counter()
    patho_files, _ = analyzer.analyze([s_patho])
    elapsed = time.perf_counter() - t0
    assert elapsed < 0.5
    assert "src/patho.py" in patho_files


def test_partition_isolation_ecmascript_bucket_and_facade() -> None:
    assert FacadePyTokenMeta is PyTokenMeta
    assert FacadeTokenInterner is TokenInterner
    assert facade_apply_dry_metrics is apply_dry_metrics
    assert facade_extract_python_tokens is extract_python_tokens

    cfg = RubricConfig()
    analyzer = DryAnalyzer(cfg)
    streams = [
        _make_stream("src/view.jsx", length=50, language="jsx", loc=15),
        _make_stream("src/view.tsx", length=50, language="tsx", loc=15),
        _make_stream("src/Service.java", length=50, language="java", loc=15),
        _make_stream("tests/view.spec.tsx", length=50, is_test=True, language="tsx", loc=15),
    ]
    per_file, summary = analyzer.analyze(streams)

    assert summary.clone_groups_count == 1
    peers = {occ.file_path for occ in summary.clone_groups[0].occurrences}
    assert peers == {"src/view.jsx", "src/view.tsx"}
    assert per_file["src/Service.java"].duplicate_blocks == 0
    assert per_file["tests/view.spec.tsx"].duplicate_blocks == 0


def test_detect_block_type3_scattered_edits_collapse_and_coverage_skip() -> None:
    cfg = RubricConfig()
    _py_stream._interner = TokenInterner()

    fn1 = (
        "def process_a(items):\n"
        + "\n".join(f"    v{i} = items[{i}] * {i + 1}" for i in range(12))
        + "\n    return v11\n"
    )
    # Scattered edits: inserted validation/audit statements + renamed locals (~85% similarity >= 0.70).
    fn2_lines = (
        ["def process_b(records):"]
        + [f"    r{i} = records[{i}] * {i + 1}" for i in range(5)]
        + ["    audit_log(r4)", "    flag = len(records)"]
        + [f"    r{i} = records[{i}] * {i + 1}" for i in range(5, 12)]
        + ["    return r11"]
    )
    fn2 = "\n".join(fn2_lines) + "\n"
    fn3_unrelated = (
        "def unrelated_calc(threshold):\n"
        + "\n".join(f"    if threshold > {i}:\n        dispatch_step({i}, threshold + 2)" for i in range(6))
        + "\n    return threshold\n"
    )

    s1 = _py_stream("src/p1.py", fn1, "process_a")
    s2 = _py_stream("src/p2.py", fn2, "process_b")
    s3 = _py_stream("src/p3.py", fn3_unrelated, "unrelated_calc")

    matches = detect_block_type3_clones([s1, s2, s3], [], cfg)
    assert len(matches) == 1
    assert matches[0].clone_type == "type3"
    assert matches[0].similarity >= 0.70
    assert (matches[0].file_a, matches[0].file_b) == (0, 1)

    # Already covered >= 75% by an existing stronger match must be skipped.
    existing = [RawCloneMatch(0, 0, len(s1.exact_ids), 1, 0, len(s2.exact_ids), "type2", 1.0)]
    assert detect_block_type3_clones([s1, s2, s3], existing, cfg) == []

    # Language & test isolation: test stream never compares against src stream; ECMAScript bucket matches JS/TS only.
    s2_test = _py_stream("tests/test_p2.py", fn2, "process_b", is_test=True)
    assert detect_block_type3_clones([s1, s2_test], [], cfg) == []

    # Identical shingle-set collapse: 3 blocks with identical 3-gram shingle sets still expand cleanly to all 3 pairs.
    rep1 = _py_stream("src/rep1.py", fn1, "process_a")
    rep2 = _py_stream("src/rep2.py", fn1, "process_a")
    rep3 = _py_stream("src/rep3.py", fn1, "process_a")
    rep_matches = detect_block_type3_clones([rep1, rep2, rep3], [], cfg)
    assert {(m.file_a, m.file_b) for m in rep_matches} == {(0, 1), (0, 2), (1, 2)}


def test_stage3a_gap_stitching_boilerplate_and_non_executable_exclusions(tmp_path: Path) -> None:
    cfg = RubricConfig()
    analyzer = DryAnalyzer(cfg)
    _py_stream._interner = TokenInterner()

    # Stage 3A test with blocks=() so ONLY contiguous gap-stitching can match the split seeds:
    # head (27 tokens >= K+W-1=25, < 35) + 6-token middle gap (<= 12) + tail (26 tokens >= 25, < 35).
    mod_a = (
        "step_1 = payload.get('user_id').strip()\n"
        "step_2 = payload.get('tenant_id')\n"
        "step_3 = step_1.strip().lower()\n"
        "step_4 = step_2.strip().upper()\n"
        "step_5 = validator.check(step_3, step_4)\n"
        "step_6 = mapper.bind(step_5, 42)\n"
    )
    mod_b = (
        "k1 = req.get('user_id').strip()\n"
        "k2 = req.get('tenant_id')\n"
        "k3 = k1.strip().lower()\n"
        "metrics.bump(k3)\n"
        "k4 = k2.strip().upper()\n"
        "k5 = verifier.check(k3, k4)\n"
        "k6 = binder.bind(k5, 99)\n"
    )
    sa = extract_python_tokens(
        ast.parse(mod_a),
        mod_a,
        PyTokenMeta("src/mod_a.py", False, len(mod_a.splitlines()), ()),
        _py_stream._interner,
    )
    sb = extract_python_tokens(
        ast.parse(mod_b),
        mod_b,
        PyTokenMeta("src/mod_b.py", False, len(mod_b.splitlines()), ()),
        _py_stream._interner,
    )
    assert sa is not None and sb is not None
    per_file_gapped, summary_gapped = analyzer.analyze([sa, sb])
    assert summary_gapped.clone_groups_count == 1
    assert summary_gapped.type3_groups == 1
    assert 0.70 <= summary_gapped.clone_groups[0].similarity < 1.0
    assert per_file_gapped["src/mod_a.py"].duplicate_blocks == 1

    # Aggressive boilerplate / cross-cutting concern detection at >= 35 tokens and >= 5 lines.
    guard_a = (
        "def create_order(ctx, payload, repo):\n"
        "    if not ctx.authenticated or ctx.actor is None:\n"
        "        raise PermissionError('unauthenticated')\n"
        "    if not ctx.has_scope('orders:write'):\n"
        "        raise PermissionError('missing scope')\n"
        "    audit.record(ctx.actor, 'orders:write', payload.id)\n"
        "    return repo.insert(payload)\n"
    )
    guard_b = (
        "def delete_invoice(session, cmd, store):\n"
        "    if not session.authenticated or session.actor is None:\n"
        "        raise PermissionError('unauthenticated')\n"
        "    if not session.has_scope('invoices:write'):\n"
        "        raise PermissionError('missing scope')\n"
        "    audit.record(session.actor, 'invoices:write', cmd.id)\n"
        "    return store.remove(cmd)\n"
    )
    _, summary_guard = analyzer.analyze([
        _py_stream("src/orders.py", guard_a, "create_order"),
        _py_stream("src/invoices.py", guard_b, "delete_invoice"),
    ])
    assert summary_guard.clone_groups_count == 1

    # Non-executable declarations only (Python imports/comments/docstrings, TS interface/type decls) yield 0 clones.
    decl_py_1 = (
        '"""Module docstring repeated verbatim."""\n'
        "import os\nimport sys\nfrom pathlib import Path\nfrom dataclasses import dataclass\n"
        "from typing import Any, Dict, List, Optional, Tuple\n# repeated comment header\n"
    )
    decl_py_2 = decl_py_1
    sp1 = extract_python_tokens(
        ast.parse(decl_py_1), decl_py_1, PyTokenMeta("src/d1.py", False, 7, ()), _py_stream._interner
    )
    sp2 = extract_python_tokens(
        ast.parse(decl_py_2), decl_py_2, PyTokenMeta("src/d2.py", False, 7, ()), _py_stream._interner
    )
    decl_streams = [s for s in (sp1, sp2) if s is not None]
    try:
        from _code_health.ts_parser import parse_typescript_file

        ts_decl = (
            "export interface OrderPayload {\n"
            "  readonly orderId: string;\n  readonly customerId: string;\n"
            "  readonly totalCents: number;\n  readonly currencyCode: string;\n"
            "  readonly tags: readonly string[];\n}\n"
            "export type AuditStatus = 'pending' | 'approved' | 'rejected';\n"
        )
        p_t1 = tmp_path / "types_a.ts"
        p_t2 = tmp_path / "types_b.ts"
        p_t1.write_text(ts_decl, encoding="utf-8")
        p_t2.write_text(ts_decl, encoding="utf-8")
        ir1 = parse_typescript_file(p_t1, "types_a.ts", False, interner=_py_stream._interner)
        ir2 = parse_typescript_file(p_t2, "types_b.ts", False, interner=_py_stream._interner)
        if ir1.token_stream is not None:
            decl_streams.append(ir1.token_stream)
        if ir2.token_stream is not None:
            decl_streams.append(ir2.token_stream)
    except ImportError:
        pass

    _, decl_summary = analyzer.analyze(decl_streams)
    assert decl_summary.clone_groups_count == 0


def test_review_fixes_subsumption_intra_method_and_dry_score_contracts() -> None:
    cfg = RubricConfig()
    # 1. Larger type2 clone containing a small type1 sub-span must NOT be dropped by _is_pair_contained.
    s1 = _make_stream("src/a.py", length=100, loc=40)
    s2 = _make_stream("src/b.py", length=100, loc=40)
    matches = [
        RawCloneMatch(0, 0, 36, 1, 0, 36, "type1", 1.0),
        RawCloneMatch(0, 0, 100, 1, 0, 100, "type2", 1.0),
    ]
    per_file, summary = cluster_and_score_clones([s1, s2], matches, cfg)
    assert {g.clone_type for g in summary.clone_groups} == {"type1", "type2"}

    # Verify per-file dry_score == clamp(100 - dry_penalty), weighted summary dry_score, (-pts) & ratio finding.
    m_a = per_file["src/a.py"]
    assert m_a.dry_score == round(100.0 - m_a.dry_penalty, 1)
    assert summary.dry_score == m_a.dry_score
    assert any("pts)" in f for f in m_a.findings)
    assert any("duplication_ratio=" in f for f in m_a.findings)

    # 2. Two distinct non-overlapping intra-method clone groups in the same method must both survive.
    lines_m = array("I", [1 + (i // 4) for i in range(160)])
    stmts_m = array("I", list(range(0, 160, 8)))
    blk_big = BlockSpan("big_fn", 0, 160, 1, 40, 40, len(stmts_m))
    stream_intra = FileTokenStream(
        "src/big.py", "python", False, 40,
        array("I", [100 + i for i in range(160)]),
        array("I", [100 + i for i in range(160)]),
        lines_m,
        array("B", [KIND_STRUCT] * 160),
        stmts_m,
        (blk_big,),
    )
    intra_matches = [
        RawCloneMatch(0, 0, 36, 0, 40, 76, "type1", 1.0),
        RawCloneMatch(0, 80, 118, 0, 120, 158, "type3", 0.85),
    ]
    pf_intra, sum_intra = cluster_and_score_clones([stream_intra], intra_matches, cfg)
    assert sum_intra.clone_groups_count == 2
    assert any("85.0%" in f and "pts)" in f for f in pf_intra["src/big.py"].findings)


