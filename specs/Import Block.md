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

 Verify at context at initialization time:
- import_path is a valid directory path.
### Implement the unary function Import Block

In the file `src/syncspec/import_block.py`.

Define a closure factory with a unary function with signature:

```python
def make_import_block(context: ImportBlockContext):	
	def import_block(block: Block) -> Union[Tuple[String, Node], Block, Error]:
```

Check that the value of `block.directive["import"]` is a string.

If dictionary `Block.directive` contains a key "import" then:

The value of `block.directive["import"]` is a relative file or symbolic link path.  The path is relative to the directory path `ImportBlockContext.import_path`.  Verify that:  
- The file must be in directory `ImportBlockContext.import_path` or one of its sub-directories.  Accessing a parent directory is not allowed.
- If the file is a symbolic link then the link target must also be in the directory `ImportBlockContext.import_path` or one of its sub-directories.  
- The file exists.  
- The file is a text file, not a binary file.  Treat it as utf-8. 
- The file is readable.

If any of these conditions are not met, return an object of type Error, copy the block line_number and name into Error and add an informative message.

Read the content of the file into string variable v.

If dictionary `Block.directive` contains a key "head" with an integer value h with then:
- Remove the first h lines from v.
- If it is not possible to remove h lines from v then return an object of type Error, copy the block line_number and name into Error and add an informative message.
And then, if dictionary `Block.directive` contains a key "tail" with an integer value t with then:
- Remove the last t lines from v. If it is not possible to remove t lines from v then return an object of type Error, copy the block line_number and name into Error and add an informative message.

First apply head then apply tail to the result. Negative head or tail values shall be rejected as invalid, head=0 or tail=0 are valid no-ops.

Return a tuple containing object of type String:
- Copy `line_number` from Block.
- Copy `name` from Block.
- Concatenate these strings in order to create `String.text`:

1. `ImportBlockContext.open_delimiter`
2. `block.prefix`
3. `ImportBlockContext.close_delimiter`
4. The value v
5. `ImportBlockContext.open_delimiter`
6. `block.suffix`
7. `ImportBlockContext.close_delimiter`

The tuple shall also contain an object of type Node:
- Copy `line_number` from Block.
- Copy `name` from Block
- Set the directive type to "import"
- Set the key to  the value of `block.directive["import"]`

If dictionary `Block.directive` does not contains a key "import" then return an object of type Block:
- Return the input parameter unchanged.

## Package

`src/syncspec` is a Python package.   Imports take the form `from src.syncspec.x import X`.
## Test the unary function  

In the file `tests/test_import_block.py`.

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.
