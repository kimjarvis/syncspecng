import pytest
from io import StringIO
import sys
from syncspec.dummy import Dummy
from syncspec.context import Context
from syncspec.example_coroutine import make_example_coroutine

@pytest.mark.parametrize("calls", [1, 3, 5])
def test_index_increment(capsys, calls):
    ctx = Context("", "", "", {}, "", "", "", "")
    coro = make_example_coroutine(ctx)
    for _ in range(calls):
        coro(Dummy())
    out = capsys.readouterr().out
    assert str(calls) in out
    assert "last" not in out

def test_return_type():
    ctx = Context("", "", "", {}, "", "", "", "")
    coro = make_example_coroutine(ctx)
    assert isinstance(coro(Dummy()), Dummy)