# Profile Contract: TypeScript Language Support

**Date**: 2026-11-09  
**Feature**: TypeScript Language Profile  
**Spec**: [spec.md](../spec.md)  

---

## 1. Parser Entrypoint Contract (`scripts/_code_health/ts_parser.py`)

### 1.1 Dependency Verification

```python
def check_typescript_dependencies() -> tuple[Any, Any]:
    """Verify tree-sitter and tree-sitter-typescript are available.
    
    Returns:
        tuple[module, module]: (tree_sitter, tree_sitter_typescript)
        
    Raises:
        MissingNativeParserError: If either package cannot be imported.
    """
```

### 1.2 File Parser

```python
def parse_typescript_file(file_path: Path, rel_path: str, is_test: bool) -> IRModule:
    """Parse a TypeScript or TSX file into an IRModule using Tree-Sitter.
    
    Args:
        file_path: Absolute or resolved Path to the source file.
        rel_path: POSIX-style repository-relative path.
        is_test: True if file matches test file path conventions.
        
    Returns:
        IRModule: Populated with classes, functions, imports, LOC, and telemetry.
        
    Raises:
        MissingNativeParserError: If tree-sitter-typescript is missing.
    """
```

---

## 2. Profile Interface Contract (`scripts/_code_health/profiles_ts.py`)

```python
class TypeScriptLanguageProfile(JavaScriptLanguageProfile):
    """Evaluates TypeScript-specific clean code, type safety, and security rules."""

    def __init__(self) -> None:
        super().__init__()
        self.name = "typescript"
        self.file_extensions = (".ts", ".tsx", ".mts", ".cts")

    def evaluate_function(self, func: IRFunction, parent: IRClass | None) -> list[RulePenalty]:
        """Evaluate TypeScript function/method penalties.
        
        Evaluates:
            - Explicit 'any' usage (-5.0 pts each, cap -20.0 pts)
            - Compiler suppression directives @ts-ignore/@ts-nocheck (-10.0 pts each, cap -20.0 pts)
            - Non-null assertions '!' (-2.0 pts each, cap -10.0 pts)
            - SQL/query string concatenation/template literal interpolation (-40.0 pts)
            - Inherited ECMAScript hygiene (var, loose ==/!=, empty catch, debugger, eval, proto)
            
        Returns:
            list[RulePenalty]: List of applied rule penalties with line numbers.
        """

    def evaluate_class(self, cls: IRClass) -> list[RulePenalty]:
        """Evaluate class-level architectural rules."""

    def is_test_assert_call(self, call_name: str) -> bool:
        """Recognize standard assertion matchers."""
```

---

## 3. Resolver Contract (`scripts/_code_health/profiles.py`)

```python
def resolve_active_profiles(
    repo_root: Path,
    file_path: Path,
    lang_override: str | None = None,
    framework_override: str | None = None,
) -> LanguageProfile:
    """Resolve active LanguageProfile for target file.
    
    Resolution order:
        1. lang_override == "typescript" or "ts" -> TYPESCRIPT_PROFILE
        2. lang_override == "javascript" or "js" -> JAVASCRIPT_PROFILE
        3. lang_override is None:
            - file_path.suffix in {".ts", ".tsx", ".mts", ".cts"} -> TYPESCRIPT_PROFILE
            - file_path.suffix in {".js", ".mjs", ".cjs"} -> JAVASCRIPT_PROFILE
            - file_path.suffix == ".java" -> JAVA_PROFILE
            - default -> PYTHON_PROFILE
    """
```
