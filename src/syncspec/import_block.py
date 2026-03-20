import logging
from pathlib import Path
from typing import Union, Tuple, Dict, Any

from src.syncspec.node import Node
from src.syncspec.utilities import format_error
from src.syncspec.string import String
from src.syncspec.block import Block
from src.syncspec.import_block_context import ImportBlockContext


def make_import_block(context: ImportBlockContext):
    def import_block(block: Block) -> Union[Tuple[String, Node, Node], Block, String]:
        if "import" not in block.directive:
            return block

        import_path = block.directive["import"]
        log_err = lambda msg: _log_and_return_error(msg, block, context)

        # Path Validation
        try:
            root = Path(context.import_path).resolve()
            target = (root / import_path).resolve()

            if not str(target).startswith(str(root) + '/') and str(target) != str(root):
                return log_err("Path traversal detected")
            if not target.exists():
                return log_err("File does not exist")
            if not target.is_file():
                return log_err("Not a file")
            if target.is_symlink():
                link_target = target.resolve()
                if not str(link_target).startswith(str(root) + '/') and str(link_target) != str(root):
                    return log_err("Symlink target outside allowed directory")

            # Read and Decode
            try:
                v = target.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                return log_err("File is not valid UTF-8 text")
            except PermissionError:
                return log_err("File is not readable")
        except Exception as e:
            return log_err(f"Validation failed: {str(e)}")

        # Head/Tail Validation
        head = block.directive.get("head", 1)
        tail = block.directive.get("tail", 1)

        if not isinstance(head, int) or isinstance(head, bool) or head < 0:
            return log_err("Invalid head value")
        if not isinstance(tail, int) or isinstance(tail, bool) or tail < 0:
            return log_err("Invalid tail value")

        u_lines = block.text.splitlines(keepends=True)
        total_lines = len(u_lines)

        if head + tail > total_lines:
            return log_err("Head and tail overlap")

        top = "".join(u_lines[:head])
        bottom = "".join(u_lines[-tail:] if tail > 0 else [])

        # Construct Result String
        eol_char = "" if block.directive.get("eol") is False else "\n"
        s_text = (
                context.open_delimiter +
                block.prefix +
                context.close_delimiter +
                top +
                v +
                eol_char +
                bottom +
                context.open_delimiter +
                block.suffix +
                context.close_delimiter
        )
        res_string = String(text=s_text, line_number=block.line_number, name=block.name)

        # Construct Nodes
        n_export = Node(directive_type="export", key=import_path, line_number=0, name=import_path)
        n_import = Node(directive_type="import", key=import_path, line_number=block.line_number, name=block.name)

        return (res_string, n_export, n_import)

    return import_block


def _log_and_return_error(message: str, block: Block, context: ImportBlockContext) -> String:
    logging.error(format_error(message, block.name, block.line_number))
    text = (
            context.open_delimiter +
            block.prefix +
            context.close_delimiter +
            block.text +
            context.open_delimiter +
            block.suffix +
            context.close_delimiter
    )
    return String(text=text, line_number=block.line_number, name=block.name)