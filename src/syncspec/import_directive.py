import logging
from pathlib import Path
from typing import Union

from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.stop import Stop
from syncspec.utilities import format_log_message

def make_import_directive(context: Context):
    def import_directive(directive: Directive) -> Union[Directive, Stop]:
        if "import" not in directive.parameters:
            return directive

        try:
            base_dir = directive.path.parent
            rel_path = Path(directive.parameters["import"])
            target_path = (base_dir / rel_path).resolve()
            input_root = context.input_path.resolve()

            if not target_path.is_relative_to(input_root):
                raise ValueError(f"Import path escapes input directory: {target_path}")
            if not target_path.exists():
                raise FileNotFoundError(f"Import file not found: {target_path}")
            if not target_path.is_file():
                raise ValueError(f"Import path is not a file: {target_path}")

            if target_path.is_symlink() and not target_path.resolve().is_relative_to(input_root):
                raise ValueError(f"Symlink target escapes input directory: {target_path.resolve()}")

            try:
                imported_text = target_path.read_text(encoding='utf-8')
            except UnicodeDecodeError as e:
                raise ValueError(f"Not a valid UTF-8 text file: {e}")
            except PermissionError as e:
                raise PermissionError(f"File not readable: {e}")

            if not imported_text.endswith('\n'):
                imported_text += '\n'

            head_val = directive.parameters.get("head", 1)
            if not isinstance(head_val, int) or isinstance(head_val, bool):
                raise TypeError("Parameter 'head' must be an integer")

            tail_val = directive.parameters.get("tail", 1)
            if not isinstance(tail_val, int) or isinstance(tail_val, bool):
                raise TypeError("Parameter 'tail' must be an integer")

            lines = directive.text.splitlines(keepends=True)
            if head_val + tail_val > len(lines):
                raise ValueError(f"head ({head_val}) + tail ({tail_val}) exceeds directive text lines ({len(lines)})")

            top = lines[:head_val]
            bottom = lines[-tail_val:] if tail_val > 0 else []
            new_text = ''.join(top) + imported_text + ''.join(bottom)

            return Directive(
                parameters=directive.parameters,
                prefix=directive.prefix,
                text=new_text,
                suffix=directive.suffix,
                path=directive.path,
                prefix_line_number=directive.prefix_line_number,
                text_line_number=directive.text_line_number,
                suffix_line_number=directive.suffix_line_number
            )

        except Exception as e:
            logging.error(format_log_message(str(e), directive.path, directive.prefix_line_number))
            return Stop()

    return import_directive