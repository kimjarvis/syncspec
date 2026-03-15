# Syncspec Text

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

Import this class from file `src/syncspec/syncspec_text_context.py`:
```python
from dataclasses import dataclass, field
from typing import Any, Dict
import networkx as nx

@dataclass
class SyncspecTextContext:
    open_delimiter: str
    close_delimiter: str
    log: str
    G: nx.DiGraph
    monad: Dict[str, Any]
    import_path: str
```

Do not generate code to initialise the context.

Verify context in function `make_syncspec_text`:
- open_delimiter and close_delimiter are not empty strings.
- G is a valid nx.DiGraph object.
- monad is a valid dictionary.
- import_path is a valid directory path.  The directory must exist.
### Implement the unary function Syncspec Text

In the file `src/syncspec/syncspec_text.py`.

Define a closure factory with a unary function with signature:

```python
def make_syncspec_text(context: SyncspecTextContext):
	def syncspec_text(text: Text) -> File
```

Modify this code to implement the function:

```python
    vtc = ValidateTextContext(
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
        line_number=1
    )
    ftc = FragmentTextContext(
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
        line_number=1
    )
    cbc = CreateBlocksContext(
        index=0,
        prefix="",
        text="",
        line_number=1,
    )
    sbc = SourceBlockContext(
        state=context.monad,
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
    )
    imbc = ImportBlockContext(
        import_path=context.import_path,
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
    )
    ibc = IncludeBlockContext(
        state=context.monad,
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
    )
    csc = CombineStringsContext(
        text="",
    )
    cec = CombineErrorsContext(
        text=context.log,
    )
    cnc = CombineNodesContext(
        G=context.G,
    )

    validate_text = make_validate_text(vtc)
    fragment_text = make_fragment_text(ftc)
    create_blocks = make_create_blocks(cbc)
    source_block = make_source_block(sbc)
    import_block = make_import_block(imbc)
    include_block = make_include_block(ibc)
    combine_strings = make_combine_strings(csc)
    combine_errors = make_combine_errors(cec)
    combine_nodes = make_combine_nodes(cnc)

    facts = [Text(name="freddy", text="""line 1
    {{"source": "a"}}A{{}}
    {{"source": "b"}}B{{}}
    line 2
    {{"include": "a"}}{{}} 
    {{"include": "b"}}{{}}
    line 3"""),
    ]

    rules = build_rules(
        [validate_text, fragment_text, create_blocks, source_block, import_block, include_block, combine_strings, combine_errors,
         combine_nodes])

	production(facts, rules)
```

- The contexts shall be initialised with values from `SyncspecTextContext`.  
- Context objects (csc, sbc, ibc, etc.) are instantiated once in the factory.  Subsequent calls to `syncspec_text` will carry over state.
- Use `SyncspecTextContext.log` to set `CombineErrorsContext.text`.
- Do not modify magic numbers, such as `index=0`.
- The parameter text shall replace the creation Text object, used to set facts.
- Return an object of type `File`, use the final value of `CombineStringsContext.text` and the parameter value `text.name`.
#### Implement a calling program

## Package

`src/syncspec` is a Python package.   Imports take the form `from src.syncspec.x import X`.
## Test the unary function  

In the file `tests/test_syncspec_text.py`.

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

Test an example call using this guidance:

Initialise the context suggestion:
```python
    open_delimiter = "{{"
    close_delimiter = "}}"
    log = "log.txt"
    G = nx.DiGraph()
	monad = {}
	import_path="."
```

Call the function with the Text object, with name "freddy", from the example.
Attach the `CombineStringsContext` to the context instance to allow access without modifying the dataclass definition.  
Assert that the `CombineStringsContext` object matches this pretty printed example.

```
CombineStringsContext(text='line 1\n'
                           '    {{"source": "a"}}A{{}}\n'
                           '    {{"source": "b"}}B{{}}\n'
                           '    line 2\n'
                           '    {{"include": "a"}}A{{}} \n'
                           '    {{"include": "b"}}B{{}}\n'
                           '    line 3')
```
## Package

`src/syncspec` is a Python package.   Imports take the form `from src.syncspec.x import X`.

Use the following imports:

```python
import pprint

import networkx as nx

from src.syncspec.combine_errors import make_combine_errors
from src.syncspec.combine_errors_context import CombineErrorsContext
from src.syncspec.combine_nodes import make_combine_nodes
from src.syncspec.combine_nodes_context import CombineNodesContext
from src.syncspec.combine_strings import make_combine_strings
from src.syncspec.combine_strings_context import CombineStringsContext
from src.syncspec.create_blocks import make_create_blocks
from src.syncspec.create_blocks_context import CreateBlocksContext
from src.syncspec.fragment_text import make_fragment_text
from src.syncspec.fragment_text_context import FragmentTextContext
from src.syncspec.include_block import make_include_block
from src.syncspec.include_block_context import IncludeBlockContext
from src.syncspec.production import build_rules, production
from src.syncspec.source_block import make_source_block
from src.syncspec.source_block_context import SourceBlockContext
from src.syncspec.text import Text
from src.syncspec.validate_text import make_validate_text
from src.syncspec.validate_text_context import ValidateTextContext
from src.syncspec.import_block import make_import_block
from src.syncspec.import_block_context import ImportBlockContext
```

## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.
