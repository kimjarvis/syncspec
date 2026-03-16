# Include Block 

## Functional specification

Import this class from file `src/syncspec/node.py`:
```python
from dataclasses import dataclass

@dataclass
class Node:
    directive_type: str
    key: str
    line_number: int    
    name: str
```

Import logging.
Import the function with this signature from file `src/syncspec/utilities.py`:
```python
def format_error(message: str, name: str, line_number: int) -> str:
```

Import this class from file `src/syncspec/string.py`:
```python
from dataclasses import dataclass

@dataclass
class String:
    text: str
    line_number: int
    name: str
```

Import this class from file `src/syncspec/block.py`:
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

Import this class from file `src/syncspec/include_block_context.py`:
```python
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Any

@dataclass
class IncludeBlockContext:
    state: Dict[str, Any]
    open_delimiter: str
    close_delimiter: str    
```

Do not generate code to initialise the context.

### Implement the unary function Include Block

In the file `src/syncspec/include_block.py`.

Define a closure factory with a unary function with signature:

```python
def make_include_block(context: IncludeBlockContext):	
	def include_block(block: Block) -> Union[Tuple[String, Node], Block]:
```

Check that the value of `block.directive["include"]` is a string.

If dictionary `Block.directive` contains a key "include" then:

Fetch the string `v` from `IncludeBlockContext.state[key]` where key is the value of `block.directive["include"]`.

Copy string `block.text` to `u`.

If dictionary `Block.directive` contains a key "head" with an integer value call it head, otherwise set `head=0`.  

Let top be the first head lines of `u`.

If dictionary `Block.directive` contains a key "tail" with an integer value call it tail, otherwise set `tail=0`.

Let bottom be the last tail lines of `u`.

Assume that:

- Directive values `Block.directive["head"]=0`  and `Block.directive["head"]=0` are valid no-ops even when `u` is an empty string.
 
Ensure that:

- `v` is a string.
- Strings top and bottom do not overlap.  Overlap is defined strictly as `head + tail > total_lines`. 
- Negative head or tail values shall be rejected as invalid.

When any of the validation conditions are violated:
- Call `format_error` to format an error messages.  Pass an informative message,   `Block.name` and the line number on which the error was detected.  Use python logging to log the error.
- Return the input parameter `block` unchanged.

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

If the key does not exist in the state dictionary or the value of `block.directive["include"]` is not a string then:
- Call `format_error` to format an error messages.  Pass an informative message,   `Block.name` and the line number on which the error was detected.  Use python logging to log the error.
- Return the input parameter `block` unchanged.

If dictionary `Block.directive` does not contains a key "include" then return an object of type Block:

- Return the input parameter `block` unchanged.

#### Assume that

- Line Splitting:  `splitlines(keepends=True)` is used to define "lines". This preserves newline characters during slicing and reconstruction.
- Integer Validation: Boolean values are excluded from integer checks for head/tail (since bool is a subclass of int in Python).

## Package

`src/syncspec` is a Python package.   Imports take the form `from src.syncspec.x import X`.
## Test the unary function  

In the file `tests/test_include_block.py`.

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.
