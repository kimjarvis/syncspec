import json
import logging
from typing import Union

from syncspec.context import Context
from syncspec.text import Text
from syncspec.stop import Stop
from syncspec.utilities import format_log_message

logger = logging.getLogger(__name__)


def make_write_keyfile(context: Context):
    state = {'last': False}

    def write_keyfile(text: Text) -> Union[Text, Stop]:
        if state['last'] and context.keyvalue_file:
            try:
                context.keyvalue_file.write_text(json.dumps(context.keyvalue))
            except Exception as exc:
                logger.error(format_log_message(
                    f"Failed to write keyvalue file: {exc}",
                    context.keyvalue_file,
                    0
                ))
                return Stop()
        return text

    write_keyfile.state = state  # Expose for external mutation per spec note
    return write_keyfile