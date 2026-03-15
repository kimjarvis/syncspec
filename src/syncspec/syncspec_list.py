from typing import List, Tuple, Dict, Any
import networkx as nx
from src.syncspec.text import Text
from src.syncspec.file import File
from src.syncspec.syncspec_text_context import SyncspecTextContext
from src.syncspec.syncspec_text import make_syncspec_text
from src.syncspec.syncspec_list_context import SyncspecListContext


def make_syncspec_list(context: SyncspecListContext):
    text_context = SyncspecTextContext(
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
        log="",
        G=nx.DiGraph(),
        monad={},
        import_path=context.import_path
    )

    def syncspec_list(text_list: List[Text]) -> Tuple[List[File], str, nx.DiGraph, Dict]:
        files = []
        for item in text_list:
            syncspec_text = make_syncspec_text(text_context)
            files.append(syncspec_text(item))

        return files, text_context.log, text_context.G, text_context.monad

    return syncspec_list