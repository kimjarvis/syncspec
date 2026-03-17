from dataclasses import dataclass
from typing import Any, Dict
import networkx as nx

from src.syncspec.text import Text
from src.syncspec.file import File
from src.syncspec.syncspec_text_context import SyncspecTextContext
from src.syncspec.validate_text import make_validate_text
from src.syncspec.validate_text_context import ValidateTextContext
from src.syncspec.fragment_text import make_fragment_text
from src.syncspec.fragment_text_context import FragmentTextContext
from src.syncspec.create_blocks import make_create_blocks
from src.syncspec.create_blocks_context import CreateBlocksContext
from src.syncspec.source_block import make_source_block
from src.syncspec.source_block_context import SourceBlockContext
from src.syncspec.import_block import make_import_block
from src.syncspec.import_block_context import ImportBlockContext
from src.syncspec.include_block import make_include_block
from src.syncspec.include_block_context import IncludeBlockContext
from src.syncspec.combine_strings import make_combine_strings
from src.syncspec.combine_strings_context import CombineStringsContext
from src.syncspec.combine_nodes import make_combine_nodes
from src.syncspec.combine_nodes_context import CombineNodesContext
from src.syncspec.graph_edges import make_graph_edges
from src.syncspec.graph_edges_context import GraphEdgesContext
from src.syncspec.production import build_rules, production


def make_syncspec_text(context: SyncspecTextContext):
    if not context.open_delimiter or not context.close_delimiter:
        raise ValueError("Delimiters cannot be empty")
    if not isinstance(context.graph, nx.DiGraph):
        raise ValueError("Graph must be nx.DiGraph")
    if not isinstance(context.monad, dict):
        raise ValueError("Monad must be dict")

    vtc = ValidateTextContext(
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
        line_number=1
    )
    ftc = FragmentTextContext(
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
        line_number=1
    )
    cbc = CreateBlocksContext(
        index=0,
        prefix="",
        text="",
        line_number=1,
    )
    sbc = SourceBlockContext(
        state=context.monad,
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
    )
    imbc = ImportBlockContext(
        import_path=context.import_path,
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
    )
    ibc = IncludeBlockContext(
        state=context.monad,
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
    )
    csc = CombineStringsContext(
        text="",
    )
    cnc = CombineNodesContext(
        G=context.graph,
    )
    gec = GraphEdgesContext(
        G=context.graph,
    )

    context._combine_strings_context = csc

    validate_text = make_validate_text(vtc)
    fragment_text = make_fragment_text(ftc)
    create_blocks = make_create_blocks(cbc)
    source_block = make_source_block(sbc)
    import_block = make_import_block(imbc)
    include_block = make_include_block(ibc)
    combine_strings = make_combine_strings(csc)
    combine_nodes = make_combine_nodes(cnc)
    graph_edges = make_graph_edges(gec)

    def syncspec_text(text: Text) -> File:
        facts = [text]
        rules = build_rules(
            [validate_text, fragment_text, create_blocks, source_block, import_block, include_block, combine_strings,
             combine_nodes, graph_edges])
        production(facts, rules)
        return File(text=csc.text, name=text.name)

    return syncspec_text