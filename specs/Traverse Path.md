## Import 

Import `Context` from file `context.py`

<!-- {- import="../src/syncspec/context.py",  head=2,  tail=2 -} -->
```python
from dataclasses import dataclass, field
from typing import Any, Dict, List
from pathlib import Path

@dataclass
class Context:
    open_delimiter: str
    close_delimiter: str
    keyvalue: dict
    input_path: Path
    keyvalue_file: Path
    ignore_rules_file: Path
```
<!-- {--} -->
<!-- {- import="../src/syncspec/dummy.py",  head=2,  tail=2 -} -->
```python
from dataclasses import dataclass

@dataclass
class Dummy:
    pass
```
<!-- {--} -->
<!-- {- import="../src/syncspec/stop.py",  head=2,  tail=2 -} -->
```python
from dataclasses import dataclass

@dataclass
class Stop:
    pass
```
<!-- {--} -->
<!-- {- export="../src/syncspec/file_path.py",  head=2,  tail=2 -} -->
```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class FilePath:
    path: Path
    text: str
```
<!-- {--} -->
## Implement a unary function

In the file `src/syncspec/traverse_path.py`.

Define a closure factory with a unary function with signature:

<!-- {- source="traverse_path_spec" -} -->
```python
def make_traverse_path(context: Context):
    def traverse_path(fact: Dummy) -> Union[List[FilePath],Stop]:

```
<!-- {--} -->

<!-- {- source="traverse_path_action" -} -->
### Traverse Path

Recursively walk through a directory, ignoring files and folders based on patterns from a specified ignore file.  Create an object for each target file encountered.

- Compile the ignore_rules file.
- Recursively traverse the directory path `context.input_path`.    
- Check the path.
- Return a list of objects of type `FilePath`, or an empty list no valid files are found.

<!-- {--} -->
### Compile the ignore_rules file

#### Action
The `ignore_rules` file contains a list of patterns to ignore in gitignore format.   
#### Steps:
- If the `ignore_rules` is specified:
	- Load and compile the ignore patterns from the file.
	- If compilation fails:
		- Log an error with an informative message:
			- Use `line_number` zero.
		- Return an object of type `Stop`.  
#### Use:
- The `PathSpec` module.
- The `GitWildMatchPattern` for the `.gitignore` syntax.
#### Assume that:
- The PathSpec module is available.
### Recursively traverse the directory.    

#### Description:

- The script shall open the ignore file and use `pathspec.PathSpec.from_lines('gitwildmatch', f)` to parse it. This creates a compiled pattern match. Uses `os.walk(start_directory)`, which is Python's standard tool for recursively traversing directories.
- Before `os.walk` descends into a sub-directory, the script checks if that directory's path matches an ignore pattern (like `node_modules/`). If it does, the directory is removed from the `dirs` list, preventing `os.walk` from even entering it. This is much faster than traversing it and then ignoring every file inside.
- For every file found, construct a relative path and uses `spec.match_file()` to test it against all loaded ignore patterns.
- Only the paths that do **not** match any pattern are added to the list.
### Check the path
#### Steps

- Ensure that:  
	- The file must be in directory `Context.input_path` or one of its sub-directories.  Accessing a parent directory is not allowed.
	- If the file is a symbolic link then the link target must also be in the directory or one of its sub-directories.  Accessing a parent directory is not allowed.
	- The file must exist.
- When any of the ensured conditions are violated:
	- Log an error with an informative message:
		- Use `line_number` zero.
	- Return an object of type `Stop`.  
- Determine whether the file should be ignored:
	- Ignore binary files.
	- Ignore unreadable files. 
	- Ignore files that do not contain either the open delimiter or the close delimiter.
- When a file is ignored :
	- Do not add to the list of `FilePath` objects.

<!-- {-  include="format_error" -} -->
## Logging info, warnings and errors

Import logging.

Import the formatting function with this signature from file `syncspec.utilities.py`:
```python
def format_log_message(message: str, path: Path, line_number: int) -> str:
```

<!-- {--} -->

<!-- {-  include="package" -} -->
## Package

- The function is part of the python package `src/syncspec` .   
- Imports from the package take the form `from syncspec.x import X`.
- Assume Python version 3.9.

<!-- {--} -->

<!-- {-  include="generate_tests" -} -->
## Write pytests to verify the functionality

- Write tests in a separate file.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

<!-- {--} -->

<!-- {-  include="explain_the_solution" -} -->
## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.

<!-- {--} -->
