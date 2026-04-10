import json
import logging
import pytest
from pathlib import Path
from unittest.mock import MagicMock

from syncspec.context import Context
from syncspec.text import Text
from syncspec.stop import Stop
from syncspec.write_keyfile import make_write_keyfile


@pytest.fixture
def ctx(tmp_path):
    return Context(
        open_delimiter="{{", close_delimiter="}}", keyvalue={"a": 1},
        input_path=tmp_path / "in.txt", keyvalue_file=tmp_path / "out.json",
        ignore_rules_file=tmp_path / "ignore.txt"
    )


@pytest.fixture
def txt():
    return Text(path=Path("dummy.txt"), text="dummy", line_number=10)


@pytest.mark.parametrize("last, expect_type", [
    (True, Text),
    (False, Text),
])
def test_returns_text_on_success(ctx, txt, last, expect_type):
    fn = make_write_keyfile(ctx)
    fn.state["last"] = last
    result = fn(txt)
    assert isinstance(result, expect_type)
    if last:
        assert json.loads(ctx.keyvalue_file.read_text()) == {"a": 1}


@pytest.mark.parametrize("last, expect_type, should_log", [
    (True, Stop, True),
    (False, Text, False),
])
def test_handles_serialization_failure(ctx, txt, last, expect_type, should_log, caplog):
    ctx.keyvalue = {object(): 1}  # Non-JSON serializable
    fn = make_write_keyfile(ctx)
    fn.state["last"] = last

    with caplog.at_level(logging.ERROR):
        result = fn(txt)

    assert isinstance(result, expect_type)
    if should_log:
        assert "Failed to write keyvalue file" in caplog.text


@pytest.mark.parametrize("last, expect_type", [(True, Text)])
def test_skips_when_no_file(ctx, txt, last, expect_type):
    ctx.keyvalue_file = None
    fn = make_write_keyfile(ctx)
    fn.state["last"] = last
    assert isinstance(fn(txt), expect_type)