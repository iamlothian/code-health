"""Unit tests for Web UI Framework Code Health Profiles (React, Next.js, Angular)."""

from __future__ import annotations

from pathlib import Path
import sys

_SCRIPTS_DIR = str(Path(__file__).resolve().parents[2] / "scripts")
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from _code_health.module_engine import _NATIVE_PARSERS, _parse_git_log_output, is_test_file_path  # noqa: E402
from _code_health.reporting import CodeHealthRunner  # noqa: E402
from code_health import _build_arg_parser  # noqa: E402


def test_is_test_file_path_recognizes_jsx_conventions() -> None:
    """Recognize *.test.jsx, *.spec.jsx, *_test.jsx, and test_*.jsx as test files."""
    assert is_test_file_path("src/components/Button.test.jsx") is True
    assert is_test_file_path("src/components/Button.spec.jsx") is True
    assert is_test_file_path("src/components/button_test.jsx") is True
    assert is_test_file_path("src/components/test_button.jsx") is True
    assert is_test_file_path("src/__tests__/Card.jsx") is True

    assert is_test_file_path("src/components/Button.jsx") is False
    assert is_test_file_path("src/pages/index.jsx") is False


def test_jsx_file_discovery_and_minified_skipping(tmp_path: Path) -> None:
    """Discover .jsx files under auto and javascript modes while skipping *.min.jsx and long lines."""
    src_dir = tmp_path / "src"
    src_dir.mkdir(parents=True)
    (src_dir / "Card.jsx").write_text("export function Card() { return <div />; }\n", encoding="utf-8")
    (src_dir / "Card.min.jsx").write_text("export function Card() { return <div />; }\n", encoding="utf-8")
    (src_dir / "bundled.jsx").write_text("const x = '" + "a" * 1050 + "';\n", encoding="utf-8")

    auto_runner = CodeHealthRunner(repo_root=tmp_path, git_mode="no-git")
    auto_rel = [p.relative_to(tmp_path).as_posix() for p in auto_runner._discover_files([tmp_path])]
    assert "src/Card.jsx" in auto_rel
    assert "src/Card.min.jsx" not in auto_rel
    assert "src/bundled.jsx" not in auto_rel

    js_runner = CodeHealthRunner(repo_root=tmp_path, git_mode="no-git", lang_override="javascript")
    js_rel = [p.relative_to(tmp_path).as_posix() for p in js_runner._discover_files([tmp_path])]
    assert "src/Card.jsx" in js_rel
    assert "src/Card.min.jsx" not in js_rel

    assert ".jsx" in _NATIVE_PARSERS
    assert _NATIVE_PARSERS[".jsx"] == ("_code_health.js_parser", "parse_javascript_file")


def test_git_log_accumulator_counts_jsx_commits() -> None:
    """Include .jsx files in git log commit stats."""
    raw_log = "COMMIT:abc123|Alice|feat: add card\nsrc/Card.jsx\n"
    stats = _parse_git_log_output(raw_log)
    assert "src/Card.jsx" in stats
    assert stats["src/Card.jsx"].commits == 1
    assert stats["src/Card.jsx"].feat_commits == 1


def test_cli_framework_help_documents_ui_profiles() -> None:
    """Document react, nextjs, angular, spring-boot, and none in --framework help text."""
    help_text = _build_arg_parser().format_help()
    for token in ("react", "nextjs", "angular", "spring-boot", "none"):
        assert token in help_text


