import pytest
from pathlib import Path
from syncspec.context import Context
from syncspec.text import Text
from syncspec.defragment_text import make_defragment_text

def _state(fn):
    return fn.__closure__[0].cell_contents

@pytest.mark.parametrize("chunks, expected", [
    ([(Path("a.txt"), "hello ", False), (Path("a.txt"), "world", True)], "hello world"),
    ([(Path("b.txt"), "line1\n", False), (Path("b.txt"), "line2", True)], "line1\nline2"),
    ([(Path("c.txt"), "single", True)], "single"),
])
def test_defragment_text(tmp_path, chunks, expected):
    ctx = Context(open_delimiter="", close_delimiter="", keyvalue={}, input_path=tmp_path, keyvalue_file=tmp_path, ignore_rules_file=tmp_path)
    defrag = make_defragment_text(ctx)

    for p, t, is_last in chunks:
        _state(defrag)['last'] = is_last
        defrag(Text(path=tmp_path / p.name, text=t, line_number=0))

    assert (tmp_path / p.name).read_text() == expected