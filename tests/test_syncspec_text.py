import pytest
import networkx as nx
import pprint

from src.syncspec.production import build_rules, production
from src.syncspec.text import Text
from src.syncspec.file import File
from src.syncspec.syncspec_text_context import SyncspecTextContext
from src.syncspec.syncspec_text import make_syncspec_text
from src.syncspec.combine_strings_context import CombineStringsContext


@pytest.mark.parametrize("name, content, expected_text", [
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
    line 3""")
])
def test_make_syncspec_text(name, content, expected_text):
    context = SyncspecTextContext(
        open_delimiter="{{",
        close_delimiter="}}",
        graph=nx.DiGraph(),
        monad={},
        import_path="."
    )
    syncspec_text = make_syncspec_text(context)
    input_text = Text(name=name, text=content)

    result = syncspec_text(input_text)

    assert isinstance(result, File)
    assert result.name == name
    assert hasattr(context, 'combine_strings_context')
    assert isinstance(context.combine_strings_context, CombineStringsContext)
    assert context.combine_strings_context.text == expected_text