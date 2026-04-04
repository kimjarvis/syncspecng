from syncspec.context import Context
from syncspec.text import Text


def make_defragment_text(context: Context):
    state = {'path': None, 'text': "", 'last': False}

    def defragment_text(text: Text) -> None:
        # Flush previous file when path changes (chunks are grouped by path)
        if state['path'] is not None and text.path != state['path']:
            state['path'].write_text(state['text'])
            state['text'] = ""

        state['path'] = text.path
        state['text'] += text.text

        # Final flush on last invocation
        if state['last']:
            state['path'].write_text(state['text'])
            state['text'] = ""

    return defragment_text