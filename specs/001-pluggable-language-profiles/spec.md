# Feature Specification: Pluggable Language & Framework Profiles (Java & Spring Boot)

**Feature Branch**: `001-pluggable-language-profiles`

**Created**: 2026-11-08

**Status**: Draft

**Input**: User description: "create a formal Spec Kit specification for the pluggable multi-language (Java/Spring Boot) feature, referencing the plan (tree-sitter-java only, no fallback parser)"

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Automatic Multi-Language Code Health Evaluation (Priority: P1)

As a developer or AI coding agent working across polyglot repositories, I want to run the code health analyzer on any source file or project folder without manually specifying the programming language, so that I receive an immediate, objective 0–100 health scorecard with exact line-numbered findings.

**Why this priority**: Core foundation of the tool. Without automatic file discovery and language identification, users face friction switching between Python, Java, or mixed repositories.

**Independent Test**: Can be tested independently by running `python scripts/code_health.py` against a Python file, a Java file, and a mixed directory, verifying each is automatically mapped to its correct language profile and scored accurately.

**Acceptance Scenarios**:

1. **Given** a directory containing `.java` source files and `tree-sitter-java` installed, **When** the user runs `code_health.py` pointing to the directory, **Then** the system automatically detects the `java` language, parses the full Concrete Syntax Tree via `tree-sitter-java`, applies Java metric rubrics (LOC, Cyclomatic Complexity, Javadoc hygiene, and class cohesion), and outputs a composite scorecard with letter grade.
2. **Given** a Python repository with existing `.py` files, **When** `code_health.py` is invoked with standard arguments, **Then** all legacy Python analysis, CLI arguments, and output structures behave with 100% backward compatibility using Python's standard library `ast`.
3. **Given** a mixed project with both `.py` and `.java` source files, **When** the analyzer scans the root, **Then** both language files are discovered, evaluated using their respective rules, and rolled up into a unified codebase scorecard.

---

### User Story 2 - Mandatory Native Parser Warning & Installation Prompt (Priority: P2)

As a developer or agent analyzing Java code in an environment lacking native parser packages (`tree-sitter` and `tree-sitter-java`), I want a prominent warning explaining that full-fidelity Java AST analysis requires `tree-sitter-java` alongside copy-paste installation commands, so that I can install the required packages without guessing package names or flags.

**Why this priority**: Essential developer clarity and parse fidelity. Heuristic/fallback parsers are strictly prohibited for Java to guarantee 100% AST accuracy for modern Java syntax (records, switch expressions, lambdas, and implicit field references).

**Independent Test**: Can be tested by running the analyzer on a Java file in a clean Python environment without `tree-sitter-java`. Verify that the process halts with exit code 2 and outputs the installation guide, and upon installing `tree-sitter` and `tree-sitter-java`, successfully analyzes the code.

**Acceptance Scenarios**:

1. **Given** an environment without `tree-sitter-java` installed, **When** the user runs `code_health.py` on a Java file or directory containing `.java` files, **Then** the process halts with exit code `2`, surfaces a warning banner explaining that native AST analysis via `tree-sitter-java` is required, and displays exact commands for `uv` and `pip` to install the dependencies.
2. **Given** an environment without `tree-sitter-java` installed, **When** the user runs `code_health.py` on purely Python files, **Then** the process executes normally using the built-in standard library `ast` parser without displaying any missing Java parser warnings.
3. **Given** JSON output mode (`--format json`) and missing `tree-sitter-java` packages when targeting Java, **Then** the command outputs valid JSON containing `"status": "missing_native_parser"` and the required installation commands before exiting with code 2.

---

### User Story 3 - Framework-Aware Architectural Health for Spring Boot (Priority: P3)

As a software engineer developing Spring Boot microservices, I want the code health scorecard to recognize framework-specific stereotypes, annotations, and architectural boundaries, so that bad practices (such as field injection, layer violations, and query concatenation) are explicitly flagged with actionable remedies.

**Why this priority**: Generic OOP metrics miss framework-specific smells that degrade maintainability in Spring Boot applications. Layer leakage and proxy misunderstandings are primary sources of technical debt.

**Independent Test**: Can be tested by evaluating sample Spring Boot classes (`@RestController`, `@Service`, `@Repository`) containing known anti-patterns and confirming the analyzer flags each with exact penalty deductions.

**Acceptance Scenarios**:

