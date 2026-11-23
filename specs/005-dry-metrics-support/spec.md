# Feature Specification: Multi-Language Duplicate Code & DRY Metrics Support

**Feature Branch**: `dry_metrics_support_plan`

**Created**: 2026-11-22

**Status**: Draft

**Input**: User description: "Multi-language (Python, Java, JavaScript/JSX, TypeScript/TSX) intra-file and cross-file Type-1, Type-2, and Type-3 duplicate code detection and DRY metrics support with memory- and compute-efficient execution."

---

## Background & Value Justification

Currently, the code health analyzer provides only minimal, Python-only duplicate detection that leaves major blind spots across real-world polyglot codebases:

- **No multi-language duplication coverage:** Java, JavaScript/JSX, TypeScript/TSX, and UI framework modules never check for duplicate code and always report zero duplicate blocks.
- **No cross-file clone detection:** Every file is scored in isolation, so copy-pasted functions, methods, components, or logic blocks across different files go completely undetected.
- **Exact-match blind spots and count inflation:** Only identical statement sequences inside a single file are detected; renaming a variable or changing a literal bypasses detection, near-duplicate edited clones are ignored, and overlapping sliding windows inflate counts on a single duplicated block.
- **Opaque findings and missing DRY metrics:** Findings report only a raw block count without line ranges, enclosing symbols, similarity scores, or peer locations, and reports lack per-file duplication density (`duplicated_loc`, `duplication_ratio`), a per-file or codebase `dry_score`, or a codebase-wide clone summary.

Adding unified, resource-efficient Type-1, Type-2, and Type-3 clone detection with actionable DRY metrics closes these gaps consistently across all supported languages and output formats.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Multi-Language Intra-File & Cross-File Exact and Parameterized Clone Detection (Priority: P1)

As an engineer or reviewer running the code health analyzer on a Python, Java, JavaScript/JSX, or TypeScript/TSX project, I want it to detect both exact clones (Type-1) and copy-pasted clones with renamed identifiers or altered literals (Type-2) within a single file and across files in the scan, so that duplicated logic is surfaced regardless of language, formatting, or variable renaming.

**Why this priority**: Catching exact and renamed copies within and across files across all supported languages delivers the core DRY capability and immediately resolves the single-language, single-file blind spots.

**Independent Test**: Can be tested independently by scanning single files and multi-file directories in Python, Java, JavaScript/JSX, and TypeScript/TSX containing Type-1 exact copies (differing only in comments, whitespace, or documentation comments) and Type-2 renamed copies (consistent variable/parameter renaming and literal changes), verifying accurate clone classification, non-overlapping spans, and exact line/symbol/peer coordinates.

**Acceptance Scenarios**:

1. **Given** a Python, Java, JavaScript/JSX, or TypeScript/TSX file containing two identical executable blocks that differ only in whitespace, comments, or docstrings/doc comments, **When** the analyzer runs on that file or its directory, **Then** a Type-1 clone group is reported with exact start/end line ranges, enclosing symbol names, and 100% similarity.
2. **Given** two files in the same language containing a duplicated function or logic block where identifiers have been consistently renamed and/or literal values changed, **When** a multi-file scan runs across those files, **Then** a cross-file Type-2 clone group is reported listing both file paths, line ranges, and enclosing symbols, and each participating file receives an actionable finding referencing its peer location.
3. **Given** the same logic block duplicated across three or more files, **When** evaluated in a multi-file scan, **Then** all occurrences are consolidated into a single multi-occurrence clone group rather than fragmented into redundant pairwise duplicates.
4. **Given** a long contiguous duplicated block (for example, 15 or more consecutive statements), **When** evaluated, **Then** it is reported as a single maximal non-overlapping clone span rather than multiple overlapping sliding-window hits.

---

### User Story 2 - Near-Miss Clone Detection (Type-3) & Cross-Cutting Boilerplate Detection (Priority: P2)

