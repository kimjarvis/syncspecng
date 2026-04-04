from syncspec.context import Context
from syncspec.production import production, build_rules
from syncspec.dummy import Dummy

from syncspec.validate_context import make_validate_context
from syncspec.example_coroutine import make_example_coroutine
from syncspec.traverse_path import make_traverse_path
from syncspec.fragment_text import make_fragment_text
from syncspec.index_fragments import make_index_fragments
from syncspec.create_blocks import make_create_blocks
from syncspec.create_directives import make_create_directives
from syncspec.import_directive import make_import_directive
from syncspec.reassemble_text import make_reassemble_text
from syncspec.defragment_text import make_defragment_text

def machine(context: Context) -> None:
    print("debug 00", context)

    validate_context = make_validate_context(context)
    # example_coroutine = make_example_coroutine(context)
    traverse_path = make_traverse_path(context)
    fragment_text = make_fragment_text(context)
    index_fragments = make_index_fragments(context)
    create_blocks = make_create_blocks(context)
    create_directives = make_create_directives(context)
    import_directive = make_import_directive(context)
    reassemble_text = make_reassemble_text(context)
    defragment_text = make_defragment_text(context)

    rules = build_rules([
        validate_context,
        # example_coroutine,
        traverse_path,
        fragment_text,
        index_fragments,
        create_blocks,
        create_directives,
        import_directive,
        reassemble_text,
        defragment_text
    ])

    initial_facts = [Dummy()]
    final_facts = production(initial_facts, rules)
    print("debug 01", final_facts)
    pass