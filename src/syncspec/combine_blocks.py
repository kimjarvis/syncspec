from src.syncspec.stop import Stop
from src.syncspec.block import Block
from src.syncspec.combine_blocks_context import CombineBlocksContext

def make_combine_blocks(context: CombineBlocksContext):
    def combine_blocks(block: Block) -> Stop:
        if isinstance(block, Block):
            if block.prefix is None:
                context.text += block.text
            else:
                context.text += (
                    context.open_delimiter
                    + block.prefix
                    + context.close_delimiter
                    + block.text
                    + context.open_delimiter
                    + block.suffix
                    + context.close_delimiter
                )
            return Stop(message="stopping")
        return block
    return combine_blocks