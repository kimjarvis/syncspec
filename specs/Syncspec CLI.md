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

Import this closure factory from the file `src/syncspec/syncspec.py`.
```python
from typing import List

def make_syncspec(context: SyncspecContext):
	def syncspec(text: List[Text]) -> List[File]
```

### Implement a command line interface

In the file `cli.py`.

Parse keyword parameters:
`--open_delimiter` with default "{{"
`--close_delimiter` with default "}}"
`--log_file` with default "log.txt"
`--graph_file` with default "graph.dot"
`--output` required.
`--import_path` optional.
And required positional parameter `path`  
#### Validate the parameters

- `--log_file` must be a valid file path.  If the file exists it shall be overwritten.
- `--graph_file` must be a valid file path.  The file suffix must be `.dot`  . If the file exists it shall be overwritten.
- Verify that output is a path to an existing directory.
- Verify that path is a path to an existing directory.

Validation failures shall print an informative message to stdout and terminate via sys.exit(1).

Construct `SyncspecContext` from the parameters.

 If `--import_path` is omitted, it defaults to the value of the positional path argument.

Traverse the directory `path` recursively.  For each markdown  `.md` file encountered create an object of type `Text` and add it to a list.  `Text.text` shall be the file content.  `Text.name` shall be the file path relative to `path`.

Pass the list of `Text` objects to `syncspec`.   A list of `File` objects shall be returned.

Iterate through the returned `File` objects.   Create a file containing `File.text` on the file path constructed from `output` + `/` + `File.name`.  `File.name` may contain sub-directories so use  `mkdir(parents=True)` to construct the path.
## Assume

- UTF-8 encoding is used for all file I/O.
- "Valid file path" for logs implies the parent directory must exist, though the file itself may be overwritten.
-  `make_syncspec` is pure and does not raise exceptions during processing.
## Package

`src/syncspec` is a Python package.   Imports take the form `from src.syncspec.x import X`.
## Explain the solution  

- Describe any logical inconsistencies in this function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.
