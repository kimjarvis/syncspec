# Combine Nodes 

## Functional specification

Import this class from file `src/syncspec/node.py`:
```python
from dataclasses import dataclass

@dataclass
class Node:
    directive_type: str
    key: str
    line_number: int    
    name: str
```

Import this class from file `src/syncspec/combine_nodes_context.py`:
```python
from dataclasses import dataclass, field
from typing import Any, Dict
import networkx as nx

@dataclass
class CombineNodesContext:
	G: nx.DiGraph
```

Do not generate code to initialise the context.
### Implement the unary function Combine Nodes

In the file `src/syncspec/combine_nodes.py`.

Define a closure factory with a unary function with signature:

```python
def make_combine_nodes(context: CombineNodesContext):	
	def combine_nodes(node: Node) -> None
```


If `node.directive_type` equals "source" then:

Add a new node to the graph G in the context.
- The node shall be named `node.name + "_" + node.line_number`
- Add an attribute key with value `node.key`
- Add an attribute directive_type with value `node.directive_type`
- The node label shall be formatted as  `node.name + "\n" + node.line_number`
- The nodes shall be light blue rectangles.

If `node.directive_type` equals "include" then:

Search for matching source nodes before adding the new node, then add the new node and edges.

Search the graph for any matching nodes with the attribute key equal to `node.key`  and attribute directive_type with value "source".  

Add a new node to the graph G in the context.  The include node shall formatted in a similar to the source nodes.  Except:
- The include nodes shall be light green rectangles.

Add edges to the graph G.
- Create directed edges from the the matching nodes found by the search to the newly added node.
- The edge label shall be the matching `node.key`.
#### Assume that:

The networkx digraph will be rendered as a graphviz dot file.
## Package

`src/syncspec` is a Python package.   Imports take the form `from src.syncspec.x import X`.
## Test the unary function  

In the file `tests/test_combine_nodes.py`.

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.
