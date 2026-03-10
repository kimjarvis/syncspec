from src.syncspec.string import String
from src.syncspec.combine_strings_context import CombineStringsContext

def make_combine_strings(context: CombineStringsContext):
    def combine_strings(string: String) -> None:
        context.text += string.text
    return combine_strings