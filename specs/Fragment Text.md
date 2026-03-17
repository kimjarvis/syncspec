# Fragment Text 

## Functional specification


<!-- {="import": "src/syncspec/validated_text.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass

@dataclass
class ValidatedText:
    text: str
    name: str
```
<!-- {==} -->


<!-- {="import": "src/syncspec/fragment.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass

@dataclass
class Fragment:
    text: str
    line_number: int
    name: str
```
<!-- {==} -->


<!-- {="import": "src/syncspec/fragment_text_context.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class FragmentTextContext:
    open_delimiter: str
    close_delimiter: str
    line_number: int
```
<!-- {==} -->

Do not generate code to initialise the context.
### Implement a unary function

In the file `src/syncspec/fragment_text.py`.

Define a closure factory with a unary function with signature:

```python
def make_fragment_text(context: FragmentTextContext):
    def fragment_text(text: ValidatedText) -> List[Fragment]:
```

- Parse the text using the delimiters and return a list of Fragment objects.
- Fragments are returned in strict left-to-right order of appearance in the source text.
- Fragments may contain empty text strings when delimiters are adjacent.
- Delimiters are treated as separators and are not included in the `Fragment.text` content.

In these examples the delimiters are `{{` and `}}`:

```python
fragment_text(ValidatedText(name="freddy",text="""A{{B}}C{{D}}EF""")) ==
[Fragment(text="A",name="freddy",line_number=1),
Fragment(text="B",name="freddy",line_number=1),
Fragment(text="C",name="freddy",line_number=1),
Fragment(text="D",name="freddy",line_number=1),
Fragment(text="EF",name="freddy",line_number=1)]
```


- text `"{{}}"` produces a list of three fragments each with `text=""`
- text `"{{A}}"` produces a list of three fragments, the middle one has `text="A"`
- text `"{{}}A"` produces a list of three fragments, the last one has `text="A"`
### Keep track of line numbers

- Field "line_number" keeps track of line numbers within text.
- Line numbers are 1-based.  The initial value of `FragmentTextContext.line_number` is 1.
- The line number is part of the context shared across multiple calls.
- The line number acts as a global offset. 
- Multi-line fragments should report the start line

Copy `ValidatedText.name` into the Fragment
### Assume that

- Delimiters only appear in balanced pairs. e.g., input may contain `{{A}}B{{C}}`.
- The open delimiter appears before any close delimiters in the text.
- Delimiters are not nested, e.g., input will not contain `{{A{{B}}C}}`.
- Delimiters are not empty strings.
- Delimiters are distinct, e.g., they will not be `{{` and `{{`.
- Delimiters do not overlap structurally, , e.g., they will not be `{{` and `{`.
- Delimiters do not contain newlines
- Delimiters may contain regex special characters  e.g., `*`.
- Strings are valid Unicode strings.
- The text has POSIX line endings  e.t.,`\n`.

<!-- {= "include": "package", "head": 1, "tail": 1 =} -->
## Package

- The function is part of the python package `src/syncspec` .   
- Imports take the form `from src.syncspec.x import X`.
- Assume Python version 3.10.

<!-- {==} -->
## Test the unary function  

In the file `tests/test_fragment_text.py`.

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
