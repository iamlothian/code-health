"""JavaScript language profile definitions and architectural rules."""

from __future__ import annotations

from _code_health.ir_models import FrameworkProfile, IRClass, IRFunction, LanguageProfile, RulePenalty


class JavaScriptLanguageProfile(LanguageProfile):
    """ECMAScript language profile evaluating code health, anti-coercion, and security rules."""

    def __init__(self, frameworks: list[FrameworkProfile] | None = None) -> None:
        super().__init__(
            name="javascript",
            file_extensions=(".js", ".jsx", ".mjs", ".cjs"),
            frameworks=list(frameworks or []),
        )

    def _eval_clean_smells(self, func: IRFunction) -> list[RulePenalty]:
        penalties: list[RulePenalty] = []
        if func.var_declarations_count > 0:
            pen = min(15.0, func.var_declarations_count * 3.0)
            penalties.append(
                RulePenalty(
                    "clean",
                    pen,
                    f"Clean: {func.var_declarations_count} legacy 'var' declaration(s) detected (prefer 'const' or 'let') (-{pen:.1f} pts)",
                    func.lineno,
                )
            )
        if func.loose_comparisons_count > 0:
            pen = min(10.0, func.loose_comparisons_count * 2.0)
            penalties.append(
                RulePenalty(
                    "clean",
                    pen,
                    f"Clean: {func.loose_comparisons_count} loose equality comparison(s) (==/!=) trigger implicit type coercion (prefer ===/!==) (-{pen:.1f} pts)",
                    func.lineno,
                )
            )
        for h in func.except_handlers:
            if h.is_empty:
                penalties.append(
                    RulePenalty("clean", 10.0, "Clean: empty catch block swallows exception (-10.0 pts)", h.lineno)
                )
        if func.has_debugger_statement:
            penalties.append(
                RulePenalty("clean", 10.0, "Clean: debugger statement detected (-10.0 pts)", func.lineno)
            )
        return penalties

    def _eval_parameter_typing(self, func: IRFunction) -> list[RulePenalty]:
        if func.is_test:
            return []
        untyped = [
            p.name for p in func.params
            if p.type_annotation is None and not p.has_default and p.name not in {"this", "arguments"}
        ]
        if not untyped:
            return []
        pen = min(10.0, len(untyped) * 2.0)
        return [
            RulePenalty(
                "clean",
                pen,
                f"Clean: {len(untyped)} unannotated parameter(s) without default values ({', '.join(untyped[:3])}) (-{pen:.1f} pts)",
                func.lineno,
            )
        ]

    def _eval_dynamic_sinks(self, func: IRFunction) -> list[RulePenalty]:
        penalties: list[RulePenalty] = []
        eval_names = {"eval", "Function", "new Function", "window.eval", "global.eval", "globalThis.eval"}
        timers = {
            "setTimeout", "setInterval", "window.setTimeout", "window.setInterval",
            "global.setTimeout", "global.setInterval", "globalThis.setTimeout", "globalThis.setInterval",
        }
        for c in func.calls:
            if c.name in eval_names or c.name.endswith(".eval"):
                penalties.append(
                    RulePenalty("security", 40.0, f"Security: dynamic code execution via {c.name} (-40.0 pts)", c.lineno)
                )
            elif c.name in timers and getattr(c, "has_string_arg", False):
                penalties.append(
                    RulePenalty(
                        "security",
                        20.0,
                        f"Security: string argument to {c.name} causes implicit code evaluation (-20.0 pts)",
                        c.lineno,
                    )
                )
        return penalties

    def _eval_scope_security(self, func: IRFunction) -> list[RulePenalty]:
        penalties: list[RulePenalty] = []
        if func.has_proto_mutation:
            penalties.append(
                RulePenalty("security", 25.0, "Security: direct prototype mutation via '__proto__' (-25.0 pts)", func.lineno)
            )
        if func.has_with_statement:
            penalties.append(
                RulePenalty("security", 30.0, "Security: 'with' statement obscures lexical scope and risks prototype pollution (-30.0 pts)", func.lineno)
            )
        return penalties

    def evaluate_function(self, func: IRFunction, parent: IRClass | None) -> list[RulePenalty]:
        """Evaluate JS and attached framework function-level rules."""
        penalties: list[RulePenalty] = super().evaluate_function(func, parent)
        penalties.extend(self._eval_clean_smells(func))
        penalties.extend(self._eval_parameter_typing(func))
        penalties.extend(self._eval_dynamic_sinks(func))
        penalties.extend(self._eval_scope_security(func))
        return penalties

    def evaluate_class(self, cls: IRClass) -> list[RulePenalty]:
        """Evaluate attached framework class-level rules."""
        return super().evaluate_class(cls)

    def is_test_assert_call(self, call_name: str) -> bool:
        """Recognize standard JS test assertion matchers."""
        short = call_name.split(".")[-1]
        return short in {
            "assert", "assertEquals", "strictEqual", "deepStrictEqual", "ok",
            "expect", "should", "toBe", "toEqual", "toStrictEqual", "toThrow",
            "toBeTruthy", "toBeFalsy", "toHaveLength", "equal",
        }


JAVASCRIPT_PROFILE = JavaScriptLanguageProfile()
