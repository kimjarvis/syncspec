import os
from pathlib import Path
from typing import Union, Tuple, Any

from src.syncspec.node import Node
from src.syncspec.error import Error
from src.syncspec.string import String
from src.syncspec.block import Block
from src.syncspec.import_block_context import ImportBlockContext


def make_import_block(context: ImportBlockContext):
    def import_block(block: Block) -> Union[Tuple[String, Node, Node], Block, Error]:
        # Check for import directive
        if "import" not in block.directive:
            return block

        import_path_val = block.directive["import"]
        if not isinstance(import_path_val, str):
            return Error(message="Import path must be a string", name=block.name, line_number=block.line_number)

        # Resolve paths securely
        try:
            base_path = Path(context.import_path).resolve()
            target_path = (base_path / import_path_val).resolve()
            # Ensure target is within base_path
            target_path.relative_to(base_path)
        except (ValueError, OSError):
            return Error(message="Invalid import path or traversal detected", name=block.name,
                         line_number=block.line_number)

        # Verify file existence and readability
        if not target_path.exists() or not target_path.is_file():
            return Error(message="Import file does not exist", name=block.name, line_number=block.line_number)

        try:
            v = target_path.read_text(encoding='utf-8')
        except (PermissionError, UnicodeDecodeError):
            return Error(message="File not readable or not valid UTF-8 text", name=block.name,
                         line_number=block.line_number)

        # Process head/tail directives
        head = block.directive.get("head", 0)
        tail = block.directive.get("tail", 0)

        if not isinstance(head, int) or not isinstance(tail, int):
            return Error(message="Head and tail must be integers", name=block.name, line_number=block.line_number)

        if head < 0 or tail < 0:
            return Error(message="Head and tail cannot be negative", name=block.name, line_number=block.line_number)

        u = block.text
        lines = u.splitlines(keepends=True)
        total_lines = len(lines)

        if head + tail > total_lines:
            return Error(message="Head and tail overlap", name=block.name, line_number=block.line_number)

        top = "".join(lines[:head])
        bottom = "".join(lines[-tail:] if tail > 0 else [])

        # Construct result String
        # Note: Spec specifies open_delimiter for step 7
        text = (
                context.open_delimiter +
                block.prefix +
                context.close_delimiter +
                top +
                v +
                bottom +
                context.open_delimiter +
                block.suffix +
                context.close_delimiter
        )
        res_string = String(text=text, line_number=block.line_number, name=block.name)

        # Construct Nodes
        node_export = Node(directive_type="export", key=import_path_val, line_number=0, name=import_path_val)
        node_import = Node(directive_type="import", key=import_path_val, line_number=block.line_number, name=block.name)

        return (res_string, node_export, node_import)

    return import_block