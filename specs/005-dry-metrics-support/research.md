# Phase 0 Research: Multi-Language Duplicate Code & DRY Metrics Support

**Date**: 2026-11-22  
**Feature**: `005-dry-metrics-support`  
**Spec**: [spec.md](./spec.md)

---

## 1. Compact Single-Pass Token Stream Representation

- **Decision:** Extract a flat, immutable `FileTokenStream` per parsed source file using `array('I')` for 32-bit `exact_ids`, `norm_ids`, `lines`, and `stmt_starts` and `array('B')` for `tok_kinds` (~13 bytes per token), paired with a single scan-wide `TokenInterner` and lightweight `slots=True` `BlockSpan` metadata. Discard every Python `ast.Module` and Tree-Sitter CST immediately after extracting the file's `FileReport` and `FileTokenStream`.
- **Rationale:** Serializing `ast.dump()` strings or keeping full syntax trees across a codebase scan causes hundreds of megabytes of object retention on medium/large repositories and cannot unify Python `ast` with Java/JS/TS Tree-Sitter grammars. Flat `array('I')`/`array('B')` buffers require ~6.5 MB for a 100k-LOC (~500k-token) corpus, support slice-free indexing, preserve exact line attribution, and require zero third-party packages.
- **Alternatives considered:**
  1. *Retain normalized AST/CST subtrees in memory across all files:* Rejected due to high per-node Python object memory overhead (>10× budget) and cross-parser structural divergence between stdlib `ast` and Tree-Sitter CSTs.
  2. *Store `list[tuple[int, int, int, int]]` per token:* Rejected because Python 4-tuples + `int` objects add ~72–104 bytes per token and slow down cache locality compared to contiguous `array('I')` typed arrays.

---

## 2. Type-1 & Type-2 Clone Detection (Winnowing + Diagonal-Deduplicated Extension)

- **Decision:** Index each `(language, is_test)` partition with a 64-bit Mersenne polynomial rolling hash ($\bmod (2^{61}-1)$, base $B = 1{,}000{,}003$, $k = 16$ tokens) and deterministic rightmost-minimum Winnowing (`w = 10` hashes per window via monotonic `deque`, guaranteeing detection of any contiguous match $\ge k + w - 1 = 25$ tokens while shrinking the inverted index by ~5×). Pack locations into single 64-bit ints `(file_idx << 28) | pos`, cap each hash bucket at `MAX_BUCKET = 64`, deduplicate diagonals via `seen_diags[(file_a, file_b, pos_b - pos_a)] = end_a`, prevent intra-file self-overlap (`end_a <= start_b`), extend matches bidirectionally, and verify Type-2 clones via a strict 1-to-1 `KIND_IDENT` alpha-renaming bijection.
- **Rationale:** Winnowing provides exact, 100% deterministic substring-anchor guarantees with far lower memory than indexing every $k$-gram. Diagonal deduplication eliminates quadratic $O(L^2)$ re-extension on long duplicated functions, while strict identifier bijection prevents structural collisions where one block reuses the same variable across distinct roles (`x = a + a` vs `p = q + r`).
- **Alternatives considered:**
  1. *MinHash LSH over sliding windows:* Rejected because random/seed-sensitive signatures introduce false-negative variance (conflicting with `FR-013` / `SC-005` 100% determinism) and yield imprecise line boundaries.
  2. *Unfiltered overlapping statement windows (current Python implementation):* Rejected because overlapping windows inflate block counts (e.g., 10 repeated statements create 5 hits) and cannot detect Type-2 renamed identifiers or cross-file clones.

---

## 3. Type-3 Near-Miss Clone Detection (Gap-Stitching + SourcererCC Prefix Filtering)

- **Decision:** Combine two complementary deterministic Type-3 passes:
  - **Stage 3A (Contiguous Gap-Stitching):** Chain consecutive Type-1/2 seed matches (`>= 16` tokens) on the same `(file_a, file_b)` pair separated by $0 \le \text{gap} \le 12$ tokens (`dry_max_gap_tokens`) whenever `matched_tokens / max_span >= dry_type3_similarity` (`0.70`) and the combined span clears minimum token/line thresholds.
  - **Stage 3B (Function/Method Scattered Edits via SourcererCC Prefix Filtering):** Partition eligible `BlockSpan` units by `(language, is_test)`, build sorted unique 3-gram normalized shingle sets, collapse identical shingle sets to one representative prior to indexing, sort globally by ascending document frequency `df`, index only the rarest prefix of length $|S| - \lceil \theta |S| \rceil + 1$ (capped at `MAX_POSTING = 64`), apply exact length filtering $\min(|A|, |B|) \ge \theta \max(|A|, |B|)$, check multiset token overlap, and finalize exact ordered similarity via `difflib.SequenceMatcher(None, stmts_a, stmts_b, autojunk=False).ratio() >= 0.70`.