def test_ts_and_jsx_cst_extracts_decorators_directives_and_wrappers(tmp_path: Path) -> None:
    """Extract decorators, module directives, React.memo/forwardRef wrappers, and field initializers."""
    from _code_health.js_parser import parse_javascript_file
    from _code_health.ts_parser import parse_typescript_file

    ng_file = tmp_path / "user.component.ts"
    ng_file.write_text(
        '@Component({ selector: "app-user" })\n'
        "export class UserComponent {\n"
        "  @Input() title: string = '';\n"
        "  private http = inject(HttpClient);\n"
        "  constructor(private svc: UserService) {}\n"
        "  @HostListener('click')\n"
        "  onClick(): void {}\n"
        "}\n",
        encoding="utf-8",
    )
    ng_mod = parse_typescript_file(ng_file, "src/user.component.ts", is_test=False)
    cls = ng_mod.classes[0]
    assert [a.name for a in cls.annotations] == ["Component"]
    fields_by_name = {f.name: f for f in cls.fields}
    assert any(a.name == "Input" for a in fields_by_name["title"].annotations)
    assert fields_by_name["http"].type_annotation == "inject(HttpClient)"
    assert fields_by_name["svc"].type_annotation == "UserService"
    on_click = next(m for m in cls.methods if m.name == "onClick")
    assert any(a.name == "HostListener" for a in on_click.annotations)

    tsx_file = tmp_path / "Card.tsx"
    tsx_file.write_text(
        '"use client";\n'
        "export const Card = React.memo(({ items }: CardProps) => {\n"
        '  const ignore = "not a directive";\n'
        "  return <div>{items.map((item, idx) => <span key={idx}>{item.name}</span>)}</div>;\n"
        "});\n",
        encoding="utf-8",
    )
    tsx_mod = parse_typescript_file(tsx_file, "app/Card.tsx", is_test=False)
    assert tsx_mod.directives == ["use client"]
    assert [f.name for f in tsx_mod.functions] == ["Card"]
    assert tsx_mod.functions[0].jsx_elements_count >= 2
    assert tsx_mod.functions[0].array_index_keys == [4]

    jsx_file = tmp_path / "RefBtn.jsx"
    jsx_file.write_text(
        "export const RefBtn = forwardRef((props, ref) => <button ref={ref}>{props.label}</button>);\n",
        encoding="utf-8",
    )
    jsx_mod = parse_javascript_file(jsx_file, "src/RefBtn.jsx", is_test=False)
    assert [f.name for f in jsx_mod.functions] == ["RefBtn"]
    assert jsx_mod.functions[0].jsx_elements_count == 1


def test_cst_extracts_dom_sinks_and_branch_hook_context(tmp_path: Path) -> None:
    """Capture DOM/XSS sinks and accurate in_branch_or_loop propagation across callbacks."""
    from _code_health.js_parser import parse_javascript_file
    from _code_health.ts_parser import parse_typescript_file

    src = (
        "function Panel({ html, items, ready }) {\n"
        "  const [open, setOpen] = useState(false);\n"
        "  if (ready) { useEffect(() => {}, []); }\n"
        "  useEffect(() => {\n"
        '    if (ready) { fetch("/api"); }\n'
        "  }, []);\n"
        "  el.innerHTML = html;\n"
        '  document.write("bad");\n'
        "  return (\n"
        "    <div dangerouslySetInnerHTML={{ __html: html }}>\n"
        "      {items.map((item) => <span key={item.id}>{item.name}</span>)}\n"
        "    </div>\n"
        "  );\n"
        "}\n"
    )
    tsx = tmp_path / "Panel.tsx"
    tsx.write_text(src, encoding="utf-8")
    jsx = tmp_path / "Panel.jsx"
    jsx.write_text(src, encoding="utf-8")

    for mod in (
        parse_typescript_file(tsx, "src/Panel.tsx", is_test=False),
        parse_javascript_file(jsx, "src/Panel.jsx", is_test=False),
    ):
        fn = mod.functions[0]
        assert fn.array_index_keys == []
        sinks = {name for name, _ in fn.dom_write_sinks}
        assert {"dangerouslySetInnerHTML", "innerHTML", "document.write"} <= sinks
        use_state = next(c for c in fn.calls if c.name == "useState")
        assert use_state.in_branch_or_loop is False
        effects = [c for c in fn.calls if c.name == "useEffect"]
        assert effects[0].in_branch_or_loop is True
        assert effects[1].in_branch_or_loop is False
        fetch_call = next(c for c in fn.calls if c.name == "fetch")
        assert fetch_call.in_branch_or_loop is True


