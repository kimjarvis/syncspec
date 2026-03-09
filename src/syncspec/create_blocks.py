from typing import Union
from src.syncspec.fragment import Fragment
from src.syncspec.string import String
from src.syncspec.block import Block
from src.syncspec.create_blocks_context import CreateBlocksContext


def make_create_blocks(context: CreateBlocksContext):
    def create_blocks(fragment: Fragment) -> Union[String, Block, None]:
        state = context.index % 4

        if state == 0:
            context.index += 1
            return String(text=fragment.text, line_number=fragment.line_number)

        elif state == 1:
            context.top_directive = fragment.text
            context.line_number = fragment.line_number
            context.index += 1
            return None

        elif state == 2:
            context.text = fragment.text
            context.index += 1
            return None

        elif state == 3:
            block_text = context.top_directive + fragment.text
            context.index += 1
            return Block(text=block_text, line_number=context.line_number)

    return create_blocks