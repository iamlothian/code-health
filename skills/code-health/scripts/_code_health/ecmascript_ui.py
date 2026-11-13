"""Generic framework-agnostic ECMAScript CST helpers shared by JS and TS parsers."""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any

from _code_health.ir_models import IRAnnotation

BRANCH_LOOP_NODES = frozenset({
    "if_statement", "for_statement", "for_in_statement", "for_of_statement",
    "while_statement", "do_statement", "switch_statement", "try_statement",
    "catch_clause", "with_statement", "ternary_expression",
    "arrow_function", "function_expression",
})
_JSX_NODES = frozenset({"jsx_element", "jsx_self_closing_element", "jsx_fragment"})
_DOM_PROP_SINKS = frozenset({"innerHTML", "outerHTML"})
_WRAPPER_CALLS = frozenset({"memo", "forwardRef"})


def get_node_text(node: Any, source_bytes: bytes) -> str:
    """Decode utf-8 text from a CST node byte span."""
    return source_bytes[node.start_byte : node.end_byte].decode("utf-8", errors="replace")


def find_first_child(node: Any, type_name: str) -> Any | None:
    """Return the first direct child matching type_name, if any."""
    return next((c for c in node.children if c.type == type_name), None)


def count_effective_loc(node: Any, lines: list[str]) -> int:
    """Count non-blank, non-comment lines of code for a CST node."""
    count, in_block = 0, False
    for line in lines[node.start_point[0] : min(node.end_point[0] + 1, len(lines))]:
        stripped = line.strip()
        if not stripped:
            continue
        if "/*" in stripped:
            in_block = True
        if in_block:
            in_block = "*/" not in stripped
            continue
        if not stripped.startswith(("//", "*")):
            count += 1
    return max(1, count)


def _attached_decorator_nodes(node: Any) -> list[Any]:
    dec_nodes = [c for c in node.children if c.type == "decorator"]
    parent = getattr(node, "parent", None)
    if parent is not None and parent.type == "export_statement":
        dec_nodes.extend(c for c in parent.children if c.type == "decorator")
    prev = getattr(node, "prev_named_sibling", None)
    while prev is not None and prev.type == "decorator":
        dec_nodes.append(prev)
        prev = getattr(prev, "prev_named_sibling", None)
    return list({d.start_byte: d for d in dec_nodes}.values())


def _effective_doc_start_line(node: Any) -> int:
    start_line = node.start_point[0]
    for dec in _attached_decorator_nodes(node):
        start_line = min(start_line, dec.start_point[0])
    parent = getattr(node, "parent", None)
    if parent is not None and parent.type == "export_statement":
        start_line = min(start_line, parent.start_point[0])
    return start_line


def has_doc_comment(node: Any, lines: list[str]) -> bool:
    """Check if CST node has a preceding JSDoc comment block (including above decorators)."""
    start_line = _effective_doc_start_line(node)
    for idx in range(max(0, start_line - 3), start_line):
        stripped = lines[idx].strip()
        if stripped.startswith(("/**", "*")) or stripped.endswith("*/"):
            return True
    return False


def extract_jsdoc_params(node: Any, lines: list[str]) -> dict[str, str]:
    """Extract JSDoc @param {type} annotations preceding a function or method."""
    doc: list[str] = []
    for idx in range(node.start_point[0] - 1, max(-1, node.start_point[0] - 20), -1):
        stripped = lines[idx].strip()
        if not stripped.startswith(("*", "/**")) and not stripped.endswith("*/"):
            if stripped:
                break
            continue
        doc.append(stripped)
        if stripped.startswith("/**"):
            break
    if not doc:
        return {}
    matches = re.findall(r"@param\s+\{([^}]+)\}\s+(?:\[)?([a-zA-Z0-9_$]+)", " ".join(reversed(doc)))
    return {name: typ.strip() for typ, name in matches}


def extract_directives(root: Any, source_bytes: bytes) -> list[str]:
    """Extract leading top-level ECMAScript directive prologue strings."""
    directives: list[str] = []
    for child in root.children:
        if child.type == "comment":
            continue
        if child.type != "expression_statement":
            break
        str_node = find_first_child(child, "string")
        if not str_node:
            break
        directives.append(get_node_text(str_node, source_bytes).strip("\"'`"))
    return directives


def _decorator_to_ir(dec_node: Any, source_bytes: bytes) -> IRAnnotation | None:
    call = find_first_child(dec_node, "call_expression")
    target = call.children[0] if call and call.children else (
        find_first_child(dec_node, "identifier") or find_first_child(dec_node, "member_expression")
    )
    if not target:
        return None
    short = get_node_text(target, source_bytes).split(".")[-1]
    return IRAnnotation(name=short, lineno=dec_node.start_point[0] + 1)


def extract_decorators(node: Any, source_bytes: bytes) -> list[IRAnnotation]:
    """Collect decorators attached directly, on enclosing export, or as preceding siblings."""
    dec_nodes = _attached_decorator_nodes(node)
    return [ann for d in sorted(dec_nodes, key=lambda n: n.start_byte) if (ann := _decorator_to_ir(d, source_bytes)) is not None]


