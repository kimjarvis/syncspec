from typing import List, Tuple, Any, Dict
import networkx as nx

from src.syncspec.text import Text
from src.syncspec.file import File
from src.syncspec.syncspec_text_context import SyncspecTextContext
from src.syncspec.syncspec_list_context import SyncspecListContext
from src.syncspec.syncspec_text import make_syncspec_text


def make_syncspec_list(context: SyncspecListContext):
    text_context = SyncspecTextContext(
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
        graph=nx.DiGraph(),
        monad=context.monad,
        import_path=context.import_path
    )

    def syncspec_list(texts: List[Text]) -> Tuple[List[File], nx.DiGraph, dict]:
        files: List[File] = []
        for text in texts:
            syncspec_text = make_syncspec_text(text_context)
            file_obj = syncspec_text(text)
            files.append(file_obj)

        print("debug 01",files)
        return files, text_context.graph, text_context.monad

    return syncspec_list