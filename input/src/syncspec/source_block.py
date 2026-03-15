from typing import Union, Tuple
from src.syncspec.error import Error
from src.syncspec.node import Node
from src.syncspec.string import String
from src.syncspec.block import Block
from src.syncspec.source_block_context import SourceBlockContext


def make_source_block(context: SourceBlockContext):
    def source_block(block: Block) -> Union[Tuple[String, Node], Block, Error]:
        directive = block.directive

        if "source" not in directive:
            return block

        source_key = directive["source"]
        if not isinstance(source_key, str):
            return Error("Directive 'source' must be a string", block.name, block.line_number)

        # Construct String text
        s_text = (
            context.open_delimiter
            + block.prefix
            + context.close_delimiter
            + block.text
            + context.open_delimiter
            + block.suffix
            + context.close_delimiter
        )
        string_obj = String(text=s_text, line_number=block.line_number, name=block.name)

        # Process content for state
        processed_text = block.text
        lines = processed_text.splitlines(keepends=True)

        # Handle head
        if "head" in directive:
            h = directive["head"]
            if not isinstance(h, int) or len(lines) < h:
                return Error(f"Cannot remove {h} lines from head", block.name, block.line_number)
            lines = lines[h:]

        # Handle tail
        if "tail" in directive:
            t = directive["tail"]
            if not isinstance(t, int) or len(lines) < t:
                return Error(f"Cannot remove {t} lines from tail", block.name, block.line_number)
            lines = lines[:-t] if t > 0 else lines

        processed_text = "".join(lines)
        context.state[source_key] = processed_text

        # Construct Node
        node_obj = Node(
            directive_type="source",
            key=source_key,
            line_number=block.line_number,
            name=block.name,
        )

        return (string_obj, node_obj)

    return source_block