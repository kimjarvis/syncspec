import pytest
from src.syncspec.string import String
from src.syncspec.combine_strings_context import CombineStringsContext
from src.syncspec.combine_strings import make_combine_strings

@pytest.mark.parametrize("initial, input_text, expected", [
    ("", "hello", "hello"),
    ("hello", " world", "hello world"),
    ("", "", ""),
    ("existing", "", "existing"),
])
def test_combine_strings_appends_text(initial, input_text, expected):
    context = CombineStringsContext(text=initial)
    combiner = make_combine_strings(context)
    combiner(String(text=input_text, line_number=1))
    assert context.text == expected

@pytest.mark.parametrize("inputs, expected", [
    (["a", "b", "c"], "abc"),
    (["", "x", ""], "x"),
])
def test_combine_strings_accumulates_state(inputs, expected):
    context = CombineStringsContext(text="")
    combiner = make_combine_strings(context)
    for text in inputs:
        combiner(String(text=text, line_number=1))
    assert context.text == expected