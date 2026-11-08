"""AST function, class, and LCOM4 analyzers for the Python Code Health Analyzer."""

from __future__ import annotations

import ast
from collections import defaultdict

from _code_health.models import (
    CONCERN_EXACT_MAP,
    CONCERN_SHORT_MAP,
    ENTRYPOINT_DECORATORS,
    EXEMPT_LCOM_BASES,
    STDLIB_TRIVIAL_CALLS,
    AnalysisContext,
    ClassReport,
    DimensionScores,
    FunctionReport,
    penalty_item,
)


def call_name(node: ast.Call) -> str:
    """Extract dotted or simple name for an ast.Call target."""
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return f"{func.value.id}.{func.attr}" if isinstance(func.value, ast.Name) else func.attr
    return ""


def docstring_lines(node: ast.AST) -> set[int]:
    """Return line numbers occupied by a node's docstring, if present."""
    body = getattr(node, "body", None)
    if not body or not isinstance(body[0], ast.Expr):
        return set()
    val = body[0].value
    if isinstance(val, ast.Constant) and isinstance(val.value, str):
        start = getattr(body[0], "lineno", 0)
        return set(range(start, getattr(body[0], "end_lineno", start) + 1))
    return set()


def count_effective_loc(node: ast.AST, source_lines: list[str]) -> int:
    """Count non-blank, non-comment, non-docstring lines within an AST node span."""
    start = getattr(node, "lineno", 1)
    end = min(getattr(node, "end_lineno", len(source_lines)), len(source_lines))
    doc = docstring_lines(node)
    valid = [ln.strip() for i, ln in enumerate(source_lines[start - 1 : end], start) if i not in doc]
    return max(1, sum(1 for s in valid if s and not s.startswith("#")))


def has_exempt_base(class_node: ast.ClassDef) -> bool:
    """Return True if class inherits from a data model, enum, exception, or dataclass."""
    bases = {getattr(b, "id", getattr(b, "attr", "")) for b in class_node.bases}
    decs = [d.func if isinstance(d, ast.Call) else d for d in class_node.decorator_list]
    dec_names = {getattr(t, "id", getattr(t, "attr", "")) for t in decs}
    suffix_match = [n for n in bases if n.endswith(("Error", "Exception"))]
    return bool((bases & EXEMPT_LCOM_BASES) or suffix_match or ("dataclass" in dec_names))


class ControlFlowVisitor:
    """Computes Cyclomatic Complexity, Cognitive Complexity, nesting depth, and returns."""

    def __init__(self, is_test: bool) -> None:
        self.is_test = is_test
        self.cc = 1
        self.cog = 0
        self.max_nesting = 0
        self.returns = 0

    def visit_block(self, stmts: list[ast.stmt], depth: int) -> None:
        """Traverse statements at a given nesting depth."""
        for stmt in stmts:
            if not isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                self._dispatch_stmt(stmt, depth)

    def _dispatch_stmt(self, stmt: ast.stmt, depth: int) -> None:
        self.returns += int(isinstance(stmt, ast.Return))
        if isinstance(stmt, ast.If):
            self._visit_if(stmt, depth)
        elif isinstance(stmt, (ast.For, ast.AsyncFor, ast.While)):
            self._visit_loop(stmt, depth)
        elif isinstance(stmt, (ast.Try, ast.Match, ast.With, ast.AsyncWith)):
            self._visit_block_construct(stmt, depth)
        else:
            self.cc += int(isinstance(stmt, ast.Assert)) * int(not self.is_test)
            self._scan_exprs(stmt)

    def _visit_if(self, stmt: ast.If, depth: int) -> None:
        self.cc += 1
        self.cog += 1 + depth
        self.max_nesting = max(self.max_nesting, depth + 1)
        self._scan_exprs(stmt.test)
        self.visit_block(stmt.body, depth + 1)
        if stmt.orelse:
            self.cog += 1
            is_elif = len(stmt.orelse) == 1 and isinstance(stmt.orelse[0], ast.If)
            self.visit_block(stmt.orelse, depth if is_elif else depth + 1)

    def _visit_loop(self, stmt: ast.For | ast.AsyncFor | ast.While, depth: int) -> None:
        self.cc += 1
        self.cog += 1 + depth
        self.max_nesting = max(self.max_nesting, depth + 1)
        if isinstance(stmt, ast.While):
            self._scan_exprs(stmt.test)
        self.visit_block(stmt.body, depth + 1)
        self.visit_block(stmt.orelse, depth + 1)

    def _visit_block_construct(self, stmt: ast.Try | ast.Match | ast.With | ast.AsyncWith, depth: int) -> None:
        if isinstance(stmt, (ast.With, ast.AsyncWith)):
            self.visit_block(stmt.body, depth + 1)
            return
        self.max_nesting = max(self.max_nesting, depth + 1)
        if isinstance(stmt, ast.Match):
            self.cog += 1 + depth
            self.cc += len(stmt.cases)
            for case in stmt.cases:
                self.visit_block(case.body, depth + 1)
            return
        self.visit_block(stmt.body + stmt.orelse + stmt.finalbody, depth + 1)
        self.cc += len(stmt.handlers)
        self.cog += len(stmt.handlers) * (1 + depth)
        for handler in stmt.handlers:
            self.visit_block(handler.body, depth + 1)

    def _scan_exprs(self, node: ast.AST) -> None:
        nodes = list(ast.walk(node))
        bool_ops = [n for n in nodes if isinstance(n, ast.BoolOp)]
        if_exps = [n for n in nodes if isinstance(n, ast.IfExp)]
        comps = [n for n in nodes if isinstance(n, ast.comprehension)]
        self.cc += sum(len(n.values) - 1 for n in bool_ops) + len(if_exps) + sum(len(c.ifs) for c in comps)
        self.cog += len(bool_ops) + len(if_exps)


