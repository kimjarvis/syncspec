import pytest
from src.syncspec.fragment import Fragment
from src.syncspec.string import String
from src.syncspec.block import Block
from src.syncspec.create_blocks_context import CreateBlocksContext
from src.syncspec.create_blocks import make_create_blocks


@pytest.mark.parametrize("index, expected_type", [
    (0, String),
    (1, type(None)),
    (2, type(None)),
    (3, Block),
])
def test_create_blocks_states(index, expected_type):
    ctx = CreateBlocksContext(index=index, top_directive="DIR_", text="BODY_", line_number=10)
    fragment = Fragment(text="FRAG", line_number=20)
    func = make_create_blocks(ctx)

    result = func(fragment)
    assert isinstance(result, expected_type)
    assert ctx.index == index + 1


@pytest.mark.parametrize("index, top_dir, frag_text, expected_text", [
    (3, "DEF ", "FUNC", "DEF FUNC"),
])
def test_create_blocks_concatenation(index, top_dir, frag_text, expected_text):
    ctx = CreateBlocksContext(index=index, top_directive=top_dir, text="", line_number=5)
    fragment = Fragment(text=frag_text, line_number=6)
    func = make_create_blocks(ctx)

    result = func(fragment)
    assert result.text == expected_text