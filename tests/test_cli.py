import pytest
import json
import os
from syncspec.cli import validate_delimiters, validate_file_path, main


@pytest.mark.parametrize(
    "open_d, close_d, expected_error",
    [
        ("{{", "}}", None),
        ("", "}}", "empty"),
        ("{{", "", "empty"),
        ("{{\n", "}}", "newlines"),
        ("{{", "{{", "distinct"),
        ("{", "{{", "overlap"),
        ("{{", "{", "overlap"),
    ],
)
def test_validate_delimiters(open_d, close_d, expected_error):
    if expected_error:
        with pytest.raises(ValueError, match=expected_error):
            validate_delimiters(open_d, close_d)
    else:
        validate_delimiters(open_d, close_d)


@pytest.mark.parametrize(
    "path, suffix, must_exist, expected_error",
    [
        ("test.log", ".log", False, None),
        ("test.txt", ".log", False, "end with"),
        ("test.md", ".md", True, "does not exist"),
    ],
)
def test_validate_file_path(tmp_path, path, suffix, must_exist, expected_error):
    if expected_error and "exists" in expected_error:
        path = str(tmp_path / "missing.md")

    if expected_error:
        with pytest.raises(ValueError, match=expected_error):
            validate_file_path(path, suffix, must_exist)
    else:
        if must_exist:
            p = tmp_path / path
            p.write_text("content")
            path = str(p)
        validate_file_path(path, suffix, must_exist)


def test_main_invalid_json(tmp_path):
    md_file = tmp_path / "input.md"
    md_file.write_text("content")
    json_file = tmp_path / "data.json"
    json_file.write_text("invalid json")

    with pytest.raises(SystemExit) as exc_info:
        main([str(md_file), "--keyvalue_file", str(json_file)])
    assert exc_info.value.code == 1


def test_main_validation_error(tmp_path):
    md_file = tmp_path / "input.txt"  # Wrong suffix
    md_file.write_text("content")
    json_file = tmp_path / "data.json"
    json_file.write_text("{}")

    exit_code = main([str(md_file), "--keyvalue_file", str(json_file)])
    assert exit_code == 1