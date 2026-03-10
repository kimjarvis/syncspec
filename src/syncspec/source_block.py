from typing import Union
from .string import String
from .block import Block
from .source_block_context import SourceBlockContext

def make_source_block(context: SourceBlockContext):
    def source_block(block: Block) -> Union[String, Block]:
        if "source" in block.directive:
            key = block.directive["source"]
            context.state[key] = block.text
            prefix = block.prefix or ""
            text = (
                context.open_delimiter +
                prefix +
                context.close_delimiter +
                block.text +
                context.open_delimiter +
                block.suffix +
                context.close_delimiter
            )
            return String(text=text, line_number=block.line_number)
        return block
    return source_block