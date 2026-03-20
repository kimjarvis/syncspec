# Include Block 

## Functional specification

<!-- {= "include": "format_error", "head": 1, "tail": 1 =} -->

Import logging.

Import the function with this signature from file `src/syncspec/utilities.py`:
```python
def format_error(message: str, name: str, line_number: int) -> str:
```

<!-- {==} -->

<!-- {="import": "src/syncspec/node.py", "head": 2, "tail": 2 =} -->
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

<!-- {="import": "src/syncspec/string.py", "head": 2, "tail": 2, "eol": true =} -->
```python
from dataclasses import dataclass

@dataclass
class String:
    text: str
    line_number: int
    name: str
```
<!-- {==} -->

<!-- {="import": "src/syncspec/block.py", "head": 2, "tail": 2,  "eol": true =} -->
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

<!-- {="import": "src/syncspec/include_block_context.py", "head": 2, "tail": 2,  "eol": true =} -->
```python
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Any

@dataclass
class IncludeBlockContext:
    state: Dict[str, Any]
    open_delimiter: str
    close_delimiter: str
```
<!-- {==} -->

Do not generate code to initialise the context.
### Implement a unary function

In the file `src/syncspec/include_block.py`.

Define a closure factory with a unary function with signature:

```python
def make_include_block(context: IncludeBlockContext):	
	def include_block(block: Block) -> Union[Tuple[String, Node], Block, String]:
```

Check that the value of `block.directive["include"]` is a string.

If dictionary `Block.directive` contains a key "include" then:

Ensure that:
- The value of `block.directive["include"]` is a string.  Call it key.
- The key exists in the dictionary `IncludeBlockContext.state`.
When any of the validation conditions are violated Log and error and return a String.

Fetch the string `v` from `IncludeBlockContext.state[key]` where key is the value of `block.directive["include"]`.

Copy string `block.text` to `u`.

If dictionary `Block.directive` contains a key "head" with an integer value call it head, otherwise set `head=1`.  

Let top be the first head lines of `u`.

If dictionary `Block.directive` contains a key "tail" with an integer value call it tail, otherwise set `tail=1`.

Let bottom be the last tail lines of `u`.

Ensure that:
- `v` is a string.
- Strings top and bottom do not overlap.  Overlap is defined strictly as `head + tail > total_lines`. 
- Negative head or tail values shall be rejected as invalid.
When any of the validation conditions are violated Log and error and return a String.

Return a tuple containing object of type String:
- Copy `line_number` from Block.
- Copy `name` from Block.
- Concatenate these strings in order to create `String.text`:

1. `IncludeBlockContext.open_delimiter`
2. `block.prefix`
3. `IncludeBlockContext.close_delimiter`
4. `top`, the first h lines of `block.text`
5. The value of `IncludeBlockContext.state[key]`
6. `bottom` the last t lines of `block.text`
7. `IncludeBlockContext.open_delimiter`
8. `block.suffix`
9. `IncludeBlockContext.close_delimiter`

The tuple shall also contain an object of type Node:
- Copy `line_number` from Block.
- Copy `name` from Block
- Set the directive type to "include"
- Set the key to  the value of `block.directive["include"]`

If dictionary `Block.directive` does not contains a key "include" then return an object of type Block:

- Return the input parameter `block` unchanged.

#### Log and error and return a String

When conditions are violated:
- Call `format_error` to format an error messages.  Pass an informative message,   `Block.name` and the line number on which the error was detected.  Use python logging to log the error.
- Return an object of type `String`.
	- Copy name and line number from block.
	- `String.text = IncludeBlockContext.open_delimiter + Block.prefix + IncludeBlockContext.close_delimiter + Block.text + IncludeBlockContext.open_delimiter + Block.suffix + IncludeBlockContext.close_delimiter

#### Assume that

- Line Splitting:  `splitlines(keepends=True)` is used to define "lines". This preserves newline characters during slicing and reconstruction.
- Integer Validation: Boolean values are excluded from integer checks for head/tail (since bool is a subclass of int in Python).

<!-- {= "include": "package", "head": 1, "tail": 1 =} -->
## Package

- The function is part of the python package `src/syncspec` .   
- Imports from the package take the form `from src.syncspec.x import X`.
- Assume Python version 3.7.

<!-- {==} -->
## Test the unary function  

In the file `tests/test_include_block.py`.

<!-- {= "include": "generate_tests", "head": 1, "tail": 1 =} -->

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

<!-- {==} -->

<!-- {= "include": "explain_the_solution" =} -->
## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.

<!-- {==} -->

<!-- {= "source": "current_implementation" =} -->
## Current implementation

- Minimise changes to the current implementation.

This is the current implementation:

<!-- {==} -->

<!-- {= "import": "src/syncspec/include_block.py", "head": 2, "tail": 2 =} -->
```python
import logging
from typing import Union, Tuple