def _detect_concerns(node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[list[str], int]:
    subnodes = list(ast.walk(node))
    has_comp = any(isinstance(s, (ast.BinOp, ast.ListComp, ast.DictComp, ast.SetComp)) for s in subnodes)
    concerns = {"domain_computation"} if has_comp else set()
    cnames = list(filter(None, (call_name(s) for s in subnodes if isinstance(s, ast.Call))))
    non_self = set(cnames) - {c for c in cnames if c.startswith(("self.", "cls."))} - STDLIB_TRIVIAL_CALLS
    ext_calls = non_self - {c for c in non_self if c.split(".")[-1] in STDLIB_TRIVIAL_CALLS}
    exact_hits = set(filter(None, map(CONCERN_EXACT_MAP.get, cnames)))
    shorts = [c.split(".")[-1] for c in cnames]
    short_hits = set(filter(None, map(CONCERN_SHORT_MAP.get, shorts)))
    return sorted(concerns | exact_hits | short_hits), len(ext_calls)


def _check_subprocess_call(sub: ast.Call, kw_map: dict[str | None, ast.expr], lineno: int) -> list[str]:
    """Check a subprocess.* call for shell=True or string command arguments."""
    if getattr(kw_map.get("shell"), "value", None) is True:
        return [f"Security: subprocess call with shell=True at L{lineno} (-40.0 pts)"]
    first_arg = sub.args[0] if sub.args else None
    if isinstance(first_arg, (ast.BinOp, ast.JoinedStr, ast.Constant)):
        return [f"Security: subprocess command not passed as list at L{lineno} (-15.0 pts)"]
    return []


def _inspect_call_security(sub: ast.Call, default_line: int) -> list[str]:
    """Check a single ast.Call for unsafe execution, deserialization, or shell=True."""
    cname = call_name(sub)
    lineno = getattr(sub, "lineno", default_line)
    kw_map = {kw.arg: kw.value for kw in sub.keywords}
    if cname in {"eval", "exec", "pickle.loads", "pickle.load"}:
        return [f"Security: unsafe {cname}() at L{lineno} (-40.0 pts)"]
    if cname == "yaml.load":
        has_loader = bool({"Loader"} & set(kw_map)) + len(sub.args[1:])
        return [] if has_loader else [f"Security: unsafe yaml.load() without SafeLoader at L{lineno} (-40.0 pts)"]
    return _check_subprocess_call(sub, kw_map, lineno) if cname.startswith("subprocess.") else []


class _SecurityHygieneScanner:
    """Scans a function AST node for unsafe calls and path/branch boundary hygiene."""

    def __init__(self, node: ast.FunctionDef | ast.AsyncFunctionDef, params: list[str], is_test: bool) -> None:
        self.node = node
        self.params = params
        self.is_test = is_test

    def evaluate(self) -> tuple[float, list[str]]:
        """Return (security_score, security_findings) for the function node."""
        if self.is_test:
            return 100.0, []
        findings, by_short = self._collect_calls()
        pen_calls = 40.0 * sum(1 for m in findings if "-40.0" in m) + 15.0 * sum(1 for m in findings if "-15.0" in m)
        writes = by_short["write_text"] + by_short["write_bytes"] + by_short["unlink"] + by_short["rmtree"]
        checkouts = by_short["checkout_branch"]
        has_bound = bool({"is_relative_to", "resolve", "resolve_inline_kb_dir", "startswith"} & set(by_short))
        dirty = int(bool(writes)) * int(bool(checkouts)) * int(min(writes, default=0) < min(checkouts, default=0))
        has_path_arg = any(k in "|".join(self.params) for k in ("path", "dir"))
        unbounded = int(bool(writes)) * int(not has_bound) * int(len(self.params) > 2) * int(has_path_arg)
        p1, f1 = penalty_item(dirty, 25.0, f"Security: file mutation (L{min(writes, default=0)}) before branch checkout (L{min(checkouts, default=0)})")
        p2, f2 = penalty_item(unbounded, 15.0, "Security: destructive/write Path operation without explicit resolve/boundary check")
        return 100.0 - pen_calls - p1 - p2, findings + f1 + f2

    def _collect_calls(self) -> tuple[list[str], dict[str, list[int]]]:
        findings: list[str] = []
        by_short: dict[str, list[int]] = defaultdict(list)
        for c in (s for s in ast.walk(self.node) if isinstance(s, ast.Call)):
            findings.extend(_inspect_call_security(c, self.node.lineno))
            by_short[call_name(c).split(".")[-1]].append(getattr(c, "lineno", self.node.lineno))
        return findings, by_short


def _is_test_assert_node(node: ast.AST) -> bool:
    """Return True if AST node is an Assert or a test assertion call."""
    if isinstance(node, ast.Assert):
        return True
    if not isinstance(node, ast.Call):
        return False
    cname = call_name(node)
    return cname in {"pytest.raises", "pytest.warns", "pytest.fail"} or cname.split(".")[-1].startswith("assert")


def _score_test_clean(node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[float, list[str]]:
    """Score assertion hygiene for a test_* function."""
    if not node.name.startswith("test_"):
        return 100.0, []
    asserts = sum(1 for s in ast.walk(node) if _is_test_assert_node(s))
    p1, f1 = penalty_item(int(asserts == 0), 30.0, "Clean (Test): test has 0 assertions")
    p2, f2 = penalty_item(asserts - 8, 3.0, f"Clean (Test): {asserts} assertions in single test (>8)", cap=30.0)
    return 100.0 - p1 - p2, f1 + f2


def _classify_except_handler(handler: ast.ExceptHandler) -> tuple[float, str | None]:
    """Return (penalty, finding) if ExceptHandler is bare or swallowed broad Exception."""
    if handler.type is None:
        return 25.0, f"Clean: bare except at L{handler.lineno} (-25.0 pts)"
    is_broad = getattr(handler.type, "id", "") == "Exception" and len(handler.body) == 1
    if is_broad and isinstance(handler.body[0], (ast.Pass, ast.Continue, ast.Return)):
        return 10.0, f"Clean: swallowed broad except Exception at L{handler.lineno} (-10.0 pts)"
    return 0.0, None


def _check_exception_handlers(node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[float, list[str]]:
    """Return penalty and findings for bare or swallowed broad exception handlers."""
    handlers = [n for n in ast.walk(node) if isinstance(n, ast.ExceptHandler)]
    results = [_classify_except_handler(h) for h in handlers]
    return sum(p for p, _ in results), [msg for _, msg in results if msg]


def _blend_class_methods(
    raw: tuple[float, float, float, float], methods: list[FunctionReport]
) -> tuple[float, float, float, float, float]:
    """Blend class structural scores (60%) with method averages (40%)."""
    if not methods:
        return (*raw, 100.0)
    n = len(methods)
    srp = sum([m.scores.srp for m in methods]) / n
    size = sum([m.scores.size for m in methods]) / n
    comp = sum([m.scores.complexity for m in methods]) / n
    clean = sum([m.scores.clean for m in methods]) / n
    sec = min([m.scores.security for m in methods])
    return (0.6 * raw[0] + 0.4 * srp, 0.6 * raw[1] + 0.4 * size, 0.6 * raw[2] + 0.4 * comp, 0.6 * raw[3] + 0.4 * clean, sec)


class UnitScorer:
    """Evaluates function/method and class AST nodes across the 5 code health dimensions."""

    def __init__(self, ctx: AnalysisContext) -> None:
        self.ctx = ctx
        self.cfg = ctx.config

    def analyze_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> FunctionReport:
        """Analyze a function node and return its FunctionReport."""
        loc = count_effective_loc(node, self.ctx.source_lines)
        params = [a.arg for a in node.args.args + node.args.kwonlyargs if a.arg not in {"self", "cls"}]
        decs = [d.func if isinstance(d, ast.Call) else d for d in node.decorator_list]
        is_entry = bool({getattr(t, "attr", getattr(t, "id", "")) for t in decs} & ENTRYPOINT_DECORATORS)
        cf = ControlFlowVisitor(self.ctx.is_test)
        cf.visit_block(node.body, 0)
        concerns, ext_calls = _detect_concerns(node)

        s_srp, f_srp = self._score_srp(node, concerns, ext_calls, is_entry)
        s_size, f_size = self._score_size(loc, len(params), cf.max_nesting, is_entry)
        s_comp, f_comp = self._score_complexity(cf.cc, cf.cog, cf.returns)
        s_clean, f_clean = self._score_clean(node, loc)
        s_sec, f_sec = _SecurityHygieneScanner(node, params, self.ctx.is_test).evaluate()

        scores = DimensionScores.from_raw((s_srp, s_size, s_comp, s_clean, s_sec), self.cfg)
        qualname = f"{self.ctx.class_name}.{node.name}" if self.ctx.class_name else node.name
        return FunctionReport(
            node.name, qualname, self.ctx.file_path, node.lineno, getattr(node, "end_lineno", node.lineno),
            loc, len(params), cf.max_nesting, cf.cc, cf.cog, cf.returns, concerns, ext_calls,
            self.ctx.is_test, scores, f_srp + f_size + f_comp + f_clean + f_sec,
        )

    def analyze_class(self, node: ast.ClassDef) -> ClassReport:
        """Analyze a ClassDef node and return its ClassReport."""
        loc = count_effective_loc(node, self.ctx.source_lines)
        m_scorer = UnitScorer(AnalysisContext(self.ctx.source_lines, self.ctx.file_path, self.ctx.is_test, self.cfg, node.name))
        methods = [m_scorer.analyze_function(m) for m in node.body if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))]
        lcom4, self_attrs = compute_lcom4(node)
        total_cc = sum(m.cyclomatic_complexity for m in methods)
        raw, findings = self._score_class_structure(node, loc, (len(methods), len(self_attrs), lcom4, total_cc))
        blended = _blend_class_methods(raw, methods)
        return ClassReport(
            node.name, self.ctx.file_path, node.lineno, getattr(node, "end_lineno", node.lineno),
            loc, len(methods), len(self_attrs), lcom4, total_cc, DimensionScores.from_raw(blended, self.cfg), findings, methods,
        )

    def _score_class_structure(self, node: ast.ClassDef, loc: int, stats: tuple[int, int, int, int]) -> tuple[tuple[float, float, float, float], list[str]]:
        """Score class-level structural SRP, size, complexity, and docstring hygiene."""
        m_cnt, a_cnt, lcom4, total_cc = stats
        p_lcom, f_lcom = penalty_item((lcom4 - 1) * int(m_cnt > 2), 15.0, f"SRP: LCOM4={lcom4} disconnected method groups")
        p_mth, f_mth = penalty_item(m_cnt - self.cfg.max_ideal_class_methods, 4.0, f"SRP: methods={m_cnt} (>{self.cfg.max_ideal_class_methods})")
        p_atr, f_atr = penalty_item(a_cnt - self.cfg.max_ideal_class_attrs, 4.0, f"SRP: self attributes={a_cnt} (>{self.cfg.max_ideal_class_attrs})")
        p_loc, f_loc = penalty_item(loc - self.cfg.max_ideal_class_loc, 0.4, f"Size: class LOC={loc} (>{self.cfg.max_ideal_class_loc})")
        p_cc, f_cc = penalty_item(total_cc - self.cfg.max_ideal_class_cc, 1.5, f"Complexity: total class CC={total_cc} (>{self.cfg.max_ideal_class_cc})")
        no_doc = int(not self.ctx.is_test) * int(not node.name.startswith("_")) * int(ast.get_docstring(node) is None)
        p_doc, f_doc = penalty_item(no_doc, 15.0, "Clean: missing class docstring")
        return (100.0 - p_lcom - p_mth - p_atr, 100.0 - p_loc, 100.0 - p_cc, 100.0 - p_doc), f_lcom + f_mth + f_atr + f_loc + f_cc + f_doc

    def _score_srp(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef, concerns: list[str], ext_calls: int, is_entry: bool
    ) -> tuple[float, list[str]]:
        if self.ctx.is_test:
            return 100.0, []
        defaults = node.args.defaults + list(filter(None, node.args.kw_defaults))
        bool_defs = 0 if is_entry else sum(1 for d in defaults if isinstance(getattr(d, "value", None), bool))
        p1, f1 = penalty_item(len(concerns) - self.cfg.max_ideal_concerns, 12.0, f"SRP: mixes {len(concerns)} concerns ({', '.join(concerns)})")
        p2, f2 = penalty_item(ext_calls - self.cfg.max_ideal_external_calls, 3.0, f"SRP: high external call fan-out={ext_calls} (>{self.cfg.max_ideal_external_calls})", cap=36.0)
        p3, f3 = penalty_item(bool_defs, 6.0, f"SRP: {bool_defs} bool default flag parameter(s)")
        return 100.0 - p1 - p2 - p3, f1 + f2 + f3

    def _score_size(self, loc: int, params_count: int, max_nesting: int, is_entry: bool) -> tuple[float, list[str]]:
        ideal = self.cfg.max_ideal_func_loc_test if self.ctx.is_test else self.cfg.max_ideal_func_loc_src
        mid = self.cfg.max_mid_func_loc_test if self.ctx.is_test else self.cfg.max_mid_func_loc_src
        r1, r2 = (1.0, 2.0) if self.ctx.is_test else (1.5, 2.5)
        loc_pen = round(max(0, min(loc, mid) - ideal) * r1 + max(0, loc - mid) * r2, 1)
        p1, f1 = penalty_item(loc_pen, 1.0, f"Size: LOC={loc} (>{ideal})", cap=100.0)
        max_p = self.cfg.max_entrypoint_params if is_entry else self.cfg.max_ideal_params
        p2, f2 = penalty_item(params_count - max_p, 6.0, f"Size: params={params_count} (>{max_p})")
        p3, f3 = penalty_item(max_nesting - self.cfg.max_ideal_nesting, 10.0, f"Size: nesting depth={max_nesting} (>{self.cfg.max_ideal_nesting})")
        return 100.0 - p1 - p2 - p3, f1 + f2 + f3

    def _score_complexity(self, cc: int, cogc: int, returns_count: int) -> tuple[float, list[str]]:
        cc_pen = max(0, min(cc, self.cfg.max_mid_cc) - self.cfg.max_ideal_cc) * 4.0 + max(0, cc - self.cfg.max_mid_cc) * 7.0
        p1, f1 = penalty_item(cc_pen, 1.0, f"Complexity: CC={cc} (>{self.cfg.max_ideal_cc})", cap=100.0)
        p2, f2 = penalty_item(cogc - self.cfg.max_ideal_cogc, 2.5, f"Complexity: cognitive={cogc} (>{self.cfg.max_ideal_cogc})")
        p3, f3 = penalty_item(returns_count - self.cfg.max_ideal_returns, 4.0, f"Complexity: returns={returns_count} (>{self.cfg.max_ideal_returns})")
        return 100.0 - p1 - p2 - p3, f1 + f2 + f3

    def _score_clean(self, node: ast.FunctionDef | ast.AsyncFunctionDef, loc: int) -> tuple[float, list[str]]:
        score, findings = _score_test_clean(node) if self.ctx.is_test else self._score_src_clean(node, loc)
        exc_pen, exc_findings = _check_exception_handlers(node)
        return score - exc_pen, findings + exc_findings

    def _score_src_clean(self, node: ast.FunctionDef | ast.AsyncFunctionDef, loc: int) -> tuple[float, list[str]]:
        non_self = [a for a in node.args.args + node.args.kwonlyargs if a.arg not in {"self", "cls"}]
        untyped = [a.arg for a in non_self if a.annotation is None]
        no_ret = int(node.returns is None) * int(not node.name.startswith("__"))
        no_doc = int(not node.name.startswith("_")) * int(ast.get_docstring(node) is None)
        p1, f1 = penalty_item(no_ret, 10.0, "Clean: missing return type annotation")
        p2, f2 = penalty_item(len(untyped), 5.0, f"Clean: {len(untyped)} untyped param(s) ({', '.join(untyped[:3])})", cap=25.0)
        p3, f3 = penalty_item(no_doc, 5.0 if loc <= 10 else 10.0, "Clean: missing public docstring")
        return 100.0 - p1 - p2 - p3, f1 + f2 + f3


class _Lcom4Analyzer:
    """Computes LCOM4 connected components and self.<attr> usage for a ClassDef node."""

    def __init__(self, class_node: ast.ClassDef) -> None:
        self.class_node = class_node
        self.methods = [n for n in class_node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        self.all_names = {m.name for m in self.methods}

    def compute(self) -> tuple[int, set[str]]:
        """Return (lcom4_components, self_attrs)."""
        usages = [(m.name, *self._method_tokens(m)) for m in self.methods]
        all_attrs = {a for _, attrs, _ in usages for a in attrs}
        m_tokens = {name: tok for name, _, tok in usages if not name.startswith("__")}
        if len(m_tokens) <= 2 or has_exempt_base(self.class_node):
            return int(bool(self.methods)), all_attrs
        return self._count_components(m_tokens), all_attrs

    def _method_tokens(self, method: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[set[str], set[str]]:
        attrs_nodes = [s for s in ast.walk(method) if isinstance(s, ast.Attribute) and isinstance(s.value, ast.Name)]
        self_refs = [s.attr for s in attrs_nodes if s.value.id == "self"]
        cls_refs = [s.attr for s in attrs_nodes if s.value.id in {"self", "cls"}]
        calls = set(cls_refs) & self.all_names
        attrs = set(self_refs) - self.all_names
        return attrs, {f"a:{a}" for a in attrs} | {f"m:{c}" for c in calls} | {f"m:{method.name}"}

    def _count_components(self, m_tokens: dict[str, set[str]]) -> int:
        adj: dict[str, set[str]] = {n: set() for n in m_tokens}
        names = list(m_tokens)
        for i, n1 in enumerate(names):
            for n2 in names[i + 1 :]:
                if m_tokens[n1] & m_tokens[n2]:
                    adj[n1].add(n2)
                    adj[n2].add(n1)
        return _bfs_component_count(names, adj)


def _bfs_component_count(nodes: list[str], adj: dict[str, set[str]]) -> int:
    """Count connected components in an undirected graph via BFS."""
    visited: set[str] = set()
    components = 0
    for start in nodes:
        if start not in visited:
            components += 1
            queue = [start]
            visited.add(start)
            while queue:
                new_nodes = adj[queue.pop()] - visited
                visited.update(new_nodes)
                queue.extend(new_nodes)
    return components


def compute_lcom4(class_node: ast.ClassDef) -> tuple[int, set[str]]:
    """Compute LCOM4 connected components and set of self.<attr> names."""
    return _Lcom4Analyzer(class_node).compute()
