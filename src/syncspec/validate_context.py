import logging
from typing import Callable

from syncspec.context import Context
from syncspec.utilities import format_error
from syncspec.dummy import Dummy

def make_validate_context(context: Context):
    def validate_context(param: Dummy) -> Dummy:
        open_delim = context.open_delimiter
        close_delim = context.close_delimiter

        # Validate Unicode strings
        try:
            open_delim.encode("utf-8")
            close_delim.encode("utf-8")
        except UnicodeEncodeError:
            logging.error(
                format_error(
                    "Delimiters must be valid Unicode strings.",
                    "Context",
                    0,
                )
            )
            raise ValueError("Invalid Unicode in delimiters")

        # Not empty
        if not open_delim or not close_delim:
            logging.error(
                format_error(
                    "Delimiters must not be empty strings.",
                    "Context",
                    0,
                )
            )
            raise ValueError("Empty delimiter")

        # Distinct
        if open_delim == close_delim:
            logging.error(
                format_error(
                    "Open and close delimiters must be distinct.",
                    "Context",
                    0,
                )
            )
            raise ValueError("Identical delimiters")

        # No structural overlap
        if open_delim in close_delim or close_delim in open_delim:
            logging.error(
                format_error(
                    "Delimiters must not be substrings of each other.",
                    "Context",
                    0,
                )
            )
            raise ValueError("Overlapping delimiters")

        # No newlines (covers all common newline forms)
        if "\n" in open_delim or "\r" in open_delim or "\n" in close_delim or "\r" in close_delim:
            logging.error(
                format_error(
                    "Delimiters must not contain newline characters.",
                    "Context",
                    0,
                )
            )
            raise ValueError("Newline in delimiter")

        return param

    return validate_context