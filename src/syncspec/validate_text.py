# src/syncspec/validate_text.py
from typing import Union
import logging
from src.syncspec.text import Text
from src.syncspec.validated_text import ValidatedText
from src.syncspec.utilities import format_error
from src.syncspec.validate_text_context import ValidateTextContext


def make_validate_text(context: ValidateTextContext):
    open_delim = context.open_delimiter
    close_delim = context.close_delimiter

    # --- Context validation (at factory creation) ---
    if not isinstance(open_delim, str) or not isinstance(close_delim, str):
        raise ValueError("Delimiters must be valid Unicode strings")
    if not open_delim or not close_delim:
        raise ValueError("Delimiters cannot be empty")
    if open_delim == close_delim:
        raise ValueError("Open and close delimiters must be distinct")
    if open_delim in close_delim or close_delim in open_delim:
        raise ValueError("Delimiters must not overlap structurally")
    if '\n' in open_delim or '\n' in close_delim:
        raise ValueError("Delimiters cannot contain newlines")

    def validate_text(text: Text) -> Union[ValidatedText, None]:
        if not isinstance(text.text, str):
            logging.error(format_error("Text must be a valid Unicode string", text.name, context.line_number))
            return None

        content = text.text
        lines = content.splitlines(keepends=True) or [''] if content == '' else content.splitlines(keepends=True)

        stack_depth = 0
        total_pairs = 0
        pos = 0

        for line_idx, line in enumerate(lines):
            current_line_number = context.line_number + line_idx
            line_start_pos = pos

            while True:
                # Find next open or close delimiter in this line (from current pos)
                rel_pos = pos - line_start_pos
                if rel_pos >= len(line):
                    break

                open_at = line.find(open_delim, rel_pos)
                close_at = line.find(close_delim, rel_pos)

                # Convert to absolute positions
                open_abs = line_start_pos + open_at if open_at != -1 else -1
                close_abs = line_start_pos + close_at if close_at != -1 else -1

                # No more delimiters in this line
                if open_abs == -1 and close_abs == -1:
                    break

                # Determine which comes first
                if (open_abs != -1 and (close_abs == -1 or open_abs < close_abs)):
                    # Open delimiter found
                    if stack_depth > 0:
                        # Nested! Not allowed
                        logging.error(format_error("Nested delimiters are not allowed", text.name, current_line_number))
                        return None
                    stack_depth += 1
                    pos = open_abs + len(open_delim)
                else:
                    # Close delimiter found
                    if stack_depth == 0:
                        logging.error(format_error("Unmatched close delimiter", text.name, current_line_number))
                        return None
                    stack_depth -= 1
                    total_pairs += 1
                    pos = close_abs + len(close_delim)

            pos += len(line) - (len(line) - rel_pos if rel_pos < len(line) else 0)

        # After processing all lines
        if stack_depth != 0:
            # Unbalanced: more opens than closes
            logging.error(format_error("Unbalanced delimiters", text.name, context.line_number + len(lines) - 1))
            return None

        if total_pairs % 2 != 0:
            # Odd number of pairs
            logging.error(format_error(f"Number of delimiter pairs must be even, found {total_pairs}", text.name, context.line_number))
            return None

        return ValidatedText(text=content, name=text.name)

    return validate_text