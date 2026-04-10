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

In the file `src/syncspec/reassemble_text.py`.

Define a closure factory with a unary function with signature:

<!-- {- source="reassemble_text_spec" -} -->
```python
def make_reassemble_text(context: Context):
    def reassemble_text(directive: Directive) -> Text:
```
<!-- {--} -->

<!-- {- source="reassemble_text_action" -} -->
## Reassemble Text

Convert a Directive object into a Text object.
<!-- {--} -->
#### Steps

- Create a Text object:
	- Copy `line_number` from `Directive.prefix_line_number`
	- Copy `path`  from `Directive.path`
	- Concatenate these strings in order to create `text`:  
		1. `Context.open_delimiter`  
		2. `directive.prefix`  
		3. `Context.close_delimiter`  
		4. `directive.text`  
		5. `Context.open_delimiter`  
		6. `directive.suffix`  
		7. `Context.close_delimiter`
	- Return the object

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