As a maintainer reviewing evolving codebases, I want the analyzer to detect near-miss clones (Type-3) where statements have been inserted, deleted, or modified—as well as repeated executable boilerplate and cross-cutting concerns across endpoints, components, handlers, or field mappings—while ignoring strictly non-executable declarations so that teams are nudged to decouple shared concerns from individual use cases.

**Why this priority**: Real-world duplication often manifests both as evolved copy-pasted logic with edits and as repeated cross-cutting boilerplate (validation, authorization, logging, hook wiring, field mapping) duplicated across parallel use cases; surfacing both drives architectural decoupling while excluding pure syntactic declarations prevents noise.

**Independent Test**: Can be tested independently by analyzing pairs of blocks/functions with small inserted/edited statement gaps or scattered edits (maintaining at least 70% similarity) and parallel cross-cutting boilerplate/mapping blocks alongside negative fixtures containing only non-executable declarations (imports, package declarations, comments, docstrings, TypeScript `interface`/`type`/ambient declarations) and tiny sub-threshold fragments, verifying Type-2/Type-3 detection and zero false positives on non-executable declarations.

**Acceptance Scenarios**:

1. **Given** two code blocks sharing matching sequences separated by a small gap of inserted, deleted, or modified statements (keeping overall similarity at or above the configured threshold, default 70%), **When** evaluated, **Then** they are reported as a Type-3 clone group with their exact combined line spans and calculated similarity percentage.
2. **Given** two functions or methods in the same language whose structure has diverged through scattered statement insertions, deletions, or modifications while preserving at least 70% ordered structural similarity, **When** evaluated, **Then** a function/method-level Type-3 clone group is reported with similarity percentage and symbol locations.
3. **Given** a clone pair already substantially covered by a stronger Type-1 or Type-2 match, **When** results are finalized, **Then** redundant overlapping Type-3 findings are suppressed so each duplicated region is counted once under its highest-fidelity clone type.
4. **Given** files containing repeated executable boilerplate or cross-cutting concerns (such as duplicated controller/endpoint scaffolding, validation/auth/logging wrappers, component hooks/handlers, or repeated field-mapping logic), **When** evaluated at or above the minimum size threshold, **Then** they are detected and surfaced as DRY clone groups; conversely, repeated non-executable declarations (imports, package declarations, comments, docstrings/doc comments, TypeScript `interface`/`type`/ambient declarations) and tiny fragments below minimum thresholds produce zero false-positive DRY clones.

---

### User Story 3 - Actionable DRY Metrics, Scoring Integration, Test Policies & Multi-Format Scorecards (Priority: P3)

As an engineering lead or CI pipeline maintainer, I want per-file and codebase-wide DRY metrics, severity-weighted Clean Code scoring integration, sensible test-file policies, configuration overrides, and structured Console, Markdown, and JSON reports, so that duplication density directly informs quality gates without cluttering clean scans.

**Why this priority**: Metrics and reporting turn raw clone matches into enforceable engineering standards, CI gates, and clear refactoring guidance.

**Independent Test**: Can be tested independently by running scans on clean files, moderately duplicated files, heavily duplicated files, mixed `src`/`tests` directories, custom configurations, and `--no-dry` invocations, inspecting JSON fields, Console tables, Markdown tables, exit codes, and Clean Code / composite grade caps.

**Acceptance Scenarios**:

