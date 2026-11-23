"""Single-pass compact token stream extraction and generated-code filtering."""

from __future__ import annotations

import ast
from array import array
from bisect import bisect_left, bisect_right
from dataclasses import dataclass, field
import fnmatch
import io
import keyword
import re
import tokenize
from typing import Any

from _code_health.dry_models import BlockSpan, FileTokenStream, PyTokenMeta
from _code_health.ir_models import IRModule

TOK_ID = 1
TOK_NUM = 2
TOK_STR = 3
TOK_BOOL = 4
TOK_STMT = 5

KIND_STRUCT = 0
KIND_IDENT = 1
KIND_LITERAL = 2

_RESERVED_OFFSET = 16
_GENERATED_MARKERS = re.compile(
    r"(?:^|[\s/*#])@generated\b|\b(?:do\s+not\s+edit|auto-?generated|automatically\s+generated|code\s+generated\s+by|generated\s+by)\b",
    re.IGNORECASE,
)
_GENERATED_SUFFIXES = ("_pb2.py", "_pb2_grpc.py")
_GENERATED_NAME_PARTS = (".generated.", ".gen.", "_pb.", ".pb.")
_PY_TRIVIA = frozenset({
    tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT,
    tokenize.COMMENT, tokenize.ENCODING, tokenize.ENDMARKER,
})
_PY_FSTRING_TOKS = frozenset(
    tok for name in ("FSTRING_START", "FSTRING_MIDDLE", "FSTRING_END")
    if (tok := getattr(tokenize, name, -1)) != -1
)
_PY_BOOL_LITERALS = frozenset({"True", "False", "None"})

_CST_SKIP_ALWAYS = frozenset({
    "comment", "line_comment", "block_comment",
    "package_declaration", "import_declaration", "import_statement",
    "interface_declaration", "type_alias_declaration", "type_annotation",
    "type_parameters", "type_arguments", "ambient_declaration", "implements_clause",
})
_CST_TS_EXPORT_SKIP = frozenset({"interface_declaration", "type_alias_declaration", "ambient_declaration", "type"})
_CST_STMT_NODES = frozenset({
    "expression_statement", "return_statement", "lexical_declaration",
    "variable_declaration", "local_variable_declaration", "if_statement",
    "for_statement", "for_in_statement", "for_of_statement", "enhanced_for_statement",
    "while_statement", "do_statement", "switch_statement", "try_statement",
    "throw_statement", "break_statement", "continue_statement", "assert_statement",
})
_CST_IDENT_NODES = frozenset({
    "identifier", "property_identifier", "shorthand_property_identifier",
    "shorthand_property_identifier_pattern", "private_property_identifier", "type_identifier",
})
_CST_STR_NODES = frozenset({"string", "string_literal", "character_literal", "string_fragment"})
_CST_NUM_NODES = frozenset({
    "number", "decimal_integer_literal", "hex_integer_literal", "octal_integer_literal",
    "binary_integer_literal", "decimal_floating_point_literal", "hex_floating_point_literal",
})
_CST_BOOL_NODES = frozenset({"true", "false", "null", "null_literal", "undefined", "none"})
_CST_LEAF_CLASSES: tuple[tuple[frozenset[str], int, int], ...] = (
    (_CST_STR_NODES, TOK_STR, KIND_LITERAL),
    (_CST_NUM_NODES, TOK_NUM, KIND_LITERAL),
    (_CST_BOOL_NODES, TOK_BOOL, KIND_LITERAL),
    (_CST_IDENT_NODES, TOK_ID, KIND_IDENT),
)


class TokenInterner:
    """Deterministic per-scan string-to-uint32 lexeme interner."""

    def __init__(self, exclude_globs: tuple[str, ...] = ()) -> None:
        self.exclude_globs = exclude_globs
        self._table: dict[str, int] = {}

    def intern(self, lexeme: str) -> int:
        """Return a stable integer ID (>= 16) for lexeme."""
        existing = self._table.get(lexeme)
        if existing is not None:
            return existing
        new_id = _RESERVED_OFFSET + len(self._table)
        self._table[lexeme] = new_id
        return new_id


def _has_generated_header(head_lines: list[str]) -> bool:
    for raw in head_lines[:15]:
        stripped = raw.strip()
        if stripped.startswith(("#", "//", "/*", "*")) and _GENERATED_MARKERS.search(stripped):
            return True
    return False


