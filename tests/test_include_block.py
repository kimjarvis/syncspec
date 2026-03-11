import pytest
from src.syncspec.include_block import make_include_block
from src.syncspec.block import Block
from src.syncspec.include_block_context import IncludeBlockContext
from src.syncspec.string import String
from src.syncspec.error import Error

@pytest.mark.parametrize(
    "directive, state, exp_type, exp_text_sub, exp_err_sub",
    [
        ({}, {}, Block, None, None),
        ({"include": "k"}, {"k": "V"}, String, "{{pre}}V{{suf}}", None),
        ({"include": "missing"}, {}, Error, None, "not found"),
        ({"include": 123}, {}, Error, None, "must be a string"),
    ]
)
def test_include_block(directive, state, exp_type, exp_text_sub, exp_err_sub):
    ctx = IncludeBlockContext(state=state, open_delimiter="{{", close_delimiter="}}")
    block = Block(directive=directive, prefix="pre", suffix="suf", text="", line_number=10, name="test_block")
    result = make_include_block(ctx)(block)

    assert isinstance(result, exp_type)
    if isinstance(result, String):
        assert result.text == exp_text_sub
        assert result.line_number == 10
        assert result.name == "test_block"
    elif isinstance(result, Error):
        assert result.line_number == 10
        assert result.name == "test_block"
        assert exp_err_sub in result.message