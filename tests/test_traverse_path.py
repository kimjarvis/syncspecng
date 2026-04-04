import pytest
from pathlib import Path
from syncspec.context import Context
from syncspec.dummy import Dummy
from syncspec.stop import Stop
from syncspec.file_path import FilePath
from syncspec.traverse_path import make_traverse_path


@pytest.mark.parametrize("exists,is_dir,expected_type", [
    (True, True, list),
    (False, True, Stop),
    (True, False, Stop),
])
def test_input_path_validation(tmp_path, exists, is_dir, expected_type):
    target = tmp_path / "input"
    if exists:
        if is_dir:
            target.mkdir()
        else:
            target.write_text("file")
    # If not exists, don't create anything

    ctx = Context(
        open_delimiter="{{", close_delimiter="}}",
        keyvalue_file="", keyvalue={},
        input_path=str(target),
        import_path_prefix="", export_path_prefix="", output_path_prefix=""
    )

    result = make_traverse_path(ctx)(Dummy())
    assert isinstance(result, expected_type)


def test_traverse_md_files(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "test.md").write_text("content")
    (input_dir / "test.txt").write_text("ignore")

    ctx = Context(
        open_delimiter="{{", close_delimiter="}}",
        keyvalue_file="", keyvalue={},
        input_path=str(input_dir),
        import_path_prefix="", export_path_prefix="", output_path_prefix=""
    )

    result = make_traverse_path(ctx)(Dummy())
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], FilePath)
    assert result[0].text == "content"


def test_symlink_exclusion(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    real_file = tmp_path / "real.md"
    real_file.write_text("real")
    link_file = input_dir / "link.md"
    link_file.symlink_to(real_file)

    ctx = Context(
        open_delimiter="{{", close_delimiter="}}",
        keyvalue_file="", keyvalue={},
        input_path=str(input_dir),
        import_path_prefix="", export_path_prefix="", output_path_prefix=""
    )

    result = make_traverse_path(ctx)(Dummy())
    assert isinstance(result, list)
    assert len(result) == 0  # Symlink excluded