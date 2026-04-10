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

In the file `src/syncspec/source_directive.py`.

Define a closure factory with a unary function with signature:

<!-- {- source="source_directive_spec" -} -->
```python
def make_source_directive(context: Context):
    def source_directive(directive: Directive) -> Union[Directive,Stop]:

```
<!-- {--} -->

<!-- {- source="source_directive_action" -} -->
## Source Directive

- If the directive contains the key "source":
	- Add the source to the context key value dictionary.
	- Return `Directive` object.
<!-- {--} -->

#### Steps

- If dictionary `directive.parameters` contains the key "source" then:
	- The value shall be called the `key`.
	<!-- {- source="source_directive_processing" -} -->
	- If dictionary `directive.parameters` contains the key "head" then:
		- Ensure that:
			- The value is an integer call it `head`.
	- Otherwise, `head=1`
	- If dictionary `directive.parameters` contains the key "tail" then:
		- Ensure that:
			- The value is an integer call it `tail`.
	- Otherwise, `tail=1`
	- Ensure that `head + tail` lines could be removed from `Directive.text`, an result is allowed.
	- Copy `Directive.text` to variable `output`
	- Ensure that:
		-  `head + tail <=`  the number of lines in variable `output` .
	- Trim the first `head` lines and the last `tail` lines from variable  `output` .
	- If the first character of `output` is and end of line character `\n`:
		- Remove the first character of `output`.
	- If the last character of `output` is not an end of line character `\n` then:
		- Add a end of line to the end of `output`.
	<!-- {--} -->
	- Add the `key` to the `context.keyvalue` dictionary with value equal to the variable `output`.
	- If the `key` is already present in the dictionary then:
		- Log an error with an informative message.
			- Use the `prefix_line_number`.
		- Return an object of type `Stop` . 
	- Return the `Directive` object.
	- When any of the ensured conditions are violated:
		- Log an error with an informative message:
			- Use the `prefix_line_number`.
		- Return an object of type `Stop` . 
- Otherwise, return the `Directive` object.

Assume that:

- `splitlines(keepends=True)` preserves original newline characters, ensuring concatenation doesn't drop formatting.
- `context.keyvalue` is a standard mutable dictionary.

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
