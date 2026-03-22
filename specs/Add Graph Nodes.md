# Add Graph Nodes 

## Functional specification

<!-- {="import": "src/syncspec/add_graph_nodes_parameter.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass

@dataclass
class AddGraphNodesParameter:
    directive_type: str
    key: str
    line_number: int
    name: str
```
<!-- {==} -->

<!-- {= "import": "src/syncspec/add_graph_nodes_context.py", "head": 2, "tail": 2 =} -->
```python
from dataclasses import dataclass, field
from typing import Any, Dict
import networkx as nx

@dataclass
class AddGraphNodesContext:
	G: nx.DiGraph
```
<!-- {==} -->

Do not generate code to initialise the context.
### Implement a unary function

In the file `src/syncspec/add_graph_nodes.py`.

Define a closure factory with a unary function with signature:

<!-- {= "source": "signature:add_graph_nodes", "head": 2, "tail": 2 =} -->
```python
def make_add_graph_nodes(context: AddGraphNodesContext):	
	def add_graph_nodes(node: AddGraphNodesParameter) -> None

```
<!-- {==} -->

Add a new node to the graph G in the context.
- The node shall be named `type + "_" + node.name + "_" + node.line_number` where type is `node.directive_type`.
- Add an attribute `directive_type` with value `node.directive_type`
- Add an attribute `key` with value `node.key`
- Add an attribute `line_number` with value `node.line_number`
- Add an attribute `file_name` with value `node.name`.
### Note that

- The function adds only nodes to the graph.
- Names are unique and collisions cannot occur.
### Assume that

- Package networkx is installed.

<!-- {= "include": "package", "head": 1, "tail": 1 =} -->
## Package

- The function is part of the python package `src/syncspec` .   
- Imports from the package take the form `from src.syncspec.x import X`.
- Assume Python version 3.7.

<!-- {==} -->
## Test the unary function  

In the file `tests/test_add_graph_nodes.py`.

<!-- {= "include": "generate_tests", "head": 1, "tail": 1 =} -->

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

<!-- {==} -->

<!-- {= "include": "explain_the_solution", "head": 1, "tail": 1 =} -->
## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.

<!-- {==} -->

