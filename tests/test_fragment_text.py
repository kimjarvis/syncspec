import pytest
from src.syncspec.fragment_text import make_fragment_text
from src.syncspec.validated_text import ValidatedText
from src.syncspec.fragment import Fragment
from src.syncspec.fragment_text_context import FragmentTextContext


@pytest.mark.parametrize(
    "text_content, expected_texts, expected_count",
    [
        ("A{{B}}C{{D}}EF", ["A", "B", "C", "D", "EF"], 5),
        ("{{}}", ["", "", ""], 3),
        ("{{A}}", ["", "A", ""], 3),
        ("{{}}A", ["", "", "A"], 3),
        ("A{{B}}", ["A", "B", ""], 3),
    ]
)
def test_fragment_text_structure(text_content, expected_texts, expected_count):
    ctx = FragmentTextContext(open_delimiter="{{", close_delimiter="}}", line_number=1)
    func = make_fragment_text(ctx)
    vt = ValidatedText(name="test", text=text_content)

    result = func(vt)

    assert len(result) == expected_count
    assert [f.text for f in result] == expected_texts
    assert all(f.name == "test" for f in result)


@pytest.mark.parametrize(
    "text_content, start_line, expected_texts, expected_lines",
    [
        ("A\nB{{C}}", 1, ["A\nB", "C", ""], [1, 2, 2]),
        ("{{\n}}", 1, ["", "\n", ""], [1, 1, 2]),
        ("Line1\nLine2", 1, ["Line1\nLine2"], [1]),
    ]
)
def test_fragment_text_line_numbers(text_content, start_line, expected_texts, expected_lines):
    ctx = FragmentTextContext(open_delimiter="{{", close_delimiter="}}", line_number=start_line)
    func = make_fragment_text(ctx)
    vt = ValidatedText(name="test", text=text_content)

    result = func(vt)

    assert [f.text for f in result] == expected_texts
    assert [f.line_number for f in result] == expected_lines
    assert ctx.line_number == start_line + text_content.count('\n')


def test_fragment_text_context_persistence():
    ctx = FragmentTextContext(open_delimiter="{{", close_delimiter="}}", line_number=1)
    func = make_fragment_text(ctx)

    func(ValidatedText(name="p1", text="Line1\n"))
    assert ctx.line_number == 2

    func(ValidatedText(name="p2", text="Line2"))
    assert ctx.line_number == 2

    frags = func(ValidatedText(name="p3", text="Line3"))
    assert frags[0].line_number == 2


def test_fragment_text_special_chars():
    ctx = FragmentTextContext(open_delimiter="*", close_delimiter="*", line_number=1)
    func = make_fragment_text(ctx)
    vt = ValidatedText(name="test", text="A*B*C")
    result = func(vt)
    assert [f.text for f in result] == ["A", "B", "C"]


def test_fragment_text_name_copy():
    ctx = FragmentTextContext(open_delimiter="{{", close_delimiter="}}", line_number=1)
    func = make_fragment_text(ctx)
    vt = ValidatedText(name="freddy", text="A{{B}}C")
    result = func(vt)
    assert all(f.name == "freddy" for f in result)