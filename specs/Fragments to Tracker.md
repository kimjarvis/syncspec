Import this class from `src/syncspec/parse_into_fragments.py`:

```python
@dataclass
class Fragment:  
    text: str
    name: str     
    open_delimiter: str 
    close_delimiter: str
```

In the file `src/syncspec/fragments_to_tracker.py`:

Define a class:
```python
@dataclass
class Tracker:  
	stack: list[str]
	index: int
    name: str     
    open_delimiter: str 
    close_delimiter: str
    line: int
```

Define a class:
```python
@dataclass
class Block:  
    prefix_directive: str 
    suffix_directive: str
    text: str
    name: str     
    line: int
    open_delimiter: str 
    close_delimiter: str    
```

Define a class:
```python
@dataclass
class Text:  
    text: str
    name: str     
    line: int
    open_delimiter: str 
    close_delimiter: str
```

Define a unary function with signature:
```python
def fragments_to_tracker(fragment: Fragment) -> Block:
```
# Implement the unary function

Encapsulate state in a  class `TrackerManager`

- Count how many times the function has been called in field `index`.  The first call shall have an index of zero.
- Accumulates the number of lines, terminated by`\n`, in the text fragments in field `line`.  Initialise to 1.  
- Record the fragment `text` fields in a stack `stack`.

The each time the function is called:
- Copy fields from the Fragment to Tracker.  
- The stack field shall be a copy of the state of the stack in `TrackerManager`
- Copy the index
- Make a copy of the stack.
- Return a `Tracker` object

When the index value is divisible by 4:
- Clear the stack in `TrackerManager`.
- Return a tuple containing
- A `Tracker` object.
- A `Block` object. 
	- The prefix_directive shall be the value of `stack[1]`
	- The suffix_directive shall be the value of `stack[3]`
	- The text shall be the value of `stack[2]`
- A `Text` object:
	- The text shall be the value of `stack[0]`


# Write pytest to verify the functionality 

In the file `tests\test_fragments_to_tracker.py`:

- Import class `Fragment`.
- Verify the cumulative state after all fragments are processed.

- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  
# Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions which are not explicitly stated in the function specification.