def test_resolve_active_profiles_auto_detect_overrides_and_isolation(tmp_path: Path) -> None:
    """Resolve react/nextjs/angular dynamically with monorepo isolation and safe package.json fallback."""
    from _code_health.profiles import resolve_active_profiles

    pkg = tmp_path / "package.json"
    pkg.write_text('{"dependencies": {"react": "^18.0.0", "next": "^14.0.0"}}', encoding="utf-8")

    # Non-UI backend file in same monorepo must stay pure TS/JS (no UI frameworks)
    backend_ts = tmp_path / "services" / "api" / "handler.ts"
    backend_ts.parent.mkdir(parents=True)
    backend_ts.write_text("export function handle(x: number): number { return x + 1; }\n", encoding="utf-8")
    p_backend = resolve_active_profiles(tmp_path, backend_ts, imports=["express"], has_jsx=False)
    assert p_backend.name == "typescript"
    assert p_backend.frameworks == []

    # Next.js App Router page & JSX React component detection
    app_page = tmp_path / "app" / "dashboard" / "page.tsx"
    app_page.parent.mkdir(parents=True)
    app_page.write_text("export default function Page() { return <main />; }\n", encoding="utf-8")
    p_next = resolve_active_profiles(tmp_path, app_page, imports=[], has_jsx=True)
    assert [fw.name for fw in p_next.frameworks] == ["nextjs"]

    jsx_card = tmp_path / "src" / "Card.jsx"
    jsx_card.parent.mkdir(parents=True)
    jsx_card.write_text("export function Card() { return <div />; }\n", encoding="utf-8")
    p_jsx_pure = resolve_active_profiles(tmp_path, jsx_card, imports=[], has_jsx=True)
    assert p_jsx_pure.name == "javascript"
    assert [fw.name for fw in p_jsx_pure.frameworks] == ["nextjs"]

    # Standalone repo without package.json falls back cleanly to file imports & JSX
    no_pkg_root = tmp_path / "isolated"
    no_pkg_root.mkdir()
    standalone_jsx = no_pkg_root / "Widget.jsx"
    standalone_jsx.write_text("import React from 'react';\n", encoding="utf-8")
    p_react = resolve_active_profiles(no_pkg_root, standalone_jsx, imports=["react"], has_jsx=True)
    assert [fw.name for fw in p_react.frameworks] == ["react"]

    # Malformed package.json gracefully falls back to imports
    bad_root = tmp_path / "badjson"
    bad_root.mkdir()
    (bad_root / "package.json").write_text("{ malformed json !!!", encoding="utf-8")
    ng_file = bad_root / "hero.component.ts"
    ng_file.write_text("import { Component } from '@angular/core';\n", encoding="utf-8")
    p_ng = resolve_active_profiles(bad_root, ng_file, imports=["@angular/core"], has_jsx=False)
    assert p_ng.name == "typescript"
    assert [fw.name for fw in p_ng.frameworks] == ["angular"]

    # Explicit overrides: --framework none and --framework angular
    p_none = resolve_active_profiles(tmp_path, app_page, framework_override="none", imports=["react"], has_jsx=True)
    assert p_none.frameworks == []
    p_forced_react = resolve_active_profiles(no_pkg_root, backend_ts, framework_override="react")
    assert [fw.name for fw in p_forced_react.frameworks] == ["react"]


def test_ui_concern_map_srp_and_xss_sinks_scored_end_to_end(tmp_path: Path) -> None:
    """Detect mixed UI operational concerns and browser/XSS sinks on TSX, JSX, and Angular TS."""
    from _code_health.models import RubricConfig
    from _code_health.module_engine import ModuleAnalyzer

    tsx_bad = tmp_path / "UnsafeBoard.tsx"
    tsx_bad.write_text(
        "import React from 'react';\n"
        "/** Render board and mix concerns dangerously. */\n"
        "export function UnsafeBoard({ html, title }: BoardProps) {\n"
        '  fetch("/api/items");\n'
        '  localStorage.setItem("title", title);\n'
        "  const el = document.getElementById('host');\n"
        "  if (el) { el.innerHTML = html; }\n"
        "  document.write(html);\n"
        "  return <div dangerouslySetInnerHTML={{ __html: html }} />;\n"
        "}\n",
        encoding="utf-8",
    )
    jsx_bad = tmp_path / "UnsafeCard.jsx"
    jsx_bad.write_text(
        "/** Render unsafe card. */\n"
        "export function UnsafeCard(html) {\n"
        "  el.insertAdjacentHTML('beforeend', html);\n"
        "  return <section dangerouslySetInnerHTML={{ __html: html }} />;\n"
        "}\n",
        encoding="utf-8",
    )

    analyzer = ModuleAnalyzer(tmp_path, set(), RubricConfig(), None)
    rep_tsx = analyzer.analyze(tsx_bad)
    fn_tsx = rep_tsx.functions[0]
    assert {"network_io", "storage_io", "dom_mutation", "render_ui"} <= set(fn_tsx.concerns)
    assert any("SRP: mixes" in f for f in fn_tsx.findings)
    assert rep_tsx.scores.security <= 30.0
    assert any("XSS" in f or "Security" in f for f in fn_tsx.findings)

    rep_jsx = analyzer.analyze(jsx_bad)
    assert rep_jsx.scores.security <= 30.0
    assert any("insertAdjacentHTML" in f or "dangerouslySetInnerHTML" in f for f in rep_jsx.functions[0].findings)

    # --framework none suppresses UI framework findings completely
    none_analyzer = ModuleAnalyzer(tmp_path, set(), RubricConfig(), None, framework_override="none")
    rep_none = none_analyzer.analyze(tsx_bad)
    assert rep_none.scores.security == 100.0
    assert "render_ui" not in rep_none.functions[0].concerns


