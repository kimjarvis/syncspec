import pytest
from unittest.mock import patch
from src.syncspec.include_block import make_include_block
from src.syncspec.block import Block
from src.syncspec.string import String
from src.syncspec.node import Node
from src.syncspec.include_block_context import IncludeBlockContext

@pytest.mark.parametrize("directive,expected_type", [
    ({}, Block),
    ({"include": "key1"}, tuple),
    ({"include": 123}, String),
    ({"include": "missing"}, String),
    ({"include": "key1", "head": -1}, String),
    ({"include": "key1", "head": 10}, String),
])
def test_include_block_logic(directive, expected_type):
    ctx = IncludeBlockContext(state={"key1": "INSERTED"}, open_delimiter="[", close_delimiter="]")
    block = Block(
        directive=directive,
        prefix="p", suffix="s",
        text="line1\nline2\n",
        line_number=1, name="test"
    )
    func = make_include_block(ctx)
    result = func(block)
    assert isinstance(result, expected_type)

def test_include_block_success_content():
    ctx = IncludeBlockContext(state={"k": "VAL"}, open_delimiter="<", close_delimiter=">")
    block = Block(
        directive={"include": "k", "head": 1, "tail": 1},
        prefix="P", suffix="S",
        text="A\nB\nC\n",
        line_number=5, name="src"
    )
    func = make_include_block(ctx)
    res, node = func(block)
    assert isinstance(res, String) and isinstance(node, Node)
    assert res.text == "<P>A\nVALC\n<S>"
    assert node.key == "k"