import pytest
import logging
from src.syncspec.validate_text import make_validate_text
from src.syncspec.text import Text
from src.syncspec.validate_text_context import ValidateTextContext
from src.syncspec.validated_text import ValidatedText
from src.syncspec.string import String


@pytest.mark.parametrize(
    "content, expected_type, error_msg",
    [
        ("", ValidatedText, None),
        ("No delimiters", ValidatedText, None),
        ("A{{B}}C{{D}}E", ValidatedText, None),
        ("A{{B}}C", String, "Odd number"),
        ("A{{B}}C{{D}}E{{F}}G", String, "Odd number"),
        ("{{A{{B}}C}}", String, "Nested"),
        ("}}A{{B}}", String, "Close delimiter"),
        ("{{A", String, "Unclosed"),
    ],
)
def test_validate_text_logic(content, expected_type, error_msg, caplog):
    context = ValidateTextContext(open_delimiter="{{", close_delimiter="}}", line_number=1)
    validator = make_validate_text(context)
    text_obj = Text(text=content, name="test.txt")

    caplog.set_level(logging.ERROR)
    result = validator(text_obj)

    assert isinstance(result, expected_type)
    if error_msg:
        assert error_msg in caplog.text
    else:
        assert caplog.text == ""


def test_context_line_number_update_non_empty():
    context = ValidateTextContext(open_delimiter="{{", close_delimiter="}}", line_number=10)
    validator = make_validate_text(context)
    text_obj = Text(text="Line1\nLine2\n", name="test.txt")

    validator(text_obj)
    # "Line1\n", "Line2\n" -> 2 lines
    assert context.line_number == 12


def test_context_line_number_update_empty():
    context = ValidateTextContext(open_delimiter="{{", close_delimiter="}}", line_number=5)
    validator = make_validate_text(context)
    text_obj = Text(text="", name="test.txt")

    validator(text_obj)
    # Empty text increments by 1
    assert context.line_number == 6


def test_error_line_number_accuracy(caplog):
    context = ValidateTextContext(open_delimiter="{{", close_delimiter="}}", line_number=10)
    validator = make_validate_text(context)
    # Error at line 11 (second line)
    text_obj = Text(text="Line1\n}}\n", name="test.txt")

    caplog.set_level(logging.ERROR)
    result = validator(text_obj)

    assert isinstance(result, String)
    assert result.line_number == 11
    assert "Close delimiter" in caplog.text


def test_odd_pairs_error_line(caplog):
    context = ValidateTextContext(open_delimiter="{{", close_delimiter="}}", line_number=1)
    validator = make_validate_text(context)
    # 1 pair on line 1
    text_obj = Text(text="{{A}}", name="test.txt")

    caplog.set_level(logging.ERROR)
    result = validator(text_obj)

    assert isinstance(result, String)
    assert result.line_number == 1
    assert "Odd number" in caplog.text