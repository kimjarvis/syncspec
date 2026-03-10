import pytest
from src.syncspec.combine_blocks import make_combine_blocks
from src.syncspec.block import Block
from src.syncspec.combine_blocks_context import CombineBlocksContext
from src.syncspec.stop import Stop


@pytest.mark.parametrize("prefix, expected_text", [
    (None, "content"),
    ("pre", "{open}pre{close}content{open}suf{close}"),
])
def test_combine_blocks_with_block(prefix, expected_text):
    ctx = CombineBlocksContext("", "{open}", "{close}")
    combiner = make_combine_blocks(ctx)
    block = Block({}, prefix, "suf", "content", 1)

    result = combiner(block)

    assert isinstance(result, Stop)
    assert ctx.text == expected_text


def test_combine_blocks_non_block():
    ctx = CombineBlocksContext("", "{open}", "{close}")
    combiner = make_combine_blocks(ctx)
    obj = object()

    assert combiner(obj) is obj
    assert ctx.text == ""