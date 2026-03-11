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
        ({"other": "val"}, {}, Block),
        ({"include": "key1"}, {"key1": "val"}, tuple),
        ({"include": "missing"}, {}, Error),
        ({"include": 123}, {}, Error),
    ]
)
def test_include_block_logic(directive, state, expected_type):
    context = IncludeBlockContext(state=state, open_delimiter="{{", close_delimiter="}}")
    func = make_include_block(context)

    block = Block(
        directive=directive,
        prefix="pre ",
        suffix=" suf",
        text="",
        line_number=1,
        name="test"
    )

    result = func(block)
    assert isinstance(result, expected_type)

    if expected_type == tuple:
        s, n = result
        assert isinstance(s, String)
        assert isinstance(n, Node)
        assert s.text == "{{pre }}val{{ suf}}"
        assert n.key == "key1"
        assert n.directive_type == "include"
    elif expected_type == Error:
        assert result.line_number == 1