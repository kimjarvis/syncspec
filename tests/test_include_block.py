import pytest
from src.syncspec.include_block import make_include_block
from src.syncspec.block import Block
from src.syncspec.string import String
from src.syncspec.error import Error
from src.syncspec.include_block_context import IncludeBlockContext


@pytest.mark.parametrize(
    "directive, state, expected_type",
    [
        ({"other": "val"}, {}, Block),
        ({"include": "key1"}, {"key1": "content"}, String),
        ({"include": "missing"}, {}, Error),
    ]
)
def test_include_block(directive, state, expected_type):
    context = IncludeBlockContext(state=state, open_delimiter="<", close_delimiter=">")
    block = Block(
        directive=directive,
        prefix="[",
        suffix="]",
        text="original",
        line_number=1
    )
    result = make_include_block(context)(block)
    assert isinstance(result, expected_type)
    if isinstance(result, Error):
        assert result.name == "test"
        assert "not found" in result.message