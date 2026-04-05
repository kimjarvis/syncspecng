import pytest
from pathlib import Path
from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.stop import Stop
from syncspec.import_directive import make_import_directive

@pytest.fixture
def ctx(tmp_path):
    return Context(
        open_delimiter="", close_delimiter="", keyvalue_file="", keyvalue={},
        input_path=str(tmp_path), import_path_prefix="", export_path_prefix="", output_path_prefix=""
    )

def _mk_dir(text, params=None, line=0):
    return Directive(
        parameters=params or {}, prefix="", text=text, suffix="",
        path=Path("dummy.md"), prefix_line_number=line,
        text_line_number=0, suffix_line_number=0
    )

def test_no_import_returns_unchanged(ctx):
    fn = make_import_directive(ctx)
    d = _mk_dir("keep\n")
    assert fn(d) is d

def test_valid_import_with_params(ctx, tmp_path):
    (tmp_path / "inc.txt").write_text("DATA\n", encoding="utf-8")
    fn = make_import_directive(ctx)
    d = _mk_dir("H1\nB1\nB2\n", {"import": "inc.txt", "head": 1, "tail": 1, "eof": True}, line=42)
    res = fn(d)
    assert isinstance(res, Directive) and res is not d
    assert res.text == "H1\nDATA\n\nB2\n"
    assert res.prefix_line_number == 42

@pytest.mark.parametrize("params, setup, err_msg", [
    ({"import": "../esc.txt"}, None, "escapes"),
    ({"import": "lnk.txt"}, lambda p: (p/"lnk.txt").symlink_to(p.parent/"esc.txt"), "escapes"),
    ({"import": "miss.txt"}, None, "does not exist"),
    ({"import": "dir"}, lambda p: (p/"dir").mkdir(), "not a regular file"),
    ({"import": "bin"}, lambda p: (p/"bin").write_bytes(b"\x80"), "not a valid text file"),
    ({"import": "f.txt", "eof": 1}, lambda p: (p/"f.txt").write_text(""), "must be a boolean"),
    ({"import": "f.txt", "head": "1"}, lambda p: (p/"f.txt").write_text("a\nb\n"), "must be an integer"),
    ({"import": "f.txt", "tail": True}, lambda p: (p/"f.txt").write_text("a\nb\n"), "must be an integer"),
    ({"import": "f.txt", "head": 3, "tail": 1}, lambda p: (p/"f.txt").write_text("x"), "exceeds line count"),
])
def test_invalid_params_return_stop(ctx, tmp_path, params, setup, err_msg, caplog):
    if setup:
        setup(tmp_path)
    fn = make_import_directive(ctx)
    # Corrected: params is now passed, and Stop is imported from syncspec.stop
    assert isinstance(fn(_mk_dir("l1\nl2\nl3\n", params)), Stop)
    assert err_msg in caplog.text