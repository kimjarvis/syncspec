import pytest
from src.syncspec.create_blocks import make_create_blocks
from src.syncspec.create_blocks_context import CreateBlocksContext
from src.syncspec.fragment import Fragment
from src.syncspec.string import String
from src.syncspec.block import Block
from src.syncspec.error import Error

@pytest.mark.parametrize("index,expected_type,prefix,text,fragment_text", [
    (0, String, "", "", "data"),
    (1, type(None), "", "", "data"),
    (2, type(None), "", "", "data"),
    (3, Block, '{"a": 1}', "body", '{"b": 2}'),
])
def test_state_routing(index, expected_type, prefix, text, fragment_text):
    ctx = CreateBlocksContext(index=index, prefix=prefix, text=text, line_number=0)
    fn = make_create_blocks(ctx)
    frag = Fragment(fragment_text, 1, "test")
    res = fn(frag)
    if expected_type != type(None):
        assert isinstance(res, expected_type)
    else:
        assert res is None
    assert ctx.index == index + 1

@pytest.mark.parametrize("prefix,suffix,should_fail,expected_directive", [
    ('{"a": 1}', '{"b": 2}', False, {"a": 1, "b": 2}),
    ('{a: 1}', '{b: 2}', False, {"a": 1, "b": 2}),
    ("invalid", "invalid", True, None),
    ('{null: 1}', '{b: 2}', True, None),
])
def test_block_parsing(prefix, suffix, should_fail, expected_directive):
    ctx = CreateBlocksContext(index=3, prefix=prefix, text="body", line_number=5)
    fn = make_create_blocks(ctx)
    frag = Fragment(suffix, 6, "frag")
    res = fn(frag)
    if should_fail:
        assert isinstance(res, Error)
    else:
        assert isinstance(res, Block)
        assert res.directive == expected_directive