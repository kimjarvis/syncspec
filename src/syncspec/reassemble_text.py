from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.text import Text

def make_reassemble_text(context: Context):
    def reassemble_text(directive: Directive) -> Text:
        assembled = (
            context.open_delimiter + directive.prefix + context.close_delimiter +
            directive.text +
            context.open_delimiter + directive.suffix + context.close_delimiter
        )
        return Text(
            path=directive.path,
            text=assembled,
            line_number=directive.prefix_line_number
        )
    return reassemble_text