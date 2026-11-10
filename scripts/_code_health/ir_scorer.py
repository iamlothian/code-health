"""Universal 5-Dimension Scorer operating over language-neutral IR models."""

from __future__ import annotations

from typing import Protocol

from _code_health.ir_models import (
    IRClass,
    IRFunction,
    RulePenalty,
)
from _code_health.models import (
    ClassReport,
    DimensionScores,
    FunctionReport,
    RubricConfig,
    penalty_item,
)


class BaseProfileProtocol(Protocol):
    """Protocol for active language and framework profiles."""

    name: str

    def evaluate_function(self, func: IRFunction, parent: IRClass | None) -> list[RulePenalty]:
        """Evaluate architectural rule violations for a function or method."""
        ...

    def evaluate_class(self, cls: IRClass) -> list[RulePenalty]:
        """Evaluate architectural rule violations for a class or record."""
        ...

    def map_concern(self, call_name: str) -> str | None:
        """Map a function/call name to an operational concern category."""
        ...

    def is_entrypoint_func(self, func: IRFunction) -> bool:
        """Check if function is an entrypoint."""
        ...

    def is_test_assert_call(self, call_name: str) -> bool:
        """Determine if a function/method call represents an assertion."""
        ...


def _apply_ir_penalties(
    scores: tuple[float, float, float, float, float], penalties: list[RulePenalty]
) -> tuple[float, float, float, float, float]:
    dims = {"srp": 0, "size": 1, "complexity": 2, "clean": 3, "security": 4}
    adj = list(scores)
    for p in penalties:
        idx = dims.get(p.dimension)
        if idx is not None:
            adj[idx] -= p.penalty_points
    return (adj[0], adj[1], adj[2], adj[3], adj[4])


def _blend_ir_class_methods(
    raw: tuple[float, float, float, float], methods: list[FunctionReport]
) -> tuple[float, float, float, float, float]:
    if not methods:
        return (*raw, 100.0)
    n = len(methods)
    return (
        sum(m.scores.srp for m in methods) / n - (100.0 - raw[0]),
        sum(m.scores.size for m in methods) / n - (100.0 - raw[1]),
        sum(m.scores.complexity for m in methods) / n - (100.0 - raw[2]),
        sum(m.scores.clean for m in methods) / n - (100.0 - raw[3]),
        min(m.scores.security for m in methods),
    )


def _count_ir_asserts(func: IRFunction, profile: BaseProfileProtocol) -> int:
    matched = [c for c in func.calls if profile.is_test_assert_call(c.name)]
    if profile.name in {"javascript", "typescript"}:
        matchers_at_line = {c.lineno for c in matched if c.name.split(".")[-1] != "expect"}
        matched = [c for c in matched if c.name.split(".")[-1] != "expect" or c.lineno not in matchers_at_line]
    return len(matched)


def _score_test_clean_ir(func: IRFunction, profile: BaseProfileProtocol) -> tuple[float, list[str]]:
    is_test_method = (
        func.name.startswith("test")
        or func.name.startswith("should")
        or any(a.name in {"Test", "ParameterizedTest", "RepeatedTest"} for a in func.annotations)
    )
    if not is_test_method:
        return 0.0, []
    asserts = _count_ir_asserts(func, profile)
    p0, f0 = penalty_item(int(asserts == 0), 30.0, "Clean (Test): test has 0 assertions")
    p_many, f_many = penalty_item(asserts - 8, 3.0, f"Clean (Test): {asserts} assertions in single test (>8)", cap=30.0)
    return p0 + p_many, f0 + f_many


def _score_source_clean_ir(func: IRFunction, profile: BaseProfileProtocol | None = None) -> tuple[float, list[str]]:
    findings: list[str] = []
    pen = 0.0
    if not func.has_docstring and not func.name.startswith("_"):
        p_doc = 5.0 if func.loc <= 10 else 10.0
        pen += p_doc
        findings.append(f"Clean: missing public docstring (-{p_doc:.1f} pts)")
    if profile and profile.name == "javascript":
        return pen, findings
    untyped = [p.name for p in func.params if p.type_annotation is None and p.name not in {"self", "cls"}]
    if untyped:
        p_un = min(25.0, len(untyped) * 5.0)
        pen += p_un
        findings.append(f"Clean: {len(untyped)} untyped param(s) ({', '.join(untyped[:3])}) (-{p_un:.1f} pts)")
    if func.return_type is None and not func.name.startswith("__"):
        pen += 10.0
        findings.append("Clean: missing return type annotation (-10.0 pts)")
    return pen, findings


