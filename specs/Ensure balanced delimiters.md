In source ensure_balanced_delimiters.py

Import this class from `encode_parameters.py`:

```python
@dataclass
class EncodeParameters:  
    data: str = ""
    open_delimiter: str = "{{"
    close_delimiter: str ="}}"
```

Import this class from `error.py`:

```python
@dataclass
class Error:  
    message: str = ""
```

Define a class:

```python
@dataclass
class BalancedDelimitersEnsured:  
    text: str 
    open_delimiter: str # copied 
    close_delimiter: str
```

Define a unary function with signature:

```python
def ensure_balanced_delimiters(encode_parameters: EncodeParameters) -> BalancedDelimitersEnsured | Error:
```

Action:

Check these conditions in order of precedence and raise an value error with message.
- Check that the delimiters in the string target are not nested.  Message "Delimiters are nested".
- Check if the delimiters in the string target are balanced.  Message "Delimiters are not matched".
Catch value errors in the function and return an Error object with the message.

When there is no error return an object of class `EnsureBalancedDelimiters` that is a copy of the `EncodeParameters` object.

# Safely assume

- Delimiters appear in valid pairs.
- Delimiters are not empty strings.
- Delimiters are distinct, e.g., they will not be `{{` and `{{`.
- Delimiters do not overlap structurally, , e.g., they will not be `{{` and `{`.
- Delimiters may contain regex special characters  e.g., `*`.
- Strings are valid Unicode strings.
# Write pytest to verify the functionality 

In source file `test_parse_segments.py`.

- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  
# Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions which are not explicitly stated in the function specification.


Reference:

This function implements similar functionality:

```python
def ensure_balanced_delimiters(string: str, open_delimiter: str = "{{", close_delimiter: str = "}}") -> None:
    open_len = len(open_delimiter)
    close_len = len(close_delimiter)

    i = 0
    found_open = False

    while i < len(string):
        # Check for opening delimiters
        if string[i:i + open_len] == open_delimiter:
            if found_open:
                raise ValueError("Parentheses cannot be nested")
            found_open = True
            i += open_len

        # Check for closing delimiters
        elif string[i:i + close_len] == close_delimiter:
            if not found_open:
                raise ValueError("Parentheses are not matched")
            found_open = False
            i += close_len
        else:
            i += 1

    # Check if there's an unclosed opening parenthesis
    if found_open:
        raise ValueError("Parentheses are not matched")
```





