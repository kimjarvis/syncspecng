import inspect
import logging
from typing import Union

from syncspec.context import Context
from syncspec.dummy import Dummy
from syncspec.stop import Stop
from syncspec.utilities import format_error

logger = logging.getLogger(__name__)


def make_validate_context(context: Context):
    state = {'active': True, 'last': False}

    def validate_context(param: Dummy) -> Union[Dummy, Stop]:
        if not state['active']:
            return Stop()

        od, cd = context.open_delimiter, context.close_delimiter
        error = None

        if not od or not cd:
            error = "Delimiters cannot be empty"
        elif od == cd:
            error = "Delimiters must be distinct"
        elif od in cd or cd in od:
            error = "Delimiters cannot overlap structurally"
        elif '\n' in od or '\n' in cd:
            error = "Delimiters cannot contain newlines"

        if error:
            state['active'] = False
            logger.error(format_error(error, __name__, inspect.currentframe().f_lineno))
            return Stop()

        return Dummy()

    return validate_context