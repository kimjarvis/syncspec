import pytest
from pathlib import Path
from src.syncspec.import_block import make_import_block
from src.syncspec.block import Block
from src.syncspec.import_block_context import ImportBlockContext
from src.syncspec.string import String
from src.syncspec.node import Node
from src.syncspec.error import Error


@pytest.fixture
def context(tmp_path):
    return ImportBlockContext(import_path=str(tmp_path), open_delimiter="<%", close_delimiter="%>")


@pytest.fixture
def factory(context):
    return make_import_block(context)


@pytest.mark.parametrize("directive,expected_type", [
    ({}, Block),
    ({"import": 123}, Error),
    ({"import": "../escape.txt"}, Error),
    ({"import": "missing.txt"}, Error),
    ({"import": "valid.txt", "head": -1}, Error),
    ({"import": "valid.txt", "head": 10, "tail": 10}, Error),  # Overlap on small file
])
def test_import_block_conditions(factory, tmp_path, directive, expected_type):
    # Setup file
    (tmp_path / "valid.txt").write_text("line1\nline2\n", encoding='utf-8')

    block = Block(directive=directive, prefix="", suffix="", text="a\nb\n", line_number=1, name="test")
    result = factory(block)
    assert isinstance(result, expected_type)


def test_import_block_success(factory, tmp_path):
    (tmp_path / "inc.txt").write_text("CONTENT", encoding='utf-8')
    block = Block(
        directive={"import": "inc.txt", "head": 1, "tail": 0},
        prefix="P", suffix="S", text="H1\nH2\n", line_number=5, name="blk"
    )
    result = factory(block)
    assert isinstance(result, tuple)
    s, n1, n2 = result
    assert isinstance(s, String)
    assert isinstance(n1, Node) and n1.directive_type == "export"
    assert isinstance(n2, Node) and n2.directive_type == "import"
    assert "CONTENT" in s.text