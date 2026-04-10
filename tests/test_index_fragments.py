import pytest
from pathlib import Path
from syncspec.context import Context
from syncspec.fragment import Fragment
from syncspec.index_fragments import make_index_fragments

_CTX = Context("", "", {}, Path("."), Path("."), Path("."))

@pytest.mark.parametrize(
    "frags, expected",
    [
        ([], []),
        ([Fragment(Path("a.py"), "x", 1)], [0]),
        ([Fragment(Path("a.py"), "x", 1), Fragment(Path("a.py"), "y", 2)], [0, 1]),
        ([Fragment(Path("a.py"), "x", 1), Fragment(Path("b.py"), "y", 1)], [0, 0]),
    ]
)
def test_index_fragments(frags, expected):
    indexer = make_index_fragments(_CTX)
    assert [indexer(f).index for f in frags] == expected