def test_react_rules_of_hooks_sprawl_keys_and_return_type_exemption(tmp_path: Path) -> None:
    """Enforce Rules of Hooks, effect/state sprawl, array-index keys, and JSX return exemption across TSX and JSX."""
    from _code_health.models import RubricConfig
    from _code_health.module_engine import ModuleAnalyzer

    # 1. Idiomatic TSX & JSX cards should score Grade A (>= 90.0) without return type penalty
    clean_tsx = tmp_path / "ProfileCard.tsx"
    clean_tsx.write_text(
        "import React, { useEffect, useState } from 'react';\n"
        "interface ProfileProps { name: string; ready: boolean; items: { id: string; label: string }[]; }\n"
        "/** Render user profile card. */\n"
        "export const ProfileCard = React.memo(({ name, ready, items }: ProfileProps) => {\n"
        "  const [count, setCount] = useState(0);\n"
        "  useEffect(() => { if (ready) { setCount(1); } }, [ready]);\n"
        "  return <div><span>{name}:{count}</span>{items.map((x) => <b key={x.id}>{x.label}</b>)}</div>;\n"
        "});\n",
        encoding="utf-8",
    )
    clean_jsx = tmp_path / "ProfileCard.jsx"
    clean_jsx.write_text(
        "import React, { useEffect, useState } from 'react';\n"
        "/** Render user profile card.\n * @param {{ name: string, ready: boolean }} props\n */\n"
        "export const ProfileCard = forwardRef((props, ref) => {\n"
        "  const [count, setCount] = useState(0);\n"
        "  useEffect(() => { if (props.ready) { setCount(1); } }, [props.ready]);\n"
        "  return <div ref={ref}>{props.name}:{count}</div>;\n"
        "});\n",
        encoding="utf-8",
    )
    # 2. Flawed React component with conditional hook, effect/state sprawl, and key={idx}
    bad_tsx = tmp_path / "BrokenDashboard.tsx"
    bad_tsx.write_text(
        "import React, { useEffect, useState } from 'react';\n"
        "/** Broken dashboard component. */\n"
        "export function BrokenDashboard(props) {\n"
        "  const [a, setA] = useState(0);\n"
        "  const [b, setB] = useState(0);\n"
        "  const [c, setC] = useState(0);\n"
        "  const [d, setD] = useState(0);\n"
        "  const [e, setE] = useState(0);\n"
        "  const [f, setF] = useState(0);\n"
        "  if (props.ready) { useEffect(() => { setA(1); }, []); }\n"
        "  useEffect(() => { setB(1); }, []);\n"
        "  useEffect(() => { setC(1); }, []);\n"
        "  return <ul>{props.items.map((it, idx) => <li key={idx}>{it}{d}{e}{f}</li>)}</ul>;\n"
        "}\n",
        encoding="utf-8",
    )
    bad_jsx = tmp_path / "BrokenList.jsx"
    bad_jsx.write_text(
        "/** Broken list. */\n"
        "export function BrokenList(items, ready) {\n"
        "  if (ready) { useState(0); }\n"
        "  return <ul>{items.map((it, i) => <li key={i}>{it}</li>)}</ul>;\n"
        "}\n",
        encoding="utf-8",
    )
    # 3. Custom hook useDashboardState is exempt from component hook sprawl, still typed in TS
    hook_ts = tmp_path / "useDashboardState.ts"
    hook_ts.write_text(
        "import { useEffect, useState } from 'react';\n"
        "/** Manage dashboard state hook. */\n"
        "export function useDashboardState(initial: number): number {\n"
        "  const [a] = useState(initial);\n"
        "  const [b] = useState(0);\n"
        "  const [c] = useState(0);\n"
        "  const [d] = useState(0);\n"
        "  const [e] = useState(0);\n"
        "  const [f] = useState(0);\n"
        "  useEffect(() => {}, []);\n"
        "  useEffect(() => {}, []);\n"
        "  useEffect(() => {}, []);\n"
        "  return a + b + c + d + e + f;\n"
        "}\n",
        encoding="utf-8",
    )

    analyzer = ModuleAnalyzer(tmp_path, set(), RubricConfig(), None)
    rep_clean_tsx = analyzer.analyze(clean_tsx)
    assert rep_clean_tsx.scores.grade == "A"
    assert not any("missing return type" in x for x in rep_clean_tsx.functions[0].findings)
    assert not any("Rules of Hooks" in x for x in rep_clean_tsx.functions[0].findings)

    rep_clean_jsx = analyzer.analyze(clean_jsx)
    assert rep_clean_jsx.scores.grade == "A"

    rep_bad_tsx = analyzer.analyze(bad_tsx)
    fn_bad = rep_bad_tsx.functions[0]
    assert any("Rules of Hooks" in x for x in fn_bad.findings)
    assert any("useEffect" in x and "SRP" in x for x in fn_bad.findings)
    assert any("useState" in x and "SRP" in x for x in fn_bad.findings)
    assert any("key" in x and "index" in x.lower() for x in fn_bad.findings)
    # Typed prop enforcement is preserved for untyped props on TSX component
    assert any("untyped param(s) (props)" in x for x in fn_bad.findings)
    assert rep_bad_tsx.scores.composite < 80.0

    rep_bad_jsx = analyzer.analyze(bad_jsx)
    assert any("Rules of Hooks" in x for x in rep_bad_jsx.functions[0].findings)
    assert any("key" in x and "index" in x.lower() for x in rep_bad_jsx.functions[0].findings)

    rep_hook = analyzer.analyze(hook_ts)
    assert not any("sprawl" in x.lower() for x in rep_hook.functions[0].findings)
    assert rep_hook.scores.grade == "A"


