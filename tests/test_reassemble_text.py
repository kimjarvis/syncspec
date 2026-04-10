import pytest
from pathlib import Path
from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.reassemble_text import make_reassemble_text


@pytest.mark.parametrize(
    "open_d, close_d, prefix, text, suffix, expected",
    [
        ("{{", "}}", "p", "t", "s", "{{p}}t{{s}}"),
        ("", "", "", "body", "", "body"),
        ("<!--", "-->", "pre", "content", "post", "<!--pre-->content<!--post-->"),
    ]
)
def test_reassemble_text_concatenation(open_d, close_d, prefix, text, suffix, expected):
    ctx = Context(open_d, close_d, {}, Path("/in"), Path("/kv"), Path("/ign"))
    dirct = Directive({}, prefix, text, suffix, Path("/src/f.txt"), 10, 11, 12)

    fn = make_reassemble_text(ctx)
    result = fn(dirct)

    assert result.text == expected
    assert result.path == Path("/src/f.txt")
    assert result.line_number == 10