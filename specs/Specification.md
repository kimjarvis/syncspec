
<!-- {- include="cli_action" -} -->
## Command line interface

- Parse parameters.  
- Validate Parameters. 
- Create context. 
- Call machine function.
<!-- {--} -->
<!-- {- include="cli_spec" -} -->
Parse optional keyword parameters

`--open_delimiter` with default "{"+"-" (Two characters, open curly brace and minus sign).  Describe the default value.
`--close_delimiter` with default "-"+"}" (Two characters, minus sign and close curly brace). Describe the default value.
`--keyvalue` is a file path.  If specified, the file must exist.  The file suffix must be `.json`. 
`--ignore_rules` is a file path.  if specified, the file must exist. 

Required positional parameter:

1. `input_path`  this must be a valid directory path.

<!-- {--} -->
<!-- {- include="validate_context_action" -} -->
## Validate Context

- Set up Python logging
- Validate the delimiters
- Read JSON file
- Verify the ignore_rules file
- Return an object of type `Dummy`
<!-- {--} -->
<!-- {- include="validate_context_spec" -} -->
```python
def make_validate_context(context: Context):
    def validate_context(fact: Dummy) -> Union[Dummy, Stop]:
```
<!-- {--} -->
<!-- {- include="traverse_path_action" -} -->
### Traverse Path

Recursively walk through a directory, ignoring files and folders based on patterns from a specified ignore file.  Create an object for each target file encountered.

- Compile the ignore_rules file.
- Recursively traverse the directory path `context.input_path`.    
- Check the path.
- Return a list of objects of type `FilePath`, or an empty list no valid files are found.

<!-- {--} -->
<!-- {- include="traverse_path_spec" -} -->
```python
def make_traverse_path(context: Context):
    def traverse_path(fact: Dummy) -> Union[List[FilePath],Stop]:

```
<!-- {--} -->
<!-- {- include="fragment_text_action" -} -->
## Fragment Text

- Determine whether file is a target
- Decompose text into fragments using the delimiters.  
- Keep track of line numbers.
- Ensure delimiter semantics.
<!-- {--} -->
<!-- {- include="fragment_text_spec" -} -->
```python
def make_fragment_text(context: Context):
    def fragment_text(fact: FilePath) -> Union[List[Fragment],Stop]:
```
<!-- {--} -->
<!-- {- include="index_fragments_action" -} -->
## Index Fragments

Add a zero based index to fragments of the same file.
<!-- {--} -->
<!-- {- include="index_fragments_spec" -} -->
```python
def make_index_fragments(context: Context):
    state = {'index': 0, 'path': None}
    def index_fragments(fragment: Fragment) -> IndexedFragment:

```
<!-- {--} -->
<!-- {- include="create_blocks_action" -} -->
## Create Blocks

Create blocks from consecutive fragments of the same file.
<!-- {--} -->
<!-- {- include="create_blocks_spec" -} -->
```python
def make_create_blocks(context: Context):
    state = {'block': None, 'last': False}
    def create_blocks(fragment: IndexedFragment) -> Union[Text,Tuple[Block,Text],Stop,None]:

```
<!-- {--} -->
<!-- {- include="create_directives_action" -} -->
## Create Directives

1. Create an object of type `Directive` by coping the fields of `block`.
2. Populate the field `parmeters` dictionary using `string_to_keyvalue_dict(block.prefix)`.
3. Return the object.
<!-- {--} -->
<!-- {- include="create_directives_spec" -} -->
```python
def make_create_directives(context: Context):
    def create_directives(block: Block) -> Union[Directive,Stop]:

```
<!-- {--} -->
<!-- {- include="export_directive_action" -} -->
## Export Directive

- If the directive contains the key "export":
	- Export the file.
	- Return a new `Directive` object.
<!-- {--} -->
<!-- {- include="export_directive_spec" -} -->
```python
def make_export_directive(context: Context):
    def export_directive(directive: Directive) -> Union[Directive,Stop]:

```
<!-- {--} -->
<!-- {- include="import_directive_action" -} -->
## Import Directive

- If the directive contains the key "import":
	- Import the file.
	- Return a new `Directive` object.
<!-- {--} -->
<!-- {- include="import_directive_spec" -} -->
```python
def make_import_directive(context: Context):
    def import_directive(directive: Directive) -> Union[Directive,Stop]:

```
<!-- {--} -->
<!-- {- include="source_directive_action" -} -->
## Source Directive

- If the directive contains the key "source":
	- Add the source to the context key value dictionary.
	- Return `Directive` object.
<!-- {--} -->
<!-- {- include="source_directive_spec" -} -->
```python
def make_source_directive(context: Context):
    def source_directive(directive: Directive) -> Union[Directive,Stop]:

```
<!-- {--} -->
<!-- {- include="include_directive_action" -} -->
## Include Directive

- If the directive contains the key "include":
	- Include the text from the context key value dictionary.
	- Return a new `Directive` object.
<!-- {--} -->
<!-- {- include="include_directive_spec" -} -->
```python
def make_include_directive(context: Context):
    def include_directive(directive: Directive) -> Union[Directive,Stop]:

```
<!-- {--} -->
<!-- {- include="reassemble_text_action" -} -->
## Reassemble Text

Convert a Directive object into a Text object.
<!-- {--} -->

<!-- {- include="reassemble_text_spec" -} -->
```python
def make_reassemble_text(context: Context):
    def reassemble_text(directive: Directive) -> Text:
```
<!-- {--} -->
<!-- {- include="defragment_text_action" -} -->
## Defragment Text

Concatenate text fragments from the same file and write them to the file.

<!-- {--} -->
<!-- {- include="defragment_text_spec" -} -->
```python
def make_defragment_text(context: Context):
	state = {'path': None, 'text': "", 'last': False }
    def defragment_text(text: Text) -> Text:

```
<!-- {--} -->
<!-- {- include="write_keyfile_action" -} -->
## Write keyfile

Write the `keyvalue` dictionary to the `keyvalue_file` JSON file.
<!-- {--} -->
<!-- {- include="write_keyfile_spec" -} -->
```python
def make_write_keyfile(context: Context):
	state = {'last': False}
    def write_keyfile(text: Text) -> Union[Text, Stop]:
```
<!-- {--} -->
