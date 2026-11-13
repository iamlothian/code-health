# Deterministic Code Health Scoring Rubric & Reference Guide

This document defines the mathematical models, metric thresholds, penalty weights, and exemptions used by the deterministic Multi-Language Code Health Analyzer (`code_health.py`).

---

## 1. Core Principles

- **Deterministic & Reproducible:** Every function/method, class, and module receives a score from `0.0` to `100.0` and a letter grade calculated purely from AST / CST structure, line tokens, and Git history. Scores never vary across identical code states.
- **Actionable Penalty Findings:** Every deducted point generates a descriptive finding string with line numbers and penalty values (e.g. `LOC=45 (>25) (-30.0 pts)`), showing agents and engineers exactly what to refactor.
- **Language & Framework-Aware:** Zero-dependency stdlib AST parsing for Python (`ast`), and native Tree-Sitter CST parsing for Java (`tree-sitter-java`), JavaScript / JSX (`tree-sitter-javascript`), and TypeScript / TSX (`tree-sitter-typescript`), layered with framework profiles (`spring-boot`, `react`, `nextjs`, `angular`).
- **Mandatory Native Parser Gate:** Java, JavaScript, and TypeScript analysis require their respective native Tree-Sitter parsers with zero fallback parsing to guarantee 100% precision. Missing dependencies halt with exit code `2` and explicit copy-paste installation commands. Pure Python files require no external dependencies.

---

## 2. Composite Score Formula & Grade Scale

Every analyzed unit (function, class, file, or codebase) is evaluated across 5 weighted dimensions clamped to $[0.0, 100.0]$:

$$\text{Weighted Score} = 0.30 \cdot S_{\text{SRP}} + 0.25 \cdot S_{\text{Size}} + 0.20 \cdot S_{\text{Complexity}} + 0.15 \cdot S_{\text{Clean}} + 0.10 \cdot S_{\text{Security}}$$

**Worst-Dimension Ceiling (No Masking Critical Smells):**
If any single dimension drops below `75.0` ($S_{\min} < 75.0$), the composite score is capped so a severe architectural, complexity, or security defect cannot be masked into an overall Grade A or B:

$$\text{Composite Score} = \begin{cases} \min(\text{Weighted Score},\; S_{\min} + 5.0,\; 79.5) & \text{if } S_{\min} < 75.0 \\ \text{Weighted Score} & \text{otherwise} \end{cases}$$

| Dimension | Weight | Primary Focus |
| :--- | :---: | :--- |
| **SRP & Cohesion ($S_{\text{SRP}}$)** | **30%** | Single responsibility, concern domain isolation, external call fan-out, boolean flag parameters, layering violations, and class LCOM4. |
| **Size & Readability ($S_{\text{Size}}$)** | **25%** | Effective non-blank, non-comment lines of code (LOC), parameter count, and maximum nesting depth. |
| **Complexity & Control Flow ($S_{\text{Complexity}}$)** | **20%** | Cyclomatic complexity (CC), cognitive complexity (CogC), and return statement count. |
| **Clean Code & Maintainability ($S_{\text{Clean}}$)** | **15%** | Type annotations, TS type safety, docstrings/JSDoc/Javadoc, exception & DI hygiene, UI hook/lifecycle hygiene, and test assertion quality. |
| **Security & Boundary Hygiene ($S_{\text{Security}}$)** | **10%** | SQL injection, unsafe execution/deserialization, XSS/DOM sinks, client/server boundaries, subprocess safety, path confinement, and transactional Git mutations. |

### Letter Grade Scale

| Grade | Score Range | Description | Target Recommendation |
| :---: | :---: | :--- | :--- |
| **A** | **90.0 – 100.0** | **Healthy / Clean Code** | Excellent design; passes all strict quality gates. Target for all production code. (`95.0+` for high-assurance core libraries.) |
| **B** | **80.0 – 89.9** | **Good Quality** | Minor design smells; acceptable for production, minor cleanup recommended. |
| **C** | **70.0 – 79.9** | **Moderate Smell** | Multiple smells or high complexity; refactoring recommended before merge. |
| **D** | **60.0 – 69.9** | **Unhealthy / High Risk** | Significant architectural violations; refactoring required. |
| **F** | **< 60.0** | **Critical Hotspot** | Severe God-class, extreme bloat, or security risks; immediate refactoring needed. |

