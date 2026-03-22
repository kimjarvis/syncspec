import pytest
from src.syncspec.parameter_string import String
from src.syncspec.combine_strings_context import CombineStringsContext
from src.syncspec.combine_strings import make_combine_strings


@pytest.mark.parametrize("input_text, expected", [
    ("hello", "hello"),
    ("", ""),
    ("world", "world"),
])
def test_combine_strings_single(input_text, expected):
    ctx = CombineStringsContext(text="")
    combiner = make_combine_strings(ctx)
    combiner(String(text=input_text, line_number=0, name="test"))
    assert ctx.text == expected


@pytest.mark.parametrize("inputs, expected", [
    (["a", "b", "c"], "abc"),
    (["", "x", ""], "x"),
])
def test_combine_strings_accumulation(inputs, expected):
    ctx = CombineStringsContext(text="")
    combiner = make_combine_strings(ctx)
    for text in inputs:
        combiner(String(text=text, line_number=0, name="test"))
    assert ctx.text == expected