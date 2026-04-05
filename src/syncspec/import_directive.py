import logging
import os
from dataclasses import replace
from pathlib import Path
from typing import Union

from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.stop import Stop
from syncspec.utilities import format_error


def make_import_directive(context: Context):
    def import_directive(directive: Directive) -> Union[Directive, Stop]:
        if "import" not in directive.parameters:
            return directive

        try:
            rel_path_str = directive.parameters["import"]
            base_dir = Path(context.input_path).resolve()
            raw_path = base_dir / rel_path_str
            resolved_path = raw_path.resolve()

            if not resolved_path.is_relative_to(base_dir):
                raise ValueError(f"Import path '{rel_path_str}' escapes the input directory.")
            if raw_path.is_symlink() and not resolved_path.is_relative_to(base_dir):
                raise ValueError(f"Symlink target for '{rel_path_str}' escapes the input directory.")
            if not resolved_path.exists():
                raise ValueError(f"File '{rel_path_str}' does not exist.")
            if not resolved_path.is_file():
                raise ValueError(f"'{rel_path_str}' is not a regular file.")
            if not os.access(resolved_path, os.R_OK):
                raise ValueError(f"File '{rel_path_str}' is not readable.")

            try:
                with open(resolved_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                raise ValueError(f"'{rel_path_str}' is not a valid text file.")

            eof = False
            if "eof" in directive.parameters:
                eof = directive.parameters["eof"]
                if not isinstance(eof, bool):
                    raise ValueError("Parameter 'eof' must be a boolean.")
            if eof:
                content += "\n"

            head = 0
            if "head" in directive.parameters:
                head = directive.parameters["head"]
                if not isinstance(head, int) or isinstance(head, bool):
                    raise ValueError("Parameter 'head' must be an integer.")

            tail = 0
            if "tail" in directive.parameters:
                tail = directive.parameters["tail"]
                if not isinstance(tail, int) or isinstance(tail, bool):
                    raise ValueError("Parameter 'tail' must be an integer.")

            lines = directive.text.splitlines(keepends=True)
            if head + tail > len(lines):
                raise ValueError(
                    f"head ({head}) + tail ({tail}) exceeds line count ({len(lines)})."
                )

            top = "".join(lines[:head])
            bottom = "".join(lines[-tail:]) if tail > 0 else ""
            new_text = top + content + bottom

            return replace(directive, text=new_text)

        except Exception as e:
            logging.error(format_error(str(e), directive.path, directive.prefix_line_number))
            return Stop()

    return import_directive