def test_nextjs_app_router_client_server_boundaries(tmp_path: Path) -> None:
    """Flag server imports in 'use client' and missing 'use client' in app/, exempting pages/ and use* hooks."""
    from _code_health.models import RubricConfig
    from _code_health.module_engine import ModuleAnalyzer

    (tmp_path / "package.json").write_text('{"dependencies": {"next": "^14.2.0", "react": "^18.2.0"}}', encoding="utf-8")

    # 1. Server-only import inside 'use client' module (-30.0 pts Security)
    leak_client = tmp_path / "app" / "LeakClient.tsx"
    leak_client.parent.mkdir(parents=True)
    leak_client.write_text(
        '"use client";\n'
        "import fs from 'node:fs';\n"
        "/** Client component leaking server fs import. */\n"
        "export function LeakClient() {\n"
        "  return <div>{String(Boolean(fs))}</div>;\n"
        "}\n",
        encoding="utf-8",
    )

    # 2. Missing 'use client' in app/ component calling useState (-15.0 pts Clean)
    missing_dir = tmp_path / "app" / "Counter.tsx"
    missing_dir.write_text(
        "import { useState } from 'react';\n"
        "/** Counter missing use client directive. */\n"
        "export function Counter() {\n"
        "  const [n, setN] = useState(0);\n"
        "  return <button onClick={() => setN(n + 1)}>{n}</button>;\n"
        "}\n",
        encoding="utf-8",
    )

    # 3. Clean 'use client' component + exempt pages/ route + exempt useCounter.ts hook
    clean_client = tmp_path / "app" / "SafeCounter.tsx"
    clean_client.write_text(
        '"use client";\n'
        "import { useState } from 'react';\n"
        "/** Safe client counter. */\n"
        "export function SafeCounter() {\n"
        "  const [n, setN] = useState(0);\n"
        "  return <button onClick={() => setN(n + 1)}>{n}</button>;\n"
        "}\n",
        encoding="utf-8",
    )
    pages_route = tmp_path / "pages" / "legacy.tsx"
    pages_route.parent.mkdir(parents=True)
    pages_route.write_text(
        "import { useState } from 'react';\n"
        "/** Pages router file does not need 'use client'. */\n"
        "export default function Legacy() {\n"
        "  const [n] = useState(0);\n"
        "  return <span>{n}</span>;\n"
        "}\n",
        encoding="utf-8",
    )
    hook_mod = tmp_path / "app" / "useCounter.ts"
    hook_mod.write_text(
        "import { useState } from 'react';\n"
        "/** Standalone hook module exempt from 'use client' directive rule. */\n"
        "export function useCounter(): number {\n"
        "  const [n] = useState(0);\n"
        "  return n;\n"
        "}\n",
        encoding="utf-8",
    )

    analyzer = ModuleAnalyzer(tmp_path, set(), RubricConfig(), None)
    rep_leak = analyzer.analyze(leak_client)
    assert rep_leak.scores.security <= 70.0
    assert any("use client" in f and "server" in f.lower() for f in rep_leak.findings)

    rep_missing = analyzer.analyze(missing_dir)
    assert rep_missing.scores.clean <= 85.0
    assert any("use client" in f and "App Router" in f for f in rep_missing.findings)

    rep_safe = analyzer.analyze(clean_client)
    assert rep_safe.scores.grade == "A"
    assert rep_safe.findings == []

    rep_pages = analyzer.analyze(pages_route)
    assert not any("use client" in f for f in rep_pages.findings)

    rep_hook = analyzer.analyze(hook_mod)
    assert not any("use client" in f for f in rep_hook.findings)


