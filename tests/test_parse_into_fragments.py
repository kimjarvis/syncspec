import pytest
from src.syncspec.parse_into_fragments import parse_into_fragments, Fragment, Error
from src.syncspec.ensure_balanced_delimiters import BalancedDelimitersEnsured

@pytest.mark.parametrize(
    "text, open_delim, close_delim, expected_texts",
    [
        ("A{{B}}C", "{{", "}}", ["A", "B", "C"]),
        ("{{A}}B{{C}}", "{{", "}}", ["A", "B", "C"]),
        ("no delims", "{{", "}}", ["no delims"]),
        ("{{*}}", "{{", "}}", ["*"]),
    ]
)
def test_parse_into_fragments(text, open_delim, close_delim, expected_texts):
    input_obj = BalancedDelimitersEnsured(
        text=text, name="test", open_delimiter=open_delim, close_delimiter=close_delim
    )
    result = parse_into_fragments(input_obj)
    assert not isinstance(result, Error)
    assert [f.text for f in result] == expected_texts
    assert all(f.name == "test" for f in result)
    assert all(f.open_delimiter == open_delim for f in result)