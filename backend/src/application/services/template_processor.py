"""Custom Handlebars-like template processor.

Supports: {{var}}, {{#if}}, {{#each}}, {{#unless}}, {{@adr_number}}, {{@next_adr}},
{{@integration_branch}}, {{@last}}, {{this}}, <!-- AI:INIT/ONGOING --> preservation.
"""

import re
from dataclasses import dataclass
from typing import Any

# ── AST Nodes ──


@dataclass
class TextNode:
    text: str


@dataclass
class VarNode:
    path: str


@dataclass
class IfNode:
    condition: "Condition"
    body: list
    else_body: list


@dataclass
class EachNode:
    path: str
    body: list


@dataclass
class UnlessNode:
    condition: "Condition"
    body: list


# ── Conditions ──


@dataclass
class TruthyCondition:
    path: str


@dataclass
class EqCondition:
    path: str
    value: str


@dataclass
class NeqCondition:
    path: str
    value: str


@dataclass
class NotEmptyCondition:
    path: str


Condition = TruthyCondition | EqCondition | NeqCondition | NotEmptyCondition
Node = TextNode | VarNode | IfNode | EachNode | UnlessNode

# ── Tokenizer ──

_TAG_RE = re.compile(r"\{\{(.*?)\}\}", re.DOTALL)


def tokenize(template: str) -> list[tuple[str, str]]:
    tokens: list[tuple[str, str]] = []
    pos = 0
    for m in _TAG_RE.finditer(template):
        if m.start() > pos:
            tokens.append(("TEXT", template[pos : m.start()]))
        tag = m.group(1).strip()
        if tag.startswith("#if "):
            tokens.append(("IF_OPEN", tag[4:].strip()))
        elif tag == "/if":
            tokens.append(("IF_CLOSE", ""))
        elif tag.startswith("#each "):
            tokens.append(("EACH_OPEN", tag[6:].strip()))
        elif tag == "/each":
            tokens.append(("EACH_CLOSE", ""))
        elif tag.startswith("#unless "):
            tokens.append(("UNLESS_OPEN", tag[8:].strip()))
        elif tag == "/unless":
            tokens.append(("UNLESS_CLOSE", ""))
        elif tag == "else":
            tokens.append(("ELSE", ""))
        else:
            tokens.append(("VAR", tag))
        pos = m.end()
    if pos < len(template):
        tokens.append(("TEXT", template[pos:]))
    return tokens


# ── Parser ──


def parse_condition(expr: str) -> Condition:
    if " == " in expr:
        path, value = expr.split(" == ", 1)
        return EqCondition(path.strip(), value.strip())
    if " != " in expr:
        path, value = expr.split(" != ", 1)
        return NeqCondition(path.strip(), value.strip())
    if " is not empty" in expr:
        path = expr.replace(" is not empty", "").strip()
        return NotEmptyCondition(path)
    return TruthyCondition(expr.strip())


def parse(tokens: list[tuple[str, str]], pos: int = 0) -> tuple[list[Node], int]:
    nodes: list[Node] = []
    while pos < len(tokens):
        ttype, content = tokens[pos]

        if ttype == "TEXT":
            nodes.append(TextNode(content))
            pos += 1

        elif ttype == "VAR":
            nodes.append(VarNode(content))
            pos += 1

        elif ttype == "IF_OPEN":
            condition = parse_condition(content)
            pos += 1
            body, pos = parse(tokens, pos)
            else_body: list[Node] = []
            if pos < len(tokens) and tokens[pos][0] == "ELSE":
                pos += 1
                else_body, pos = parse(tokens, pos)
            if pos < len(tokens) and tokens[pos][0] == "IF_CLOSE":
                pos += 1
            nodes.append(IfNode(condition, body, else_body))

        elif ttype == "EACH_OPEN":
            pos += 1
            body, pos = parse(tokens, pos)
            if pos < len(tokens) and tokens[pos][0] == "EACH_CLOSE":
                pos += 1
            nodes.append(EachNode(content, body))

        elif ttype == "UNLESS_OPEN":
            condition = parse_condition(content)
            pos += 1
            body, pos = parse(tokens, pos)
            if pos < len(tokens) and tokens[pos][0] == "UNLESS_CLOSE":
                pos += 1
            nodes.append(UnlessNode(condition, body))

        elif ttype in ("IF_CLOSE", "EACH_CLOSE", "UNLESS_CLOSE", "ELSE"):
            break

        else:
            pos += 1

    return nodes, pos


