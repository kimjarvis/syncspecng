import logging
from pathlib import Path
from typing import Callable, Union

from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.stop import Stop
from syncspec.utilities import format_error


def make_import_directive(context: Context) -> Callable[[Directive], Union[Directive, Stop]]:
    def import_directive(directive: Directive) -> Union[Directive, Stop]:
        if "import" not in directive.parameters:
            return directive

        try:
            import_rel = directive.parameters["import"]
            base_path = Path(context.import_path_prefix).resolve()
            target_path = (base_path / import_rel).resolve()

            # Path traversal & symlink target check
            try:
                target_path.relative_to(base_path)
            except ValueError:
                raise ValueError("File or symlink target escapes import prefix.")

            if not target_path.exists():
                raise FileNotFoundError(f"File not found: {target_path}")
            if not target_path.is_file():
                raise ValueError(f"Path is not a file: {target_path}")

            # Read as text (assumes UTF-8)
            file_content = target_path.read_text(encoding="utf-8")

            # Validate & apply 'eof'
            eof_val = directive.parameters.get("eof", False)
            if not isinstance(eof_val, bool):
                raise TypeError("'eof' must be a boolean.")
            if eof_val:
                file_content += "\n"

            # Validate & apply 'head'
            head_val = directive.parameters.get("head", 0)
            if not isinstance(head_val, int) or isinstance(head_val, bool):
                raise TypeError("'head' must be an integer.")

            # Validate & apply 'tail'
            tail_val = directive.parameters.get("tail", 0)
            if not isinstance(tail_val, int) or isinstance(tail_val, bool):
                raise TypeError("'tail' must be an integer.")

            # Split & validate line counts
            lines = directive.text.splitlines(keepends=True)
            if head_val + tail_val > len(lines):
                raise ValueError(f"head + tail ({head_val + tail_val}) exceeds available lines ({len(lines)}).")

            top = "".join(lines[:head_val])
            bottom = "".join(lines[-tail_val:]) if tail_val else ""

            # Replace directive text (variable 'in' renamed to avoid syntax error)
            directive.text = top + file_content + bottom
            return directive

        except Exception as exc:
            logging.error(format_error(str(exc), directive.path, directive.prefix_line_number))
            return Stop()

    return import_directive