---

## 3. Function & Method Rubric

Starts at `100.0` in each dimension and applies deductions.

### 3.1 Single Responsibility & Cohesion ($S_{\text{SRP}}$, 30%)
*(Tests are exempt from SRP checks and score 100.0)*

1. **Concern Domain Mixing:**
   Functions are scanned for distinct operational concerns across predefined buckets:
   - Python: `presentation`, `cli_or_rpc_framework`, `filesystem_io`, `subprocess_git`, `serialization`, `domain_computation`.
   - Java / Spring Boot: `http_transport` (`ResponseEntity`, `HttpServletRequest`), `persistence_db` (`JdbcTemplate`, `EntityManager`, `JpaRepository`), `external_client` (`RestTemplate`, `WebClient`, `KafkaTemplate`), `serialization` (`ObjectMapper`), `filesystem_io` (`Files.readString`, `Files.writeString`).
   - Web UI (React / Next.js / Angular): `network_io` (`fetch`, `axios`, `HttpClient`), `storage_io` (`localStorage`, `sessionStorage`), `dom_mutation` (`document.*`, `window.open`), `presentation` (`console.*`), and `render_ui` (functions constructing/returning JSX).
   - **Penalty:** If distinct concerns > 2, deduct **-12.0 pts** per concern over 2:
     $$\text{Penalty} = (\text{concerns} - 2) \cdot 12.0$$

2. **External Call Fan-Out:**
   Counts distinct external non-stdlib function/method calls:
   - **Penalty:** If external calls > 6, deduct **-3.0 pts** per excess call (capped at -36.0 pts):
     $$\text{Penalty} = \min(36.0, (\text{ext\_calls} - 6) \cdot 3.0)$$

3. **Boolean Default Flag Parameters:**
   Functions taking boolean parameters with default values indicate violating SRP by executing two distinct branches.
   - *(CLI / RPC / Web entrypoint decorators like `@app.command`, `@mcp.tool`, `@GetMapping`, `@HostListener` are exempt).*
   - **Penalty:** Deduct **-6.0 pts** per boolean default parameter.

4. **Spring Boot Architectural Layering (Framework Profile):**
   - `@RestController` or `@Controller` directly injecting a `@Repository` / `*Repository` field: Deduct **-20.0 pts** from SRP.
   - `@Transactional` placed on web controllers: Deduct **-15.0 pts** from SRP.
   - `@Transactional` placed on `private` methods: Deduct **-15.0 pts** from SRP.

5. **React & Angular SRP Rules (UI Framework Profiles):**
   - **React Effect Sprawl:** $> 2$ `useEffect` / `useLayoutEffect` calls in a non-custom-hook function: Deduct **-8.0 pts** per excess call (capped at -24.0 pts).
   - **React State Sprawl:** $> 5$ `useState` calls in a non-custom-hook function: Deduct **-5.0 pts** per excess call (capped at -20.0 pts).
   - **Angular Layering:** `@Component` or `@Directive` injecting `HttpClient` directly instead of delegating to a service: Deduct **-20.0 pts** from SRP (class-level).

---

### 3.2 Size & Readability ($S_{\text{Size}}$, 25%)

1. **Effective Lines of Code (LOC):**
   Calculated strictly on executable statements (excluding blanks, comments, and docstring/Javadoc/JSDoc spans).
   - **Source code (`src/`):**
     - Ideal: $\le 25$ LOC.
     - Between 26 and 50 LOC: **-1.5 pts / line**.
     - Above 50 LOC: **-2.5 pts / line**.
   - **Test code (`tests/` / `src/test/java/` / `*.test.*` / `*.spec.*` / `__tests__/`):**
     - Ideal: $\le 40$ LOC.
     - Between 41 and 75 LOC: **-1.0 pt / line**.
     - Above 75 LOC: **-2.0 pts / line**.

2. **Parameter Count ($N_{\text{params}}$, excluding `self` / `cls`):**
   - Standard functions/methods: Ideal $\le 4$ parameters.
   - Web / CLI / RPC entrypoints (`@GetMapping`, `@PostMapping`, `@app.command`, `@mcp.tool`, `@HostListener`): Ideal $\le 6$ parameters.
   - **Penalty:** Deduct **-6.0 pts** per parameter exceeding the threshold.

