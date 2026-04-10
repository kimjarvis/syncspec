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
<!-- {- import="../src/syncspec/block.py", head=2, tail=2 -} -->
```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Block:
    prefix: str
    text: str
    suffix: str
    path: Path
    prefix_line_number: int
    text_line_number: int
    suffix_line_number: int
```
<!-- {--} -->
<!-- {- export="../src/syncspec/directive.py",  head=2,  tail=2  -} -->
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

In the file `src/syncspec/create_directives.py`.

Define a closure factory with a unary function with signature:

<!-- {- source="create_directives_spec" -} -->
```python
def make_create_directives(context: Context):
    def create_directives(block: Block) -> Union[Directive,Stop]:

```
<!-- {--} -->

<!-- {- source="create_directives_action" -} -->
## Create Directives

1. Create an object of type `Directive` by coping the fields of `block`.
2. Populate the field `parmeters` dictionary using `string_to_keyvalue_dict(block.prefix)`.
3. Return the object.
<!-- {--} -->
### Implement function string_to_keyvalue_dict

- The string field `block.prefix` contains key value pairs in python code format.
- Use `ast.literal_eval` for safe type conversion and a regex to extract key=value pairs.
- Strip the string to discard trailing space or punctuation before conversion.

Use this code as a guideline for the conversion:

<!-- {- import="../src/syncspec/parse_params.py",  head=2,  tail=2 -} -->
```python
import ast
import re


def parse_params(param_str: str) -> dict:
    params = {}
    # Matches: key="quoted", key=123, key=True
    pattern = re.compile(r'(\w+)\s*=\s*("(?:[^"\\]|\\.)*"|[^,]+)')

    for m in pattern.finditer(param_str):
        key, raw_val = m.group(1), m.group(2).strip()
        try:
            params[key] = ast.literal_eval(raw_val)
        except (ValueError, SyntaxError):
            params[key] = raw_val  # Fallback to raw string
    return params


# Example
s = 'import="../src/syncspec/context.py", head=2, eol=True'
print(parse_params(s))
# {'import': 'src/syncspec/context.py', 'head': 2, 'eol': True}
```
<!-- {--} -->

If a syntax error occurs 
- Log an error with an informative message:
	- Use the `prefix_line_number`.
- Return an object of type `Stop`.  

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
