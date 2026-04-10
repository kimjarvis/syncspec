# syncspec
**Transclusion for Spec-as-Source Development**

Syncspec enables bidirectional content embedding between files, allowing you to maintain specifications and source code in sync.

## Installation

Install the CLI tool from PyPI:

```bash
pip install syncspec

## Quick start

Run syncspec in your working directory:

```bash
syncspec .
```

The tool recursively processes all files in the specified directory.

### Ignore files and directories

Create a rules file in .gitignore format to exclude specific paths. By default, syncspec looks for .syncspec_ignore in the working directory.

Example .syncspec_ignore file:

<!-- {- import=".syncspec_ignore", head=2, tail=2 -} -->
```
# Ignore Python cache and virtual environment
__pycache__/
.venv/
.git/
.pytest_cache/

# Ignore Python source files and build output
*.py
dist/
```
<!-- {--} -->

### Import directive

Embeds content from another file into the current file.

Behavior:

- Paths are relative to the receiving file
- Files must be within the working directory
- Imports are idempotent (only updates when source changes)

Example:

```
<!-- {- import="src/syncspec/dummy.py" -} -->
from dataclasses import dataclass

@dataclass
class Dummy:
    pass
<!-- {--} -->
```

### Export directive

Writes content from the current file to an external file.

Example:

```
<!-- {- export="packge_info.md" -} -->
- The function is part of the python package `src/syncspec` .   
- Imports from the package take the form `from syncspec.x import X`.
- Assume Python version 3.9.
<!-- {--} -->
```

### Source and Include directives

These directives work like export and import but operate on named content blocks without creating files.

Use cases:

- `source`: Define reusable content blocks
- `include`: Reference defined content blocks


```
<!-- {- source="explain" -} -->
## Explain the solution  

- Describe logical inconsistencies in the function specification
- Suggest improvements
- List unstated assumptions
<!-- {--} -->
<!-- {- include="explain" -} -->
## Explain the solution  

- Describe logical inconsistencies in the function specification
- Suggest improvements
- List unstated assumptions
<!-- {--} -->
```

### Head and tail

Control how many lines to skip from the beginning (head) or end (tail) of imported content.

Example - Skip first 2 and last 2 lines:

````
<!-- {- import="src/syncspec/dummy.py", head=2, tail=2 -} -->
```python
from dataclasses import dataclass

@dataclass
class Dummy:
    pass
```
<!-- {--} -->
````

## Safety

- **Idempotent operations**: Running the same directive multiple times only updates content when the source has changed.
- **Relative paths**: All file paths are relative to the file containing the directive.
- **Working directory**: All imported/exported files reside within the  working directory.




