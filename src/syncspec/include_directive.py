import logging
from typing import Union

from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.stop import Stop
from syncspec.utilities import format_error


def make_include_directive(context: Context):
    def include_directive(directive: Directive) -> Union[Directive, Stop]:
        if "include" not in directive.parameters:
            return directive

        key = directive.parameters["include"]

        if key not in context.keyvalue:
            logging.warning(format_error(f"Include key '{key}' not found in context.", directive.path, directive.text_line_number))
            return directive

        input_text = context.keyvalue[key]

        eof = directive.parameters.get("eof", False)
        if not isinstance(eof, bool):
            logging.error(format_error("Parameter 'eof' must be a boolean.", directive.path, directive.text_line_number))
            return Stop()
        if eof:
            input_text += "\n"

        head = directive.parameters.get("head", 0)
        if isinstance(head, bool) or not isinstance(head, int):
            logging.error(format_error("Parameter 'head' must be an integer.", directive.path, directive.text_line_number))
            return Stop()

        tail = directive.parameters.get("tail", 0)
        if isinstance(tail, bool) or not isinstance(tail, int):
            logging.error(format_error("Parameter 'tail' must be an integer.", directive.path, directive.text_line_number))
            return Stop()

        lines = directive.text.splitlines(keepends=True)
        if head + tail > len(lines):
            logging.error(format_error(f"head ({head}) + tail ({tail}) exceeds line count ({len(lines)}).", directive.path, directive.text_line_number))
            return Stop()

        top = "".join(lines[:head])
        bottom = "".join(lines[-tail:]) if tail else ""

        # Preserve line structure when replacing the middle section
        separator = "\n" if bottom and not input_text.endswith("\n") else ""
        directive.text = top + input_text + separator + bottom
        return directive

    return include_directive