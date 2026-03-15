# Graph Edges 

## Functional specification

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

Import this class from file `src/syncspec/graph_edges_context.py`:
```python
from dataclasses import dataclass, field
from typing import Any, Dict
import networkx as nx

@dataclass
class GraphEdgesContext:
	G: nx.DiGraph
```

Do not generate code to initialise the context.
### Implement the unary function Graph Edges

In the file `src/syncspec/graph_edges.py`.

Define a closure factory with a unary function with signature:

```python
def make_graph_edges(context: GraphEdgesContext):	
	def graph_edges(edge: Edge) -> None
```

Add edges to the graph G.

If the node has attribute `directive_type` equal to "include":
- Let key be the attribute `key`.
- Search the graph for nodes with attribute `directive_type` equal to "source" and matching attribute `key`.
- Create a directed edges from nodes with type "source" to nodes with type "include".

If the node has attribute `directive_type` equal to "import":
- Let key be the attribute `key`.
- Search the graph for nodes with attribute `directive_type` equal to "export" and matching attribute `key`.
- Create a directed edges from nodes with type "export" to nodes with type "import".
###  Note that

- Nodes have attributes `directive_type`, `name`, `line_number`, `key`.
- The node names are constructed from their attributes `directive_type + "_" + name + "_" + line_number`.
- The graph already contain all relevant nodes.
- The function adds only edges to the graph.
- Snapshot nodes to avoid Runtime Errors during graph mutation.  Iterate with data to access attributes directly using:

```python
	    nodes = list(context.G.nodes(data=True))
        for node_id, attrs in nodes:
```
### Assume that

- The networkx digraph will be rendered as a graphviz dot file.
- Packge pydot is installed.  
- Graphviz is installed.  
- Package networkx is installed.
## Package

`src/syncspec` is a Python package.   Imports take the form `from src.syncspec.x import X`.
## Test the unary function  

In the file `tests/test_graph_edges.py`.

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  
## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.
