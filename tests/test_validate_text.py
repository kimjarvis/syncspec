# tests/test_validate_text.py
import pytest
import logging
from src.syncspec.text import Text
from src.syncspec.validated_text import ValidatedText
from src.syncspec.validate_text_context import ValidateTextContext
from src.syncspec.validate_text import make_validate_text


@pytest.fixture
def valid_context():
    return ValidateTextContext(open_delimiter="{{", close_delimiter="}}", line_number=1)


@pytest.mark.parametrize("open_delim, close_delim, expected_error", [
    ("", "}}", "empty"),
    ("{{", "", "empty"),
    ("{{", "{{", "distinct"),
    ("{{", "{", "overlap"),
    ("{\n", "}}", "newline"),
])
def test_make_validate_text_invalid_context(open_delim, close_delim, expected_error):
    context = ValidateTextContext(open_delimiter=open_delim, close_delimiter=close_delim, line_number=1)
    with pytest.raises(ValueError):
        make_validate_text(context)


@pytest.mark.parametrize("text_content, expected_pairs", [
    ("", 0),
    ("Hello World", 0),
    ("{{A}}B{{C}}", 2),
    ("{{A}}\n{{B}}", 2),
])
def test_validate_text_success(valid_context, text_content, expected_pairs):
    validator = make_validate_text(valid_context)
    text_obj = Text(text=text_content, name="test.txt")
    result = validator(text_obj)
    assert isinstance(result, ValidatedText)
    assert result.text == text_content


@pytest.mark.parametrize("text_content, error_keyword", [
    ("{{A}}", "even"),           # 1 pair (odd)
    ("{{A}}B{{C}}D{{E}}", "even"), # 3 pairs (odd)
    ("{{A{{B}}C}}", "Nested"),   # Nesting
    ("A}}B", "close"),           # Unmatched close
    ("{{A", "Unbalanced"),       # Unmatched open
])
def test_validate_text_failure(valid_context, text_content, error_keyword, caplog):
    caplog.set_level(logging.ERROR)
    validator = make_validate_text(valid_context)
    text_obj = Text(text=text_content, name="test.txt")
    result = validator(text_obj)
    assert result is None
    assert any(error_keyword in record.message for record in caplog.records)


@pytest.mark.parametrize("text_content, expected_line", [
    ("}}", 1),
    ("A\n}}", 2),
    ("A\nB\n}}", 3),
])
def test_validate_text_line_numbers(valid_context, text_content, expected_line, caplog):
    caplog.set_level(logging.ERROR)
    validator = make_validate_text(valid_context)
    text_obj = Text(text=text_content, name="test.txt")
    result = validator(text_obj)
    assert result is None
    # Verify line number is in the log message (format_error includes it)
    assert any(str(expected_line) in record.message for record in caplog.records)