import pytest
from pathlib import Path
from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.source_directive import make_source_directive
from syncspec.stop import Stop


def _ctx() -> Context:
    return Context("", "", "", {}, "", "", "", "")


def _dir(text: str, params: dict) -> Directive:
    return Directive(params, "", text, "", Path("test.py"), 10, 11, 12)


@pytest.mark.parametrize("text,params,expected", [
    ("a\nb\nc\n", {"source": "k"}, "a\nb\nc\n"),
    ("a\nb\nc\n", {"source": "k", "head": 1}, "b\nc\n"),
    ("a\nb\nc\n", {"source": "k", "tail": 1}, "a\nb\n"),
    ("a\nb\nc\n", {"source": "k", "head": 1, "tail": 1}, "b\n"),
    ("x\ny", {"source": "k", "eof": True}, "x\ny\n"),
    ("line\n", {"source": "k", "head": 1}, ""),
])
def test_valid_source(text, params, expected):
    ctx = _ctx()
    res = make_source_directive(ctx)(_dir(text, params))
    assert isinstance(res, Directive)
    assert ctx.keyvalue[params["source"]] == expected


def test_overwrite_warning(caplog):
    ctx = _ctx()
    ctx.keyvalue["k"] = "old"
    make_source_directive(ctx)(_dir("new", {"source": "k"}))
    assert ctx.keyvalue["k"] == "new"
    assert "Overwriting" in caplog.text


@pytest.mark.parametrize("params", [
    {"source": "k", "eof": "yes"},
    {"source": "k", "head": 1.5},
    {"source": "k", "head": True},
    {"source": "k", "tail": None},
    {"source": "k", "head": 5},
])
def test_invalid_returns_stop(params, caplog):
    ctx = _ctx()
    res = make_source_directive(ctx)(_dir("a\nb\nc\n", params))
    assert isinstance(res, Stop)
    assert any("error" in rec.levelname.lower() for rec in caplog.records)


def test_passthrough():
    ctx = _ctx()
    d = _dir("data", {"other": "v"})
    res = make_source_directive(ctx)(d)
    assert res is d
    assert not ctx.keyvalue