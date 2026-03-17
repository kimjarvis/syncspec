# Import Block 

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

Import this class from file `src/syncspec/import_block_context.py`:
```python
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Any

@dataclass
class ImportBlockContext:
	import_path: str
    open_delimiter: str
    close_delimiter: str    
```

Do not generate code to initialise the context.

### Implement the unary function Import Block

In the file `src/syncspec/import_block.py`.

Define a closure factory with a unary function with signature:

```python
def make_import_block(context: ImportBlockContext):	
	def import_block(block: Block) -> Union[Tuple[String, Node, Node], Block, String]:
```

If dictionary `Block.directive` contains a key "import" then:

The value of `block.directive["import"]` is a relative file or symbolic link path.  The path is relative to the directory path `ImportBlockContext.import_path`.  

Ensure that:  
- The file must be in directory `ImportBlockContext.import_path` or one of its sub-directories.  Accessing a parent directory is not allowed.
- If the file is a symbolic link then the link target must also be in the directory `ImportBlockContext.import_path` or one of its sub-directories.  
- The file exists.  
- The file is a text file, not a binary file.  Treat it as utf-8. 
- The file is readable.
When any of the validation conditions are violated Log and error and return a String.

Read the content of the file into string variable `v`.

Copy string `block.text` to `u`.

If dictionary `Block.directive` contains a key "head" with an integer value call it head, otherwise set `head=0`.  

Let top be the first head lines of `u`.

If dictionary `Block.directive` contains a key "tail" with an integer value call it tail, otherwise set `tail=0`.

Let bottom be the last tail lines of `u`.

Assume that:

- Directive values `Block.directive["head"]=0`  and `Block.directive["tail"]=0` are valid no-ops even when `u` is an empty string.
 
Ensure that:
- `v` is a string.
- Strings top and bottom do not overlap.  Overlap is defined strictly as `head + tail > total_lines`. 
- Negative head or tail values shall be rejected as invalid.
When any of the validation conditions are violated Log and error and return a String.

Return a tuple containing object of type String:
- Copy `line_number` from Block.
- Copy `name` from Block.
- Concatenate these strings in order to create `String.text`:

1. `ImportBlockContext.open_delimiter`
2. `block.prefix`
3. `ImportBlockContext.close_delimiter`
4. `top`, the first h lines of `block.text`
5. The value of v
6. A new line character `\n`
7. `bottom` the last t lines of `block.text`
8. `ImportBlockContext.open_delimiter`
9. `block.suffix`
10. `ImportBlockContext.close_delimiter`

The tuple shall also contain an object of type Node:
- The `line_number` shall be zero.
- `name` shall be the value of `block.directive["import"]` 
- Set the directive type to "export"
- Set the key to  the value of `block.directive["import"]`

The tuple shall also contain another object of type Node:
- Copy `line_number` from Block.
- Copy `name` from Block
- Set the directive type to "import"
- Set the key to  the value of `block.directive["import"]` 

If dictionary `Block.directive` does not contains a key "import" then return an object of type Block:
- Return the input parameter unchanged.

#### Log and error and return a String

When conditions are violated:
- Call `format_error` to format an error messages.  Pass an informative message,   `Block.name` and the line number on which the error was detected.  Use python logging to log the error.
- Return an object of type `String`.
	- Copy name and line number from block.
	- `String.text = ImportBlockContext.open_delimiter + Block.prefix + ImportBlockContext.close_delimiter + Block.text + ImportBlockContext.open_delimiter + Block.suffix + ImportBlockContext.close_delimiter

#### Assume that

- Line Splitting:  `splitlines(keepends=True)` is used to define "lines". This preserves newline characters during slicing and reconstruction.
- Integer Validation: Boolean values are excluded from integer checks for head/tail (since bool is a subclass of int in Python).
## Package

- `src/syncspec` is a Python package.   Imports take the form `from src.syncspec.x import X`.
- Assume Python version 3.10.

## Test the unary function  

In the file `tests/test_import_block.py`.

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.
