"""TypeScript language profile definitions and architectural rules."""

from __future__ import annotations

from _code_health.ir_models import IRClass, IRFunction, RulePenalty
from _code_health.profiles_js import JavaScriptLanguageProfile


class TypeScriptLanguageProfile(JavaScriptLanguageProfile):
    """TypeScript language profile evaluating strict typing, escape hatches, anti-coercion, and security rules."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "typescript"
        self.file_extensions = (".ts", ".tsx", ".mts", ".cts")

    def _eval_ts_type_safety(self, func: IRFunction) -> list[RulePenalty]:
        penalties: list[RulePenalty] = []
        if func.explicit_any_count > 0:
            pen = min(20.0, func.explicit_any_count * 5.0)
            penalties.append(
                RulePenalty(
                    "clean",
                    pen,
                    f"Clean (TS): {func.explicit_any_count} explicit 'any' type usage(s) defeat type safety (-{pen:.1f} pts)",
                    func.lineno,
                )
            )
        if func.ts_ignore_count > 0:
            pen = min(20.0, func.ts_ignore_count * 10.0)
            penalties.append(
                RulePenalty(
                    "clean",
                    pen,
                    f"Clean (TS): {func.ts_ignore_count} '@ts-ignore'/'@ts-nocheck' directive(s) suppress compiler checks (-{pen:.1f} pts)",
                    func.lineno,
                )
            )
        if func.non_null_assertion_count > 0:
            pen = min(10.0, func.non_null_assertion_count * 2.0)
            penalties.append(
                RulePenalty(
                    "clean",
                    pen,
                    f"Clean (TS): {func.non_null_assertion_count} non-null assertion(s) ('!') bypass strict null checks (-{pen:.1f} pts)",
                    func.lineno,
                )
            )
        return penalties

    def _eval_ts_query_injection(self, func: IRFunction) -> list[RulePenalty]:
        penalties: list[RulePenalty] = []
        query_methods = {"query", "execute", "raw", "$queryRawUnsafe", "$executeRawUnsafe"}
        for c in func.calls:
            short = c.name.split(".")[-1]
            if short in query_methods and getattr(c, "has_string_concat", False):
                penalties.append(
                    RulePenalty(
                        "security",
                        40.0,
                        f"Security (TS): potential SQL/query injection in {c.name} via string concatenation (-40.0 pts)",
                        c.lineno,
                    )
                )
        return penalties

    def evaluate_function(self, func: IRFunction, parent: IRClass | None) -> list[RulePenalty]:
        """Evaluate function-level TypeScript code health rules and penalties."""
        penalties: list[RulePenalty] = []
        penalties.extend(self._eval_clean_smells(func))
        penalties.extend(self._eval_ts_type_safety(func))
        penalties.extend(self._eval_dynamic_sinks(func))
        penalties.extend(self._eval_scope_security(func))
        penalties.extend(self._eval_ts_query_injection(func))
        return penalties

    def is_test_assert_call(self, call_name: str) -> bool:
        """Recognize Jest, Vitest, Mocha, and Testing Library assertion matchers."""
        if super().is_test_assert_call(call_name):
            return True
        return call_name.split(".")[-1] in _TS_EXTRA_MATCHERS


_TS_EXTRA_MATCHERS = frozenset({
    "toBeDefined", "toBeUndefined", "toBeNull", "toContain", "toMatch",
    "toMatchObject", "toHaveBeenCalled", "toHaveBeenCalledWith",
    "toHaveBeenCalledTimes", "toHaveProperty", "toBeInstanceOf",
    "toBeGreaterThan", "toBeLessThan", "toBeInTheDocument",
})

TYPESCRIPT_PROFILE = TypeScriptLanguageProfile()
