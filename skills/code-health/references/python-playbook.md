# Python Refactoring Playbook by Dimension

> **Profile:** `python` · **Detection:** `.py` files (stdlib `ast`, zero external dependencies) · **Force:** `--lang python`
> **Worked examples:** [good](../../../samples/python/good/) · [bad](../../../samples/python/bad/)

This reference provides targeted refactoring patterns to resolve deterministic code health penalties in Python code.

---

## 1. Single Responsibility & Cohesion (SRP)

- **Finding: `SRP: mixes X concerns (presentation, filesystem_io, ...)`**
  - *Cause:* Function mixes printing/UI output, raw file I/O, subprocess execution, or data serialization inside business logic.
  - *Fix:* Separate pure business logic from I/O. Extract filesystem writes (`Path.write_text`), console printing, or JSON/YAML operations into dedicated adapter or entrypoint functions.
- **Finding: `SRP: facade delegation keyword argument collision`**
  - *Cause:* When splitting large modules or God-classes into submodules, delegating calls using `**kwargs` or `**options` causes `TypeError: got multiple values for keyword argument` if an explicit parameter is also passed.
  - *Fix:* Always sanitize or pop explicit keys (`options.pop("param_name", None)`) before delegating forwarded option dictionaries.
- **Finding: `SRP: optional argument defaults with None in frameworks`**
  - *Cause:* In Typer CLI or FastMCP RPC tools, optional parameters may receive `None` explicitly as default. `kwargs.get("key", default)` still returns `None` because the key exists in the dictionary.
  - *Fix:* Use `kwargs.get("key") or default` or defensive coercion `str(val) if val is not None else default`.
- **Finding: `SRP: preserving complete predicates in scanner / walker refactors`**
  - *Cause:* When refactoring complex directory walkers or repository detectors into helpers, unintentionally omitting an alternative predicate (e.g. checking `INDEX.md` or `.git` while dropping `AGENTS.md`) causes regressions in repository discovery.
  - *Fix:* Extract boolean predicates into dedicated, single-responsibility helper functions (e.g., `_is_candidate_kb_dir()`) to preserve 100% of branch logic while reducing function complexity.
- **Finding: `SRP: high external call fan-out=X (>6)`**
  - *Cause:* Function calls too many distinct external systems or modules.
  - *Fix:* Introduce an intermediary coordinator or data structure to bundle interactions, or split into smaller sequential steps.
- **Finding: `SRP: X bool default flag parameter(s)`**
  - *Cause:* Parameter like `def process(data, save_to_disk: bool = True):` indicates two different execution paths combined into one function.
  - *Fix:* Split into two distinct functions (e.g., `process_data()` and `process_and_save_data()`), or pass a strategy/callable instead.
- **Finding: `SRP: LCOM4=X disconnected method groups`**
  - *Cause:* Methods in a class do not share instance state (`self.x`), indicating two or more unrelated responsibilities jammed into one class.
  - *Fix:* Split the class into separate, cohesive classes grouped by the state attributes they access, or turn stateless methods into standalone module-level functions.

---

## 2. Size & Readability

- **Finding: `Size: LOC=X (>25)`**
  - *Cause:* Function exceeds 25 non-comment statements in `src/` (or 40 statements in `tests/`).
  - *Fix:* Extract logical chunks (loop bodies, validation blocks, formatting steps) into private helper functions (`_validate_input()`, `_format_row()`).
  - *Note on Contract & Schema Docstrings:* For FastMCP tools, Typer CLI commands, or OpenAPI generators, docstrings form the runtime API contract (`openapi.json`, `--help`). Never truncate or delete docstring sections (`Args:`, `Returns:`) simply to reduce LOC.
- **Finding: `Size: file LOC=X (>350)`**
  - *Cause:* Module exceeds 350 lines of code.
  - *Fix:* Partition large files into cohesive submodules grouped by domain or workflow (e.g. `test_cli_contracts.py` -> `test_cli_contracts_workspace.py`, `test_cli_contracts_scaffold.py`, with an `__init__.py` re-exporting if necessary).
- **Finding: `Size: params=X (>4)`**
  - *Cause:* Function accepts more than 4 arguments (or > 6 for `@app.command` entrypoints).
  - *Fix:* Group related parameters into a dataclass, `@dataclass(frozen=True)`, or `TypedDict`.
