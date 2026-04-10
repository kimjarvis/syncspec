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

## Implement a unary function

In the file `src/syncspec/defragment_text.py`.

Define a closure factory with a unary function with signature:

<!-- {- source="defragment_text_spec" -} -->
```python
def make_defragment_text(context: Context):
	state = {'path': None, 'text': "", 'last': False }
    def defragment_text(text: Text) -> Text:

```
<!-- {--} -->

<!-- {- source="defragment_text_action" -} -->
## Defragment Text

Concatenate text fragments from the same file and write them to the file.

<!-- {--} -->
#### Description

- Each Text object contains a chunk of text `text.text` that must be written to the file `text.path`.
- Multiple chunks may be written to the same file.
- The caller guarantees `Text` objects arrive grouped by path, so the algorithm can rely on contiguous chunks per file.
- Text can be accumulated by concatenating them in `state['text']` .
- Flush when paths change.  That is, `text.path != state['path']`.   
- Flush when `state['last']` is True, this is the last call to the function, so write the accumulated text and the current text to file.
- Return the parameter text object.

Assume that:
- `state['last']` is mutated outside this function.
- `text.path` represents a valid absolute file path.
- File overwrites are intended; no append or conflict-resolution logic is needed.

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
