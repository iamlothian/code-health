# Feature Specification: Web UI Framework Code Health Profiles

**Feature Branch**: `evaluate_ui_frameworks`

**Created**: 2026-11-12

**Status**: Draft

**Input**: User description: "Now that we have typescript let's add some common web UI frameworks support, explore whether this adds value or if typescript alone covers UI framework specific code health issues."

---

## Background & Value Justification

Empirical evaluation of the existing TypeScript analyzer against realistic React and Angular components demonstrates that TypeScript language rules alone cover component size, cyclomatic/cognitive complexity, type escape hatches (`any`, `@ts-ignore`, `!`), and generic dynamic execution (`eval`, `new Function`), **but miss critical UI-specific security, architectural, and lifecycle defects**:

- **Zero UI concern mapping**: TypeScript files currently detect zero operational concerns, so components mixing network fetching, browser storage, logging, and UI rendering never trigger Single Responsibility concern-mixing warnings.
- **Invisible browser and framework XSS sinks**: JSX/DOM injection patterns (`dangerouslySetInnerHTML`, `innerHTML`, `document.write`, Angular `bypassSecurityTrust*`) score 100.0 in Security.
- **Undetected framework architectural defects**: Conditional React hooks (runtime crashes), hook/effect sprawl, Angular components directly injecting `HttpClient`, and unmanaged RxJS `.subscribe()` memory leaks currently score Grade A (`96.4–99.7 / 100`).
- **Component wrapper and decorator blind spots**: Components wrapped in higher-order helpers (`React.memo`, `React.forwardRef`) are skipped, and class/field decorators (`@Component`, `@Input`) are ignored.
- **Idiomatic UI false positives**: Angular DI constructors and React components relying on TypeScript's inferred JSX return types incur spurious Clean Code or cohesion penalties.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Automatic UI Framework Detection & Browser XSS Protection (Priority: P1)

As a frontend or full-stack developer running the code health analyzer on a web project, I want the tool to automatically recognize common TypeScript web UI frameworks from project manifests and file imports (or accept an explicit framework flag) and detect browser/UI XSS sinks and mixed operational concerns, so that security vulnerabilities and bloated multi-concern components are caught immediately.

**Why this priority**: Security blind spots (XSS sinks scoring 100.0) and missing UI concern classification are the highest-impact gaps that TypeScript-only analysis cannot cover.

**Independent Test**: Can be tested independently by analyzing UI component files containing `dangerouslySetInnerHTML`, `innerHTML` assignments, `document.write`, or mixed `fetch` + `localStorage` + UI rendering calls, verifying Security and SRP deductions with exact line numbers, and verifying `--framework none` disables framework rules.

**Acceptance Scenarios**:

1. **Given** a workspace or source file referencing React, Next.js, or Angular (via `package.json` dependencies or module imports), **When** the analyzer runs with default auto-detection, **Then** the corresponding UI framework profile is activated for those UI source files.
2. **Given** a component containing `dangerouslySetInnerHTML`, direct `innerHTML`/`outerHTML` assignment, `insertAdjacentHTML`, `document.write`, or Angular `bypassSecurityTrust*` calls, **When** evaluated under the active UI framework profile, **Then** the Security dimension deducts points and reports the exact line-numbered XSS sink.
3. **Given** a UI component that mixes three or more distinct operational concerns (such as UI rendering, network I/O, browser storage, and console/logging), **When** evaluated, **Then** SRP flags the mixed concerns with their category names.
4. **Given** an explicit `--framework none` flag, **When** the analyzer scans UI files, **Then** only base TypeScript/JavaScript language rules apply without framework penalties.

---

### User Story 2 - React & Next.js Component, Hook, and Boundary Hygiene (Priority: P2)

As a React or Next.js engineer, I want the analyzer to inspect wrapped components (`React.memo`, `React.forwardRef`), flag Rules of Hooks violations, flag excessive effect/state hook sprawl, catch unstable array-index keys, and enforce Next.js server/client module boundaries, so that subtle runtime bugs and architectural coupling are surfaced before code review.

**Why this priority**: React and Next.js represent the dominant TypeScript UI ecosystem, and hook ordering bugs, effect soup, and server/client boundary leaks are invisible to TypeScript's compiler and generic complexity metrics.

**Independent Test**: Can be tested independently by analyzing React/Next.js components containing conditional `useEffect` calls, 3+ effects, 6+ state hooks, `key={index}`, `React.memo`-wrapped components, and `"use client"` modules importing server-only APIs, verifying each triggers an accurate finding while clean modular components score Grade A.

**Acceptance Scenarios**:

