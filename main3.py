import pprint
import networkx as nx

from src.syncspec.syncspec_string_context import SyncspecStringContext
from src.syncspec.syncspec_string import make_syncspec_string
from src.syncspec.text import Text

def main():
    open_delimiter = "{{"
    close_delimiter = "}}"
    log = "log.txt"
    G = nx.DiGraph()
    monad = {}
    import_path = "."

    context = SyncspecStringContext(
        open_delimiter=open_delimiter,
        close_delimiter=close_delimiter,
        log=log,
        G=G,
        monad=monad,
        import_path=import_path
    )

    syncspec_string = make_syncspec_string(context)

    text_obj = Text(name="freddy", text="""line 1
    {{"source": "a"}}A{{}}
    {{"source": "b"}}B{{}}
    line 2
    {{"include": "a"}}{{}} 
    {{"include": "b"}}{{}}
    line 3""")

    result = syncspec_string(text_obj)

    pprint.pp(context.csc)

if __name__ == "__main__":
    main()