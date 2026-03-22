# Combine Strings 

## Functional specification


<!-- {="import": "src/syncspec/parameter_string.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass

@dataclass
class String:
    text: str
    line_number: int
    name: str
```
<!-- {==} -->

<!-- {="import": "src/syncspec/combine_strings_context.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class CombineStringsContext:
    text: str

```
<!-- {==} -->

Do not generate code to initialise the context.
### Implement a unary function

In the file `src/syncspec/combine_strings.py`.

Define a closure factory with a unary function with signature:

<!-- {="source": "signature:combine_strings", "head": 2, "tail": 2=} -->
```python
def make_combine_strings(context: CombineStringsContext):	
	def combine_strings(string: String) -> None

```
<!-- {==} -->

 - Append `String.text` to the end of string `CombineStringsContext.text`.

<!-- {= "include": "package", "head": 1, "tail": 1 =} -->
## Package

- The function is part of the python package `src/syncspec` .   
- Imports from the package take the form `from src.syncspec.x import X`.
- Assume Python version 3.7.

<!-- {==} -->

## Test the unary function  

In the file `tests/test_combine_strings.py`.

<!-- {= "include": "generate_tests", "head": 1, "tail": 1 =} -->

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

<!-- {==} -->

<!-- {= "include": "explain_the_solution", "head": 1, "tail": 1 =} -->
## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.

<!-- {==} -->
