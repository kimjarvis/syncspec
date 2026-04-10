import pytest
from pathlib import Path
from unittest.mock import patch
from syncspec.traverse_path import make_traverse_path
from syncspec.context import Context
from syncspec.dummy import Dummy
from syncspec.stop import Stop
from syncspec.file_path import FilePath


@pytest.mark.parametrize("setup_files, ignore_txt, expected_count", [
    ({"valid.txt": "{ok}"}, None, 1),
    ({"valid.txt": "no delimiters"}, None, 0),
    ({"skip.txt": "{ok}"}, "skip.txt", 0),
    ({"bin.dat": b"\x00data"}, None, 0),
    ({}, None, 0),
])
def test_traverse_paths(tmp_path, setup_files, ignore_txt, expected_count):
    for name, content in setup_files.items():
        p = tmp_path / name
        p.write_bytes(content if isinstance(content, bytes) else content.encode())

    ignore_file = tmp_path / ".ignore"
    if ignore_txt:
        ignore_file.write_text(ignore_txt)

    ctx = Context(
        open_delimiter="{", close_delimiter="}",
        keyvalue={}, input_path=tmp_path,
        keyvalue_file=tmp_path / "kv.txt",
        ignore_rules_file=ignore_file if ignore_txt else None
    )

    fn = make_traverse_path(ctx)
    result = fn(Dummy())
    assert isinstance(result, list)
    assert len(result) == expected_count
    if expected_count:
        assert isinstance(result[0], FilePath)


def test_bad_ignore_file_returns_stop(tmp_path):
    ctx = Context(
        open_delimiter="{", close_delimiter="}",
        keyvalue={}, input_path=tmp_path,
        keyvalue_file=tmp_path / "kv.txt",
        ignore_rules_file=tmp_path / ".badignore"
    )
    (tmp_path / ".badignore").write_text("[invalid")
    fn = make_traverse_path(ctx)
    assert isinstance(fn(Dummy()), Stop)


def test_symlink_escape_returns_stop(tmp_path):
    escape_dir = tmp_path.parent / "outside"
    escape_dir.mkdir(exist_ok=True)
    link = tmp_path / "bad_link"
    link.symlink_to(escape_dir / "secret.txt")

    ctx = Context(open_delimiter="{", close_delimiter="}", keyvalue={},
                  input_path=tmp_path, keyvalue_file=tmp_path / "kv", ignore_rules_file=None)

    # Mock places symlink in dirs to simulate directory escape
    with patch("os.walk", return_value=[(str(tmp_path), ["bad_link"], [])]):
        fn = make_traverse_path(ctx)
        assert isinstance(fn(Dummy()), Stop)