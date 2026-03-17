import logging
from typing import Union, Tuple

from src.syncspec.node import Node
from src.syncspec.utilities import format_error
from src.syncspec.string import String
from src.syncspec.block import Block
from src.syncspec.include_block_context import IncludeBlockContext


def make_include_block(context: IncludeBlockContext):
    def include_block(block: Block) -> Union[Tuple[String, Node], Block, String]:
        def return_error(msg: str) -> String:
            logging.error(format_error(msg, block.name, block.line_number))
            return String(
                text=context.open_delimiter + block.prefix + context.close_delimiter +
                     block.text +
                     context.open_delimiter + block.suffix + context.close_delimiter,
                line_number=block.line_number,
                name=block.name
            )

        if "include" not in block.directive:
            return block

        key = block.directive["include"]
        if not isinstance(key, str):
            return return_error("'include' directive must be a string")

        if key not in context.state:
            return return_error(f"include key '{key}' not found in context")

        v = context.state[key]
        if not isinstance(v, str):
            return return_error(f"value for key '{key}' must be a string")

        head = block.directive.get("head", 0)
        tail = block.directive.get("tail", 0)

        if isinstance(head, bool) or not isinstance(head, int) or head < 0:
            return return_error("'head' must be a non-negative integer")
        if isinstance(tail, bool) or not isinstance(tail, int) or tail < 0:
            return return_error("'tail' must be a non-negative integer")

        lines = block.text.splitlines(keepends=True)
        total_lines = len(lines)

        if head + tail > total_lines:
            return return_error(f"head ({head}) + tail ({tail}) exceeds total lines ({total_lines})")

        top = "".join(lines[:head])
        bottom = "".join(lines[-tail:]) if tail > 0 else ""

        s_text = (
            context.open_delimiter + block.prefix + context.close_delimiter +
            top + v + bottom +
            context.open_delimiter + block.suffix + context.close_delimiter
        )

        s_obj = String(text=s_text, line_number=block.line_number, name=block.name)
        n_obj = Node(directive_type="include", key=key, line_number=block.line_number, name=block.name)

        return s_obj, n_obj

    return include_block