- **Finding: `Size: nesting depth=X (>3)`**
  - *Cause:* Deeply nested `if`, `for`, `while`, or `try` blocks.
  - *Fix:* Invert `if` conditions to use early returns / guard clauses:
    ```python
    # Before (nesting = 3):
    if user is not None:
        if user.is_active:
            perform_action()

    # After (nesting = 1):
    if user is None or not user.is_active:
        return
    perform_action()
    ```

---

## 3. Complexity & Control Flow

- **Finding: `Complexity: CC=X (>5)` or `Complexity: cognitive=X (>8)`**
  - *Cause:* High branching, multiple `elif`/`else` chains, nested loops, and compound boolean expressions.
  - *Fix:*
    - Replace long `if/elif/elif` chains with dictionary lookups, `match` statements, or dispatch tables.
    - Extract nested loops into generator expressions or helper functions.
- **Finding: `Complexity: returns=X (>3)`**
  - *Cause:* More than 3 return points in a single function.
  - *Fix:* Consolidate exit paths or extract pre-validation logic into a separate validator function.

---

## 4. Clean Code & Maintainability

- **Finding: `Clean: missing return type annotation` or `untyped param(s)`**
  - *Fix:* Add explicit type annotations to all parameters and return values (e.g. `def format_item(name: str, count: int) -> str:`).
- **Finding: `Clean: missing public docstring`**
  - *Fix:* Add a concise docstring describing the function's purpose, parameters, and return value.
- **Finding: `Clean: bare except` or `swallowed broad except Exception`**
  - *Fix:* Catch specific exceptions (e.g. `except (FileNotFoundError, ValueError):`). Never use bare `except:`. If catching `Exception`, log it, re-raise it, or record the error rather than swallowing with `pass`.
- **Finding: `Clean: mid-file/late import(s)` (-4.0 pts each)**
  - *Cause:* Imports placed after line 50 or inside functions/fixtures.
  - *Fix:* Hoist all imports to module top level. In test suites, avoid inline `import subprocess` or `import json` inside test functions or fixtures. Use top-level imports and pytest fixtures or module patching if isolation is needed.
- **Finding (Tests): `Clean (Test): test has 0 assertions` (-30.0 pts)**
  - *Cause:* Test function has no direct `assert` statements (e.g. when assertions are delegated to a helper function).
  - *Fix:* Add explicit `assert` statements or `pytest.raises()` checks. If extracting verification into sub-step helper functions, ensure the top-level test function retains explicit assertions on the returned outcomes or status models.
- **Finding (Tests): `Clean (Test): X assertions in single test (>8)`**
  - *Cause:* End-to-end and contract tests frequently chain 15–30 assertions in a single test, triggering heavy penalty deductions (-3.0 pts per assertion > 8).
  - *Fix:* Split large multi-step workflows into focused test functions, or decompose into chronological sub-step verification helpers that test $\le 8$ assertions each.
- **Finding: `Clean (DRY): DRY-XXX (type1|type2|type3, N toks, M LOC) L<start>-<end> in <symbol> matches <peer>:<start>-<end> (<peer_symbol>)`**
  - *Cause:* Exact (`type1`), identifier/literal-renamed (`type2`), or gapped/near-miss (`type3`) duplicated logic meeting thresholds ($\ge 35$ tokens / $\ge 5$ lines in source files; $\ge 55$ tokens / $\ge 8$ lines inside test functions).
  - *Fix:* Extract shared domain validators, parsers, or formatters into a reusable helper function (parameterized by changing inputs/callbacks). In test suites, consolidate repeated multi-step setup/assert workflows into `@pytest.mark.parametrize` or focused verification helpers while keeping test cases self-contained (`tests/` ignores module-level static fixture data when test functions are present).

---

## 5. Security & Operational Hygiene

- **Finding: `Security: subprocess call with shell=True`**
  - *Fix:* Remove `shell=True`. Pass the command as a list: `subprocess.run(["git", "status"], check=True)`.
- **Finding: `Security: subprocess command not passed as list`**
  - *Fix:* Convert command string to `list[str]`.
- **Finding: `Security: unsafe yaml.load() without SafeLoader`**
  - *Fix:* Use `yaml.safe_load(content)`.
- **Finding: `Security: destructive/write Path operation without explicit resolve/boundary check`**
  - *Fix:* Call `.resolve()` and verify path containment (e.g., `target_path.is_relative_to(safe_root)`).
- **Finding: `Security: file mutation (L...) before branch checkout (L...)`**
  - *Fix:* Ensure Git branch checkouts occur before file modifications, not after.
