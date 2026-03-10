# Combine Blocks 

## Functional specification


Import this class from file `src/syncspec/block.py`:
```python
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class Block:
    directive: Dict[str, Any]  
    prefix: Optional[str]
    suffix: str
    text: str
    line_number: int    
```

Import this class from file `src/syncspec/string.py`:
```python
from dataclasses import dataclass

@dataclass
class String:
    text: str
    line_number: int    
```

Import this class from file `src/syncspec/combine_blocks_context.py`:
```python
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class CombineBlocksContext:
	text: str
    open_delimiter: str
    close_delimiter: str	
```

Do not generate code to initialise the context.

### Implement the unary function Combine Blocks

In the file `src/syncspec/combine_blocks.py`.

Define a closure factory with a unary function with signature:

```python
def make_combine_blocks(context: CombineBlocksContext):	
	def combine_blocks(block: Block) -> String
```

If `block.prefix` is None:
-  Append `block.text` to the end of string `CombineBlocksContext.text`.
If `block.prefix` is not None, append these fields, in order, to the end of to string `CombineBlocksContext.text`:
1. `CombineBlocksContext.open_delimiter`
2. `block.prefix`
3. `CombineBlocksContext.close_delimiter`
4. `block.text`
5. `CombineBlocksContext.open_delimiter`
6. `block.suffix`
7. `CombineBlocksContext.close_delimiter`

Return an object of class Stop with message string "stopping".

If the parent class of the parameter block is not Block:
- Return the object block.
## Test the unary function  

In the file `tests/test_combine_blocks.py`.

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.
