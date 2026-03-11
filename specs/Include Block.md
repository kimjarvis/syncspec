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


Import this class from file `src/syncspec/error.py`:
```python
from dataclasses import dataclass

@dataclass
class Error:
    message: str
    name: str
    line_number: int
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
	def include_block(block: Block) -> Union[Tuple[String, Node], Block, Error]:
```

Check that the value of `block.directive["include"]` is a string.

If dictionary `Block.directive` contains a key "include" then:

Return a tuple containing object of type String:
- Copy `line_number` from Block.
- Copy `name` from Block.
- Concatenate these strings in order to create `String.text`:

1. `IncludeBlockContext.open_delimiter`
2. `block.prefix`
3. `IncludeBlockContext.close_delimiter`
4. `IncludeBlockContext.state[key]` where key is the value of `block.directive["include"]`
5. `IncludeBlockContext.open_delimiter`
6. `block.suffix`
7. `IncludeBlockContext.close_delimiter`

The tuple shall also contain an object of type Node:
- Copy `line_number` from Block.
- Copy `name` from Block
- Set the directive type to "include"
- Set the key to  the value of `block.directive["include"]`

- If the key does not exist in the state dictionary then:
	- Return an object of type Error instead. 
	- Copy the `name` and `line_number` from Block.
	- Add an informative error message.

If dictionary `Block.directive` does not contains a key "include" then return an object of type Block:
- Return the input parameter unchanged.

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
