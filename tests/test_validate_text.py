import pytest
from src.syncspec.validate_text import make_validate_text
from src.syncspec.text import Text
from src.syncspec.validated_text import ValidatedText
from src.syncspec.error import Error
from src.syncspec.validate_text_context import ValidateTextContext


@pytest.mark.parametrize("content,expected_type,pairs", [
    ("No delimiters", ValidatedText, 0),
    ("{{A}}{{B}}", ValidatedText, 2),
    ("{{A}}{{B}}{{C}}{{D}}", ValidatedText, 4),
    ("{{A}}", Error, 1),
    ("{{A}}{{B}}{{C}}", Error, 3),
    ("}} {{", Error, 0),
    ("{{ {{ }} }}", Error, 2),
    ("{{A}} {{", Error, 1),
])
def test_validate_text_logic(content, expected_type, pairs):
    ctx = ValidateTextContext(open_delimiter="{{", close_delimiter="}}", line_number=1)
    validator = make_validate_text(ctx)
    text_obj = Text(text=content, name="test")
    result = validator(text_obj)
    assert isinstance(result, expected_type)
    if expected_type is Error:
        assert result.name == "test"
        assert result.line_number >= 1


def test_line_number_accumulation():
    ctx = ValidateTextContext(open_delimiter="{{", close_delimiter="}}", line_number=1)
    validator = make_validate_text(ctx)
    validator(Text(text="Line1\nLine2\n", name="t1"))
    assert ctx.line_number == 3
    validator(Text(text="Line3\n", name="t2"))
    assert ctx.line_number == 4


def test_context_validation():
    with pytest.raises(ValueError):
        make_validate_text(ValidateTextContext("", "}}", 1))
    with pytest.raises(ValueError):
        make_validate_text(ValidateTextContext("{{", "{{", 1))
    with pytest.raises(ValueError):
        make_validate_text(ValidateTextContext("{", "{{", 1))


def test_error_line_number_accuracy():
    ctx = ValidateTextContext(open_delimiter="{{", close_delimiter="}}", line_number=10)
    validator = make_validate_text(ctx)
    text_obj = Text(text="Line1\n}}", name="t1")
    result = validator(text_obj)
    assert isinstance(result, Error)
    assert result.line_number == 11
    assert ctx.line_number == 11