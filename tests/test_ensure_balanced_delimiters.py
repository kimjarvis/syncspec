import pytest
from src.syncspec.ensure_balanced_delimiters import ensure_balanced_delimiters, BalancedDelimitersEnsured
from src.syncspec.encode_parameters import EncodedParameters
from src.syncspec.error import Error


@pytest.mark.parametrize(
    "text, open_d, close_d, expected_type",
    [
        ("{{A}}", "{{", "}}", BalancedDelimitersEnsured),
        ("{{A}}B{{C}}", "{{", "}}", BalancedDelimitersEnsured),
        ("", "{{", "}}", BalancedDelimitersEnsured),
        ("No delimiters", "{{", "}}", BalancedDelimitersEnsured),
        ("*+", "*", "+", BalancedDelimitersEnsured),  # Fixed: Balanced special chars
    ]
)
def test_valid_balanced(text, open_d, close_d, expected_type):
    params = EncodedParameters(text, "test", open_d, close_d)
    result = ensure_balanced_delimiters(params)
    assert isinstance(result, expected_type)
    if expected_type == BalancedDelimitersEnsured:
        assert result.text == text


@pytest.mark.parametrize(
    "text, open_d, close_d, error_msg_substring",
    [
        ("}}", "{{", "}}", "before open"),
        ("{{A", "{{", "}}", "Unclosed"),
        ("{{A{{B}}", "{{", "}}", "Nesting"),
        ("{{A}}B{{", "{{", "}}", "Unclosed"),
        ("*", "*", "+", "Unclosed"),  # Added: Unbalanced special chars
    ]
)
def test_invalid_balanced(text, open_d, close_d, error_msg_substring):
    params = EncodedParameters(text, "test", open_d, close_d)
    result = ensure_balanced_delimiters(params)
    assert isinstance(result, Error)
    assert error_msg_substring in result.message
    assert result.name == "test"
    assert isinstance(result.line, int)
    assert result.line >= 1