1. **Given** a source file with detected clones, **When** scored, **Then** `Clean Code` deducts severity-weighted occurrence penalties (Type-1: `-5.0 pts`, Type-2: `-4.0 pts`, Type-3: `-3.0 pts`; penalizing redundant intra-file copies and cross-file participation) plus `-0.5 pts` per percentage point of `duplication_ratio` above `10.0%` (capped at `35.0 pts` for source), exposes `dry_score`, `duplicated_loc`, `duplication_ratio`, and `duplicate_blocks`, and enforces the worst-dimension ceiling (`Clean < 75.0` caps composite score at or below `79.5`, preventing Grade A/B).
2. **Given** test files in a codebase alongside production source files, **When** evaluated, **Then** test files use relaxed thresholds (`>= 55` executable tokens, `>= 8` lines, `15.0%` excess density threshold, `25.0 pts` penalty cap) and cross-file clone matching compares source files only against source files and test files only against test files.
3. **Given** a scan with zero detected clones, **When** rendered in console format, **Then** the console output remains clean and uncluttered without adding a duplicate-code summary section, whereas scans with one or more clone groups render a dedicated DRY summary and clone-group table in Console and Markdown alongside full structured data in JSON.
4. **Given** the `--no-dry` flag or custom DRY threshold overrides in project configuration, **When** the analyzer runs, **Then** `--no-dry` disables duplicate detection cleanly (`dry_score = 100.0`, zero DRY findings/groups) and custom configuration overrides adjust thresholds and caps deterministically.

---

### User Story 4 - Resource-Efficient, Deterministic Analysis & Baseline Integrity (Priority: P4)

As a user running the analyzer interactively in tight edit-check loops or across multi-thousand-line repositories, I want clone detection across all languages to be fast, bounded in memory, 100% deterministic, dependency-light, and free of regressions on healthy reference codebases.

**Why this priority**: Ensuring bounded memory, low latency, determinism, and zero regressions guarantees the feature scales cleanly to real repositories without slowing down developer or automated workflows.

**Independent Test**: Can be tested by benchmarking a 100-file (~15,000 LOC) multi-language corpus for runtime and peak memory, verifying byte-for-byte identical outputs across repeated runs, verifying zero new external dependencies are required, and running the full multi-language reference baseline suite.

**Acceptance Scenarios**:

1. **Given** identical source and test files scanned across repeated runs, **When** reports are generated, **Then** clone group IDs (`DRY-001`, `DRY-002`, ...), line spans, similarity scores, metrics, and grades are 100% deterministic and identically ordered.
2. **Given** a 100-file (~15,000 LOC) multi-file repository containing planted Type-1, Type-2, and Type-3 clones, **When** scanned end-to-end, **Then** all planted clones are detected accurately in under 2.5 seconds while keeping peak analysis memory bounded under 25 MB.
3. **Given** existing clean reference baseline samples across Python, Java, Spring Boot, JavaScript, TypeScript, React, Next.js, and Angular, **When** evaluated, **Then** all clean Grade A baselines retain Grade A with zero false-positive DRY penalties.

---

### Edge Cases

