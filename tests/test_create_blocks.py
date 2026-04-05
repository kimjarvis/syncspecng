import pytest
import logging
from pathlib import Path
from unittest.mock import patch

from syncspec.context import Context
from syncspec.create_blocks import make_create_blocks
from syncspec.indexedfragment import IndexedFragment
from syncspec.block import Block
from syncspec.text import Text
from syncspec.stop import Stop


@pytest.fixture
def ctx():
    return Context("", "", "", {}, "", "", "", "")


def mk_frag(idx):
    return IndexedFragment(Path("file.txt"), "content", 5, idx)


@pytest.mark.parametrize("idx, exp_type", [
    (0, Text), (1, type(None)), (2, type(None)), (3, type(None)), (4, tuple)
])
def test_fragment_processing(ctx, idx, exp_type):
    fn = make_create_blocks(ctx)
    # Pre-populate state for indices that depend on block initialization
    if idx > 1:
        fn.state["block"] = Block(prefix="", text="", suffix="", path=Path("file.txt"),
                                  prefix_line_number=0, text_line_number=0, suffix_line_number=0)
    assert isinstance(fn(mk_frag(idx)), exp_type)


def test_last_flag_returns_stop(ctx, caplog):
    fn = make_create_blocks(ctx)
    fn.state["last"] = True
    caplog.set_level(logging.ERROR)

    with patch("syncspec.create_blocks.format_error", return_value="fmt_err"):
        res = fn(mk_frag(2))
        assert isinstance(res, Stop)
        assert any("fmt_err" in rec.msg for rec in caplog.records)