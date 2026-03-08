## Functions

### Validate Text  

Performs all validation.
### Fragment Text

Returns Fragment objects.
### Generate Blocks

Returns objects of  types, String, Block.
### Process Source Blocks

Populate the dictionary with from blocks of type source.
### Process Include Blocks

Use the dictionary to create blocks of type include.
### Combine Blocks

Combines the blocks to produce the output text.
## Classes

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

Import this class from file `src/syncspec/fragment.py`:
```python
from dataclasses import dataclass

@dataclass
class Fragment:  
    text: str
    line_number: int
```

Import this class from file `src/syncspec/string.py`:
```python
from dataclasses import dataclass

@dataclass
class String:
    text: str
    line_number: int    
```

Import this class from file `src/syncspec/block.py`:
```python
from dataclasses import dataclass

@dataclass
class Block:
    directive: str  
    text: str
    line_number: int    
```

## Monad

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


