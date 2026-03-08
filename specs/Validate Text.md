# Validate Text 

## Functional specification

Import this class from file `src/syncspec/text.py`:
```python
from dataclasses import dataclass

@dataclass
class Text:
    text: str
```

Import this class from file `src/syncspec/validated_text.py`:
```python
from dataclasses import dataclass

@dataclass
class ValidatedText:
    text: str
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

Class Monad preserves state between function calls in a dictionary.

Import this class from file `src/syncspec/monad.py`:
```python
from dataclasses import dataclass
from typing import ClassVar, Dict, Any

@dataclass
class Monad:
    state: ClassVar[Dict[str, Dict[str, Any]]] = {}
```

Monad is initialised with values.  For example:
```python
    Monad.state["open_delimiter"] = "{{"
    Monad.state["close_delimiter"] = "}}"
    Monad.state["name"] = "test"
    Monad.state["length"]
    Monad.state["index"]
```
- When  `Monad.state["index"] == 0` we call this the first function call.
- When  `Monad.state["index"] + 1 == Monad.state["length"]` we call this the last function call.

### Implement the unary function Validate Text

In the file `src/syncspec/validate_text.py`.

Define a unary function with signature:

```python
def validate_text(text: Text) -> ValidatedText | Error:
```

### Ensure that

### Verify the monad

#### Ensure that:

- Delimiters are valid Unicode strings.
- Delimiters are not empty strings.
- Delimiters are distinct, e.g., they will not be `{{` and `{{`.
- Delimiters do not overlap structurally, , e.g., they will not be `{{` and `{`. 
- Monad.state["index"] < Monad.state["length"]
- 0 <= Monad.state["index"]
#### Assume that:

- Delimiters may contain regex special characters  e.g., `*`.
- The text has POSIX line endings  e.t.,`\n`.
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
### Error return

When any of the conditions are violated return object of type Error with an informative message, a copy of the name and the line number on which the error was detected.
### Successful return

Return ValidatedText object.  Copy the Text.text field to ValidatedText.text.
#### Assume that:

- Line numbers are 1-based.
- If an open delimiter is never closed, the error line corresponds to the line where the open delimiter started.
## Test the unary function  

In the file `tests/test_validate_text.py`.

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.
