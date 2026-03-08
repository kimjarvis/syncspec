from typing import Union
from src.syncspec.text import Text
from src.syncspec.validated_text import ValidatedText
from src.syncspec.error import Error
from src.syncspec.validate_text_context import ValidateTextContext


def make_validate_text(context: ValidateTextContext):
    def validate_text(text: Text) -> Union[ValidatedText, Error]:
        # Verify Context Configuration
        if not isinstance(context.name, str) or not context.name:
            return Error(message="Context name must be a non-empty Unicode string",
                         name=context.name, line_number=context.line_number)

        open_d = context.open_delimiter
        close_d = context.close_delimiter

        if not isinstance(open_d, str) or not isinstance(close_d, str):
            return Error(message="Delimiters must be Unicode strings",
                         name=context.name, line_number=context.line_number)
        if not open_d or not close_d:
            return Error(message="Delimiters cannot be empty",
                         name=context.name, line_number=context.line_number)
        if open_d == close_d:
            return Error(message="Delimiters must be distinct",
                         name=context.name, line_number=context.line_number)
        if open_d in close_d or close_d in open_d:
            return Error(message="Delimiters overlap structurally",
                         name=context.name, line_number=context.line_number)

        # Verify Text Type
        if not isinstance(text.text, str):
            return Error(message="Text must be a Unicode string",
                         name=context.name, line_number=context.line_number)

        content = text.text
        base_line = context.line_number

        # Find Delimiters
        occurrences = []
        start = 0
        while start < len(content):
            open_idx = content.find(open_d, start)
            close_idx = content.find(close_d, start)

            if open_idx == -1 and close_idx == -1:
                break

            # Determine which comes first
            if open_idx != -1 and (close_idx == -1 or open_idx < close_idx):
                occurrences.append((open_idx, 'open'))
                start = open_idx + len(open_d)
            else:
                occurrences.append((close_idx, 'close'))
                start = close_idx + len(close_d)

        if not occurrences:
            return ValidatedText(text=content)

        # Verify Order: First must be Open
        if occurrences[0][1] == 'close':
            line = content[:occurrences[0][0]].count('\n') + base_line
            return Error(message="Close delimiter appears before open delimiter",
                         name=context.name, line_number=line)

        # Verify Structure: Balance, Nesting, Even Pairs
        stack = []
        pair_count = 0

        for pos, dtype in occurrences:
            line = content[:pos].count('\n') + base_line

            if dtype == 'open':
                if stack:
                    return Error(message="Nested delimiters detected",
                                 name=context.name, line_number=line)
                stack.append(line)
            else:
                if not stack:
                    return Error(message="Unbalanced close delimiter",
                                 name=context.name, line_number=line)
                stack.pop()
                pair_count += 1

        if stack:
            return Error(message="Unclosed open delimiter",
                         name=context.name, line_number=stack[0])

        if pair_count % 2 != 0:
            return Error(message="Number of delimiter pairs must be even",
                         name=context.name, line_number=base_line)

        return ValidatedText(text=content)

    return validate_text