# ── Evaluator ──


class TemplateProcessor:
    def __init__(self) -> None:
        self._adr_counter: int = 2

    def render(self, template: str, context: dict[str, Any]) -> str:
        self._adr_counter = 2
        tokens = tokenize(template)
        nodes, _ = parse(tokens)
        result = self._eval_nodes(nodes, context)
        return self._post_process(result)

    # ── Internal ──

    def _eval_nodes(self, nodes: list[Node], context: dict[str, Any]) -> str:
        return "".join(self._eval_node(n, context) for n in nodes)

    def _eval_node(self, node: Node, context: dict[str, Any]) -> str:
        if isinstance(node, TextNode):
            return node.text
        if isinstance(node, VarNode):
            return self._resolve_var(node.path, context)
        if isinstance(node, IfNode):
            if self._eval_condition(node.condition, context):
                return self._eval_nodes(node.body, context)
            return self._eval_nodes(node.else_body, context)
        if isinstance(node, EachNode):
            return self._eval_each(node, context)
        if isinstance(node, UnlessNode):
            if not self._eval_condition(node.condition, context):
                return self._eval_nodes(node.body, context)
            return ""
        return ""

    def _resolve_var(self, path: str, context: dict[str, Any]) -> str:
        if path == "@adr_number":
            num = self._adr_counter
            self._adr_counter += 1
            return f"{num:03d}"
        if path == "@next_adr":
            return f"{self._adr_counter:03d}"
        if path == "@integration_branch":
            strategy = self._resolve_path("git.branch_strategy", context)
            return "develop" if strategy in ("master_develop_task", "gitflow") else "main"
        if path == "this":
            val = context.get("this", "")
            return str(val).rstrip("\n") if isinstance(val, str) else str(val)

        value = self._resolve_path(path, context)
        if value is None:
            return ""
        if isinstance(value, str):
            return value.rstrip("\n")
        return str(value)

    def _resolve_path(self, path: str, context: dict[str, Any]) -> Any:
        parts = path.split(".")
        current: Any = context
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                return None
            if current is None:
                return None
        return current

    def _eval_condition(self, cond: Condition, ctx: dict[str, Any]) -> bool:
        if isinstance(cond, EqCondition):
            value = self._resolve_path(cond.path, ctx)
            if value is None:
                return False
            return str(value).strip() == cond.value

        if isinstance(cond, NeqCondition):
            value = self._resolve_path(cond.path, ctx)
            if value is None:
                return True
            return str(value).strip() != cond.value

        if isinstance(cond, NotEmptyCondition):
            value = self._resolve_path(cond.path, ctx)
            return self._is_truthy(value)

        # TruthyCondition
        value = self._resolve_path(cond.path, ctx)
        return self._is_truthy(value)

    @staticmethod
    def _is_truthy(value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return len(value.strip()) > 0
        if isinstance(value, (list, dict)):
            return len(value) > 0
        return bool(value)

    def _eval_each(self, node: EachNode, context: dict[str, Any]) -> str:
        items = self._resolve_path(node.path, context)
        if not items or not isinstance(items, list):
            return ""

        parts: list[str] = []
        for i, item in enumerate(items):
            loop_ctx = dict(context)
            loop_ctx["@last"] = i == len(items) - 1
            loop_ctx["@first"] = i == 0
            loop_ctx["@index"] = i

            if isinstance(item, dict):
                if "engine" in item:
                    loop_ctx["db"] = item
                elif "name" in item and "type" in item:
                    loop_ctx["service"] = item
                else:
                    loop_ctx.update(item)
                loop_ctx["this"] = item
            else:
                loop_ctx["this"] = item

            parts.append(self._eval_nodes(node.body, loop_ctx))

        return "".join(parts)

    @staticmethod
    def _post_process(text: str) -> str:
        text = re.sub(r"(GET|POST|PUT|DELETE|PATCH)\s{2,}/", r"\1 /", text)
        text = re.sub(r"\n{4,}", "\n\n\n", text)
        return text
