import pytest
import sys
from pathlib import Path
import efr


@pytest.fixture(autouse=True)
def patch_base(monkeypatch, tmp_path):
    """Redirect BASE to a temporary directory for isolation"""
    monkeypatch.setattr(efr, "BASE", tmp_path)


@pytest.fixture
def setup_dirs(tmp_path):
    """Create required directory structure"""
    (tmp_path / "specs").mkdir()
    (tmp_path / "src" / "syncspec").mkdir(parents=True)
    (tmp_path / "tests").mkdir()
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "template.md").write_text("# {{ spec_name }}\n{{ spec_file }}")
    return tmp_path


@pytest.mark.parametrize("char", ['.', '/', '\n'])
def test_invalid_spec_chars(char):
    with pytest.raises(ValueError):
        efr.main(["--add", f"valid{char}name"])


def test_missing_directory(tmp_path):
    # Do not create dirs
    with pytest.raises(FileNotFoundError):
        efr.main(["--add", "valid"])


def test_missing_template(tmp_path):
    (tmp_path / "specs").mkdir()
    (tmp_path / "src" / "syncspec").mkdir(parents=True)
    (tmp_path / "tests").mkdir()
    # Do not create scripts/template.md
    with pytest.raises(FileNotFoundError):
        efr.main(["--add", "valid"])


def test_add_success(setup_dirs):
    efr.main(["--add", "My Spec"])
    assert (setup_dirs / "specs" / "My Spec.md").exists()
    assert (setup_dirs / "src" / "syncspec" / "my_spec.py").exists()
    assert (setup_dirs / "tests" / "test_my_spec.py").exists()
    # Check template rendering
    content = (setup_dirs / "specs" / "My Spec.md").read_text()
    assert "My Spec" in content
    assert "my_spec" in content


def test_add_atomic_failure(setup_dirs):
    # Pre-create one file to trigger atomic failure
    (setup_dirs / "tests" / "test_my_spec.py").touch()
    with pytest.raises(FileExistsError):
        efr.main(["--add", "My Spec"])
    # Ensure no new files were created (specs md should not exist)
    assert not (setup_dirs / "specs" / "My Spec.md").exists()


def test_remove_success(setup_dirs):
    # Create files first (matching add logic)
    (setup_dirs / "src" / "syncspec" / "my_spec.py").touch()
    (setup_dirs / "tests" / "test_my_spec.py").touch()

    efr.main(["--remove", "My Spec"])

    assert not (setup_dirs / "src" / "syncspec" / "my_spec.py").exists()
    assert not (setup_dirs / "tests" / "test_my_spec.py").exists()
    # Ensure specs md is NOT removed per spec
    (setup_dirs / "specs" / "My Spec.md").touch()
    assert (setup_dirs / "specs" / "My Spec.md").exists()


def test_remove_atomic_failure(setup_dirs):
    # Create only one file to trigger atomic failure
    (setup_dirs / "src" / "syncspec" / "my_spec.py").touch()
    # tests/test_my_spec.py is missing

    with pytest.raises(FileNotFoundError):
        efr.main(["--remove", "My Spec"])

    # Ensure existing file was NOT removed (atomicity)
    assert (setup_dirs / "src" / "syncspec" / "my_spec.py").exists()


def test_mutually_exclusive(capsys):
    with pytest.raises(SystemExit):
        efr.main(["--add", "--remove", "spec"])
    # Capture and discard output to prevent console noise
    capsys.readouterr()