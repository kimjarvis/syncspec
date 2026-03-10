## Functions

### Validate Text  

Performs all validation.
### Fragment Text

Returns Fragment objects.
### Create Blocks

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

Import this class from file `src/syncspec/block.py`:
```python
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Block:
    directive: Dict[str, Any]  
    prefix: str
    suffix: str
    text: str
    line_number: int    
```

Import this class from file `src/syncspec/source.py`:
```python
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Source(Block):
	pass
```




