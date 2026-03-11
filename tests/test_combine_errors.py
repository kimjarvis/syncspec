import pytest
from src.syncspec.error import Error
from src.syncspec.combine_errors_context import CombineErrorsContext
from src.syncspec.combine_errors import make_combine_errors

@pytest.mark.parametrize("message, name, line, expected", [
    ("Fail", "a.py", 1, "Error: Fail\nLine: 1\nFile: a.py\n\n"),
    ("Stop", "b.py", 2, "Error: Stop\nLine: 2\nFile: b.py\n\n"),
])
def test_combine_errors_single(message, name, line, expected):
    ctx = CombineErrorsContext(text="")
    combiner = make_combine_errors(ctx)
    combiner(Error(message=message, name=name, line_number=line))
    assert ctx.text == expected

def test_combine_errors_accumulate():
    ctx = CombineErrorsContext(text="")
    combiner = make_combine_errors(ctx)
    combiner(Error("A", "x", 1))
    combiner(Error("B", "y", 2))
    assert ctx.text.count("Error:") == 2