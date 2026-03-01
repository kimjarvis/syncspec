Import this class from `src/syncspec/encode_parameters.py`:
```python
@dataclass
class EncodedParameters:  
    text: str
    name: str    
    open_delimiter: str
    close_delimiter: str
```

Import this class from `src/syncspec/error.py`:
```python
@dataclass
class Error:  
    message: str
    name: str
    line: int
```

In the file `src/syncspec/ensure_balanced_delimiters.py`:

Define a class:
```python
@dataclass
class BalancedDelimitersEnsured:  
    text: str
    name: str     
    open_delimiter: str 
    close_delimiter: str
```

Define a unary function with signature:
```python
def ensure_balanced_delimiters(encoded_parameters: EncodedParameters) -> BalancedDelimitersEnsured | Error:
```
# Implement the unary function

# Ensure that

- Delimiters only appear in balanced pairs. e.g., input may contain `{{A}}B{{C}}`.
- The open delimiter appears before any close delimiters in the text.
- Delimiters are not nested, e.g., ensure that input  does not contain `{{A{{B}}C}}`.

When any of these conditions are violated return object of type Error with an informative message, a copy of the name and the line number on which the error was detected.

-  Line numbers are 1-based.
- If an open delimiter is never closed, the error line corresponds to the line where the open delimiter started.

Otherwise, copy the fields of the parameter object into the returned object.
# Assume that

- Delimiters are not empty strings.
- Delimiters are distinct, e.g., they will not be `{{` and `{{`.
- Delimiters do not overlap structurally, , e.g., they will not be `{{` and `{`. 
- Delimiters may contain regex special characters  e.g., `*`.
- Strings are valid Unicode strings.
- The text has POSIX line endings  e.t.,`\n`.
# Write pytest to verify the functionality 

In the file `tests/test_ensure_balanced_delimiters.py`:

- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  
# Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions which are not explicitly stated in the function specification.

