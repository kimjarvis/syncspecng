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


<!-- {- import="src/syncspec/directive.py",  head=2,  tail=2,  eof=True -} -->
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
<!-- {--} -->


<!-- {- import="src/syncspec/stop.py",  head=2,  tail=2,  eof=True -} -->
```python
from dataclasses import dataclass

@dataclass
class Stop:
    pass

```
<!-- {--} -->

## Implement a unary function

In the file `src/syncspec/source_directive.py`.

Define a closure factory with a unary function with signature:

<!-- {- source="source_directive",  head=2,  tail=2 -} -->
```python
def make_source_directive(context: Context):
    def source_directive(directive: Directive) -> Directive:

```
<!-- {--} -->

- If dictionary `directive.parameters` contains the key "source" then:
	- The value shall be called the `key`.
	- If dictionary `directive.parameters` contains the key "eof" then:
		- Ensure that:
			- The value is an boolean call it `eof`.
	- Otherwise, `eof=False`.
	- If dictionary `directive.parameters` contains the key "head" then:
		- Ensure that:
			- The value is an integer call it `head`.
	- Otherwise, `head=0`
	- If dictionary `directive.parameters` contains the key "tail" then:
		- Ensure that:
			- The value is an integer call it `tail`.
	- Otherwise, `tail=0`
	- Ensure that `head + tail` lines could be removed from `Directive.text`, an result is allowed.
	- Copy `Directive.text` to variable `output`
	- Ensure that:
		-  `head + tail <=`  the number of lines in variable `output` .
	- Trim the first `head` lines and the last `tail` lines from variable  `output` 
	- If `eof` is True then add an end of line, `\n`,  character to the end of variable `output`.
	- Add the `key` to the `context.keyvalue` dictionary with value equal to the variable `output`.
	- If the `key` is already present in the dictionary then:
		- Overwrite the value.
		- Log a warning with an informative message using `format_error`.
		- Use the `prefix_line_number`.
	- Return the `Directive` object.
	- When any of the ensured conditions are violated:
		- Log an error with an informative message using `format_error`.
		- Use the `prefix_line_number`.
		- Return an object of type `Stop` . 
- Otherwise, return the `Directive` object.

Assume that:

- Directive.text uses standard newline characters. `splitlines(keepends=True)` safely handles `\n, \r\n, and \r`.
- `context.keyvalue` is a standard mutable dictionary.
- `format_error` is purely for message formatting; actual logging is handled via logging.

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
