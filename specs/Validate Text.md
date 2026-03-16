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

Import logging.
Import the function with this signature from file `src/syncspec/utilities.py`:
```python
def format_error(message: str, name: str, line_number: int) -> str:
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
    def validate_text(text: Text) -> Union[ValidatedText, None]:
```


### Verify the context

#### Ensure that:

- Delimiters are valid Unicode strings.
- Delimiters are not empty strings.
- Delimiters are distinct, e.g., they will not be `{{` and `{{`.
- Delimiters do not overlap structurally, , e.g., they will not be `{{` and `{`. 
- Delimiters do not contain newlines.
#### Assume that:

- The context is instantiated before the factory is called.
- Delimiters may contain regex special characters  e.g., `*`.  Delimiters are treated as literal strings using `str.find` rather than compiled regex patterns.
- The text has POSIX line endings  e.t.,`\n`.

### Keep track of line numbers

- Field `line_number` keeps track of line numbers within text.
- Line numbers are 1-based.  The initial value of `ValidateTextContext.line_number` is 1.
- Empty text increments line_number by 1 (represents one logical line).
- The line number reported when an error is logged is the line number where the error was detected.  
- Line Splitting: splitlines(keepends=True) is used to define "lines". This preserves newline characters during slicing and reconstruction.
### Verify the text

#### Ensure that:

- text is a valid Unicode string.
- Delimiters only appear in balanced pairs. e.g., input may contain `{{A}}B{{C}}`.
- The open delimiter appears before any close delimiters in the text.
	- So, the last delimiter appearing in the text is the close delimiter.
- Delimiters are not nested, e.g., ensure that input  does not contain `{{A{{B}}C}}`.
- Ensure that the number of pairs of balanced delimiters is even.  e.g.,
	- Zero pairs `A` is valid.
	- One pair `A{{B}}C` is not valid.  
	- Two pairs `A{{B}}C{{D}}E` is valid.  
	- Three pairs `A{{B}}C{{D}}E{{F}}G` are not valid.

### Note that

Requiring an even number of delimiter pairs is a specific requirement for this application

### Errors

Raise a Value Error during factory creation for configuration errors.

When any of the validation conditions are violated:
- return None.
- call `format_error` to format an error messages.  Pass an informative message,   `Text.name` and the line number on which the error was detected.  Use python logging to log the error.

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
