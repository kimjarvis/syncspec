import pytest
from src.syncspec.source_block import make_source_block
from src.syncspec.block import Block
from src.syncspec.string import String
from src.syncspec.source_block_context import SourceBlockContext


@pytest.mark.parametrize("directive, expected_type, state_updated", [
    ({"source": "key1"}, String, True),
    ({}, Block, False),
])
def test_source_block(directive, expected_type, state_updated):
    context = SourceBlockContext(state={}, open_delimiter="{{", close_delimiter="}}")
    block = Block(directive=directive, prefix="p", suffix="s", text="t", line_number=1, name="n")

    func = make_source_block(context)
    result = func(block)

    assert isinstance(result, expected_type)
    if state_updated:
        assert context.state["key1"] == "t"
        assert result.text == "{{p}}t{{s}}"
    else:
        assert result is block