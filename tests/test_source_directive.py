import logging
import pytest
from pathlib import Path

from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.source_directive import make_source_directive


@pytest.fixture
def context():
    return Context("", "", "", {}, "", "", "", "")


@pytest.mark.parametrize(
    "params, initial_kv, expected_kv, expect_warning",
    [
        ({}, {}, {}, False),
        ({"source": "k1"}, {}, {"k1": "content"}, False),
        ({"source": "k1"}, {"k1": "old"}, {"k1": "content"}, True),
        ({"other": "val"}, {"k1": "old"}, {"k1": "old"}, False),
    ],
)
def test_source_directive(context, params, initial_kv, expected_kv, expect_warning, caplog):
    context.keyvalue.update(initial_kv)
    caplog.set_level(logging.WARNING)

    directive = Directive(params, "", "content", "", Path("src.txt"), 12, 13, 14)
    handler = make_source_directive(context)
    result = handler(directive)

    assert result is directive
    assert context.keyvalue == expected_kv

    if expect_warning:
        assert any("Overwriting" in rec.message for rec in caplog.records)