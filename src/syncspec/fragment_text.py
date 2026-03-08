import re
from typing import List

from src.syncspec.fragment_text_context import FragmentTextContext
from src.syncspec.validated_text import ValidatedText
from src.syncspec.fragment import Fragment


def make_fragment_text(context: FragmentTextContext):
    pattern = re.compile(f"{re.escape(context.open_delimiter)}|{re.escape(context.close_delimiter)}")

    def fragment_text(text: ValidatedText) -> List[Fragment]:
        fragments = []
        for part in pattern.split(text.text):
            fragments.append(Fragment(text=part, line_number=context.line_number))
            context.line_number += part.count("\n")
        return fragments

    return fragment_text