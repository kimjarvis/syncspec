# Source Block 

## Functional specification

<!-- {= "include": "format_error", "head": 1, "tail": 1 =} -->

Import logging.

Import the function with this signature from file `src/syncspec/utilities.py`:
```python
def format_error(message: str, name: str, line_number: int) -> str:
```

<!-- {==} -->

<!-- {="import": "src/syncspec/node.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass

@dataclass
class Node:
    directive_type: str
    key: str
    line_number: int
    name: str
```
<!-- {==} -->

<!-- {="import": "src/syncspec/string.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass

@dataclass
class String:
    text: str
    line_number: int
    name: str
```
<!-- {==} -->

<!-- {="import": "src/syncspec/block.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class Block:
    directive: Dict[str, Any]
    prefix: str
    suffix: str
    text: str
    line_number: int
    name: str
```
<!-- {==} -->

<!-- {="import": "src/syncspec/source_block_context.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Any

@dataclass
class SourceBlockContext:
    state: Dict[str, Any]
    open_delimiter: str
    close_delimiter: str
```
<!-- {==} -->

Do not generate code to initialise the context.
### Implement a unary function

In the file `src/syncspec/source_block.py`.

Define a closure factory with a unary function with signature:

<!-- {="source": "signature:source_block", "head": 2, "tail": 2=} -->
```python
def make_source_block(context: SourceBlockContext):	
	def source_block(block: Block) -> Union[Tuple[String, Node], Block, String]:

```
<!-- {==} -->

If dictionary `Block.directive` contains a key "source" then:

Return a tuple containing object of type String:
- Copy `line_number` from Block.
- Copy `name` from Block
- Concatenate these strings in order to create `String.text`:

1. `SourceBlockContext.open_delimiter`
2. `block.prefix`
3. `SourceBlockContext.close_delimiter`
4. `block.text`
5. `SourceBlockContext.open_delimiter`
6. `block.suffix`
7. `SourceBlockContext.close_delimiter`

Copy to `Block.text` to `text`.

- If dictionary `Block.directive` contains a key "head", call the value `Block.directive["head"]` h, otherwise let h=1.
- If dictionary `Block.directive` contains a key "tail", call the value `Block.directive["tail"]` t, otherwise let t=1.

The default value of "head" and "tail" shall be 1. 

Ensure that:

- h is a positive integer or zero.
- t is a positive integer or zero,
- t+h lines can be removed from `text`.
When any of the validation conditions are violated Log and error and return a String.

- If `h>0`, remove the first h lines from `text`.
- If `t>0`, remove the last t lines from `text`. 

And add a key value pair to the `SourceBlockContext.state` dictionary:
- key is the value of `block.directive["source"]`
- Store `text` in `SourceBlockContext.state[key]` .

The tuple shall also contain an object of type Node:
- Copy `line_number` from Block.
- Copy `name` from Block
- Set the directive type to "source"
- Set the key to  the value of `block.directive["source"]`

If dictionary `Block.directive` does not contains a key "source" then return an object of type Block:
- Return the input parameter `block` unchanged.

#### Log and error and return a String

When conditions are violated:
- Call `format_error` to format an error messages.  Pass an informative message,   `Block.name` and the line number on which the error was detected.  Use python logging to log the error.
- Return an object of type `String`.
	- Copy name and line number from block.
	- `String.text = SourceBlockContext.open_delimiter + Block.prefix + SourceBlockContext.close_delimiter + Block.text + SourceBlockContext.open_delimiter + Block.suffix + SourceBlockContext.close_delimiter

<!-- {= "include": "package", "head": 1, "tail": 1 =} -->
## Package

- The function is part of the python package `src/syncspec` .   
- Imports from the package take the form `from src.syncspec.x import X`.
- Assume Python version 3.7.

<!-- {==} -->
## Test the unary function  

In the file `tests/test_source_block.py`.

<!-- {= "include": "generate_tests", "head": 1, "tail": 1 =} -->

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

<!-- {==} -->

<!-- {= "include": "explain_the_solution", "head": 1, "tail": 1 =} -->
## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.

<!-- {==} -->

<!-- {= "include": "current_implementation", "head": 1, "tail": 1 =} -->
## Current implementation

- Minimise changes to the current implementation.

This is the current implementation:
<!-- {==} -->

<!-- {= "import": "src/syncspec/source_block.py", "head": 2, "tail": 2 =} -->
```python
import logging
from typing import Any, Dict, Tuple, Union

from src.syncspec.node import Node
from src.syncspec.utilities import format_error
from src.syncspec.string import String
from src.syncspec.block import Block
from src.syncspec.source_block_context import SourceBlockContext

logger = logging.getLogger(__name__)


def make_source_block(context: SourceBlockContext):
    def source_block(block: Block) -> Union[Tuple[String, Node], Block, String]:
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
        node_obj = Node(
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
```
<!-- {==} -->


<!-- {= "import": "tests/test_source_block.py", "head": 2, "tail": 2 =} -->
```python
import pytest
from src.syncspec.source_block import make_source_block
from src.syncspec.source_block_context import SourceBlockContext
from src.syncspec.block import Block
from src.syncspec.string import String
from src.syncspec.node import Node


@pytest.mark.parametrize(
    "directive, expected_type",
    [
        ({}, Block),
        ({"source": "key"}, tuple),
    ]
)
def test_directive_handling(directive, expected_type):
    ctx = SourceBlockContext(state={}, open_delimiter="[", close_delimiter="]")
    block = Block(directive=directive, prefix="", suffix="", text="a\nb\nc", line_number=1, name="test")
    func = make_source_block(ctx)
    result = func(block)
    assert isinstance(result, expected_type)


@pytest.mark.parametrize(
    "head, tail, text, should_fail",
    [
        (0, 0, "a\nb\nc", False),
        (1, 1, "a\nb\nc", False),
        (1, 1, "a", True),  # Fails with default 1+1=2 lines required
        (-1, 0, "a", True),
        (0, 5, "a\nb", True),
    ]
)
def test_head_tail_validation(head, tail, text, should_fail):
    ctx = SourceBlockContext(state={}, open_delimiter="[", close_delimiter="]")
    directive = {"source": "key", "head": head, "tail": tail}
    block = Block(directive=directive, prefix="", suffix="", text=text, line_number=1, name="test")
    func = make_source_block(ctx)
    result = func(block)

    if should_fail:
        assert isinstance(result, String)
        assert "key" not in ctx.state
    else:
        assert isinstance(result, tuple)
        assert "key" in ctx.state


def test_default_head_tail():
    ctx = SourceBlockContext(state={}, open_delimiter="[", close_delimiter="]")
    directive = {"source": "key"}  # Defaults to head=1, tail=1
    block = Block(directive=directive, prefix="", suffix="", text="line1\nline2\nline3", line_number=1, name="test")
    func = make_source_block(ctx)
    func(block)
    assert ctx.state["key"] == "line2"


def test_state_update():
    ctx = SourceBlockContext(state={}, open_delimiter="[", close_delimiter="]")
    directive = {"source": "my_key", "head": 1, "tail": 0}
    block = Block(directive=directive, prefix="", suffix="", text="line1\nline2", line_number=1, name="test")
    func = make_source_block(ctx)
    func(block)
    assert ctx.state["my_key"] == "line2"
```
<!-- {==} -->