- **Empty files, empty `__init__.py`, and files with syntax errors**: Files that are empty, qualifying empty Python `__init__.py` files, or files containing parse/syntax errors are safely excluded from clone matching with zero DRY penalties (`duplicated_loc = 0`, `duplication_ratio = 0.0`, `dry_score = 100.0`).
- **Auto-generated source files**: Files marked by standard generated-code patterns—leading file header comments (e.g., `@generated`, `DO NOT EDIT`, `AUTO-GENERATED`, `Generated by`, `Code generated by`), Java `@Generated` annotations (`@Generated`, `javax.annotation.Generated`, `javax.annotation.processing.Generated`, `jakarta.annotation.Generated`), or standard generated filename patterns (`*_pb2.py`, `*_pb2_grpc.py`, `*.generated.*`, `*.gen.*`, `*_pb.*`, `*.pb.*`)—are automatically excluded from DRY clone detection (`duplicated_loc = 0`, `duplication_ratio = 0.0`, `dry_score = 100.0`).
- **Overlapping clone regions in a single file**: Multiple clone group occurrences within the same file must have their line intervals merged before counting `duplicated_loc`, ensuring `0 <= duplicated_loc <= loc` and `0.0% <= duplication_ratio <= 100.0%`.
- **Single-file vs. multi-file analysis**: Analyzing a single file evaluates intra-file Type-1, Type-2, and Type-3 duplication using the exact same rules and thresholds as a directory scan, without requiring a multi-file corpus; scanning directories additionally discovers cross-file clones.
- **Cross-language scans**: Files from different language families (for instance, Java and TypeScript in the same monorepo) are evaluated using their respective language rules and compared strictly within three comparison buckets: `python`, `java`, and a shared `ecmascript` bucket combining JavaScript/JSX (`.js`, `.jsx`, `.mjs`, `.cjs`) and TypeScript/TSX (`.ts`, `.tsx`, `.mts`, `.cts`) since TypeScript type annotations are stripped from executable tokens.
- **Highly repetitive code or large switch/lookup structures**: Pathologically repetitive executable blocks (such as long series of nearly identical case branches or repeated validation/mapping steps) are handled within bounded processing time and memory so analysis never degrades quadratically.
- **Existing baseline samples containing genuine clones**: Existing negative baseline files that already contain real intra-file clones (such as Python test suites or data structures with duplicated rotations/branches) surface the upgraded line-numbered DRY findings while preserving overall baseline scenario separation (`good` strictly outscores `bad`).

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST detect duplicate code across all supported languages: Python (`.py`), Java (`.java`), JavaScript/JSX (`.js`, `.jsx`, `.mjs`, `.cjs`), and TypeScript/TSX (`.ts`, `.tsx`, `.mts`, `.cts`), including UI framework codebases (React, Next.js, Angular) and Spring Boot.
- **FR-002**: System MUST support both **intra-file** clone detection (including single-file scans) and **cross-file** clone detection across all target files discovered within a scan, grouping comparisons into three language buckets: `python`, `java`, and a shared `ecmascript` bucket combining JavaScript/JSX and TypeScript/TSX (where type annotations are stripped from executable tokens to catch copy-paste across hybrid JS/TS codebases).
- **FR-003**: System MUST detect all three syntactic clone types:
  - **Type-1 (Exact):** Identical executable syntax ignoring whitespace, comments, docstrings/doc comments, and signature type annotations.
  - **Type-2 (Parameterized):** Structurally identical syntax with normalized literals and a verified consistent 1-to-1 identifier renaming correspondence.
  - **Type-3 (Near-Miss):** Edited clones containing inserted, deleted, or modified statements—covering both contiguous blocks bridged across small gaps (default up to `12` tokens) and function/method-level clones with scattered edits—meeting a configurable minimum similarity threshold (default `0.70`).
- **FR-004**: System MUST enforce configurable minimum size thresholds before reporting any clone—defaulting to aggressive source thresholds of `>= 35` executable tokens and `>= 5` effective lines for source files, and relaxed defaults of `>= 55` executable tokens and `>= 8` effective lines for test files.
- **FR-005**: System MUST exclude strictly non-executable declarations from clone matching (imports, package declarations, comments, docstrings/doc comments, and TypeScript `interface`/`type`/ambient declarations) while preserving detection of repeated executable boilerplate, cross-cutting concerns, and field-mapping logic at or above minimum size thresholds.
- **FR-006**: System MUST suppress redundant lower-fidelity matches already covered by higher-priority matches (Type-1 > Type-2 > Type-3, merging contiguous maximal spans rather than reporting overlapping sliding windows) and cluster multi-occurrence clones (`3+` identical or mutually linked occurrences) into unified clone groups with deterministic IDs (`DRY-001`, `DRY-002`, ...).
- **FR-007**: System MUST isolate cross-file comparisons by file role so production source files are compared only with production source files and test files are compared only with test files.
- **FR-008**: System MUST compute and expose per-file DRY metrics on every analyzed file report (`duplicate_blocks`, `duplicated_loc`, interval-merged `duplication_ratio` %, and `dry_score` on a `0.0–100.0` scale) and codebase-wide aggregates (`DrySummary` covering total LOC, total duplicated LOC, overall `duplication_ratio`, overall `dry_score`, and clone group counts broken down by Type-1/2/3 and intra-file/cross-file scope, plus the sorted `clone_groups` list).
- **FR-009**: System MUST integrate DRY penalties into each file's **Clean Code (`15%`)** dimension rather than altering the existing 5-dimension composite weighting (`SRP 30%`, `Size 25%`, `Complexity 20%`, `Clean 15%`, `Security 10%`):
  - Per-occurrence deductions: Type-1 `-5.0 pts`, Type-2 `-4.0 pts`, Type-3 `-3.0 pts` (charging `k - 1` redundant copies for an intra-file group of `k` occurrences, and `1` occurrence per participating file for cross-file groups).
  - Excess density deduction: `-0.5 pts` per percentage point of `duplication_ratio` above `10.0%` (source) or `15.0%` (test).
  - Total per-file DRY deduction capped at `35.0 pts` (source) and `25.0 pts` (test), with `dry_score = clamp(100.0 - dry_penalty)` and full enforcement of the worst-dimension ceiling when `Clean < 75.0`.