def test_angular_di_layering_subscriptions_xss_and_exemptions(tmp_path: Path) -> None:
    """Enforce Angular @Component HttpClient layering, unmanaged .subscribe(), XSS bypass, and DI/LCOM4 exemptions."""
    from _code_health.models import RubricConfig
    from _code_health.module_engine import ModuleAnalyzer
    from _code_health.profiles import resolve_active_profiles

    # 1. Bad Angular @Component: injects HttpClient, unmanaged .subscribe(), bypassSecurityTrustHtml
    bad_ng = tmp_path / "orders.component.ts"
    bad_ng.write_text(
        "import { Component, OnInit } from '@angular/core';\n"
        "import { HttpClient } from '@angular/common/http';\n"
        "import { DomSanitizer } from '@angular/platform-browser';\n"
        "/** Orders component with layering, leak, and XSS issues. */\n"
        "@Component({ selector: 'app-orders', template: '<div></div>' })\n"
        "export class OrdersComponent implements OnInit {\n"
        "  orders: string[] = [];\n"
        "  trusted: unknown = null;\n"
        "  constructor(private http: HttpClient, private sanitizer: DomSanitizer) {}\n"
        "  /** Initialize orders stream. */\n"
        "  ngOnInit(): void {\n"
        "    this.http.get<string[]>('/api/orders').subscribe((res: string[]) => {\n"
        "      this.orders = res;\n"
        "    });\n"
        "  }\n"
        "  /** Render unsafe banner HTML. */\n"
        "  renderBanner(raw: string): void {\n"
        "    this.trusted = this.sanitizer.bypassSecurityTrustHtml(raw);\n"
        "  }\n"
        "}\n",
        encoding="utf-8",
    )

    # 2. Bad @Component using field inject(HttpClient)
    bad_inject_ng = tmp_path / "inject.component.ts"
    bad_inject_ng.write_text(
        "import { Component, inject } from '@angular/core';\n"
        "import { HttpClient } from '@angular/common/http';\n"
        "/** Component using inject(HttpClient) directly. */\n"
        "@Component({ selector: 'app-inject', template: '<p></p>' })\n"
        "export class InjectComponent {\n"
        "  private http = inject(HttpClient);\n"
        "}\n",
        encoding="utf-8",
    )

    # 3. Clean @Component with service DI, takeUntilDestroyed teardown, LCOM4=3 disconnected handlers, and DI ctor without docstring
    clean_ng = tmp_path / "user-panel.component.ts"
    clean_ng.write_text(
        "import { Component, DestroyRef, inject, OnInit } from '@angular/core';\n"
        "import { takeUntilDestroyed } from '@angular/core/rxjs-interop';\n"
        "/** Clean Angular component with proper service delegation and teardown. */\n"
        "@Component({ selector: 'app-user-panel', template: '<section></section>' })\n"
        "export class UserPanelComponent implements OnInit {\n"
        "  private readonly destroyRef = inject(DestroyRef);\n"
        "  constructor(private readonly userService: UserService) {}\n"
        "  /** Initialize subscription with takeUntilDestroyed. */\n"
        "  ngOnInit(): void {\n"
        "    this.userService.loadUsers().pipe(takeUntilDestroyed(this.destroyRef)).subscribe(() => {});\n"
        "  }\n"
        "  /** Handle filter selection. */\n"
        "  onSelect(id: string): string { return id; }\n"
        "  /** Format display title. */\n"
        "  formatLabel(name: string): string { return name.trim(); }\n"
        "}\n",
        encoding="utf-8",
    )

    # 4. Clean @Component with ngOnDestroy + unsubscribe teardown & @Injectable service allowed to inject HttpClient
    destroy_ng = tmp_path / "legacy-sub.component.ts"
    destroy_ng.write_text(
        "import { Component, OnDestroy, OnInit } from '@angular/core';\n"
        "/** Component tearing down via ngOnDestroy unsubscribe. */\n"
        "@Component({ selector: 'app-legacy', template: '' })\n"
        "export class LegacySubComponent implements OnInit, OnDestroy {\n"
        "  private sub: SubscriptionLike | null = null;\n"
        "  constructor(private readonly svc: FeedService) {}\n"
        "  /** Subscribe on init. */\n"
        "  ngOnInit(): void { this.sub = this.svc.stream().subscribe(() => {}); }\n"
        "  /** Unsubscribe on destroy. */\n"
        "  ngOnDestroy(): void { this.sub?.unsubscribe(); }\n"
        "}\n",
        encoding="utf-8",
    )
    svc_ng = tmp_path / "orders.service.ts"
    svc_ng.write_text(
        "import { Injectable } from '@angular/core';\n"
        "import { HttpClient } from '@angular/common/http';\n"
        "/** Service layer permitted to inject HttpClient. */\n"
        "@Injectable({ providedIn: 'root' })\n"
        "export class OrdersService {\n"
        "  constructor(private readonly http: HttpClient) {}\n"
        "  /** Fetch orders from API. */\n"
        "  list(): unknown { return this.http.get('/api/orders'); }\n"
        "}\n",
        encoding="utf-8",
    )

    analyzer = ModuleAnalyzer(tmp_path, set(), RubricConfig(), None)
    rep_bad = analyzer.analyze(bad_ng)
    cls_bad = rep_bad.classes[0]
    assert any("HttpClient" in f and "SRP" in f for f in cls_bad.findings)
    assert any("subscribe" in f.lower() and "Clean" in f for f in cls_bad.findings)
    assert rep_bad.scores.security <= 65.0
    assert rep_bad.scores.composite < 80.0

    rep_inj = analyzer.analyze(bad_inject_ng)
    assert any("HttpClient" in f for f in rep_inj.classes[0].findings)

    rep_clean = analyzer.analyze(clean_ng)
    cls_clean = rep_clean.classes[0]
    assert rep_clean.scores.grade == "A"
    assert not any("LCOM4" in f for f in cls_clean.findings)
    assert not any("missing public docstring" in f for f in cls_clean.methods[0].findings)
    assert not any("subscribe" in f.lower() for f in cls_clean.findings)

    rep_destroy = analyzer.analyze(destroy_ng)
    assert rep_destroy.scores.grade == "A"
    assert not any("subscribe" in f.lower() for f in rep_destroy.classes[0].findings)

    rep_svc = analyzer.analyze(svc_ng)
    assert rep_svc.scores.grade == "A"
    assert not any("HttpClient" in f for f in rep_svc.classes[0].findings)

    # Confirm Angular never activates on .js / .jsx files under auto mode (even with Angular package.json)
    ng_repo = tmp_path / "ng_app"
    ng_repo.mkdir()
    (ng_repo / "package.json").write_text('{"dependencies": {"@angular/core": "^18.0.0"}}', encoding="utf-8")
    plain_jsx = ng_repo / "plain.jsx"
    plain_jsx.write_text("export function Plain() { return 1; }\n", encoding="utf-8")
    p_js = resolve_active_profiles(ng_repo, plain_jsx, imports=["@angular/core"], has_jsx=False)
    assert all(fw.name != "angular" for fw in p_js.frameworks)


