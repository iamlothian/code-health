"""Tree-Sitter Concrete Syntax Tree (CST) parser for TypeScript and TSX source files."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

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
from _code_health.js_parser import (
    _calc_js_lcom4,
    _count_effective_js_loc,
    _extract_jsdoc_params,
    _find_first_child,
    _get_node_text,
    _has_doc_comment,
)


def check_typescript_dependencies() -> tuple[Any, Any]:
    """Verify tree-sitter and tree-sitter-typescript are available or raise MissingNativeParserError."""
    try:
        import tree_sitter
        import tree_sitter_typescript
        return tree_sitter, tree_sitter_typescript
    except ImportError as exc:
        raise MissingNativeParserError("typescript", ["tree-sitter", "tree-sitter-typescript"]) from exc


@dataclass
class _TSTypeSmells:
    """Type safety escape hatch counters."""

    any_count: int = 0
    ts_ignore_count: int = 0
    non_null_count: int = 0
    ignore_lines: set[int] = field(default_factory=set)


@dataclass
class _TSSmells:
    """ECMAScript and TypeScript anti-pattern and escape hatch tracking."""

    var_count: int = 0
    loose_eq: int = 0
    has_proto: bool = False
    has_with: bool = False
    has_debugger: bool = False
    types: _TSTypeSmells = field(default_factory=_TSTypeSmells)

    def scan_node(self, node: Any, bytes_: bytes) -> None:
        """Scan a CST node for language smells and type escape hatches."""
        _scan_syntax_smell(node, bytes_, self)

    def _walk_escapes(self, node: Any, bytes_: bytes) -> None:
        _scan_type_escape(node, bytes_, self.types)
        for c in node.children:
            self._walk_escapes(c, bytes_)

    def scan_header(self, fn_node: Any, body: Any, bytes_: bytes, lines: list[str]) -> None:
        """Scan signature types and preceding comment directives for a function."""
        if body and body != fn_node:
            for c in fn_node.children:
                if c.type in {"formal_parameters", "type_annotation"}:
                    self._walk_escapes(c, bytes_)
        for idx in range(fn_node.start_point[0] - 1, max(-1, fn_node.start_point[0] - 6), -1):
            s = lines[idx].strip()
            if s and not (s.startswith(("//", "/*", "*")) or s.endswith("*/")):
                break
            if "@ts-ignore" in s or "@ts-nocheck" in s:
                self.types.ts_ignore_count += 1
                self.types.ignore_lines.add(idx + 1)

    def _has_str_leaf(self, node: Any) -> bool:
        return node.type in {"string", "template_string"} or any(self._has_str_leaf(c) for c in node.children)

    def is_unsafe_query_arg(self, arg: Any) -> bool:
        """Check whether an argument uses string concatenation or template interpolation."""
        if arg.type == "template_string":
            return any(c.type == "template_substitution" for c in arg.children)
        if arg.type == "binary_expression" and any(c.type == "+" for c in arg.children):
            return self._has_str_leaf(arg)
        return False


def _scan_type_escape(node: Any, bytes_: bytes, types: _TSTypeSmells) -> None:
    """Record occurrences of explicit any, ts-ignore, or non-null assertions."""
    t = node.type
    if t == "non_null_expression":
        types.non_null_count += 1
    elif t == "any":
        types.any_count += 1
    elif t == "comment":
        txt = _get_node_text(node, bytes_)
        if "@ts-ignore" in txt or "@ts-nocheck" in txt:
            types.ts_ignore_count += 1
            types.ignore_lines.add(node.start_point[0] + 1)


def _scan_syntax_smell(node: Any, bytes_: bytes, smells: _TSSmells) -> None:
    """Check for debugger, with, var, loose equality, and proto mutations."""
    t = node.type
    if t == "debugger_statement":
        smells.has_debugger = True
    elif t == "with_statement":
        smells.has_with = True
    elif t == "variable_declaration":
        smells.var_count += sum(c.type == "variable_declarator" for c in node.children)
    elif t == "binary_expression":
        smells.loose_eq += sum(c.type in {"==", "!="} for c in node.children)
    elif t == "assignment_expression" and node.children:
        if "__proto__" in _get_node_text(node.children[0], bytes_):
            smells.has_proto = True
    else:
        _scan_type_escape(node, bytes_, smells.types)


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

    def scan(self, body_node: Any, depth: int = 0) -> None:
        """Scan AST recursively updating complexity and collecting smells."""
        if not body_node:
            return
        for child in body_node.children:
            self._dispatch_node(child, depth)

    def _dispatch_node(self, node: Any, depth: int) -> None:
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
            self._dispatch_expressions(node)
        next_d = depth + 1 if t in {"if_statement", "for_statement", "for_in_statement", "for_of_statement", "while_statement", "do_statement", "switch_statement", "try_statement", "catch_clause", "with_statement"} else depth
        self.scan(node, next_d)

    def _record_call(self, node: Any) -> None:
        c_name = _get_node_text(node.children[0], self.bytes) if node.children else ""
        args = _find_first_child(node, "arguments")
        first = next((c for c in args.children if c.type not in {"(", ")", ","}), None) if args else None
        has_concat = bool(first and self.smells.is_unsafe_query_arg(first))
        has_str_arg = bool(first and (first.type in {"string", "template_string"} or has_concat))
        self.calls.append(IRCall(c_name, c_name, node.start_point[0] + 1, has_concat, has_str_arg))
        if c_name.endswith(".setPrototypeOf") or c_name == "setPrototypeOf":
            self.smells.has_proto = True

    def _dispatch_expressions(self, node: Any) -> None:
        t = node.type
        self.smells.scan_node(node, self.bytes)
        if t == "binary_expression":
            self.stats[0] += sum(c.type in {"&&", "||", "??"} for c in node.children)
        elif t == "call_expression" and node.children:
            self._record_call(node)
        elif t == "new_expression":
            con = _find_first_child(node, "identifier")
            if con and _get_node_text(con, self.bytes) == "Function":
                self.calls.append(IRCall("new Function", "Function", node.start_point[0] + 1))
        elif t == "member_expression" and any(c.type == "this" for c in node.children):
            prop = _find_first_child(node, "property_identifier")
            if prop:
                self.accessed_fields.add(_get_node_text(prop, self.bytes))

    def _visit_switch(self, node: Any, depth: int) -> None:
        body = _find_first_child(node, "switch_body") or node
        cases = [c for c in body.children if c.type == "switch_case"]
        self.stats[0] += max(1, len(cases))
        self.stats[1] += 1 + depth
        self.stats[2] = max(self.stats[2], depth + 1)

    def _visit_try(self, node: Any, depth: int) -> None:
        catch = _find_first_child(node, "catch_clause")
        if not catch:
            return
        self.stats[0] += 1
        self.stats[1] += 1 + depth
        self.stats[2] = max(self.stats[2], depth + 1)
        param = _find_first_child(catch, "identifier")
        p_text = _get_node_text(param, self.bytes) if param else None
        block = _find_first_child(catch, "statement_block")
        stmts = [c for c in block.children if c.type not in {"{", "}", "comment"}] if block else []
        self.except_handlers.append(IRExceptHandler(p_text, len(stmts) == 0, True, catch.start_point[0] + 1))


@dataclass(frozen=True)
class _TSFuncSpec:
    """Specification metadata for constructing an IRFunction."""

    name: str
    qualname: str
    is_test: bool
    fields: set[str] | None = None
    claimed_lines: set[int] | None = None


def _parse_ts_param(c: Any, source_bytes: bytes, jsdoc: dict[str, str]) -> IRParam | None:
    """Extract a single IRParam from a parameter CST node."""
    if c.type in {"(", ")", ","}:
        return None
    id_node = _find_first_child(c, "identifier") or (c if c.type == "identifier" else None)
    nm = _get_node_text(id_node, source_bytes) if id_node else "arg"
    type_node = _find_first_child(c, "type_annotation")
    d_type = _get_node_text(type_node, source_bytes).strip(": ") if type_node else jsdoc.get(nm)
    has_assign = any(ch.type == "=" for ch in c.children)
    has_def = c.type == "optional_parameter" or has_assign
    is_bool_lit = has_assign and any(ch.type in {"true", "false"} for ch in c.children)
    eff_type = "bool" if (d_type in {"boolean", "bool"} or is_bool_lit) else ("inferred" if (not d_type and has_def) else d_type)
    return IRParam(nm, eff_type, has_def)


def _extract_ts_params(fn_node: Any, source_bytes: bytes, jsdoc: dict[str, str]) -> list[IRParam]:
    """Extract formal parameters and types from function or arrow definition."""
    p_list = _find_first_child(fn_node, "formal_parameters")
    if not p_list:
        first = fn_node.children[0] if fn_node.children else None
        if fn_node.type == "arrow_function" and first and first.type == "identifier":
            nm = _get_node_text(first, source_bytes)
            return [IRParam(nm, jsdoc.get(nm), False)]
        return []
    result = [_parse_ts_param(c, source_bytes, jsdoc) for c in p_list.children]
    return [p for p in result if p is not None]


def _extract_ts_return_type(fn_node: Any, source_bytes: bytes) -> str | None:
    """Extract return type annotation from function or method definition."""
    if fn_node.type == "method_definition":
        prop = _find_first_child(fn_node, "property_identifier")
        if prop and _get_node_text(prop, source_bytes) == "constructor":
            return "void"
    ret = fn_node.child_by_field_name("return_type") or _find_first_child(fn_node, "type_annotation")
    return _get_node_text(ret, source_bytes).strip(": ") if ret else None


def _build_ts_ir_function(
    spec: _TSFuncSpec, node: Any, body: Any, source_bytes: bytes, lines: list[str]
) -> IRFunction:
    """Construct a complete IRFunction from TypeScript syntax node."""
    v = _TSVisitor(source_bytes, spec.fields)
    v.smells.scan_header(node, body, source_bytes, lines)
    v.scan(body or node, 0)
    if spec.claimed_lines is not None:
        spec.claimed_lines.update(v.smells.types.ignore_lines)
    return IRFunction(
        name=spec.name,
        qualname=spec.qualname,
        lineno=node.start_point[0] + 1,
        end_lineno=node.end_point[0] + 1,
        loc=_count_effective_js_loc(node, lines),
        params=_extract_ts_params(node, source_bytes, _extract_jsdoc_params(node, lines)),
        return_type=_extract_ts_return_type(node, source_bytes),
        max_nesting=v.stats[2],
        cyclomatic_complexity=v.stats[0],
        cognitive_complexity=v.stats[1],
        returns_count=v.stats[3],
        calls=v.calls,
        accessed_fields=list(v.accessed_fields),
        except_handlers=v.except_handlers,
        is_test=spec.is_test,
        has_docstring=_has_doc_comment(node, lines),
        var_declarations_count=v.smells.var_count,
        loose_comparisons_count=v.smells.loose_eq,
        has_proto_mutation=v.smells.has_proto,
        has_with_statement=v.smells.has_with,
        has_debugger_statement=v.smells.has_debugger,
        explicit_any_count=v.smells.types.any_count,
        ts_ignore_count=v.smells.types.ts_ignore_count,
        non_null_assertion_count=v.smells.types.non_null_count,
    )


def _extract_param_properties(ctor_node: Any, bytes_: bytes) -> list[IRField]:
    """Extract constructor parameter properties (public, private, protected, readonly)."""
    fields: list[IRField] = []
    p_list = _find_first_child(ctor_node, "formal_parameters")
    if not p_list:
        return fields
    for p in p_list.children:
        p_text = _get_node_text(p, bytes_)
        if any(k in p_text for k in ("public ", "private ", "protected ", "readonly ")):
            id_node = _find_first_child(p, "identifier")
            if id_node:
                fields.append(IRField(_get_node_text(id_node, bytes_), None, [], p.start_point[0] + 1))
    return fields


def _extract_this_assignments(ctor_node: Any, bytes_: bytes) -> list[IRField]:
    """Extract this.field assignments inside constructor body."""
    fields: list[IRField] = []
    block = _find_first_child(ctor_node, "statement_block")
    if not block:
        return fields
    for s in [c for c in block.children if c.type == "expression_statement"]:
        asn = _find_first_child(s, "assignment_expression")
        left = asn.children[0] if asn and asn.children else None
        if left and left.type == "member_expression" and len(left.children) >= 3 and _get_node_text(left.children[0], bytes_) == "this":
            fields.append(IRField(_get_node_text(left.children[2], bytes_), None, [], s.start_point[0] + 1))
    return fields


class TSClassExtractor:
    """Extracts methods, fields (including parameter properties), and LCOM4 for a TypeScript class."""

    def __init__(self, class_node: Any, source_bytes: bytes, lines: list[str]) -> None:
        """Initialize class extractor with CST node and source text."""
        self.node = class_node
        self.bytes = source_bytes
        self.lines = lines
        id_node = _find_first_child(self.node, "type_identifier") or _find_first_child(self.node, "identifier")
        self.name = _get_node_text(id_node, self.bytes) if id_node else "AnonymousClass"
        self.fields = self._collect_fields()
        self.field_names = {f.name for f in self.fields}

    def _collect_fields(self) -> list[IRField]:
        body = _find_first_child(self.node, "class_body") or self.node
        fields: dict[str, IRField] = {}
        for child in body.children:
            prop = _find_first_child(child, "property_identifier")
            name = _get_node_text(prop, self.bytes) if prop else ""
            if child.type in {"field_definition", "public_field_definition", "property_definition"} and name:
                fields[name] = IRField(name, None, [], child.start_point[0] + 1)
            elif child.type == "method_definition" and name == "constructor":
                for f in _extract_param_properties(child, self.bytes) + _extract_this_assignments(child, self.bytes):
                    fields[f.name] = f
        return list(fields.values())

    def extract_methods(self, is_test: bool, claimed: set[int] | None = None) -> tuple[list[IRFunction], int]:
        """Extract all methods and calculate LCOM4 cohesion score."""
        body = _find_first_child(self.node, "class_body") or self.node
        methods: list[IRFunction] = []
        for m in body.children:
            if m.type == "method_definition":
                prop = _find_first_child(m, "property_identifier")
                m_name = _get_node_text(prop, self.bytes) if prop else "<method>"
                spec = _TSFuncSpec(m_name, f"{self.name}.{m_name}", is_test, self.field_names, claimed)
                methods.append(_build_ts_ir_function(spec, m, _find_first_child(m, "statement_block"), self.bytes, self.lines))
        return methods, _calc_js_lcom4(methods, is_test)


def _handle_ts_test_call(
    call: Any, args: list[Any], bytes_: bytes, lines: list[str]
) -> IRFunction | None:
    """Build IRFunction for an it() or test() call."""
    cb = next((a for a in args[1:] if a.type in {"arrow_function", "function_expression"}), None)
    if not cb:
        return None
    desc = _get_node_text(args[0], bytes_).strip("\"'`") if args and args[0].type in {"string", "template_string"} else ""
    nm = f"test: {desc}" if desc else f"test: line {call.start_point[0] + 1}"
    body = _find_first_child(cb, "statement_block") or cb
    return _build_ts_ir_function(_TSFuncSpec(nm, nm, True), cb, body, bytes_, lines)


def _handle_ts_suite_call(args: list[Any], funcs: list[IRFunction], bytes_: bytes, lines: list[str]) -> None:
    """Recursively process nested test calls inside describe/context/suite blocks."""
    cb = next((a for a in args if a.type in {"arrow_function", "function_expression"}), None)
    body = _find_first_child(cb, "statement_block") if cb else None
    if not body:
        return
    for s in [c for c in body.children if c.type == "expression_statement"]:
        nested = _find_first_child(s, "call_expression")
        if nested:
            _process_ts_test_call(nested, funcs, bytes_, lines)


_TS_TEST_CALLS = frozenset({
    "it", "test", "it.only", "it.skip", "it.concurrent",
    "test.only", "test.skip", "test.concurrent", "fit", "xit",
})
_TS_SUITE_CALLS = frozenset({
    "describe", "describe.only", "describe.skip", "context", "suite", "fdescribe", "xdescribe",
})


def _process_ts_test_call(call: Any, funcs: list[IRFunction], bytes_: bytes, lines: list[str]) -> None:
    """Process Jest/Vitest/Mocha BDD test blocks."""
    name = _get_node_text(call.children[0], bytes_) if call.children else ""
    args_node = _find_first_child(call, "arguments")
    args = [c for c in args_node.children if c.type not in {"(", ")", ","}] if args_node else []
    if name in _TS_TEST_CALLS:
        fn = _handle_ts_test_call(call, args, bytes_, lines)
        if fn:
            funcs.append(fn)
    elif name in _TS_SUITE_CALLS:
        _handle_ts_suite_call(args, funcs, bytes_, lines)


def _extract_ts_var_funcs(
    decl: Any, bytes_: bytes, lines: list[str], is_t: bool, claimed: set[int] | None = None
) -> list[IRFunction]:
    """Extract named arrow functions and function expressions from variable declarations."""
    id_n = _find_first_child(decl, "identifier")
    if not id_n:
        return []
    v_name = _get_node_text(id_n, bytes_)
    val = _find_first_child(decl, "arrow_function") or _find_first_child(decl, "function_expression")
    if val:
        spec = _TSFuncSpec(v_name, v_name, is_t, None, claimed)
        return [_build_ts_ir_function(spec, val, _find_first_child(val, "statement_block") or val, bytes_, lines)]
    return []


def _extract_ts_units(
    root: Any, source_bytes: bytes, lines: list[str], is_test: bool
) -> tuple[list[IRClass], list[IRFunction], list[str], int]:
    """Traverse CST root and extract classes, functions, imports, and module directives."""
    classes, functions, imports = [], [], []
    claimed: set[int] = set()

    def dispatch(node: Any) -> None:
        t = node.type
        if t == "import_statement":
            src = _find_first_child(node, "string")
            if src:
                imports.append(_get_node_text(src, source_bytes).strip("\"'`"))
        elif t == "export_statement":
            for c in node.children:
                if c.type in {"class_declaration", "abstract_class_declaration", "function_declaration", "lexical_declaration", "variable_declaration"}:
                    dispatch(c)
        elif t in {"class_declaration", "abstract_class_declaration"}:
            ext = TSClassExtractor(node, source_bytes, lines)
            methods, lcom4 = ext.extract_methods(is_test, claimed)
            classes.append(IRClass(ext.name, ext.name, node.start_point[0] + 1, node.end_point[0] + 1, _count_effective_js_loc(node, lines), [], [], ext.fields, methods, lcom4, _has_doc_comment(node, lines)))
        elif t in {"function_declaration", "generator_function_declaration"}:
            n = _find_first_child(node, "identifier")
            f_name = _get_node_text(n, source_bytes) if n else "anonymous"
            spec = _TSFuncSpec(f_name, f_name, is_test, None, claimed)
            functions.append(_build_ts_ir_function(spec, node, _find_first_child(node, "statement_block"), source_bytes, lines))
        elif t in {"lexical_declaration", "variable_declaration"}:
            for d in [c for c in node.children if c.type == "variable_declarator"]:
                functions.extend(_extract_ts_var_funcs(d, source_bytes, lines, is_test, claimed))
        elif t == "expression_statement":
            call = _find_first_child(node, "call_expression")
            if call:
                _process_ts_test_call(call, functions, source_bytes, lines)

    for child in root.children:
        dispatch(child)
    mod_ignores = sum(
        1 for c in root.children
        if c.type == "comment" and (c.start_point[0] + 1) not in claimed and ("@ts-ignore" in _get_node_text(c, source_bytes) or "@ts-nocheck" in _get_node_text(c, source_bytes))
    )
    return classes, functions, imports, mod_ignores


def parse_typescript_file(file_path: Path, rel_path: str, is_test: bool) -> IRModule:
    """Parse a TypeScript or TSX file into an IRModule using Tree-Sitter."""
    tree_sitter, tree_sitter_typescript = check_typescript_dependencies()
    source_bytes = file_path.read_bytes()
    lines = source_bytes.decode("utf-8", errors="replace").splitlines()

    lang_func = tree_sitter_typescript.language_tsx if file_path.suffix.lower() == ".tsx" else tree_sitter_typescript.language_typescript
    language = tree_sitter.Language(lang_func())
    parser = tree_sitter.Parser(language)
    tree = parser.parse(source_bytes)

    classes, functions, imports, mod_ignores = _extract_ts_units(tree.root_node, source_bytes, lines, is_test)
    loc = max(sum(c.loc for c in classes) + sum(f.loc for f in functions), _count_effective_js_loc(tree.root_node, lines))
    return IRModule(rel_path, "typescript", is_test, loc, imports, classes, functions, "native", _has_doc_comment(tree.root_node, lines), ts_ignore_count=mod_ignores)