- **FR-010**: System MUST emit actionable per-file DRY findings specifying clone type, group ID, line range(s), enclosing symbol(s), similarity percentage (for Type-3), peer location(s), and exact point deduction.
- **FR-011**: System MUST surface DRY metrics across all output formats:
  - **JSON:** Always include per-file DRY fields and codebase `dry` summary.
  - **Console:** Preserve existing uncluttered console formatting when `clone_groups_count == 0`, and render a `[DUPLICATE CODE & DRY SUMMARY]` banner and clone-group table when clones are detected.
  - **Markdown:** Include a DRY summary bullet and a `Duplicate Code & DRY Findings` table when clones are detected.
- **FR-012**: System MUST provide a `--no-dry` CLI flag (and programmatic invocation option) to disable duplicate detection cleanly, and allow all DRY thresholds, similarity cutoffs, density tolerances, and penalty caps to be customized via project configuration files.
- **FR-013**: System MUST produce 100% deterministic outputs across repeated runs (identical group IDs, line spans, similarity scores, metrics, and grades) and process each file in a single pass with bounded memory without retaining full syntax trees across the codebase pass.
- **FR-014**: System MUST introduce **zero new external runtime dependencies** beyond the existing baseline runtime and native language parsers already supported by the analyzer.
- **FR-015**: System MUST keep the bundled agent skill scripts synchronized byte-for-byte with the standalone scripts, update scoring rubric and language refactoring playbook documentation to reflect multi-language DRY rules, and maintain Grade A (`>= 90.0`) self-health across all analyzer code.
- **FR-016**: System MUST automatically detect and exclude generated source files from DRY clone analysis using standard language conventions—generated file header markers (`@generated`, `DO NOT EDIT`, `AUTO-GENERATED`, `Generated by` in leading comments), Java `@Generated` / `javax.annotation.processing.Generated` / `jakarta.annotation.Generated` annotations, and standard generated filename suffixes (`*_pb2.py`, `*_pb2_grpc.py`, `*.generated.*`, `*.gen.*`, `*_pb.*`, `*.pb.*`)—with optional custom exclusion patterns supported via project configuration.

### Key Entities

