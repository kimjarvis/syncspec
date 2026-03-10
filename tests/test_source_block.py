import pytest
from src.syncspec.source_block import make_source_block
from src.syncspec.block import Block
from src.syncspec.string import String
from src.syncspec.source_block_context import SourceBlockContext


@pytest.mark.parametrize(
    "directive, prefix, suffix, expected_type, check_state",
    [
        ({"source": "k"}, "p", "s", String, True),
        ({"source": "k"}, None, "s", String, True),
        ({"other": "v"}, "p", "s", Block, False),
        ({}, "p", "s", Block, False),
    ]
)
def test_source_block(directive, prefix, suffix, expected_type, check_state):
    context = SourceBlockContext(state={}, open_delimiter="{", close_delimiter="}")
    transformer = make_source_block(context)
    block = Block(directive=directive, prefix=prefix, suffix=suffix, text="t", line_number=1)

    result = transformer(block)

    assert isinstance(result, expected_type)
    if check_state:
        assert context.state["k"] == "t"
        exp_prefix = prefix or ""
        # Constructs: { + prefix + } + text + { + suffix + }
        assert result.text == f"{{{exp_prefix}}}t{{{suffix}}}"
    else:
        assert result is block