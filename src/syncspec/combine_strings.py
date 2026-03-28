from syncspec.input_file_parameter import InputFileParameter
from syncspec.output_file_parameter import OutputFileParameter
from syncspec.context import Context


def make_combine_strings(context: Context):
    def combine_strings(fact: InputFileParameter) -> OutputFileParameter:
        return OutputFileParameter(text=fact.text, file=fact.file)

    return combine_strings