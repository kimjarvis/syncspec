# Combine Strings 

## Functional specification

Import this class from file `src/syncspec/string.py`:
```python
from dataclasses import dataclass

@dataclass
class String:
    text: str
    line_number: int    
```

Import this class from file `src/syncspec/combine_strings_context.py`:
```python
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class CombineStringsContext:
	text: str
```

Do not generate code to initialise the context.
### Implement the unary function Combine Strings

In the file `src/syncspec/combine_strings.py`.

Define a closure factory with a unary function with signature:

```python
def make_combine_strings(context: CombineStringsContext):	
	def combine_strings(string: String) -> None
```

 - Append `String.text` to the end of string `CombineStringsContext.text`.
## Test the unary function  

In the file `tests/test_combine_strings.py`.

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.
