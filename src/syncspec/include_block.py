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
        if not isinstance(key, str):
            return Error(
                message=f"Include key must be a string, got {type(key).__name__}",
                name=block.name,
                line_number=block.line_number
            )

        if key not in context.state:
            return Error(
                message=f"Include key '{key}' not found in state",
                name=block.name,
                line_number=block.line_number
            )

        value = context.state[key]
        text = (
            context.open_delimiter + block.prefix + context.close_delimiter +
            str(value) +
            context.open_delimiter + block.suffix + context.close_delimiter
        )
        return String(text=text, line_number=block.line_number, name=block.name)

    return include_block