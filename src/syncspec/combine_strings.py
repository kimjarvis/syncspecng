from syncspec.input_file_parameter import InputFileParameter
from syncspec.output_file_parameter import OutputFileParameter
from syncspec.combine_strings_context import CombineStringsContext


def make_combine_strings(context: CombineStringsContext):
    def combine_strings(fact: InputFileParameter) -> OutputFileParameter:
        context.text += fact.text
        return OutputFileParameter(text=fact.text, file=fact.file)

    return combine_strings