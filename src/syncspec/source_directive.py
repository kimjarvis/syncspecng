import logging
from typing import Callable

from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.utilities import format_error

logger = logging.getLogger(__name__)

def make_source_directive(context: Context) -> Callable[[Directive], Directive]:
    def source_directive(directive: Directive) -> Directive:
        if "source" in directive.parameters:
            key = directive.parameters["source"]
            if key in context.keyvalue:
                logger.warning(format_error(
                    f"Overwriting existing source key '{key}'.",
                    directive.path,
                    directive.prefix_line_number
                ))
            context.keyvalue[key] = directive.text
        return directive
    return source_directive