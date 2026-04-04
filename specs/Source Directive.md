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


<!-- {="import": "src/syncspec/directive.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Directive:
    parameters: dict
    prefix: str
    text: str
    suffix: str
    path: Path
    prefix_line_number: int
    text_line_number: int
    suffix_line_number: int
```
<!-- {==} -->

## Implement a unary function

In the file `src/syncspec/source_directive.py`.

Define a closure factory with a unary function with signature:

<!-- {="source": "source_directive", "head": 2, "tail": 2=} -->
```python
def make_source_directive(context: Context):
    def source_directive(directive: Directive) -> Directive:

```
<!-- {==} -->

- If dictionary `directive.parameters` contains the key "source" then:
	- The value shall be called the `key`.
	- Add the `key` to the `context.keyvalue` dictionary with value `directive.text`.
	- If the `key` is already present in the dictionary then:
		-  overwrite the value.
		- Log a warning with an informative message using `format_error.
	- Return the `Directive` object.
- Otherwise, return the `Directive` object.

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
