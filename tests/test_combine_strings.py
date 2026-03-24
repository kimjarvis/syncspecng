import pytest
from syncspec.combine_strings import make_combine_strings
from syncspec.input_file_parameter import InputFileParameter
from syncspec.combine_strings_context import CombineStringsContext


@pytest.mark.parametrize(
    "init_text, inputs, expected_context",
    [
        ("", [("a", "f1")], "a"),
        ("", [("a", "f1"), ("b", "f2")], "ab"),
        ("pre", [("x", "f3")], "prex"),
    ],
)
def test_combine_strings_sequence(init_text, inputs, expected_context):
    context = CombineStringsContext(text=init_text)
    combiner = make_combine_strings(context)

    for text, file in inputs:
        fact = InputFileParameter(text=text, file=file)
        result = combiner(fact)
        assert result.text == text
        assert result.file == file

    assert context.text == expected_context