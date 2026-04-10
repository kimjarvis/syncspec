import pytest
from pathlib import Path
from unittest.mock import patch
from syncspec.cli import parse_args, main

def test_defaults(tmp_path):
    args = parse_args([str(tmp_path)])
    assert args.open_delimiter == "{-"
    assert args.close_delimiter == "-}"
    assert args.keyvalue is None

@pytest.mark.parametrize("flag", ["--keyvalue", "--ignore_rules"])
def test_missing_optional_file_raises(flag, tmp_path):
    missing = tmp_path / "missing.txt"
    with pytest.raises(SystemExit):
        parse_args([str(tmp_path), flag, str(missing)])

def test_keyvalue_bad_suffix_raises(tmp_path):
    bad_file = tmp_path / "config.yaml"
    bad_file.touch()
    with pytest.raises(SystemExit):
        parse_args([str(tmp_path), "--keyvalue", str(bad_file)])

def test_input_not_dir_raises():
    with pytest.raises(SystemExit):
        parse_args(["/nonexistent"])

@patch("syncspec.cli.machine")
def test_main_invokes_machine(mock_machine, tmp_path):
    with pytest.raises(SystemExit):
        main([str(tmp_path)])
    mock_machine.assert_called_once()
    ctx = mock_machine.call_args.args[0]
    assert ctx.keyvalue == {}
    assert ctx.input_path == tmp_path.resolve()