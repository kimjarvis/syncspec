import os
import networkx as nx

from src.syncspec.text import Text
from src.syncspec.file import File
from src.syncspec.syncspec_string_context import SyncspecStringContext
from src.syncspec.combine_errors import make_combine_errors
from src.syncspec.combine_errors_context import CombineErrorsContext
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
from src.syncspec.validate_text import make_validate_text
from src.syncspec.validate_text_context import ValidateTextContext
from src.syncspec.import_block import make_import_block
from src.syncspec.import_block_context import ImportBlockContext


def make_syncspec_string(context: SyncspecStringContext):
    # Validate context
    if not context.open_delimiter or not context.close_delimiter:
        raise ValueError("Delimiters cannot be empty.")
    if not isinstance(context.log, str):
        raise ValueError("Log must be a string path.")
    if not isinstance(context.G, nx.DiGraph):
        raise ValueError("G must be nx.DiGraph.")
    if not isinstance(context.monad, dict):
        raise ValueError("Monads must be dict.")
    if not os.path.isdir(context.import_path):
        raise ValueError("Import path must exist.")

    # Initialize contexts
    vtc = ValidateTextContext(context.open_delimiter, context.close_delimiter, 1)
    ftc = FragmentTextContext(context.open_delimiter, context.close_delimiter, 1)
    cbc = CreateBlocksContext(0, "", "", 1)
    sbc = SourceBlockContext(context.monad, context.open_delimiter, context.close_delimiter)
    imbc = ImportBlockContext(context.import_path, context.open_delimiter, context.close_delimiter)
    ibc = IncludeBlockContext(context.monad, context.open_delimiter, context.close_delimiter)
    csc = CombineStringsContext("")
    cec = CombineErrorsContext(context.log)
    cnc = CombineNodesContext(context.G)

    # Expose stateful context for diagnostics
    context.csc = csc

    # Initialize functions
    validate_text = make_validate_text(vtc)
    fragment_text = make_fragment_text(ftc)
    create_blocks = make_create_blocks(cbc)
    source_block = make_source_block(sbc)
    import_block = make_import_block(imbc)
    include_block = make_include_block(ibc)
    combine_strings = make_combine_strings(csc)
    combine_errors = make_combine_errors(cec)
    combine_nodes = make_combine_nodes(cnc)

    rules = build_rules([
        validate_text, fragment_text, create_blocks, source_block,
        import_block, include_block, combine_strings, combine_errors,
        combine_nodes
    ])

    def syncspec_string(text: Text) -> File:
        facts = [text]
        production(facts, rules)
        return File(text=csc.text, name=text.name)

    return syncspec_string