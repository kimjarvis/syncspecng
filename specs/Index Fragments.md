## Import 

Import `Context` from file `context.py`

<!-- {="import": "src/syncspec/context.py", "head": 2, "tail": 2=} -->
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
<!-- {==} -->

<!-- {="import": "src/syncspec/fragment.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Fragment:
    path: Path
    text: str
    line_number: int
```
<!-- {==} -->

<!-- {="import": "src/syncspec/indexedfragment.py", "head": 2, "tail": 2=} -->
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
<!-- {==} -->


<!-- {="import": "src/syncspec/stop.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass

@dataclass
class Stop:
    pass

```
<!-- {==} -->

## Implement a unary function

In the file `src/syncspec/index_fragments.py`.

Define a closure factory with a unary function with signature:

<!-- {="source": "index_fragments", "head": 2, "tail": 2=} -->
```python
def make_index_fragments(context: Context):
    state = {'index': 0, 'path': None}
    def index_fragments(fragment: Fragment) -> IndexedFragment:

```
<!-- {==} -->

Add a zero based index to fragments of the same file.

If  `state["path"]!=Fragment.path`  then:
- `state["index"]=0`
- `state["path"]=Fragment.path`

Copy the fields of `Fragment` to `IndexedFragment` and set `IndexedFragment.index=state["index"]`

Increment `state["index"]`

Return the `IndexedFragment`.

<!-- {= "include": "package", "head": 1, "tail": 1 =} -->
## Package

- The function is part of the python package `src/syncspec` .   
- Imports from the package take the form `from syncspec.x import X`.
- Assume Python version 3.9.
<!-- {==} -->

<!-- {= "include": "generate_tests", "head": 1, "tail": 1 =} -->
## Write pytests to verify the functionality

- Write tests in a separate file.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  
<!-- {==} -->

<!-- {= "include": "explain_the_solution", "head": 1, "tail": 1 =} -->
## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.
<!-- {==} -->
