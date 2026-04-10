import pytest
from pathlib import Path

from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.stop import Stop
from syncspec.export_directive import make_export_directive

@pytest.fixture
def context(tmp_path):
    return Context(
        open_delimiter="{{", close_delimiter="}}", keyvalue={},
        input_path=tmp_path, keyvalue_file=Path(), ignore_rules_file=Path()
    )

@pytest.fixture
def directive(tmp_path):
    p = tmp_path / "sub" / "source.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    return Directive(
        parameters={}, prefix="", text="1\n2\n3\n4\n5\n", suffix="",
        path=p, prefix_line_number=5, text_line_number=6, suffix_line_number=7
    )

@pytest.mark.parametrize("params,expected", [
    ({}, Directive),
    ({"export": "out.txt", "head": 1, "tail": 1}, Directive),
    ({"export": "../../escape.txt"}, Stop),
    ({"export": "out.txt", "head": "invalid"}, Stop),
    ({"export": "out.txt", "head": 10}, Stop),
    ({"export": "out.txt", "tail": 10}, Stop),
])
def test_export_directive(context, directive, params, expected):
    directive.parameters.update(params)
    func = make_export_directive(context)
    result = func(directive)
    assert isinstance(result, expected)
    if expected is Directive and "export" in params:
        out_file = directive.path.parent / params["export"]
        assert out_file.exists()
        assert out_file.read_text().startswith("2\n")