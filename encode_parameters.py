from dataclasses import dataclass
from error import Error
import pytest

@dataclass
class EncodedParameters:
    text: str
    name: str
    open_delimiter: str
    close_delimiter: str

def encode_parameters(text: str, name: str = "", open_delimiter: str = "{{", close_delimiter: str = "}}") -> EncodedParameters | Error:
    if not open_delimiter or not close_delimiter:
        return Error("Delimiters cannot be empty", name, 1)
    if open_delimiter == close_delimiter:
        return Error("Delimiters must be distinct", name, 1)
    if open_delimiter in close_delimiter or close_delimiter in open_delimiter:
        return Error("Delimiters cannot overlap structurally", name, 1)
    return EncodedParameters(text, name, open_delimiter, close_delimiter)

@pytest.mark.parametrize("text, name, open_d, close_d, expected", [
    ("", "", "{{", "}}", EncodedParameters),
    ("txt", "n", "{{", "}}", EncodedParameters),
    ("", "", "", "}}", Error),
    ("", "", "{{", "", Error),
    ("", "", "{{", "{{", Error),
    ("", "", "{{", "{", Error),
    ("", "", "{", "{{", Error),
])
def test_encode_parameters(text, name, open_d, close_d, expected):
    assert isinstance(encode_parameters(text, name, open_d, close_d), expected)