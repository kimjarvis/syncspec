from typing import List
import networkx as nx
from src.syncspec.syncspec_context import SyncspecContext
from src.syncspec.syncspec_string_context import SyncspecStringContext
from src.syncspec.syncspec_string import make_syncspec_string
from src.syncspec.text import Text
from src.syncspec.file import File


def make_syncspec(context: SyncspecContext):
    string_context = SyncspecStringContext(
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
        log="",
        G=nx.DiGraph(),
        monad={},
        import_path=context.import_path
    )
    syncspec_string = make_syncspec_string(string_context)

    def syncspec(texts: List[Text]) -> List[File]:
        return [syncspec_string(t) for t in texts]

    return syncspec