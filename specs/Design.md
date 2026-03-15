# Functions

### [[Validate Text]]  

Performs all validation.
### [[Fragment Text]]

Returns Fragment objects.
### [[Create Blocks]]

Returns objects of  types, String, Block.
### [[Source Block]]

Populate the dictionary from blocks of type source.  Converts a block of type Source into a String.
### [[Include Block]]

Use the dictionary to look up a key.  Converts a block of type Include into a String.
### [[Import Block]]

Create blocks of type String from files.
### [[Combine Strings]]

Combines the Strings to produce the output text.
### [[Combine Errors]]

Combines the Errors to produce a log.
### [[Combine Nodes]]

Combine Nodes to make a graph.
# Classes

Import this class from file `src/syncspec/text.py`:
```python
from dataclasses import dataclass

@dataclass
class Text:
    text: str
    name: str
```

Import this class from file `src/syncspec/validated_text.py`:
```python
from dataclasses import dataclass

@dataclass
class ValidatedText:
    text: str
    name: str    
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
    name: str    
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

Import this class from file `src/syncspec/string.py`:
```python
from dataclasses import dataclass

@dataclass
class String:
    text: str
    line_number: int
    name: str
```

Import this class from file `src/syncspec/file.py`:
```python
from dataclasses import dataclass

@dataclass
class File:
    text: str
    name: str
```


Import this class from file `src/syncspec/node.py`:
```python
from dataclasses import dataclass

@dataclass
class Node:
    directive_type: str
    key: str
    line_number: int    
    name: str
```


Import this class from file `src/syncspec/edge.py`:
```python
from dataclasses import dataclass

@dataclass
class Edge:
    directive_type: str
    key: str
    line_number: int    
    name: str
```


