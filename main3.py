import pprint
import networkx as nx

from src.syncspec.text import Text
from src.syncspec.syncspec_string_context import SyncspecStringContext
from src.syncspec.syncspec_string import make_syncspec_string

if __name__ == "__main__":
    context = SyncspecStringContext(
        open_delimiter="{{",
        close_delimiter="}}",
        log="",
        G=nx.DiGraph(),
        monad={}
    )

    syncspec_string = make_syncspec_string(context)

    input_text = Text(
        name="freddy",
        text="""line 1
    {{"source": "a"}}A{{}}
    {{"source": "b"}}B{{}}
    line 2
    {{"include": "a"}}{{}} 
    {{"include": "b"}}{{}}
    line 3"""
    )

    result = syncspec_string(input_text)

    # Diagnostic information
    monad = context.monad
    cec = context.cec
    cnc = type('obj', (object,), {'G': context.G})()  # Wrapper to match diagnostic var name

    pprint.pp(result)
    pprint.pp(monad)
    pprint.pp(cec)
    nx.drawing.nx_pydot.write_dot(cnc.G, "graph.dot")