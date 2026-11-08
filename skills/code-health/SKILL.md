---
name: code-health
description: Generic multi-language code health analyzer (Python, Java, Spring Boot) evaluating deterministic SRP, size, complexity, clean code, and security scorecards.
---

# Deterministic Multi-Language Code Health

Use this skill to inspect, grade, and iteratively refactor **Python** and **Java** (including **Spring Boot**) code against an objective, deterministic 0–100 engineering rubric across five dimensions:
1. **Single Responsibility & Cohesion (SRP) — 30%**
2. **Size & Readability — 25%**
3. **Complexity & Control Flow — 20%**
4. **Clean Code & Maintainability — 15%**
5. **Security & Boundary Hygiene — 10%**

---

## Quick Reference & Commands

The analyzer scripts are bundled inside this skill's `scripts/` folder:

```bash
# 1. Fast inner-loop check on a single modified file (sub-second AST/CST check)
python <path-to-skill>/scripts/code_health.py path/to/File.java --no-git

# 2. Focus on a specific class or method
python <path-to-skill>/scripts/code_health.py path/to/File.java --symbol OrderService.processOrder --no-git

# 3. Quality-gate threshold (exits 1 if score < 90.0)
python <path-to-skill>/scripts/code_health.py src/main/java --only-flagged --fail-under 90.0 --no-git

# 4. Multi-language repository scan (Python + Java) with Git churn analysis
python <path-to-skill>/scripts/code_health.py src tests --format console

# 5. Language or framework profile override
python <path-to-skill>/scripts/code_health.py src --lang java --framework spring-boot --no-git
```

> [!TIP]
> **Locating the script:**
> - Inside this repository: `python scripts/code_health.py`.
> - From global skills (`~/.gemini/config/skills/code-health`): `python ~/.gemini/config/skills/code-health/scripts/code_health.py`.
> - If copied to project `.agents/skills/code-health`: `python .agents/skills/code-health/scripts/code_health.py`.

---

## Language & Framework Auto-Detection

The analyzer automatically detects language and framework context without requiring manual flags:
- **Language Detection:** Inferred from file extensions (`.py` $\to$ Python, `.java` $\to$ Java).
- **Spring Boot Framework Detection:** Automatically enabled when:
  1. File source contains `org.springframework` imports or Spring annotations (`@RestController`, `@Service`, `@SpringBootApplication`).
  2. Workspace contains `pom.xml`, `build.gradle`, or `build.gradle.kts` referencing `spring-boot` or `org.springframework`.

### CLI Overrides

Override automatic detection when necessary:
- `--lang {auto,python,java}`: Restrict discovery to a specific language.
- `--framework {auto,spring-boot,python-cli-mcp,none}`: Force or disable framework rules (e.g., `--framework none` for vanilla Java).

---

## Mandatory Native Parser Gate (Java Analysis)

To guarantee 100% syntactic precision, Java code health analysis requires the native Tree-Sitter parser (`tree-sitter-java`). There is **no fallback parser**.

If `tree-sitter-java` is missing when analyzing Java code, the CLI halts with **exit code 2** and emits a clear banner:

```text
[WARNING] Native Java AST parser ('tree-sitter-java') is not installed.
To analyze Java files, install the native parser dependencies:
  • uv (ephemeral): uv run --with tree-sitter --with tree-sitter-java python scripts/code_health.py <paths>
  • uv (project):   uv pip install "tree-sitter>=0.23.0" "tree-sitter-java>=0.23.0"
  • pip:            pip install "py-code-health[java]"  (or: pip install tree-sitter tree-sitter-java)
```

In JSON mode (`--format json`), the CLI returns:
```json
{
  "status": "missing_native_parser",
  "language": "java",
  "missing_packages": ["tree-sitter", "tree-sitter-java"],
  "install_commands": {
    "uv_ephemeral": "uv run --with tree-sitter --with tree-sitter-java python scripts/code_health.py",
    "uv_project": "uv pip install 'tree-sitter>=0.23.0' 'tree-sitter-java>=0.23.0'",
    "pip": "pip install 'py-code-health[java]'"
  },
  "message": "[WARNING] Native Java AST parser ('tree-sitter-java') is not installed..."
}
```

> [!IMPORTANT]
> **Pure Python files never trigger the Java parser warning.** Python analysis has zero external dependencies and runs out of the box on standard Python 3.11+.

---

## Grade Scale

- **Grade A (90.0 – 100.0):** Healthy, cohesive, clean code. Target for all production code.
- **Grade B (80.0 – 89.9):** Minor smells or slightly long methods. Easy to polish to Grade A.
- **Grade C (70.0 – 79.9):** Moderate smells (e.g. mixed concerns, high cognitive complexity).
- **Grade D / F (< 70.0):** Architectural violations, God classes, deep nesting, or SQL injection risks.

---

## References & Playbooks

- [Scoring Rubric Reference](references/scoring-rubric.md): Detailed mathematical models, metric thresholds, and penalty weights across Python and Java.
- [Spring Boot Refactoring Playbook](references/java-spring-playbook.md): Before/after refactoring patterns for `@Autowired`, controller layering, `@Transactional`, and SQL parameterization.
