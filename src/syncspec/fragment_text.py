import logging
from typing import List, Union
from pathlib import Path

from syncspec.context import Context
from syncspec.fragment import Fragment
from syncspec.file_path import FilePath
from syncspec.stop import Stop
from syncspec.utilities import format_error


def make_fragment_text(context: Context):
    def fragment_text(fact: FilePath) -> Union[List[Fragment], Stop]:
        # Verify text is not empty
        if fact.text == "":
            logging.error(format_error("Empty text", fact.path, 1))
            return Stop()

        fragments = []
        text = fact.text
        pos = 0
        line_number = 1
        expect_open = True

        open_del = context.open_delimiter
        close_del = context.close_delimiter
        len_open = len(open_del)
        len_close = len(close_del)

        def fail(msg):
            logging.error(format_error(msg, fact.path, line_number))
            return Stop()

        while pos <= len(text):
            if expect_open:
                idx_open = text.find(open_del, pos)
                idx_close = text.find(close_del, pos)

                # Close before open (or close without open)
                if idx_close != -1 and (idx_open == -1 or idx_close < idx_open):
                    return fail(f"Unexpected close delimiter '{close_del}' before open delimiter")

                # No more opens, take rest of text
                if idx_open == -1:
                    segment = text[pos:]
                    fragments.append(Fragment(path=fact.path, text=segment, line_number=line_number))
                    break

                # Add segment before open delimiter
                segment = text[pos:idx_open]
                fragments.append(Fragment(path=fact.path, text=segment, line_number=line_number))
                line_number += segment.count('\n')

                pos = idx_open + len_open
                expect_open = False

            else:
                idx_close = text.find(close_del, pos)
                idx_open = text.find(open_del, pos)

                # Nested open before close
                if idx_open != -1 and (idx_close == -1 or idx_open < idx_close):
                    return fail(f"Nested open delimiter '{open_del}' detected")

                # Unclosed delimiter
                if idx_close == -1:
                    return fail(f"Unclosed delimiter '{open_del}'")

                # Add segment before close delimiter
                segment = text[pos:idx_close]
                fragments.append(Fragment(path=fact.path, text=segment, line_number=line_number))
                line_number += segment.count('\n')

                pos = idx_close + len_close
                expect_open = True

        return fragments

    return fragment_text