from typing import Union, Dict, Any
from src.syncspec.error import Error
from src.syncspec.fragment import Fragment
from src.syncspec.block import Block
from src.syncspec.string import String
from src.syncspec.create_blocks_context import CreateBlocksContext
import json
import yaml


def _parse_to_dict(text: str) -> Dict[str, Any]:
    """Parse text as JSON or YAML, with brace wrapping fallback."""
    if not text or not text.strip():
        raise ValueError("Empty text")

    candidates = [text, f"{{{text}}}"]
    for candidate in candidates:
        # Try JSON first
        try:
            res = json.loads(candidate)
            if isinstance(res, dict):
                if None in res:
                    raise ValueError("None keys not allowed")
                if len(res) == 0:
                    raise ValueError("Empty dict not allowed")
                return {str(k): v for k, v in res.items()}
        except Exception:
            pass

        # Try YAML
        try:
            res = yaml.safe_load(candidate)
            if isinstance(res, dict):
                if None in res:
                    raise ValueError("None keys not allowed")
                if len(res) == 0:
                    raise ValueError("Empty dict not allowed")
                # Check if values are all None (indicates bare word parsing)
                if all(v is None for v in res.values()):
                    raise ValueError("Invalid YAML structure")
                return {str(k): v for k, v in res.items()}
            elif res is None:
                continue
        except Exception:
            continue

    raise ValueError(f"Invalid JSON/YAML: {text}")


def make_create_blocks(context: CreateBlocksContext):
    def create_blocks(fragment: Fragment) -> Union[Block, String, None, Error]:
        state = context.index % 4
        res = None

        try:
            if state == 0:
                res = String(fragment.text, fragment.line_number, fragment.name)
            elif state == 1:
                context.prefix = fragment.text
                context.line_number = fragment.line_number
            elif state == 2:
                context.text = fragment.text
            elif state == 3:
                p_dict = _parse_to_dict(context.prefix)
                s_dict = _parse_to_dict(fragment.text)
                directive = p_dict | s_dict
                res = Block(directive, context.prefix, fragment.text, context.text, context.line_number, fragment.name)
        except Exception as e:
            if state == 3:
                res = Error(str(e), fragment.name, context.line_number)
            else:
                raise

        context.index += 1
        return res

    return create_blocks