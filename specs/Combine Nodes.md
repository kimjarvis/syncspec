# Combine Nodes 

## Functional specification

Import this class from file `src/syncspec/node.py`:
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

Import this class from file `src/syncspec/edge.py`:
```python
from dataclasses import dataclass

@dataclass
class Edge:
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
	def combine_nodes(node: Node) -> Edge
```

If `node.directive_type` equals "source" or "export" then:

Add a new node to the graph G in the context.
- The node shall be named `type + "_" + node.name + "_" + node.line_number` where type is `node.directive_type`.
- Add an attribute key with value `node.key`
- Add an attribute directive_type with value `node.directive_type`
- The node label shall be formatted as  `type + "\n" + node.name + "\n" + ":" + node.line_number` where type is `node.directive_type`.
- The "source" nodes shall be light blue rectangles.  
- The "export" nodes shall be red rectangles.

If `node.directive_type` equals "include" or "import" then:

Add a new node to the graph G in the context.  The include node shall formatted in a similar to the source nodes.  Except:
- The "include" nodes shall be light green rectangles.
- The "import" nodes shall be yellow rectangles.

In all cases, return an object of type Edge.  Initialise the object with fields from `node`.
### Note that

- The function adds only nodes to the graph.
- Names are unique and collisions cannot occur.
### Assume that

- The networkx digraph will be rendered as a graphviz dot file.
- Packge pydot is installed.  
- Graphviz is installed.  
- Package networkx is installed.
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
