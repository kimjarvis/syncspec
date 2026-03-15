import pytest
from src.syncspec.include_block import make_include_block
from src.syncspec.block import Block
from src.syncspec.include_block_context import IncludeBlockContext
from src.syncspec.string import String
from src.syncspec.node import Node
from src.syncspec.error import Error


@pytest.mark.parametrize("directive,expected_type", [
    ({}, Block),
    ({"include": 123}, Error),
    ({"include": "missing"}, Error),
    ({"include": "key", "head": -1}, Error),
    ({"include": "key", "tail": -1}, Error),
    ({"include": "key", "head": 5, "tail": 5}, Error),
    ({"include": "key", "head": True}, Error),
])
def test_include_block_variants(directive, expected_type):
    ctx = IncludeBlockContext(state={"key": "VAL"}, open_delimiter="[", close_delimiter="]")
    block = Block(directive=directive, prefix="", suffix="", text="A\nB\nC\n", line_number=1, name="test")
    result = make_include_block(ctx)(block)
    assert isinstance(result, expected_type)


def test_include_block_success():
    ctx = IncludeBlockContext(state={"key": "INSERT"}, open_delimiter="<", close_delimiter=">")
    block = Block(
        directive={"include": "key", "head": 1, "tail": 1},
        prefix="p", suffix="s",
        text="1\n2\n3\n", line_number=10, name="blk"
    )
    result = make_include_block(ctx)(block)
    assert isinstance(result, tuple)
    s, n = result
    assert isinstance(s, String) and isinstance(n, Node)
    assert s.text == "<p>1\nINSERT3\n<s>"
    assert n.directive_type == "include" and n.key == "key"