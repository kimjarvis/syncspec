# Create Blocks 

## Functional specification


<!-- {= "include": "format_error", "head": 1, "tail": 1 =} -->

Import logging.

Import the function with this signature from file `src/syncspec/utilities.py`:
```python
def format_error(message: str, name: str, line_number: int) -> str:
```

<!-- {==} -->

<!-- {= "import": "src/syncspec/fragment.py", "head": 2, "tail": 2 =} -->
```python
from dataclasses import dataclass

@dataclass
class Fragment:
    text: str
    line_number: int
    name: str
```
<!-- {==} -->

<!-- {= "import": "src/syncspec/block.py", "head": 2, "tail": 2 =} -->
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

<!-- {= "import": "src/syncspec/string.py", "head": 2, "tail": 2 =} -->
```python
from dataclasses import dataclass

@dataclass
class String:
    text: str
    line_number: int
    name: str
```
<!-- {==} -->

<!-- {= "import": "src/syncspec/create_blocks_context.py", "head": 2, "tail": 2 =} -->
```python
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class CreateBlocksContext:
	index: int
	prefix: str
	prefix_line_number: int
	prefix_valid: bool
	directive: Dict[str, Any]
	text: str
	open_delimiter: str
	close_delimiter: str


```
<!-- {==} -->


Do not generate code to initialise the context.

Assume that:

- Index is initialised to zero.
### Implement the unary function Create Blocks

In the file `src/syncspec/create_blocks.py`.

Define a closure factory with a unary function with signature:

```python
def make_create_blocks(context: CreateBlocksContext):	
	def create_blocks(fragment: Fragment) -> Union[Block, String, None]:
```

The field `index` acts as a global counter of the number of function calls.  Index is incremented after processing the current state to ensure the modulo check corresponds to the current call count (0-based).

If index mod 4 equals zero then return an object of type `String`.
- Return a `Sting` object constructed using field values from `Fragment`.

If index mod 4 equals 1 then:
- Copy the fragment text into `CreateBlocksContext.prefix`
- Copy the fragment line_number into `CreateBlocksContext.prefix_line_number`
- Copy the fragment name into `CreateBlocksContext.prefix_name`
- Interpret `Fragment.text` as JSON.  Parse text as JSON object, wrapping in braces if necessary.  Supports raw fragments and complete objects.  Convert the resulting JSON object to a dictionary.  An empty string is valid.    

If dictionary creation is successful:
- Set `CreateBlocksContext.prefix_valid` to True.  
- Store the dictionary in `CreateBlocksContext.directive`.
- Return None.

If an error occurs when converting the strings to JSON or when converting the JSON to a dictionary.
- Call `format_error` to format an error messages.  Pass an informative message,   `Fragment.name` and the line number on which the error was detected.  Use python logging to log the error.
- Return an object of type `String` constructed using field values from `Fragment`.
	- Copy the line number and name
	- `String.text = CreateBlocksContext.open_delimiter + Fragment.text + CreateBlocksContext.close_delimiter

If index mod 4 equals 2 and `CreateBlocksContext.prefix_valid` is True then:
- Copy the fragment text into `CreateBlocksContext.text`
- Return None.

If index mod 4 equals 2 and `CreateBlocksContext.prefix_valid` is False then:
- Return an object of type `String` constructed using field values from `Fragment`.

If index mod 4 equals 3 and and `CreateBlocksContext.prefix_valid` is True then:
- Copy  `CreateBlocksContext.prefix` and store it in `Block.prefix`
- Copy `CreateBlocksContext.directive` and store it in `Block.directive`
- Copy  `CreateBlocksContext.text` and store it in `Block.text`
- Copy  `Fragment.text` and store it in `Block.suffix`
- Copy  `Fragment.name` and store it in `Block.name`
- Copy the `CreateBlocksContext.prefix_line_number` into the Block.
- Return an object of type Block.

If index mod 4 equals 3 and and `CreateBlocksContext.prefix_valid` is False then:
- Return an object of type `String` constructed using field values from `Fragment`.
	- Copy the line number and name
	- `String.text = CreateBlocksContext.open_delimiter + Fragment.text + CreateBlocksContext.close_delimiter

#### Assume that

- Ensure that keys are valid strings.  Reject dictionaries containing None keys.
- Mutable Context: `CreateBlocksContext` is mutable and shared across calls to the closure.
- Brace Wrapping: If raw text fails parsing, {} are added around the text and parsing is retried.  That is, try `json.loads`, and if that fails, attempt `json.loads('{' + text + '}')`.


<!-- {= "include": "package", "head": 1, "tail": 1 =} -->
## Package

- The function is part of the python package `src/syncspec` .   
- Imports from the package take the form `from src.syncspec.x import X`.
- Assume Python version 3.7.

<!-- {==} -->
## Test the unary function  

In the file `tests/test_create_blocks.py`.

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
