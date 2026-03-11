from typing import Union
from src.syncspec.string import String
from src.syncspec.block import Block
from src.syncspec.source_block_context import SourceBlockContext


def make_source_block(context: SourceBlockContext):
    def source_block(block: Block) -> Union[String, Block]:
        if "source" in block.directive:
            key = block.directive["source"]
            context.state[key] = block.text

            text = (
                    context.open_delimiter + block.prefix + context.close_delimiter +
                    block.text +
                    context.open_delimiter + block.suffix + context.close_delimiter
            )
            return String(text=text, line_number=block.line_number, name=block.name)

        return block

    return source_block