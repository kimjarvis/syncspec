import pprint
import networkx as nx

from src.syncspec.syncspec_string import make_syncspec_string
from src.syncspec.syncspec_string_context import SyncspecStringContext
from src.syncspec.text import Text

if __name__ == "__main__":
    # Initialise the context
    context = SyncspecStringContext(
        open_delimiter="{{",
        close_delimiter="}}",
        log="",
        G=nx.DiGraph(),
        monad={}
    )

    # Create the syncspec_string function
    syncspec_string = make_syncspec_string(context)

    # Call the function with the Text object
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

    # Map internal contexts to variables for diagnostic output
    monad = context.monad
    csc = syncspec_string._csc
    cec = syncspec_string._cec
    cnc = syncspec_string._cnc

    # Produce diagnostic information
    pprint.pp(monad)
    pprint.pp(csc)
    pprint.pp(cec)
    nx.drawing.nx_pydot.write_dot(cnc.G, "graph.dot")