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

## Implement a unary function

In the file `src/syncspec/validate_context.py`.

Define a closure factory with a unary function with signature:

<!-- {="source": "validate_context", "head": 2, "tail": 2=} -->
```python
def make_validate_context(context: Context):
	state = {'active': True}
    def validate_context(fact: Dummy) -> Union[Dummy, Stop]:
```
<!-- {==} -->

If `state["active"]==False`:
- Return an object of type `Stop`.  

Otherwise:

Verify that:

<!-- {="source": "delimiter assumptions", "head": 2, "tail": 2=} -->
- Delimiters are not empty strings.
- Delimiters are distinct, e.g., they will not be `{{` and `{{`.
- Delimiters do not overlap structurally.  Open cannot be a sub-string of close and vice versa. e.g., they will not be `{{` and `{`. 
- Delimiters do not contain newlines.
<!-- {==} -->

If verification fails:
- Do not raise an exception.
- Set `state["active"]=False`
- Log an error with an informative message using `format_error.
- Return an object of type `Stop`.  

If verification succeeds:
- Return an object of type `Dummy`.
### Note that

State is modified by an external process. 

<!-- {= "source": "format_error", "head": 1, "tail": 1 =} -->
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
