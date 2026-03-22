from typing import Any, Dict, List
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


def make_syncspec_text(context: SyncspecTextContext):
    if not context.open_delimiter or not context.close_delimiter:
        raise ValueError("Delimiters cannot be empty strings.")
    if not isinstance(context.graph, nx.DiGraph):
        raise TypeError("graph must be a nx.DiGraph object.")
    if not isinstance(context.monad, dict):
        raise TypeError("monad must be a dictionary.")

    validate_text_context = ValidateTextContext(
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
        line_number=1
    )
    validate_text = make_validate_text(validate_text_context)

    fragment_text_context = FragmentTextContext(
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
        line_number=1
    )
    fragment_text = make_fragment_text(fragment_text_context)

    create_blocks_context = CreateBlocksContext(
        index=0,
        prefix="",
        prefix_line_number=1,
        prefix_valid=False,
        directive={},
        text="",
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
    )
    create_blocks = make_create_blocks(create_blocks_context)

    source_block_context = SourceBlockContext(
        state=context.monad,
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
    )
    source_block = make_source_block(source_block_context)

    include_block_context = IncludeBlockContext(
        state=context.monad,
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
    )
    include_block = make_include_block(include_block_context)

    import_block_context = ImportBlockContext(
        import_path=context.import_path,
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
    )
    import_block = make_import_block(import_block_context)

    combine_strings_context = CombineStringsContext(text="")
    combine_strings = make_combine_strings(combine_strings_context)

    add_graph_nodes_context = AddGraphNodesContext(G=context.graph)
    add_graph_nodes = make_add_graph_nodes(add_graph_nodes_context)

    context.combine_strings_context = combine_strings_context

    rules = build_rules([
        validate_text,
        fragment_text,
        create_blocks,
        source_block,
        import_block,
        include_block,
        combine_strings,
        add_graph_nodes,
    ])

    def syncspec_text(text: Text) -> File:
        facts = [text]
        production(facts, rules)
        return File(text=combine_strings_context.text, name=text.name)

    return syncspec_text