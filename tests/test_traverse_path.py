# test_traverse_path.py
import pytest
from pathlib import Path
from syncspec.context import Context
from syncspec.dummy import Dummy
from syncspec.stop import Stop
from syncspec.file_path import FilePath
from syncspec.traverse_path import make_traverse_path  # Assuming module name


@pytest.mark.parametrize("path_structure, expected_count", [
    ({"a.md": "content"}, 1),
    ({"b.txt": "content"}, 0),
    ({"sub/a.md": "content"}, 1),
    ({"a.md": "content", "b.md": "content"}, 2),
])
def test_traverse_success(tmp_path, path_structure, expected_count):
    for name, content in path_structure.items():
        file_path = tmp_path / name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)

    context = Context(
        open_delimiter="", close_delimiter="", keyvalue_file="", keyvalue={},
        input_path=str(tmp_path), import_path_prefix="", export_path_prefix="", output_path_prefix=""
    )
    traverse = make_traverse_path(context)
    results = []
    while True:
        res = traverse(Dummy())
        if isinstance(res, Stop):
            break
        results.append(res)

    assert len(results) == expected_count
    if expected_count > 0:
        assert isinstance(results[0], FilePath)


def test_invalid_path(tmp_path):
    context = Context(
        open_delimiter="", close_delimiter="", keyvalue_file="", keyvalue={},
        input_path=str(tmp_path / "nonexistent"), import_path_prefix="", export_path_prefix="", output_path_prefix=""
    )
    traverse = make_traverse_path(context)
    assert isinstance(traverse(Dummy()), Stop)


def test_relative_path_security(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    outside = tmp_path.parent / "outside"
    outside.mkdir(exist_ok=True)

    context = Context(
        open_delimiter="", close_delimiter="", keyvalue_file="", keyvalue={},
        input_path="../outside", import_path_prefix="", export_path_prefix="", output_path_prefix=""
    )
    traverse = make_traverse_path(context)
    assert isinstance(traverse(Dummy()), Stop)