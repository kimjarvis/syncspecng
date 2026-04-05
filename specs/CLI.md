# CLI

Implement a command line interface.  
### Parameters

Parse optional keyword parameters

`--open_delimiter` with default "{{".  Describe the default value.
`--close_delimiter` with default "}}". Describe the default value.
`--log_file` if specified, this must be a valid file path.  The file suffix must be `.log`.  

Required positional parameter:

1. `input_path`  this must be a valid directory path.

Optional  positional parameter:

2. `keyvalue_file`, if specified the file must exist and the file suffix must be `.json`.  

If verification fails, print an informative message to  `sys.stderr`  and `sys.exit(1)`.

Use `argsparse`.  The `--help` message shall print an explanation of the parameters.
### Set up Python logging:

- If `--log_file` is specified log to this file.  Otherwise, log to the console.
- Use basic configuration with format `"%(levelname)s - %(message)s"`.  
- Set the log level to warning.

Clear any existing handlers, ensuring `basicConfig()` will create a new file handler when --`log_file` is specified.   Write an initial log message `logging.warning("CLI started")`  to guarantees the log file is created and written.
### Read JSON file

If the `keyvalue_file` parameter is specified:
- Read the JSON file  `keyvalue_file`  into a dictionary `keyvalue`.  
- If JSON validation fails: 
	- print an informative message to  `sys.stderr`  and `sys.exit(1)`.
### Create Context

Create an object from the parameter values.

- `output_path_prefix` shall be None
- `import_path_prefix` shall be None
- `export_path_prefix` shall be None
- If the `--keyvalue_file` parameter is not specified:
	- Set `keyvalue` to an empty dictionary,
	 
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

Import `machine`.

Call function with signature

```python
def machine(context: Context) -> None:
```
### Note 

- Note that `sys.exit(0)` raises a `SystemExit` exception.
- `logging.basicConfig()` only creates the file handler when a log message is actually written.

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
