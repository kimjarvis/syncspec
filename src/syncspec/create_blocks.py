import json
import logging
from typing import Union

from src.syncspec.utilities import format_error
from src.syncspec.fragment import Fragment
from src.syncspec.block import Block
from src.syncspec.string import String
from src.syncspec.create_blocks_context import CreateBlocksContext

logger = logging.getLogger(__name__)


def make_create_blocks(context: CreateBlocksContext):
    def create_blocks(fragment: Fragment) -> Union[Block, String, None]:
        state = context.index % 4
        result: Union[Block, String, None] = None

        try:
            if state == 0:
                result = String(text=fragment.text, line_number=fragment.line_number, name=fragment.name)
            elif state == 1:
                context.prefix = fragment.text
                context.line_number = fragment.line_number
            elif state == 2:
                context.text = fragment.text
            elif state == 3:
                context.line_number = context.line_number  # Redundant but explicit per spec
                prefix_dict = _parse_json(context.prefix, fragment.name, context.line_number)
                suffix_dict = _parse_json(fragment.text, fragment.name, fragment.line_number)

                if prefix_dict is None or suffix_dict is None:
                    return None

                # Check for None keys
                if None in prefix_dict or None in suffix_dict:
                    msg = format_error("Dictionary contains None keys", fragment.name, fragment.line_number)
                    logger.error(msg)
                    return None

                directive = {**prefix_dict, **suffix_dict}
                result = Block(
                    directive=directive,
                    prefix=context.prefix,
                    suffix=fragment.text,
                    text=context.text,
                    line_number=context.line_number,
                    name=fragment.name
                )
        except Exception as e:
            logger.error(format_error(str(e), fragment.name, fragment.line_number))
            return None
        finally:
            context.index += 1

        return result

    def _parse_json(text: str, name: str, line_number: int) -> Union[dict, None]:
        if not text:
            return {}
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            try:
                return json.loads(f"{{{text}}}")
            except json.JSONDecodeError:
                msg = format_error("Invalid JSON", name, line_number)
                logger.error(msg)
                return None

    return create_blocks