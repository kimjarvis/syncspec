from typing import Union, Dict, Any
import json
import yaml

from src.syncspec.error import Error
from src.syncspec.fragment import Fragment
from src.syncspec.block import Block
from src.syncspec.string import String
from src.syncspec.create_blocks_context import CreateBlocksContext


def _parse_to_dict(text: str) -> Dict[str, Any]:
    """Parse text as JSON or YAML, wrapping in braces if necessary."""
    if not text or not text.strip():
        return {}

    candidates = [text, f"{{{text}}}"]

    for candidate in candidates:
        # Try JSON first (stricter)
        try:
            data = json.loads(candidate)
            if isinstance(data, dict):
                if any(k is None or not isinstance(k, str) for k in data.keys()):
                    continue
                return data
        except (json.JSONDecodeError, ValueError):
            pass

        # Try YAML only if it looks like structured data
        try:
            # Reject bare strings that aren't structured
            if ":" not in candidate and "{" not in candidate and "[" not in candidate:
                continue

            data = yaml.safe_load(candidate)
            if isinstance(data, dict):
                if any(k is None or not isinstance(k, str) for k in data.keys()):
                    continue
                # Reject if all values are None (bare string parsed as mapping)
                if len(data) > 0 and all(v is None for v in data.values()):
                    continue
                return data
        except (yaml.YAMLError, Exception):
            continue

    raise ValueError(f"Invalid JSON/YAML: {text}")


def make_create_blocks(context: CreateBlocksContext):
    def create_blocks(fragment: Fragment) -> Union[Block, String, None, Error]:
        state = context.index % 4

        try:
            if state == 0:
                return String(text=fragment.text, line_number=fragment.line_number)
            elif state == 1:
                context.prefix = fragment.text
                context.line_number = fragment.line_number
                return None
            elif state == 2:
                context.text = fragment.text
                return None
            elif state == 3:
                prefix_dict = _parse_to_dict(context.prefix)
                suffix_dict = _parse_to_dict(fragment.text)
                directive = {**prefix_dict, **suffix_dict}
                return Block(
                    directive=directive,
                    prefix=context.prefix,
                    suffix=fragment.text,
                    text=context.text,
                    line_number=context.line_number
                )
        except Exception as e:
            return Error(
                message=str(e),
                name=context.name,
                line_number=context.line_number
            )
        finally:
            context.index += 1

    return create_blocks