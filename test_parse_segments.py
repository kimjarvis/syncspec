import pytest
from parse_segments import parse_segments, Segment
from ensure_balanced_delimiters import EnsureBalancedDelimiters

@pytest.mark.parametrize("text, open_d, close_d, expected_texts", [
    ("A{{B}}C", "{{", "}}", ["A", "B", "C"]),
    ("{{}}", "{{", "}}", ["", "", ""]),
    ("ABC", "{{", "}}", ["ABC"]),
    ("{{A}}{{B}}", "{{", "}}", ["", "A", "", "B", ""]),
    ("A*B*C", "*", "*", ["A", "B", "C"]),
    ("α{{β}}γ", "{{", "}}", ["α", "β", "γ"]),
    ("", "{{", "}}", [""]),
])
def test_parse_segments(text, open_d, close_d, expected_texts):
    ebd = EnsureBalancedDelimiters(text, open_d, close_d)
    expected = [Segment(t, open_d, close_d) for t in expected_texts]
    assert parse_segments(ebd) == expected