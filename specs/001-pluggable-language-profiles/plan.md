# Implementation Plan: Pluggable Language & Framework Profiles (Java & Spring Boot)

**Branch**: `001-pluggable-language-profiles` | **Date**: 2026-11-08 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-pluggable-language-profiles/spec.md`

---

## Summary

Extend the deterministic code health analyzer into a multi-language, framework-aware engine by introducing a normalized Intermediate Representation (IR), a pluggable Profile system (`LanguageProfile` for Python and Java; `FrameworkProfile` for Spring Boot), and a native `tree-sitter-java` parser. When optional native grammar dependencies (`tree-sitter` and `tree-sitter-java`) are absent, the CLI returns a structured warning with installation instructions and halts (exit code 2) prompting the user to install them. Fallback/heuristic parsing for Java is explicitly omitted to ensure 100% parse precision and metric fidelity.

---

## Technical Context

**Language/Version**: Python 3.11+ (Runtime and analyzer engine)  
**Target Languages Evaluated**: Python (`.py`), Java 11–21+ (`.java`)  
**Primary Dependencies**:  
- Core analyzer: Zero external dependencies (Python stdlib: `ast`, `dataclasses`, `re`, `subprocess`, `pathlib`, `json`, `tomllib`).  
- Optional native Java grammar extras: `tree-sitter>=0.23.0`, `tree-sitter-java>=0.23.0`.  
**Storage**: File-based reports (`JSON`, `Markdown`, console stdout).  
**Testing**: `pytest>=8.0.0` with mock/AST fixtures; dogfooding self-health check via `code_health.py`.  
**Target Platform**: Cross-platform (Windows, macOS, Linux).  
**Project Type**: Standalone CLI tool + Antigravity agent skill.  
**Performance Goals**: Sub-second inner-loop AST check on single files (<1.0s); <15 seconds for a 50-file repository.  
**Constraints**: Zero hard external dependencies for core Python usage; 100% backward compatibility for existing Python test suites.  
**Scale/Scope**: 5 core metrics modules, 2 language profiles, 2 framework profiles, ~250 unit test assertions.

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Library-First**: The analyzer engine is decoupled into modular components (`ir_models`, `profiles`, `java_parser`, `ir_scorer`, `module_engine`, `reporting`) with clean programmatic APIs. **Status: PASS.**
- **Principle II: CLI Interface**: Clean text in/out protocol supporting `--format console`, `--format json`, `--format markdown`, standard exit codes (0, 1, 2), and stderr/stdout separation. **Status: PASS.**
- **Principle III: Test-First & Deterministic Quality**: Full pytest unit test suite covering AST parsing, profile detection, missing parser gate, Spring Boot rules, and self-health dogfooding $\ge 90.0$ (Grade A). **Status: PASS.**
- **Principle IV: Backward Compatibility**: Existing Python public API and CLI invocations remain unchanged. **Status: PASS.**

---

## Project Structure

### Documentation (this feature)

```text
specs/001-pluggable-language-profiles/
├── spec.md              # Feature specification
├── plan.md              # This file (/speckit-plan output)
├── research.md          # Phase 0: Technology decisions & tradeoffs
├── data-model.md        # Phase 1: IR & Profile entity definitions
├── quickstart.md        # Phase 1: Validation and verification guide
├── contracts/           # Phase 1: CLI and Profile interfaces
│   ├── cli-contract.md
│   └── profile-contract.md
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2: Actionable tasks (/speckit-tasks output)
```

### Source Code (repository root)

```text
py-code-health/
├── pyproject.toml                         # Add optional [project.optional-dependencies] java
├── scripts/
│   ├── code_health.py                     # CLI entrypoint with --lang, --framework
│   └── _code_health/
│       ├── __init__.py
│       ├── models.py                      # Core reporting and rubric models
│       ├── ir_models.py                   # Unified Intermediate Representation (IR)
│       ├── profiles.py                    # Language & Framework Profile registries & auto-detection
│       ├── java_parser.py                 # Tree-sitter-java parser + Missing native parser guard
│       ├── ir_scorer.py                   # Universal 5-dimension scorer executing profile rules
│       ├── ast_engine.py                  # Python-native AST scorer (legacy compatibility & IR adapter)
│       ├── module_engine.py               # File dispatcher and multi-language Git churn tracking
│       └── reporting.py                   # Multi-language discovery, package inference & formatters
├── skills/
│   ├── code-health/                       # Generic auto-detecting agent skill
│   │   ├── SKILL.md
│   │   ├── references/
│   │   │   ├── python-playbook.md
│   │   │   ├── java-spring-playbook.md
│   │   │   └── scoring-rubric.md
│   │   └── scripts/ -> synced with scripts/
│   └── python-code-health/                # Preserved for backward compatibility
└── tests/
    └── unit/
        ├── test_code_health.py            # Existing Python regression suite
        └── test_java_spring_health.py     # New Java, Spring Boot, parser gate & multi-language tests
```

**Structure Decision**: Modular extension inside `scripts/_code_health/`, maintaining a single unified CLI entrypoint at `scripts/code_health.py` and syncing into `skills/code-health/` for agent usage.

---

## Complexity Tracking

*No constitutional violations identified. No unjustified architectural complexity.*
