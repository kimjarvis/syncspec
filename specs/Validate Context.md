## Imports 

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

<!-- {- export="../src/syncspec/dummy.py",  head=2,  tail=2 -} -->
```python
from dataclasses import dataclass

@dataclass
class Dummy:
    pass
```
<!-- {--} -->

<!-- {- source="../src/syncspec/stop.py",  head=2,  tail=2 -} -->
```python
from dataclasses import dataclass

@dataclass
class Stop:
    pass
```
<!-- {--} -->

## Implement a unary function

In the file `src/syncspec/validate_context.py`.

Define a closure factory with a unary function with signature:

<!-- {- source="validate_context_spec" -} -->
```python
def make_validate_context(context: Context):
    def validate_context(fact: Dummy) -> Union[Dummy, Stop]:
```
<!-- {--} -->

<!-- {- source="validate_context_action" -} -->
## Validate Context

- Set up Python logging
- Validate the delimiters
- Read JSON file
- Verify the ignore_rules file
- Return an object of type `Dummy`
<!-- {--} -->
### Set up Python logging:

#### Action:
Initialise python logging.
#### Steps:
- If `log_file` is specified log to this file.  Otherwise, log to the console.
- Use basic configuration with format `"%(levelname)s - %(message)s"`.  
- Set the log level to INFO.

Clear any existing handlers, ensuring `basicConfig()` will create a new file handler when --`log_file` is specified.   Write an initial log info message "Syncspec started ", followed by the `path`,  to guarantee the log file is created and written.
### Validate the delimiters

#### Action:
Validate the delimiters.
#### Steps:
Verify that:
<!-- {- source="delimiter assumptions"-} -->
- Delimiters are not empty strings.
- Delimiters are distinct, e.g., they will not be `{{` and `{{`.
- Delimiters do not overlap structurally.  Open cannot be a sub-string of close and vice versa. e.g., they will not be `{{` and `{`. 
- Delimiters do not contain newlines.
<!-- {--} -->

If verification fails:
- Log an error with an informative message using `format_log_message`.
- Return an object of type `Stop`.  
### Read JSON file

#### Action:
Read the `keyvalue_file` into a dictionary.
#### Steps:
- If the `keyvalue_file`  is specified:
	- Read the JSON file  `keyvalue_file`  into a dictionary `keyvalue`.  
	- If JSON validation fails: 
		- Log an error with an informative message:
			- Use `line_number` zero.
		- Return an object of type `Stop`.  
- Otherwise:
	- Set `keyvalue` to an empty dictionary.
### Verify the ignore_rules file

#### Action
The `ignore_rules_file` contains a list of patterns to ignore in `gitignore` format.   If not specified, `.syncspec_ignore` may be used instead.  Verify that the file is in the correct format.
#### Steps:
- If the `context.ignore_rules_file` path does not point to a file:
	- If `.syncspec_ignore`  is a file:
		- set the `contex.ignore_rules_file` to point to this file.
- If `context.ignore_rules_file` points to a file:
	- Load and compile the ignore patterns from the file.
	- If compilation fails:
		- Log an error with an informative message:
			- Use `line_number` zero.
		- Return an object of type `Stop`.  
- Otherwise
	- Ignore nothing.
#### Use:
- The `PathSpec` module.
- The `GitWildMatchPattern` for the `.gitignore` syntax.
#### Assume that:
- The PathSpec module is available.

<!-- {-  source="format_error" -} -->
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
