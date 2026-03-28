import pytest
from pathlib import Path
from unittest.mock import patch
from syncspec.fragment_text import make_fragment_text
from syncspec.context import Context
from syncspec.file_path import FilePath
from syncspec.fragment import Fragment
from syncspec.stop import Stop

CTX = Context(
    open_delimiter="{{", close_delimiter="}}",
    keyvalue_file="", keyvalue={},
    input_path="", import_path_prefix="",
    export_path_prefix="", output_path_prefix=""
)


@pytest.mark.parametrize("text,expected_type,frag_count", [
    ("A{{B}}C", list, 3),
    ("{{}}", list, 3),
    ("{{A}}", list, 3),
    ("{{}}A", list, 3),
    ("NoDelims", list, 1),
    ("A\n{{B}}", list, 3),
    ("{{A}}B{{C}}", list, 5),
    ("}}", Stop, 0),
    ("{{A{{B}}", Stop, 0),
    ("{{A", Stop, 0),
    ("", Stop, 0),
])
def test_fragment_text(text, expected_type, frag_count):
    parser = make_fragment_text(CTX)
    fact = FilePath(Path("test.txt"), text)
    result = parser(fact)

    assert isinstance(result, expected_type)
    if expected_type == list:
        assert len(result) == frag_count
        assert all(f.path == fact.path for f in result)


@patch('syncspec.fragment_text.logging')
@patch('syncspec.fragment_text.format_error')
def test_error_logging(mock_format, mock_logging):
    parser = make_fragment_text(CTX)
    fact = FilePath(Path("err.txt"), "}}")
    result = parser(fact)

    assert isinstance(result, Stop)
    mock_format.assert_called_once()
    mock_logging.error.assert_called_once()


def test_line_numbers():
    parser = make_fragment_text(CTX)
    fact = FilePath(Path("test.txt"), "A{{B}}C\n{{D}}EF")
    result = parser(fact)

    assert len(result) == 5
    assert result[0].line_number == 1  # A
    assert result[1].line_number == 1  # B
    assert result[2].line_number == 1  # C\n
    assert result[3].line_number == 2  # D
    assert result[4].line_number == 2  # EF


def test_empty_fragments():
    parser = make_fragment_text(CTX)
    fact = FilePath(Path("test.txt"), "{{}}")
    result = parser(fact)

    assert len(result) == 3
    assert all(f.text == "" for f in result)


def test_empty_text():
    parser = make_fragment_text(CTX)
    fact = FilePath(Path("test.txt"), "")
    result = parser(fact)

    assert isinstance(result, Stop)


@patch('syncspec.fragment_text.logging')
@patch('syncspec.fragment_text.format_error')
def test_empty_text_logging(mock_format, mock_logging):
    parser = make_fragment_text(CTX)
    fact = FilePath(Path("empty.txt"), "")
    parser(fact)

    mock_format.assert_called_once()
    mock_logging.error.assert_called_once()