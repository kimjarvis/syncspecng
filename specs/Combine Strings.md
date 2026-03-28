# Combine Strings 

<!-- {="import": "src/syncspec/input_file_parameter.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass

@dataclass
class InputFileParameter:
    text: str
    file: str
```
<!-- {==} -->

<!-- {="import": "src/syncspec/output_file_parameter.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass

@dataclass
class OutputFileParameter:
    text: str
    file: str
```
<!-- {==} -->

<!-- {="import": "src/syncspec/combine_strings_context.py", "head": 2, "tail": 2=} -->
```python
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class CombineStringsContext:
    text: str
```
<!-- {==} -->

Do not generate code to initialise the context.
The attribute `last` may be added to the context.
### Implement a unary function

In the file `src/syncspec/combine_strings.py`.

Define a closure factory with a unary function with signature:

<!-- {="source": "signature:combine_strings", "head": 2, "tail": 2=} -->
```python
def make_combine_strings(context: CombineStringsContext):	
	def combine_strings(fact: InputFileParameter) -> OutputFileParameter

```
<!-- {==} -->

 - Append `fact.text` to the end of string `context.text`.
 - Copy the fields in `fact` to the returned object. 

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