from src.syncspec.node import Node
from src.syncspec.utilities import format_error
from src.syncspec.string import String
from src.syncspec.block import Block
from src.syncspec.include_block_context import IncludeBlockContext


def make_include_block(context: IncludeBlockContext):
    def include_block(block: Block) -> Union[Tuple[String, Node], Block, String]:
        def return_error(msg: str) -> String:
            logging.error(format_error(msg, block.name, block.line_number))
            return String(
                text=context.open_delimiter + block.prefix + context.close_delimiter +
                     block.text +
                     context.open_delimiter + block.suffix + context.close_delimiter,
                line_number=block.line_number,
                name=block.name
            )

        if "include" not in block.directive:
            return block

        key = block.directive["include"]
        if not isinstance(key, str):
            return return_error("'include' directive must be a string")

        if key not in context.state:
            return return_error(f"include key '{key}' not found in context")

        v = context.state[key]
        if not isinstance(v, str):
            return return_error(f"value for key '{key}' must be a string")

        head = block.directive.get("head", 1)
        tail = block.directive.get("tail", 1)

        if isinstance(head, bool) or not isinstance(head, int) or head < 0:
            return return_error("'head' must be a non-negative integer")
        if isinstance(tail, bool) or not isinstance(tail, int) or tail < 0:
            return return_error("'tail' must be a non-negative integer")

        lines = block.text.splitlines(keepends=True)
        total_lines = len(lines)

        if head + tail > total_lines:
            return return_error(f"head ({head}) + tail ({tail}) exceeds total lines ({total_lines})")

        top = "".join(lines[:head])
        bottom = "".join(lines[-tail:]) if tail > 0 else ""

        s_text = (
            context.open_delimiter + block.prefix + context.close_delimiter +
            top + v + bottom +
            context.open_delimiter + block.suffix + context.close_delimiter
        )

        s_obj = String(text=s_text, line_number=block.line_number, name=block.name)
        n_obj = Node(directive_type="include", key=key, line_number=block.line_number, name=block.name)

        return s_obj, n_obj

    return include_block
```
<!-- {==} -->

<!-- {= "import": "tests/test_include_block.py", "head": 2, "tail": 2 =} -->
```python
import pytest
from unittest.mock import patch
from src.syncspec.include_block import make_include_block
from src.syncspec.block import Block
from src.syncspec.string import String
from src.syncspec.node import Node
from src.syncspec.include_block_context import IncludeBlockContext

@pytest.mark.parametrize("directive,expected_type", [
    ({}, Block),
    ({"include": "key1"}, tuple),
    ({"include": 123}, String),
    ({"include": "missing"}, String),
    ({"include": "key1", "head": -1}, String),
    ({"include": "key1", "head": 10}, String),
])
def test_include_block_logic(directive, expected_type):
    ctx = IncludeBlockContext(state={"key1": "INSERTED"}, open_delimiter="[", close_delimiter="]")
    block = Block(
        directive=directive,
        prefix="p", suffix="s",
        text="line1\nline2\n",
        line_number=1, name="test"
    )
    func = make_include_block(ctx)
    result = func(block)
    assert isinstance(result, expected_type)

def test_include_block_success_content():
    ctx = IncludeBlockContext(state={"k": "VAL"}, open_delimiter="<", close_delimiter=">")
    block = Block(
        directive={"include": "k", "head": 1, "tail": 1},
        prefix="P", suffix="S",
        text="A\nB\nC\n",
        line_number=5, name="src"
    )
    func = make_include_block(ctx)
    res, node = func(block)
    assert isinstance(res, String) and isinstance(node, Node)
    assert res.text == "<P>A\nVALC\n<S>"
    assert node.key == "k"
```
<!-- {==} -->