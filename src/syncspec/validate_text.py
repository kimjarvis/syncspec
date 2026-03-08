from src.syncspec.text import Text
from src.syncspec.error import Error
from src.syncspec.fragment import Fragment
from src.syncspec.monad import Monad
from typing import Union


def validate_text(text: Text) -> Union[Fragment, Error]:
    # Verify Monad State Existence
    required_keys = ["open_delimiter", "close_delimiter", "name", "length", "index"]
    if not all(k in Monad.state for k in required_keys):
        return Error(message="Monad state missing required keys", name="", line_number=0)

    idx = Monad.state["index"]
    length = Monad.state["length"]
    name = Monad.state["name"]
    open_d = Monad.state["open_delimiter"]
    close_d = Monad.state["close_delimiter"]

    # Verify Monad Bounds
    if not (0 <= idx < length):
        return Error(message=f"Invalid index {idx} for length {length}", name=name, line_number=0)

    # Verify Delimiters
    if not isinstance(open_d, str) or not isinstance(close_d, str):
        return Error(message="Delimiters must be Unicode strings", name=name, line_number=0)
    if not open_d or not close_d:
        return Error(message="Delimiters cannot be empty", name=name, line_number=0)
    if open_d == close_d:
        return Error(message="Delimiters must be distinct", name=name, line_number=0)
    if open_d in close_d or close_d in open_d:
        return Error(message="Delimiters overlap structurally", name=name, line_number=0)

    # Verify Text Type
    if not isinstance(text.text, str):
        return Error(message="Text must be a Unicode string", name=name, line_number=0)

    content = text.text
    occurrences = []

    # Find all delimiter occurrences
    start = 0
    while start < len(content):
        open_idx = content.find(open_d, start)
        close_idx = content.find(close_d, start)

        if open_idx == -1 and close_idx == -1:
            break

        if open_idx != -1 and (close_idx == -1 or open_idx < close_idx):
            occurrences.append((open_idx, 'open'))
            start = open_idx + len(open_d)
        else:
            occurrences.append((close_idx, 'close'))
            start = close_idx + len(close_d)

    # Verify Text Structure
    if not occurrences:
        # 0 pairs is even (0 % 2 == 0), valid
        return Fragment(text=content, line_number=content.count('\n') + 1)

    # First delimiter must be open
    if occurrences[0][1] == 'close':
        line = content[:occurrences[0][0]].count('\n') + 1
        return Error(message="Close delimiter appears before open delimiter", name=name, line_number=line)

    stack = []
    pair_count = 0

    for pos, dtype in occurrences:
        line = content[:pos].count('\n') + 1
        if dtype == 'open':
            if stack:
                return Error(message="Nested delimiters detected", name=name, line_number=line)
            stack.append(line)
        else:
            if not stack:
                return Error(message="Unbalanced close delimiter", name=name, line_number=line)
            stack.pop()
            pair_count += 1

    if stack:
        return Error(message="Unclosed open delimiter", name=name, line_number=stack[0])

    if pair_count % 2 != 0:
        # Error on the last pair's close delimiter roughly, or just general
        # Spec says "line number on which the error was detected".
        # We detect this after parsing. Let's point to the last line.
        return Error(message="Number of delimiter pairs must be even", name=name, line_number=content.count('\n') + 1)

    return Fragment(text=content, line_number=content.count('\n') + 1)