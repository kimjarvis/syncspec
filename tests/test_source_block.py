import pytest
from src.syncspec.source_block import make_source_block
from src.syncspec.source_block_context import SourceBlockContext
from src.syncspec.block import Block
from src.syncspec.parameter_string import String
from src.syncspec.node import Node


@pytest.mark.parametrize(
    "directive, expected_type",
    [
        ({}, Block),
        ({"source": "key"}, tuple),
    ]
)
def test_directive_handling(directive, expected_type):
    ctx = SourceBlockContext(state={}, open_delimiter="[", close_delimiter="]")
    block = Block(directive=directive, prefix="", suffix="", text="a\nb\nc", line_number=1, name="test")
    func = make_source_block(ctx)
    result = func(block)
    assert isinstance(result, expected_type)


@pytest.mark.parametrize(
    "head, tail, text, should_fail",
    [
        (0, 0, "a\nb\nc", False),
        (1, 1, "a\nb\nc", False),
        (1, 1, "a", True),  # Fails with default 1+1=2 lines required
        (-1, 0, "a", True),
        (0, 5, "a\nb", True),
    ]
)
def test_head_tail_validation(head, tail, text, should_fail):
    ctx = SourceBlockContext(state={}, open_delimiter="[", close_delimiter="]")
    directive = {"source": "key", "head": head, "tail": tail}
    block = Block(directive=directive, prefix="", suffix="", text=text, line_number=1, name="test")
    func = make_source_block(ctx)
    result = func(block)

    if should_fail:
        assert isinstance(result, String)
        assert "key" not in ctx.state
    else:
        assert isinstance(result, tuple)
        assert "key" in ctx.state


def test_default_head_tail():
    ctx = SourceBlockContext(state={}, open_delimiter="[", close_delimiter="]")
    directive = {"source": "key"}  # Defaults to head=1, tail=1
    block = Block(directive=directive, prefix="", suffix="", text="line1\nline2\nline3", line_number=1, name="test")
    func = make_source_block(ctx)
    func(block)
    assert ctx.state["key"] == "line2"


def test_state_update():
    ctx = SourceBlockContext(state={}, open_delimiter="[", close_delimiter="]")
    directive = {"source": "my_key", "head": 1, "tail": 0}
    block = Block(directive=directive, prefix="", suffix="", text="line1\nline2", line_number=1, name="test")
    func = make_source_block(ctx)
    func(block)
    assert ctx.state["my_key"] == "line2"