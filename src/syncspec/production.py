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