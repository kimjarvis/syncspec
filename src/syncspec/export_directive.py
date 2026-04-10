import logging
import os
from pathlib import Path
from typing import Union

from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.stop import Stop
from syncspec.utilities import format_log_message

logger = logging.getLogger(__name__)

def make_export_directive(context: Context):
    def export_directive(directive: Directive) -> Union[Directive, Stop]:
        if "export" not in directive.parameters:
            return directive

        try:
            base_dir = directive.path.parent
            file_path = (base_dir / str(directive.parameters["export"])).resolve()

            if not file_path.is_relative_to(context.input_path):
                raise ValueError(f"Export path '{file_path}' escapes '{context.input_path}'.")

            if file_path.exists():
                if not os.access(file_path, os.R_OK):
                    raise PermissionError(f"File '{file_path}' is not readable.")
                with open(file_path, "r", encoding="utf-8") as f:
                    f.read()

            head = directive.parameters.get("head", 1)
            tail = directive.parameters.get("tail", 1)
            if not isinstance(head, int) or not isinstance(tail, int):
                raise TypeError("'head' and 'tail' must be integers.")

            output = directive.text
            lines = output.splitlines(keepends=True)

            if head + tail > len(lines):
                raise ValueError(f"head({head}) + tail({tail}) exceeds line count({len(lines)}).")

            trimmed = lines[head:-tail] if tail > 0 else lines[head:]
            output = "".join(trimmed)

            if output and output[0] == "\n":
                output = output[1:]
            if output and output[-1] != "\n":
                output += "\n"

            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(output, encoding="utf-8")
            return directive

        except Exception as e:
            logger.error(format_log_message(str(e), directive.path, directive.prefix_line_number))
            return Stop()

    return export_directive