import logging
import json
from typing import Union, Dict, Any

from src.syncspec.utilities import format_error
from src.syncspec.fragment import Fragment
from src.syncspec.block import Block
from src.syncspec.parameter_string import String
from src.syncspec.create_blocks_context import CreateBlocksContext


def _parse_json_content(text: str) -> Dict[str, Any]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        try:
            data = json.loads('{' + text + '}')
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON structure")

    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object")
    if any(k is None for k in data.keys()):
        raise ValueError("Dictionary contains None keys")
    return data


def make_create_blocks(context: CreateBlocksContext):
    def create_blocks(fragment: Fragment) -> Union[Block, String, None]:
        state = context.index % 4
        result: Union[Block, String, None] = None

        if state == 0:
            result = String(text=fragment.text, line_number=fragment.line_number, name=fragment.name)

        elif state == 1:
            context.prefix = fragment.text
            context.prefix_line_number = fragment.line_number
            # Spec requests context.prefix_name = fragment.name, but field missing in class.

            try:
                context.directive = _parse_json_content(fragment.text)
                context.prefix_valid = True
                result = None
            except (json.JSONDecodeError, ValueError):
                context.prefix_valid = False
                logging.error(format_error("JSON parsing failed", fragment.name, fragment.line_number))
                result = String(
                    text=context.open_delimiter + fragment.text + context.close_delimiter,
                    line_number=fragment.line_number,
                    name=fragment.name
                )

        elif state == 2:
            if context.prefix_valid:
                context.text = fragment.text
                result = None
            else:
                result = String(text=fragment.text, line_number=fragment.line_number, name=fragment.name)

        elif state == 3:
            if context.prefix_valid:
                result = Block(
                    directive=context.directive,
                    prefix=context.prefix,
                    suffix=fragment.text,
                    text=context.text,
                    line_number=context.prefix_line_number,
                    name=fragment.name
                )
            else:
                result = String(
                    text=context.open_delimiter + fragment.text + context.close_delimiter,
                    line_number=fragment.line_number,
                    name=fragment.name
                )

        context.index += 1
        return result

    return create_blocks