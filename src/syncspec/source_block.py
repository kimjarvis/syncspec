from typing import Union, Tuple
from src.syncspec.block import Block
from src.syncspec.string import String
from src.syncspec.node import Node
from src.syncspec.source_block_context import SourceBlockContext


def make_source_block(context: SourceBlockContext):
    def source_block(block: Block) -> Union[Tuple[String, Node], Block]:
        source_key = block.directive.get("source")

        if isinstance(source_key, str):
            context.state[source_key] = block.text

            text = (
                    context.open_delimiter + block.prefix + context.close_delimiter +
                    block.text +
                    context.open_delimiter + block.suffix + context.close_delimiter
            )
            string_obj = String(text=text, line_number=block.line_number, name=block.name)
            node_obj = Node(directive_type="source", key=source_key, line_number=block.line_number, name=block.name)

            return string_obj, node_obj

        return block

    return source_block