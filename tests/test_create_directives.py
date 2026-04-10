import pytest
from pathlib import Path

from syncspec.block import Block
from syncspec.context import Context
from syncspec.create_directives import make_create_directives
from syncspec.directive import Directive
from syncspec.stop import Stop

MOCK_CONTEXT = Context(
    open_delimiter="<!--{-", close_delimiter="-}-->",
    keyvalue={}, input_path=Path("."), keyvalue_file=Path("."), ignore_rules_file=Path(".")
)

@pytest.mark.parametrize(
    "prefix, expected",
    [
        ('import="src/file.py", head=2, eol=True', {'import': 'src/file.py', 'head': 2, 'eol': True}),
        ('count=10, flag=False', {'count': 10, 'flag': False}),
        ('name="test",', {'name': 'test'}),
    ]
)
def test_create_directives_valid(prefix, expected):
    block = Block(prefix=prefix, text="body", suffix="end", path=Path("test.py"),
                  prefix_line_number=1, text_line_number=2, suffix_line_number=3)
    fn = make_create_directives(MOCK_CONTEXT)
    res = fn(block)
    assert isinstance(res, Directive)
    assert res.parameters == expected
    assert res.path == block.path

@pytest.mark.parametrize("prefix", ["key=invalid_syntax", 'unclosed="str'])
def test_create_directives_invalid(prefix, caplog):
    block = Block(prefix=prefix, text="x", suffix="y", path=Path("err.py"),
                  prefix_line_number=5, text_line_number=6, suffix_line_number=7)
    fn = make_create_directives(MOCK_CONTEXT)
    res = fn(block)
    assert isinstance(res, Stop)
    assert "ERROR" in caplog.text