import pytest
from pathlib import Path
from syncspec.context import Context
from syncspec.directive import Directive
from syncspec.stop import Stop
from syncspec.import_directive import make_import_directive

@pytest.fixture
def import_prefix(tmp_path):
    p = tmp_path / "imports"
    p.mkdir()
    (p / "sample.txt").write_text("imported\n")
    return p

@pytest.fixture
def ctx(import_prefix):
    return Context(
        open_delimiter="<!--", close_delimiter="-->", keyvalue_file="", keyvalue={},
        input_path="", import_path_prefix=str(import_prefix), export_path_prefix="", output_path_prefix=""
    )

@pytest.fixture
def directive_factory():
    def _make(params: dict, text: str = "top\nmid\nbottom\n") -> Directive:
        return Directive(parameters=params, prefix="", text=text, suffix="",
                         path=Path("src/test.py"), prefix_line_number=10, text_line_number=11, suffix_line_number=12)
    return _make

@pytest.mark.parametrize(
    "params, expected_type, desc", [
        ({}, Directive, "no import key"),
        ({"import": "sample.txt"}, Directive, "valid import"),
        ({"import": "../etc/passwd"}, Stop, "path traversal"),
        ({"import": "missing.txt"}, Stop, "missing file"),
        ({"import": "sample.txt", "eof": "true"}, Stop, "invalid eof type"),
        ({"import": "sample.txt", "head": 1, "tail": 1}, Directive, "head & tail"),
        ({"import": "sample.txt", "head": 5}, Stop, "head exceeds lines"),
    ]
)
def test_import_directive_logic(import_prefix, ctx, directive_factory, params, expected_type, desc):
    func = make_import_directive(ctx)
    directive = directive_factory(params)
    result = func(directive)
    assert isinstance(result, expected_type), f"Failed: {desc}"

    if expected_type is Directive and params.get("import"):
        if params.get("eof") is True:
            assert result.text.endswith("\n\n") or "imported\n" in result.text