3. **Max Nesting Depth ($D_{\text{nest}}$):**
   Depth of control flow structures (`if`, `for`, `while`, `try`, `switch`, `match`).
   - Ideal: $\le 3$ levels.
   - **Penalty:** Deduct **-10.0 pts** per nesting level above 3.

---

### 3.3 Complexity & Control Flow ($S_{\text{Complexity}}$, 20%)

1. **Cyclomatic Complexity (CC):**
   Branches evaluated: `1 + count(if, for, while, catch/except, switch cases, compound boolean operators)`.
   - Ideal: $\le 5$.
   - Between 6 and 10 CC: **-4.0 pts / point**.
   - Above 10 CC: **-7.0 pts / point**.

2. **Cognitive Complexity (CogC):**
   Penalizes nested control structures by nesting depth ($+1 + \text{depth}$ for `if`/`for`/`while`/`catch`/`switch`), $+1$ for `else`/`default`, and $+1$ for compound boolean chains.
   - Ideal: $\le 8$.
   - **Penalty:** Deduct **-2.5 pts** per point over 8.

3. **Return Statement Count:**
   - Ideal: $\le 3$ return statements.
   - **Penalty:** Deduct **-4.0 pts** per return statement above 3.

---

### 3.4 Clean Code & Maintainability ($S_{\text{Clean}}$, 15%)

1. **Type Annotations & Defaults:**
   - **Python & TypeScript Source:** Missing return type annotation: **-10.0 pts** (exempt for dunder methods like `__init__`, and PascalCase JSX-returning UI components in React/Next.js); untyped parameter (excluding `self`/`cls`): **-5.0 pts** each (capped at -25.0 pts).
   - **JavaScript Source:** Parameter defaults (`param = default`) and JSDoc `@param {type}` satisfy type reasoning with zero penalty. Untyped, un-defaulted parameters in non-test functions incur **-2.0 pts** each (capped at -10.0 pts).

2. **TypeScript Type-Safety Escape Hatches:**
   - Explicit `any` type usage: Deduct **-5.0 pts** each (capped at -20.0 pts).
   - `@ts-ignore` / `@ts-nocheck` directive: Deduct **-10.0 pts** each (capped at -20.0 pts).
   - Non-null assertion (`!`): Deduct **-2.0 pts** each (capped at -10.0 pts).

3. **ECMAScript Clean Code Smells (JavaScript & TypeScript):**
   - Legacy `var` declarations: Deduct **-3.0 pts** each (capped at -15.0 pts). Prefer `const` or `let`.
   - Loose equality comparisons (`==` / `!=`): Deduct **-2.0 pts** each (capped at -10.0 pts). Prefer `===` / `!==`.
   - Empty `catch` blocks: Deduct **-10.0 pts** per occurrence.
   - `debugger;` statements: Deduct **-10.0 pts** per occurrence.

4. **Docstring, JSDoc & Javadoc Presence (Source Code):**
   - Missing docstring, JSDoc block, or Javadoc on public function/method:
     - Methods $\le 10$ LOC: **-5.0 pts**.
     - Methods $> 10$ LOC: **-10.0 pts**.
   - *(Angular DI constructors in `@Component`, `@Directive`, `@Injectable`, `@Pipe`, `@NgModule` classes are exempt).*

5. **Exception Handling Hygiene:**
   - Bare `except:` in Python: Deduct **-25.0 pts**.
   - Swallowed broad `except Exception:` / `catch (Exception e)` / empty JS/TS `catch`: Deduct **-10.0 pts** per occurrence.

6. **Dependency Injection & UI Framework Hygiene:**
   - **Spring Boot:** Field injection using `@Autowired` or `@Inject`: Deduct **-8.0 pts** per injected field.
   - **React / Next.js:** Rules of Hooks violation (calling `use*` hook inside branch or loop): Deduct **-25.0 pts** each (capped at -50.0 pts).
   - **React / Next.js:** Array index used as JSX `key`: Deduct **-8.0 pts** each (capped at -24.0 pts).
   - **Next.js:** App Router module under `app/` using client hooks (`useState`, `useEffect`, `useReducer`, `useRef`, `useContext`) without `'use client'` directive: Deduct **-15.0 pts** (module-level).
   - **Angular:** Unmanaged `.subscribe()` without `takeUntilDestroyed`, `takeUntil`, `DestroyRef`, or `ngOnDestroy` + `unsubscribe`: Deduct **-15.0 pts** (class-level).

