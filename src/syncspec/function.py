import logging
from pathlib import Path
from typing import Tuple, Dict, List

import networkx as nx

from src.syncspec.text import Text
from src.syncspec.file import File
from src.syncspec.syncspec_list_context import SyncspecListContext
from src.syncspec.syncspec_list import make_syncspec_list


def syncspec(
    path: str,
    output: str,
    open_delimiter: str,
    close_delimiter: str,
    import_path: str,
    keyvalue: dict,
    log_file: str
) -> Tuple[nx.DiGraph, dict]:

    # Validate Directories
    for p, name in [(path, "path"), (output, "output"), (import_path, "import_path")]:
        if not Path(p).exists() or not Path(p).is_dir():
            raise ValueError(f"{name} must be an existing directory")

    # Validate Log File
    log_path = Path(log_file)
    if log_path.suffix != ".log":
        raise ValueError("log_file must have .log suffix")
    if not log_path.parent.exists():
        raise ValueError("log_file parent directory must exist")

    # Validate Delimiters
    for d, name in [(open_delimiter, "open_delimiter"), (close_delimiter, "close_delimiter")]:
        if not d:
            raise ValueError(f"{name} cannot be empty")
        if "\n" in d:
            raise ValueError(f"{name} cannot contain newlines")

    if open_delimiter == close_delimiter:
        raise ValueError("Delimiters must be distinct")
    if open_delimiter in close_delimiter or close_delimiter in open_delimiter:
        raise ValueError("Delimiters cannot overlap structurally")

    # Validate Keyvalue
    if not all(isinstance(k, str) for k in keyvalue.keys()):
        raise ValueError("keyvalue keys must be strings")

    # Setup Logging
    logging.basicConfig(
        filename=log_file,
        level=logging.WARNING,
        format="%(levelname)s - %(message)s"
    )

    # Construct Context
    context = SyncspecListContext(
        open_delimiter=open_delimiter,
        close_delimiter=close_delimiter,
        monad=keyvalue,
        import_path=import_path
    )

    # Get Processor
    syncspec_list = make_syncspec_list(context)

    # Traverse Input
    texts: List[Text] = []
    root = Path(path)
    for md_file in root.rglob("*.md"):
        relative_name = str(md_file.relative_to(root))
        content = md_file.read_text(encoding="utf-8")
        texts.append(Text(text=content, name=relative_name))

    # Process
    files, graph, meta = syncspec_list(texts)

    # Write Output
    out_root = Path(output)
    for file_obj in files:
        out_path = out_root / file_obj.name
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(file_obj.text, encoding="utf-8")

    return graph, meta