from typing import Union, Tuple, Any, List
from src.syncspec.node import Node
from src.syncspec.error import Error
from src.syncspec.string import String
from src.syncspec.block import Block
from src.syncspec.include_block_context import IncludeBlockContext


def make_include_block(context: IncludeBlockContext):
    def include_block(block: Block) -> Union[Tuple[String, Node], Block, Error]:
        directive = block.directive

        if "include" not in directive:
            return block

        key = directive["include"]
        if not isinstance(key, str):
            return Error("Include key must be a string", block.name, block.line_number)

        if key not in context.state:
            return Error(f"Include key '{key}' not found in state", block.name, block.line_number)

        v = context.state[key]
        if not isinstance(v, str):
            return Error(f"State value for '{key}' is not a string", block.name, block.line_number)

        head = directive.get("head", 0)
        if not isinstance(head, int) or isinstance(head, bool) or head < 0:
            return Error(f"Invalid head value: {head}", block.name, block.line_number)

        tail = directive.get("tail", 0)
        if not isinstance(tail, int) or isinstance(tail, bool) or tail < 0:
            return Error(f"Invalid tail value: {tail}", block.name, block.line_number)

        lines = block.text.splitlines(keepends=True)
        if head + tail > len(lines):
            return Error(f"Head ({head}) and tail ({tail}) overlap", block.name, block.line_number)

        top = "".join(lines[:head])
        bottom = "".join(lines[-tail:]) if tail > 0 else ""

        text = (
            context.open_delimiter + block.prefix + context.close_delimiter +
            top + v + bottom +
            context.open_delimiter + block.suffix + context.close_delimiter
        )

        return (
            String(text, block.line_number, block.name),
            Node("include", key, block.line_number, block.name)
        )

    return include_block