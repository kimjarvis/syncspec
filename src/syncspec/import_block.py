import os
from pathlib import Path
from typing import Union, Tuple, Dict, Any

from src.syncspec.node import Node
from src.syncspec.error import Error
from src.syncspec.string import String
from src.syncspec.block import Block
from src.syncspec.import_block_context import ImportBlockContext


def make_import_block(context: ImportBlockContext):
    def import_block(block: Block) -> Union[Tuple[String, Node], Block, Error]:
        if "import" not in block.directive:
            return block

        path = block.directive["import"]
        if not isinstance(path, str):
            return Error("Import path must be a string", block.name, block.line_number)

        if os.path.isabs(path):
            return Error("Absolute file paths are not allowed", block.name, block.line_number)

        import_dir = Path(context.import_path).resolve()

        # Build the path relative to import directory (do NOT resolve symlinks yet)
        try:
            import_path = import_dir / path
            # Normalize without following symlinks
            normalized_path = Path(os.path.normpath(import_path))
        except Exception as e:
            return Error(f"Failed to resolve path: {e}", block.name, block.line_number)

        # Check that the import path itself (not resolved target) is within import directory
        try:
            normalized_path.relative_to(import_dir)
        except ValueError:
            return Error(f"File path escapes import directory: {path}", block.name, block.line_number)

        # Now resolve symlinks for existence and file checks
        try:
            resolved_path = import_path.resolve(strict=True)
        except FileNotFoundError:
            return Error(f"File does not exist: {path}", block.name, block.line_number)
        except Exception as e:
            return Error(f"Failed to resolve path: {e}", block.name, block.line_number)

        # Check that resolved symlink target is also within import directory
        try:
            resolved_path.relative_to(import_dir)
        except ValueError:
            return Error(f"Symlink target escapes import directory: {path}", block.name, block.line_number)

        if not resolved_path.is_file():
            return Error(f"Not a text file: {path}", block.name, block.line_number)
        if not os.access(resolved_path, os.R_OK):
            return Error(f"File is not readable: {path}", block.name, block.line_number)

        try:
            with open(resolved_path, "r", encoding="utf-8") as f:
                v = f.read()
        except UnicodeDecodeError:
            return Error(f"File is not valid UTF-8 text: {path}", block.name, block.line_number)
        except Exception as e:
            return Error(f"Failed to read file: {e}", block.name, block.line_number)

        lines = v.splitlines(keepends=True)

        # Apply head first, then tail (per specification)
        if "head" in block.directive:
            h = block.directive["head"]
            if not isinstance(h, int) or h < 0:
                return Error(f"Invalid head value: {h}", block.name, block.line_number)
            if h > len(lines):
                return Error(f"Cannot remove {h} lines from {len(lines)} line(s)", block.name, block.line_number)
            lines = lines[h:]

        if "tail" in block.directive:
            t = block.directive["tail"]
            if not isinstance(t, int) or t < 0:
                return Error(f"Invalid tail value: {t}", block.name, block.line_number)
            if t > len(lines):
                return Error(f"Cannot remove {t} lines from {len(lines)} line(s)", block.name, block.line_number)
            lines = lines[:-t] if t > 0 else lines

        v = "".join(lines)

        s_text = (
                context.open_delimiter +
                block.prefix +
                context.close_delimiter +
                v +
                context.open_delimiter +
                block.suffix +
                context.close_delimiter
        )
        string_obj = String(text=s_text, line_number=block.line_number, name=block.name)
        node_obj = Node(
            directive_type="import",
            key=path,
            line_number=block.line_number,
            name=block.name
        )

        return (string_obj, node_obj)

    return import_block