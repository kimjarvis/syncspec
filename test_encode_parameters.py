import pytest
from encode_parameters import encode_parameters, EncodeParameters
from error import Error

@pytest.mark.parametrize(
    "data, open_del, close_del, expected_type, expected_msg",
    [
        ("test", "{{", "}}", EncodeParameters, ""),
        ("test", "", "}}", Error, "Empty delimiter"),
        ("test", "{{", "", Error, "Empty delimiter"),
        ("test", "{{", "{{", Error, "Equal delimiters"),
    ]
)
def test_encode_parameters(data, open_del, close_del, expected_type, expected_msg):
    result = encode_parameters(data, open_del, close_del)
    assert isinstance(result, expected_type)
    if expected_type == Error:
        assert result.message == expected_msg
    else:
        assert result.data == data