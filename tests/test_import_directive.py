import pytest
from pathlib import Path
from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.stop import Stop
from syncspec.import_directive import make_import_directive

@pytest.fixture
def ctx(tmp_path):
    root = tmp_path / "input"
    root.mkdir()
    return Context("", "", {}, root, root/"kv", root/"ign")

@pytest.fixture
def doc(tmp_path, ctx):
    p = ctx.input_path / "doc.txt"
    p.write_text("T1\nT2\nM1\nB1\nB2\n")
    return Directive({}, "", "T1\nT2\nM1\nB1\nB2\n", "", p, 1, 2, 6)

@pytest.mark.parametrize("params,assertion", [
    ({}, lambda d: isinstance(d, Directive)),
    ({"import": "inc.txt", "head": 2, "tail": 2}, lambda d: d.text.startswith("T1\nT2\nimported\nB1\nB2\n")),
    ({"import": "inc.txt"}, lambda d: "imported\n" in d.text),
])
def test_import_success(ctx, doc, params, assertion, tmp_path):
    (ctx.input_path / "inc.txt").write_text("imported")
    doc.parameters = params
    assert assertion(make_import_directive(ctx)(doc))

@pytest.mark.parametrize("params", [
    {"import": "../escape.txt"},
    {"import": "inc.txt", "head": "str"},
    {"import": "inc.txt", "head": 10},
    {"import": "bin.dat"},
    {"import": "symlink.txt"},
])
def test_import_failure_returns_stop(ctx, doc, params, tmp_path):
    (ctx.input_path / "inc.txt").write_text("data\n")
    (tmp_path / "escape.txt").write_text("no\n")
    (ctx.input_path / "bin.dat").write_bytes(b"\x80\x81")
    (ctx.input_path / "symlink.txt").symlink_to(tmp_path / "outside.txt")
    doc.parameters = params
    assert isinstance(make_import_directive(ctx)(doc), Stop)