def test_multiline_decorators_preserve_preceding_jsdoc(tmp_path: Path) -> None:
    """JSDoc placed immediately above multi-line class or method decorators must still count as a docstring."""
    from _code_health.models import RubricConfig
    from _code_health.module_engine import ModuleAnalyzer

    comp = tmp_path / "decorated.component.ts"
    comp.write_text(
        "import { Component, HostListener } from '@angular/core';\n"
        "/** Multi-line decorated Angular component. */\n"
        "@Component({\n"
        "  selector: 'app-decorated',\n"
        "  standalone: true,\n"
        "  templateUrl: './decorated.component.html',\n"
        "  styleUrls: ['./decorated.component.scss'],\n"
        "})\n"
        "export class DecoratedComponent {\n"
        "  /** Handle global escape key cleanly. */\n"
        "  @HostListener('window:keydown.escape', [\n"
        "    '$event',\n"
        "  ])\n"
        "  onEscape(event: KeyboardEvent): string {\n"
        "    return event.key;\n"
        "  }\n"
        "}\n",
        encoding="utf-8",
    )
    undoc = tmp_path / "undocumented.component.ts"
    undoc.write_text(
        "import { Component } from '@angular/core';\n"
        "/** Unrelated header note. */\n"
        "const TAG_A = 'v1';\n"
        "const TAG_B = 'v2';\n"
        "const TAG_C = 'v3';\n"
        "@Component({\n"
        "  selector: 'app-undoc',\n"
        "  template: '<p></p>',\n"
        "})\n"
        "export class UndocComponent {\n"
        "  ping(): string { return TAG_A + TAG_B + TAG_C; }\n"
        "}\n",
        encoding="utf-8",
    )

    analyzer = ModuleAnalyzer(tmp_path, set(), RubricConfig(), None)
    rep_ok = analyzer.analyze(comp)
    assert len(rep_ok.classes) == 1
    assert not any("missing class docstring" in f for f in rep_ok.classes[0].findings)
    assert not any("missing public docstring" in f for f in rep_ok.classes[0].methods[0].findings)
    assert rep_ok.scores.grade == "A"

    rep_missing = analyzer.analyze(undoc)
    assert any("missing class docstring" in f for f in rep_missing.classes[0].findings)


