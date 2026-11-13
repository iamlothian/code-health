"""Tree-Sitter Concrete Syntax Tree (CST) parser for TypeScript and TSX source files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from _code_health.ecmascript_ui import (
    BRANCH_LOOP_NODES,
    collect_ui_cst_telemetry,
    count_effective_loc,
    extract_decorators,
    extract_directives,
    extract_field_type_or_init,
    extract_jsdoc_params,
    find_first_child,
    get_node_text,
    has_doc_comment,
    unwrap_wrapper_callable,
)
from _code_health.ir_models import (
    IRAnnotation,
    IRCall,
    IRClass,
    IRExceptHandler,
    IRField,
    IRFunction,
    IRModule,
    IRParam,
    MissingNativeParserError,
)
from _code_health.js_parser import _calc_js_lcom4, _collect_this_assignments
from _code_health.ts_smells import _TSSmells, collect_syntax_errors, count_unclaimed_ts_ignores

_LOOP_CF_TYPES = frozenset({"for_statement", "for_in_statement", "for_of_statement", "while_statement", "do_statement", "if_statement"})
_NESTED_CF_TYPES = _LOOP_CF_TYPES | frozenset({"switch_statement", "try_statement", "catch_clause", "with_statement"})
_TS_TEST_CALLS = frozenset({"it", "test", "it.only", "it.skip", "it.concurrent", "test.only", "test.skip", "test.concurrent", "fit", "xit"})
_TS_SUITE_CALLS = frozenset({"describe", "describe.only", "describe.skip", "context", "suite", "fdescribe", "xdescribe"})
_EXPORTED_UNIT_TYPES = frozenset({"class_declaration", "abstract_class_declaration", "function_declaration", "generator_function_declaration", "lexical_declaration", "variable_declaration"})


def check_typescript_dependencies() -> tuple[Any, Any]:
    """Verify tree-sitter and tree-sitter-typescript are available or raise MissingNativeParserError."""
    try:
        import tree_sitter
        import tree_sitter_typescript
        return tree_sitter, tree_sitter_typescript
    except ImportError as exc:
        raise MissingNativeParserError("typescript", ["tree-sitter", "tree-sitter-typescript"]) from exc


def _record_ts_call(visitor: _TSVisitor, node: Any, in_branch: bool) -> None:
    """Record call expression target, query concat flag, and setPrototypeOf mutation."""
    c_name = get_node_text(node.children[0], visitor.bytes) if node.children else ""
    args = find_first_child(node, "arguments")
    first = next((c for c in args.children if c.type not in {"(", ")", ","}), None) if args else None
    has_concat = bool(first and visitor.smells.is_unsafe_query_arg(first))
    has_str = bool(first and (first.type in {"string", "template_string"} or has_concat))
    visitor.calls.append(IRCall(c_name, c_name, node.start_point[0] + 1, has_concat, has_str, in_branch))
    if c_name.endswith(".setPrototypeOf") or c_name == "setPrototypeOf":
        visitor.smells.has_proto = True


def _dispatch_ts_expr(visitor: _TSVisitor, node: Any, in_branch: bool) -> None:
    """Inspect expression CST node for smells, calls, dynamic Function, and this fields."""
    t = node.type
    visitor.smells.scan_node(node, visitor.bytes)
    if t == "binary_expression":
        visitor.stats[0] += sum(c.type in {"&&", "||", "??"} for c in node.children)
    elif t == "call_expression" and node.children:
        _record_ts_call(visitor, node, in_branch)
    elif t == "new_expression":
        con = find_first_child(node, "identifier")
        if con and get_node_text(con, visitor.bytes) == "Function":
            visitor.calls.append(IRCall("new Function", "Function", node.start_point[0] + 1, in_branch_or_loop=in_branch))
    elif t == "member_expression" and any(c.type == "this" for c in node.children):
        prop = find_first_child(node, "property_identifier")
        if prop:
            visitor.accessed_fields.add(get_node_text(prop, visitor.bytes))


class _TSVisitor:
    """Computes complexity, nesting, calls, and smells for a TypeScript function or method."""

    def __init__(self, source_bytes: bytes, class_fields: set[str] | None = None) -> None:
        """Initialize visitor with source bytes and optional class field names."""
        self.bytes = source_bytes
        self.fields = class_fields or set()
        self.stats = [1, 0, 0, 0]  # [cc, cog, max_nesting, returns]
        self.calls: list[IRCall] = []
        self.accessed_fields: set[str] = set()
        self.except_handlers: list[IRExceptHandler] = []
        self.smells = _TSSmells()

    def scan(self, body_node: Any, depth: int = 0, in_branch: bool = False) -> None:
        """Scan AST recursively updating complexity and collecting smells."""
        if not body_node:
            return
        for child in body_node.children:
            self._dispatch_node(child, depth, in_branch)

    def _bump_branch(self, cc_delta: int, depth: int) -> None:
        self.stats[0] += cc_delta
        self.stats[1] += 1 + depth
        self.stats[2] = max(self.stats[2], depth + 1)

    def _dispatch_node(self, node: Any, depth: int, in_branch: bool) -> None:
        t = node.type
        if t in _LOOP_CF_TYPES or t == "ternary_expression":
            self._bump_branch(1, depth)
        elif t == "return_statement":
            self.stats[3] += 1
        elif t == "switch_statement":
            body = find_first_child(node, "switch_body") or node
            self._bump_branch(max(1, sum(c.type == "switch_case" for c in body.children)), depth)
        elif t == "try_statement":
            self._visit_try(node, depth)
        else:
            _dispatch_ts_expr(self, node, in_branch)
        self.scan(node, depth + 1 if t in _NESTED_CF_TYPES else depth, in_branch or t in BRANCH_LOOP_NODES)

    def _visit_try(self, node: Any, depth: int) -> None:
        catch = find_first_child(node, "catch_clause")
        if not catch:
            return
        self._bump_branch(1, depth)
        param = find_first_child(catch, "identifier")
        block = find_first_child(catch, "statement_block")
        stmts = [c for c in block.children if c.type not in {"{", "}", "comment"}] if block else []
        self.except_handlers.append(IRExceptHandler(get_node_text(param, self.bytes) if param else None, len(stmts) == 0, True, catch.start_point[0] + 1))


@dataclass(frozen=True)
class _TSCtx:
    """Shared module parsing state passed cleanly across CST unit extractors."""

    bytes: bytes
    lines: list[str]
    is_test: bool
    claimed: set[int]


@dataclass(frozen=True)
class _TSFuncSpec:
    """Specification metadata for constructing an IRFunction."""

    name: str
    qualname: str
    is_test: bool
    fields: set[str] | None = None
    claimed_lines: set[int] | None = None
    modifiers: tuple[str, ...] = ()
    var_type_node: Any = None
    doc_node: Any = None
    annotations: tuple[IRAnnotation, ...] = ()


def _parse_ts_param(c: Any, source_bytes: bytes, jsdoc: dict[str, str]) -> IRParam | None:
    """Extract a single IRParam from a parameter CST node."""
    if c.type in {"(", ")", ","}:
        return None
    id_node = find_first_child(c, "identifier") or (c if c.type == "identifier" else None)
    nm = get_node_text(id_node, source_bytes) if id_node else "arg"
    type_node = find_first_child(c, "type_annotation")
    d_type = get_node_text(type_node, source_bytes).strip(": ") if type_node else jsdoc.get(nm)
    has_assign = any(ch.type == "=" for ch in c.children)
    is_opt = c.type == "optional_parameter"
    is_bool_lit = has_assign and any(ch.type in {"true", "false"} for ch in c.children)
    eff_type = "bool" if (d_type in {"boolean", "bool"} or is_bool_lit) else ("inferred" if (not d_type and (has_assign or is_opt)) else d_type)
    return IRParam(nm, eff_type, has_assign, extract_decorators(c, source_bytes))


def _extract_ts_params(fn_node: Any, source_bytes: bytes, jsdoc: dict[str, str], has_var_type: bool = False) -> list[IRParam]:
    """Extract formal parameters and types from function or arrow definition."""
    p_list = find_first_child(fn_node, "formal_parameters")
    if p_list:
        params = [p for c in p_list.children if (p := _parse_ts_param(c, source_bytes, jsdoc)) is not None]
    elif fn_node.type == "arrow_function":
        param_id = next((c for c in fn_node.children if c.type in {"identifier", "=>"}), None)
        nm = get_node_text(param_id, source_bytes) if param_id and param_id.type == "identifier" else ""
        params = [IRParam(nm, jsdoc.get(nm), False)] if nm else []
    else:
        params = []
    if has_var_type:
        return [IRParam(p.name, p.type_annotation or "inferred", p.has_default, p.annotations) for p in params]
    return params


def _extract_ts_return_type(fn_node: Any, source_bytes: bytes) -> str | None:
    """Extract return type annotation from function or method definition."""
    if fn_node.type == "method_definition":
        prop = find_first_child(fn_node, "property_identifier")
        if (prop and get_node_text(prop, source_bytes) == "constructor") or any(c.type == "set" for c in fn_node.children):
            return "void"
    ret = fn_node.child_by_field_name("return_type") or find_first_child(fn_node, "type_annotation")
    return get_node_text(ret, source_bytes).strip(": ") if ret else None


def _build_ts_ir_function(spec: _TSFuncSpec, node: Any, body: Any, ctx: _TSCtx) -> IRFunction:
    """Construct a complete IRFunction from TypeScript syntax node."""
    v = _TSVisitor(ctx.bytes, spec.fields)
    if spec.var_type_node is not None:
        v.smells.walk_escapes(spec.var_type_node, ctx.bytes)
    target = body or node
    v.smells.scan_header(spec.doc_node or node, body, ctx.bytes, ctx.lines)
    v.scan(target, 0, False)
    jsx_cnt, sinks, idx_keys = collect_ui_cst_telemetry(target, ctx.bytes)
    if spec.claimed_lines is not None:
        spec.claimed_lines.update(v.smells.types.ignore_lines)
    ret_type = _extract_ts_return_type(node, ctx.bytes)
    if ret_type is None and spec.var_type_node is not None:
        ret_type = get_node_text(spec.var_type_node, ctx.bytes).strip(": ")
    return IRFunction(
        name=spec.name,
        qualname=spec.qualname,
        lineno=node.start_point[0] + 1,
        end_lineno=node.end_point[0] + 1,
        loc=count_effective_loc(node, ctx.lines),
        params=_extract_ts_params(node, ctx.bytes, extract_jsdoc_params(spec.doc_node or node, ctx.lines), spec.var_type_node is not None),
        return_type=ret_type,
        max_nesting=v.stats[2],
        cyclomatic_complexity=v.stats[0],
        cognitive_complexity=v.stats[1],
        returns_count=v.stats[3],
        calls=v.calls,
        accessed_fields=list(v.accessed_fields),
        except_handlers=v.except_handlers,
        is_test=spec.is_test,
        annotations=list(spec.annotations),
        modifiers=list(spec.modifiers),
        has_docstring=has_doc_comment(spec.doc_node or node, ctx.lines),
        var_declarations_count=v.smells.var_count,
        loose_comparisons_count=v.smells.loose_eq,
        has_proto_mutation=v.smells.has_proto,
        has_with_statement=v.smells.has_with,
        has_debugger_statement=v.smells.has_debugger,
        explicit_any_count=v.smells.types.any_count,
        ts_ignore_count=v.smells.types.ts_ignore_count,
        non_null_assertion_count=v.smells.types.non_null_count,
        jsx_elements_count=jsx_cnt,
        dom_write_sinks=sinks,
        array_index_keys=idx_keys,
    )


def _extract_param_properties(ctor_node: Any, bytes_: bytes) -> list[IRField]:
    """Extract constructor parameter properties (public, private, protected, readonly)."""
    p_list = find_first_child(ctor_node, "formal_parameters")
    if not p_list:
        return []
    fields: list[IRField] = []
    for p in p_list.children:
        if any(ch.type in {"accessibility_modifier", "readonly"} for ch in p.children):
            id_node = find_first_child(p, "identifier")
            if id_node:
                ta = find_first_child(p, "type_annotation")
                f_type = get_node_text(ta, bytes_).strip(": ") if ta else None
                fields.append(IRField(get_node_text(id_node, bytes_), f_type, extract_decorators(p, bytes_), p.start_point[0] + 1))
    return fields


class TSClassExtractor:
    """Extracts methods, fields (including parameter properties), and LCOM4 for a TypeScript class."""

    def __init__(self, class_node: Any, source_bytes: bytes, lines: list[str]) -> None:
        """Initialize class extractor with CST node and source text."""
        self.node, self.bytes, self.lines = class_node, source_bytes, lines
        id_node = find_first_child(self.node, "type_identifier") or find_first_child(self.node, "identifier")
        self.name = get_node_text(id_node, self.bytes) if id_node else "AnonymousClass"
        self.fields = self._collect_fields()
        self.field_names = {f.name for f in self.fields}

    def _collect_fields(self) -> list[IRField]:
        body = find_first_child(self.node, "class_body") or self.node
        fields: dict[str, IRField] = {}
        for child in body.children:
            prop = find_first_child(child, "property_identifier")
            name = get_node_text(prop, self.bytes) if prop else ""
            if child.type in {"field_definition", "public_field_definition", "property_definition"} and name:
                fields[name] = IRField(name, extract_field_type_or_init(child, self.bytes), extract_decorators(child, self.bytes), child.start_point[0] + 1)
            elif child.type == "method_definition" and name == "constructor":
                for f in _extract_param_properties(child, self.bytes) + _collect_this_assignments(child, self.bytes):
                    fields[f.name] = f
        return list(fields.values())

    def extract_methods(self, is_test: bool, claimed: set[int] | None = None) -> tuple[list[IRFunction], int]:
        """Extract concrete and abstract methods and calculate LCOM4 cohesion."""
        body = find_first_child(self.node, "class_body") or self.node
        ctx = _TSCtx(self.bytes, self.lines, is_test, claimed if claimed is not None else set())
        methods: list[IRFunction] = []
        for m in body.children:
            if m.type in {"method_definition", "abstract_method_signature"}:
                prop = find_first_child(m, "property_identifier")
                m_name = get_node_text(prop, self.bytes) if prop else "<method>"
                is_abs = m.type == "abstract_method_signature"
                mods = ("abstract",) if is_abs else ()
                decs = tuple(extract_decorators(m, self.bytes))
                spec = _TSFuncSpec(m_name, f"{self.name}.{m_name}", is_test, self.field_names, claimed, mods, annotations=decs)
                fn_body = None if is_abs else find_first_child(m, "statement_block")
                methods.append(_build_ts_ir_function(spec, m, fn_body, ctx))
        return methods, _calc_js_lcom4([m for m in methods if "abstract" not in m.modifiers], is_test)


def _extract_ts_test_fn(call: Any, args: list[Any], ctx: _TSCtx) -> IRFunction | None:
    cb = next((a for a in args[1:] if a.type in {"arrow_function", "function_expression"}), None)
    if not cb:
        return None
    has_desc = bool(args and args[0].type in {"string", "template_string"})
    desc = get_node_text(args[0], ctx.bytes).strip("\"'`") if has_desc else ""
    nm = f"test: {desc}" if desc else f"test: line {call.start_point[0] + 1}"
    body = find_first_child(cb, "statement_block") or cb
    return _build_ts_ir_function(_TSFuncSpec(nm, nm, True, None, ctx.claimed), cb, body, ctx)


def _process_ts_test_call(call: Any, funcs: list[IRFunction], ctx: _TSCtx) -> None:
    """Process Jest/Vitest/Mocha BDD test and suite blocks recursively."""
    name = get_node_text(call.children[0], ctx.bytes) if call.children else ""
    args_node = find_first_child(call, "arguments")
    args = [c for c in args_node.children if c.type not in {"(", ")", ","}] if args_node else []
    if name in _TS_TEST_CALLS and (fn := _extract_ts_test_fn(call, args, ctx)):
        funcs.append(fn)
    elif name in _TS_SUITE_CALLS:
        cb = next((a for a in args if a.type in {"arrow_function", "function_expression"}), None)
        body = find_first_child(cb, "statement_block") if cb else None
        for s in [c for c in body.children if c.type == "expression_statement"] if body else []:
            if nested := find_first_child(s, "call_expression"):
                _process_ts_test_call(nested, funcs, ctx)


def _extract_ts_prop_func(prop_node: Any, obj_name: str, ctx: _TSCtx) -> IRFunction | None:
    prop = find_first_child(prop_node, "property_identifier")
    val = prop_node if prop_node.type == "method_definition" else (find_first_child(prop_node, "arrow_function") or find_first_child(prop_node, "function_expression"))
    if not prop or not val:
        return None
    pn = get_node_text(prop, ctx.bytes)
    spec = _TSFuncSpec(pn, f"{obj_name}.{pn}", ctx.is_test, None, ctx.claimed, doc_node=prop_node)
    return _build_ts_ir_function(spec, val, find_first_child(val, "statement_block") or val, ctx)


def _extract_ts_var_funcs(decl: Any, ctx: _TSCtx) -> list[IRFunction]:
    """Extract arrow/function variables, wrapped HOC callables, and object literal methods."""
    id_n = find_first_child(decl, "identifier")
    if not id_n:
        return []
    v_name = get_node_text(id_n, ctx.bytes)
    val = unwrap_wrapper_callable(decl, ctx.bytes)
    if val:
        var_type = find_first_child(decl, "type_annotation")
        spec = _TSFuncSpec(v_name, v_name, ctx.is_test, None, ctx.claimed, var_type_node=var_type, doc_node=decl)
        return [_build_ts_ir_function(spec, val, find_first_child(val, "statement_block") or val, ctx)]
    val_root = find_first_child(decl, "as_expression") or find_first_child(decl, "satisfies_expression") or decl
    obj = find_first_child(val_root, "object")
    return [f for c in obj.children if (f := _extract_ts_prop_func(c, v_name, ctx)) is not None] if obj else []


def _extract_ts_units(root: Any, ctx: _TSCtx) -> tuple[list[IRClass], list[IRFunction], list[str], int]:
    """Traverse CST root and extract classes, functions, imports, and unclaimed ignores."""
    classes, functions, imports = [], [], []

    def dispatch(node: Any) -> None:
        t = node.type
        if t == "import_statement" and (src := find_first_child(node, "string")):
            imports.append(get_node_text(src, ctx.bytes).strip("\"'`"))
        elif t == "export_statement":
            for c in [ch for ch in node.children if ch.type in _EXPORTED_UNIT_TYPES]:
                dispatch(c)
        elif t in {"class_declaration", "abstract_class_declaration"}:
            ext = TSClassExtractor(node, ctx.bytes, ctx.lines)
            methods, lcom4 = ext.extract_methods(ctx.is_test, ctx.claimed)
            cls_decs = extract_decorators(node, ctx.bytes)
            classes.append(IRClass(ext.name, ext.name, node.start_point[0] + 1, node.end_point[0] + 1, count_effective_loc(node, ctx.lines), cls_decs, [], ext.fields, methods, lcom4, has_doc_comment(node, ctx.lines)))
        elif t in {"function_declaration", "generator_function_declaration"}:
            n = find_first_child(node, "identifier")
            f_name = get_node_text(n, ctx.bytes) if n else "anonymous"
            decs = tuple(extract_decorators(node, ctx.bytes))
            functions.append(_build_ts_ir_function(_TSFuncSpec(f_name, f_name, ctx.is_test, None, ctx.claimed, annotations=decs), node, find_first_child(node, "statement_block"), ctx))
        elif t in {"lexical_declaration", "variable_declaration"}:
            for d in [c for c in node.children if c.type == "variable_declarator"]:
                functions.extend(_extract_ts_var_funcs(d, ctx))
        elif t == "expression_statement" and (call := find_first_child(node, "call_expression")):
            _process_ts_test_call(call, functions, ctx)

    for child in root.children:
        dispatch(child)
    return classes, functions, imports, count_unclaimed_ts_ignores(root, ctx.bytes, ctx.claimed)


def parse_typescript_file(file_path: Path, rel_path: str, is_test: bool) -> IRModule:
    """Parse a TypeScript or TSX file into an IRModule using Tree-Sitter."""
    tree_sitter, tree_sitter_typescript = check_typescript_dependencies()
    source_bytes = file_path.read_bytes()
    lines = source_bytes.decode("utf-8", errors="replace").splitlines()
    lang_fn = tree_sitter_typescript.language_tsx if file_path.suffix.lower() == ".tsx" else tree_sitter_typescript.language_typescript
    tree = tree_sitter.Parser(tree_sitter.Language(lang_fn())).parse(source_bytes)
    ctx = _TSCtx(source_bytes, lines, is_test, set())
    classes, functions, imports, mod_ignores = _extract_ts_units(tree.root_node, ctx)
    directives = extract_directives(tree.root_node, source_bytes)
    loc = max(sum(c.loc for c in classes) + sum(f.loc for f in functions), count_effective_loc(tree.root_node, lines))
    return IRModule(rel_path, "typescript", is_test, loc, imports, classes, functions, "native", has_doc_comment(tree.root_node, lines), ts_ignore_count=mod_ignores, syntax_errors=collect_syntax_errors(tree.root_node), directives=directives)
