from syncspec.context import Context
from syncspec.production import production, build_rules

from syncspec.validate_context import make_validate_context
from syncspec.example_coroutine import make_example_coroutine
from syncspec.dummy import Dummy

def machine(context: Context) -> None:
    print(context)

    validate_context = make_validate_context(context)
    example_coroutine = make_example_coroutine(context)

    rules = build_rules([
        validate_context,
        example_coroutine,
    ])

    initial_facts = [Dummy(),Dummy()]
    final_facts = production(initial_facts, rules)
    pass