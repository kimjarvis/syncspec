import logging
from typing import Union, Tuple

from src.syncspec.node import Node
from src.syncspec.utilities import format_error
from src.syncspec.string import String
from src.syncspec.block import Block
from src.syncspec.include_block_context import IncludeBlockContext

def make_include_block(context: IncludeBlockContext):
    def include_block(block: Block) -> Union[Tuple[String, Node], Block]:
        directive = block.directive

        if "include" not in directive:
            return block

        key = directive["include"]
        if not isinstance(key, str):
            logging.error(format_error("Include key must be a string", block.name, block.line_number))
            return block

        if key not in context.state:
            logging.error(format_error(f"Include key '{key}' not found in state", block.name, block.line_number))
            return block

        v = context.state[key]
        if not isinstance(v, str):
            logging.error(format_error(f"State value for '{key}' is not a string", block.name, block.line_number))
            return block

        head = directive.get("head", 0)
        if isinstance(head, bool) or not isinstance(head, int) or head < 0:
            logging.error(format_error("Head must be a non-negative integer", block.name, block.line_number))
            return block

        tail = directive.get("tail", 0)
        if isinstance(tail, bool) or not isinstance(tail, int) or tail < 0:
            logging.error(format_error("Tail must be a non-negative integer", block.name, block.line_number))
            return block

        lines = block.text.splitlines(keepends=True)
        total_lines = len(lines)

        if head + tail > total_lines:
            logging.error(format_error("Head and tail overlap", block.name, block.line_number))
            return block

        top = "".join(lines[:head])
        bottom = "".join(lines[-tail:]) if tail > 0 else ""

        text = (
            context.open_delimiter +
            block.prefix +
            context.close_delimiter +
            top +
            v +
            bottom +
            context.open_delimiter +
            block.suffix +
            context.close_delimiter
        )

        string_obj = String(text=text, line_number=block.line_number, name=block.name)
        node_obj = Node(directive_type="include", key=key, line_number=block.line_number, name=block.name)

        return (string_obj, node_obj)

    return include_block