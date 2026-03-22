# Add Graph Edges 

## Functional specification

<!-- {="import": "src/syncspec/graph_node.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass

@dataclass
class GraphNode:
    directive_type: str
    key: str
    line_number: int
    name: str

```
<!-- {==} -->

<!-- {="import": "src/syncspec/add_graph_edges_context.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass, field
from typing import Any, Dict
import networkx as nx

@dataclass
class AddGraphEdgesContext:
	G: nx.DiGraph
```
<!-- {==} -->

Do not generate code to initialise the context.
### Implement the unary function Graph Edges

In the file `src/syncspec/add_graph_edges.py`.

Define a closure factory with a unary function with signature:

<!-- {="source": "signature:add_graph_edges", "head": 2, "tail": 2=} -->
```python
def make_add_graph_edges(context: AddGraphEdgesContext):	
	def add_graph_edges() -> None

```
<!-- {==} -->

Add edges to the graph G.

Iterate through all nodes, for each node:

Let the node name be `from_node`.

If the node has attribute `directive_type` equal to "include":
- Let `key` be the attribute `key`.
- Search the graph for nodes with attribute `directive_type` equal to "source" and matching attribute `key`.   For each matching node:
	- Let the name of the matching node be `to_node` .
	- Create a directed edge from the `from_node` to the `to_node`.

If the node has attribute `directive_type` equal to "import":
- Let `key` be the attribute `key`.
- Search the graph for all nodes with attribute `directive_type` equal to "export" and matching attribute `key`.  For each matching node:
	- Let the name of the matching node be `to_node` .
	- Create a directed edge from the `from_node` to the `to_node`.

###  Note that

- Nodes have attributes `directive_type`, `file_name`, `line_number`, `key`.
- The node names are constructed from their attributes `directive_type + "_" + file_name + "_" + line_number`.
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

<!-- {= "include": "package", "head": 1, "tail": 1 =} -->
## Package

- The function is part of the python package `src/syncspec` .   
- Imports from the package take the form `from src.syncspec.x import X`.
- Assume Python version 3.7.

<!-- {==} -->
## Test the unary function  

In the file `tests/test_add_graph_edges.py`.

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
