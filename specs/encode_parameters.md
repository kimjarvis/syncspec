In source `encode_parameters.py`.

Define a function with signature:

```python
def encode_parameters(data: str, open_delimiter: str, close_delimiter: str) -> EncodeParameters | Error:
```

Action:

Return an object instantiated from the parameter values or an Error object.

Define a class:

```python
@dataclass
class EncodeParameters:  
    data: str = ""
    open_delimiter: str = "{{"
    close_delimiter: str ="}}"
```

In method `__post_init__`  ensure that:
1. open and close delimiters are not empty strings.  Message: "Empty delimiter"  
2. open and close delimiters are not equal.  Message: "Equal delimiters"
Check these conditions in order of precedence and raise an value error with message.

Catch value errors in the function and return an Error object with the message.

Import this class from `error.py`:

```python
@dataclass
class Error:  
    message: str = ""
```
# Write pytest to verify the functionality 
  
In source file `test_encode_parameters.py`.

- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  
  
# Explain the solution  
  
- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions which are not explicitly stated in the function specification.




