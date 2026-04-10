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
<!-- {- import="../src/syncspec/text.py",  head=2,  tail=2 -} -->
```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Text:
    path: Path
    text: str
    line_number: int
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

In the file `src/syncspec/write_keyfile.py`.

Define a closure factory with a unary function with signature:

<!-- {- source="write_keyfile_spec" -} -->
```python
def make_write_keyfile(context: Context):
	state = {'last': False}
    def write_keyfile(text: Text) -> Union[Text, Stop]:
```
<!-- {--} -->

<!-- {- source="write_keyfile_action" -} -->
## Write keyfile

Write the `keyvalue` dictionary to the `keyvalue_file` JSON file.
<!-- {--} -->
#### Note

`state["last"]` is set outside this function.  
#### Steps

- If `state["last"]==True` and `keyvalue_file` JSON file is specified:
	- Write the `keyvalue` file to the file.  Overwrite the file if it exists.
	- When conversion fails:
		- Log an error with an informative message:
			- Use `line_number` zero.
		- Return an object of type `Stop`.  
	- Otherwise, Return the parameter text object.
- Otherwise, Return the parameter text object.

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
