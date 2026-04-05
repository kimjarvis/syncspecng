## Import 

Import `Context` from file `context.py`

<!-- {- import="src/syncspec/context.py",  head=2,  tail=2,  eof=True -} -->
```python
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Context:
    open_delimiter: str
    close_delimiter: str
    keyvalue_file: str
    keyvalue: dict
    input_path: str
    import_path_prefix: str
    export_path_prefix: str
    output_path_prefix: str
```
<!-- {--} -->

<!-- {- import="src/syncspec/block.py",  head=2,  tail=2,  eof=True -} -->
```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Block:
    prefix: str
    text: str
    suffix: str
    path: Path
    prefix_line_number: int
    text_line_number: int
    suffix_line_number: int
```
<!-- {--} -->


<!-- {- import="src/syncspec/indexedfragment.py", head=2, tail=2, eof=True -} -->
```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class IndexedFragment:
    path: Path
    text: str
    line_number: int
    index: int
```
<!-- {--} -->

<!-- {- import="src/syncspec/text.py", head=2, tail=2, eof=True -} -->
```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Text:
    path: Path
    text: str
    line_number: int
```
<!-- {--} -->


<!-- {- import="src/syncspec/stop.py", head=2, tail=2, eof=True -} -->
```python
from dataclasses import dataclass

@dataclass
class Stop:
    pass

```
<!-- {--} -->
## Implement a unary function

In the file `src/syncspec/create_blocks.py`.

Define a closure factory with a unary function with signature:

<!-- {- source="create_blocks",  head=1,  tail=1 -} -->
```python
def make_create_blocks(context: Context):
    state = {'block': None, 'last': False}
    def create_blocks(fragment: IndexedFragment) -> Union[Text,Tuple[Block,Text],Stop,None]:

```
<!-- {--} -->

`state["last"]` is set outside this function.  

- If `state["last"]==True` and `IndexedFragment.index` modulo 4 not equals 0:
	- Log an error with an informative message using `format_error.
	- Return an object of type `Stop`.  
- Otherwise
	- If `IndexedFragment.index` equals 0:
		- Return an object of type `Text`, copy fields from `IndexedFragment`.
	- Otherwise:
		- If `IndexedFragment.index` modulo 4 equals 0:
			- Return a tuple `Tuple[Block,Text]`.  With an object of type `Text`, copy fields from `IndexedFragment` and an object of type Block which shall be `state["block"]` .
		- If `IndexedFragment.index` modulo 4 equals 1: 
			- Create an object of type `Block` and set `state["block"]` 
			- `state["block"].prefix=IndexedFragment.text`
			- `state["block"].prefix_line_number=IndexedFragment.line_number`
			- `state["block"].path=IndexedFragment.path`
			- Return None
		- If `IndexedFragment.index` modulo 4 equals 2:
			- `state["block"].text=IndexedFragment.text`
			- `state["block"].text_line_number=IndexedFragment.line_number`
			- `state["block"].path=IndexedFragment.path`
			- Return None
		- If `IndexedFragment.index` modulo 4 equals 3:
			- `state["block"].suffix=IndexedFragment.text`
			- `state["block"].suffix_line_number=IndexedFragment.line_number`
			- `state["block"].path=IndexedFragment.path`
			- Return None
 
<!-- {-  include="format_error",  head=1,  tail=1 -} -->
## Log warnings and errors

Import logging.

Import the function with this signature from file `utilities.py`:
```python
from pathlib import Path
def format_error(message: str, path: Path, line_number: int) -> str:
```

<!-- {--} -->

<!-- {-  include="package",  head=1,  tail=1 -} -->
## Package

- The function is part of the python package `src/syncspec` .   
- Imports from the package take the form `from syncspec.x import X`.
- Assume Python version 3.9.

<!-- {--} -->

<!-- {-  include="generate_tests",  head=1,  tail=1 -} -->
## Write pytests to verify the functionality

- Write tests in a separate file.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

<!-- {--} -->

<!-- {-  include="explain_the_solution",  head=1,  tail=1 -} -->
## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.

<!-- {--} -->
