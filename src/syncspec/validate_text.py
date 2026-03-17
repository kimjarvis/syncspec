import logging
from typing import Union

from src.syncspec.text import Text
from src.syncspec.validated_text import ValidatedText
from src.syncspec.string import String
from src.syncspec.utilities import format_error
from src.syncspec.validate_text_context import ValidateTextContext


def make_validate_text(context: ValidateTextContext):
    def validate_text(text_obj: Text) -> Union[ValidatedText, String]:
        text = text_obj.text
        name = text_obj.name
        start_line = context.line_number

        # Update context line_number for subsequent calls
        # Empty text represents one logical line
        if not text:
            context.line_number += 1
        else:
            context.line_number += len(text.splitlines(keepends=True))

        open_d = context.open_delimiter
        close_d = context.close_delimiter
        len_open = len(open_d)
        len_close = len(close_d)

        pos = 0
        depth = 0
        pairs = 0
        last_close_line = start_line

        while pos < len(text):
            idx_open = text.find(open_d, pos)
            idx_close = text.find(close_d, pos)

            next_idx = -1
            is_open = False

            if idx_open == -1 and idx_close == -1:
                break
            elif idx_open == -1:
                next_idx = idx_close
                is_open = False
            elif idx_close == -1:
                next_idx = idx_open
                is_open = True
            else:
                if idx_open < idx_close:
                    next_idx = idx_open
                    is_open = True
                else:
                    next_idx = idx_close
                    is_open = False

            # Calculate 1-based line number for the error location
            current_line = start_line + text[:next_idx].count('\n')

            if is_open:
                if depth == 1:
                    msg = "Nested open delimiter"
                    logging.error(format_error(msg, name, current_line))
                    return String(text=text, name=name, line_number=current_line)
                depth = 1
                pos = next_idx + len_open
            else:
                if depth == 0:
                    msg = "Close delimiter before open"
                    logging.error(format_error(msg, name, current_line))
                    return String(text=text, name=name, line_number=current_line)
                depth = 0
                pairs += 1
                last_close_line = current_line
                pos = next_idx + len_close

        if depth == 1:
            end_line = start_line + text.count('\n')
            msg = "Unclosed delimiter"
            logging.error(format_error(msg, name, end_line))
            return String(text=text, name=name, line_number=end_line)

        if pairs % 2 != 0:
            msg = "Odd number of delimiter pairs"
            report_line = last_close_line if pairs > 0 else start_line
            logging.error(format_error(msg, name, report_line))
            return String(text=text, name=name, line_number=report_line)

        return ValidatedText(text=text, name=name)

    return validate_text