import logging
import networkx as nx
from pathlib import Path
from typing import Optional, Dict, Tuple

from src.syncspec.text import Text
from src.syncspec.file import File
from src.syncspec.syncspec_list_context import SyncspecListContext
from src.syncspec.syncspec_list import make_syncspec_list


def syncspec(
        path: str,
        output: Optional[str] = None,
        open_delimiter: str = "{{",
        close_delimiter: str = "}}",
        import_path: Optional[str] = None,
        keyvalue: Optional[Dict[str, str]] = {},
        log_file: Optional[str] = "syncspec.log",
) -> Tuple[nx.DiGraph, dict]:
    # Validate delimiters
    if not open_delimiter or not close_delimiter:
        raise ValueError("Delimiters cannot be empty.")
    if open_delimiter == close_delimiter:
        raise ValueError("Delimiters must be distinct.")
    if open_delimiter in close_delimiter or close_delimiter in open_delimiter:
        raise ValueError("Delimiters cannot overlap structurally.")
    if '\n' in open_delimiter or '\n' in close_delimiter:
        raise ValueError("Delimiters cannot contain newlines.")

    # Validate paths
    path_obj = Path(path)
    if not path_obj.is_dir():
        raise ValueError(f"Path '{path}' must be an existing directory.")

    output_obj = Path(output) if output else path_obj
    output_obj.mkdir(parents=True, exist_ok=True)

    import_path_obj = Path(import_path) if import_path else path_obj
    if not import_path_obj.is_dir():
        raise ValueError(f"Import path '{import_path}' must be an existing directory.")

    log_file_obj = Path(log_file)
    if log_file_obj.suffix != '.log':
        raise ValueError("Log file suffix must be .log")
    if not log_file_obj.parent.exists():
        raise ValueError("Log file parent directory must exist.")

    # Setup logging
    logging.basicConfig(
        filename=str(log_file_obj),
        format="%(levelname)s - %(message)s",
        level=logging.WARNING
    )

    # Construct Context
    context = SyncspecListContext(
        open_delimiter=open_delimiter,
        close_delimiter=close_delimiter,
        monad=keyvalue,
        import_path=str(import_path_obj)
    )

    # Traverse and collect Text objects
    text_objects = []
    for md_file in path_obj.rglob('*.md'):
        content = md_file.read_text(encoding='utf-8')
        rel_name = str(md_file.relative_to(path_obj))
        text_objects.append(Text(text=content, name=rel_name))

    # Process
    syncspec_list = make_syncspec_list(context)
    files, graph, meta = syncspec_list(text_objects)

    # Write Output Files
    for file_obj in files:
        out_path = output_obj / file_obj.name
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(file_obj.text, encoding='utf-8')

    return graph, meta