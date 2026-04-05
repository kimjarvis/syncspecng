<!-- {- include="validate_context", head=1, tail=1 -} -->
```python
def make_validate_context(context: Context):
	state = {'active': True}
    def validate_context(fact: Dummy) -> Union[Dummy, Stop]:

```
<!-- {--} -->

<!-- {- include="traverse_path", head=1, tail=1 -} -->
```python
def make_traverse_path(context: Context):
    def traverse_path(fact: Dummy) -> Union[List[Union[FilePath,Stop]], Stop]:

```
<!-- {--} -->

<!-- {- include="fragment_text", head=1, tail=1 -} -->
```python
def make_fragment_text(context: Context):
    def fragment_text(fact: FilePath) -> Union[List[Fragment],Stop]:

```
<!-- {--} -->

<!-- {- include="index_fragments", head=1, tail=1 -} -->
```python
def make_index_fragments(context: Context):
    state = {'index': 0, 'path': None}
    def index_fragments(fragment: Fragment) -> IndexedFragment:

```
<!-- {--} -->

<!-- {- include="create_blocks", head=1, tail=1 -} -->
```python
def make_create_blocks(context: Context):
    state = {'block': None, 'last': False}
    def create_blocks(fragment: IndexedFragment) -> Union[Text,Tuple[Block,Text],Stop,None]:

```
<!-- {--} -->

<!-- {- include="create_directives", head=1, tail=1 -} -->
```python
def make_create_directives(context: Context):
    def create_directives(block: Block) -> Union[Directive,Stop]:

```
<!-- {--} -->

<!-- {- include="import_directive", head=1, tail=1 -} -->
```python
def make_import_directive(context: Context):
    def import_directive(directive: Directive) -> Union[Directive,Stop]:

```
<!-- {--} -->

<!-- {- include="include_directive", head=1, tail=1 -} -->
```python
def make_include_directive(context: Context):
    def include_directive(directive: Directive) -> Directive:

```
<!-- {--} -->

<!-- {- include="reassemble_text", head=1, tail=1 -} -->
```python
def make_reassemble_text(context: Context):
    def reassemble_text(directive: Directive) -> Text:
```
<!-- {--} -->
