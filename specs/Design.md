
<!-- {="include": "validate_context", "head": 2, "tail": 2=} -->
```python
def make_validate_context(context: Context):
	state = {'active': True}
    def validate_context(fact: Dummy) -> Union[Dummy, Stop]:    def validate_context(fact: Dummy) -> Union[Dummy, Stop]:    def validate_context(fact: Dummy) -> Union[Dummy, Stop]:    def validate_context(fact: Dummy) -> Union[Dummy, Stop]:```
<!-- {==} -->


<!-- {="include": "traverse_path", "head": 2, "tail": 2=} -->
```python
def make_traverse_path(context: Context):
    def traverse_path(fact: Dummy) -> Union[FilePath, Stop]:    def traverse_path(fact: Dummy) -> Union[FilePath, Stop]:    def traverse_path(fact: Dummy) -> Union[FilePath, Stop]:    def traverse_path(fact: Dummy) -> Union[FilePath, Stop]:```
<!-- {==} -->


<!-- {="include": "fragment_text", "head": 2, "tail": 2=} -->
```python
def make_fragment_text(context: Context):
    def fragment_text(fact: FilePath) -> Union[List[Fragment],Stop]:    def fragment_text(fact: FilePath) -> Union[List[Fragment],Stop]:    def fragment_text(fact: FilePath) -> Union[List[Fragment],Stop]:    def fragment_text(fact: FilePath) -> List[Fragment]:```
<!-- {==} -->