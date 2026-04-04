import pytest
from pathlib import Path
from syncspec.defragment_text import make_defragment_text
from syncspec.text import Text
from syncspec.context import Context

_CTX = Context("", "", "", {}, "", "", "", "")

@pytest.mark.parametrize("files, chunks, expected", [
    (["a.txt", "a.txt"], ["Hello ", "World"], {"a.txt": "Hello World"}),
    (["a.txt", "b.txt"], ["P1", "P2"], {"a.txt": "P1", "b.txt": "P2"}),
])
def test_defragment_text(tmp_path, files, chunks, expected):
    paths = [tmp_path / f for f in files]
    fn = make_defragment_text(_CTX)
    state = fn.__closure__[0].cell_contents

    for i, (p, txt) in enumerate(zip(paths, chunks)):
        state['last'] = (i == len(chunks) - 1)
        fn(Text(path=p, text=txt, line_number=0))

    for f, content in expected.items():
        assert (tmp_path / f).read_text() == content