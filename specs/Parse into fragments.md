Import this class from `src/syncspec/ensure_balanced_delimiters.py`:
```python
@dataclass
class BalancedDelimitersEnsured:  
    text: str
    name: str
    open_delimiter: str
    close_delimiter: str    
```

In the file `src/syncspec/parse_into_fragments.py`:

Define a class:
```python
@dataclass
class Fragment:  
    text: str
    name: str     
    open_delimiter: str 
    close_delimiter: str
```

Define a unary function with signature:
```python
def parse_into_fragments(ensure_balanced_delimiters: BalancedDelimitersEnsured) -> list[Fragment] | Error:
```
# Implement the unary function

For example, ensure that this test passes:
```
def test_parse_fragments():
    e = EnsureBalancedDelimiters(text="A{{B}}C", open_delimiter="{{", close_delimiter="}}")
    p = [Fragment(text="A", open_delimiter="{{", close_delimiter="}}"),
         Fragment(text="B", open_delimiter="{{", close_delimiter="}}"),
         Fragment(text="C", open_delimiter="{{", close_delimiter="}}")]
    assert(parse_Fragments(e)==p)
```

Fragments are returned in strict left-to-right order of appearance in the source text.
# Assume that

- Delimiters only appear in balanced pairs. e.g., input may contain `{{A}}B{{C}}`.
- The open delimiter appears before any close delimiters in the text.
- Delimiters are not nested, e.g., input will not contain `{{A{{B}}C}}`.
- Delimiters are not empty strings.
- Delimiters are distinct, e.g., they will not be `{{` and `{{`.
- Delimiters do not overlap structurally, , e.g., they will not be `{{` and `{`.
- Delimiters may contain regex special characters  e.g., `*`.
- Strings are valid Unicode strings.
- The text has POSIX line endings  e.t.,`\n`.
# Write pytest to verify the functionality 

In the file `tests\test_parse_into_fragments.py`:

- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  
# Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions which are not explicitly stated in the function specification.