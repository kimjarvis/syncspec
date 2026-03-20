# Import Block 

## Functional specification

<!-- {= "include": "format_error", "head": 1, "tail": 1 =} -->

Import logging.

Import the function with this signature from file `src/syncspec/utilities.py`:
```python
def format_error(message: str, name: str, line_number: int) -> str:
```

<!-- {==} -->

<!-- {="import": "src/syncspec/node.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass

@dataclass
class Node:
    directive_type: str
    key: str
    line_number: int
    name: str
```
<!-- {==} -->

<!-- {="import": "src/syncspec/string.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass

@dataclass
class String:
    text: str
    line_number: int
    name: str
```
<!-- {==} -->

<!-- {="import": "src/syncspec/block.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class Block:
    directive: Dict[str, Any]
    prefix: str
    suffix: str
    text: str
    line_number: int
    name: str
```
<!-- {==} -->

<!-- {="import": "src/syncspec/import_block_context.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass, field
from typing import ClassVar, Dict, Any

@dataclass
class ImportBlockContext:
    import_path: str
    open_delimiter: str
    close_delimiter: str
```
<!-- {==} -->

Do not generate code to initialise the context.
### Implement a unary function

In the file `src/syncspec/import_block.py`.

Define a closure factory with a unary function with signature:

```python
def make_import_block(context: ImportBlockContext):	
	def import_block(block: Block) -> Union[Tuple[String, Node, Node], Block, String]:
```

If dictionary `Block.directive` contains a key "import" then:

The value of `block.directive["import"]` is a relative file or symbolic link path.  The path is relative to the directory path `ImportBlockContext.import_path`.  

Ensure that:  
- The file must be in directory `ImportBlockContext.import_path` or one of its sub-directories.  Accessing a parent directory is not allowed.
- If the file is a symbolic link then the link target must also be in the directory `ImportBlockContext.import_path` or one of its sub-directories.  
- The file exists.  
- The file is a text file, not a binary file.  Treat it as utf-8. 
- The file is readable.
When any of the validation conditions are violated Log and error and return a String.

Read the content of the file into string variable `v`.

Copy string `block.text` to `u`.

If dictionary `Block.directive` contains a key "head" with an integer value call it head, otherwise set `head=1`.  

Let top be the first head lines of `u`.

If dictionary `Block.directive` contains a key "tail" with an integer value call it tail, otherwise set `tail=1`.

Let bottom be the last tail lines of `u`.

Assume that:

- Directive values `Block.directive["head"]=0`  and `Block.directive["tail"]=0` are valid no-ops even when `u` is an empty string.
 
Ensure that:
- `v` is a string.
- Strings top and bottom do not overlap.  Overlap is defined strictly as `head + tail > total_lines`. 
- Negative head or tail values shall be rejected as invalid.
When any of the validation conditions are violated Log and error and return a String.

Return a tuple containing object of type String:
- Copy `line_number` from Block.
- Copy `name` from Block.
- Concatenate these strings in order to create `String.text`:

1. `ImportBlockContext.open_delimiter`
2. `block.prefix`
3. `ImportBlockContext.close_delimiter`
4. `top`, the first h lines of `block.text`
5. The value of v
6. Add a new line character `\n` unless `Block.directive["eol"]=False` 
7. `bottom` the last t lines of `block.text`
8. `ImportBlockContext.open_delimiter`
9. `block.suffix`
10. `ImportBlockContext.close_delimiter`

The tuple shall also contain an object of type Node:
- The `line_number` shall be zero.
- `name` shall be the value of `block.directive["import"]` 
- Set the directive type to "export"
- Set the key to  the value of `block.directive["import"]`

The tuple shall also contain another object of type Node:
- Copy `line_number` from Block.
- Copy `name` from Block
- Set the directive type to "import"
- Set the key to  the value of `block.directive["import"]` 

If dictionary `Block.directive` does not contains a key "import" then return an object of type Block:
- Return the input parameter unchanged.

#### Log and error and return a String

When conditions are violated:
- Call `format_error` to format an error messages.  Pass an informative message,   `Block.name` and the line number on which the error was detected.  Use python logging to log the error.
- Return an object of type `String`.
	- Copy name and line number from block.
	- `String.text = ImportBlockContext.open_delimiter + Block.prefix + ImportBlockContext.close_delimiter + Block.text + ImportBlockContext.open_delimiter + Block.suffix + ImportBlockContext.close_delimiter

#### Assume that

- Line Splitting:  `splitlines(keepends=True)` is used to define "lines". This preserves newline characters during slicing and reconstruction.
- Integer Validation: Boolean values are excluded from integer checks for head/tail (since bool is a subclass of int in Python).

<!-- {= "include": "package", "head": 1, "tail": 1 =} -->
## Package

- The function is part of the python package `src/syncspec` .   
- Imports from the package take the form `from src.syncspec.x import X`.
- Assume Python version 3.7.

<!-- {==} -->
## Test the unary function  

In the file `tests/test_import_block.py`.

<!-- {= "include": "generate_tests", "head": 1, "tail": 1 =} -->

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

<!-- {==} -->

<!-- {= "include": "explain_the_solution" =} -->
## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.

<!-- {==} -->

<!-- {= "include": "current_implementation" =} -->
## Current implementation

- Minimise changes to the current implementation.

This is the current implementation:
<!-- {==} -->

<!-- {= "import": "src/syncspec/import_block.py", "head": 2, "tail": 2 =} -->
```python
import logging
from pathlib import Path
from typing import Union, Tuple, Dict, Any

from src.syncspec.node import Node
from src.syncspec.utilities import format_error
from src.syncspec.string import String
from src.syncspec.block import Block
from src.syncspec.import_block_context import ImportBlockContext


def make_import_block(context: ImportBlockContext):
    def import_block(block: Block) -> Union[Tuple[String, Node, Node], Block, String]:
        if "import" not in block.directive:
            return block

        import_path = block.directive["import"]
        log_err = lambda msg: _log_and_return_error(msg, block, context)

        # Path Validation
        try:
            root = Path(context.import_path).resolve()
            target = (root / import_path).resolve()

            if not str(target).startswith(str(root) + '/') and str(target) != str(root):
                return log_err("Path traversal detected")
            if not target.exists():
                return log_err("File does not exist")
            if not target.is_file():
                return log_err("Not a file")
            if target.is_symlink():
                link_target = target.resolve()
                if not str(link_target).startswith(str(root) + '/') and str(link_target) != str(root):
                    return log_err("Symlink target outside allowed directory")

            # Read and Decode
            try:
                v = target.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                return log_err("File is not valid UTF-8 text")
            except PermissionError:
                return log_err("File is not readable")
        except Exception as e:
            return log_err(f"Validation failed: {str(e)}")

        # Head/Tail Validation
        head = block.directive.get("head", 1)
        tail = block.directive.get("tail", 1)

        if not isinstance(head, int) or isinstance(head, bool) or head < 0:
            return log_err("Invalid head value")
        if not isinstance(tail, int) or isinstance(tail, bool) or tail < 0:
            return log_err("Invalid tail value")

        u_lines = block.text.splitlines(keepends=True)
        total_lines = len(u_lines)

        if head + tail > total_lines:
            return log_err("Head and tail overlap")

        top = "".join(u_lines[:head])
        bottom = "".join(u_lines[-tail:] if tail > 0 else [])

        # Construct Result String
        eol_char = "" if block.directive.get("eol") is False else "\n"
        s_text = (
                context.open_delimiter +
                block.prefix +
                context.close_delimiter +
                top +
                v +
                eol_char +
                bottom +
                context.open_delimiter +
                block.suffix +
                context.close_delimiter
        )
        res_string = String(text=s_text, line_number=block.line_number, name=block.name)

        # Construct Nodes
        n_export = Node(directive_type="export", key=import_path, line_number=0, name=import_path)
        n_import = Node(directive_type="import", key=import_path, line_number=block.line_number, name=block.name)

        return (res_string, n_export, n_import)

    return import_block


def _log_and_return_error(message: str, block: Block, context: ImportBlockContext) -> String:
    logging.error(format_error(message, block.name, block.line_number))
    text = (
            context.open_delimiter +
            block.prefix +
            context.close_delimiter +
            block.text +
            context.open_delimiter +
            block.suffix +
            context.close_delimiter
    )
    return String(text=text, line_number=block.line_number, name=block.name)
```
<!-- {==} -->

This is the current implementation:

<!-- {= "import": "tests/test_import_block.py", "head": 2, "tail": 2 =} -->
```python
import pytest
from pathlib import Path
from src.syncspec.import_block import make_import_block
from src.syncspec.block import Block
from src.syncspec.import_block_context import ImportBlockContext
from src.syncspec.string import String
from src.syncspec.node import Node

@pytest.mark.parametrize("directive,expected_type", [
    ({}, Block),
    ({"import": "valid.txt"}, tuple),
])
def test_import_key_presence(tmp_path, directive, expected_type):
    ctx = ImportBlockContext(import_path=str(tmp_path), open_delimiter="<", close_delimiter=">")
    func = make_import_block(ctx)
    (tmp_path / "valid.txt").write_text("content")
    # Provide enough lines for default head=1, tail=1
    block = Block(directive=directive, prefix="", suffix="", text="line1\nline2\n", line_number=1, name="test")
    result = func(block)
    assert isinstance(result, expected_type)

@pytest.mark.parametrize("import_path,should_fail", [
    ("valid.txt", False),
    ("../etc/passwd", True),
    ("missing.txt", True),
])
def test_path_security(tmp_path, import_path, should_fail):
    (tmp_path / "valid.txt").write_text("content")
    ctx = ImportBlockContext(import_path=str(tmp_path), open_delimiter="<", close_delimiter=">")
    func = make_import_block(ctx)
    # Provide enough lines for default head=1, tail=1
    block = Block(directive={"import": import_path}, prefix="", suffix="", text="line1\nline2\n", line_number=1, name="test")
    result = func(block)
    if should_fail:
        assert isinstance(result, String)
    else:
        assert isinstance(result, tuple)

@pytest.mark.parametrize("head, tail, block_lines, should_fail", [
    (1, 1, 5, False),
    (0, 0, 5, False),
    (0, 0, 0, False),  # Empty text with head=0, tail=0 is valid
    (1, 1, 1, True),  # Overlap: 1+1 > 1
    (3, 3, 5, True),  # Overlap: 3+3 > 5
    (-1, 0, 5, True),  # Negative head
    (True, 0, 5, True),  # Bool head
    (0, True, 5, True),  # Bool tail
])
def test_head_tail_validation(tmp_path, head, tail, block_lines, should_fail):
    (tmp_path / "valid.txt").write_text("imported content")
    ctx = ImportBlockContext(import_path=str(tmp_path), open_delimiter="<", close_delimiter=">")
    func = make_import_block(ctx)
    block_text = "\n".join(["block_line"] * block_lines)
    if block_lines > 0:
        block_text += "\n"
    block = Block(
        directive={"import": "valid.txt", "head": head, "tail": tail},
        prefix="", suffix="", text=block_text, line_number=1, name="test"
    )
    result = func(block)
    if should_fail:
        assert isinstance(result, String)
    else:
        assert isinstance(result, tuple)

@pytest.mark.parametrize("eol,expected_sep", [
    (True, "\n"),
    (False, ""),
    (None, "\n"),
])
def test_eol_directive(tmp_path, eol, expected_sep):
    (tmp_path / "valid.txt").write_text("imported")
    ctx = ImportBlockContext(import_path=str(tmp_path), open_delimiter="<", close_delimiter=">")
    func = make_import_block(ctx)
    directive = {"import": "valid.txt"}
    if eol is not None:
        directive["eol"] = eol
    # Provide enough lines for default head=1, tail=1
    block = Block(
        directive=directive,
        prefix="", suffix="", text="line1\nline2\n", line_number=1, name="test"
    )
    result = func(block)
    assert isinstance(result, tuple)
    assert expected_sep in result[0].text

def test_return_structure(tmp_path):
    (tmp_path / "valid.txt").write_text("imported")
    ctx = ImportBlockContext(import_path=str(tmp_path), open_delimiter="<", close_delimiter=">")
    func = make_import_block(ctx)
    # Provide enough lines for default head=1, tail=1
    block = Block(
        directive={"import": "valid.txt"},
        prefix="pre", suffix="suf", text="line1\nline2\n", line_number=10, name="myblock"
    )
    result = func(block)
    assert isinstance(result, tuple)
    assert len(result) == 3
    s, n_export, n_import = result
    assert isinstance(s, String)
    assert isinstance(n_export, Node)
    assert isinstance(n_import, Node)
    assert n_export.directive_type == "export"
    assert n_import.directive_type == "import"
    assert n_import.line_number == 10
```
<!-- {==} -->