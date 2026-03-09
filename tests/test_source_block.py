import pytest
from src.syncspec.source_block import make_source_block
from src.syncspec.block import Block
from src.syncspec.source import Source
from src.syncspec.source_block_context import SourceBlockContext


@pytest.mark.parametrize("directive, expected_type, should_store", [
    ({"source": "key1"}, Source, True),
    ({"other": "val"}, Block, False),
    ({}, Block, False),
])
def test_create_blocks(directive, expected_type, should_store):
    SourceBlockContext.state = {}
    context = SourceBlockContext()
    transformer = make_source_block(context)

    block = Block(directive=directive, combined_directives="", text="content", line_number=1)
    result = transformer(block)

    assert isinstance(result, expected_type)
    if should_store:
        assert SourceBlockContext.state[directive["source"]] == "content"
    else:
        assert SourceBlockContext.state == {}