
## Imports

<!-- {- export="../src/syncspec/context.py",  head=2,  tail=2 -} -->
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

<!-- {- source="cli_action" -} -->
## Command line interface

- Parse parameters.  
- Validate Parameters. 
- Create context. 
- Call machine function.
<!-- {--} -->
#### Description:

<!-- {- source="cli_spec" -} -->

Parse optional keyword parameters

`--open_delimiter` with default "{"+"-" (Two characters, open curly brace and minus sign).  Describe the default value.
`--close_delimiter` with default "-"+"}" (Two characters, minus sign and close curly brace). Describe the default value.
`--keyvalue` is a file path.  If specified, the file must exist.  The file suffix must be `.json`. 
`--ignore_rules` is a file path.  if specified, the file must exist. 

Required positional parameter:

1. `input_path`  this must be a valid directory path.

<!-- {--} -->
#### Use:
- `argsparse`.  
- The `--help` message shall print an explanation of the parameters.
- Implement the main idiom:
```python
if __name__ == "__main__":
    main()
```

#### Steps:
- Create a `Context` object from the parameter values.
	- Convert the parameter values to absolute paths.
	- Set `keyvalue` to an empty dictionary.  
- Import `machine`.
- Call function with signature:

```python
def machine(context: Context) -> None:
```
### Note 

- Note that `sys.exit(0)` raises a `SystemExit` exception.

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
