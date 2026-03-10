from dataclasses import dataclass
from src.syncspec.error import Error


@dataclass
class BalancedDelimitersEnsured:
    text: str
    name: str
    open_delimiter: str
    close_delimiter: str


def ensure_balanced_delimiters(encoded_parameters: EncodedParameters) -> BalancedDelimitersEnsured | Error:
    print(f"ensure_balanced_delimiters called with: {encoded_parameters}")
    text = encoded_parameters.text
    open_d = encoded_parameters.open_delimiter
    close_d = encoded_parameters.close_delimiter
    name = encoded_parameters.name

    state_open = False
    pos = 0
    length = len(text)

    while pos < length:
        next_open = text.find(open_d, pos)
        next_close = text.find(close_d, pos)

        # Determine which delimiter appears next
        if next_open == -1 and next_close == -1:
            break

        if next_open != -1 and (next_close == -1 or next_open < next_close):
            index = next_open
            is_open_tag = True
        else:
            index = next_close
            is_open_tag = False

        if is_open_tag:
            if state_open:
                line = text[:index].count('\n') + 1
                return Error(f"Nesting detected at open delimiter", name, line)
            state_open = True
            pos = index + len(open_d)
        else:
            if not state_open:
                line = text[:index].count('\n') + 1
                return Error(f"Close delimiter found before open delimiter", name, line)
            state_open = False
            pos = index + len(close_d)

    if state_open:
        # Find the start of the unclosed open delimiter for line number
        # We need to search backwards or track last open index.
        # Simplification: Report end of text or search back.
        # To be precise, we should have tracked the index of the last open.
        # Refactoring slightly to track last_open_index for accurate error reporting.
        pass

        # Refactored loop to track last_open_index for unclosed error
    # Re-implementing cleanly below for correctness regarding unclosed line number
    return _validate(text, name, open_d, close_d)


def _validate(text: str, name: str, open_d: str, close_d: str) -> BalancedDelimitersEnsured | Error:
    state_open = False
    pos = 0
    last_open_index = 0
    length = len(text)

    while pos < length:
        next_open = text.find(open_d, pos)
        next_close = text.find(close_d, pos)

        if next_open == -1 and next_close == -1:
            break

        if next_open != -1 and (next_close == -1 or next_open < next_close):
            index = next_open
            is_open_tag = True
        else:
            index = next_close
            is_open_tag = False

        if is_open_tag:
            if state_open:
                line = text[:index].count('\n') + 1
                return Error(f"Nesting detected at open delimiter", name, line)
            state_open = True
            last_open_index = index
            pos = index + len(open_d)
        else:
            if not state_open:
                line = text[:index].count('\n') + 1
                return Error(f"Close delimiter found before open delimiter", name, line)
            state_open = False
            pos = index + len(close_d)

    if state_open:
        line = text[:last_open_index].count('\n') + 1
        return Error(f"Unclosed open delimiter", name, line)

    x = BalancedDelimitersEnsured(text, name, open_d, close_d)
    print(f"ensure_balanced_delimiters returning: {x}")
    return x