7. **Test Quality Signals (Test Methods Only):**
   - Test method (`test_*`, `@Test`, `@ParameterizedTest`, BDD `it`/`test`) with `0` assertions: Deduct **-30.0 pts**.
   - Test method with $> 8$ assertions: Deduct **-3.0 pts** per assertion over 8 (capped at -30.0 pts).
   - *Recognized assertion idioms:*
     - Python: `assert`, `pytest.raises`, `pytest.warns`, `pytest.fail`, `self.assert*`.
     - Java / JUnit 5 / AssertJ / MockMvc / Mockito: `assertEquals`, `assertTrue`, `assertFalse`, `assertNotNull`, `assertThrows`, `assertAll`, `assertThat`, `assertThatThrownBy`, `.andExpect(...)`, `.andExpectAll(...)`, `verify(...)`.
     - JavaScript / TypeScript: `assert`, `assertEquals`, `strictEqual`, `deepStrictEqual`, `ok`, `expect`, `should`, `toBe`, `toEqual`, `toStrictEqual`, `toThrow`, `toBeTruthy`, `toBeFalsy`, `toHaveLength`, `equal`, `toBeDefined`, `toBeUndefined`, `toBeNull`, `toContain`, `toMatch`, `toMatchObject`, `toHaveBeenCalled`, `toHaveBeenCalledWith`, `toHaveBeenCalledTimes`, `toHaveProperty`, `toBeInstanceOf`, `toBeGreaterThan`, `toBeLessThan`, `toBeInTheDocument`.

---

### 3.5 Security & Boundary Hygiene ($S_{\text{Security}}$, 10%)
*(Tests score 100.0)*

1. **SQL / JPQL String Concatenation (Java, Python & TypeScript):**
   - Passing concatenated or interpolated strings into database query methods (`jdbcTemplate.query`, `entityManager.createQuery`, `createNativeQuery`, `query`, `execute`, `raw`, `$queryRawUnsafe`, `$executeRawUnsafe`): Deduct **-40.0 pts**. Use parameterized queries.

2. **Unsafe Execution & Deserialization (Python, JavaScript & TypeScript):**
   - Python: Calls to `eval()`, `exec()`, `pickle.loads()`, `pickle.load()`, unsafe `yaml.load()` without `SafeLoader`, `subprocess` with `shell=True`: Deduct **-40.0 pts**.
   - JavaScript / TypeScript: Calls to `eval()` or `new Function()`: Deduct **-40.0 pts**.
   - JavaScript / TypeScript: String argument to `setTimeout` or `setInterval`: Deduct **-20.0 pts**.

3. **Prototype Pollution & Scope Security (JavaScript & TypeScript):**
   - Direct prototype mutation via `__proto__`: Deduct **-25.0 pts**.
   - `with` statement obscuring lexical scope: Deduct **-30.0 pts**.

4. **UI XSS Sinks & Client-Server Boundaries (React, Next.js & Angular):**
   - Browser/framework DOM XSS sinks (`dangerouslySetInnerHTML`, `innerHTML`, `outerHTML`, `document.write`, `insertAdjacentHTML`, Angular `bypassSecurityTrust*`): Deduct **-35.0 pts** each (capped at -70.0 pts).
   - **Next.js:** Server-only imports (`fs`, `child_process`, `server-only`, `next/headers`, `node:*`) inside `'use client'` module: Deduct **-30.0 pts** (module-level).

5. **Subprocess Argument Safety, Path Confinement & Transactional Git Mutations (Python):**
   - Subprocess command passed as raw concatenated string instead of argument list: Deduct **-15.0 pts**.
   - Unconfined file writes or deletes without `.resolve()` / `.is_relative_to()`: Deduct **-15.0 pts**.
   - Mutating files (`write_text`, `unlink`, `rmtree`) before checking out a Git branch in the same function: Deduct **-25.0 pts**.

---

## 4. Class Rubric

A class score starts from the **arithmetic mean of its methods** and subtracts all **class-level structural and framework penalty deductions**:

$$\text{Class Dimension} = \overline{S}_{\text{methods}} - \text{Penalties}_{\text{class}}$$

*(If a class has no methods, it uses `100.0 - Penalties_class`. Security takes the minimum security score among its methods minus any class-level framework security penalties, or `100.0` when empty.)*

