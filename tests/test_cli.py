import json
from pathlib import Path
from unittest.mock import patch

import pytest

from syncspec.cli import main

@pytest.fixture
def valid_dir(tmp_path: Path) -> Path:
    d = tmp_path / "input"
    d.mkdir()
    return d

@pytest.mark.parametrize("args, error_keyword", [
    (["non_existent"], "input_path"),
    ([".", "--log_file", "test.txt"], "log_file"),
    ([".", "data.xml"], "keyvalue_file"),
    ([".", "missing.json"], "exist"),
])
def test_validation_errors(valid_dir, capsys, args, error_keyword):
    if args[0] == ".":
        args = [str(valid_dir)] + args[1:]
    with pytest.raises(SystemExit) as exc:
        main(args)
    assert exc.value.code == 1
    assert error_keyword in capsys.readouterr().err

def test_invalid_json(valid_dir, tmp_path, capsys):
    bad_json = tmp_path / "bad.json"
    bad_json.write_text("{invalid")
    with pytest.raises(SystemExit) as exc:
        main([str(valid_dir), str(bad_json)])
    assert exc.value.code == 1
    assert "JSON" in capsys.readouterr().err

@patch("syncspec.cli.machine")
def test_success_with_file_logging(mock_machine, valid_dir, tmp_path, capsys):
    kv = tmp_path / "kv.json"
    kv.write_text(json.dumps({"k": "v"}))
    log = tmp_path / "run.log"
    main([str(valid_dir), str(kv), "--log_file", str(log)])
    mock_machine.assert_called_once()
    ctx = mock_machine.call_args[0][0]
    assert ctx.keyvalue == {"k": "v"} and log.read_text().strip() == "WARNING - CLI started"

@patch("syncspec.cli.machine")
def test_success_with_console_logging(mock_machine, valid_dir, capsys):
    main([str(valid_dir)])
    assert "WARNING - CLI started" in capsys.readouterr().err