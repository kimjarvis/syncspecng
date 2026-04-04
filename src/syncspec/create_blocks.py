import logging
from typing import Union, Tuple

from syncspec.context import Context
from syncspec.indexedfragment import IndexedFragment
from syncspec.text import Text
from syncspec.block import Block
from syncspec.stop import Stop
from syncspec.utilities import format_error

logger = logging.getLogger(__name__)

def make_create_blocks(context: Context):
    state = {'block': None, 'last': False}

    def create_blocks(fragment: IndexedFragment) -> Union[Text, Tuple[Text, Block], Stop, None]:
        if state["last"] and fragment.index % 4 != 0:
            logger.error(format_error(
                "Expected fragment index to be a multiple of 4 when last flag is active.",
                fragment.path,
                fragment.line_number
            ))
            return Stop()

        idx_mod = fragment.index % 4

        if fragment.index == 0:
            return Text(
                path=fragment.path,
                text=fragment.text,
                line_number=fragment.line_number
            )

        if idx_mod == 0:
            return (
                Text(path=fragment.path, text=fragment.text, line_number=fragment.line_number),
                state["block"]
            )
        elif idx_mod == 1:
            state["block"] = Block(
                prefix=fragment.text,
                text="",
                suffix="",
                path=fragment.path,
                prefix_line_number=fragment.line_number,
                text_line_number=0,
                suffix_line_number=0
            )
            return None
        elif idx_mod == 2:
            state["block"].text = fragment.text
            state["block"].text_line_number = fragment.line_number
            state["block"].path = fragment.path
            return None
        elif idx_mod == 3:  # Spec listed 2 twice; corrected to 3
            state["block"].suffix = fragment.text
            state["block"].suffix_line_number = fragment.line_number
            state["block"].path = fragment.path
            return None

        return None

    return create_blocks