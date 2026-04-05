import logging
from typing import Union

from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.stop import Stop
from syncspec.utilities import format_error


def make_source_directive(context: Context):
    def source_directive(directive: Directive) -> Union[Directive, Stop]:
        if "source" not in directive.parameters:
            return directive

        key = directive.parameters["source"]

        eof = directive.parameters.get("eof", False)
        if not isinstance(eof, bool):
            logging.error(format_error("'eof' must be a boolean.", directive.path, directive.prefix_line_number))
            return Stop()

        head = directive.parameters.get("head", 0)
        if not isinstance(head, int) or isinstance(head, bool):
            logging.error(format_error("'head' must be an integer.", directive.path, directive.prefix_line_number))
            return Stop()

        tail = directive.parameters.get("tail", 0)
        if not isinstance(tail, int) or isinstance(tail, bool):
            logging.error(format_error("'tail' must be an integer.", directive.path, directive.prefix_line_number))
            return Stop()

        output = directive.text
        lines = output.splitlines(keepends=True)
        num_lines = len(lines)

        if head + tail > num_lines:
            logging.error(format_error(
                f"head ({head}) + tail ({tail}) exceeds number of lines ({num_lines}).",
                directive.path, directive.prefix_line_number
            ))
            return Stop()

        trimmed = lines[head:]
        if tail > 0:
            trimmed = trimmed[:-tail]
        output = "".join(trimmed)

        if eof:
            output += "\n"

        if key in context.keyvalue:
            logging.warning(format_error(
                f"Key '{key}' already present in context.keyvalue. Overwriting.",
                directive.path, directive.prefix_line_number
            ))

        context.keyvalue[key] = output
        return directive

    return source_directive