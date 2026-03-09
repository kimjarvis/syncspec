# Source Block 

## Functional specification

Import this class from file `src/syncspec/block.py`:
```python
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Block:
    directive: Dict[str, Any]  
    combined_directives: str
    text: str
    line_number: int    
```

Import this class from file `src/syncspec/source.py`:
```python
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Source:
    directive: Dict[str, Any]  
    text: str
    line_number: int    
```

Import this class from file `src/syncspec/source_block_context.py`:
```python
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Any

@dataclass
class SourceBlockContext:
    state: ClassVar[Dict[str, Any]]
```

### Implement the unary function Source Block

In the file `src/syncspec/source_block.py`.

Define a closure factory with a unary function with signature:

```python
def make_source_block(context: SourceBlockContext):	
	def create_blocks(block: Block) -> Union[Source, Block]:
```

If dictionary `Block.directive` contains a key "source" return an object of type Source:
- Copy `Block.line_number` to Source.
- Copy `Block.text` to Source.
- value shall be the value associated with the key "source".
- Store `Block.text` in `SourceBlockContext.state[value]` .

If dictionary `Block.directive` does not contains a key "source" return an object of type Block:
- Return the input parameter unchanged.

## Test the unary function  

In the file `tests/test_source_block.py`.

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.
