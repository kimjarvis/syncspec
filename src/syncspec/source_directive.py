import logging
from typing import Union
from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.stop import Stop
from syncspec.utilities import format_log_message

def make_source_directive(context: Context):
    def source_directive(directive: Directive) -> Union[Directive, Stop]:
        if "source" not in directive.parameters:
            return directive

        key = directive.parameters["source"]
        head = directive.parameters.get("head", 1)
        tail = directive.parameters.get("tail", 1)

        if not isinstance(head, int) or not isinstance(tail, int):
            logging.error(format_log_message("'head' and 'tail' must be integers", directive.path, directive.prefix_line_number))
            return Stop()

        lines = directive.text.splitlines(keepends=True)
        if head + tail > len(lines):
            logging.error(format_log_message(f"Cannot remove {head} head and {tail} tail lines from {len(lines)} line(s)", directive.path, directive.prefix_line_number))
            return Stop()

        output = "".join(lines[head : len(lines) - tail])

        if output.startswith("\n"):
            output = output[1:]
        if not output.endswith("\n"):
            output += "\n"

        if key in context.keyvalue:
            logging.error(format_log_message(f"Key '{key}' already exists in context", directive.path, directive.prefix_line_number))
            return Stop()

        context.keyvalue[key] = output
        return directive
    return source_directive