- **Clone Location**: A single occurrence of duplicated code within a file, capturing `file_path`, `start_line`, `end_line`, enclosing `symbol`, effective `loc`, and `token_count`.
- **Clone Group**: A deterministic cluster (`group_id` such as `DRY-001`) of two or more matching `Clone Location` occurrences sharing a `clone_type` (`type1`, `type2`, or `type3`), `scope` (`intra_file` or `cross_file`), `similarity` ratio (`0.0–1.0`), representative `tokens` and `loc`, and ordered `occurrences`.
- **File DRY Metrics**: Per-file duplication measurements comprising `duplicate_blocks`, merged `duplicated_loc`, `duplication_ratio` (percentage of file LOC), `dry_score` (`0.0–100.0`), `dry_penalty`, and actionable `findings`.
- **Codebase DRY Summary (`DrySummary`)**: Aggregated corpus-wide DRY state capturing `total_loc`, `duplicated_loc`, `duplication_ratio`, `dry_score`, `clone_groups_count`, per-type counts (`type1_groups`, `type2_groups`, `type3_groups`), per-scope counts (`intra_file_groups`, `cross_file_groups`), and `clone_groups`.
- **DRY Configuration Thresholds**: Configurable parameters controlling minimum token and line spans (source and test), Type-3 minimum similarity, maximum contiguous gap tokens, excess density thresholds (source and test), and maximum Clean Code DRY penalty caps (source and test).

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Type-1, Type-2, and Type-3 clones are accurately detected both within a single file and across multiple files in all four supported language families (Python, Java, JavaScript/JSX, TypeScript/TSX), with exact line ranges and enclosing symbols reported for 100% of verified clones.
- **SC-002**: Strictly non-executable declarations (imports, package declarations, comments, docstrings/doc comments, and pure TypeScript `interface`/`type`/ambient declarations) and short fragments below minimum size thresholds produce zero false-positive DRY penalties, while repeated executable boilerplate and cross-cutting concerns are detected; any clean reference baseline sample flagged during calibration is inspected empirically.
- **SC-003**: Source files exhibiting heavy duplication (`>= 30%` duplication ratio or `>= 5` distinct clone occurrences) have their Clean Code score reduced sufficiently to prevent Grade A/B via the worst-dimension ceiling (`composite <= 79.5`), while duplicate-free files score `100.0` on `dry_score`.
- **SC-004**: End-to-end analysis of a 100-file (~15,000 LOC) multi-file corpus containing planted Type-1, Type-2, and Type-3 clones completes in under 2.5 seconds wall-clock time while keeping peak analysis memory allocation under 25 MB.
- **SC-005**: Repeated executions on identical inputs produce 100% deterministic, byte-for-byte identical clone group IDs, spans, similarity scores, metrics, and scorecards.
- **SC-006**: Zero additional third-party runtime dependencies are required for Python, Java, JavaScript, or TypeScript analysis beyond the analyzer's existing baseline prerequisites.
- **SC-007**: All existing and new automated unit tests, baseline scenario tests, documentation link checks, and skill mirror parity checks pass with zero skipped or failing tests, and the analyzer achieves Grade A (`>= 90.0`) on its own codebase.

---

## Assumptions

- **Rubric integration choice**: Initial DRY penalties are integrated into the existing **Clean Code (`15%`)** dimension while exposing `dry_score`, `duplication_ratio`, `duplicated_loc`, and `DrySummary` as first-class metrics; this preserves the established 5-dimension composite contract (`30/25/20/15/10`) and avoids invalidating unaffected baseline scorecards, with initial penalty weights inside `Clean Code (15%)` to be fine-tuned empirically against real-world code samples.
- **Test-file policy choice**: Test files intentionally use relaxed DRY thresholds (`>= 55` tokens, `>= 8` lines, `15.0%` excess density threshold, `25.0 pts` cap) and are isolated in a dedicated `test` partition so individual test cases remain self-contained and readable (DAMP) while still flagging severely copy-pasted test suites and preventing cross-matching with production source code.
- **Language-boundary isolation**: Duplicate detection compares files strictly within three comparison buckets (`python`, `java`, and a shared `ecmascript` bucket combining JavaScript/JSX and TypeScript/TSX); cross-family comparisons (e.g., matching Python against Java or ECMAScript) are out of scope.
- **Static single-pass analysis**: Detection operates strictly via deterministic static lexical/syntax inspection of the files in target paths without spawning external compilers, linters, language servers, or runtime tools.
- **Baseline sample updates**: Only existing negative baseline samples that genuinely contain intra-file duplication (such as duplicated test routines or duplicated tree rotations) will have their expected scorecard snapshots updated; all unaffected baselines remain unchanged.

---

## Open Questions

