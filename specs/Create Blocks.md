# Create Blocks 

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


Import this class from file `src/syncspec/fragment.py`:
```python
from dataclasses import dataclass

@dataclass
class Fragment:  
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



Import this class from file `src/syncspec/create_blocks_context.py`:
```python
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class CreateBlocksContext:
	index: int
	top_directive: str
	text: str
	line_number: int
	name: str
```

Do not generate code to initialise the context.

Assume that:

- Index is initialised to zero.
- top_directive is initialised to the empty string.
### Implement the unary function Create Blocks

In the file `src/syncspec/create_blocks.py`.

Define a closure factory with a unary function with signature:

```python
def make_create_blocks(context: CreateBlocksContext):	
	def create_blocks(fragment: Fragment) -> Union[String, Block, None]:
```

The field `index` acts as a global counter of the number of function calls. 

If index mod 4 equals zero then return an object of type String.
- Copy the Fragment.text into String.text
- Copy the line number into String.

If index mod 4 equals 1 then return None.
- Copy the fragment text into `CreateBlocksContext.top_directive`
- Copy the fragment line_number into the context.

If index mod 4 equals 2 then return None.
- Copy the fragment text into `CreateBlocksContext.text`

If index mod 4 equals 3 then return an object of type Block or Error.
- Copy  `CreateBlocksContext.text` and store it in `Block.text`
- Copy the context line_number into the Block.
- Concatenate "{ " + `top_directive` + " " + fragment text + " }"and store it in `Block.combined_directives`
- Interpret Block.combined_directives as a JSON.  Convert it into a dictionary and store in `Block.directive`.
- If an error occurs converting the string to JSON return an object of type Error, otherwise return an object of type Block.
- Copy the context line_number and name from the context into Error and add an informative text message.



## Package

`src/syncspec` is a Python package.   Imports take the form `from src.syncspec.x import X`.
## Test the unary function  

In the file `tests/test_create_blocks.py`.

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.
