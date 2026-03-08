import pytest

from src.syncspec.fragment_text import make_fragment_text
from src.syncspec.fragment_text_context import FragmentTextContext
from src.syncspec.validated_text import ValidatedText
from src.syncspec.fragment import Fragment


@pytest.mark.parametrize("text,expected_texts,expected_lines,final_line", [
    ("A{{B}}C", ["A", "B", "C"], [1, 1, 1], 1),
    ("A\n{{B}}", ["A\n", "B", ""], [1, 2, 2], 2),
    ("{{}}", ["", "", ""], [1, 1, 1], 1),
    ("*{{X}}*", ["*", "X", "*"], [1, 1, 1], 1),
])
def test_fragment_text(text, expected_texts, expected_lines, final_line):
    ctx = FragmentTextContext("test", "{{", "}}", 1)
    fn = make_fragment_text(ctx)
    result = fn(ValidatedText(text))
    assert [f.text for f in result] == expected_texts
    assert [f.line_number for f in result] == expected_lines
    assert ctx.line_number == final_line


def test_context_persistence():
    ctx = FragmentTextContext("test", "{{", "}}", 1)
    fn = make_fragment_text(ctx)
    fn(ValidatedText("A\n"))
    assert ctx.line_number == 2
    res = fn(ValidatedText("B"))
    assert res[0].line_number == 2