from typing import Union, Dict, Any
from .block import Block
from .source import Source
from .source_block_context import SourceBlockContext

def make_source_block(context: SourceBlockContext):
    def create_blocks(block: Block) -> Union[Source, Block]:
        if "source" in block.directive:
            value = block.directive["source"]
            context.state[value] = block.text
            return Source(
                directive=block.directive,
                text=block.text,
                line_number=block.line_number
            )
        return block
    return create_blocks