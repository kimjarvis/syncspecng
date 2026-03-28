from syncspec.context import Context
from syncspec.production import production, build_rules
from syncspec.dummy import Dummy

from syncspec.validate_context import make_validate_context
from syncspec.example_coroutine import make_example_coroutine
from syncspec.traverse_path import make_traverse_path
from syncspec.fragment_text import make_fragment_text

def machine(context: Context) -> None:
    print(context)

    validate_context = make_validate_context(context)
    example_coroutine = make_example_coroutine(context)
    traverse_path = make_traverse_path(context)
    fragment_text = make_fragment_text(context)

    rules = build_rules([
        validate_context,
        example_coroutine,
        traverse_path,
        fragment_text,
    ])

    initial_facts = [Dummy()]
    final_facts = production(initial_facts, rules)
    pass