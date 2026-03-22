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

<!-- {="import": "src/syncspec/parameter_file.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass

@dataclass
class File:
    text: str
    name: str
```
<!-- {==} -->

<!-- {= "import": "src/syncspec/syncspec_list_context.py", "head": 2, "tail": 2 =} -->
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

Import this closure factory from the file `src/syncspec/syncspec_list.py`.
```python
from typing import List, Tuple

def make_syncspec_list(context: SyncspecListContext):
	def syncspec_list(text: List[Text]) -> Tuple[List[File], nx.DiGraph, dict]: 
```

### Implement the unary function

In the file `src/syncspec/function.py`.

Define a function with signature:

```python
def syncspec(
        path: str,
        output: Optional[str] = None,
        open_delimiter: str = "{{",
        close_delimiter: str = "}}",
        import_path: Optional[str] = None,
        keyvalue: Optional[Dict[str, str]] = {},
        log_file: Optional[str] = "syncspec.log",
) -> Tuple[nx.DiGraph, dict]:
```

- `path` is a path to an existing directory.  Required parameter.
- `output` is a valid directory path.  Create the directory if missing.  If not specified default to `path`.
- `import_path` is a path to an existing directory.  If not specified default to `path`.
- `log_file` is a valid path to file.  That is, the parent directory exists.  The file suffix must be `.log` .   Default to `Path("syncspec.log")`
- The `keyvalue` dictionary keys are strings.   Default to an empty dictionary. 
- `open_delimiter` default to "{{"
- `close_delimiter` default to "}}"
#### Ensure that:

- Delimiters are valid Unicode strings.
- Delimiters are not empty strings.
- Delimiters are distinct, e.g., they will not be `{{` and `{{`.
- Delimiters do not overlap structurally.  Open cannot be a sub-string of close and vice versa. e.g., they will not be `{{` and `{`. 
- Delimiters do not contain newlines.

Validation failures shall raise a value error exception.

Set up Python logging:
- Log to file `log_file`.
- Use basic configuration with format `"%(levelname)s - %(message)s"`.  
- Set the log level to warning.

Construct the `SyncspecListContext`:
- Set the delimiters.
- Set the import path.
- Set `monad` to the `keyvalue` dictionary

Traverse the directory `path` recursively.  For each markdown  `.md` file encountered create an object of type `Text` and add it to a list.  `Text.text` shall be the file content.  `Text.name` shall be the file path relative to `path`.

Pass the list of `Text` objects to `syncspec_list`.   

The function `syncspec_list` returns a tuple:

The first tuple item is a list of `File` objects.

Iterate through the returned `File` objects.   Create a file containing `File.text` on the file path constructed from `output` and `File.name`.  `File.name` may contain sub-directories so use  `mkdir(parents=True)` to construct the path.

Return a tuple comprised of the: 
- The second tuple item returned by `syncspec_list`, which is an item is of type `nx.DiGraph`.   
- The third tuple item returned by `syncspec_list`, which is an item is a dictionary with string keys.  
## Test the function  

In the file `tests/test_syncspec.py`.

Write a test function `test_syncspec`. 

Add `src` directory to Python path for development tests like this. 

```
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from syncspec import syncspec
```

Use this code as a guideline:

```python
syncspec(path="../syncspec-test/input/",output="../syncspec-test/output/",import_path="../syncspec-test/input/",keyvalue={},log_file="syncspec.log")
```

The function returns a tuple:
- Convert networkx graph to dot format and write to file "syncspec.dot".   Use the function `nx.nx_pydot.write_dot`
- Convert the dictionary to JSON and write to file "syncspec.json".

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





