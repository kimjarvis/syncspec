import logging
from dataclasses import replace
from typing import Union

from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.stop import Stop
from syncspec.utilities import format_log_message


def make_include_directive(context: Context):
    def include_directive(directive: Directive) -> Union[Directive, Stop]:
        if "include" not in directive.parameters:
            return directive

        key = directive.parameters["include"]
        if key not in context.keyvalue:
            logging.warning(format_log_message(
                f"Key '{key}' not found in context.keyvalue",
                directive.path, directive.prefix_line_number
            ))
            return directive

        input_text = context.keyvalue[key]
        if not input_text.endswith("\n"):
            input_text += "\n"

        raw_head = directive.parameters.get("head", 1)
        if not isinstance(raw_head, int) or isinstance(raw_head, bool):
            logging.error(format_log_message(
                "Parameter 'head' must be an integer",
                directive.path, directive.prefix_line_number
            ))
            return Stop()

        raw_tail = directive.parameters.get("tail", 1)
        if not isinstance(raw_tail, int) or isinstance(raw_tail, bool):
            logging.error(format_log_message(
                "Parameter 'tail' must be an integer",
                directive.path, directive.prefix_line_number
            ))
            return Stop()

        lines = directive.text.splitlines(keepends=True)
        if raw_head + raw_tail > len(lines):
            logging.error(format_log_message(
                f"head ({raw_head}) + tail ({raw_tail}) exceeds line count ({len(lines)})",
                directive.path, directive.prefix_line_number
            ))
            return Stop()

        top = "".join(lines[:raw_head])
        bottom = "".join(lines[-raw_tail:]) if raw_tail > 0 else ""

        return replace(directive, text=top + input_text + bottom)

    return include_directive