1. **Given** a React component calling a hook (`use*`) inside a conditional branch, loop, or ternary expression, **When** evaluated, **Then** Clean Code penalizes the Rules of Hooks violation with the hook name and line number.
2. **Given** a React component containing more than 2 effect hooks (`useEffect`/`useLayoutEffect`) or more than 5 `useState` hooks, **When** evaluated, **Then** SRP penalizes the effect or state sprawl and suggests extracting a custom hook or reducer.
3. **Given** a list rendering `.map(...)` callback using the iteration index as the JSX `key` prop, **When** evaluated, **Then** Clean Code flags the reconciliation anti-pattern.
4. **Given** a component defined via `React.memo(...)` or `React.forwardRef(...)`, **When** evaluated, **Then** the inner component function is extracted, scored, and surfaced in the scorecard rather than skipped.
5. **Given** a Next.js module marked with `"use client"` that imports server-only modules (`fs`, `node:*`, `next/headers`, `server-only`), **When** evaluated under the `nextjs` profile, **Then** Security/Boundary Hygiene flags the server-to-client boundary violation.
6. **Given** a Next.js App Router file under `app/` lacking `"use client"` that invokes client-only hooks (`useState`, `useEffect`, `useReducer`, `useRef`, `useContext`), **When** evaluated under the `nextjs` profile (and not a `use*` hook module or `pages/` route), **Then** Clean/Boundary Hygiene flags the missing `"use client"` directive.

---

### User Story 3 - Angular Component Layering, Lifecycle, and Subscription Hygiene (Priority: P3)

As an Angular engineer, I want the analyzer to recognize Angular decorators (`@Component`, `@Directive`, `@Injectable`, `@Input`, `@Output`), flag components directly injecting `HttpClient`, flag unmanaged RxJS `.subscribe()` calls, and avoid penalizing idiomatic DI constructors or template-bound lifecycle classes, so that Angular scorecards reflect real architectural health.

**Why this priority**: Angular applications rely heavily on decorators, dependency injection layering, and reactive subscriptions; without framework awareness, real architectural leaks pass with Grade A while idiomatic DI constructors incur noise.

**Independent Test**: Can be tested independently by analyzing an Angular `@Component` injecting `HttpClient` and calling `.subscribe()` without teardown vs. a clean `@Component` delegating HTTP calls to an `@Injectable` service using `takeUntilDestroyed` / `async` pipe, verifying strict score separation.

**Acceptance Scenarios**:

1. **Given** a class decorated with `@Component` or `@Directive` that injects `HttpClient` directly, **When** evaluated under the `angular` profile, **Then** SRP flags a layering violation recommending delegating HTTP access to an `@Injectable` service.
2. **Given** an Angular `@Component` or `@Directive` invoking `.subscribe(...)` without `takeUntilDestroyed`, `takeUntil`, `DestroyRef`, or `.unsubscribe()` teardown, **When** evaluated, **Then** Clean Code flags an unmanaged subscription memory-leak risk.
3. **Given** an Angular `@Component`, `@Directive`, `@Pipe`, or `@Injectable` class with a dependency-injection constructor and lifecycle hooks (`ngOnInit`, `ngOnDestroy`), **When** evaluated, **Then** the DI constructor is not penalized for missing a docstring and template-bound classes are not falsely penalized for LCOM4 cohesion splits.

---

### User Story 4 - Polyglot Isolation & Baseline Integrity (Priority: P4)

As a maintainer of a polyglot or monorepo codebase, I want UI framework profiles to activate strictly on relevant UI files and preserve all existing Python, Java, Spring Boot, JavaScript, and pure TypeScript scorecard behaviors, so that backend or utility modules are never subjected to UI-specific rules.

**Why this priority**: Prevents regressions and false positives in non-UI TypeScript files (such as backend APIs, algorithms, and test suites) within the same repository.

**Independent Test**: Can be tested by running the full existing multi-language baseline suite and verifying zero regressions across non-UI samples and pure TypeScript utility files inside a React/Angular workspace.

**Acceptance Scenarios**:

1. **Given** a monorepo containing both a React frontend directory and a backend Node/TypeScript service file that does not import UI libraries, **When** evaluated, **Then** UI-specific rules do not produce false-positive findings on backend service files.
2. **Given** existing non-UI Python, Java, Spring Boot, JavaScript, and TypeScript baseline files, **When** evaluated, **Then** all existing scores and findings remain deterministic and unchanged.

---

### Edge Cases

