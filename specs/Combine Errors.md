# Combine Errors 

## Functional specification

Import this class from file `src/syncspec/error.py`:
```python
from dataclasses import dataclass

@dataclass
class Error:
    message: str
    name: str
    line_number: int
```

Import this class from file `src/syncspec/combine_errors_context.py`:
```python
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class CombineErrorsContext:
	text: str
```

Do not generate code to initialise the context.
### Implement the unary function Combine Errors

In the file `src/syncspec/combine_errors.py`.

Define a closure factory with a unary function with signature:

```python
def make_combine_errors(context: CombineErrorsContext):	
	def combine_errors(error: Error) -> None
```

Format the a multi-line message using values from `error`

```
Error: message
Line: line_number
File: name

```

 - Append the message to the end of string `CombineErrorsContext.text`.
## Package

`src/syncspec` is a Python package.   Imports take the form `from src.syncspec.x import X`.
## Test the unary function  

In the file `tests/test_combine_errors.py`.

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.
