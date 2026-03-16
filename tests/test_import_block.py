import pytest
import logging
from pathlib import Path
from src.syncspec.import_block import make_import_block
from src.syncspec.import_block_context import ImportBlockContext
from src.syncspec.block import Block
from src.syncspec.string import String
from src.syncspec.node import Node


@pytest.fixture
def valid_context(tmp_path):
    return ImportBlockContext(import_path=str(tmp_path), open_delimiter="{{", close_delimiter="}}")


@pytest.fixture
def valid_block():
    return Block(
        directive={"import": "sub/file.txt"},
        prefix="p",
        suffix="s",
        text="line1\nline2\nline3\n",
        line_number=10,
        name="test_block"
    )


def test_no_import_key(valid_context, valid_block):
    func = make_import_block(valid_context)
    valid_block.directive = {}
    assert func(valid_block) is valid_block


def test_success_import(valid_context, valid_block, tmp_path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "file.txt").write_text("imported\n")
    func = make_import_block(valid_context)
    result = func(valid_block)

    assert isinstance(result, tuple)
    assert isinstance(result[0], String)
    assert isinstance(result[1], Node)
    assert isinstance(result[2], Node)
    assert "imported" in result[0].text


@pytest.mark.parametrize("directive, setup_file", [
    ({"import": 123}, False),
    ({"import": "../escape.txt"}, False),
    ({"import": "missing.txt"}, False),
    ({"import": "file.txt", "head": -1}, True),
    ({"import": "file.txt", "head": 10, "tail": 10}, True),
    ({"import": "file.txt", "head": True}, True),
])
def test_validation_failures(valid_context, valid_block, tmp_path, directive, setup_file):
    if setup_file:
        (tmp_path / "file.txt").write_text("content")
    (tmp_path / "sub").mkdir(exist_ok=True)

    valid_block.directive = directive
    func = make_import_block(valid_context)
    result = func(valid_block)

    assert result is None


def test_head_tail_extraction(valid_context, valid_block, tmp_path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "file.txt").write_text("imported_content\n")
    valid_block.directive = {"import": "sub/file.txt", "head": 1, "tail": 1}
    valid_block.text = "top\nmiddle\nbottom\n"

    func = make_import_block(valid_context)
    result = func(valid_block)

    assert result is not None
    assert "top\n" in result[0].text
    assert "imported_content\n" in result[0].text
    assert "bottom\n" in result[0].text


def test_node_properties(valid_context, valid_block, tmp_path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "file.txt").write_text("content\n")
    func = make_import_block(valid_context)
    result = func(valid_block)

    assert result[1].directive_type == "export"
    assert result[1].key == "sub/file.txt"
    assert result[1].line_number == 0
    assert result[2].directive_type == "import"
    assert result[2].key == "sub/file.txt"
    assert result[2].line_number == 10
    assert result[2].name == "test_block"