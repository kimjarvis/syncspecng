# CLI

### Implement a command line interface

Parse keyword parameters:
`--open_delimiter` with default "{{".
`--close_delimiter` with default "}}".
`--log_file` if specified, this must be a valid file path.  The file suffix must be `.log`.  
`--keyvalue_file` Required,  this must be a valid file path.  The file suffix must be `.json`.
Required positional parameter `file` .  This must be a path to an existing file with suffix `.md`.

### Set up Python logging:

- If `--log_file` is specified log to this file.  Otherwise, log to the console.
- Use basic configuration with format `"%(levelname)s - %(message)s"`.  
- Set the log level to warning.
## Core Components

#### Initialise the dictionary

Initialise a dictionary.
#### Create an object containing the input file

Instantiate an object of type:

<!-- {="import": "src/syncspec/input_file_parameter.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass

@dataclass
class InputFileParameter:
    text: str
    file: str
```
<!-- {==} -->

Read the file `file` into the text field and set the file field to the file path `file`.

#### Create an object containing the dictionary

Instantiate an object of type:

<!-- {="import": "src/syncspec/input_dictionary_parameter.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass

@dataclass
class InputDictionaryParameter:
    dictionary: dict

```
<!-- {==} -->

Read the JSON file `keyvalue_file` into the dictionary.  If the file is not valid JSON, print an informative message to  `sys.stderr`  and `sys.exit(1)`.

#### Call the production machine

<!-- {="import": "src/syncspec/combine_strings_context.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class CombineStringsContext:
    text: str
```
<!-- {==} -->

The closure is defined in file `combine_strings`.

```
def make_combine_strings(context: CombineStringsContext):
    def combine_strings(fact: InputFileParameter) -> OutputFileParameter:
```

The production machine is defined in file `production`.  It defines two functions:

```python
def build_rules(rule_functions: Sequence[Callable[[Any], Any]]) -> List[Tuple[type, Callable[[Any], Any]]]:
```

```python
def production(facts: List[Any], rules: List[Tuple[type, Callable[[Any], Any]]]) -> List[Any]:
```

Call the production machine like this:

```python
	combine_strings_context = CombineStringsContext(text="")  
	combine_strings = make_combine_strings(combine_strings_context)

    rules = build_rules([
        combine_strings,
    ])

	initial_facts = [input_object, dictionary_object]
    final_facts = production(initial_facts, rules)
```

Iterate over the facts returned by the production function.   

For each item of type:

<!-- {="import": "src/syncspec/output_file_parameter.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass

@dataclass
class OutputFileParameter:
    text: str
    file: str
```
<!-- {==} -->

Write a file to the path in field file with the content of field text.   Overwrite the existing file content.

For each item of type:

<!-- {="import": "src/syncspec/output_dictionary_parameter.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass

@dataclass
class OutputDictionaryParameter:
    dictionary: dict

```
<!-- {==} -->

Convert the dictionary to JSON overwriting the file `keyvalue_file` .

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
