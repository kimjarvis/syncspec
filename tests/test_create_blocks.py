import pytest
from src.syncspec.create_blocks import make_create_blocks
from src.syncspec.fragment import Fragment
from src.syncspec.block import Block
from src.syncspec.error import Error
from src.syncspec.create_blocks_context import CreateBlocksContext


@pytest.mark.parametrize("index,expected_type", [
    (0, Block),
    (1, type(None)),
    (2, type(None)),
    (3, Block),
])
def test_state_progression(index, expected_type):
    ctx = CreateBlocksContext(index=index, prefix="", text="", line_number=1, name="test")
    fn = make_create_blocks(ctx)
    result = fn(Fragment(text="data", line_number=1))
    assert isinstance(result, expected_type)
    assert ctx.index == index + 1


@pytest.mark.parametrize("prefix,suffix,expected_type", [
    ('{"k": 1}', '{"v": 2}', Block),
    ('"k": 1', '"v": 2', Block),
    ('k: 1', 'v: 2', Block),
    ('!', 'k: 1', Error),
    ('', '', Block),
    ('~', 'k: 1', Error),
    ('{null: 1}', 'k: 1', Error),
])
def test_parsing_logic(prefix, suffix, expected_type):
    ctx = CreateBlocksContext(index=3, prefix=prefix, text="body", line_number=1, name="test")
    fn = make_create_blocks(ctx)
    result = fn(Fragment(text=suffix, line_number=1))
    assert isinstance(result, expected_type)
    if isinstance(result, Block):
        assert isinstance(result.directive, dict)
        assert all(isinstance(k, str) for k in result.directive.keys())


def test_state_0_block_structure():
    ctx = CreateBlocksContext(index=0, prefix="", text="", line_number=1, name="test")
    fn = make_create_blocks(ctx)
    result = fn(Fragment(text="content", line_number=5))
    assert isinstance(result, Block)
    assert result.text == "content"
    assert result.line_number == 5
    assert result.prefix is None
    assert result.suffix is None
    assert result.directive == {'text': ''}


@pytest.mark.parametrize("index,prefix,text,suffix,expected_keys", [
    (0, "", "", "frag", []),
    (1, "pre", "", "frag", []),
    (2, "pre", "txt", "frag", []),
    (3, '"k": 1', "body", '"v": 2', ["k", "v"]),
])
def test_block_content(index, prefix, text, suffix, expected_keys):
    ctx = CreateBlocksContext(index=index, prefix=prefix, text=text, line_number=1, name="test")
    fn = make_create_blocks(ctx)
    result = fn(Fragment(text=suffix, line_number=1))
    if isinstance(result, Block):
        if index == 0:
            assert result.prefix is None
            assert result.suffix is None
        else:
            assert result.prefix == prefix
            assert result.suffix == suffix
            assert all(k in result.directive for k in expected_keys)