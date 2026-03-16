import pytest
import logging
from src.syncspec.include_block import make_include_block
from src.syncspec.block import Block
from src.syncspec.include_block_context import IncludeBlockContext


@pytest.mark.parametrize("directive, state, expect_block, error_substr", [
    ({}, {}, True, None),
    ({"include": 123}, {}, True, "string"),
    ({"include": "missing"}, {}, True, "not found"),
    ({"include": "k"}, {"k": 123}, True, "not a string"),
    ({"include": "k", "head": -1}, {"k": "v"}, True, "Head"),
    ({"include": "k", "head": True}, {"k": "v"}, True, "Head"),
    ({"include": "k", "tail": -1}, {"k": "v"}, True, "Tail"),
    ({"include": "k", "head": 5, "tail": 5}, {"k": "v"}, True, "overlap"),
    ({"include": "k", "head": 1, "tail": 1}, {"k": "v"}, False, None),
])
def test_include_block(directive, state, expect_block, error_substr, caplog):
    context = IncludeBlockContext(state=state, open_delimiter="[", close_delimiter="]")
    block = Block(
        directive=directive, prefix="P", suffix="S",
        text="1\n2\n3\n4\n5\n", line_number=10, name="test"
    )
    caplog.set_level(logging.ERROR)
    result = make_include_block(context)(block)

    if expect_block:
        assert result is block
        if error_substr is not None:
            assert any(error_substr in rec.message for rec in caplog.records)
        else:
            assert len(caplog.records) == 0
    else:
        assert isinstance(result, tuple)
        assert len(caplog.records) == 0