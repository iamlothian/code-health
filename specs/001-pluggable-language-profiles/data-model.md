# Data Model: Pluggable Language & Framework Profiles

**Feature**: [spec.md](./spec.md) | **Date**: 2026-11-08

This document defines the language-neutral Intermediate Representation (IR), profile metadata models, and parser guard error models.

---

## 1. Unified Intermediate Representation (IR)

The analyzer decouples source language syntax parsing from metric scoring by transforming language ASTs into a normalized IR hierarchy:

```mermaid
classDiagram
    class IRModule {
        +str file_path
        +str language
        +bool is_test
        +int loc
        +List~str~ imports
        +List~IRClass~ classes
        +List~IRFunction~ functions
        +str parser_backend
    }

    class IRClass {
        +str name
        +str qualname
        +int lineno
        +int end_lineno
        +int loc
        +List~IRAnnotation~ annotations
        +List~str~ base_types
        +List~IRField~ fields
        +List~IRFunction~ methods
        +int lcom4
    }

    class IRFunction {
        +str name
        +str qualname
        +int lineno
        +int end_lineno
        +int loc
        +List~IRAnnotation~ annotations
        +List~IRParam~ params
        +str return_type
        +int max_nesting
        +int cyclomatic_complexity
        +int cognitive_complexity
        +int returns_count
        +List~IRCall~ calls
        +List~str~ accessed_fields
        +List~IRExceptHandler~ except_handlers
        +bool is_test
    }

    class IRAnnotation {
        +str name
        +Dict~str, Any~ args
        +int lineno
    }

    class IRParam {
        +str name
        +str type_annotation
        +bool has_default
        +List~IRAnnotation~ annotations
    }

    class IRField {
        +str name
        +str type_annotation
        +List~IRAnnotation~ annotations
        +int lineno
    }

    class IRCall {
        +str name
        +str callee_symbol
        +int lineno
        +bool has_string_concat
    }

    class IRExceptHandler {
        +str exception_type
        +bool is_empty
        +bool is_broad
        +int lineno
    }

    IRModule "1" *-- "many" IRClass
    IRModule "1" *-- "many" IRFunction
    IRClass "1" *-- "many" IRField
    IRClass "1" *-- "many" IRFunction
    IRClass "1" *-- "many" IRAnnotation
    IRFunction "1" *-- "many" IRParam
    IRFunction "1" *-- "many" IRCall
    IRFunction "1" *-- "many" IRAnnotation
    IRFunction "1" *-- "many" IRExceptHandler
```

---

## 2. Profile Contracts

### `LanguageProfile`
Encapsulates language-level parsing rules and metric customizations:
- `name: str` (e.g., `"python"`, `"java"`).
- `file_extensions: tuple[str, ...]` (e.g., `(".java",)`).
- `comment_prefixes: tuple[str, ...]` (e.g., `("//", "/*", "*/", "*")`).
- `test_path_patterns: tuple[str, ...]` (e.g., `("src/test/java", "*Test.java", "*Tests.java")`).
- `parse(file_path: Path, rel_path: str, is_test: bool) -> IRModule`.
- `score_clean_code_hooks(func: IRFunction, ctx: AnalysisContext) -> tuple[float, list[str]]`.

### `FrameworkProfile`
Layered architectural rules that plug into a language profile:
- `name: str` (e.g., `"spring-boot"`, `"python-cli-mcp"`).
- `target_language: str` (e.g., `"java"`, `"python"`).
- `concern_map: dict[str, str]` (maps method calls/types to concern buckets).
- `entrypoint_annotations: set[str]` (e.g., `{"GetMapping", "PostMapping", "Bean"}`).
- `lcom4_exempt_annotations: set[str]` (e.g., `{"Entity", "Data", "Configuration"}`).
- `evaluate_function(func: IRFunction, parent_class: IRClass | None) -> list[RulePenalty]`.
- `evaluate_class(cls: IRClass) -> list[RulePenalty]`.

---

## 3. Parser Guard & Error Models

### `MissingNativeParserError`
Raised when a target language requires native grammar packages (`tree-sitter` and `tree-sitter-java`) that are absent from the environment:
- `language: str`: Name of the target language (`"java"`).
- `missing_packages: list[str]`: Packages required (`["tree-sitter", "tree-sitter-java"]`).
- `install_instructions: dict[str, str]`: Exact commands for `uv run`, `uv pip`, and `pip`.
- `message: str`: Formatted explanation for the user.
