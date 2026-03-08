# Fragment Text 

## Functional specification

Import this class from file `src/syncspec/validated_text.py`:
```python
from dataclasses import dataclass

@dataclass
class ValidatedText:
    text: str
```

Import this class from file `src/syncspec/fragment.py`:
```python
from dataclasses import dataclass

@dataclass
class Fragment:  
    text: str
    line_number: int
```


Import this class from file `src/syncspec/fragment_text_context.py`:
```python
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class FragmentTextContext:
    name: str
    open_delimiter: str
    close_delimiter: str
    line_number: int    
```

### Implement the unary function Fragment Text

In the file `src/syncspec/fragment_text.py`.

Define a closure factory with a unary function with signature:

```python
def make_fragment_text(context: FragmentTextContext):
    def fragment_text(text: ValidatedText) -> List[Fragment]:
```

- Parse the text using the delimiters and return a list of Fragment objects.
- Fragments are returned in strict left-to-right order of appearance in the source text.
- Fragments may contain empty text strings when delimiters are adjacent.
- Delimiters are treated as separators and are not included in the Fragment.text content.

```python
fragment_text(ValidatedText(text="""A{{B}}C{{D}}EF""")) ==
[Fragment(text="A",line_number=1),
Fragment(text="B",line_number=1),
Fragment(text="C",line_number=1),
Fragment(text="D",line_number=1),
Fragment(text="EF",line_number=1)]
```

### Keep track of line numbers

- Field "line_number" keeps track of line numbers within text.
- Line numbers are 1-based.  The initial value of `FragmentTextContext.line_number` is 1.
- The line number is part of the context shared across multiple calls.
- The line number acts as a global offset. 
- Multi-line fragments should report the start line
### Assume that

- Delimiters only appear in balanced pairs. e.g., input may contain `{{A}}B{{C}}`.
- The open delimiter appears before any close delimiters in the text.
- Delimiters are not nested, e.g., input will not contain `{{A{{B}}C}}`.
- Delimiters are not empty strings.
- Delimiters are distinct, e.g., they will not be `{{` and `{{`.
- Delimiters do not overlap structurally, , e.g., they will not be `{{` and `{`.
- Delimiters may contain regex special characters  e.g., `*`.
- Strings are valid Unicode strings.
- The text has POSIX line endings  e.t.,`\n`.
## Package

`src/syncspec` is a Python package.   Imports take the form `from src.syncspec.x import X`.
## Test the unary function  

In the file `tests/test_fragment_text.py`.

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.
## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.
