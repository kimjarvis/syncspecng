import pytest
from unittest.mock import patch
from dataclasses import dataclass

from syncspec.context import Context
from syncspec.validate_context import make_validate_context


@dataclass
class MockContext(Context):
    pass


@pytest.mark.parametrize(
    "open_delim,close_delim,should_raise",
    [
        ("{{", "}}", False),
        ("{", "}", False),
        ("", "}", True),
        ("{", "", True),
        ("{{", "{{", True),
        ("{", "{{", True),
        ("{{", "{", True),
        ("{\n", "}", True),
        ("{", "}\r", True),
        ("\u2028", "}", False),  # Valid Unicode line separator but not \n or \r
    ],
)
def test_delimiter_validation(open_delim, close_delim, should_raise):
    ctx = MockContext(
        open_delimiter=open_delim,
        close_delimiter=close_delim,
        keyvalue_file="",
        keyvalue={},
        input_path="",
        import_path_prefix="",
        export_path_prefix="",
        output_path_prefix="",
    )

    validator = make_validate_context(ctx)
    if should_raise:
        with pytest.raises(ValueError):
            validator("test")
    else:
        assert validator("test") == "test"


def test_non_unicode_strings():
    # Simulate non-UTF-8 by using surrogate strings (edge case)
    ctx = MockContext(
        open_delimiter="\udcff",
        close_delimiter="}",
        keyvalue_file="",
        keyvalue={},
        input_path="",
        import_path_prefix="",
        export_path_prefix="",
        output_path_prefix="",
    )
    validator = make_validate_context(ctx)
    with pytest.raises(ValueError):
        validator("test")