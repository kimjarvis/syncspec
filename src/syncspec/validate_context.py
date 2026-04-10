import json
import logging
from pathlib import Path
from typing import Union

from pathspec import PathSpec

from syncspec.context import Context
from syncspec.dummy import Dummy
from syncspec.stop import Stop
from syncspec.utilities import format_log_message


def make_validate_context(context: Context):
    def validate_context(fact: Dummy) -> Union[Dummy, Stop]:
        # Logging setup
        logging.root.handlers.clear()
        log_file = getattr(context, 'log_file', None)
        cfg = dict(level=logging.INFO, format="%(levelname)s - %(message)s")
        if log_file:
            cfg["filename"] = str(log_file)
        logging.basicConfig(**cfg)
        logging.info("Syncspec started %s", context.input_path)

        # Validate delimiters
        od, cd = context.open_delimiter, context.close_delimiter
        if not od or not cd or od == cd or od in cd or cd in od or '\n' in od or '\n' in cd:
            logging.error(format_log_message("Invalid delimiters", context.input_path, 0))
            return Stop()

        # Read JSON
        if context.keyvalue_file:
            try:
                with open(context.keyvalue_file, "r", encoding="utf-8") as f:
                    context.keyvalue = json.load(f)
            except (json.JSONDecodeError, OSError) as e:
                logging.error(format_log_message(str(e), context.keyvalue_file, 0))
                return Stop()
        else:
            context.keyvalue = {}

        # Verify ignore_rules file
        ignore_file = context.ignore_rules_file
        if not ignore_file or not ignore_file.is_file():
            fallback = Path(".syncspec_ignore")
            if fallback.is_file():
                context.ignore_rules_file = fallback
                ignore_file = fallback

        if ignore_file and ignore_file.is_file():
            try:
                with open(ignore_file, "r", encoding="utf-8") as f:
                    patterns = f.read().splitlines()
                # Use string-based pattern specification (no import needed)
                PathSpec.from_lines('gitignore', patterns)
            except Exception as e:
                logging.error(format_log_message(str(e), ignore_file, 0))
                return Stop()

        return Dummy()

    return validate_context