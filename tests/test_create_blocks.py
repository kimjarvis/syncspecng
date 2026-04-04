import pytest
from pathlib import Path
from syncspec.context import Context
from syncspec.indexedfragment import IndexedFragment
from syncspec.text import Text
from syncspec.block import Block
from syncspec.stop import Stop
from syncspec.create_blocks import make_create_blocks

_PATH = Path("test.txt")
_CTX = Context("", "", "", {}, "", "", "", "")


def _frag(idx: int) -> IndexedFragment:
    return IndexedFragment(path=_PATH, text=f"content_{idx}", line_number=idx, index=idx)


def test_create_blocks_sequence():
    factory = make_create_blocks(_CTX)
    # Stateful closures require sequential execution; isolated parametrization breaks state.
    for idx, expected in [(0, Text), (1, type(None)), (2, type(None)), (3, type(None)), (4, tuple)]:
        res = factory(_frag(idx))
        assert isinstance(res, expected), f"Failed at index {idx}"
        if isinstance(res, tuple):
            assert isinstance(res[1], Block)


def test_create_blocks_last_flag_error(caplog):
    factory = make_create_blocks(_CTX)
    state = next(c.cell_contents for c in factory.__closure__ if isinstance(c.cell_contents, dict))
    state["last"] = True

    with caplog.at_level("ERROR"):
        res = factory(_frag(5))

    assert isinstance(res, Stop)
    assert "multiple of 4" in caplog.text