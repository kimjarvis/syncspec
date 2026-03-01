from ensure_balanced_delimiters import BalancedDelimitersEnsured
from dataclasses import dataclass
from typing import Union
import re
import pytest

Error = Exception

@dataclass
class Fragment:
    text: str
    name: str
    open_delimiter: str
    close_delimiter: str

def parse_fragments(ensure_balanced_delimiters: BalancedDelimitersEnsured) -> Union[list[Fragment], Error]:
    pattern = f"{re.escape(ensure_balanced_delimiters.open_delimiter)}|{re.escape(ensure_balanced_delimiters.close_delimiter)}"
    texts = re.split(pattern, ensure_balanced_delimiters.text)
    return [
        Fragment(text=t, name=ensure_balanced_delimiters.name,
                 open_delimiter=ensure_balanced_delimiters.open_delimiter,
                 close_delimiter=ensure_balanced_delimiters.close_delimiter)
        for t in texts
    ]

@pytest.mark.parametrize("text,expected_texts", [
    ("A{{B}}C", ["A", "B", "C"]),
    ("{{X}}", ["", "X", ""]),
    ("NoDelims", ["NoDelims"]),
    ("*A*B*", ["*A*B*",]), # Delimiters '*' would split differently, testing distinct delimiters
])
def test_parse_fragments_basic(text, expected_texts):
    # Using dummy delimiters for parametrize unless specific logic needed
    # Re-defining specific cases for clarity regarding delimiters
    pass

@pytest.mark.parametrize("text,open_cl,close_cl,expected_texts", [
    ("A{{B}}C", "{{", "}}", ["A", "B", "C"]),
    ("{{X}}", "{{", "}}", ["", "X", ""]),
    ("NoDelims", "{{", "}}", ["NoDelims"]),
    ("A*B*C", "*", "*", ["A", "B", "C"]), # Overlap check assumption violation, but tests split logic
])
def test_parse_fragments(text, open_cl, close_cl, expected_texts):
    e = BalancedDelimitersEnsured(text=text, name="test", open_delimiter=open_cl, close_delimiter=close_cl)
    result = parse_fragments(e)
    assert [f.text for f in result] == expected_texts
    assert all(f.name == "test" for f in result)
    assert all(f.open_delimiter == open_cl for f in result)