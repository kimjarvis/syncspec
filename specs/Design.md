# Design

### [[Validate Text]]  

Perform validation.

<!-- {= "include": "signature:validate_text", "head": 2, "tail": 2 =} -->
```python
def make_validate_text(context: ValidateTextContext):
    def validate_text(text: Text) -> Union[ValidatedText, String]:
```
<!-- {==} -->
### [[Fragment Text]]

Returns Fragment objects.

<!-- {= "include": "signature:fragment_text", "head": 2, "tail": 2 =} -->
```python
def make_fragment_text(context: FragmentTextContext):
    def fragment_text(text: ValidatedText) -> List[Fragment]:
```
<!-- {==} -->
### [[Create Blocks]]

Returns objects of  types, String, Block.

<!-- {= "include": "signature:create_blocks", "head": 2, "tail": 2 =} -->
```python
def make_create_blocks(context: CreateBlocksContext):	
	def create_blocks(fragment: Fragment) -> Union[Block, String, None]:
```
<!-- {==} -->
### [[Source Block]]

Populate the dictionary from blocks of type source.  Converts a block of type Source into a String.

<!-- {= "include": "signature:source_block", "head": 2, "tail": 2 =} -->
```python
def make_source_block(context: SourceBlockContext):	
	def source_block(block: Block) -> Union[Tuple[String, Node], Block, String]:
```
<!-- {==} -->
### [[Include Block]]

Use the dictionary to look up a key.  Converts a block of type Include into a String.

<!-- {= "include": "signature:include_block", "head": 2, "tail": 2 =} -->
```python
def make_include_block(context: IncludeBlockContext):	
	def include_block(block: Block) -> Union[Tuple[String, Node], Block, String]:
```
<!-- {==} -->
### [[Import Block]]

Create blocks of type String from files.

<!-- {= "include": "signature:import_block", "head": 2, "tail": 2 =} -->
```python
def make_import_block(context: ImportBlockContext):	
	def import_block(block: Block) -> Union[Tuple[String, Node, Node], Block, String]:
```
<!-- {==} -->
### [[Combine Strings]]

Combines the Strings to produce the output text.

<!-- {= "include": "signature:combine_strings", "head": 2, "tail": 2 =} -->
```python
def make_combine_strings(context: CombineStringsContext):	
	def combine_strings(string: String) -> None
```
<!-- {==} -->
### [[Add Graph Nodes]]

Create graph nodes.

<!-- {= "include": "signature:add_graph_nodes", "head": 2, "tail": 2 =} -->
```python
def make_add_graph_nodes(context: AddGraphNodesContext):	
	def add_graph_nodes(node: Node) -> GraphNode
```
<!-- {==} -->
### [[Add Graph Edges]]

Add edges to make a graph.

<!-- {= "include": "signature:add_graph_edges", "head": 2, "tail": 2 =} -->
```python
def make_add_graph_edges(context: AddGraphEdgesContext):	
	def add_graph_edges() -> None
```
<!-- {==} -->
### [[Syncspec Text]]

Process a single file.

<!-- {= "include": "signature:syncspec_text", "head": 2, "tail": 2 =} -->
```python
def make_syncspec_text(context: SyncspecTextContext):
	def syncspec_text(text: Text) -> File
```
<!-- {==} -->
### [[Syncspec List]]

Process a list of files.
### [[Syncspec CLI]]

The command line interface
