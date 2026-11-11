# Superspec Code Review Checklist: TypeScript Language Profile (`003-typescript-language-profile`)

**Reviewed Range**: `610df8e` (`main`) .. `a5083bf` (`add_typescript_support`)  
**Review Date**: 2026-11-10  
**Verdict**: **All Findings Fixed & Verified via TDD**

---

## Compliance Summary

| Dimension | Status | Notes |
|:---|:---:|:---|
| **US1 (Discovery & Scoring)** | Pass | Discovery, skips (`*.d.*`, `node_modules`, `dist`, `build`, `coverage`, `.next`, `.nuxt`, minified + stderr notice), `FR-024` malformed syntax grading (`0.0 / F`), and `FR-025` object literal method `qualname` all verified. |
| **US2 (Missing Parser Guard)** | Pass | Exit code `2` + console/JSON instructions verified; non-TS targets unaffected. |
| **US3 (Typing & Escape Hatches)** | Pass | Strict typing, `any` (including generics/typed arrows), `@ts-ignore`/`@ts-nocheck` (including class fields), `!`, `set` accessors, optional booleans without defaults, and ECMAScript hygiene all verified. |
| **US4 (Security Hygiene)** | Pass | `eval`, `new Function`, string timers, `__proto__`/`setPrototypeOf`, `with`, and query concat/interpolation all enforced. |
| **US5 (Test & Assertion Hygiene)** | Pass | Core BDD (`it`/`test` + modifiers), `to.equal` & extended matchers, `_test.mts`/`_test.cts`, and `0`/`>8` checks verified. |
| **Constitution I–IV** | Pass | Library-first, CLI, determinism, and backward compatibility (`147/147` tests) hold; all files in `scripts/_code_health/` score Grade A (`<= 350` LOC for all new/modified modules) and `_TSVisitor` class now scores Grade A (`99.2`). |

---

## Findings (Confidence >= 80)

### Critical (Must Fix)

