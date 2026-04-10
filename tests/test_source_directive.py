import pytest
import logging
from pathlib import Path
from syncspec.source_directive import make_source_directive
from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.stop import Stop

@pytest.fixture
def ctx():
    return Context(open_delimiter="", close_delimiter="", keyvalue={}, input_path=Path("."), keyvalue_file=Path("."), ignore_rules_file=Path("."))

@pytest.fixture
def fn(ctx):
    return make_source_directive(ctx)

def mk_directive(text, params, line=1):
    return Directive(parameters=params, prefix="", text=text, suffix="", path=Path("f.py"), prefix_line_number=line, text_line_number=line+1, suffix_line_number=line+2)

@pytest.mark.parametrize("text, head, tail, expected", [
    ("a\nb\nc\nd\n", 1, 1, "b\nc\n"),
    ("\na\nb\nc\n", 0, 1, "a\nb\n"),
    ("a\nb\nc", 1, 1, "b\n"),
])
def test_normal_trimming(fn, ctx, text, head, tail, expected):
    res = fn(mk_directive(text, {"source": "k", "head": head, "tail": tail}))
    assert isinstance(res, Directive) and ctx.keyvalue["k"] == expected

def test_no_source_key(fn):
    d = mk_directive("x", {})
    assert fn(d) is d

def test_invalid_head_tail(fn, caplog):
    d = mk_directive("x\n", {"source": "k", "head": "a"})
    with caplog.at_level(logging.ERROR):
        assert isinstance(fn(d), Stop)
        assert any("must be integers" in r.message for r in caplog.records)

def test_insufficient_lines(fn, caplog):
    d = mk_directive("x\n", {"source": "k", "head": 2, "tail": 0})
    with caplog.at_level(logging.ERROR):
        assert isinstance(fn(d), Stop)
        assert any("Cannot remove" in r.message for r in caplog.records)

def test_duplicate_key(fn, ctx, caplog):
    ctx.keyvalue["dup"] = "old"
    d = mk_directive("a\nb\n", {"source": "dup", "head": 1, "tail": 1})
    with caplog.at_level(logging.ERROR):
        assert isinstance(fn(d), Stop)
        assert any("already exists" in r.message for r in caplog.records)