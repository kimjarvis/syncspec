import json
import pytest
from pathlib import Path
from unittest.mock import patch

from syncspec.context import Context
from syncspec.dummy import Dummy
from syncspec.stop import Stop
from syncspec.validate_context import make_validate_context

@pytest.mark.parametrize("od,cd,stop", [
    ("{{", "}}", False), ("", "}}", True), ("{{", "", True),
    ("{{", "{{", True), ("{", "{{", True), ("{{", "{", True),
    ("{\n", "}", True), ("{", "}\n", True),
])
def test_delimiter_validation(tmp_path, od, cd, stop):
    ctx = Context(od, cd, {}, tmp_path, None, None)
    assert isinstance(make_validate_context(ctx)(Dummy()), Stop if stop else Dummy)

def test_json_read_success(tmp_path):
    f = tmp_path / "cfg.json"; f.write_text('{"a":1}')
    ctx = Context("{{", "}}", {}, tmp_path, f, None)
    assert isinstance(make_validate_context(ctx)(Dummy()), Dummy) and ctx.keyvalue == {"a":1}

@pytest.mark.parametrize("bad", ['{"x":}', '', 'raw'])
def test_json_read_failure(tmp_path, bad):
    f = tmp_path / "bad.json"; f.write_text(bad)
    ctx = Context("{{", "}}", {}, tmp_path, f, None)
    assert isinstance(make_validate_context(ctx)(Dummy()), Stop)

def test_ignore_rules_fallback(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".syncspec_ignore").write_text("*.log\n")
    ctx = Context("{{", "}}", {}, tmp_path, None, None)
    res = make_validate_context(ctx)(Dummy())
    assert isinstance(res, Dummy) and ctx.ignore_rules_file == Path(".syncspec_ignore")

def test_ignore_rules_compile_error(tmp_path):
    f = tmp_path / "rules.ignore"; f.write_text("valid")
    ctx = Context("{{", "}}", {}, tmp_path, None, f)
    with patch("pathspec.PathSpec.from_lines", side_effect=Exception("bad")):
        assert isinstance(make_validate_context(ctx)(Dummy()), Stop)

def test_logging_to_file(tmp_path):
    lf = tmp_path / "test.log"
    ctx = Context("{{", "}}", {}, tmp_path, None, None)
    ctx.log_file = lf
    res = make_validate_context(ctx)(Dummy())
    assert isinstance(res, Dummy) and "Syncspec started" in lf.read_text()