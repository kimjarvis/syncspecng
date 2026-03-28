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

<!-- {="import": "src/syncspec/dummy.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass

@dataclass
class Dummy:
    pass

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


<!-- {="import": "src/syncspec/file_path.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class FilePath:
    path: Path
    text: str

```
<!-- {==} -->

## Implement a unary function

In the file `src/syncspec/traverse_path.py`.

Define a closure factory with a unary function with signature:

<!-- {="source": "traverse_path", "head": 2, "tail": 2=} -->
```python
def make_traverse_path(context: Context):
    def traverse_path(fact: Dummy) -> Union[FilePath, Stop]:

```
<!-- {==} -->

Verify that `context.input_path` is a path to an existing directory.  

The path may be absolute or relative to the cwd.  When a relative path is given it can only reference the cwd or directories that are children of the cwd.

Recursively traverse the directory path `context.input_path`.    
- Do not follow links.

For each file with the extension `.md` :
- Read the file content into `FilePath.text` and set the path.

If directory traversal or reading fails:
- Do not raise an exception.
- Log an error with an informative message using `format_error.
- Return an object of type `Stop`.

If reading succeeds:
- Return an object of type `FilePath`.

<!-- {= "include": "format_error", "head": 1, "tail": 1 =} -->
## Log warnings and errors

Import logging.

Import the function with this signature from file `utilities.py`:
```python
from pathlib import Path
def format_error(message: str, path: Path, line_number: int) -> str:
```
<!-- {==} -->

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
