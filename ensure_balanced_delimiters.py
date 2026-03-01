from dataclasses import dataclass
from typing import Union
import pytest


# In production, uncomment imports and remove class definitions below
# from encode_parameters import EncodedParameters
# from error import Error

@dataclass
class EncodedParameters:
    text: str
    name: str
    open_delimiter: str
    close_delimiter: str


@dataclass
class Error:
    message: str
    name: str
    line: int


@dataclass
class BalancedDelimitersEnsured:
    text: str
    name: str
    open_delimiter: str
    close_delimiter: str


def ensure_balanced_delimiters(encoded_parameters: EncodedParameters) -> Union[BalancedDelimitersEnsured, Error]:
    text = encoded_parameters.text
    open_d = encoded_parameters.open_delimiter
    close_d = encoded_parameters.close_delimiter
    name = encoded_parameters.name

    pos = 0
    inside = False
    open_pos = -1

    while pos < len(text):
        i_open = text.find(open_d, pos)
        i_close = text.find(close_d, pos)

        if i_open == -1 and i_close == -1:
            break

        if i_open != -1 and (i_close == -1 or i_open < i_close):
            next_idx, is_open = i_open, True
        else:
            next_idx, is_open = i_close, False

        line = text[:next_idx].count('\n') + 1

        if is_open:
            if inside:
                return Error("Nesting detected", name, line)
            inside = True
            open_pos = next_idx
            pos = next_idx + len(open_d)
        else:
            if not inside:
                return Error("Unbalanced close delimiter", name, line)
            inside = False
            pos = next_idx + len(close_d)

    if inside:
        line = text[:open_pos].count('\n') + 1
        return Error("Unclosed open delimiter", name, line)

    return BalancedDelimitersEnsured(text, name, open_d, close_d)


@pytest.mark.parametrize("text,open_d,close_d,expected_type", [
    ("{{A}}", "{{", "}}", BalancedDelimitersEnsured),
    ("{{A}}B{{C}}", "{{", "}}", BalancedDelimitersEnsured),
    ("A{{B}}C", "{{", "}}", BalancedDelimitersEnsured),
    ("}}A{{B}}", "{{", "}}", Error),
    ("{{A{{B}}C}}", "{{", "}}", Error),
    ("{{A", "{{", "}}", Error),
    ("A}}B", "{{", "}}", Error),
    ("{{*}}", "{{", "}}", BalancedDelimitersEnsured),
    ("{{A}}", "{", "}", Error),
])
def test_ensure_balanced_delimiters(text, open_d, close_d, expected_type):
    params = EncodedParameters(text, "test", open_d, close_d)
    result = ensure_balanced_delimiters(params)
    assert isinstance(result, expected_type)
    if expected_type == Error:
        assert result.line >= 1
        assert result.name == "test"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])