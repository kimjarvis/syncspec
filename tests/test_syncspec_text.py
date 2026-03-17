import pytest
import networkx as nx

from src.syncspec.text import Text
from src.syncspec.file import File
from src.syncspec.syncspec_text_context import SyncspecTextContext
from src.syncspec.combine_strings_context import CombineStringsContext
from src.syncspec.syncspec_text import make_syncspec_text


@pytest.mark.parametrize("name, input_text, expected_text", [
    ("freddy", """line 1
    {{"source": "a"}}A{{}}
    {{"source": "b"}}B{{}}
    line 2
    {{"include": "a"}}{{}} 
    {{"include": "b"}}{{}}
    line 3""", """line 1
    {{"source": "a"}}A{{}}
    {{"source": "b"}}B{{}}
    line 2
    {{"include": "a"}}A{{}} 
    {{"include": "b"}}B{{}}
    line 3"""),
])
def test_syncspec_text(name, input_text, expected_text):
    context = SyncspecTextContext(
        open_delimiter="{{",
        close_delimiter="}}",
        graph=nx.DiGraph(),
        monad={},
        import_path="."
    )

    syncspec_text = make_syncspec_text(context)
    result = syncspec_text(Text(name=name, text=input_text))

    assert isinstance(result, File)
    assert result.name == name
    assert result.text == expected_text
    assert context.csc.text == expected_text