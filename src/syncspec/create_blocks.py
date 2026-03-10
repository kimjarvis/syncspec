import json
import yaml
from typing import Union, Dict, Any, Optional

from src.syncspec.error import Error
from src.syncspec.fragment import Fragment
from src.syncspec.block import Block
from src.syncspec.create_blocks_context import CreateBlocksContext


def _parse_directive(text: str) -> Dict[str, Any]:
    """Parse JSON/YAML fragment or object into a dictionary with string keys."""
    if not text.strip():
        return {}

    for loader in (json.loads, yaml.safe_load):
        for candidate in (text, "{ " + text + " }"):
            try:
                data = loader(candidate)
                if isinstance(data, dict):
                    if all(isinstance(k, str) for k in data.keys()):
                        return data
            except Exception:
                continue
    raise ValueError(f"Invalid JSON/YAML: {text}")


def make_create_blocks(context: CreateBlocksContext):
    def create_blocks(fragment: Fragment) -> Union[Block, None, Error]:
        state = context.index % 4
        result = None

        if state == 0:
            result = Block(
                directive={'text': ''},
                prefix=None,
                suffix=None,
                text=fragment.text,
                line_number=fragment.line_number
            )
        elif state == 1:
            context.prefix = fragment.text
            context.line_number = fragment.line_number
        elif state == 2:
            context.text = fragment.text
        elif state == 3:
            try:
                directive = {**_parse_directive(context.prefix), **_parse_directive(fragment.text)}
                result = Block(
                    directive=directive,
                    prefix=context.prefix,
                    suffix=fragment.text,
                    text=context.text,
                    line_number=context.line_number
                )
            except Exception as e:
                result = Error(
                    message=f"Directive parse failed: {str(e)}",
                    name=context.name,
                    line_number=context.line_number
                )

        context.index += 1
        return result

    return create_blocks