import pytest
from src.syncspec.encode_parameters import encode_parameters, EncodedParameters, Error


@pytest.mark.parametrize(
    "open_delim,close_delim,expected_type,msg_substring",
    [
        ("", "}}", Error, "empty"),
        ("{{", "", Error, "empty"),
        ("{{", "{{", Error, "distinct"),
        ("{{", "{", Error, "overlap"),
        ("{", "{{", Error, "overlap"),
    ],
)
def test_encode_parameters_validation(open_delim, close_delim, expected_type, msg_substring):
    result = encode_parameters("text", "test_name", open_delim, close_delim)
    assert isinstance(result, expected_type)
    if expected_type is Error:
        assert msg_substring in result.message
        assert result.name == "test_name"
        assert result.line == 1


@pytest.mark.parametrize(
    "open_delim,close_delim",
    [
        ("{{", "}}"),
        ("<?", "?>"),
        ("*", "#"),
    ],
)
def test_encode_parameters_success(open_delim, close_delim):
    result = encode_parameters("text", "test_name", open_delim, close_delim)
    assert isinstance(result, EncodedParameters)
    assert result.open_delimiter == open_delim
    assert result.close_delimiter == close_delim