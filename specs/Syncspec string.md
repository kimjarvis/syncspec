# Syncspec String

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
### Implement the unary function Syncspec String

In the file `src/syncspec/syncspec_string.py`.

Define a closure factory with a unary function with signature:

```python
def make_syncspec_string(context: SyncspecStringContext):
	def syncspec_string(text: Text) -> File
```

Modify this code to implement the function:

```python
    vtc = ValidateTextContext(
        open_delimiter="{{",
        close_delimiter="}}",
        line_number=1
    )
    ftc = FragmentTextContext(
        open_delimiter="{{",
        close_delimiter="}}",
        line_number=1
    )
    cbc = CreateBlocksContext(
        index=0,
        prefix="",
        text="",
        line_number=1,
    )
    monad = {}
    sbc = SourceBlockContext(
        state=monad,
        open_delimiter="{{",
        close_delimiter="}}",
    )
    ibc = IncludeBlockContext(
        state=monad,
        open_delimiter="{{",
        close_delimiter="}}",
    )
    csc = CombineStringsContext(
        text="",
    )
    cec = CombineErrorsContext(
        text="",
    )
    graph = nx.DiGraph()
    cnc = CombineNodesContext(
        G=graph,
    )

    validate_text = make_validate_text(vtc)
    fragment_text = make_fragment_text(ftc)
    create_blocks = make_create_blocks(cbc)
    source_block = make_source_block(sbc)
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
        [validate_text, fragment_text, create_blocks, source_block, include_block, combine_strings, combine_errors,
         combine_nodes])

	production(facts, rules)
```

- The contexts shall be initialised with values from `SyncspecStringContext`.  
- Context objects (csc, sbc, ibc, etc.) are instantiated once in the factory.  Subsequent calls to `syncspec_string` will carry over state.
- Use `SyncspecStringContext.log` to set `CombineErrorsContext.text`.
- Do not modify magic numbers, such as `index=0`.
- The parameter text shall replace the creation Text object, used to set facts.
- Return an object of type `File`, use the final value of `CombineStringsContext.text` and the parameter value `text.name`.

#### Implement a calling program

Write a main program `main3.py` that calls `syncspec_string`.

Initialise the context with:

```
    open_delimiter = "{{"
    close_delimiter = "}}"
    log: ""
    G: nx.DiGraph()
	monad: {}
```

Call the function with the Text object, with name "freddy", from the example text.

Produce this diagnostic information after the program has run. 

```
    # Diagnostic information
    monad = context.monad
    cec = context.cec
    cnc = type('obj', (object,), {'G': context.G})()  # Wrapper to match diagnostic var name

    pprint.pp(result)
    pprint.pp(monad)
    pprint.pp(cec)
    nx.drawing.nx_pydot.write_dot(cnc.G, "graph.dot")
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
```

## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.
