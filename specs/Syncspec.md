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
```

Do not generate code to initialise the context.

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
```

Do not generate code to initialise the context.


Use this code as a guideline. 
### Implement the unary function Syncspec

In the file `src/syncspec/syncspec.py`.

Define a closure factory with a unary function with signature:

```python
from typing import List

def make_syncspec(context: SyncspecContext):
	def syncspec(text: List[Text]) -> List[File]
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

#### Implement a calling program

Generate a python program `main1.py` that calls `syncspec`.  The main function shall parse keyword parameters:
`--open_delimiter` with default "{{"
`--close_delimiter` with default "}}"
`--log_file` with default "log.txt"
`--graph_file` with default "graph.dot"
`--output` required.   
And required positional parameter `path`  
#### Validate the parameters

- `--log_file` must be a valid file path.  The file should not exist.
- `--graph_file` must be a valid file path.  The file suffix must be `.dot`  . The file should not exist.
- Verify that output is a path to an existing directory.
- Verify that path is a path to an existing directory.

Print an informative error message and stop if verification fails.

Construct the syncspec context from the parameters.

Traverse the directory `path` recursively.  For each markdown  `.md` file encountered create an object of type `Text` and add it to a list.  `Text.text` shall be the file content.  `Text.name` shall be the file path relative to `path`.

Pass the list of `Text` objects to `syncspec`.   A list of `File` objects shall be returned.

Iterate through the returned `File` objects.   Create a file containing `File.text` on the file path constructed from `output` + `/` + `File.name`.
## Package

`src/syncspec` is a Python package.   Imports take the form `from src.syncspec.x import X`.

## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.



