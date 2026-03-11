from typing import List
from pathlib import Path
import networkx as nx

from src.syncspec.text import Text
from src.syncspec.syncspec_context import SyncspecContext
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


def make_syncspec(context: SyncspecContext):
    def syncspec(texts: List[Text]) -> List[Text]:
        vtc = ValidateTextContext(context.open_delimiter, context.close_delimiter, 1)
        ftc = FragmentTextContext(context.open_delimiter, context.close_delimiter, 1)
        cbc = CreateBlocksContext(0, "", "", 1)
        monad = {}
        sbc = SourceBlockContext(monad, context.open_delimiter, context.close_delimiter)
        ibc = IncludeBlockContext(monad, context.open_delimiter, context.close_delimiter)
        csc = CombineStringsContext("")
        cec = CombineErrorsContext("")
        graph = nx.DiGraph()
        cnc = CombineNodesContext(graph)

        funcs = [
            make_validate_text(vtc), make_fragment_text(ftc), make_create_blocks(cbc),
            make_source_block(sbc), make_include_block(ibc), make_combine_strings(csc),
            make_combine_errors(cec), make_combine_nodes(cnc)
        ]
        rules = build_rules(funcs)
        result = production(texts, rules)

        # Write logs and graph
        Path(context.log_file).write_text(cec.text)
        nx.drawing.nx_pydot.write_dot(graph, context.graph_file)

        # Map results back to Text
        # Assuming result is List[str] corresponding to inputs
        return [Text(name=t.name, text=str(r)) for t, r in zip(texts, result)]

    return syncspec