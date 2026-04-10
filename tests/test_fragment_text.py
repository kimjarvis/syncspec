import pytest
from pathlib import Path
from syncspec.context import Context
from syncspec.file_path import FilePath
from syncspec.fragment import Fragment
from syncspec.stop import Stop
from syncspec.fragment_text import make_fragment_text

@pytest.fixture
def fragment_text():
    ctx = Context(
        open_delimiter="{{", close_delimiter="}}",
        keyvalue={}, input_path=Path("in"), keyvalue_file=Path("kv"), ignore_rules_file=Path("ig")
    )
    return make_fragment_text(ctx)

@pytest.mark.parametrize("text, count", [
    ("A{{B}}C", 3),
    ("{{}}", 3),
    ("{{A}}", 3),
    ("{{}}A", 3),
    ("no delimiters", 1),
    ("{{A}}{{B}}", 5),
])
def test_fragment_count(text, count, fragment_text):
    res = fragment_text(FilePath(path=Path("p"), text=text))
    assert isinstance(res, list) and len(res) == count

@pytest.mark.parametrize("text, expected_lines", [
    ("line1\n{{line2}}", [1, 2, 2]),  # Trailing empty fragment after closing delimiter
    ("{{multi\nline}}\nend", [1, 1, 2]),
])
def test_line_numbers(text, expected_lines, fragment_text):
    res = fragment_text(FilePath(path=Path("p"), text=text))
    assert isinstance(res, list) and [f.line_number for f in res] == expected_lines

@pytest.mark.parametrize("text", [
    "", "{{A", "A}}", "{{A}}B{{"
])
def test_invalid_syntax(text, fragment_text):
    assert isinstance(fragment_text(FilePath(path=Path("p"), text=text)), Stop)