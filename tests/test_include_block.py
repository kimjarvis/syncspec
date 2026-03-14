import pytest
from src.syncspec.include_block import make_include_block
from src.syncspec.block import Block
from src.syncspec.include_block_context import IncludeBlockContext
from src.syncspec.string import String
from src.syncspec.node import Node
from src.syncspec.error import Error


@pytest.mark.parametrize(
    "directive, state, expected_type",
    [
        ({}, {}, Block),
        ({"include": 123}, {}, Error),
        ({"include": "missing"}, {}, Error),
        ({"include": "key"}, {"key": 123}, Error),
        ({"include": "key", "head": 10}, {"key": "a\nb"}, Error),
        ({"include": "key", "tail": 10}, {"key": "a\nb"}, Error),
        ({"include": "key"}, {"key": "content"}, tuple),
        ({"include": "key", "head": 1}, {"key": "a\nb"}, tuple),
        ({"include": "key", "tail": 1}, {"key": "a\nb"}, tuple),
    ],
)
def test_include_block_logic(directive, state, expected_type):
    ctx = IncludeBlockContext(state=state, open_delimiter="{", close_delimiter="}")
    block = Block(
        directive=directive,
        prefix="pre",
        suffix="suf",
        text="",
        line_number=1,
        name="test",
    )
    func = make_include_block(ctx)
    result = func(block)
    assert isinstance(result, expected_type)

    if expected_type is tuple:
        s, n = result
        assert isinstance(s, String)
        assert isinstance(n, Node)
        assert n.directive_type == "include"
        assert n.key == directive["include"]
    elif expected_type is Error:
        assert result.line_number == 1
        assert result.name == "test"
    elif expected_type is Block:
        assert result is block


def test_include_block_text_construction():
    ctx = IncludeBlockContext(state={"k": "line1\nline2"}, open_delimiter="[", close_delimiter="]")
    block = Block(
        directive={"include": "k", "head": 1},
        prefix="P",
        suffix="S",
        text="",
        line_number=5,
        name="N",
    )
    func = make_include_block(ctx)
    result = func(block)
    assert isinstance(result, tuple)
    s, _ = result
    assert s.text == "[P]line2[S]"
    assert s.line_number == 5