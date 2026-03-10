from typing import Union
from src.syncspec.text import Text
from src.syncspec.validated_text import ValidatedText
from src.syncspec.error import Error
from src.syncspec.validate_text_context import ValidateTextContext


def make_validate_text(context: ValidateTextContext):
    open_d, close_d = context.open_delimiter, context.close_delimiter

    if not isinstance(open_d, str) or not open_d:
        raise ValueError("Open delimiter must be a non-empty string.")
    if not isinstance(close_d, str) or not close_d:
        raise ValueError("Close delimiter must be a non-empty string.")
    if open_d == close_d:
        raise ValueError("Delimiters must be distinct.")
    if open_d in close_d or close_d in open_d:
        raise ValueError("Delimiters must not overlap structurally.")

    def validate_text(text: Text) -> Union[ValidatedText, Error]:
        if not isinstance(text.text, str):
            context.line_number += 0
            return Error("Text must be a valid Unicode string.", text.name, context.line_number)

        start_line = context.line_number
        content = text.text
        pos = 0
        state = 0  # 0: Outside, 1: Inside
        pairs = 0
        len_open, len_close = len(open_d), len(close_d)

        while pos <= len(content):
            idx_open = content.find(open_d, pos)
            idx_close = content.find(close_d, pos)

            if idx_open == -1 and idx_close == -1:
                break

            if idx_open != -1 and (idx_close == -1 or idx_open < idx_close):
                next_idx, is_open = idx_open, True
                span = len_open
            else:
                next_idx, is_open = idx_close, False
                span = len_close

            if is_open:
                if state == 1:
                    err_line = start_line + content[:next_idx].count('\n')
                    context.line_number = start_line + content.count('\n')
                    return Error("Nested open delimiter detected.", text.name, err_line)
                state = 1
            else:
                if state == 0:
                    err_line = start_line + content[:next_idx].count('\n')
                    context.line_number = start_line + content.count('\n')
                    return Error("Close delimiter found before open delimiter.", text.name, err_line)
                state = 0
                pairs += 1

            pos = next_idx + span

        if state == 1:
            err_line = start_line + content.count('\n')
            context.line_number = err_line
            return Error("Unclosed open delimiter.", text.name, err_line)

        if pairs % 2 != 0:
            err_line = start_line + content.count('\n')
            context.line_number = err_line
            return Error("Number of delimiter pairs must be even.", text.name, err_line)

        context.line_number = start_line + content.count('\n')
        return ValidatedText(text=text.text, name=text.name)

    return validate_text