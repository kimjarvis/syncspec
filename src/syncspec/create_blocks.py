import json
from typing import Any, Dict

from src.syncspec.error import Error
from src.syncspec.fragment import Fragment
from src.syncspec.block import Block
from src.syncspec.string import String
from src.syncspec.create_blocks_context import CreateBlocksContext


def _parse_json(text: str) -> Dict[str, Any]:
    if not text:
        return {}
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        try:
            data = json.loads(f"{{{text}}}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON")
    if not isinstance(data, dict):
        raise ValueError("JSON must be an object")
    if None in data:
        raise ValueError("None keys not allowed")
    return data


def make_create_blocks(context: CreateBlocksContext):
    def create_blocks(fragment: Fragment) -> Block | String | None | Error:
        state = context.index % 4
        context.index += 1

        if state == 0:
            return String(text=fragment.text, line_number=fragment.line_number, name=fragment.name)

        if state == 1:
            context.prefix = fragment.text
            context.line_number = fragment.line_number
            return None

        if state == 2:
            context.text = fragment.text
            return None

        if state == 3:
            try:
                prefix_dict = _parse_json(context.prefix)
                suffix_dict = _parse_json(fragment.text)
                directive = {**prefix_dict, **suffix_dict}
                return Block(
                    directive=directive,
                    prefix=context.prefix,
                    suffix=fragment.text,
                    text=context.text,
                    line_number=context.line_number,
                    name=fragment.name
                )
            except ValueError as e:
                return Error(
                    message=str(e),
                    name=fragment.name,
                    line_number=context.line_number
                )
        return None
    return create_blocks