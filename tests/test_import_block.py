import pytest
from pathlib import Path
from src.syncspec.import_block import make_import_block
from src.syncspec.block import Block
from src.syncspec.import_block_context import ImportBlockContext
from src.syncspec.string import String
from src.syncspec.node import Node

@pytest.mark.parametrize("directive,expected_type", [
    ({}, Block),
    ({"import": "valid.txt"}, tuple),
])
def test_import_key_presence(tmp_path, directive, expected_type):
    ctx = ImportBlockContext(import_path=str(tmp_path), open_delimiter="<", close_delimiter=">")
    func = make_import_block(ctx)
    (tmp_path / "valid.txt").write_text("content")
    block = Block(directive=directive, prefix="", suffix="", text="", line_number=1, name="test")
    result = func(block)
    assert isinstance(result, expected_type)

@pytest.mark.parametrize("import_path,should_fail", [
    ("valid.txt", False),
    ("../etc/passwd", True),
    ("missing.txt", True),
])
def test_path_security(tmp_path, import_path, should_fail):
    (tmp_path / "valid.txt").write_text("content")
    ctx = ImportBlockContext(import_path=str(tmp_path), open_delimiter="<", close_delimiter=">")
    func = make_import_block(ctx)
    block = Block(directive={"import": import_path}, prefix="", suffix="", text="", line_number=1, name="test")
    result = func(block)
    if should_fail:
        assert isinstance(result, String)
    else:
        assert isinstance(result, tuple)

@pytest.mark.parametrize("head, tail, block_lines, should_fail", [
    (0, 0, 5, False),
    (1, 1, 5, False),
    (3, 3, 5, True),  # Overlap: 3+3 > 5
    (-1, 0, 5, True),  # Negative head
    (True, 0, 5, True),  # Bool head
    (0, True, 5, True),  # Bool tail
])
def test_head_tail_validation(tmp_path, head, tail, block_lines, should_fail):
    (tmp_path / "valid.txt").write_text("imported content")
    ctx = ImportBlockContext(import_path=str(tmp_path), open_delimiter="<", close_delimiter=">")
    func = make_import_block(ctx)
    # block.text must have enough lines for head/tail validation
    block_text = "\n".join(["block_line"] * block_lines)
    block = Block(
        directive={"import": "valid.txt", "head": head, "tail": tail},
        prefix="", suffix="", text=block_text, line_number=1, name="test"
    )
    result = func(block)
    if should_fail:
        assert isinstance(result, String)
    else:
        assert isinstance(result, tuple)

def test_return_structure(tmp_path):
    (tmp_path / "valid.txt").write_text("imported")
    ctx = ImportBlockContext(import_path=str(tmp_path), open_delimiter="<", close_delimiter=">")
    func = make_import_block(ctx)
    block = Block(
        directive={"import": "valid.txt"},
        prefix="pre", suffix="suf", text="block", line_number=10, name="myblock"
    )
    result = func(block)
    assert isinstance(result, tuple)
    assert len(result) == 3
    s, n_export, n_import = result
    assert isinstance(s, String)
    assert isinstance(n_export, Node)
    assert isinstance(n_import, Node)
    assert n_export.directive_type == "export"
    assert n_import.directive_type == "import"
    assert n_import.line_number == 10