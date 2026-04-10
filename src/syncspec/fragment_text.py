import logging
from typing import List, Union

from syncspec.context import Context
from syncspec.file_path import FilePath
from syncspec.fragment import Fragment
from syncspec.stop import Stop
from syncspec.utilities import format_log_message

def make_fragment_text(context: Context):
    open_delim = context.open_delimiter
    close_delim = context.close_delimiter

    def fragment_text(fact: FilePath) -> Union[List[Fragment], Stop]:
        text = fact.text
        path = fact.path
        logger = logging.getLogger(__name__)

        if not text:
            logger.error(format_log_message("Input text is empty", path, 1))
            return Stop()

        fragments: List[Fragment] = []
        pos = 0
        expect_open = True
        last_open_pos = 0

        while True:
            next_open = text.find(open_delim, pos)
            next_close = text.find(close_delim, pos)

            if next_open == -1 and next_close == -1:
                break

            if next_open != -1 and (next_close == -1 or next_open < next_close):
                next_type, next_pos = 'open', next_open
            else:
                next_type, next_pos = 'close', next_close

            line_num = 1 + text[:pos].count('\n')

            if expect_open:
                if next_type == 'close':
                    logger.error(format_log_message("First delimiter must be open delimiter", path, line_num))
                    return Stop()
                last_open_pos = pos
                fragments.append(Fragment(path=path, text=text[pos:next_pos], line_number=line_num))
                pos = next_pos + len(open_delim)
                expect_open = False
            else:
                if next_type == 'open':
                    logger.error(format_log_message("Unexpected open delimiter (nesting or mismatch)", path, line_num))
                    return Stop()
                fragments.append(Fragment(path=path, text=text[pos:next_pos], line_number=line_num))
                pos = next_pos + len(close_delim)
                expect_open = True

        if not expect_open:
            line_num = 1 + text[:last_open_pos].count('\n')
            logger.error(format_log_message("Unmatched open delimiter", path, line_num))
            return Stop()

        # Append trailing fragment (covers empty string after final delimiter)
        line_num = 1 + text[:pos].count('\n')
        fragments.append(Fragment(path=path, text=text[pos:], line_number=line_num))

        return fragments

    return fragment_text