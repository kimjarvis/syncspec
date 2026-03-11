# Syncspec

## Functional specification

Import this class from file `src/syncspec/text.py`:
```python
from dataclasses import dataclass

@dataclass
class Text:
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
```

Do not generate code to initialise the context.

Use this code as a guideline. 

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


def main():
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

    # 2. Create Unary Function bound to context
    validate_text = make_validate_text(vtc)
    fragment_text = make_fragment_text(ftc)
    create_blocks = make_create_blocks(cbc)
    source_block = make_source_block(sbc)
    include_block = make_include_block(ibc)
    combine_strings = make_combine_strings(csc)
    combine_errors = make_combine_errors(cec)
    combine_nodes = make_combine_nodes(cnc)

    facts = [Text(name="freddy", text="""A{{"source": "first"}}C{{}}
    E{{"include": "first"}}{{}}I""")]

    # 3. Build Rules
    rules = build_rules(
        [validate_text, fragment_text, create_blocks, source_block, include_block, combine_strings, combine_errors,
         combine_nodes])

    # 4. Run Production (no context passed)
    result = production(facts, rules)
    pprint.pp(result)
    pprint.pp(monad)
    pprint.pp(csc)
    pprint.pp(cec)
    nx.drawing.nx_pydot.write_dot(cnc.G, "graph.dot")


if __name__ == "__main__":
    main()
```

### Implement the unary function Syncspec

In the file `src/syncspec/syncspec.py`.

Define a closure factory with a unary function with signature:

```python
def make_syncspec(context: SyncspecContext):
	def syncspec(text: List[Text]) -> List[Text]
```

- The context parameters are used to set the delimiters.
- The context objects are shared by each iteration.
- The production function applies rules to each Text object in the list.  
- The resulting text is gathered in `CombineStringsContext.text` 
- Logging information is collected in `CombineErrorsContext.text` it shall be written to the file `log_file`.
- The graph is collected in `CombineNodesContext` is shall be written to the file `graph_file`. 
- The function can assume that the file paths are valid. 
#### main

Generate a main function in file `main1.py` the main function shall parse keyword parameters:
`--open_delimiter` with default "{{"
`--close_delimiter` with default "}}"
`--log_file` with default "log.txt"
`--graph_file` with default "graph.dot"
`--output` required.   
And required positional parameter `path`  

#### Validate the parameters

- `--log_file` must be a valid file path.  The file should not exist.
- `--graph_file` must be a valid file path.  The file suffix must be `.dot`  . The file should not exist.
- Verify that output is a path to an existing directory.
- Verify that path is a path to an existing directory.

Print an informative error message and stop if verification fails.

Construct the syncspec context from the parameters.

Traverse the directory `path` recursively.  For each markdown  `.md` file encountered create an object of type `Text` and add it to a list.  `Text.text` shall be the file content.  `Text.name` shall be the file path relative to `path`.

Pass the list of `Text` objects to `syncspec`.   A list of `Text` objects shall be returned.

Iterate through the returned `Text` objects.   Create a file containing `Text.text` on the file path constructed from `output` + `/` + `Text.name`.
## Package

`src/syncspec` is a Python package.   Imports take the form `from src.syncspec.x import X`.
## Test the unary function  

In the file `tests/test_syncspec.py`.

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  
## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.



