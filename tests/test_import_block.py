import pytest
import os
from pathlib import Path

from src.syncspec.import_block import make_import_block
from src.syncspec.block import Block
from src.syncspec.import_block_context import ImportBlockContext
from src.syncspec.string import String
from src.syncspec.node import Node
from src.syncspec.error import Error


@pytest.mark.parametrize("directive,expected_type,setup_file", [
    ({}, Block, False),
    ({"import": 123}, Error, False),
    ({"import": "/abs/path"}, Error, False),
    ({"import": "missing.txt"}, Error, False),
    ({"import": "../parent.txt"}, Error, True),
    ({"import": "valid.txt", "head": 10}, Error, True),
    ({"import": "valid.txt", "tail": 10}, Error, True),
    ({"import": "valid.txt"}, tuple, True),
    ({"import": "valid.txt", "head": 1, "tail": 1}, tuple, True),
    ({"import": "valid.txt", "head": 0, "tail": 0}, tuple, True),
    ({"import": "valid.txt", "head": -1}, Error, True),
    ({"import": "valid.txt", "tail": -1}, Error, True),
])
def test_import_block_logic(tmp_path, directive, expected_type, setup_file):
    import_dir = tmp_path / "imports"
    import_dir.mkdir()

    if setup_file and "import" in directive and isinstance(directive["import"], str):
        if directive["import"] != "missing.txt" and not directive["import"].startswith("../"):
            file_path = import_dir / "valid.txt"
            file_path.write_text("line1\nline2\nline3\n", encoding="utf-8")
        elif directive["import"].startswith("../"):
            parent_file = tmp_path / "parent.txt"
            parent_file.write_text("parent content\n", encoding="utf-8")

    ctx = ImportBlockContext(
        import_path=str(import_dir),
        open_delimiter="<%",
        close_delimiter="%>"
    )
    block = Block(
        directive=directive, prefix="pre ", suffix=" suf",
        text="", line_number=1, name="test_block"
    )

    func = make_import_block(ctx)
    result = func(block)

    if expected_type == tuple:
        assert isinstance(result, tuple)
        assert isinstance(result[0], String)
        assert isinstance(result[1], Node)
    else:
        assert isinstance(result, expected_type)


def test_import_block_head_tail_order(tmp_path):
    import_dir = tmp_path / "imports"
    import_dir.mkdir()

    file_path = import_dir / "content.txt"
    file_path.write_text("a\nb\nc\nd\n", encoding="utf-8")

    ctx = ImportBlockContext(
        import_path=str(import_dir),
        open_delimiter="[",
        close_delimiter="]"
    )
    block = Block(
        directive={"import": "content.txt", "head": 1, "tail": 1},
        prefix="", suffix="", text="", line_number=5, name="mod"
    )

    result = make_import_block(ctx)(block)
    assert isinstance(result, tuple)
    # Head first (remove first 1: a), then tail (remove last 1: d) -> b\nc\n
    assert result[0].text == "[]b\nc\n[]"
    assert result[1].key == "content.txt"


def test_import_block_subdirectory(tmp_path):
    import_dir = tmp_path / "imports"
    import_dir.mkdir()

    subdir = import_dir / "sub"
    subdir.mkdir()
    file_path = subdir / "nested.txt"
    file_path.write_text("nested content\n", encoding="utf-8")

    ctx = ImportBlockContext(
        import_path=str(import_dir),
        open_delimiter="<%",
        close_delimiter="%>"
    )
    block = Block(
        directive={"import": "sub/nested.txt"},
        prefix="", suffix="", text="", line_number=1, name="sub_test"
    )

    result = make_import_block(ctx)(block)
    assert isinstance(result, tuple)
    assert "nested content" in result[0].text


def test_import_block_symlink_to_parent_rejected(tmp_path):
    """Symlink target in parent directory should be rejected"""
    import_dir = tmp_path / "imports"
    import_dir.mkdir()

    parent_file = tmp_path / "parent.txt"
    parent_file.write_text("parent via symlink\n", encoding="utf-8")

    symlink_path = import_dir / "linked.txt"
    symlink_path.symlink_to(parent_file)

    ctx = ImportBlockContext(
        import_path=str(import_dir),
        open_delimiter="<%",
        close_delimiter="%>"
    )
    block = Block(
        directive={"import": "linked.txt"},
        prefix="", suffix="", text="", line_number=1, name="symlink_test"
    )

    result = make_import_block(ctx)(block)
    assert isinstance(result, Error)
    assert "escapes import directory" in result.message


def test_import_block_symlink_within_dir(tmp_path):
    """Symlink target within import directory should be accepted"""
    import_dir = tmp_path / "imports"
    import_dir.mkdir()

    target_file = import_dir / "target.txt"
    target_file.write_text("target content\n", encoding="utf-8")

    symlink_path = import_dir / "linked.txt"
    symlink_path.symlink_to(target_file)

    ctx = ImportBlockContext(
        import_path=str(import_dir),
        open_delimiter="<%",
        close_delimiter="%>"
    )
    block = Block(
        directive={"import": "linked.txt"},
        prefix="", suffix="", text="", line_number=1, name="symlink_test"
    )

    result = make_import_block(ctx)(block)
    assert isinstance(result, tuple)
    assert "target content" in result[0].text


def test_import_block_string_node_fields(tmp_path):
    import_dir = tmp_path / "imports"
    import_dir.mkdir()

    file_path = import_dir / "test.txt"
    file_path.write_text("hello\n", encoding="utf-8")

    ctx = ImportBlockContext(
        import_path=str(import_dir),
        open_delimiter="<%",
        close_delimiter="%>"
    )
    block = Block(
        directive={"import": "test.txt"},
        prefix="PRE ", suffix=" SUFF",
        text="", line_number=10, name="myblock"
    )

    result = make_import_block(ctx)(block)
    assert isinstance(result, tuple)
    assert result[0].line_number == 10
    assert result[0].name == "myblock"
    assert result[1].directive_type == "import"
    assert result[1].key == "test.txt"
    assert result[1].line_number == 10
    assert result[1].name == "myblock"


def test_import_block_head_zero(tmp_path):
    """head=0 should be a no-op"""
    import_dir = tmp_path / "imports"
    import_dir.mkdir()

    file_path = import_dir / "test.txt"
    file_path.write_text("line1\nline2\n", encoding="utf-8")

    ctx = ImportBlockContext(
        import_path=str(import_dir),
        open_delimiter="<%",
        close_delimiter="%>"
    )
    block = Block(
        directive={"import": "test.txt", "head": 0},
        prefix="", suffix="", text="", line_number=1, name="head_zero"
    )

    result = make_import_block(ctx)(block)
    assert isinstance(result, tuple)
    assert "line1\nline2\n" in result[0].text


def test_import_block_tail_zero(tmp_path):
    """tail=0 should be a no-op"""
    import_dir = tmp_path / "imports"
    import_dir.mkdir()

    file_path = import_dir / "test.txt"
    file_path.write_text("line1\nline2\n", encoding="utf-8")

    ctx = ImportBlockContext(
        import_path=str(import_dir),
        open_delimiter="<%",
        close_delimiter="%>"
    )
    block = Block(
        directive={"import": "test.txt", "tail": 0},
        prefix="", suffix="", text="", line_number=1, name="tail_zero"
    )

    result = make_import_block(ctx)(block)
    assert isinstance(result, tuple)
    assert "line1\nline2\n" in result[0].text