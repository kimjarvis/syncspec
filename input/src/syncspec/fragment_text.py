import re
from typing import List
from src.syncspec.validated_text import ValidatedText
from src.syncspec.fragment import Fragment
from src.syncspec.fragment_text_context import FragmentTextContext


def make_fragment_text(context: FragmentTextContext):
    def fragment_text(text: ValidatedText) -> List[Fragment]:
        pattern = f"({re.escape(context.open_delimiter)}|{re.escape(context.close_delimiter)})"
        parts = re.split(pattern, text.text)

        fragments = []
        current_line = context.line_number

        for part in parts:
            if part in (context.open_delimiter, context.close_delimiter):
                current_line += part.count('\n')
            else:
                fragments.append(Fragment(
                    text=part,
                    name=text.name,
                    line_number=current_line
                ))
                current_line += part.count('\n')

        context.line_number = current_line
        return fragments

    return fragment_text