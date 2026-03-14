from typing import Union, Tuple, List, Any
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

        include_key = directive["include"]
        if not isinstance(include_key, str):
            return Error(
                message="Include directive key must be a string",
                name=block.name,
                line_number=block.line_number,
            )

        if include_key not in context.state:
            return Error(
                message=f"Include key '{include_key}' not found in state",
                name=block.name,
                line_number=block.line_number,
            )

        v = context.state[include_key]
        if not isinstance(v, str):
            return Error(
                message=f"State value for '{include_key}' must be a string",
                name=block.name,
                line_number=block.line_number,
            )

        lines: List[str] = v.splitlines()
        total_lines = len(lines)

        head = directive.get("head", 0)
        if not isinstance(head, int):
            return Error(
                message="Head value must be an integer",
                name=block.name,
                line_number=block.line_number,
            )
        if head > total_lines:
            return Error(
                message=f"Cannot remove {head} lines from {total_lines}",
                name=block.name,
                line_number=block.line_number,
            )
        lines = lines[head:]

        tail = directive.get("tail", 0)
        if not isinstance(tail, int):
            return Error(
                message="Tail value must be an integer",
                name=block.name,
                line_number=block.line_number,
            )
        if tail > len(lines):
            return Error(
                message=f"Cannot remove {tail} lines from {len(lines)}",
                name=block.name,
                line_number=block.line_number,
            )
        if tail > 0:
            lines = lines[:-tail]

        processed_v = "\n".join(lines)

        text = (
            context.open_delimiter
            + block.prefix
            + context.close_delimiter
            + processed_v
            + context.open_delimiter
            + block.suffix
            + context.close_delimiter
        )

        string_obj = String(text=text, line_number=block.line_number, name=block.name)
        node_obj = Node(
            directive_type="include",
            key=include_key,
            line_number=block.line_number,
            name=block.name,
        )

        return string_obj, node_obj

    return include_block