### Structural Penalties:
1. **Lack of Cohesion of Methods (LCOM4):**
   - Undirected graph where nodes are instance methods, and edges connect methods that access common fields (`self.attr` / `this.field` or implicit declared fields) or call each other.
   - Ideal: $\text{LCOM4} \le 1$.
   - **Penalty:** If class has $> 2$ methods and $\text{LCOM4} > 1$, deduct **-15.0 pts** per disconnected component over 1:
     $$\text{Penalty} = (\text{LCOM4} - 1) \cdot 15.0$$
2. **Method Count:** Ideal $\le 10$ methods. Deduct **-4.0 pts** per method over 10.
3. **Instance Attribute / Field Count:** Ideal $\le 7$ fields. Deduct **-4.0 pts** per field over 7.
4. **Class LOC:** Ideal $\le 200$ LOC. Deduct **-0.4 pts** per line over 200.
5. **Total Class Cyclomatic Complexity ($\sum \text{CC}$):** Ideal $\le 25$. Deduct **-1.5 pts** per point over 25.
6. **Class Documentation:** Missing docstring / JSDoc / Javadoc on public class deducts **-15.0 pts** from Clean Code.

### Class LCOM4 Exemptions:
The following patterns are exempt from LCOM4 cohesion penalties:
- Data models: Python `@dataclass`, `BaseModel`, `TypedDict`, `NamedTuple`; Java `record`, `@Entity`, `@Data`, `@Value`.
- Enums: Python `Enum`, `StrEnum`, `IntEnum`; Java/TS `enum`.
- Configuration & CLI groups: Spring `@Configuration`, `@ConfigurationProperties`, `@SpringBootApplication`; Python `TyperGroup`, `TyperCommand`, `Protocol`.
- Angular UI units: `@Component`, `@Directive`, `@Pipe`, `@NgModule`.
- Exception classes inheriting from `Exception` or ending in `Error` / `Exception`.
- Small utility classes with $\le 2$ methods.

---

## 5. File / Module Rubric

A file score starts from the **LOC-weighted mean of all top-level classes and functions in the file** and subtracts all **module-level architectural, clean-code, framework, and Git penalty deductions**:

$$\text{File Dimension} = \sum \left( \frac{\text{LOC}_u}{\text{LOC}_{\text{total}}} \cdot S_u \right) - \text{Penalties}_{\text{module}}$$

*(Complexity uses the LOC-weighted unit mean directly. Security takes the minimum security score across all top-level units minus module-level security penalties. Files with no classes or top-level functions fall back to `100.0 - Penalties_module`, with Complexity `100.0`.)*

### Module-Level Penalties:
1. **Multi-Class Bloat:** More than 4 non-exempt classes in a single file: **-3.0 pts** per extra class.
2. **Top-Level Function Sprawl:** More than 15 top-level functions: **-3.0 pts** per extra function.
3. **Internal Package Import Fan-Out:** More than 5 distinct internal package imports: **-5.0 pts** per dependency over 5.
4. **File LOC:**
   - Ideal: $\le 350$ LOC.
   - 351 to 600 LOC: **-0.15 pts / line**.
   - Above 600 LOC: **-0.25 pts / line**.
5. **Clean Code:**
   - Missing file/module docstring (Python source files): **-10.0 pts**.
   - Mid-file / late imports (imports after line 60 or inside functions, excluding `TYPE_CHECKING`): **-4.0 pts** each (capped at -20.0 pts).
   - Duplicate code blocks ($\ge 6$ identical AST statements repeated): **-5.0 pts** each (capped at -25.0 pts).
   - Unclaimed `@ts-ignore` / `@ts-nocheck` directives at module scope: **-10.0 pts** each (capped at -20.0 pts).
6. **Git History Signals (when Git is enabled):**
   - Commit Churn: $> 8$ commits touching the file deducts **-2.0 pts** per commit over 8 (capped at -25.0 pts).
   - Co-Change Coupling: Repeated co-changes with $\ge 3$ peer files deducts **-3.0 pts** per peer (capped at -15.0 pts).
   - Multi-Feature Churn: File touched across $\ge 4$ distinct `feat(...)` commits deducts **-10.0 pts**.
7. **Empty `__init__.py` Exemption:**
   - Python files named `__init__.py` with no executable statements and $\le 10$ lines automatically receive **100.0 (Grade A)** across all dimensions.
