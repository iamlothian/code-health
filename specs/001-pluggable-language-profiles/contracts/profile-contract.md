# Interface Contract: Profile Registration & Rule Hooks

**Feature**: [spec.md](../spec.md) | **Date**: 2026-11-08

This document defines the Python protocols and hook contracts for registering custom language and framework profiles.

---

## 1. `RulePenalty`

```python
@dataclass(frozen=True)
class RulePenalty:
    dimension: str          # "srp", "size", "complexity", "clean", "security"
    penalty_points: float   # e.g., 20.0
    finding: str            # e.g., "SRP (Spring): @RestController directly injects UserRepository (-20.0 pts)"
    lineno: int             # Line number of the violation
```

---

## 2. `LanguageProfile` Protocol

```python
class LanguageProfile(Protocol):
    name: str
    file_extensions: tuple[str, ...]
    
    def is_test_file(self, rel_path: str) -> bool:
        """Return True if path matches language test conventions."""
        ...

    def parse(self, file_path: Path, rel_path: str, is_test: bool, allow_fallback: bool) -> IRModule:
        """Parse source file into normalized IRModule or raise MissingNativeParserError."""
        ...

    def score_clean_code(self, func: IRFunction, ctx: AnalysisContext) -> list[RulePenalty]:
        """Evaluate language-specific clean code rules (e.g. documentation, exceptions)."""
        ...
```

---

## 3. `FrameworkProfile` Protocol

```python
class FrameworkProfile(Protocol):
    name: str
    target_language: str
    concern_map: dict[str, str]
    entrypoint_annotations: set[str]
    lcom4_exempt_annotations: set[str]

    def evaluate_class(self, cls: IRClass) -> list[RulePenalty]:
        """Evaluate class-level architectural rules (e.g. field injection, stereotype layering)."""
        ...

    def evaluate_function(self, func: IRFunction, parent_class: IRClass | None) -> list[RulePenalty]:
        """Evaluate function-level framework rules (e.g. transaction boundaries, query safety)."""
        ...

    def is_test_assert_call(self, call_name: str) -> bool:
        """Return True if call represents a framework-specific test assertion."""
        ...
```