| ID | Question | Status | Resolution |
|----|----------|--------|------------|
| Q1 | Should DRY penalties live inside `Clean Code (15%)` alongside standalone DRY metrics, or become a 6th weighted dimension? | Resolved | Start inside `Clean Code (15%)` with standalone `dry_score` / `duplication_ratio` / `DrySummary` metrics, then fine-tune penalty weights empirically against real-world code samples. |
| Q2 | Should Type-2/Type-3 err conservative on parallel scaffolding/boilerplate or lean aggressive to flag repeated boilerplate and cross-cutting concerns? | Resolved | Lean aggressive: detect repeated executable boilerplate and cross-cutting concerns so they are refactored into shared decoupled concerns; exclude only non-executable declarations (imports, package declarations, comments, docstrings, pure type/interface declarations) and sub-threshold fragments. |
| Q3 | Should test files follow the same aggressive DRY bar as production code, or keep looser thresholds so test cases can stay self-contained? | Resolved | Keep relaxed test thresholds (`>= 55` tokens, `>= 8` lines, `15.0%` excess density tolerance, `25.0 pts` cap) and isolate `test` from `src` cross-file matching so individual test cases remain self-contained and readable. |
| Q4 | Should v1 exclude generated or intentional files from DRY checks via config/inline markers or standard generated-code detection? | Resolved | Automatically skip generated code using standard per-language conventions (generated header comments like `@generated` / `DO NOT EDIT` / `Generated by`, Java `@Generated` annotations, and standard generated filename suffixes), plus optional config path patterns. |
| Q5 | Which detection approach should guide planning, and should JS/TS share an ECMAScript comparison bucket? | Resolved | Approach A selected (deterministic single-pass compact token-stream indexing with contiguous exact/parameterized matching, gap bridging, and function-level near-miss matching — chosen over probabilistic LSH and syntax-subtree edit distance for 100% determinism, zero new dependencies, and bounded memory); JS and TS share an ECMAScript comparison bucket (explicitly noted as a sensible default). |

---

## Brainstorm Log

### 2026-11-22 — `/speckit-superspec-brainstorm` Session Summary
- **Rubric Integration & Empirical Calibration (Q1)**: Keep initial DRY penalties inside `Clean Code (15%)` alongside standalone `dry_score`, `duplication_ratio`, `duplicated_loc`, and `DrySummary` metrics, preserving the 5-dimension composite contract while fine-tuning penalty weights empirically against real-world code samples.
- **Aggressive Boilerplate & Cross-Cutting Concern Detection (Q2)**: Lean aggressive on Type-2 and Type-3 detection (source defaults `>= 35` tokens, `>= 5` lines, `>= 0.70` similarity) so repeated executable boilerplate, controller/endpoint scaffolding, UI component wiring, field-mapping logic, and cross-cutting concerns are surfaced and refactored into decoupled shared concerns. Exclude only strictly non-executable declarations (imports, package declarations, comments, docstrings/doc comments, and pure TypeScript `interface`/`type`/ambient declarations) and sub-threshold fragments.
- **Self-Contained Test Policy (Q3)**: Keep relaxed DRY thresholds for test files (`>= 55` tokens, `>= 8` lines, `15.0%` excess density tolerance, `25.0 pts` penalty cap) and isolate `test` from `src` cross-file matching so individual test cases remain self-contained and readable (DAMP).
- **Standard Generated-Code Exclusion (Q4)**: Automatically exclude auto-generated source files from DRY analysis via standard per-language conventions (leading header comments such as `@generated`, `DO NOT EDIT`, `AUTO-GENERATED`, `Generated by`; Java `@Generated` / `javax.annotation.processing.Generated` / `jakarta.annotation.Generated` annotations; standard generated filename suffixes like `*_pb2.py`, `*.generated.*`, `*.gen.*`, `*.pb.*`), plus optional custom path patterns in project config.
- **Architecture Direction & ECMAScript Bucket (Q5)**: Locked Approach A for technical planning (deterministic single-pass compact token-stream indexing supporting intra- and cross-file Type-1, Type-2, and Type-3 detection with bounded memory and zero new dependencies); JS/JSX and TS/TSX share an `ecmascript` comparison bucket while `python` and `java` remain separate buckets.
