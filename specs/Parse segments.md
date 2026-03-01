# Parse segments

In source parse_segments.py

Import this class from `ensure_balanced_delimiters.py`:
```python
@dataclass
class BalancedDelimitersEnsured:  
    text: str
    open_delimiter: str
    close_delimiter: str    
```

Define a class:
```python
@dataclass
class Segment:  
    text: str # text content between delimiters
    open_delimiter: str # copied 
    close_delimiter: str
```

Define a unary function with signature:
```python
def parse_segments(ensure_balanced_delimiters: EnsureBalancedDelimiters) -> list[Segment]:
```
# Implement the unary function

For example, ensure that this test passes:
```
def test_parse_segments():
    e = EnsureBalancedDelimiters(text="A{{B}}C", open_delimiter="{{", close_delimiter="}}")
    p = [Segment(text="A", open_delimiter="{{", close_delimiter="}}"),
         Segment(text="B", open_delimiter="{{", close_delimiter="}}"),
         Segment(text="C", open_delimiter="{{", close_delimiter="}}")]
    assert(parse_segments(e)==p)
```

Segments are returned in strict left-to-right order of appearance in the source text.
# Safely assume

- Delimiters appear in valid pairs.
- Delimiters are not empty strings.
- Delimiters are distinct, e.g., they will not be `{{` and `{{`.
- Delimiters do not overlap structurally, , e.g., they will not be `{{` and `{`.
- Delimiters are not nested, e.g., input will not contain `{{A{{B}}C}}`.
- Empty strings are preserved.  `{{}} → ["", "", ""]`
- Delimiters may contain regex special characters  e.g., `*`.
- Strings are valid Unicode strings.
# Write pytest to verify the functionality 

In source file `test_parse_segments.py`.

- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  
# Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions which are not explicitly stated in the function specification.