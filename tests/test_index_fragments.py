import pytest
from pathlib import Path
from syncspec.context import Context
from syncspec.fragment import Fragment
from syncspec.index_fragments import make_index_fragments

@pytest.fixture
def ctx():
    return Context("{{", "}}", "", {}, "", "", "", "")

@pytest.mark.parametrize("paths, expected", [
    (["a.py", "a.py", "b.py"], [0, 1, 0]),
    (["x.py", "y.py", "z.py"], [0, 0, 0]),
    (["same.py"] * 3, [0, 1, 2]),
])
def test_indexing(ctx, paths, expected):
    fn = make_index_fragments(ctx)
    for path, exp_idx in zip(paths, expected):
        res = fn(Fragment(Path(path), "", 0))
        assert res.index == exp_idx
        assert res.path == Path(path)