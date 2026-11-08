# Research: Pluggable Language & Framework Profiles (Java & Spring Boot)

**Feature**: [spec.md](./spec.md) | **Date**: 2026-11-08

This document records the research findings, technical tradeoffs, and architectural decisions made to support multi-language code health analysis and Spring Boot architectural checks.

---

## 1. Parser Strategy & Java AST Extraction

### Decision
Require **Native `tree-sitter-java` CST Parsing Only** for Java analysis; strictly reject fallback/heuristic parsers:
1. **Native AST Parsing**: Use `tree-sitter` and `tree-sitter-java` (installed via optional extra `py-code-health[java]`) for full-fidelity Concrete Syntax Tree (CST) parsing of Java 8–21+ syntax (records, switch expressions, text blocks, lambdas, annotations, and member references).
2. **Missing Parser Warning & Prompt**: When `.java` files are targeted in an environment without `tree-sitter-java`, the CLI surfaces a prominent warning detailing why native AST analysis is required, outputs copy-paste installation commands (`uv` / `pip`), and halts with exit code `2`.
3. **No Fallback Parser**: A heuristic regex/token fallback is explicitly rejected to ensure 100% deterministic, high-assurance metrics without approximations.

### Rationale
- Python standard library includes `ast` out of the box, which makes Python analysis zero-dependency. Java has no standard library AST parser in Python.
- `tree-sitter-java` provides 100% grammar accuracy for modern Java 17/21 features (pattern matching, switch expressions, records, compact constructors).
- Heuristic/regex parsers struggle with nested anonymous classes, multi-line lambda chains, and ternary operators, producing inaccurate complexity and LCOM4 scores. Requiring `tree-sitter-java` ensures identical rigor between Python and Java scorecards.
- Core Python analysis remains 100% zero-dependency, because `tree-sitter` is only loaded when `.java` files are encountered.

### Alternatives Considered
- **Dual-Mode with Regex/Heuristic Fallback**: Rejected per user requirement: imprecise fallback parsing risks inaccurate scoring and false positives on modern Java features.
- **Mandatory `tree-sitter` in core dependencies**: Rejected because it adds binary wheel installation overhead for users who only analyze Python projects.
- **External JVM CLI delegation (e.g. calling `javaparser` / `checkstyle`)**: Rejected because it requires a local JDK/JRE installation and slows down inner-loop sub-second checks.

---

## 2. Java LCOM4 Cohesion Graph Modeling

### Decision
Build an undirected graph for each Java class where vertices represent instance methods, and edges are added between $m_1$ and $m_2$ if:
1. Both methods access at least one common instance attribute (`field`).
2. Method $m_1$ calls $m_2$ (or vice versa).

In Java, class fields are accessed both explicitly (`this.myField`) and implicitly (`myField`). The Java adapter extracts all declared class-level field names first, then inspects method body tokens against this declared field set, correctly linking methods sharing instance state.

### Exemptions
LCOM4 penalties are waived (`LCOM4` set to 1) for:
- Java `record` declarations (data carriers).
- Java `enum` declarations.
- Classes with Lombok annotations (`@Data`, `@Value`, `@Getter`, `@Setter`).
- Spring `@Configuration`, `@ConfigurationProperties`, or JPA `@Entity` classes.
- Small classes with $\le 2$ methods.

---

## 3. Spring Boot Architectural Smell Detection

### Decision
Model Spring Boot as a composable `FrameworkProfile` with dedicated rule hooks attached to the Java language profile:

1. **Dependency Injection Hygiene (Clean Code -15%)**:
   - Field injection using `@Autowired` or `@Inject` on class fields deducts **-8.0 pts** per field. Finding recommends constructor injection for immutability and testability.
2. **Layering & Separation of Concerns (SRP -30%)**:
   - Controllers (`@RestController`, `@Controller`) injecting `*Repository`, `EntityManager`, or `JdbcTemplate` deduct **-20.0 pts**. Finding recommends encapsulating data access behind a `@Service` layer.
   - Controllers directly calling persistence methods (`.save(`, `.findById(`, `.delete(`, `.createQuery(`) deduct **-15.0 pts**.
3. **Transaction Boundary Hygiene (SRP / Clean Code)**:
   - `@Transactional` placed directly on a `@RestController` or on a `private` method deducts **-15.0 to -20.0 pts** (Spring AOP proxies do not intercept private method calls; controllers should not hold database transactions open).
4. **SQL/JPQL Injection Hygiene (Security -10%)**:
   - Calls to `JdbcTemplate.query/update/execute` or `EntityManager.createQuery/createNativeQuery` constructed using string concatenation (`+` operator or `String.format`) deduct **-40.0 pts**.
5. **Web Entrypoint Parameter Relaxations (Size -25%)**:
   - Methods annotated with `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`, `@RequestMapping`, `@Bean`, or `@KafkaListener` allow up to 6 parameters (annotated with `@RequestParam`, `@PathVariable`, `@RequestBody`) before applying parameter count penalties.

---

## 4. Test Framework Recognition & Assertion Hygiene

### Decision
The Java profile classifies files under `src/test/java/`, `test/`, or matching `*Test.java`, `*Tests.java`, `*IT.java` as test suites.
Test functions are identified by `@Test` or `@ParameterizedTest`.
Test assertions are recognized across popular Java testing libraries:
- **JUnit 5**: `assertEquals`, `assertTrue`, `assertFalse`, `assertNotNull`, `assertThrows`, `assertAll`.
- **AssertJ**: `assertThat(...)`.
- **Mockito**: `verify(...)`.
- **Spring MockMvc**: `mockMvc.perform(...).andExpect(...)`.
