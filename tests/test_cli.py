import json
import sys
from pathlib import Path

import pytest
from syncspec.cli import main


@pytest.mark.parametrize("suffix, should_fail", [(".json", False), (".txt", True)])
def test_keyvalue_file_suffix(tmp_path, monkeypatch, suffix, should_fail):
    (tmp_path / "input").mkdir()
    kv_file = tmp_path / f"test{suffix}"
    kv_file.write_text("{}")
    args = ["cli.py", str(tmp_path / "input"), str(kv_file)]
    monkeypatch.setattr(sys, "argv", args)
    monkeypatch.setattr("syncspec.cli.machine", lambda ctx: None)
    if should_fail:
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
    else:
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0


@pytest.mark.parametrize("exists", [True, False])
def test_input_path_directory(tmp_path, monkeypatch, exists):
    kv_file = tmp_path / "test.json"
    kv_file.write_text("{}")
    if exists:
        (tmp_path / "input").mkdir()
        path_arg = str(tmp_path / "input")
    else:
        path_arg = str(tmp_path / "nonexistent")
    args = ["cli.py", path_arg, str(kv_file)]
    monkeypatch.setattr(sys, "argv", args)
    monkeypatch.setattr("syncspec.cli.machine", lambda ctx: None)
    if not exists:
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
    else:
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0


def test_invalid_json(tmp_path, monkeypatch):
    (tmp_path / "input").mkdir()
    bad_json = tmp_path / "bad.json"
    bad_json.write_text("{invalid}")
    args = ["cli.py", str(tmp_path / "input"), str(bad_json)]
    monkeypatch.setattr(sys, "argv", args)
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1


def test_logging_to_file(tmp_path, monkeypatch):
    (tmp_path / "input").mkdir()
    kv_file = tmp_path / "test.json"
    kv_file.write_text("{}")
    log_file = tmp_path / "test.log"
    args = ["cli.py", str(tmp_path / "input"), str(kv_file), "--log_file", str(log_file)]
    monkeypatch.setattr(sys, "argv", args)
    monkeypatch.setattr("syncspec.cli.machine", lambda ctx: None)
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0
    assert log_file.exists()


def test_prefix_defaults(tmp_path, monkeypatch):
    (tmp_path / "input").mkdir()
    kv_file = tmp_path / "test.json"
    kv_file.write_text("{}")
    args = ["cli.py", str(tmp_path / "input"), str(kv_file)]
    monkeypatch.setattr(sys, "argv", args)
    monkeypatch.setattr("syncspec.cli.machine", lambda ctx: None)
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0


def test_help_message(tmp_path, monkeypatch, capsys):
    args = ["cli.py", "--help"]
    monkeypatch.setattr(sys, "argv", args)
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "open_delimiter" in captured.out
    assert "close_delimiter" in captured.out
    assert "log_file" in captured.out
    assert "output_path_prefix" in captured.out
    assert "import_path_prefix" in captured.out
    assert "export_path_prefix" in captured.out
    assert "input_path" in captured.out
    assert "keyvalue_file" in captured.out