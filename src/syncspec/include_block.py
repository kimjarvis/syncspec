from typing import Union
from src.syncspec.error import Error
from src.syncspec.string import String
from src.syncspec.block import Block
from src.syncspec.include_block_context import IncludeBlockContext


def make_include_block(context: IncludeBlockContext):
    def include_block(block: Block) -> Union[String, Block, Error]:
        if "include" not in block.directive:
            return block

        key = block.directive["include"]
        if key not in context.state:
            return Error(
                message=f"Include key '{key}' not found in state",
                name="test",
                line_number=block.line_number
            )

        content = context.state[key]
        text = (
            context.open_delimiter +
            block.prefix +
            context.close_delimiter +
            content +
            context.open_delimiter +
            block.suffix +
            context.close_delimiter
        )
        return String(text=text, line_number=block.line_number)

    return include_block