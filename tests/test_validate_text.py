import pytest
from src.syncspec.text import Text
from src.syncspec.validated_text import ValidatedText
from src.syncspec.error import Error
from src.syncspec.validate_text_context import ValidateTextContext
from src.syncspec.validate_text import make_validate_text

@pytest.fixture
def context():
    return ValidateTextContext(
        name="test",
        open_delimiter="{{",
        close_delimiter="}}",
        line_number=1
    )

@pytest.mark.parametrize("content, expected_type", [
    ("", ValidatedText),
    ("Hello World", ValidatedText),
    ("{{A}}B{{C}}", ValidatedText),
    ("{{A}}", Error),
    ("{{A{{B}}C}}", Error),
    ("}}A{{", Error),
    ("{{A}}B{{C}}D{{E}}", Error),
])
def test_validate_text_cases(content, expected_type, context):
    validate_text = make_validate_text(context)
    result = validate_text(Text(text=content))
    assert isinstance(result, expected_type)

def test_context_validation(context):
    context.open_delimiter = ""
    validate_text = make_validate_text(context)
    result = validate_text(Text(text=""))
    assert isinstance(result, Error)
    assert "empty" in result.message

def test_line_number_offset(context):
    context.line_number = 10
    validate_text = make_validate_text(context)
    result = validate_text(Text(text="}}"))
    assert isinstance(result, Error)
    assert result.line_number == 10