def is_generated_source(
    file_path: str,
    head_lines: list[str],
    annotations: tuple[str, ...] = (),
    exclude_globs: tuple[str, ...] = (),
) -> bool:
    """Return True when file matches standard generated-code markers, suffixes, or globs."""
    norm = file_path.replace("\\", "/")
    fname = norm.rsplit("/", 1)[-1].lower()
    has_suffix = fname.endswith(_GENERATED_SUFFIXES) or any(part in fname for part in _GENERATED_NAME_PARTS)
    has_glob = any(fnmatch.fnmatch(norm, pat) for pat in exclude_globs)
    has_ann = any(ann.split(".")[-1] == "Generated" for ann in annotations)
    return has_suffix or has_glob or has_ann or _has_generated_header(head_lines)


@dataclass
class _StreamBuf:
    """Mutable typed-array buffer assembling a compact FileTokenStream."""

    interner: TokenInterner
    exact: array[int] = field(default_factory=lambda: array("I"))
    norm: array[int] = field(default_factory=lambda: array("I"))
    lines: array[int] = field(default_factory=lambda: array("I"))
    kinds: array[int] = field(default_factory=lambda: array("B"))
    stmts: array[int] = field(default_factory=lambda: array("I"))

    def append(self, lexeme: str, norm_id: int, kind: int, line: int) -> None:
        """Append one classified token to all parallel typed arrays."""
        eid = self.interner.intern(lexeme)
        self.exact.append(eid)
        self.norm.append(eid if norm_id == 0 else norm_id)
        self.kinds.append(kind)
        self.lines.append(line)

    def mark_stmt(self, idx: int) -> None:
        """Record an executable statement start offset if not already recorded."""
        if not self.stmts or self.stmts[-1] != idx:
            self.stmts.append(idx)

    def to_stream(self, stream_meta: tuple[str, str, bool, int], blocks: tuple[BlockSpan, ...]) -> FileTokenStream:
        """Freeze collected arrays into an immutable FileTokenStream."""
        path, lang, is_test, loc = stream_meta
        return FileTokenStream(path, lang, is_test, loc, self.exact, self.norm, self.lines, self.kinds, self.stmts, blocks)


def _node_span(node: ast.AST) -> tuple[int, int, int, int]:
    ln, col = getattr(node, "lineno", 0), getattr(node, "col_offset", 0)
    return (ln, col, getattr(node, "end_lineno", ln), getattr(node, "end_col_offset", col))


def _add_span(table: dict[int, list[tuple[int, int, int, int]]], span: tuple[int, int, int, int]) -> None:
    for ln in range(span[0], span[2] + 1):
        table.setdefault(ln, []).append(span)


def _in_spans(pos: tuple[int, int], spans: dict[int, list[tuple[int, int, int, int]]]) -> bool:
    line_spans = spans.get(pos[0])
    return bool(line_spans) and any((s_ln, s_col) <= pos < (e_ln, e_col) for s_ln, s_col, e_ln, e_col in line_spans)


@dataclass
class _PyMaskAccumulator:
    """Collects Python AST skip lines, annotation spans, and statement positions."""

    skip_lines: set[int] = field(default_factory=set)
    ann_spans: dict[int, list[tuple[int, int, int, int]]] = field(default_factory=dict)
    full_skip: dict[int, list[tuple[int, int, int, int]]] = field(default_factory=dict)
    stmt_pos: list[tuple[int, int]] = field(default_factory=list)

    def collect(self, tree: ast.Module) -> None:
        """Populate mask collections by walking a parsed Python module."""
        for node in ast.walk(tree):
            if not self._skip_non_exec(node):
                self._record_ann(node)
                self._record_stmt(node)
        self.stmt_pos = sorted(set(self.stmt_pos))

    def _skip_non_exec(self, node: ast.AST) -> bool:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            self.skip_lines.update(range(node.lineno, getattr(node, "end_lineno", node.lineno) + 1))
            return True
        if isinstance(node, ast.Expr) and isinstance(getattr(node.value, "value", None), str):
            self.skip_lines.update(range(node.lineno, getattr(node, "end_lineno", node.lineno) + 1))
            return True
        return False

    def _record_ann(self, node: ast.AST) -> None:
        ann = getattr(node, "returns", None) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) else getattr(node, "annotation", None)
        if ann is None:
            return
        if isinstance(node, ast.AnnAssign) and node.value is None:
            _add_span(self.full_skip, _node_span(node))
        else:
            _add_span(self.ann_spans, _node_span(ann))

    def _record_stmt(self, node: ast.AST) -> None:
        if isinstance(node, ast.stmt) and not isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            self.stmt_pos.append((node.lineno, node.col_offset))


