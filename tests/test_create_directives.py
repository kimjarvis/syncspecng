import logging
import pytest
from dataclasses import replace
from pathlib import Path

from syncspec.block import Block
from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.stop import Stop
from syncspec.create_directives import make_create_directives

_CTX = Context(open_delimiter="", close_delimiter="", keyvalue_file="",
               keyvalue={}, input_path="", import_path_prefix="",
               export_path_prefix="", output_path_prefix="")
_BASE_BLOCK = Block(prefix="", text="", suffix="", path=Path("x.py"),
                    prefix_line_number=1, text_line_number=2, suffix_line_number=3)

@pytest.mark.parametrize("prefix,expected", [
    ("", {}),
    ("k=1", {"k": 1}),
    ('s="hi", fl=False', {"s": "hi", "fl": False}),
])
def test_valid_prefix_creates_directive(prefix, expected):
    block = replace(_BASE_BLOCK, prefix=prefix)
    res = make_create_directives(_CTX)(block)
    assert isinstance(res, Directive)
    assert res.parameters == expected

def test_invalid_syntax_returns_stop(caplog):
    caplog.set_level(logging.ERROR)
    block = replace(_BASE_BLOCK, prefix="bad={invalid}", path=Path("err.py"), prefix_line_number=10)
    res = make_create_directives(_CTX)(block)
    assert isinstance(res, Stop)
    assert "Syntax error" in caplog.text