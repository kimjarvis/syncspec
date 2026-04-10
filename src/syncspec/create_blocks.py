import logging
from typing import Union, Tuple

from syncspec.context import Context
from syncspec.block import Block
from syncspec.indexedfragment import IndexedFragment
from syncspec.text import Text
from syncspec.stop import Stop
from syncspec.utilities import format_log_message


def make_create_blocks(context: Context):
    state = {'block': None, 'last': False}

    def create_blocks(fragment: IndexedFragment) -> Union[Text, Tuple[Block, Text], Stop, None]:
        if state["last"] and fragment.index % 4 != 0:
            logging.error(
                format_log_message("Unexpected fragment index after last marker", fragment.path, fragment.line_number))
            return Stop()

        mod = fragment.index % 4
        if mod == 0:
            txt = Text(path=fragment.path, text=fragment.text, line_number=fragment.line_number)
            return txt if fragment.index == 0 else (state["block"], txt)

        if mod == 1:
            state["block"] = Block(
                prefix=fragment.text, prefix_line_number=fragment.line_number, path=fragment.path,
                text="", text_line_number=0, suffix="", suffix_line_number=0
            )
            return None
        if mod == 2:
            state["block"].text = fragment.text
            state["block"].text_line_number = fragment.line_number
            state["block"].path = fragment.path
            return None
        if mod == 3:
            state["block"].suffix = fragment.text
            state["block"].suffix_line_number = fragment.line_number
            state["block"].path = fragment.path
            return None

        return None

    return create_blocks