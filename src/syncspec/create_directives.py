import ast
import logging
import re
from pathlib import Path
from typing import Union

from syncspec.block import Block
from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.stop import Stop
from syncspec.utilities import format_error

logger = logging.getLogger(__name__)

def string_to_keyvalue_dict(prefix_str: str, path: Path, line_number: int) -> Union[dict, Stop]:
    params = {}
    pattern = re.compile(r'(\w+)\s*=\s*("(?:[^"\\]|\\.)*"|[^,]+)')
    for m in pattern.finditer(prefix_str):
        key, raw_val = m.group(1), m.group(2).strip()
        try:
            params[key] = ast.literal_eval(raw_val)
        except (ValueError, SyntaxError) as e:
            logger.error(format_error(f"Syntax error in parameter '{key}': {e}", path, line_number))
            return Stop()
    return params

def make_create_directives(context: Context):
    def create_directives(block: Block) -> Union[Directive, Stop]:
        parsed = string_to_keyvalue_dict(block.prefix, block.path, block.prefix_line_number)
        if isinstance(parsed, Stop):
            return parsed
        return Directive(
            parameters=parsed,
            prefix=block.prefix,
            text=block.text,
            suffix=block.suffix,
            path=block.path,
            prefix_line_number=block.prefix_line_number,
            text_line_number=block.text_line_number,
            suffix_line_number=block.suffix_line_number
        )
    return create_directives