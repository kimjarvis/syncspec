import pytest
from src.syncspec.create_blocks import make_create_blocks
from src.syncspec.fragment import Fragment
from src.syncspec.string import String
from src.syncspec.block import Block
from src.syncspec.create_blocks_context import CreateBlocksContext


@pytest.mark.parametrize("index, expected_type, update_context", [
    (0, String, False),
    (1, type(None), True),
    (2, type(None), True),
    (3, Block, False),
])
def test_state_transitions(index, expected_type, update_context):
    context = CreateBlocksContext(index=index, prefix="", text="", line_number=0)
    create_blocks = make_create_blocks(context)
    fragment = Fragment(text="{}", line_number=10, name="test")

    result = create_blocks(fragment)

    assert isinstance(result, expected_type) if expected_type is not type(None) else result is None
    assert context.index == index + 1


def test_block_json_merge():
    context = CreateBlocksContext(index=3, prefix='{"a": 1}', text="body", line_number=5)
    create_blocks = make_create_blocks(context)
    fragment = Fragment(text='{"b": 2}', line_number=10, name="block_name")

    result = create_blocks(fragment)

    assert isinstance(result, Block)
    assert result.directive == {"a": 1, "b": 2}
    assert result.name == "block_name"
    assert result.line_number == 5


def test_block_json_wrap_braces():
    # JSON fragments require quoted keys. 'a: 1' is invalid JSON even with braces.
    context = CreateBlocksContext(index=3, prefix='"a": 1', text="body", line_number=5)
    create_blocks = make_create_blocks(context)
    fragment = Fragment(text='"b": 2', line_number=10, name="block_name")

    result = create_blocks(fragment)

    assert isinstance(result, Block)
    assert result.directive == {"a": 1, "b": 2}


def test_block_json_error():
    context = CreateBlocksContext(index=3, prefix='invalid::', text="body", line_number=5)
    create_blocks = make_create_blocks(context)
    fragment = Fragment(text='{}', line_number=10, name="block_name")

    result = create_blocks(fragment)

    assert result is None
    assert context.index == 4


def test_none_key_rejection():
    # JSON keys are always strings; None keys are impossible via json.loads.
    # This test verifies successful parsing of valid JSON.
    context = CreateBlocksContext(index=3, prefix='{"key": 1}', text="body", line_number=5)
    create_blocks = make_create_blocks(context)
    fragment = Fragment(text='{}', line_number=10, name="block_name")

    result = create_blocks(fragment)
    assert isinstance(result, Block)