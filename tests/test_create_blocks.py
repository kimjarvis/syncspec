import pytest
from src.syncspec.create_blocks import make_create_blocks
from src.syncspec.create_blocks_context import CreateBlocksContext
from src.syncspec.fragment import Fragment
from src.syncspec.parameter_string import String
from src.syncspec.block import Block


@pytest.fixture
def ctx():
    return CreateBlocksContext(0, "", 0, False, {}, "", "[", "]")


@pytest.fixture
def frag():
    return Fragment("data", 10, "test")


@pytest.mark.parametrize("idx", [0, 4, 8])
def test_state_0_returns_string(ctx, frag, idx):
    ctx.index = idx
    fn = make_create_blocks(ctx)
    res = fn(frag)
    assert isinstance(res, String) and res.text == "data"
    assert ctx.index == idx + 1


@pytest.mark.parametrize("txt,valid", [
    ("{}", True), ('{"k":"v"}', True), ('"k":"v"', True), ("", True),
    ("invalid", False), ("{unclosed", False),
])
def test_state_1_json_validation(ctx, frag, txt, valid):
    ctx.index = 1
    frag.text = txt
    fn = make_create_blocks(ctx)
    res = fn(frag)
    if valid:
        assert res is None and ctx.prefix_valid
    else:
        assert isinstance(res, String) and not ctx.prefix_valid
        assert res.text == f"[{txt}]"


@pytest.mark.parametrize("idx,valid,expect_none", [(2, True, True), (2, False, False), (6, True, True)])
def test_state_2_dependent_on_prefix(ctx, frag, idx, valid, expect_none):
    ctx.index = idx
    ctx.prefix_valid = valid
    fn = make_create_blocks(ctx)
    res = fn(frag)
    if expect_none:
        assert res is None and ctx.text == "data"
    else:
        assert isinstance(res, String) and res.text == "data"  # No delimiters in State 2 error


@pytest.mark.parametrize("idx,valid,expect_block", [(3, True, True), (3, False, False), (7, True, True)])
def test_state_3_builds_block_or_string(ctx, frag, idx, valid, expect_block):
    ctx.index = idx
    ctx.prefix_valid = valid
    ctx.prefix = "pre"
    ctx.prefix_line_number = 5
    ctx.directive = {"k": "v"}
    ctx.text = "body"
    fn = make_create_blocks(ctx)
    res = fn(frag)
    if expect_block:
        assert isinstance(res, Block) and res.prefix == "pre" and res.line_number == 5
    else:
        assert isinstance(res, String) and res.text == "[data]"  # Delimiters in State 3 error