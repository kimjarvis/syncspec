Import this class from `src/syncspec/parse_into_fragments.py`:

```python
@dataclass
class Fragment:  
    text: str
    name: str     
    open_delimiter: str 
    close_delimiter: str
```

In the file `src/syncspec/fragments_to_blocks.py`:

Define a class:
```python
class BlockManager:
    def __init__(self):
        self.stack: List[str] = []
        self.line: int = 1
```

Define a class:
```python
@dataclass
class Block:  
    prefix_directive: str 
    suffix_directive: str
    text: str
    line: int
    name: str     
    open_delimiter: str 
    close_delimiter: str    
```

Define a class:
```python
@dataclass
class Text:  
    text: str
    line: int
    name: str     
    open_delimiter: str 
    close_delimiter: str
```

Define a unary function with signature:
```python
def fragments_to_blocks(fragment: Fragment) -> Block | Text | None:
```
# Implement the unary function

Encapsulate state in the class `BlockManager`

- Accumulates the number of lines, terminated by`\n`, in the text fragments in field `line`.   
- Record the fragment `text` fields in a stack `stack`.

The each time the function is called:
- Update `BlockManger`

When the length of `stack` is one return:
- A `Text` object:
	- The text shall be the value of `stack[0]`

When the length of `stack` plus one is greater than one and divisible by 4 return a tuple containing:
- A `Block` object. 
	- The prefix_directive shall be the value of `stack[-2]`
	- The suffix_directive shall be the value of `stack[-4]`
	- The text shall be the value of `stack[-3]`
- A `Text` object:
	- The text shall be the value of `stack[-1]`

# Write pytest to verify the functionality 

In the file `tests\test_fragments_to_tracker.py`:

- Import class `Fragment`.
- Verify the cumulative state after all fragments are processed.

- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  
# Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions which are not explicitly stated in the function specification.
