import logging
from pathlib import Path
import pytest
from unittest.mock import patch

from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.stop import Stop
from syncspec.include_directive import make_include_directive

CXT = Context("", "", {"k": "VAL\n"}, Path("in"), Path("kv"), Path("ig"))
TXT = "L1\nL2\nL3\n"

@pytest.mark.parametrize("params, outcome", [
    ({}, "return"),
    ({"include": "missing"}, "warn_return"),
    ({"include": "k", "head": "x"}, "error_stop"),
    ({"include": "k", "head": 2, "tail": 2}, "error_stop"),
    ({"include": "k"}, "replace"),
])
def test_include_directive(params, outcome):
    factory = make_include_directive(CXT)
    directive = Directive(
        parameters=params, prefix="p", text=TXT, suffix="s",
        path=Path("t.txt"), prefix_line_number=1, text_line_number=2, suffix_line_number=3
    )

    with patch("syncspec.include_directive.logging.warning") as m_warn, \
         patch("syncspec.include_directive.logging.error") as m_err:
        result = factory(directive)

    if outcome == "return":
        assert result is directive
    elif outcome == "warn_return":
        m_warn.assert_called_once()
        assert result is directive
    elif outcome == "error_stop":
        m_err.assert_called_once()
        assert isinstance(result, Stop)
    elif outcome == "replace":
        assert isinstance(result, Directive)
        assert result.text == "L1\nVAL\nL3\n"
        assert result is not directive