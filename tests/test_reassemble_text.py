import pytest
from pathlib import Path
from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.reassemble_text import make_reassemble_text


@pytest.mark.parametrize(
    "open_del, close_del, prefix, text, suffix, expected",
    [
        ("{", "}", "pre", "mid", "suf", "{pre}mid{suf}"),
        ("<!--", "-->", "a", "b", "c", "<!--a-->b<!--c-->"),
        ("", "", "", "plain", "", "plain"),
    ]
)
def test_reassemble_text_construction(open_del, close_del, prefix, text, suffix, expected):
    ctx = Context(
        open_delimiter=open_del, close_delimiter=close_del,
        keyvalue_file="", keyvalue={},
        input_path="", import_path_prefix="",
        export_path_prefix="", output_path_prefix=""
    )
    directive = Directive(
        parameters={}, prefix=prefix, text=text, suffix=suffix,
        path=Path("test.py"),
        prefix_line_number=10, text_line_number=11, suffix_line_number=12
    )

    result = make_reassemble_text(ctx)(directive)

    assert result.text == expected
    assert result.path == directive.path
    assert result.line_number == directive.prefix_line_number