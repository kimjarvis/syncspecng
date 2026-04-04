import logging
import pytest
from pathlib import Path
from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.stop import Stop
from syncspec.include_directive import make_include_directive

@pytest.fixture
def ctx():
    return Context(
        open_delimiter="", close_delimiter="", keyvalue_file="",
        keyvalue={"k": "INS"}, input_path="",
        import_path_prefix="", export_path_prefix="", output_path_prefix=""
    )

def _dir(params, text="L1\nL2\nL3\n", path="t.txt", line=1):
    return Directive(params, "", text, "", Path(path), 0, line, 0)

def test_missing_include_key(ctx):
    fn = make_include_directive(ctx)
    d = _dir({})
    assert fn(d) is d

def test_unknown_context_key(ctx, caplog):
    fn = make_include_directive(ctx)
    d = _dir({"include": "unknown"})
    with caplog.at_level(logging.WARNING):
        assert fn(d) is d
    assert "unknown" in caplog.text

@pytest.mark.parametrize("p", [
    {"include": "k", "eof": 1},
    {"include": "k", "head": "0"},
    {"include": "k", "tail": 2.5},
    {"include": "k", "head": 2, "tail": 2}
])
def test_invalid_or_excess_params_return_stop(ctx, p, caplog):
    fn = make_include_directive(ctx)
    with caplog.at_level(logging.ERROR):
        assert isinstance(fn(_dir(p)), Stop)

def test_eof_appends_newline(ctx, caplog):
    fn = make_include_directive(ctx)
    with caplog.at_level(logging.ERROR):
        res = fn(_dir({"include": "k", "eof": True}))
    assert res.text == "INS\n"

def test_head_tail_slicing(ctx, caplog):
    fn = make_include_directive(ctx)
    with caplog.at_level(logging.ERROR):
        res = fn(_dir({"include": "k", "head": 1, "tail": 1}))
    assert res.text == "L1\nINS\nL3\n"