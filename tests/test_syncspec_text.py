import pytest
import pprint
import networkx as nx
from pathlib import Path
import tempfile

from src.syncspec.combine_errors import make_combine_errors
from src.syncspec.combine_errors_context import CombineErrorsContext
from src.syncspec.graph_edges import make_graph_edges
from src.syncspec.graph_edges_context import GraphEdgesContext
from src.syncspec.combine_nodes import make_combine_nodes
from src.syncspec.combine_nodes_context import CombineNodesContext
from src.syncspec.combine_strings import make_combine_strings
from src.syncspec.combine_strings_context import CombineStringsContext
from src.syncspec.create_blocks import make_create_blocks
from src.syncspec.create_blocks_context import CreateBlocksContext
from src.syncspec.fragment_text import make_fragment_text
from src.syncspec.fragment_text_context import FragmentTextContext
from src.syncspec.include_block import make_include_block
from src.syncspec.include_block_context import IncludeBlockContext
from src.syncspec.production import build_rules, production
from src.syncspec.source_block import make_source_block
from src.syncspec.source_block_context import SourceBlockContext
from src.syncspec.text import Text
from src.syncspec.validate_text import make_validate_text
from src.syncspec.validate_text_context import ValidateTextContext
from src.syncspec.import_block import make_import_block
from src.syncspec.import_block_context import ImportBlockContext
from src.syncspec.file import File
from src.syncspec.syncspec_text_context import SyncspecTextContext
from src.syncspec.syncspec_text import make_syncspec_text


@pytest.mark.parametrize("name", ["freddy"])
def test_syncspec_text_functionality(name):
    with tempfile.TemporaryDirectory() as tmpdir:
        open_delimiter = "{{"
        close_delimiter = "}}"
        log = "log.txt"
        G = nx.DiGraph()
        monad = {}
        import_path = tmpdir

        context = SyncspecTextContext(
            open_delimiter=open_delimiter,
            close_delimiter=close_delimiter,
            log=log,
            G=G,
            monad=monad,
            import_path=import_path
        )

        syncspec_text = make_syncspec_text(context)

        input_text = Text(name=name, text="""line 1
    {{"source": "a"}}A{{}}
    {{"source": "b"}}B{{}}
    line 2
    {{"include": "a"}}{{}} 
    {{"include": "b"}}{{}}
    line 3""")

        result = syncspec_text(input_text)

        assert isinstance(result, File)
        assert result.name == name

        expected_text = """line 1
    {{"source": "a"}}A{{}}
    {{"source": "b"}}B
{{}}
    line 2
    {{"include": "a"}}A{{}} 
    {{"include": "b"}}B
{{}}
    line 3"""

        assert context._csc.text == expected_text