def unwrap_wrapper_callable(decl: Any, source_bytes: bytes, depth: int = 0) -> Any | None:
    """Unwrap arrow/function expressions or nested HOC wrapper calls up to depth 3."""
    direct = find_first_child(decl, "arrow_function") or find_first_child(decl, "function_expression")
    if direct or depth >= 3:
        return direct
    call = decl if decl.type == "call_expression" else find_first_child(decl, "call_expression")
    if not call or not call.children:
        return None
    short = get_node_text(call.children[0], source_bytes).split(".")[-1]
    if short not in _WRAPPER_CALLS:
        return None
    args = find_first_child(call, "arguments")
    for child in args.children if args else ():
        if child.type in {"arrow_function", "function_expression"}:
            return child
        if child.type == "call_expression" and (inner := unwrap_wrapper_callable(child, source_bytes, depth + 1)):
            return inner
    return None


def extract_field_type_or_init(field_node: Any, source_bytes: bytes) -> str | None:
    """Return explicit type annotation or factory initializer call on a class field."""
    type_node = find_first_child(field_node, "type_annotation")
    if type_node:
        return get_node_text(type_node, source_bytes).strip(": ")
    call = find_first_child(field_node, "call_expression")
    return get_node_text(call, source_bytes) if call else None


@dataclass
class _UICSTState:
    """Accumulates generic JSX/DOM/key telemetry across a function CST subtree."""

    bytes: bytes
    jsx_count: int = 0
    sinks: list[tuple[str, int]] = field(default_factory=list)
    index_keys: list[int] = field(default_factory=list)

    def inspect(self, node: Any, map_idx_vars: frozenset[str]) -> frozenset[str]:
        """Inspect node and return updated in-scope array-index variable names."""
        t = node.type
        if t in _JSX_NODES:
            self.jsx_count += 1
        elif t == "jsx_attribute":
            self._check_jsx_attr(node, map_idx_vars)
        elif t == "assignment_expression":
            self._check_assignment_sink(node)
        elif t == "call_expression":
            return self._check_call(node, map_idx_vars)
        return map_idx_vars

    def _check_jsx_attr(self, attr: Any, map_idx_vars: frozenset[str]) -> None:
        prop = find_first_child(attr, "property_identifier")
        if not prop:
            return
        name = get_node_text(prop, self.bytes)
        if name == "dangerouslySetInnerHTML":
            self.sinks.append(("dangerouslySetInnerHTML", attr.start_point[0] + 1))
        elif name == "key" and map_idx_vars:
            expr = find_first_child(attr, "jsx_expression")
            if expr and find_first_child(expr, "identifier") and get_node_text(find_first_child(expr, "identifier"), self.bytes) in map_idx_vars:
                self.index_keys.append(attr.start_point[0] + 1)

    def _check_assignment_sink(self, asn: Any) -> None:
        left = asn.children[0] if asn.children else None
        if left and left.type == "member_expression" and left.children:
            prop = get_node_text(left.children[-1], self.bytes)
            if prop in _DOM_PROP_SINKS:
                self.sinks.append((prop, asn.start_point[0] + 1))

    def _check_call(self, call: Any, map_idx_vars: frozenset[str]) -> frozenset[str]:
        callee = get_node_text(call.children[0], self.bytes) if call.children else ""
        line = call.start_point[0] + 1
        if callee in {"document.write", "document.writeln"}:
            self.sinks.append((callee, line))
        elif callee.endswith(".insertAdjacentHTML"):
            self.sinks.append(("insertAdjacentHTML", line))
        if not callee.endswith(".map"):
            return map_idx_vars
        return map_idx_vars | _extract_map_index_var(call, self.bytes)


def _extract_map_index_var(call: Any, source_bytes: bytes) -> frozenset[str]:
    args = find_first_child(call, "arguments")
    cb = next((c for c in (args.children if args else ()) if c.type in {"arrow_function", "function_expression"}), None)
    params = find_first_child(cb, "formal_parameters") if cb else None
    raw_params = [c for c in (params.children if params else ()) if c.type not in {"(", ")", ","}]
    if len(raw_params) < 2:
        return frozenset()
    idx_node = raw_params[1] if raw_params[1].type == "identifier" else find_first_child(raw_params[1], "identifier")
    return frozenset({get_node_text(idx_node, source_bytes)}) if idx_node else frozenset()


def collect_ui_cst_telemetry(body_node: Any, source_bytes: bytes) -> tuple[int, list[tuple[str, int]], list[int]]:
    """Return (jsx_elements_count, dom_write_sinks, array_index_keys) for body_node."""
    if not body_node:
        return 0, [], []
    state = _UICSTState(source_bytes)

    def walk(node: Any, map_vars: frozenset[str]) -> None:
        next_vars = state.inspect(node, map_vars)
        for child in node.children:
            walk(child, next_vars)

    for child in body_node.children:
        walk(child, frozenset())
    return state.jsx_count, state.sinks, state.index_keys