def _raw_py_tokens(raw_text: str, acc: _PyMaskAccumulator) -> list[tuple[int, str, tuple[int, int]]]:
    toks: list[tuple[int, str, tuple[int, int]]] = []
    try:
        for tok in tokenize.generate_tokens(io.StringIO(raw_text).readline):
            if tok.type not in _PY_TRIVIA and tok.start[0] not in acc.skip_lines and not _in_spans(tok.start, acc.full_skip):
                toks.append((tok.type, tok.string, tok.start))
    except tokenize.TokenError:
        return toks
    return toks


def _classify_py_token(t_type: int, t_str: str) -> tuple[int, int]:
    if t_type == tokenize.NAME:
        if t_str in _PY_BOOL_LITERALS:
            return TOK_BOOL, KIND_LITERAL
        return (0, KIND_STRUCT) if keyword.iskeyword(t_str) else (TOK_ID, KIND_IDENT)
    if t_type == tokenize.NUMBER:
        return TOK_NUM, KIND_LITERAL
    return (TOK_STR, KIND_LITERAL) if (t_type == tokenize.STRING or t_type in _PY_FSTRING_TOKS) else (0, KIND_STRUCT)


def _is_skipped_py_ann(toks: list[tuple[int, str, tuple[int, int]]], idx: int, acc: _PyMaskAccumulator) -> bool:
    t_type, t_str, start = toks[idx]
    if _in_spans(start, acc.ann_spans):
        return True
    return t_type == tokenize.OP and t_str in {":", "->"} and idx + 1 < len(toks) and _in_spans(toks[idx + 1][2], acc.ann_spans)


def _populate_py_stream(toks: list[tuple[int, str, tuple[int, int]]], acc: _PyMaskAccumulator, buf: _StreamBuf) -> None:
    stmt_idx = 0
    for i, (t_type, t_str, start) in enumerate(toks):
        if _is_skipped_py_ann(toks, i, acc):
            continue
        while stmt_idx < len(acc.stmt_pos) and start >= acc.stmt_pos[stmt_idx]:
            buf.mark_stmt(len(buf.exact))
            stmt_idx += 1
        norm_id, kind = _classify_py_token(t_type, t_str)
        buf.append(t_str, norm_id, kind, start[0])


def _map_block_spans(lines: array[int], stmts: array[int], bounds: tuple[tuple[str, int, int, int], ...]) -> tuple[BlockSpan, ...]:
    blocks: list[BlockSpan] = []
    for symbol, s_ln, e_ln, loc in bounds:
        s_tok = bisect_left(lines, s_ln)
        e_tok = bisect_right(lines, e_ln)
        s_cnt = bisect_right(stmts, max(0, e_tok - 1)) - bisect_left(stmts, s_tok)
        blocks.append(BlockSpan(symbol, s_tok, e_tok, s_ln, e_ln, loc, max(0, s_cnt)))
    return tuple(blocks)


def extract_python_tokens(
    tree: ast.Module, raw_text: str, meta: PyTokenMeta, interner: TokenInterner
) -> FileTokenStream | None:
    """Extract compact normalized token stream from a Python AST and source text."""
    if is_generated_source(meta.rel_path, raw_text.splitlines()[:15], exclude_globs=interner.exclude_globs):
        return None
    acc = _PyMaskAccumulator()
    acc.collect(tree)
    buf = _StreamBuf(interner)
    _populate_py_stream(_raw_py_tokens(raw_text, acc), acc, buf)
    if not buf.exact:
        return None
    blocks = _map_block_spans(buf.lines, buf.stmts, meta.block_bounds)
    return buf.to_stream((meta.rel_path, "python", meta.is_test, meta.loc), blocks)


