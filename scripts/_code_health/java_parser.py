"""Tree-Sitter Concrete Syntax Tree (CST) parser for Java source files."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from _code_health.ast_engine import _bfs_component_count

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

EXEMPT_JAVA_ANNOTATIONS = {"Entity", "Table", "Data", "Value", "Configuration", "ConfigurationProperties", "SpringBootApplication"}


def check_java_dependencies() -> tuple[Any, Any]:
    """Verify tree-sitter and tree-sitter-java are available or raise MissingNativeParserError."""
    try:
        import tree_sitter
        import tree_sitter_java
        return tree_sitter, tree_sitter_java
    except ImportError as exc:
        raise MissingNativeParserError("java", ["tree-sitter", "tree-sitter-java"]) from exc


def _get_node_text(node: Any, source_bytes: bytes) -> str:
    return source_bytes[node.start_byte : node.end_byte].decode("utf-8", errors="replace")


def _find_children(node: Any, type_name: str) -> list[Any]:
    return [c for c in node.children if c.type == type_name]


def _find_first_child(node: Any, type_name: str) -> Any | None:
    for c in node.children:
        if c.type == type_name:
            return c
    return None


def _parse_annotations(node: Any, source_bytes: bytes) -> list[IRAnnotation]:
    modifiers = _find_first_child(node, "modifiers")
    if not modifiers:
        return []
    decs: list[IRAnnotation] = []
    for c in modifiers.children:
        if c.type in {"annotation", "marker_annotation"}:
            name_node = _find_first_child(c, "identifier") or _find_first_child(c, "scoped_identifier")
            if name_node:
                raw_name = _get_node_text(name_node, source_bytes).strip("@")
                decs.append(IRAnnotation(raw_name, {}, c.start_point[0] + 1))
    return decs


def _parse_modifiers(node: Any, source_bytes: bytes) -> list[str]:
    modifiers = _find_first_child(node, "modifiers")
    if not modifiers:
        return []
    mods: list[str] = []
    for c in modifiers.children:
        if c.type not in {"annotation", "marker_annotation"}:
            text = _get_node_text(c, source_bytes).strip()
            if text:
                mods.append(text)
    return mods


def _has_doc_comment(node: Any, lines: list[str]) -> bool:
    start_line = node.start_point[0]
    for idx in range(max(0, start_line - 3), start_line):
        line = lines[idx].strip()
        if line.startswith("/**") or line.endswith("*/") or line.startswith("*"):
            return True
    return False


def _count_effective_java_loc(node: Any, lines: list[str]) -> int:
    start = node.start_point[0]
    end = min(node.end_point[0] + 1, len(lines))
    count = 0
    in_block = False
    for line in lines[start:end]:
        stripped = line.strip()
        if not stripped:
            continue
        if "/*" in stripped:
            in_block = True
        if in_block:
            if "*/" in stripped:
                in_block = False
            continue
        if not stripped.startswith("//") and not stripped.startswith("*"):
            count += 1
    return max(1, count)


class _MethodCSTVisitor:
    """Computes complexity, nesting, calls, and field references for a Java method node."""

    def __init__(self, source_bytes: bytes, class_fields: set[str]) -> None:
        self.bytes = source_bytes
        self.class_fields = class_fields
        self.stats = [1, 0, 0, 0]  # [cc, cog, max_nesting, returns]
        self.calls: list[IRCall] = []
        self.accessed_fields: set[str] = set()
        self.concat_vars: set[str] = set()
        self.except_handlers: list[IRExceptHandler] = []

    def scan(self, body_node: Any, depth: int = 0) -> None:
        """Scan a method body block recursively."""
        if not body_node:
            return
        for child in body_node.children:
            self._dispatch_node(child, depth)

    def _dispatch_node(self, node: Any, depth: int) -> None:
        t = node.type
        if t == "return_statement":
            self.stats[3] += 1
        elif t in {"for_statement", "enhanced_for_statement", "while_statement", "do_statement"}:
            self._visit_loop(node, depth)
        elif t in {"switch_expression", "switch_statement"}:
            self._visit_switch(node, depth)
        elif t == "if_statement":
            self._visit_if(node, depth)
        elif t == "try_statement":
            self._visit_try(node, depth)
        elif t == "variable_declarator":
            self._record_var_decl(node)
        elif t == "method_invocation":
            self._record_call(node)
        elif t in {"identifier", "field_access"}:
            self._record_field_access(node)
        self.scan(node, depth)

    def _visit_if(self, node: Any, depth: int) -> None:
        self.stats[0] += 1
        self.stats[1] += 1 + depth
        self.stats[2] = max(self.stats[2], depth + 1)

    def _visit_loop(self, node: Any, depth: int) -> None:
        self.stats[0] += 1
        self.stats[1] += 1 + depth
        self.stats[2] = max(self.stats[2], depth + 1)

    def _visit_switch(self, node: Any, depth: int) -> None:
        cases = _find_children(node, "switch_block_statement_group") + _find_children(node, "switch_rule")
        self.stats[0] += max(1, len(cases))
        self.stats[1] += 1 + depth
        self.stats[2] = max(self.stats[2], depth + 1)

    def _visit_try(self, node: Any, depth: int) -> None:
        for catch in _find_children(node, "catch_clause"):
            self.stats[0] += 1
            self.stats[1] += 1 + depth
            param = _find_first_child(catch, "catch_formal_parameter")
            p_text = _get_node_text(param, self.bytes) if param else ""
            is_broad = "Exception" in p_text or "Throwable" in p_text
            block = _find_first_child(catch, "block")
            is_empty = not block or len(block.children) <= 2
            self.except_handlers.append(IRExceptHandler(p_text, is_empty, is_broad, catch.start_point[0] + 1))

    def _record_var_decl(self, node: Any) -> None:
        val = node.child_by_field_name("value")
        if val and ("+" in _get_node_text(val, self.bytes) or "concat" in _get_node_text(val, self.bytes)):
            name_node = node.child_by_field_name("name")
            if name_node:
                self.concat_vars.add(_get_node_text(name_node, self.bytes))

    def _record_call(self, node: Any) -> None:
        name_node = node.child_by_field_name("name") or _find_first_child(node, "identifier")
        call_name = _get_node_text(name_node, self.bytes) if name_node else ""
        obj_node = node.child_by_field_name("object")
        full_call = f"{_get_node_text(obj_node, self.bytes)}.{call_name}" if obj_node else call_name
        args_node = node.child_by_field_name("arguments")
        args_text = _get_node_text(args_node, self.bytes) if args_node else ""
        has_concat = "+" in args_text or any(v in args_text for v in self.concat_vars)
        self.calls.append(IRCall(full_call, full_call, node.start_point[0] + 1, has_concat))

    def _record_field_access(self, node: Any) -> None:
        field = node.child_by_field_name("field") if node.type == "field_access" else node
        if field:
            token = _get_node_text(field, self.bytes)
            if token in self.class_fields or node.type == "field_access":
                self.accessed_fields.add(token)


def _compute_java_lcom4(m_tokens: dict[str, set[str]]) -> int:
    names = list(m_tokens)
    adj: dict[str, set[str]] = {n: set() for n in names}
    for i, n1 in enumerate(names):
        for n2 in names[i + 1 :]:
            if m_tokens[n1] & m_tokens[n2]:
                adj[n1].add(n2)
                adj[n2].add(n1)
    return _bfs_component_count(names, adj)


def _extract_java_params(m_node: Any, source_bytes: bytes) -> list[IRParam]:
    p_list = _find_first_child(m_node, "formal_parameters")
    if not p_list:
        return []
    params: list[IRParam] = []
    for p in _find_children(p_list, "formal_parameter"):
        p_id = _find_first_child(p, "identifier")
        p_decs = _parse_annotations(p, source_bytes)
        p_name = _get_node_text(p_id, source_bytes) if p_id else "arg"
        params.append(IRParam(p_name, "Object", False, p_decs))
    return params


class JavaClassExtractor:
    """Extracts methods, fields, and LCOM4 for a Java class or record."""

    def __init__(self, class_node: Any, source_bytes: bytes, lines: list[str]) -> None:
        self.node = class_node
        self.bytes = source_bytes
        self.lines = lines
        self.name = self._resolve_name()
        self.fields = self._collect_fields()
        self.field_names = {f.name for f in self.fields}

    def _resolve_name(self) -> str:
        name_node = _find_first_child(self.node, "identifier")
        return _get_node_text(name_node, self.bytes) if name_node else "Anonymous"

    def _collect_fields(self) -> list[IRField]:
        body = _find_first_child(self.node, "class_body") or self.node
        fields: list[IRField] = []
        for decl in _find_children(body, "field_declaration"):
            decs = _parse_annotations(decl, self.bytes)
            for var in _find_children(decl, "variable_declarator"):
                id_node = _find_first_child(var, "identifier")
                if id_node:
                    fields.append(IRField(_get_node_text(id_node, self.bytes), "", decs, decl.start_point[0] + 1))
        return fields

    def extract_methods(self, is_test: bool) -> tuple[list[IRFunction], int]:
        """Extract method reports and calculate LCOM4 connected components."""
        body = _find_first_child(self.node, "class_body") or self.node
        m_nodes = _find_children(body, "method_declaration") + _find_children(body, "constructor_declaration")
        methods: list[IRFunction] = []
        m_tokens: dict[str, set[str]] = {}

        for m in m_nodes:
            fn = self._build_function(m, is_test)
            methods.append(fn)
            if not fn.name.startswith("<"):
                tokens = {f"a:{a}" for a in fn.accessed_fields} | {f"m:{m_name}" for m_name in fn.accessed_fields} | {f"m:{fn.name}"}
                m_tokens[fn.name] = tokens

        is_exempt = self.node.type in {"record_declaration", "enum_declaration"} or bool(
            {a.name for a in _parse_annotations(self.node, self.bytes)} & EXEMPT_JAVA_ANNOTATIONS
        )
        lcom4 = 1 if is_exempt or len(methods) <= 2 else _compute_java_lcom4(m_tokens)
        return methods, lcom4

    def _build_function(self, m_node: Any, is_test: bool) -> IRFunction:
        id_node = _find_first_child(m_node, "identifier")
        m_name = _get_node_text(id_node, self.bytes) if id_node else "<init>"
        body = _find_first_child(m_node, "block")
        v = _MethodCSTVisitor(self.bytes, self.field_names)
        v.scan(body, 0)
        loc = _count_effective_java_loc(m_node, self.lines)
        return IRFunction(
            name=m_name,
            qualname=f"{self.name}.{m_name}",
            lineno=m_node.start_point[0] + 1,
            end_lineno=m_node.end_point[0] + 1,
            loc=loc,
            params=_extract_java_params(m_node, self.bytes),
            return_type="void",
            max_nesting=v.stats[2],
            cyclomatic_complexity=v.stats[0],
            cognitive_complexity=v.stats[1],
            returns_count=v.stats[3],
            calls=v.calls,
            accessed_fields=list(v.accessed_fields),
            except_handlers=v.except_handlers,
            is_test=is_test,
            annotations=_parse_annotations(m_node, self.bytes),
            modifiers=_parse_modifiers(m_node, self.bytes),
            has_docstring=_has_doc_comment(m_node, self.lines),
        )


def _extract_java_classes(root: Any, source_bytes: bytes, lines: list[str], is_test: bool) -> list[IRClass]:
    classes: list[IRClass] = []
    class_types = {"class_declaration", "record_declaration", "interface_declaration", "enum_declaration"}
    for child in root.children:
        if child.type in class_types:
            extractor = JavaClassExtractor(child, source_bytes, lines)
            methods, lcom4 = extractor.extract_methods(is_test)
            decs = _parse_annotations(child, source_bytes)
            classes.append(
                IRClass(
                    name=extractor.name,
                    qualname=extractor.name,
                    lineno=child.start_point[0] + 1,
                    end_lineno=child.end_point[0] + 1,
                    loc=_count_effective_java_loc(child, lines),
                    annotations=decs,
                    base_types=[],
                    fields=extractor.fields,
                    methods=methods,
                    lcom4=lcom4,
                    has_docstring=_has_doc_comment(child, lines),
                )
            )
    return classes


def parse_java_file(file_path: Path, rel_path: str, is_test: bool) -> IRModule:
    """Parse a Java file into an IRModule using Tree-Sitter."""
    tree_sitter, tree_sitter_java = check_java_dependencies()
    source_bytes = file_path.read_bytes()
    lines = source_bytes.decode("utf-8", errors="replace").splitlines()

    language = tree_sitter.Language(tree_sitter_java.language())
    parser = tree_sitter.Parser(language)
    tree = parser.parse(source_bytes)

    classes = _extract_java_classes(tree.root_node, source_bytes, lines, is_test)
    loc = sum(c.loc for c in classes) or max(1, len(lines))
    return IRModule(rel_path, "java", is_test, loc, [], classes, [], "native")
