import pytest
from src.syncspec.create_blocks import make_create_blocks
from src.syncspec.create_blocks_context import CreateBlocksContext
from src.syncspec.fragment import Fragment
from src.syncspec.string import String
from src.syncspec.block import Block
from src.syncspec.error import Error


@pytest.mark.parametrize("index, exp_type", [
    (0, String), (1, type(None)), (2, type(None)), (3, Block)
])
def test_state_sequence(index, exp_type):
    ctx = CreateBlocksContext(index=index, prefix="", text="", line_number=0)
    fn = make_create_blocks(ctx)
    frag = Fragment(text="{}", line_number=1, name="test")

    # Pre-fill context for state 3
    if index == 3:
        ctx.prefix = "{}"
        ctx.text = "body"
        ctx.line_number = 1

    result = fn(frag)
    assert isinstance(result, exp_type)
    assert ctx.index == index + 1


@pytest.mark.parametrize("prefix, suffix, expect_error", [
    ("{}", "{}", False),
    ("", "", False),
    ("invalid", "{}", True),
    ("{}", "invalid", True),
    ('{"key": null}', "{}", False),
])
def test_json_parsing(prefix, suffix, expect_error):
    ctx = CreateBlocksContext(index=3, prefix=prefix, text="body", line_number=1)
    fn = make_create_blocks(ctx)
    frag = Fragment(text=suffix, line_number=2, name="json_test")

    result = fn(frag)
    if expect_error:
        assert isinstance(result, Error)
    else:
        assert isinstance(result, Block)
        assert isinstance(result.directive, dict)


def test_none_key_rejection():
    # Simulating a case where None key might exist (though standard json prevents it)
    # We test the validation logic explicitly if _parse_json were modified,
    # but standard json.loads won't produce None keys.
    # This test verifies the Block creation path works normally.
    ctx = CreateBlocksContext(index=3, prefix='{"a": 1}', text="body", line_number=1)
    fn = make_create_blocks(ctx)
    frag = Fragment(text='{"b": 2}', line_number=2, name="merge_test")
    result = fn(frag)
    assert isinstance(result, Block)
    assert result.directive == {"a": 1, "b": 2}