class _CSTWalker:
    """Iterative Tree-Sitter CST walker populating a compact FileTokenStream buffer."""

    def __init__(self, source_bytes: bytes, buf: _StreamBuf, is_ts: bool) -> None:
        self.bytes = source_bytes
        self.buf = buf
        self.is_ts = is_ts

    def walk(self, root: Any) -> None:
        """Traverse root subtree iteratively, skipping non-executable declarations."""
        stack: list[Any] = [root]
        while stack:
            self._step_node(stack.pop(), stack)

    def _step_node(self, node: Any, stack: list[Any]) -> None:
        if self._should_skip(node):
            return
        if node.type in _CST_STMT_NODES:
            self.buf.mark_stmt(len(self.buf.exact))
        if self._is_atomic_leaf(node):
            self._emit_leaf(node)
        elif self.is_ts and node.type in {"as_expression", "satisfies_expression"} and node.children:
            stack.append(node.children[0])
        else:
            stack.extend(reversed(node.children))

    def _is_atomic_leaf(self, node: Any) -> bool:
        if node.type == "template_string":
            return not any(c.type == "template_substitution" for c in node.children)
        return node.child_count == 0 or node.type in _CST_STR_NODES

    def _should_skip(self, node: Any) -> bool:
        t = node.type
        if t in _CST_SKIP_ALWAYS:
            return True
        return self.is_ts and t == "export_statement" and any(c.type in _CST_TS_EXPORT_SKIP for c in node.children)

    def _emit_leaf(self, node: Any) -> None:
        txt = self.bytes[node.start_byte : node.end_byte].decode("utf-8", errors="replace").strip()
        if not txt:
            return
        t, ln = node.type, node.start_point[0] + 1
        if t == "template_string":
            self.buf.append(txt, TOK_STR, KIND_LITERAL, ln)
            return
        for node_set, norm_id, kind in _CST_LEAF_CLASSES:
            if t in node_set:
                self.buf.append(txt, norm_id, kind, ln)
                return
        self.buf.append(txt, 0, KIND_STRUCT, ln)


def _collect_nested_cst_bounds(root: Any, existing: set[tuple[int, int]]) -> list[tuple[str, int, int, int]]:
    out: list[tuple[str, int, int, int]] = []
    stack: list[tuple[Any, str]] = [(root, "")]
    while stack:
        node, cls_prefix = stack.pop()
        t = node.type
        if t == "class_declaration":
            ident = next((c for c in node.children if c.type == "identifier"), None)
            cname = ident.text.decode("utf-8", errors="replace") if ident and getattr(ident, "text", None) else ""
            cls_prefix = f"{cls_prefix}.{cname}" if (cls_prefix and cname) else (cname or cls_prefix)
        elif t in {"method_declaration", "constructor_declaration"}:
            s_ln, e_ln = node.start_point[0] + 1, node.end_point[0] + 1
            if (s_ln, e_ln) not in existing:
                existing.add((s_ln, e_ln))
                ident = next((c for c in node.children if c.type == "identifier"), None)
                mname = ident.text.decode("utf-8", errors="replace") if ident and getattr(ident, "text", None) else "method"
                sym = f"{cls_prefix}.{mname}" if cls_prefix else mname
                out.append((sym, s_ln, e_ln, e_ln - s_ln + 1))
        for child in reversed(node.children):
            stack.append((child, cls_prefix))
    return out


def _cst_block_bounds(ir_mod: IRModule, root: Any = None) -> tuple[tuple[str, int, int, int], ...]:
    fns = list(ir_mod.functions) + [m for c in ir_mod.classes for m in c.methods]
    bounds = [(f.qualname, f.lineno, f.end_lineno, f.loc) for f in fns]
    if root is not None and ir_mod.language == "java":
        seen = {(f.lineno, f.end_lineno) for f in fns}
        bounds.extend(_collect_nested_cst_bounds(root, seen))
    return tuple(bounds)


def extract_cst_tokens(
    root: Any, source_bytes: bytes, ir_mod: IRModule, interner: TokenInterner
) -> FileTokenStream | None:
    """Extract compact normalized token stream from a Tree-Sitter CST root."""
    if ir_mod.syntax_errors or getattr(root, "has_error", False):
        return None
    head = source_bytes[:2048].decode("utf-8", errors="replace").splitlines()[:15]
    anns = tuple(a.name for c in ir_mod.classes for a in c.annotations)
    if is_generated_source(ir_mod.file_path, head, anns, interner.exclude_globs):
        return None
    bucket = "ecmascript" if ir_mod.language in {"javascript", "typescript"} else ir_mod.language
    buf = _StreamBuf(interner)
    _CSTWalker(source_bytes, buf, is_ts=(ir_mod.language == "typescript")).walk(root)
    if not buf.exact:
        return None
    blocks = _map_block_spans(buf.lines, buf.stmts, _cst_block_bounds(ir_mod, root))
    return buf.to_stream((ir_mod.file_path, bucket, ir_mod.is_test, ir_mod.loc), blocks)
