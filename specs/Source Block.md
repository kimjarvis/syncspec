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

```python
def make_source_block(context: SourceBlockContext):	
	def source_block(block: Block) -> Union[Tuple[String, Node], Block, String]:
```

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

- If dictionary `Block.directive` contains a key "head", call the value `Block.directive["head"]` h, otherwise let h=0.
- If dictionary `Block.directive` contains a key "tail", call the value `Block.directive["head"]` t, otherwise let t=0.

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
- Imports take the form `from src.syncspec.x import X`.
- Assume Python version 3.10.

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
