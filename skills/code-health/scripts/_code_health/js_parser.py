"""Tree-Sitter Concrete Syntax Tree (CST) parser for Vanilla JavaScript source files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from _code_health.ast_engine import _bfs_component_count
from _code_health.ecmascript_ui import (
    BRANCH_LOOP_NODES,
    collect_ui_cst_telemetry,
    count_effective_loc,
    extract_directives,
    extract_jsdoc_params,
    find_first_child,
    get_node_text,
    has_doc_comment,
    unwrap_wrapper_callable,
)
from _code_health.ir_models import (
    IRCall,
    IRClass,
    IRExceptHandler,
    IRField,
    IRFunction,
    IRModule,
    IRParam,
    MissingNativeParserError,
)


def check_javascript_dependencies() -> tuple[Any, Any]:
    """Verify tree-sitter and tree-sitter-javascript are available or raise MissingNativeParserError."""
    try:
        import tree_sitter
        import tree_sitter_javascript
        return tree_sitter, tree_sitter_javascript
    except ImportError as exc:
        raise MissingNativeParserError("javascript", ["tree-sitter", "tree-sitter-javascript"]) from exc


def _extract_js_params(fn_node: Any, source_bytes: bytes, jsdoc: dict[str, str]) -> list[IRParam]:
    p_list = find_first_child(fn_node, "formal_parameters")
    if not p_list:
        first = fn_node.children[0] if fn_node.children else None
        if fn_node.type == "arrow_function" and first and first.type == "identifier":
            nm = get_node_text(first, source_bytes)
            return [IRParam(nm, jsdoc.get(nm), False)]
        return []
    params: list[IRParam] = []
    for c in p_list.children:
        t = c.type
        if t == "identifier":
            nm = get_node_text(c, source_bytes)
            params.append(IRParam(nm, jsdoc.get(nm), False))
        elif t == "assignment_pattern":
            left = find_first_child(c, "identifier")
            nm = get_node_text(left, source_bytes) if left else "arg"
            params.append(IRParam(nm, jsdoc.get(nm), True))
        elif t in {"rest_pattern", "object_pattern", "array_pattern"}:
            params.append(IRParam(get_node_text(c, source_bytes).strip(), None, False))
    return params


@dataclass
class _JSSmells:
    var_count: int = 0
    loose_eq: int = 0
    has_proto: bool = False
    has_with: bool = False
    has_debugger: bool = False

    def scan_node(self, node: Any, bytes_: bytes) -> None:
        """Scan AST node for var, debugger, with, loose equality, and proto mutations."""
        t = node.type
        if t == "debugger_statement":
            self.has_debugger = True
        elif t == "with_statement":
            self.has_with = True
        elif t == "variable_declaration":
            self.var_count += sum(c.type == "variable_declarator" for c in node.children)
        elif t == "binary_expression":
            self.loose_eq += sum(c.type in {"==", "!="} for c in node.children)
        elif t == "assignment_expression" and node.children:
            txt = get_node_text(node.children[0], bytes_)
            if txt == "__proto__" or txt.endswith(".__proto__"):
                self.has_proto = True


class _JSVisitor:
    """Computes complexity, nesting, calls, and smells for a JavaScript function or method."""

    def __init__(self, source_bytes: bytes, class_fields: set[str] | None = None) -> None:
        self.bytes = source_bytes
        self.fields = class_fields or set()
        self.stats = [1, 0, 0, 0]  # [cc, cog, max_nesting, returns]
        self.calls: list[IRCall] = []
        self.accessed_fields: set[str] = set()
        self.except_handlers: list[IRExceptHandler] = []
        self.smells = _JSSmells()

    def scan(self, body_node: Any, depth: int = 0, in_branch: bool = False) -> None:
        """Scan function body block recursively."""
        if not body_node:
            return
        for child in body_node.children:
            self._dispatch_node(child, depth, in_branch)

    def _dispatch_node(self, node: Any, depth: int, in_branch: bool) -> None:
        t = node.type
        loop_types = {"for_statement", "for_in_statement", "for_of_statement", "while_statement", "do_statement", "if_statement"}
        if t in loop_types or t == "ternary_expression":
            self.stats[0] += 1
            self.stats[1] += 1 + depth
            self.stats[2] = max(self.stats[2], depth + 1)
        elif t == "return_statement":
            self.stats[3] += 1
        elif t == "switch_statement":
            self._visit_switch(node, depth)
        elif t == "try_statement":
            self._visit_try(node, depth)
        else:
            self._dispatch_expressions(node, in_branch)

        next_d = depth + 1 if t in {"if_statement", "for_statement", "for_in_statement", "for_of_statement", "while_statement", "do_statement", "switch_statement", "try_statement", "catch_clause", "with_statement"} else depth
        self.scan(node, next_d, in_branch or t in BRANCH_LOOP_NODES)

    def _record_call(self, node: Any, in_branch: bool) -> None:
        c_name = get_node_text(node.children[0], self.bytes)
        args = find_first_child(node, "arguments")
        first = next((c for c in args.children if c.type not in {"(", ")", ","}), None) if args else None
        is_str = bool(first and first.type in {"string", "template_string"})
        self.calls.append(IRCall(c_name, c_name, node.start_point[0] + 1, False, is_str, in_branch))
        if c_name.endswith(".setPrototypeOf"):
            self.smells.has_proto = True

    def _dispatch_expressions(self, node: Any, in_branch: bool) -> None:
        t = node.type
        self.smells.scan_node(node, self.bytes)
        if t == "binary_expression":
            self.stats[0] += sum(c.type in {"&&", "||", "??"} for c in node.children)
        elif t == "call_expression" and node.children:
            self._record_call(node, in_branch)
        elif t == "new_expression":
            con = find_first_child(node, "identifier")
            if con and get_node_text(con, self.bytes) == "Function":
                self.calls.append(IRCall("new Function", "Function", node.start_point[0] + 1, in_branch_or_loop=in_branch))
        elif t == "member_expression" and any(c.type == "this" for c in node.children):
            prop = find_first_child(node, "property_identifier")
            if prop:
                self.accessed_fields.add(get_node_text(prop, self.bytes))

    def _visit_switch(self, node: Any, depth: int) -> None:
        body = find_first_child(node, "switch_body") or node
        cases = [c for c in body.children if c.type == "switch_case"]
        self.stats[0] += max(1, len(cases))
        self.stats[1] += 1 + depth
        self.stats[2] = max(self.stats[2], depth + 1)

    def _visit_try(self, node: Any, depth: int) -> None:
        catch = find_first_child(node, "catch_clause")
        if not catch:
            return
        self.stats[0] += 1
        self.stats[1] += 1 + depth
        self.stats[2] = max(self.stats[2], depth + 1)
        param = find_first_child(catch, "identifier")
        p_text = get_node_text(param, self.bytes) if param else None
        block = find_first_child(catch, "statement_block")
        stmts = [c for c in block.children if c.type not in {"{", "}", "comment"}] if block else []
        self.except_handlers.append(IRExceptHandler(p_text, len(stmts) == 0, True, catch.start_point[0] + 1))


@dataclass(frozen=True)
class _FuncSpec:
    name: str
    qualname: str
    is_test: bool
    fields: set[str] | None = None
    doc_node: Any = None


def _build_ir_function(
    spec: _FuncSpec, node: Any, body: Any, source_bytes: bytes, lines: list[str]
) -> IRFunction:
    v = _JSVisitor(source_bytes, spec.fields)
    target = body or node
    v.scan(target, 0, False)
    jsx_cnt, sinks, idx_keys = collect_ui_cst_telemetry(target, source_bytes)
    doc_src = spec.doc_node or node
    return IRFunction(
        name=spec.name,
        qualname=spec.qualname,
        lineno=node.start_point[0] + 1,
        end_lineno=node.end_point[0] + 1,
        loc=count_effective_loc(node, lines),
        params=_extract_js_params(node, source_bytes, extract_jsdoc_params(doc_src, lines)),
        return_type=None,
        max_nesting=v.stats[2],
        cyclomatic_complexity=v.stats[0],
        cognitive_complexity=v.stats[1],
        returns_count=v.stats[3],
        calls=v.calls,
        accessed_fields=list(v.accessed_fields),
        except_handlers=v.except_handlers,
        is_test=spec.is_test,
        has_docstring=has_doc_comment(doc_src, lines),
        var_declarations_count=v.smells.var_count,
        loose_comparisons_count=v.smells.loose_eq,
        has_proto_mutation=v.smells.has_proto,
        has_with_statement=v.smells.has_with,
        has_debugger_statement=v.smells.has_debugger,
        jsx_elements_count=jsx_cnt,
        dom_write_sinks=sinks,
        array_index_keys=idx_keys,
    )


def _calc_js_lcom4(methods: list[IRFunction], is_test: bool) -> int:
    all_n = {m.name for m in methods}
    toks = {
        m.name: {f"a:{a}" for a in m.accessed_fields} | {f"m:{c}" for c in {c.name.split(".")[-1] for c in m.calls} & all_n} | {f"m:{m.name}"}
        for m in methods if m.name != "constructor"
    }
    if is_test or len(toks) <= 2:
        return 1
    names = list(toks)
    adj: dict[str, set[str]] = {n: set() for n in names}
    for i, n1 in enumerate(names):
        for n2 in names[i + 1 :]:
            if toks[n1] & toks[n2]:
                adj[n1].add(n2)
                adj[n2].add(n1)
    return _bfs_component_count(names, adj)


def _collect_this_assignments(ctor_node: Any, source_bytes: bytes) -> list[IRField]:
    """Extract this.field assignments inside a constructor body."""
    block = find_first_child(ctor_node, "statement_block")
    if not block:
        return []
    fields: list[IRField] = []
    for s in [c for c in block.children if c.type == "expression_statement"]:
        asn = find_first_child(s, "assignment_expression")
        left = asn.children[0] if asn and asn.children else None
        if left and left.type == "member_expression" and len(left.children) >= 3 and get_node_text(left.children[0], source_bytes) == "this":
            fields.append(IRField(get_node_text(left.children[2], source_bytes), None, [], s.start_point[0] + 1))
    return fields


class JSClassExtractor:
    """Extracts methods, fields, and LCOM4 for a JavaScript class."""

    def __init__(self, class_node: Any, source_bytes: bytes, lines: list[str]) -> None:
        self.node = class_node
        self.bytes = source_bytes
        self.lines = lines
        id_node = find_first_child(self.node, "identifier")
        self.name = get_node_text(id_node, self.bytes) if id_node else "AnonymousClass"
        self.fields = self._collect_fields()
        self.field_names = {f.name for f in self.fields}

    def _collect_fields(self) -> list[IRField]:
        body = find_first_child(self.node, "class_body") or self.node
        fields: dict[str, IRField] = {}
        for child in body.children:
            prop = find_first_child(child, "property_identifier")
            name = get_node_text(prop, self.bytes) if prop else ""
            if child.type in {"field_definition", "public_field_definition"} and name:
                fields[name] = IRField(name, None, [], child.start_point[0] + 1)
            elif child.type == "method_definition" and name == "constructor":
                for f in _collect_this_assignments(child, self.bytes):
                    fields[f.name] = f
        return list(fields.values())

    def extract_methods(self, is_test: bool) -> tuple[list[IRFunction], int]:
        """Extract all methods and calculate LCOM4 cohesion score."""
        body = find_first_child(self.node, "class_body") or self.node
        methods: list[IRFunction] = []
        for m in body.children:
            if m.type == "method_definition":
                prop = find_first_child(m, "property_identifier")
                m_name = get_node_text(prop, self.bytes) if prop else "<method>"
                spec = _FuncSpec(m_name, f"{self.name}.{m_name}", is_test, self.field_names)
                methods.append(_build_ir_function(spec, m, find_first_child(m, "statement_block"), self.bytes, self.lines))
        return methods, _calc_js_lcom4(methods, is_test)


def _extract_test_func(call: Any, args: list[Any], bytes_: bytes, lines: list[str]) -> IRFunction | None:
    cb = next((a for a in args[1:] if a.type in {"arrow_function", "function_expression"}), None)
    if not cb:
        return None
    desc = get_node_text(args[0], bytes_).strip("\"'`") if args and args[0].type in {"string", "template_string"} else ""
    nm = f"test: {desc}" if desc else f"test: line {call.start_point[0] + 1}"
    return _build_ir_function(_FuncSpec(nm, nm, True), cb, find_first_child(cb, "statement_block") or cb, bytes_, lines)


def _process_test_call(call: Any, funcs: list[IRFunction], bytes_: bytes, lines: list[str]) -> None:
    name = get_node_text(call.children[0], bytes_) if call.children else ""
    args_node = find_first_child(call, "arguments")
    args = [c for c in args_node.children if c.type not in {"(", ")", ","}] if args_node else []
    if name in {"it", "test"}:
        fn = _extract_test_func(call, args, bytes_, lines)
        if fn:
            funcs.append(fn)
    elif name in {"describe", "context", "suite"}:
        cb = next((a for a in args if a.type in {"arrow_function", "function_expression"}), None)
        body = find_first_child(cb, "statement_block") if cb else None
        for s in [c for c in body.children if c.type == "expression_statement"] if body else []:
            nested = find_first_child(s, "call_expression")
            if nested:
                _process_test_call(nested, funcs, bytes_, lines)


def _extract_prop_func(c: Any, v_name: str, bytes_: bytes, lines: list[str], is_t: bool) -> IRFunction | None:
    p = find_first_child(c, "property_identifier")
    pn = get_node_text(p, bytes_) if p else "prop"
    val = c if c.type == "method_definition" else (find_first_child(c, "arrow_function") or find_first_child(c, "function_expression"))
    if not val:
        return None
    return _build_ir_function(_FuncSpec(pn, f"{v_name}.{pn}", is_t, doc_node=c), val, find_first_child(val, "statement_block") or val, bytes_, lines)


def _extract_var_funcs(decl: Any, bytes_: bytes, lines: list[str], is_t: bool) -> list[IRFunction]:
    id_n = find_first_child(decl, "identifier")
    if not id_n:
        return []
    v_name = get_node_text(id_n, bytes_)
    val = unwrap_wrapper_callable(decl, bytes_)
    if val:
        return [_build_ir_function(_FuncSpec(v_name, v_name, is_t, doc_node=decl), val, find_first_child(val, "statement_block") or val, bytes_, lines)]
    obj = find_first_child(decl, "object")
    res = [_extract_prop_func(c, v_name, bytes_, lines, is_t) for c in obj.children] if obj else []
    return [f for f in res if f is not None]


def _extract_js_units(
    root: Any, source_bytes: bytes, lines: list[str], is_test: bool
) -> tuple[list[IRClass], list[IRFunction], list[str]]:
    classes: list[IRClass] = []
    functions: list[IRFunction] = []
    imports: list[str] = []

    def dispatch(node: Any) -> None:
        t = node.type
        if t == "import_statement":
            src = find_first_child(node, "string")
            if src:
                imports.append(get_node_text(src, source_bytes).strip("\"'`"))
        elif t == "export_statement":
            for c in node.children:
                if c.type in {"class_declaration", "function_declaration", "lexical_declaration", "variable_declaration"}:
                    dispatch(c)
        elif t == "class_declaration":
            ext = JSClassExtractor(node, source_bytes, lines)
            methods, lcom4 = ext.extract_methods(is_test)
            classes.append(IRClass(ext.name, ext.name, node.start_point[0] + 1, node.end_point[0] + 1, count_effective_loc(node, lines), [], [], ext.fields, methods, lcom4, has_doc_comment(node, lines)))
        elif t == "function_declaration":
            n = find_first_child(node, "identifier")
            f_name = get_node_text(n, source_bytes) if n else "anonymous"
            functions.append(_build_ir_function(_FuncSpec(f_name, f_name, is_test), node, find_first_child(node, "statement_block"), source_bytes, lines))
        elif t in {"lexical_declaration", "variable_declaration"}:
            for d in [c for c in node.children if c.type == "variable_declarator"]:
                functions.extend(_extract_var_funcs(d, source_bytes, lines, is_test))
        elif t == "expression_statement":
            call = find_first_child(node, "call_expression")
            if call:
                _process_test_call(call, functions, source_bytes, lines)

    for child in root.children:
        dispatch(child)
    return classes, functions, imports


def parse_javascript_file(file_path: Path, rel_path: str, is_test: bool) -> IRModule:
    """Parse a JavaScript or JSX file into an IRModule using Tree-Sitter."""
    tree_sitter, tree_sitter_javascript = check_javascript_dependencies()
    source_bytes = file_path.read_bytes()
    lines = source_bytes.decode("utf-8", errors="replace").splitlines()

    language = tree_sitter.Language(tree_sitter_javascript.language())
    parser = tree_sitter.Parser(language)
    tree = parser.parse(source_bytes)

    classes, functions, imports = _extract_js_units(tree.root_node, source_bytes, lines, is_test)
    directives = extract_directives(tree.root_node, source_bytes)
    loc = max(sum(c.loc for c in classes) + sum(f.loc for f in functions), count_effective_loc(tree.root_node, lines))
    return IRModule(rel_path, "javascript", is_test, loc, imports, classes, functions, "native", has_doc_comment(tree.root_node, lines), directives=directives)
