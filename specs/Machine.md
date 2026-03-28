
<!-- {="import": "src/syncspec/production.py", "head": 2, "tail": 2=} -->
```python
import inspect
from typing import Any, Callable, List, Sequence, Tuple, get_type_hints

def build_rules(rule_functions: Sequence[Callable[[Any], Any]]) -> List[Tuple[type, Callable[[Any], Any]]]:
    return [
        (get_type_hints(fn).get(next(iter(inspect.signature(fn).parameters)), object), fn)
        for fn in rule_functions
    ]

def production(facts: List[Any], rules: List[Tuple[type, Callable[[Any], Any]]]) -> List[Any]:
    print(facts)
    for rule_type, fn in rules:
        new_facts: List[Any] = []
        for fact in facts:
            if isinstance(fact, rule_type):
                res = fn(fact)
                new_facts.extend(res) if isinstance(res, (list, tuple)) else new_facts.append(res)
            else:
                new_facts.append(fact)
        facts = new_facts
        print(facts)
    return facts
```
<!-- {==} -->

<!-- {="import": "src/syncspec/example_coroutine.py", "head": 2, "tail": 2=} -->
```python
from syncspec.context import Context
from syncspec.dummy import Dummy

def make_example_coroutine(context: Context):
    state = {'index': 0, 'last': False}

    def example_coroutine(fact: Dummy) -> Dummy:
        state['index'] += 1
        print(state['index'])
        if state['last']:
            print("last")
        return Dummy()

    return example_coroutine
```
<!-- {==} -->

Modify `production` to set `state.last` to True when:

The fact is the last item, of its type, in the list of facts.   For example if the initial facts are:
`[Dummy(),Freddy(),Dummy()]` Then `state.last==True` in the object of type Freddy and the last object of type Dummy in the list.  It is False in the first item of type Dummy.

This shall be done on each iteration of the loop through the rules.


<!-- {= "include": "explain_the_solution", "head": 1, "tail": 1 =} -->
## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.
<!-- {==} -->
