"""TypeScript type-escape, syntax error, and ECMAScript smell detectors."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from _code_health.js_parser import _get_node_text


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

    def walk_escapes(self, node: Any, bytes_: bytes) -> None:
        """Recursively count explicit any, @ts-ignore, and non-null escapes in a subtree."""
        _scan_type_escape(node, bytes_, self.types)
        for c in node.children:
            self.walk_escapes(c, bytes_)

    def scan_header(self, fn_node: Any, body: Any, bytes_: bytes, lines: list[str]) -> None:
        """Scan signature types and preceding comment directives for a function."""
        if body and body != fn_node:
            for c in fn_node.children:
                if c.type in {"formal_parameters", "type_parameters", "type_annotation"}:
                    self.walk_escapes(c, bytes_)
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


def collect_syntax_errors(root: Any) -> list[int]:
    """Collect sorted 1-based line numbers for all CST error/missing nodes."""
    if not root.has_error:
        return []
    lines: list[int] = []
    stack = [root]
    while stack:
        n = stack.pop()
        if n.is_error or n.is_missing or n.type == "ERROR":
            lines.append(n.start_point[0] + 1)
        else:
            stack.extend(reversed(n.children))
    return sorted(set(lines)) or [1]


def count_unclaimed_ts_ignores(root: Any, bytes_: bytes, claimed: set[int]) -> int:
    """Count @ts-ignore/@ts-nocheck comments anywhere in the CST outside claimed functions."""
    lines: set[int] = set()
    stack = [root]
    while stack:
        n = stack.pop()
        if n.type == "comment":
            ln = n.start_point[0] + 1
            if ln not in claimed:
                txt = _get_node_text(n, bytes_)
                if "@ts-ignore" in txt or "@ts-nocheck" in txt:
                    lines.add(ln)
        else:
            stack.extend(n.children)
    return len(lines)