def test_resolve_active_profiles_auto_string_matches_none_override(tmp_path: Path) -> None:
    """Passing framework_override='auto' via API must behave identically to None for UI detection."""
    from _code_health.profiles import resolve_active_profiles

    react_file = tmp_path / "Card.tsx"
    next_file = tmp_path / "app" / "page.tsx"
    ng_file = tmp_path / "card.component.ts"

    p_react_none = resolve_active_profiles(tmp_path, react_file, framework_override=None, imports=["react"], has_jsx=True)
    p_react_auto = resolve_active_profiles(tmp_path, react_file, framework_override="auto", imports=["react"], has_jsx=True)
    assert [f.name for f in p_react_auto.frameworks] == [f.name for f in p_react_none.frameworks] == ["react"]

    p_next_auto = resolve_active_profiles(tmp_path, next_file, framework_override="auto", imports=["next/link"], has_jsx=True)
    assert [f.name for f in p_next_auto.frameworks] == ["nextjs"]

    p_ng_auto = resolve_active_profiles(tmp_path, ng_file, framework_override="auto", imports=["@angular/core"])
    assert [f.name for f in p_ng_auto.frameworks] == ["angular"]

    p_disabled = resolve_active_profiles(tmp_path, react_file, framework_override="none", imports=["react"], has_jsx=True)
    assert p_disabled.frameworks == []




