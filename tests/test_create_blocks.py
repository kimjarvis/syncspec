import pytest
from src.syncspec.create_blocks import make_create_blocks
from src.syncspec.create_blocks_context import CreateBlocksContext
from src.syncspec.fragment import Fragment
from src.syncspec.string import String
from src.syncspec.block import Block
from src.syncspec.error import Error


@pytest.fixture
def context():
    return CreateBlocksContext(index=0, prefix="", text="", line_number=1, name="test")


@pytest.mark.parametrize("index, expected_type, prefix, text, fragment_text", [
    (0, String, "", "", "data"),
    (1, type(None), "", "", "data"),
    (2, type(None), "data", "", "data"),
    (3, Block, '{"key": "value"}', "content", '{"other": "data"}'),
])
def test_create_blocks_sequence(context, index, expected_type, prefix, text, fragment_text):
    context.index = index
    context.prefix = prefix
    context.text = text
    fragment = Fragment(text=fragment_text, line_number=5)
    creator = make_create_blocks(context)

    result = creator(fragment)

    assert isinstance(result, expected_type)
    assert context.index == index + 1


def test_create_blocks_error_parsing(context):
    context.index = 3
    context.prefix = "invalid::json"
    context.text = "content"
    fragment = Fragment(text="also::invalid", line_number=10)
    creator = make_create_blocks(context)

    result = creator(fragment)

    assert isinstance(result, Error)
    assert context.index == 4


def test_create_blocks_invalid_keys(context):
    context.index = 3
    context.prefix = "null: value"  # YAML parses null key
    context.text = "content"
    fragment = Fragment(text="{}", line_number=10)
    creator = make_create_blocks(context)

    result = creator(fragment)

    assert isinstance(result, Error)


def test_create_blocks_full_cycle(context):
    """Test complete 4-call cycle building a Block."""
    creator = make_create_blocks(context)

    # Call 0: String
    result0 = creator(Fragment(text="line1", line_number=1))
    assert isinstance(result0, String)

    # Call 1: Set prefix
    result1 = creator(Fragment(text='{"prefix": "data"}', line_number=2))
    assert result1 is None

    # Call 2: Set text
    result2 = creator(Fragment(text="block content", line_number=3))
    assert result2 is None

    # Call 3: Create Block
    result3 = creator(Fragment(text='{"suffix": "info"}', line_number=4))
    assert isinstance(result3, Block)
    assert result3.directive == {"prefix": "data", "suffix": "info"}
    assert result3.text == "block content"