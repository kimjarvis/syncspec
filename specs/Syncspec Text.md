# Syncspec Text

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

<!-- {="import": "src/syncspec/syncspec_text_context.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass, field
from typing import Any, Dict
import networkx as nx

@dataclass
class SyncspecTextContext:
    open_delimiter: str
    close_delimiter: str
    graph: nx.DiGraph
    monad: Dict[str, Any]
    import_path: str
```
<!-- {==} -->

Do not generate code to initialise the context.

Verify context in function `make_syncspec_text`:
- `open_delimiter` and `close_delimiter` are not empty strings.  Otherwise, raise a value error with message.
- `graph` is a valid `nx.DiGraph` object.  Otherwise, raise a type error.
- `monad` is a valid dictionary.  Otherwise, raise a type error.

### ### Implement a unary function

In the file `src/syncspec/syncspec_text.py`.

Define a closure factory with a unary function with signature:

<!-- {="source": "signature:syncspec_text", "head": 2, "tail": 2=} -->
```python
def make_syncspec_text(context: SyncspecTextContext):
	def syncspec_text(text: Text) -> File

```
<!-- {==} -->

Initialise each imported closure factory with context.
### [[Validate Text]]  

<!-- {= "include": "signature:validate_text", "head": 2, "tail": 2 =} -->
```python
def make_validate_text(context: ValidateTextContext):
    def validate_text(text: Text) -> Union[ValidatedText, String]:
```
<!-- {==} -->

```python
ValidateTextContext(
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
        line_number=1
)
```
### [[Fragment Text]]

<!-- {= "include": "signature:fragment_text", "head": 2, "tail": 2 =} -->
```python
def make_fragment_text(context: FragmentTextContext):
    def fragment_text(text: ValidatedText) -> List[Fragment]:
```
<!-- {==} -->

```python
FragmentTextContext(
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
        line_number=1
    )
```
### [[Create Blocks]]

<!-- {= "include": "signature:create_blocks", "head": 2, "tail": 2 =} -->
```python
def make_create_blocks(context: CreateBlocksContext):	
	def create_blocks(fragment: Fragment) -> Union[Block, String, None]:
```
<!-- {==} -->

```
CreateBlocksContext(
        index=0,
        prefix="",
        prefix_line_number=1,
        prefix_valid=False,
        directive={},
        text="",
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
    )
```

### [[Source Block]]

<!-- {= "include": "signature:source_block", "head": 2, "tail": 2 =} -->
```python
def make_source_block(context: SourceBlockContext):	
	def source_block(block: Block) -> Union[Tuple[String, Node], Block, String]:
```
<!-- {==} -->

```python
SourceBlockContext(
        state=context.monad,
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
    )
```
### [[Include Block]]

<!-- {= "include": "signature:include_block", "head": 2, "tail": 2 =} -->
```python
def make_include_block(context: IncludeBlockContext):	
	def include_block(block: Block) -> Union[Tuple[String, Node], Block, String]:
```
<!-- {==} -->

```python
IncludeBlockContext(
        state=context.monad,
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
    )
```
### [[Import Block]]

<!-- {= "include": "signature:import_block", "head": 2, "tail": 2 =} -->
```python
def make_import_block(context: ImportBlockContext):	
	def import_block(block: Block) -> Union[Tuple[String, Node, Node], Block, String]:
```
<!-- {==} -->

```python
ImportBlockContext(
        import_path=context.import_path,
        open_delimiter=context.open_delimiter,
        close_delimiter=context.close_delimiter,
    )
```
### [[Combine Strings]]

<!-- {= "include": "signature:combine_strings", "head": 2, "tail": 2 =} -->
```python
def make_combine_strings(context: CombineStringsContext):	
	def combine_strings(string: String) -> None
```
<!-- {==} -->

```python
CombineStringsContext(text="")
```
### [[Add Graph Nodes]]

<!-- {= "include": "signature:add_graph_nodes", "head": 2, "tail": 2 =} -->
```python
def make_add_graph_nodes(context: AddGraphNodesContext):	
	def add_graph_nodes(node: AddGraphNodesParameter) -> None
```
<!-- {==} -->

```python
AddGraphNodesContext(G=context.graph)
```

- Append each function, such as validate_text, to the list after creation.
- Construct the `build_rules`.
- Pass the rules to `production`.

```python
    rules = build_rules(
        [validate_text, 
        fragment_text, 
        create_blocks, 
        source_block, 
        import_block, 
        include_block, 
        combine_strings, 
        add_graph_nodes, 
        ])
	production(facts, rules)
```

- The contexts shall be initialised with values from `SyncspecTextContext`.  
- Context objects are instantiated once in the factory.  Subsequent calls to `syncspec_text` will carry over state.
- Do not modify magic numbers, such as `index=0`.
- The parameter text shall replace the creation Text object, used to set facts.
- Return an object of type `File`, use the final value of `CombineStringsContext.text` and the parameter value `text.name`.
#### Implement a calling program

## Package

`src/syncspec` is a Python package.   Imports take the form `from src.syncspec.x import X`.

All referenced modules (e.g., validate_text, fragment_text) exist in `src.syncspec` and export the specified factories and context classes.
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
    graph = nx.DiGraph()
	monad = {}
	import_path="."
```

Call the function with the Text object, with name "freddy", from this example.

```python
    facts = [Text(name="freddy", text="""line 1
    {{"source": "a"}}A{{}}
    {{"source": "b"}}B{{}}
    line 2
    {{"include": "a"}}{{}} 
    {{"include": "b"}}{{}}
    line 3"""),
    ]	
```

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

Follow this pattern to import closure factories and contexts.

```python
from src.syncspec.combine_strings import make_combine_strings
from src.syncspec.combine_strings_context import CombineStringsContext
```

Additionally, use the following imports:

```python
import pprint

import networkx as nx

from src.syncspec.production import build_rules, production
from src.syncspec.text import Text
```


!-- {= "include": "explain_the_solution", "head": 1, "tail": 1 =} -->
## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.

<!-- {==} -->
