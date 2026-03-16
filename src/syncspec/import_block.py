import logging
from pathlib import Path
from typing import Union, Tuple, Dict, Any

from src.syncspec.node import Node
from src.syncspec.string import String
from src.syncspec.block import Block
from src.syncspec.import_block_context import ImportBlockContext
from src.syncspec.utilities import format_error


def make_import_block(context: ImportBlockContext):
    base_path = Path(context.import_path).resolve()

    def import_block(block: Block) -> Union[Tuple[String, Node, Node], Block, None]:
        directive = block.directive
        if "import" not in directive:
            return block

        import_path = directive["import"]
        if not isinstance(import_path, str):
            logging.error(format_error("'import' must be a string", block.name, block.line_number))
            return None

        # Resolve and validate path
        try:
            target_path = (base_path / import_path).resolve()
            target_path.relative_to(base_path)
        except (ValueError, RuntimeError):
            logging.error(format_error("Invalid import path (escape attempt)", block.name, block.line_number))
            return None

        if not target_path.exists() or not target_path.is_file():
            logging.error(format_error("Import file does not exist", block.name, block.line_number))
            return None

        # Validate text/utf-8
        try:
            v = target_path.read_text(encoding='utf-8')
        except (UnicodeDecodeError, PermissionError):
            logging.error(format_error("Import file is not readable text", block.name, block.line_number))
            return None

        # Validate head/tail
        head = directive.get("head", 0)
        tail = directive.get("tail", 0)

        if not isinstance(head, int) or isinstance(head, bool) or head < 0:
            logging.error(format_error("Invalid 'head' value", block.name, block.line_number))
            return None
        if not isinstance(tail, int) or isinstance(tail, bool) or tail < 0:
            logging.error(format_error("Invalid 'tail' value", block.name, block.line_number))
            return None

        lines = block.text.splitlines(keepends=True)
        total_lines = len(lines)

        if head + tail > total_lines:
            logging.error(format_error("Head and tail overlap", block.name, block.line_number))
            return None

        top = "".join(lines[:head])
        bottom = "".join(lines[total_lines - tail:]) if tail > 0 else ""

        # Construct String
        s_text = (
            context.open_delimiter +
            block.prefix +
            context.close_delimiter +
            top +
            v +
            "\n" +
            bottom +
            context.open_delimiter +
            block.suffix +
            context.close_delimiter
        )
        res_string = String(text=s_text, line_number=block.line_number, name=block.name)

        # Construct Nodes
        export_node = Node(
            directive_type="export",
            key=import_path,
            line_number=0,
            name=import_path
        )
        import_node = Node(
            directive_type="import",
            key=import_path,
            line_number=block.line_number,
            name=block.name
        )

        return (res_string, export_node, import_node)

    return import_block