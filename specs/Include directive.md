
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

In the file `src/syncspec/include_directive.py`.

Define a closure factory with a unary function with signature:

<!-- {- source="include_directive_spec" -} -->
```python
def make_include_directive(context: Context):
    def include_directive(directive: Directive) -> Union[Directive,Stop]:

```
<!-- {--} -->
<!-- {- source="include_directive_action" -} -->
## Include Directive

- If the directive contains the key "include":
	- Include the text from the context key value dictionary.
	- Return a new `Directive` object.
<!-- {--} -->
#### Steps

- If dictionary `directive.parameters` contains the key "include" then:
	-  The value shall be called the `key`.
	- If the `key` is already present in the dictionary `context.keyvalue` then:
		-  Call the value `input`
	- Otherwise
		- Log a warning with an informative message:
			- Use the `prefix_line_number`.
		- Return the `Directive` object.  
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
		- Log an error with an informative message:
			- Use the `prefix_line_number`.
		- Return an object of type `Stop`.  
- Otherwise, return the `Directive` object.
#### Note

 - `splitlines(keepends=True)` preserves original newline characters, ensuring concatenation doesn't drop formatting.
 - Logging configuration (handlers, levels) is managed externally.

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