- **Rationale:** Gap-stitching catches module-level and sub-function near-miss clones with localized insertions/modifications, while SourcererCC prefix filtering indexes only ~30% of shingles (`\theta = 0.70`), skips frequent boilerplate tokens, collapses exact copies before pairing, and sets `autojunk=False` so Python's `SequenceMatcher` heuristic never silently drops repeated statements in large functions.
- **Alternatives considered:**
  1. *Tree Edit Distance on AST/CST subtrees:* Rejected due to $O(N^2 \cdot d^2)$ worst-case complexity on large methods and memory pressure retaining trees.
  2. *All-pairs token Jaccard without prefix filtering:* Rejected due to quadratic $O(N^2)$ scaling on 100+ file repositories.

---

## 4. Multi-Language Token Extraction & Shared `ecmascript` Bucket

- **Decision:** Extract Python tokens via stdlib `tokenize.generate_tokens` guided by `ast.Module` line/column exclusions (imports, docstrings, signature and `AnnAssign` type annotations). Share a single iterative stack-based Tree-Sitter CST walker (`extract_cst_tokens`) across Java, JavaScript/JSX, and TypeScript/TSX—stripping comments, `package_declaration`, `import_declaration`, `import_statement`, and TS `interface_declaration`, `type_alias_declaration`, `type_annotation`, `type_parameters`, `ambient_declaration`, and `implements_clause`. Group `.js`/`.jsx`/`.mjs`/`.cjs` and `.ts`/`.tsx`/`.mts`/`.cts` into one shared `"ecmascript"` comparison bucket (Q5) and preserve repeated executable boilerplate/cross-cutting logic (Q2).
- **Rationale:** Extracting CST tokens inside `parse_java_file`, `parse_javascript_file`, and `parse_typescript_file` guarantees **zero double-parsing** per file. Stripping TypeScript compile-time annotations yields identical normalized token sequences for equivalent JS and TS code, surfacing cross-extension duplication in mixed JS/TS repositories while keeping `python` and `java` isolated.
- **Alternatives considered:**
  1. *Separate `"javascript"` and `"typescript"` comparison buckets:* Rejected per Q5 default because `.js` and `.tsx`/`.ts` in hybrid repositories share the same ECMAScript runtime syntax once type annotations are stripped.
  2. *Second-pass re-parse during codebase aggregation:* Rejected to avoid 2× Tree-Sitter parsing latency.

---

## 5. Automatic Standard Generated-Code Exclusion

- **Decision:** Exclude generated source files before indexing via `is_generated_source(...)` (Q4):
  - **Filename suffixes:** `*_pb2.py`, `*_pb2_grpc.py`, `*.generated.*`, `*.gen.*`, `*_pb.*`, `*.pb.*`.
  - **Leading header comments (first 15 lines, comment-prefixed lines only):** boundary-matched `@generated\b` (explicitly rejecting `@not-generated`), `DO NOT EDIT`, `AUTO-GENERATED`, `Generated by`, `Code generated by`.
  - **Java annotations:** `@Generated`, `@javax.annotation.Generated`, `@javax.annotation.processing.Generated`, `@jakarta.annotation.Generated`.
  - **User config globs:** `dry_exclude_globs` matched with `fnmatch` on POSIX relative paths.
- **Rationale:** Prevents protobuf stubs, OpenAPI/GraphQL codegen, and annotation-processor outputs from skewing Clean Code scores under aggressive Type-2/3 detection while inspecting comment markers strictly so runtime strings containing `"generated by user"` are never falsely skipped.
- **Alternatives considered:**
  1. *Subprocess heuristics or gitignore parsing:* Rejected to keep analysis self-contained and predictable.
  2. *Path-only exclusions:* Rejected per Q4 because generated Java/TS/Python files commonly live alongside handwritten source inside `src/`.

---

## 6. Rubric Integration, Test-File Policy, Modularity & Baseline Calibration

- **Decision:** Integrate DRY penalties into **Clean Code (15%)** (`Type-1: -5.0`, `Type-2: -4.0`, `Type-3: -3.0`, excess density `-0.5/pct` above `10.0%` src / `15.0%` test, caps `35.0` src / `25.0` test) alongside standalone `dry_score`, `duplication_ratio`, `duplicated_loc`, and `DrySummary` metrics (Q1), enforce relaxed test thresholds (`55` tokens, `8` lines) and `src`/`test` partition isolation (Q3), organize DRY code into 5 focused modules (`dry_models.py`, `dry_tokens.py`, `dry_type3.py`, `dry_scoring.py`, `dry_engine.py`) with every file `<= 350` LOC and `<= 5` internal imports, and empirically calibrate against the 160 baseline samples in `samples/`.
- **Rationale:** Preserves the 5-dimension composite contract and clean file outputs when `clone_groups_count == 0`, enforces worst-dimension ceilings (`Clean < 75.0` caps composite `<= 79.5`) when duplication is severe, allows self-contained DAMP tests, and satisfies `py-code-health`'s own strict Grade-A self-health constraints (`<= 25` LOC/func, `CC <= 5`, `<= 5` internal imports/module).
- **Alternatives considered:**
  1. *Adding a 6th weighted rubric dimension immediately:* Deferred per Q1 resolution; weights inside Clean Code will be validated and fine-tuned empirically against real samples first.
  2. *Single monolithic `dry_engine.py` (>700 LOC):* Rejected because it violates `py-code-health` modularity limits (`max_ideal_file_loc = 350`, `max_ideal_internal_imports = 5`).