1. **Given** a Spring Boot class declaring `@Autowired` on private fields, **When** evaluated, **Then** the analyzer deducts points from Clean Code and outputs a finding recommending constructor injection.
2. **Given** a `@RestController` class directly injecting a `@Repository` or `EntityManager`, **When** analyzed, **Then** the analyzer flags a Single Responsibility / Layering violation (-20 pts) recommending routing database access through a `@Service` layer.
3. **Given** a method annotated with `@Transactional` on a private method or on a `@RestController`, **When** analyzed, **Then** the analyzer flags the invalid transaction boundary.
4. **Given** a data access method executing `JdbcTemplate` or `EntityManager` queries constructed with string concatenation (`+` or `String.format`), **When** analyzed, **Then** the Security dimension penalizes the method (-40 pts) for potential SQL/JPQL injection.
5. **Given** a controller endpoint with up to 6 parameters annotated with `@RequestParam`, `@PathVariable`, or `@RequestBody`, **When** analyzed, **Then** parameter count limits are relaxed for web entrypoints without triggering function size penalties.

---

### User Story 4 - Multi-Language Quality Gates and CI Integration (Priority: P4)

As a tech lead or CI/CD engineer, I want to enforce minimum score thresholds across polyglot microservices, so that PRs introducing high complexity or architectural debt in either Python or Java are caught automatically.

**Why this priority**: Enables automated enforcement of engineering standards in CI pipelines across diverse repositories.

**Independent Test**: Can be tested by executing `code_health.py` with `--fail-under 90.0` against clean and smell-laden Java/Spring codebases and verifying correct non-zero return codes.

**Acceptance Scenarios**:

1. **Given** a Java repository scoring an overall composite of `88.5`, **When** executed with `--fail-under 90.0`, **Then** the tool outputs the scorecard and exits with code `1`.
2. **Given** a test suite in `src/test/java/`, **When** analyzed, **Then** standard test conventions (`*Test.java`, `@Test`, `@ParameterizedTest`, MockMvc `.andExpect()`, and AssertJ `assertThat()`) are recognized so test assertion rules evaluate accurately without false positives.

---

### Edge Cases

- **Mixed-Language Files in a Single Repo**: The analyzer must group and aggregate files across different languages into a cohesive top-level summary while preserving language-specific findings.
- **Empty or Package-Only Java Files**: Files containing only `package-info.java` or empty interface markers must be graded 100.0 (Grade A) without penalty.
- **Non-Standard Directory Layouts**: Java files located outside standard Maven/Gradle structures (e.g. flat directories or scratch scripts) must still be identified and parsed via file extension.
- **Novel Java Syntax (Java 17–21+)**: Source files using `record`, sealed classes, text blocks, pattern matching, and switch expressions must parse with high fidelity via `tree-sitter-java`.
- **Lombok and Code-Generation Annotations**: Classes annotated with `@Data`, `@Value`, `@Builder`, or `@NoArgsConstructor` must receive LCOM4 class cohesion exemptions matching Python dataclasses.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST automatically detect the programming language of target files based on file extension (`.py` for Python, `.java` for Java) unless explicitly overridden via `--lang`.
- **FR-002**: System MUST automatically detect the presence of the Spring Boot framework when analyzing Java projects by checking for build configuration files (`pom.xml`, `build.gradle`, `build.gradle.kts`) containing Spring Boot dependencies, or package imports starting with `org.springframework`.
- **FR-003**: System MUST require native `tree-sitter` and `tree-sitter-java` CST parsing for all Java language analysis. Heuristic or fallback parsing for Java is strictly forbidden.
- **FR-004**: When analyzing Java files in an environment where `tree-sitter` or `tree-sitter-java` is not installed:
  - The system MUST print a prominent warning explaining that native AST parsing via `tree-sitter-java` is required.
  - The system MUST provide exact `uv` and `pip` installation commands.
  - The system MUST halt and exit with code `2`.
- **FR-005**: In JSON output mode (`--format json`), if `tree-sitter-java` is missing when targeting Java, the system MUST emit valid JSON containing `"status": "missing_native_parser"`, missing package names, and installation commands, exiting with code 2.
- **FR-006**: System MUST translate parsed source structures into a unified Intermediate Representation (`IRModule`, `IRClass`, `IRFunction`, `IRField`, `IRCall`, `IRAnnotation`) before evaluating metrics.
- **FR-007**: System MUST evaluate Java code against the universal 5-dimension rubric:
  - Single Responsibility & Cohesion (30%)
  - Size & Readability (25%)
  - Complexity & Control Flow (20%)
  - Clean Code & Maintainability (15%)
  - Security & Operational Hygiene (10%)
