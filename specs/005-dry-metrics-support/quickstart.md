# Quickstart Validation Guide: Multi-Language DRY Metrics

**Date**: 2026-11-22  
**Feature**: `005-dry-metrics-support`  
**Spec**: [spec.md](./spec.md) | **Data Model**: [data-model.md](./data-model.md) | **Contracts**: [cli-contract.md](./contracts/cli-contract.md) · [dry-engine-contract.md](./contracts/dry-engine-contract.md)

---

## 1. Prerequisites

- **Python:** 3.11+ (on Windows with `uv`, pin `--python 3.13` to use prebuilt native `tree-sitter` wheels without needing MSVC build tools).
- **Optional Native Grammars (already in project extras):** `tree-sitter>=0.23.0`, `tree-sitter-java>=0.23.0`, `tree-sitter-javascript>=0.23.0`, `tree-sitter-typescript>=0.23.0`. Zero new dependencies required.

---

## 2. Core End-to-End Validation Scenarios

### A. Single-File & Multi-File CLI Scans
```powershell
# Single Python file with intra-file duplication (actionable DRY-001 findings)
python scripts/code_health.py samples/python/bad/test_basic.py --no-git

# Multi-file scan across scripts/ with JSON and Markdown scorecard exports
python scripts/code_health.py scripts --no-git --json-out tmp_dry.json --markdown-out tmp_dry.md

# Opt out of DRY detection cleanly (clone_groups_count == 0, dry_score == 100.0)
python scripts/code_health.py scripts --no-git --no-dry --format json
```
**Expected:**
- Clean duplicate-free scans emit no `[DUPLICATE CODE & DRY SUMMARY]` console section.
- Scans with clones render `[DUPLICATE CODE & DRY SUMMARY]` in console, `## Duplicate Code & DRY Findings` in Markdown, and populated `dry` + per-file `duplicated_loc` / `duplication_ratio` / `dry_score` fields in JSON (per [cli-contract.md](./contracts/cli-contract.md)).

### B. Automated Unit, Polyglot & Benchmark Suite
```powershell
uv run --python 3.13 --with pytest --with tree-sitter --with tree-sitter-java --with tree-sitter-javascript --with tree-sitter-typescript pytest -v
```
**Expected:**
- `tests/unit/test_dry_models_and_tokens.py`, `tests/unit/test_dry_engine.py`, and `tests/unit/test_dry_integration.py` pass across Type-1/2/3 clones in Python, Java, JS/JSX, and TS/TSX (including shared `ecmascript` JS↔TS matching, generated-code exclusion, non-bijective Type-2 rejection, `--config` TOML/JSON overrides, and skill mirror byte-for-byte parity).
- 100-file (~15,000 LOC) benchmark completes in `< 2.5s` with `tracemalloc` peak `< 25 MB`.
- All 160 baseline samples in `tests/unit/test_language_scorecard_samples.py` pass with zero regressions on clean baselines and strict `good > bad` pair dominance.
- `tests/unit/test_skill_playbooks.py` passes (all playbook links resolve; `README.md` contains no penalty rules).

### C. Self-Health Quality Gate
```powershell
python scripts/code_health.py scripts --no-git --fail-under 90.0 --only-flagged
```
**Expected:** Exit code `0`, overall composite score `>= 90.0` (Grade A), and all new `_code_health/dry_*.py` modules achieve Grade A (`>= 95.0`).
