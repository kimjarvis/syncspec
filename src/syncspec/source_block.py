import logging
from typing import Any, Dict, Tuple, Union

from src.syncspec.add_graph_nodes_parameter import AddGraphNodesParameter
from src.syncspec.utilities import format_error
from src.syncspec.parameter_string import String
from src.syncspec.block import Block
from src.syncspec.source_block_context import SourceBlockContext

logger = logging.getLogger(__name__)


def make_source_block(context: SourceBlockContext):
    def source_block(block: Block) -> Union[Tuple[String, AddGraphNodesParameter], Block, String]:
        if "source" not in block.directive:
            return block

        key = block.directive["source"]
        # Spec updated: defaults are now 1
        h = block.directive.get("head", 1)
        t = block.directive.get("tail", 1)

        # Validate head/tail
        if not isinstance(h, int) or h < 0 or not isinstance(t, int) or t < 0:
            msg = "Head and tail must be non-negative integers"
            logger.error(format_error(msg, block.name, block.line_number))
            return _make_error_string(context, block)

        lines = block.text.split('\n')
        if len(lines) < h + t:
            msg = f"Cannot remove {h + t} lines from {len(lines)}"
            logger.error(format_error(msg, block.name, block.line_number))
            return _make_error_string(context, block)

        # Process text
        modified_text = '\n'.join(lines[h : len(lines) - t if t else None])
        context.state[key] = modified_text

        # Construct return objects
        string_obj = _make_decorated_string(context, block)
        node_obj = AddGraphNodesParameter(
            directive_type="source",
            key=key,
            line_number=block.line_number,
            name=block.name
        )
        return (string_obj, node_obj)

    return source_block


def _make_decorated_string(context: SourceBlockContext, block: Block) -> String:
    text = (
        context.open_delimiter +
        block.prefix +
        context.close_delimiter +
        block.text +
        context.open_delimiter +
        block.suffix +
        context.close_delimiter
    )
    return String(text=text, line_number=block.line_number, name=block.name)


def _make_error_string(context: SourceBlockContext, block: Block) -> String:
    return _make_decorated_string(context, block)