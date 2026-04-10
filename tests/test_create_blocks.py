import pytest
from pathlib import Path

from syncspec.create_blocks import make_create_blocks
from syncspec.context import Context
from syncspec.indexedfragment import IndexedFragment
from syncspec.text import Text
from syncspec.block import Block
from syncspec.stop import Stop

PATH = Path("src/test.py")


def get_ctx() -> Context:
    return Context("", "", {}, PATH, PATH, PATH)


def make_frag(idx: int) -> IndexedFragment:
    return IndexedFragment(PATH, f"t{idx}", idx * 10, idx)


@pytest.mark.parametrize("idx,expected", [
    (0, Text), (1, type(None)), (2, type(None)), (3, type(None)), (4, tuple)
])
def test_fragment_flow(idx: int, expected: type):
    fn = make_create_blocks(get_ctx())
    for i in range(idx + 1):
        res = fn(make_frag(i))

    if idx == 4:
        assert isinstance(res, tuple) and len(res) == 2
        assert isinstance(res[0], Block) and isinstance(res[1], Text)
    else:
        assert isinstance(res, expected)


def test_last_invalid_returns_stop(caplog):
    fn = make_create_blocks(get_ctx())
    fn.__closure__[0].cell_contents['last'] = True
    res = fn(make_frag(1))

    assert isinstance(res, Stop)
    assert "Unexpected fragment index" in caplog.text