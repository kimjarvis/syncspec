import pytest
from src.syncspec.source_block import make_source_block
from src.syncspec.block import Block
from src.syncspec.source_block_context import SourceBlockContext
from src.syncspec.error import Error
from src.syncspec.string import String
from src.syncspec.node import Node


@pytest.mark.parametrize(
    "directive,expected_type",
    [
        ({}, Block),
        ({"source": 123}, Error),
        ({"source": "key"}, tuple),
    ],
)
def test_source_directive_variations(directive, expected_type):
    ctx = SourceBlockContext(state={}, open_delimiter="<", close_delimiter=">")
    block = Block(directive=directive, prefix="", suffix="", text="content", line_number=1, name="test")
    result = make_source_block(ctx)(block)
    assert isinstance(result, expected_type)


@pytest.mark.parametrize(
    "text,head,tail,expected_state,error_expected",
    [
        ("a\nb\nc\n", 1, 1, "b\n", False),
        ("a\n", 1, 0, "", False),
        ("a\n", 2, 0, None, True),
        ("a\n", 0, 2, None, True),
    ],
)
def test_head_tail_processing(text, head, tail, expected_state, error_expected):
    ctx = SourceBlockContext(state={}, open_delimiter="<", close_delimiter=">")
    directive = {"source": "key", "head": head, "tail": tail}
    block = Block(directive=directive, prefix="", suffix="", text=text, line_number=1, name="test")
    result = make_source_block(ctx)(block)

    if error_expected:
        assert isinstance(result, Error)
    else:
        assert isinstance(result, tuple)
        assert ctx.state["key"] == expected_state