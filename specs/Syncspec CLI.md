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
    monad: Dict[str, Any]
	import_path: str
```

Import this closure factory from the file `src/syncspec/syncspec_list.py`.
```python
from typing import List, Tuple

def make_syncspec_list(context: SyncspecListContext):
	def syncspec_list(text: List[Text]) -> Tuple[List[File], nx.DiGraph, dict]: 
```

### Implement a command line interface

In the file `cli.py`.

Parse keyword parameters:
`--open_delimiter` with default "{{"
`--close_delimiter` with default "}}"
`--log_file` optional
`--graph_file` with default "syncspec.dot"
`--keyvalue_file` optional
`--output` required.
`--import_path` optional.
And required positional parameter `path`  
#### Validate the parameters

- `--log_file` if specified, this must be a valid file path.  The file suffix must be `.log`.  
- `--keyvalue_file` if specified, this must be a valid file path.  The file suffix must be `.json`.  
- `--graph_file` must be a valid file path.  The file suffix must be `.dot` . 
- `--output` must be a path to an existing directory.
- `path` is a path to an existing directory.
#### Ensure that:

- Delimiters are valid Unicode strings.
- Delimiters are not empty strings.
- Delimiters are distinct, e.g., they will not be `{{` and `{{`.
- Delimiters do not overlap structurally.  Open cannot be a sub-string of close and vice versa. e.g., they will not be `{{` and `{`. 
- Delimiters do not contain newlines.

Validation failures shall print an informative message to `stderr` and terminate via `sys.exit(1)`.

Set up Python logging:
- If `--log_file` is specified log to this file.  Otherwise, log to the console.
- Use basic configuration with format `"%(levelname)s - %(message)s"`.  
- Set the log level to warning.

Construct `SyncspecListContext` from the parameters.

Argument `--keyvalue_file` specifies a state input file.  The file is optional for input. defaulting to "syncspec.json" if exists, else `{}`.
- Covert the state input file into a dictionary.
- Set the value of `SyncspecListContext.monad` to the dictionary.  
- The dictionary keys must be strings.  

JSON validation failures and errors resulting from the conversion of the JSON to a dictionary shall print an informative message to `stderr` and terminate via `sys.exit(1)`.

If `--import_path` is omitted, it defaults to the value of the positional path argument.

Traverse the directory `path` recursively.  For each markdown  `.md` file encountered create an object of type `Text` and add it to a list.  `Text.text` shall be the file content.  `Text.name` shall be the file path relative to `path`.

Pass the list of `Text` objects to `syncspec_list`.   

The function `syncspec_list` returns a tuple:

The first tuple item is a list of `File` objects.

Iterate through the returned `File` objects.   Create a file containing `File.text` on the file path constructed from `output` and `File.name`.  `File.name` may contain sub-directories so use  `mkdir(parents=True)` to construct the path.

Catch any value error exceptions raised in `make_syncspec_list` and `syncspec_list`.  Print the message to stderr and terminate via sys.exit(1).

The second tuple item is of type `nx.DiGraph`.  Use it to create a Grapviz dot file.  Use `nx.nx_pydot.write_dot` to write the file specified by `--graph_file`.

The third tuple item is a dictionary with string keys.  Convert the dictionary to JSON.  

If `--keyvalue_file` is specified, write the JSON to the file specified by `--keyvalue_file`.  

If `--keyvalue_file` is not specified, write the JSON to the file "syncspec.json".

Catch any exception raised by the conversion.  If an exception is raised print an informative message to `stderr` and terminate via `sys.exit(1)`. 

## Note

- Use pathlib to construct paths.   
## Assume

- UTF-8 encoding is used for all file I/O.
- "Valid file path" implies the parent directory must exist.
- Package pydot is installed.  The executable is accessible.
- Graphviz is installed.  The executable is accessible.
- Package networkx is installed.  The executable is accessible.
- The user has read and write access to the file locations.
## Package

`src/syncspec` is a Python package.   Imports take the form `from src.syncspec.x import X`.
## Explain the solution  

- Describe any logical inconsistencies in this function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.
