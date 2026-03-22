### Implement a command line interface

In the file `syncspec-graph.py`.

Parse keyword parameters:
`--output` optional.
And required positional parameter `path`  
#### Validate the parameters

- `--output`  is a path to a file with a `.dot` suffix.  The file may or may not exist.  If it exists it will be overwritten.
- `path` is a path to an existing graphviz dot input file with a `.dot` suffix.  

Example file content:

```
strict digraph {
"export_lines.txt_0" [directive_type=export, key="lines.txt", line_number=0, file_name="lines.txt"];
"import_import.md_3" [directive_type=import, key="lines.txt", line_number=3, file_name="import.md"];
}
```

- Verify that the input file contains a valid digraph.  
- Verify that the input graph only contains nodes.  There are no edges.
- Verify that each node has string attributes `directive_type`, `file_name`, `key`.
- Verify that each node has attribute `line_number` which is, or converts to, an integer.
- Do not make any assumptions about the format of the node names.
## Add edges to the graph

Iterate through all nodes, for each node:

Let the node name be `to_node`.

If the node has attribute `directive_type` equal to "include":
- Let `key` be the attribute `key`.
- Search the graph for nodes with attribute `directive_type` equal to "source" and matching attribute `key`.   For each matching node:
	- Let the name of the matching node be `from_node` .
	- Create a directed edge pointing from the `from_node` to the `to_node`.
	- The edge shall have attributes:
		- The edge label shall be the `key`
		- Add an attribute `directive_type` equal to "include"
		- The edge colour shall be yellow.

If the node has attribute `directive_type` equal to "import":
- Let `key` be the attribute `key`.
- Search the graph for all nodes with attribute `directive_type` equal to "export" and matching attribute `key`.  For each matching node:
	- Let the name of the matching node be `from_node` .
	- Create a directed edge pointing from the `from_node` to the `to_node`.
	- The edge shall have attributes:
		- The edge label shall be the `key`
		- Add an attribute `directive_type` equal to "import"
		- The edge colour shall be red.
## Decorate the nodes

For each node in the graph:
- Set the shape to circle
- Set the node label to "line_number", using the attributes.
- If the directive type attribute is 'export' then:
	- set the fill colour to lightblue
- If the directive type attribute is 'source' then:
	- set the fill colour to lightblue
- If the directive type attribute is 'import' then:
	- set the fill colour to lightgreen
- If the directive type attribute is 'include' then:
	- set the fill colour to lightgreen
## Decorate the edges

For each node in the graph:
- An arrow points from the `from_node` to the `to_node`.
## Group the nodes

- Group graph nodes with the same `file_name` attribute. 
- Use Graphviz Sub-graphs to group nodes.

## Write the graph

If the `--output` parameter is specified: 
- Write the new graph to the output `.dot` file.    Overwrite the file if it already exists.
Otherwise 
- Overwrite the input  `.dot` file.    
### Note that

-  networkx.read_dot was removed in NetworkX 3.4+.  Use  pydot directly for I/O.
- Test graph content must contain `strict digraph`.
- Node names and attributes from pydot include quotes that need stripping.
- Edges added to the main pydot.Dot object must be properly serialized when nodes are in subgraphs.
### Assume that

- The networkx digraph will be rendered as a graphviz dot file.
- Packge pydot is installed.  
- Graphviz is installed.  
- Package networkx is installed.
- Files are UTF-8 encoded.

<!-- {= "include": "package", "head": 1, "tail": 1 =} -->
## Package

- The function is part of the python package `src/syncspec` .   
- Imports from the package take the form `from src.syncspec.x import X`.
- Assume Python version 3.7.

<!-- {==} -->
## Test the unary function  

In the file `tests/test_syncspec-graph.py`.

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
