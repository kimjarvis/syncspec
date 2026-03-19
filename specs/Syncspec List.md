# Syncspec List

## Functional specification

<!-- {="import": "src/syncspec/text.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass

@dataclass
class Text:
    text: str
    name: str
```
<!-- {==} -->

<!-- {="import": "src/syncspec/file.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass

@dataclass
class File:
    text: str
    name: str
```
<!-- {==} -->

<!-- {="import": "src/syncspec/syncspec_text_context.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass, field
from typing import Any, Dict
import networkx as nx

@dataclass
class SyncspecTextContext:
    open_delimiter: str
    close_delimiter: str
    graph: nx.DiGraph
    monad: Dict[str, Any]
    import_path: str
```
<!-- {==} -->

Import this function from file  `src/syncspec/syncspec_text.py`:
```python
def make_syncspec_text(context: SyncspecTextContext):
	def syncspec_text(text: Text) -> File
```

The function `make_syncspec_text` is already implemented, it contains: 
- Logic to write to the log file and graph file.
- Transformation logic, using the delimiters.

<!-- {="import": "src/syncspec/syncspec_list_context.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class SyncspecListContext:
    open_delimiter: str
    close_delimiter: str
    monad: Dict[str, Any]
    import_path: str
```
<!-- {==} -->

Do not generate code to initialise `SyncspecListContext`.
### Implement the unary function

In the file `src/syncspec/syncspec_list.py`.

Define a closure factory with a unary function with signature:

```python
from typing import List, Tuple

def make_syncspec_list(context: SyncspecListContext):
	def syncspec_list(text: List[Text]) -> Tuple[List[File], nx.DiGraph, dict] 
```

In `make_syncspec_list`:

- Construct a `SyncspecTextContext` object.
	- Copy the open and closing delimiter from `SyncspecListContext` to  `SyncspecTextContext`.
	- Initialise `SyncspecTextContext.graph` to an empty DiGraph.
	- Copy monad from `SyncspecListContext` to  `SyncspecTextContext`.

In `syncspec_list`:

- For each item in the list text:
	- Call `make_syncspec_text` , passing the initialised instance of `SyncspecTextContext`  which returns a function which we call `syncspec_text`.
	- Call the unary `syncspec_text` function passing the Text object as a parameter.
	- Add the returned object of type File to the list of type `List[File]`.

Return a tuple containing:
- The list of file objects
- An object of type nx.DiGraph  `SyncspecTextContext.G`
- Dictionary `SyncspecTextContext.monad`

<!-- {= "include": "package_assumptions", "head": 1, "tail": 1 =} -->
## Assume

- UTF-8 encoding is used for all file I/O.
- "Valid file path" implies the parent directory must exist.
- Package pydot is installed.  The executable is accessible.
- Graphviz is installed.  The executable is accessible.
- Package networkx is installed.  The executable is accessible.
- The user has read and write access to the file locations.
<!-- {==} -->


<!-- {= "include": "package", "head": 1, "tail": 1 =} -->
## Package

- The function is part of the python package `src/syncspec` .   
- Imports from the package take the form `from src.syncspec.x import X`.
- Assume Python version 3.7.

<!-- {==} -->

<!-- {= "include": "explain_the_solution", "head": 1, "tail": 1 =} -->
## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.

<!-- {==} -->


