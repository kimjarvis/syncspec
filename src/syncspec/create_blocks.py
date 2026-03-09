import json
from typing import Union, Dict, Any
from src.syncspec.fragment import Fragment
from src.syncspec.string import String
from src.syncspec.block import Block
from src.syncspec.error import Error
from src.syncspec.create_blocks_context import CreateBlocksContext


def make_create_blocks(context: CreateBlocksContext):
    def create_blocks(fragment: Fragment) -> Union[String, Block, Error, None]:
        state = context.index % 4
        context.index += 1

        if state == 0:
            return String(text=fragment.text, line_number=fragment.line_number)
        elif state == 1:
            context.top_directive = fragment.text
            context.line_number = fragment.line_number
            return None
        elif state == 2:
            context.text = fragment.text
            return None
        elif state == 3:
            combined = "{ " + context.top_directive + " " + fragment.text + " }"
            try:
                directive = json.loads(combined)
                return Block(
                    directive=directive,
                    combined_directives=combined,
                    text=context.text,
                    line_number=context.line_number
                )
            except json.JSONDecodeError:
                return Error(
                    message=f"Invalid JSON in directive: {combined}",
                    name=context.name,
                    line_number=context.line_number
                )
        return None

    return create_blocks