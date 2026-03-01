Import this class from file `src/syncspec/error.py`:
```python
@dataclass
class Error:  
    message: str
    name: str
    line: int
```

In the file `src/syncspec/encode_parameters.py`:

Define a class:
```python
@dataclass
class EncodedParameters:  
    text: str
    name: str
    open_delimiter: str
    close_delimiter: str
```

Define a function with signature:
```python
def encode_parameters(text: str, name: str, open_delimiter: str, close_delimiter: str) -> EncodedParameters | Error:
```
# Implement the unary function

Default parameters are `open_delimiter="{{"` and `close_delimiter="}}"` and `name=""`.
# Ensure that

- Delimiters are not empty strings.
- Delimiters are distinct, e.g., they will not be `{{` and `{{`.
- Delimiters do not overlap structurally, , e.g., they will not be `{{` and `{`.

When any of these conditions are violated return object of type Error with an informative message, a copy of the name and set the line number on which the error was detected to 1.

Otherwise, construct the return object using the parameters.
# Assume that

- Delimiters may contain regex special characters  e.g., `*`.
- Strings are valid Unicode strings.
- The text has POSIX line endings  e.t.,`\n`.
# Write pytest to verify the functionality 

In the file `tests/test_encode_parameters.py`:

- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  
# Explain the solution  
  
- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions which are not explicitly stated in the function specification.