- [x] **C1 [Confidence: 98] Malformed TypeScript syntax (`ERROR` / `MISSING` CST nodes) scores Grade A instead of `0.0` (Grade F)** (`FR-024`, Edge Case #8)
  - Location: `scripts/_code_health/ts_parser.py`, `scripts/_code_health/ts_smells.py`, `scripts/_code_health/ir_models.py`, `scripts/_code_health/module_engine.py`
  - Resolution: Added `IRModule.syntax_errors`, `collect_syntax_errors` scanning `ERROR`/`is_missing` CST nodes when `has_error` is `True`, and `0.0` (Grade F) short-circuit scoring in `_score_ir_module` emitting `"Syntax: parse error at L<line>"`.
- [x] **C2 [Confidence: 97] Object literal methods (`object.method`) are never extracted** (`FR-025`)
  - Location: `scripts/_code_health/ts_parser.py` (`_extract_ts_prop_func`, `_extract_ts_var_funcs`)
  - Resolution: Extracted `method_definition` and function-valued `pair` nodes inside `object` (and `as`/`satisfies`) initializers with `qualname = f"{v_name}.{pn}"`.

### Important (Should Fix)

- [x] **I1 [Confidence: 96] TypeScript `set` accessors receive false `-10.0 pts` missing return type penalty** (`FR-011`)
  - Location: `scripts/_code_health/ts_parser.py` (`_extract_ts_return_type`)
  - Resolution: Returned `"void"` when `method_definition` contains a `set` child.
- [x] **I2 [Confidence: 95] Optional boolean params without defaults (`flag?: boolean`) falsely trigger `-6.0 pts` SRP default-flag penalty** (`FR-015`)
  - Location: `scripts/_code_health/ts_parser.py` (`_parse_ts_param`)
  - Resolution: Set `has_default=has_assign` only, while preserving `"inferred"` typing for untyped `optional_parameter` nodes.
- [x] **I3 [Confidence: 93] Abstract method signatures (`abstract run(): void;`) are omitted from abstract classes** (Edge Case #4)
  - Location: `scripts/_code_health/ts_parser.py` (`TSClassExtractor.extract_methods`)
  - Resolution: Extracted `abstract_method_signature` nodes with `modifiers=["abstract"]`, excluding bodyless abstract signatures from LCOM4 component calculation.
- [x] **I4 [Confidence: 92] Constructor parameter-property detection uses substring matching (`is_public = true` false positive, multiline `private\n svc` false negative)** (`FR-009`, Edge Case #2)
  - Location: `scripts/_code_health/ts_parser.py` (`_extract_param_properties`)
  - Resolution: Checked CST parameter children directly for `accessibility_modifier` or `readonly`.
- [x] **I5 [Confidence: 92] Exported generator functions (`export function*`) are silently skipped**
  - Location: `scripts/_code_health/ts_parser.py` (`_EXPORTED_UNIT_TYPES`)
  - Resolution: Included `"generator_function_declaration"` in `_EXPORTED_UNIT_TYPES`.
- [x] **I6 [Confidence: 90] `@ts-ignore` / `@ts-nocheck` comments on class fields/members outside function bodies are missed** (`FR-013`)
  - Location: `scripts/_code_health/ts_smells.py` (`count_unclaimed_ts_ignores`), `scripts/_code_health/ts_parser.py` (`_TSCtx.claimed`)
  - Resolution: Recursively counted unclaimed `@ts-ignore`/`@ts-nocheck` comment lines across the full CST while claiming test callback lines in `ctx.claimed`.
- [x] **I7 [Confidence: 88] Automated tests miss required spec scenarios and edge cases**
  - Location: `tests/unit/test_typescript_edge_cases.py`
  - Resolution: Added 11 behavioral tests covering C1–C2, I1–I6, empty/comment files, `--lang ts`, `to.equal`, `_test.mts`/`_test.cts`, and `collect_git_stats` (`.d.ts` exclusion).

### Suggestions / Minor (Nice to Have)

- [x] **S1 [Confidence: 86] Unparenthesized `async` arrows (`async x => x + 1`) and generic `<T extends any>` type constraints**
  - Location: `scripts/_code_health/ts_parser.py` (`_extract_ts_params`), `scripts/_code_health/ts_smells.py` (`scan_header`)
  - Resolution: Extracted `identifier` before `=>` for unparenthesized `arrow_function` nodes and included `"type_parameters"` in `scan_header`.
- [x] **S2 [Confidence: 88] Self-health polish on `_TSVisitor` (Grade `C`, `CC=39`) and `module_engine.py` mid-file imports**
  - Location: `scripts/_code_health/ts_parser.py` (`_TSVisitor`), `scripts/_code_health/module_engine.py` (`_analyze_native`)
  - Resolution: Extracted `_record_ts_call` / `_dispatch_ts_expr` / `_extract_ts_test_fn` (bringing `_TSVisitor` to Grade A `99.2`) and unified `_NATIVE_PARSERS` in `module_engine.py` (bringing `module_engine.py` to Grade A `99.3` with zero mid-file import penalties).
- [x] **S3 [Confidence: 83] Typed arrow variables (`const fn: (a: number) => number = (a) => ...`) trigger false typing penalties**
  - Location: `scripts/_code_health/ts_parser.py` (`_extract_ts_var_funcs`, `_build_ts_ir_function`)
  - Resolution: Propagated enclosing `variable_declarator` `type_annotation` for signature inference while still scanning `var_type_node` for `any`.
- [x] **S4 [Confidence: 82] Contract & test-suffix alignment (`coverage` dir, minified skip notice, `_test.mts`/`_test.cts`)**
  - Location: `scripts/_code_health/models.py`, `scripts/_code_health/reporting.py`, `scripts/_code_health/module_engine.py`
  - Resolution: Added `"coverage"` to `IGNORED_SCAN_DIRS`, `_test.mts`/`_test.cts` to `is_test_file_path`, and `Skipped minified asset: <path>` notice on `stderr` for minified files.
