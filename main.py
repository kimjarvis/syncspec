import pprint

import networkx as nx

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
from src.syncspec.text import Text
from src.syncspec.validate_text import make_validate_text
from src.syncspec.validate_text_context import ValidateTextContext


def main():
    vtc = ValidateTextContext(
        open_delimiter="{{",
        close_delimiter="}}",
        line_number=1
    )
    ftc = FragmentTextContext(
        open_delimiter="{{",
        close_delimiter="}}",
        line_number=1
    )
    cbc = CreateBlocksContext(
        index=0,
        prefix="",
        text="",
        line_number=1,
    )
    monad = {}
    sbc = SourceBlockContext(
        state=monad,
        open_delimiter="{{",
        close_delimiter="}}",
    )
    ibc = IncludeBlockContext(
        state=monad,
        open_delimiter="{{",
        close_delimiter="}}",
    )
    csc = CombineStringsContext(
        text="",
        name="",
    )
    cec = CombineErrorsContext(
        text="",
    )
    graph = nx.DiGraph()
    cnc = CombineNodesContext(
        G=graph,
    )

    # 2. Create Unary Function bound to context
    validate_text = make_validate_text(vtc)
    fragment_text = make_fragment_text(ftc)
    create_blocks = make_create_blocks(cbc)
    source_block = make_source_block(sbc)
    include_block = make_include_block(ibc)
    combine_strings = make_combine_strings(csc)
    combine_errors = make_combine_errors(cec)
    combine_nodes = make_combine_nodes(cnc)

    facts = [Text(name="freddy", text="""line 1
    {{"source": "a"}}A{{}}
    {{"source": "b"}}B{{}}
    line 2
    {{"include": "a"}}{{}} 
    {{"include": "b"}}{{}}
    line 3"""),
    ]

    rules = build_rules(
        [validate_text, fragment_text, create_blocks, source_block, include_block, combine_strings, combine_errors,
         combine_nodes])


    # 4. Run Production (no context passed)
    result = production(facts, rules)
    pprint.pp(result)
    pprint.pp(monad)
    pprint.pp(csc)
    pprint.pp(cec)
    nx.drawing.nx_pydot.write_dot(cnc.G, "graph.dot")


if __name__ == "__main__":
    main()