def _check_ir_exceptions(handlers: list) -> tuple[float, list[str]]:
    pen = 0.0
    findings: list[str] = []
    for h in handlers:
        if h.is_broad and h.is_empty:
            pen += 10.0
            findings.append(f"Clean: swallowed broad except Exception at L{h.lineno} (-10.0 pts)")
    return pen, findings


def _score_security_ir(func: IRFunction, is_test: bool) -> tuple[float, list[str]]:
    if is_test:
        return 100.0, []
    findings: list[str] = []
    pen = 0.0
    for call in func.calls:
        if call.name in {"eval", "exec", "pickle.loads", "pickle.load"}:
            pen += 40.0
            findings.append(f"Security: unsafe {call.name}() at L{call.lineno} (-40.0 pts)")
    return 100.0 - pen, findings


class UniversalIRScorer:
    """Scores IR models across SRP, Size, Complexity, Clean Code, and Security."""

    def __init__(self, config: RubricConfig, profile: BaseProfileProtocol) -> None:
        self.cfg = config
        self.profile = profile

    def score_function(
        self, func: IRFunction, file_path: str, is_test: bool, parent: IRClass | None = None
    ) -> FunctionReport:
        """Evaluate an IRFunction into a FunctionReport."""
        concerns = sorted({c for call in func.calls if (c := self.profile.map_concern(call.name))})
        ext_calls = len({c.name for c in func.calls if not self.profile.map_concern(c.name)})
        is_entry = self.profile.is_entrypoint_func(func)

        s_srp, f_srp = self._score_srp(func, concerns, ext_calls, is_entry, is_test)
        s_size, f_size = self._score_size(func, is_entry, is_test)
        s_comp, f_comp = self._score_complexity(func)
        p_cln, f_cln = _score_test_clean_ir(func, self.profile) if is_test else _score_source_clean_ir(func, self.profile)
        p_ex, f_ex = (0.0, []) if self.profile.name in {"javascript", "typescript"} else _check_ir_exceptions(func.except_handlers)
        s_clean = 100.0 - p_cln - p_ex
        s_sec, f_sec = (100.0, []) if self.profile.name in {"javascript", "typescript"} else _score_security_ir(func, is_test)

        penalties = self.profile.evaluate_function(func, parent)
        raw_scores = (s_srp, s_size, s_comp, s_clean, s_sec)
        final_scores = _apply_ir_penalties(raw_scores, penalties)
        rule_findings = [p.finding for p in penalties]

        return FunctionReport(
            name=func.name,
            qualname=func.qualname,
            file_path=file_path,
            lineno=func.lineno,
            end_lineno=func.end_lineno,
            loc=func.loc,
            params_count=len(func.params),
            max_nesting=func.max_nesting,
            cyclomatic_complexity=func.cyclomatic_complexity,
            cognitive_complexity=func.cognitive_complexity,
            returns_count=func.returns_count,
            concerns=concerns,
            external_calls_count=ext_calls,
            is_test=is_test,
            scores=DimensionScores.from_raw(final_scores, self.cfg),
            findings=f_srp + f_size + f_comp + f_cln + f_ex + f_sec + rule_findings,
        )

    def score_class(self, cls: IRClass, file_path: str, is_test: bool) -> ClassReport:
        """Evaluate an IRClass into a ClassReport blending structure and method scores."""
        methods = [self.score_function(m, file_path, is_test, cls) for m in cls.methods]
        m_cnt = len(cls.methods)
        a_cnt = len(cls.fields)
        total_cc = sum(m.cyclomatic_complexity for m in methods)

        p_lcom, f_lcom = penalty_item((cls.lcom4 - 1) * int(m_cnt > 2), 15.0, f"SRP: LCOM4={cls.lcom4} disconnected method groups")
        p_mc, f_mc = penalty_item(m_cnt - self.cfg.max_ideal_class_methods, 4.0, f"SRP: methods={m_cnt} (>{self.cfg.max_ideal_class_methods})")
        p_fc, f_fc = penalty_item(a_cnt - self.cfg.max_ideal_class_attrs, 4.0, f"SRP: self attributes={a_cnt} (>{self.cfg.max_ideal_class_attrs})")
        s_srp = 100.0 - p_lcom - p_mc - p_fc

        p_loc, f_loc = penalty_item(cls.loc - self.cfg.max_ideal_class_loc, 0.4, f"Size: class LOC={cls.loc} (>{self.cfg.max_ideal_class_loc})")
        s_size = 100.0 - p_loc

        p_cc, f_cc = penalty_item(total_cc - self.cfg.max_ideal_class_cc, 1.5, f"Complexity: total class CC={total_cc} (>{self.cfg.max_ideal_class_cc})")
        s_comp = 100.0 - p_cc

        p_doc, f_doc = penalty_item(int(not is_test and not cls.has_docstring), 15.0, "Clean: missing class docstring")
        s_clean = 100.0 - p_doc

        raw_struct = (s_srp, s_size, s_comp, s_clean)
        blended = _blend_ir_class_methods(raw_struct, methods)
        penalties = self.profile.evaluate_class(cls)
        final_scores = _apply_ir_penalties(blended, penalties)
        rule_findings = [p.finding for p in penalties]

        return ClassReport(
            name=cls.name,
            file_path=file_path,
            lineno=cls.lineno,
            end_lineno=cls.end_lineno,
            loc=cls.loc,
            methods_count=m_cnt,
            attrs_count=a_cnt,
            lcom4=cls.lcom4,
            total_cc=total_cc,
            scores=DimensionScores.from_raw(final_scores, self.cfg),
            findings=f_lcom + f_mc + f_fc + f_loc + f_cc + f_doc + rule_findings,
            methods=methods,
        )

    def _score_srp(
        self, func: IRFunction, concerns: list[str], ext_calls: int, is_entry: bool, is_test: bool
    ) -> tuple[float, list[str]]:
        if is_test:
            return 100.0, []
        p_c, f_c = penalty_item(len(concerns) - self.cfg.max_ideal_concerns, 12.0, f"SRP: mixes {len(concerns)} concerns ({', '.join(concerns)})")
        p_ext, f_ext = penalty_item(ext_calls - self.cfg.max_ideal_external_calls, 3.0, f"SRP: high external call fan-out={ext_calls} (>{self.cfg.max_ideal_external_calls})", cap=36.0)
        p_bool, f_bool = penalty_item(0 if is_entry else sum(1 for p in func.params if p.has_default and p.type_annotation == "bool"), 6.0, "SRP: boolean flag parameter with default value")
        return 100.0 - p_c - p_ext - p_bool, f_c + f_ext + f_bool

    def _score_size(self, func: IRFunction, is_entry: bool, is_test: bool) -> tuple[float, list[str]]:
        ideal = self.cfg.max_ideal_func_loc_test if is_test else self.cfg.max_ideal_func_loc_src
        mid = self.cfg.max_mid_func_loc_test if is_test else self.cfg.max_mid_func_loc_src
        r1, r2 = (1.0, 2.0) if is_test else (1.5, 2.5)
        loc_pen = round(max(0, min(func.loc, mid) - ideal) * r1 + max(0, func.loc - mid) * r2, 1)
        p_loc, f_loc = penalty_item(loc_pen, 1.0, f"Size: LOC={func.loc} (>{ideal})", cap=100.0)

        max_p = self.cfg.max_entrypoint_params if is_entry else self.cfg.max_ideal_params
        p_prm, f_prm = penalty_item(len(func.params) - max_p, 6.0, f"Size: params={len(func.params)} (>{max_p})")
        p_nst, f_nst = penalty_item(func.max_nesting - self.cfg.max_ideal_nesting, 10.0, f"Size: nesting depth={func.max_nesting} (>{self.cfg.max_ideal_nesting})")
        return 100.0 - p_loc - p_prm - p_nst, f_loc + f_prm + f_nst

    def _score_complexity(self, func: IRFunction) -> tuple[float, list[str]]:
        cc = func.cyclomatic_complexity
        cc_pen = max(0, min(cc, self.cfg.max_mid_cc) - self.cfg.max_ideal_cc) * 4.0 + max(0, cc - self.cfg.max_mid_cc) * 7.0
        p_cc, f_cc = penalty_item(cc_pen, 1.0, f"Complexity: CC={cc} (>{self.cfg.max_ideal_cc})", cap=100.0)
        p_cog, f_cog = penalty_item(func.cognitive_complexity - self.cfg.max_ideal_cogc, 2.5, f"Complexity: cognitive={func.cognitive_complexity} (>{self.cfg.max_ideal_cogc})")
        p_ret, f_ret = penalty_item(func.returns_count - self.cfg.max_ideal_returns, 4.0, f"Complexity: returns={func.returns_count} (>{self.cfg.max_ideal_returns})")
        return 100.0 - p_cc - p_cog - p_ret, f_cc + f_cog + f_ret
