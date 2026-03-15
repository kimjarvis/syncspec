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

Import this class from file `src/syncspec/syncspec_list_context.py`:
```python
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class SyncspecListContext:
    open_delimiter: str
    close_delimiter: str
    log_file: str
    graph_file: str
	import_path: str
```

Import this closure factory from the file `src/syncspec/syncspec_list.py`.
```python
from typing import List, Tuple

def make_syncspec_list(context: SyncspecListContext):
	def syncspec_list(text: List[Text]) -> Tuple[List[File], str, nx.DiGraph, dict]: 
```

### Implement a command line interface

In the file `cli.py`.

Parse keyword parameters:
`--open_delimiter` with default "{{"
`--close_delimiter` with default "}}"
`--log_file` with default "log.txt"
`--graph_file` with default "graph.dot"
`--keyvalue_file` with default "keyvalue.json"
`--output` required.
`--import_path` optional.
And required positional parameter `path`  
#### Validate the parameters

- `--log_file` must be a valid file path.  Create and empty file.  If the file already exists it shall be overwritten.
- `--keyvalue_file` must be a valid file path.  Create and empty file.  If the file already exists it shall be overwritten.
- `--graph_file` must be a valid file path.  The file suffix must be `.dot`  . Create and empty file.  If the file already exists it shall be overwritten.
- Verify that output is a path to an existing directory.
- Verify that path is a path to an existing directory.

Validation failures shall print an informative message to stdout and terminate via sys.exit(1).

Construct `SyncspecListContext` from the parameters.

 If `--import_path` is omitted, it defaults to the value of the positional path argument.

Traverse the directory `path` recursively.  For each markdown  `.md` file encountered create an object of type `Text` and add it to a list.  `Text.text` shall be the file content.  `Text.name` shall be the file path relative to `path`.

Pass the list of `Text` objects to `syncspec`.   

The function `syncspec_list` returns a tuple:

`Tuple[List[File], str, nx.DiGraph, dict]`

The first tuple item is a list of `File` objects shall be returned.

Iterate through the returned `File` objects.   Create a file containing `File.text` on the file path constructed from `output` + `/` + `File.name`.  `File.name` may contain sub-directories so use  `mkdir(parents=True)` to construct the path.

Catch any value error exceptions raised in `make_syncspec_list` and `syncspec_list`.  Print the message to stdout and terminate via sys.exit(1).

The second tuple item is a string.  Write the string to the file specified by `--log_file`.

The third tuple item is a nx.DiGraph.  Use it to create a grapviz dot file.  Use `nx.nx_pydot.write_dot` to write the file specified by `--graph_file`.

The forth tuple item is a dictionary with string keys.  Convert the dictionary to json.  Write to the file specified by `--keyvalue_file`.  Catch any exception raised by the conversion.  If an exception is raised print an informative message to stdout and terminate via sys.exit(1). 
## Assume

- UTF-8 encoding is used for all file I/O.
- "Valid file path" for logs implies the parent directory must exist, though the file itself may be overwritten.
- Packge pydot is installed.  Graphviz is installed.  Package networkx is installed.
## Package

`src/syncspec` is a Python package.   Imports take the form `from src.syncspec.x import X`.
## Explain the solution  

- Describe any logical inconsistencies in this function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.