- **No or Malformed `package.json`**: Framework detection must fall back cleanly to per-file imports (e.g., `import ... from "react"`, `"@angular/core"`, `"next/..."`) when `package.json` is absent or invalid JSON, without failing the scan.
- **Destructured Props & Wrapper Components**: Components using destructured parameter objects (`function Card({ title }: CardProps)`) or higher-order wrappers (`memo`, `forwardRef`) must still report accurate parameter counts, LOC, and complexity.
- **Custom Hooks (`useSomething`) vs. Components**: A custom hook (`useAuthData`) legitimately calls `useState`/`useEffect` at top level and may return data rather than JSX; rules targeting JSX return types, component hook-sprawl, or Next.js `app/` `"use client"` checks must distinguish custom hooks cleanly.
- **Next.js Server Components vs. Pages Router / Utility Modules**: Client-hook checks for missing `"use client"` must apply strictly under `app/` routes/components and exempt `pages/` router files and standalone `use*` hook modules.
- **Existing TSX Baselines (`task_board_legacy.tsx`, `task_filter_bar.tsx`)**: Both files import `"react"` and will be routed to the `react` framework profile under `auto`; move them into dedicated React framework samples and replace the pure TypeScript scenario with a framework-free TypeScript sample pair.
- **Single-File Components (`.vue`, `.svelte`)**: Deferred to Phase 2; Phase 1 scopes strictly to React, Next.js, and Angular.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support explicit UI framework selection via `--framework` for `react`, `nextjs`, and `angular` (in addition to `auto`, `spring-boot`, and `none`) across TypeScript (`.ts`, `.tsx`, `.mts`, `.cts`) and JavaScript (`.js`, `.jsx`, `.mjs`, `.cjs`) source files.
- **FR-002**: System MUST automatically detect active UI frameworks per file using project dependency manifests (`package.json`) combined with file-level imports, applying UI framework rules only when relevant to the file/workspace context.
- **FR-003**: System MUST map common web UI and browser operational concerns (`network_io`, `storage_io`, `presentation`, `dom_mutation`, `render_ui`) so SRP detects mixed-concern UI components.
- **FR-004**: System MUST detect and penalize browser and framework XSS sinks (`dangerouslySetInnerHTML`, `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, and Angular `bypassSecurityTrust*` methods) under the Security dimension.
- **FR-005**: System MUST extract functions wrapped in common UI higher-order wrappers (`React.memo`, `memo`, `React.forwardRef`, `forwardRef`) as scored function units.
- **FR-006**: System MUST extract class, method, and field decorators (`@Component`, `@Directive`, `@Injectable`, `@Pipe`, `@Input`, `@Output`) on TypeScript classes for framework rule evaluation.
- **FR-007**: Under `react` and `nextjs` profiles, system MUST detect conditional/looped React hook calls, excessive `useEffect`/`useState` counts per component, and array-index JSX `key` usage in `.map(...)`, while exempting JSX-returning UI components from missing return-type annotation penalties (preserving typed parameter requirements).
- **FR-008**: Under the `nextjs` profile, system MUST detect both (a) server-only imports (`fs`, `node:*`, `next/headers`, `server-only`) inside `"use client"` modules and (b) client-only React hooks (`useState`, `useEffect`, `useReducer`, `useRef`, `useContext`) inside `app/` files missing `"use client"` (exempting `pages/` router files and standalone `use*` custom hook modules).
- **FR-009**: Under the `angular` profile, system MUST flag `@Component`/`@Directive` classes directly injecting `HttpClient`, flag unmanaged `.subscribe()` calls lacking teardown guards, and exempt Angular DI constructors and template-bound component classes from false-positive docstring and LCOM4 penalties.
- **FR-010**: System MUST keep framework rules, concern mappings, and framework-specific thresholds strictly isolated inside pluggable framework profiles rather than inside raw language profiles, parsers, or the core scorer, so disabling frameworks (`--framework none`) or analyzing non-UI files executes pure language rules only.
- **FR-011**: System MUST preserve 100% deterministic reproducibility and ensure all new or modified analyzer modules achieve Grade A (`>= 90.0`) self-health.

### Key Entities

- **UI Framework Profile**: A framework-specific rule and concern-mapping layer (`react`, `nextjs`, `angular`) attached to TypeScript (and optionally JavaScript) language profiles.
- **UI Concern Category**: An operational domain label (`network_io`, `storage_io`, `dom_mutation`, `render_ui`, `presentation`) assigned to component calls and JSX rendering.
- **UI Security Sink**: A dangerous DOM, JSX, or sanitizer-bypass pattern recorded with its line number during syntax-tree traversal.
- **Boundary Directive**: A module-level directive string (`"use client"`, `"use server"`) used to validate server/client import and hook boundaries.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Realistic flawed React and Angular components containing XSS sinks, conditional hooks, DI layering violations, or unmanaged subscriptions drop from Grade A (`>90.0`) to Grade D/F (`<70.0`) with exact line-numbered findings.
- **SC-002**: Clean, idiomatic React, Next.js, and Angular reference components achieve Grade A (`>= 90.0`) without false-positive penalties.
- **SC-003**: Existing Python, Java, Spring Boot, JavaScript, and non-UI TypeScript unit tests and baseline scorecards pass with zero unintended regressions.
- **SC-004**: Single-file analysis with UI framework rules enabled completes in under 2 seconds with zero additional required PyPI packages beyond existing `tree-sitter-typescript` / `tree-sitter-javascript`.

---

## Assumptions

- Target UI codebases use TypeScript/TSX (`.ts`, `.tsx`, `.mts`, `.cts`) and JavaScript/JSX (`.js`, `.jsx`, `.mjs`, `.cjs`), with Angular scoped to TypeScript and React/Next.js covering both JavaScript and TypeScript.
- Analysis remains strictly per-file syntax-tree + repository manifest/Git inspection without spawning `tsc`, ESLint, or a Node.js runtime.

---

## Open Questions

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| Q1 | Should Phase 1 scope target **React, Next.js, and Angular** (using existing `tree-sitter-typescript`), deferring **Vue (`.vue`) and Svelte (`.svelte`)** Single-File Components to Phase 2? | Resolved | Phase 1 targets **React, Next.js, and Angular**; Vue and Svelte deferred to Phase 2. |
| Q2 | How should existing React TSX sample baselines (`task_board_legacy.tsx`, `task_filter_bar.tsx`) be handled—pin to `framework: "none"` as pure TS baselines or update their `.expected.json` sidecars for React-aware scoring? | Resolved | Move React TSX samples (`task_board_legacy.tsx`, `task_filter_bar.tsx`) to dedicated React framework samples and replace the pure TypeScript sample slot with framework-free TypeScript samples. |
| Q3 | Should the `react` profile exempt PascalCase JSX-returning components from the `-10.0 pts` missing return-type annotation penalty (matching React 18+ inferred return types)? | Resolved | Yes — `react` and `nextjs` profiles exempt JSX-returning UI components from missing return-type annotation penalties while preserving typed prop parameter enforcement. |
| Q4 | Should React/Next.js profiles also attach to `JavaScriptLanguageProfile` and add `.jsx` file discovery? | Resolved | Yes — include both JavaScript (`.js`, `.jsx`, `.mjs`, `.cjs`) and TypeScript (`.ts`, `.tsx`, `.mts`, `.cts`), keeping framework concepts strictly modular and isolated from raw language profiles. |
| Q5 | Should `NextJsFrameworkProfile` flag client hooks (`useState`, `useEffect`) in files lacking `"use client"`, or restrict Phase 1 boundary checks to `"use client"` importing server-only APIs to avoid false positives in Pages Router / custom hooks? | Resolved | Flag both — enforce server-only imports in `"use client"` files and flag client hooks in `app/` files missing `"use client"` (exempting `pages/` and `use*` custom hook modules). |

---

## Brainstorm Log

### 2026-11-12 — `/speckit-superspec-brainstorm` Session Summary
- **Scope Locked (Q1, Q4)**: Phase 1 targets **React, Next.js, and Angular** across both **TypeScript** (`.ts`, `.tsx`, `.mts`, `.cts`) and **JavaScript** (`.js`, `.jsx`, `.mjs`, `.cjs`), with Angular scoped to TypeScript and React/Next.js covering both JS and TS. Vue (`.vue`) and Svelte (`.svelte`) Single-File Components are deferred to Phase 2.
- **Architectural Isolation**: Parsers emit only generic syntax primitives (decorators, directives, imports, JSX presence, call branch/loop context, DOM/JSX attribute sinks); raw language profiles remain framework-free; all framework concern maps, entrypoints, exemptions, and rules live solely in pluggable `FrameworkProfile` classes composed per file.
- **React Return-Type Calibration (Q3)**: Exempt JSX-returning UI components from the `-10.0 pts` missing return-type annotation penalty under `react` and `nextjs` while preserving typed prop parameter enforcement.
- **Next.js App Router Boundaries (Q5)**: Flag both server-only imports inside `"use client"` modules and client hooks (`useState`, `useEffect`, etc.) in `app/` files missing `"use client"`, exempting `pages/` router files and `use*` custom hook modules.
- **Baseline Integrity (Q2)**: Move `task_board_legacy.tsx` and `task_filter_bar.tsx` into dedicated React framework samples (since they import `"react"` and will be scanned by the React profile under `auto`) and replace them in `samples/typescript/` with pure, framework-free TypeScript samples.
- **Edge Cases Added**: Graceful fallback on malformed/missing `package.json`; custom hook (`use*`) exemptions from component-only heuristics.
