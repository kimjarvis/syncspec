from dataclasses import dataclass
from typing import Any, Dict

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


def make_syncspec_string(context: SyncspecStringContext):
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
    ibc = IncludeBlockContext(
        state=context.monad,
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
    )
    csc = CombineStringsContext(
        text="",
    )
    cec = CombineErrorsContext(
        text=context.log,
    )
    cnc = CombineNodesContext(
        G=context.G,
    )

    validate_text = make_validate_text(vtc)
    fragment_text = make_fragment_text(ftc)
    create_blocks = make_create_blocks(cbc)
    source_block = make_source_block(sbc)
    include_block = make_include_block(ibc)
    combine_strings = make_combine_strings(csc)
    combine_errors = make_combine_errors(cec)
    combine_nodes = make_combine_nodes(cnc)

    rules = build_rules(
        [validate_text, fragment_text, create_blocks, source_block, include_block, combine_strings, combine_errors,
         combine_nodes])

    def syncspec_string(text: Text) -> File:
        print(text)
        facts = [text]
        production(facts, rules)
        print(csc)
        return File(text=csc.text, name=text.name)

    # Expose internal contexts for diagnostics in main program
    context.cec = cec

    return syncspec_string