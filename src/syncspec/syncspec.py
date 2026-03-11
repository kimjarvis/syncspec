from typing import List
import networkx as nx
from src.syncspec.syncspec_context import SyncspecContext
from src.syncspec.syncspec_string_context import SyncspecStringContext
from src.syncspec.text import Text
from src.syncspec.file import File
from src.syncspec.syncspec_string import make_syncspec_string


def make_syncspec(context: SyncspecContext):
    string_context = SyncspecStringContext(
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
        log="",
        G=nx.DiGraph(),
        monad={}
    )

    def syncspec(texts: List[Text]) -> List[File]:
        return [make_syncspec_string(string_context)(text) for text in texts]

    return syncspec