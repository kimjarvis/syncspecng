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