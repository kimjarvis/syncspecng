from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.text import Text


def make_reassemble_text(context: Context):
    def reassemble_text(directive: Directive) -> Text:
        return Text(
            path=directive.path,
            line_number=directive.prefix_line_number,
            text=(
                f"{context.open_delimiter}"
                f"{directive.prefix}"
                f"{context.close_delimiter}"
                f"{directive.text}"
                f"{context.open_delimiter}"
                f"{directive.suffix}"
                f"{context.close_delimiter}"
            )
        )
    return reassemble_text