from typing import List, Any
import networkx as nx

from src.syncspec.syncspec_text_context import SyncspecTextContext
from src.syncspec.text import Text
from src.syncspec.file import File
from src.syncspec.production import build_rules, production

from src.syncspec.validate_text import make_validate_text
from src.syncspec.validate_text_context import ValidateTextContext
from src.syncspec.fragment_text import make_fragment_text
from src.syncspec.fragment_text_context import FragmentTextContext
from src.syncspec.create_blocks import make_create_blocks
from src.syncspec.create_blocks_context import CreateBlocksContext
from src.syncspec.source_block import make_source_block
from src.syncspec.source_block_context import SourceBlockContext
from src.syncspec.include_block import make_include_block
from src.syncspec.include_block_context import IncludeBlockContext
from src.syncspec.import_block import make_import_block
from src.syncspec.import_block_context import ImportBlockContext
from src.syncspec.combine_strings import make_combine_strings
from src.syncspec.combine_strings_context import CombineStringsContext
from src.syncspec.add_graph_nodes import make_add_graph_nodes
from src.syncspec.add_graph_nodes_context import AddGraphNodesContext
from src.syncspec.add_graph_edges import make_add_graph_edges
from src.syncspec.add_graph_edges_context import AddGraphEdgesContext


def make_syncspec_text(context: SyncspecTextContext):
    assert context.open_delimiter and context.close_delimiter
    assert isinstance(context.graph, nx.DiGraph)
    assert isinstance(context.monad, dict)

    validate_text = make_validate_text(ValidateTextContext(
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
        line_number=1
    ))
    fragment_text = make_fragment_text(FragmentTextContext(
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
        line_number=1
    ))
    create_blocks = make_create_blocks(CreateBlocksContext(
        index=0,
        prefix="",
        prefix_line_number=1,
        prefix_valid=False,
        directive={},
        text="",
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
    ))
    source_block = make_source_block(SourceBlockContext(
        state=context.monad,
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
    ))
    include_block = make_include_block(IncludeBlockContext(
        state=context.monad,
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
    ))
    import_block = make_import_block(ImportBlockContext(
        import_path=context.import_path,
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
    ))
    combine_strings_context = CombineStringsContext(text="")
    combine_strings = make_combine_strings(combine_strings_context)
    add_graph_nodes = make_add_graph_nodes(AddGraphNodesContext(G=context.graph))
    add_graph_edges = make_add_graph_edges(AddGraphEdgesContext(G=context.graph))

    context.combine_strings_context = combine_strings_context

    def syncspec_text(text: Text) -> File:
        facts = [text]
        rules = build_rules([
            validate_text,
            fragment_text,
            create_blocks,
            source_block,
            import_block,
            include_block,
            combine_strings,
            add_graph_nodes,
            # add_graph_edges
        ])
        production(facts, rules)
        return File(text=context.combine_strings_context.text, name=text.name)

    return syncspec_text