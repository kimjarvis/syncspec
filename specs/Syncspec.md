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
def make_syncspec(context: SyncspecContext):
	def syncspec(text: List[Text]) -> List[Text]
```

- The context parameters are used to set the delimiters.
- The context objects are shared by each iteration.
- The function can assume that the file paths are valid. 
- Construct a `SyncspecStringContext` object.
	- Copy the open and closing delimiter from `SyncspecContext` to  `SyncspecStringContext`.
	- Initialise `SyncspecContext.log` to an empty string.
	- Initialise `SyncspecContext.G` to an empty DiGraph.
	- Initialise `SyncspecContext.monad` to an empty dictionary.
- Call `make_syncspec_string`.
- For each item in the list text:
	- Call the unary `syncspec_string` function passing text as a parameter.
	- Construct a Text object .

#### Implement a calling program

Generate a python programe `main1.py` that calls `syncspec`.  The main function shall parse keyword parameters:
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

Pass the list of `Text` objects to `syncspec`.   A list of `Text` objects shall be returned.

Iterate through the returned `Text` objects.   Create a file containing `Text.text` on the file path constructed from `output` + `/` + `Text.name`.
## Package

`src/syncspec` is a Python package.   Imports take the form `from src.syncspec.x import X`.
## Test the unary function  

In the file `tests/test_syncspec.py`.

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  
## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.



