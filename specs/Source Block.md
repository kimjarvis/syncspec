# Source Block 

## Functional specification


Import this class from file `src/syncspec/error.py`:
```python
from dataclasses import dataclass

@dataclass
class Error:
    message: str
    name: str
    line_number: int
```

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

Import this class from file `src/syncspec/source_block_context.py`:
```python
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Any

@dataclass
class SourceBlockContext:
    state: Dict[str, Any]
    open_delimiter: str
    close_delimiter: str    
```

Do not generate code to initialise the context.
### Implement the unary function Source Block

In the file `src/syncspec/source_block.py`.

Define a closure factory with a unary function with signature:

```python
def make_source_block(context: SourceBlockContext):	
	def source_block(block: Block) -> Union[Tuple[String, Node], Block, Error]:
```

Check that the value of `block.directive["source"]` is a string.

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

If dictionary `Block.directive` contains a key "head" with an integer value h with then:
- Remove the first h lines from `text`.
- If it is not possible to remove h lines from `text` then return an object of type Error, copy the block line_number and name into Error and add an informative message.
And then, if dictionary `Block.directive` contains a key "tail" with an integer value t with then:
- Remove the last t lines from `text`. If it is not possible to remove t lines from `text` then return an object of type Error, copy the block line_number and name into Error and add an informative message.

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

## Package

`src/syncspec` is a Python package.   Imports take the form `from src.syncspec.x import X`.
## Test the unary function  

In the file `tests/test_source_block.py`.

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.
