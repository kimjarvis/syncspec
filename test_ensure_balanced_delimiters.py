import pytest
from ensure_balanced_delimiters import ensure_balanced_delimiters, EnsureBalancedDelimiters
from encode_parameters import EncodeParameters
from error import Error


@pytest.mark.parametrize(
    "data, expected_type, expected_msg",
    [
        ("{{content}}", EnsureBalancedDelimiters, ""),
        ("{{a}}{{b}}", EnsureBalancedDelimiters, ""),
        ("", EnsureBalancedDelimiters, ""),
        ("{{ {{ }} }}", Error, "Delimiters are nested"),
        ("{{ content", Error, "Delimiters are not matched"),
        ("content }}", Error, "Delimiters are not matched"),
    ],
)
def test_ensure_balanced_delimiters(data, expected_type, expected_msg):
    params = EncodeParameters(data=data)
    result = ensure_balanced_delimiters(params)
    assert isinstance(result, expected_type)
    if isinstance(result, Error):
        assert result.message == expected_msg
    else:
        assert result.data == data