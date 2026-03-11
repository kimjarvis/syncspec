import pytest
from src.syncspec.source_block import make_source_block
from src.syncspec.block import Block
from src.syncspec.source_block_context import SourceBlockContext
from src.syncspec.string import String
from src.syncspec.node import Node


@pytest.mark.parametrize(
    "directive, expected_type, updates_state",
    [
        ({"source": "key1"}, tuple, True),
        ({}, Block, False),
        ({"source": 123}, Block, False),
    ]
)
def test_source_block(directive, expected_type, updates_state):
    context = SourceBlockContext(state={}, open_delimiter="<", close_delimiter=">")
    block = Block(directive=directive, prefix="p", suffix="s", text="t", line_number=1, name="n")
    handler = make_source_block(context)
    result = handler(block)

    assert isinstance(result, expected_type)

    if updates_state:
        s, n = result
        assert isinstance(s, String)
        assert isinstance(n, Node)
        assert context.state["key1"] == "t"
        assert s.text == "<p>t<s>"  # Based on spec delimiter order
        assert n.key == "key1"
        assert n.directive_type == "source"
    else:
        assert result is block