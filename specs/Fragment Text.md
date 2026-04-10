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
<!-- {- export="../src/syncspec/fragment.py",  head=2,  tail=2 -} -->
```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Fragment:
    path: Path
    text: str
    line_number: int
```
<!-- {--} -->
<!-- {- import="../src/syncspec/file_path.py",  head=2,  tail=2 -} -->
```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class FilePath:
    path: Path
    text: str
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

In the file `src/syncspec/fragment_text.py`.

Define a closure factory with a unary function with signature:

<!-- {- source="fragment_text_spec" -} -->
```python
def make_fragment_text(context: Context):
    def fragment_text(fact: FilePath) -> Union[List[Fragment],Stop]:
```
<!-- {--} -->

<!-- {- source="fragment_text_action" -} -->
## Fragment Text

- Determine whether file is a target
- Decompose text into fragments using the delimiters.  
- Keep track of line numbers.
- Ensure delimiter semantics.
<!-- {--} -->

### Decompose text into fragments
#### Description

- Parse the text using the delimiters and return a list of `Fragment` objects.
- Fragments are returned in strict left-to-right order of appearance in the source text.
- Fragments may contain empty text strings when delimiters are adjacent.
- Delimiters are treated as separators and are not included in the `Fragment.text` content.
#### Example

In this examples the delimiters are `{{` and `}}`.  Note that not all of the fields are shown.

```python
fragment_text(FilePath(text="""A{{B}}C
{{D}}EF""")) ==
[Fragment(text="A",line_number=1),
Fragment(text="B",line_number=1),
Fragment(text="C",line_number=1),
Fragment(text="D",line_number=2),
Fragment(text="EF",line_number=2)]
```

- text `"{{}}"` produces a list of three fragments each with `text=""`
- text `"{{A}}"` produces a list of three fragments, the middle one has `text="A"`
- text `"{{}}A"` produces a list of three fragments, the last one has `text="A"`

`Fragment.path = FilePath.path`
### Ensure semantics

#### steps

- Verify that:
	- The first delimiter is the open delimiter.
	- Open and close delimiters are matched.  
	- Delimiters are not nested. 
	- `text != ""`
- If verification fails:
	- Log an error with an informative message:
		- Use the `line_number`.
	- Return an object of type `Stop`.  
	- Do not attempt to recover or parse further.
- If verification succeeds:
	- Return a list of Fragment objects.
#### Assume

<!-- {- include="delimiter assumptions"-} -->
- Delimiters are not empty strings.
- Delimiters are distinct, e.g., they will not be `{{` and `{{`.
- Delimiters do not overlap structurally.  Open cannot be a sub-string of close and vice versa. e.g., they will not be `{{` and `{`. 
- Delimiters do not contain newlines.
 <!-- {--} -->

<!-- {- source="line_numbers",  head=2,  tail=2 -} -->
### Keep track of line numbers

- Field "line_number" keeps track of line numbers within text.
- Line numbers are 1-based.  
- The line number acts as a global offset. 
- The line number of a Multi-line fragment is the line number of the first line.

<!-- {--} -->

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
