## Import 

Import `Context` from file `context.py`

<!-- {- import="../src/syncspec/context.py",  head=2,  tail=2 -} -->
```python
from dataclasses import dataclass, field
from typing import Any, Dict, List
from pathlib import Path

@dataclass
class Context:
    open_delimiter: str
    close_delimiter: str
    keyvalue: dict
    input_path: Path
    keyvalue_file: Path
    ignore_rules_file: Path
```
<!-- {--} -->
<!-- {- import="../src/syncspec/directive.py",  head=2,  tail=2 -} -->
```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Directive:
    parameters: dict
    prefix: str
    text: str
    suffix: str
    path: Path
    prefix_line_number: int
    text_line_number: int
    suffix_line_number: int
```
<!-- {--} -->
<!-- {- import="../src/syncspec/stop.py",  head=2,  tail=2 -} -->
```python
from dataclasses import dataclass

@dataclass
class Stop:
    pass
```
<!-- {--} -->
## Implement a unary function

In the file `src/syncspec/import_directive.py`.

Define a closure factory with a unary function with signature:

<!-- {- source="import_directive_spec" -} -->
```python
def make_import_directive(context: Context):
    def import_directive(directive: Directive) -> Union[Directive,Stop]:

```
<!-- {--} -->

<!-- {- source="import_directive_action" -} -->
## Import Directive

- If the directive contains the key "import":
	- Import the file.
	- Return a new `Directive` object.
<!-- {--} -->
#### Steps

- If dictionary `directive.parameters` contains the key "import" then:
	- Note that the value of `directive.parameters["import"]` is a file path relative to the directory part of the file path `Directive.path`.  
	- Ensure that:  
		- The file must be in directory `Context.input_path` or one of its sub-directories.  Accessing a parent directory is not allowed.
		- If the file is a symbolic link then the link target must also be in the directory or one of its sub-directories.  Accessing a parent directory is not allowed.
		- The file must exist.
		- The file must be a text file.
		- The file must be readable.
	- Read the file into the variable `input`
	- If the last character of `input` is not an end of line character `\n` then:
		- Add an end of line character to the end of `input`.
	- If dictionary `directive.parameters` contains the key "head" then:
		- Ensure that:
			- The value is an integer call it `head`.
	- Otherwise, `head=1`
	- If dictionary `directive.parameters` contains the key "tail" then:
		- Ensure that:
			- The value is an integer call it `tail`.
	- Otherwise, `tail=1`
	- Ensure that:
		- `head + tail <=`  the number of lines in  `Directive.text`.
	- Call the first `head` lines from  `Directive.text` `top`
	- Call the last `tail` lines from   `Directive.text` `bottom`
	- Return a `Directive` object:
		- Copy fields from `directive`
		- Set `Directive.text` to be the concatenation `top + input + bottom`.  
	- When any of the ensured conditions are violated:
		- Log an error with an informative message.
			- Use the `prefix_line_number`.
		- Return an object of type `Stop`.  
- Otherwise, return the `Directive` object.
#### Note

- "Text file" validation shall be handled by attempting UTF-8 decoding. Binary files will raise `UnicodeDecodeError`, triggering the `Stop` return.
-  `splitlines(keepends=True)` preserves original newline characters, ensuring concatenation doesn't drop formatting.

<!-- {-  include="format_error" -} -->
## Logging info, warnings and errors

Import logging.

Import the formatting function with this signature from file `syncspec.utilities.py`:
```python
def format_log_message(message: str, path: Path, line_number: int) -> str:
```

<!-- {--} -->

<!-- {-  include="package" -} -->
## Package

- The function is part of the python package `src/syncspec` .   
- Imports from the package take the form `from syncspec.x import X`.
- Assume Python version 3.9.

<!-- {--} -->

<!-- {-  include="generate_tests" -} -->
## Write pytests to verify the functionality

- Write tests in a separate file.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

<!-- {--} -->

<!-- {-  include="explain_the_solution" -} -->
## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.

<!-- {--} -->
