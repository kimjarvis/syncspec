from typing import List, Callable
from pathlib import Path
from src.syncspec.syncspec_context import SyncspecContext
from src.syncspec.syncspec_string_context import SyncspecStringContext
from src.syncspec.text import Text
from src.syncspec.file import File
from src.syncspec.syncspec_string import make_syncspec_string
import networkx as nx

def make_syncspec(context: SyncspecContext) -> Callable[[List[Text]], List[File]]:
    if not context.open_delimiter or not context.close_delimiter:
        raise ValueError("Delimiters cannot be empty.")
    if Path(context.log_file).exists():
        raise ValueError(f"log_file {context.log_file} already exists.")
    if Path(context.graph_file).exists():
        raise ValueError(f"graph_file {context.graph_file} already exists.")
    if not Path(context.import_path).is_dir():
        raise ValueError(f"import_path {context.import_path} is not a valid directory.")

    string_context = SyncspecStringContext(
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
        log="",
        G=nx.DiGraph(),
        monad={},
        import_path=context.import_path
    )

    def syncspec(text_list: List[Text]) -> List[File]:
        files = []
        for item in text_list:
            syncspec_string = make_syncspec_string(string_context)
            files.append(syncspec_string(item))
        return files

    return syncspec