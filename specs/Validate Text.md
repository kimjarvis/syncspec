# Validate Text 

## Functional specification

Import this class from file `src/syncspec/text.py`:
```python
from dataclasses import dataclass

@dataclass
class Text:
    text: str
    name: str
```

Import this class from file `src/syncspec/validated_text.py`:
```python
from dataclasses import dataclass

@dataclass
class ValidatedText:
    text: str
    name: str
```

Import this class from file `src/syncspec/error.py`:
```python
from dataclasses import dataclass

@dataclass
class Error:
    message: str
    name: str
    line_number: int
```

Import this class from file `src/syncspec/validate_text_context.py`:
```python
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class ValidateTextContext:
    open_delimiter: str
    close_delimiter: str
    line_number: int    
```

Do not generate code to initialise the context.
### Implement the unary function Validate Text

In the file `src/syncspec/validate_text.py`.

Define a closure factory with a unary function with signature:

```python
def make_validate_text(context: ValidateTextContext):
    def validate_text(text: Text) -> Union[ValidatedText, Error]:
```

### Ensure that

### Verify the context

#### Ensure that:

- Delimiters are valid Unicode strings.
- Delimiters are not empty strings.
- Delimiters are distinct, e.g., they will not be `{{` and `{{`.
- Delimiters do not overlap structurally, , e.g., they will not be `{{` and `{`. 
#### Assume that:

- The context is instantiated before the factory is called.
- Delimiters may contain regex special characters  e.g., `*`.  Delimiters are treated as literal strings using `str.find` rather than compiled regex patterns.
- The text has POSIX line endings  e.t.,`\n`.

### Keep track of line numbers

- Field "line_number" keeps track of line numbers within text.
- Line numbers are 1-based.  The initial value of ValidateTextContext.line_number is 1.
- The line number reported when class Error is returned is the line number where the error was detected. 
- The line number is part of the context shared across multiple calls.
- The line number acts as a global offset. 
- "line_number" is based on total newlines in the input even when returning an Error.
### Verify the text

#### Ensure that:

- text is a valid Unicode string.
- Delimiters only appear in balanced pairs. e.g., input may contain `{{A}}B{{C}}`.
- The open delimiter appears before any close delimiters in the text.
	- So, the last delimiter appearing in the text is the close delimiter.
- Delimiters are not nested, e.g., ensure that input  does not contain `{{A{{B}}C}}`.
- Ensure that the number of pairs of balanced delimiters is even.  e.g.,
	- One pair `A{{B}}C` is not valid.  
	- Two pairs `A{{B}}C{{D}}E` is valid.  
	- Three pairs `A{{B}}C{{D}}E{{F}}G` are not valid.

### Note that

Requiring an even number of delimiter pairs is a specific requirement for this application.
### Error return

Raise a ValueError during factory creation for configuration errors.

Return Error objects for text validation failures.  When any of the validation conditions are violated return object of type Error with an informative message, a copy of the `Text.name` and the line number on which the error was detected.
### Successful return

Return a `ValidatedText` object.  Copy the `Text.text` field to `ValidatedText.text`.
## Package

`src/syncspec` is a Python package.   Imports take the form `from src.syncspec.x import X`.
## Test the unary function  

In the file `tests/test_validate_text.py`.

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.
