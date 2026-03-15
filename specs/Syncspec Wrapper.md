# Syncspec

## Functional specification

Import this class from file `src/syncspec/text.py`:
```python
from dataclasses import dataclass

@dataclass
class Text:
    text: str
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

Import this class from file `src/syncspec/syncspec_string_context.py`:
```python
from dataclasses import dataclass, field
from typing import Any, Dict
import networkx as nx

@dataclass
class SyncspecStringContext:
    open_delimiter: str
    close_delimiter: str
    log: str
	G: nx.DiGraph
	monad: Dict[str, Any]
	import_path: str
```

Import this function from file  `src/syncspec/syncspec_string.py`:
```python
def make_syncspec_string(context: SyncspecStringContext):
	def syncspec_string(text: Text) -> File
```

The function `make_syncspec_string` is already implemented, it contains: 
- Logic to write to the log file and graph file.
- Transformation logic, using the delimiters.

Import this class from file `src/syncspec/syncspec_context.py`:
```python
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class SyncspecContext:
    open_delimiter: str
    close_delimiter: str
    log_file: str
    graph_file: str
	import_path: str    
```

Do not generate code to initialise `SyncspecContext`.

Verify at context in function `make_syncspec`:
- open_delimiter and close_delimiter are not empty strings.
- log_file is a valid file path.  The file does not exist already.
- graph_file is a valid file path.  The file does not exist already.
- import_path is a valid directory path.  The directory must exist.
### Implement the unary function Syncspec

In the file `src/syncspec/syncspec_file.py`.

Define a closure factory with a unary function with signature:

```python
from typing import List

def make_syncspec_file(context: SyncspecContext):
	def syncspec_file(text: List[Text]) -> List[File]
```

- The context parameters are used to set the delimiters.
- The function can assume that the file paths are valid. 
- Construct a `SyncspecStringContext` object.
	- Copy the open and closing delimiter from `SyncspecContext` to  `SyncspecStringContext`.
	- Initialise `SyncspecStringContext.log` to an empty string.
	- Initialise `SyncspecStringContext.G` to an empty DiGraph.
	- Initialise `SyncspecStringContext.monad` to an empty dictionary.
- For each item in the list text:
	- Call `make_syncspec_string` , passing the initialised instance of `SyncspecStringContext`  which returns a function which we call `syncspec_string`.
	- Call the unary `syncspec_string` function passing the Text object as a parameter.
	- Add the returned object of type File to the list to be returned.
 
## Package

`src/syncspec` is a Python package.   Imports take the form `from src.syncspec.x import X`.

## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.