- **FR-008**: System MUST compute LCOM4 class cohesion for Java classes by resolving both explicit (`this.field`) and implicit field references against declared class fields.
- **FR-009**: System MUST exempt Java `record` types, `enum` types, and classes annotated with `@Entity`, `@Data`, `@Value`, `@Configuration`, or `@ConfigurationProperties` from LCOM4 cohesion penalties.
- **FR-010**: System MUST enforce Spring Boot architectural rules when the `spring-boot` profile is active:
  - Penalize field injection using `@Autowired` or `@Inject` on class fields (-8 pts per field).
  - Penalize `@RestController` or `@Controller` classes that directly inject `@Repository` or `EntityManager` (-20 pts).
  - Penalize `@Transactional` annotations placed on `@RestController` classes or `private` methods (-15 to -20 pts).
  - Penalize string-concatenated SQL/JPQL queries passed to `JdbcTemplate` or `EntityManager` (-40 pts).
- **FR-011**: System MUST relax parameter limits from $\le 4$ to $\le 6$ for web entrypoints annotated with `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`, `@RequestMapping`, `@Bean`, or `@KafkaListener`.
- **FR-012**: System MUST recognize Java test directories (`src/test/java/`, `test/`) and test naming conventions (`*Test.java`, `*Tests.java`, `*IT.java`), exempting test files from source SRP rules.
- **FR-013**: System MUST detect assertions in Java tests, recognizing JUnit 5 (`assertEquals`, `assertTrue`, `assertThrows`), AssertJ (`assertThat`), Mockito (`verify`), and MockMvc (`andExpect`).
- **FR-014**: System MUST support Git commit churn and co-change coupling analysis across `.java` files identically to `.py` files when Git history is enabled.
- **FR-015**: System MUST maintain 100% backward compatibility for existing Python AST analysis functions and CLI invocations.

---

### Key Entities

- **LanguageProfile**: Configuration and hook provider specifying file extensions, standard library exclusions, comment/docstring patterns, test path conventions, and language-specific clean code checkers.
- **FrameworkProfile**: Layered architectural rule provider defining domain concern mappings, entrypoint decorators/annotations, cohesion exemptions, and framework anti-pattern checks.
- **IRModule / IRClass / IRFunction**: Language-neutral structural units representing code elements, their metrics, annotations, dependencies, and control-flow graphs.
- **ParserGuard**: Subsystem responsible for verifying `tree-sitter-java` availability, generating installation instructions, and halting execution when packages are absent.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of existing unit tests in `tests/unit/test_code_health.py` pass without modification.
- **SC-002**: A developer analyzing a Java or Spring Boot project with `tree-sitter-java` installed receives a complete, deterministic scorecard in under 2 seconds on a typical single file (sub-second AST check) and under 15 seconds for a 50-file repository.
- **SC-003**: 100% of Spring Boot anti-patterns specified in User Story 3 (field injection, direct repository injection in controllers, transaction boundary misuse, and SQL string concatenation) trigger exact line-numbered findings with penalty explanations.
- **SC-004**: When optional native Java dependencies (`tree-sitter-java`) are missing, the analyzer guarantees zero silent failures or imprecise parsing: 100% of invocations halt with exit code `2` and display clear copy-paste installation instructions.
- **SC-005**: All new Python modules introduced into `scripts/_code_health/` achieve a self-health composite score $\ge 90.0$ (Grade A) with zero critical findings.

---

## Assumptions

- **Target Java Versions**: Targets modern Java conventions (Java 11 through Java 21+), including records, switch expressions, and text blocks parsed via `tree-sitter-java`.
- **Build Tools**: Automatically recognizes Maven (`pom.xml`) and Gradle (`build.gradle`, `build.gradle.kts`) project roots.
- **Optional Native Dependencies**: Core Python analysis remains 100% zero-dependency. Java analysis requires `tree-sitter` and `tree-sitter-java` as documented optional extras (`py-code-health[java]`).
- **Cross-Platform Compatibility**: All file discovery, path normalization, and CLI options work identically across Windows, macOS, and Linux.
