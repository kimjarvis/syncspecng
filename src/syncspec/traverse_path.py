import logging
import os
from pathlib import Path
from typing import List, Union

from syncspec.context import Context
from syncspec.dummy import Dummy
from syncspec.file_path import FilePath
from syncspec.stop import Stop
from syncspec.utilities import format_error


def make_traverse_path(context: Context):
    def traverse_path(fact: Dummy) -> Union[List[Union[FilePath, Stop]], Stop]:
        input_path = Path(context.input_path)
        cwd = Path.cwd().resolve()

        # Resolve and validate path
        try:
            if input_path.is_absolute():
                resolved = input_path.resolve()
            else:
                resolved = (cwd / input_path).resolve()
                if not resolved.is_relative_to(cwd):
                    raise ValueError("Relative path escapes cwd")

            if not resolved.exists() or not resolved.is_dir():
                raise FileNotFoundError("Invalid directory")
        except Exception as e:
            logging.error(format_error(str(e), input_path, 0))
            return Stop()

        results: List[Union[FilePath, Stop]] = []

        try:
            for root, dirs, files in os.walk(resolved, followlinks=False):
                for file in files:
                    if not file.endswith(".md"):
                        continue

                    file_path = Path(root) / file
                    if file_path.is_symlink():
                        continue

                    try:
                        text = file_path.read_text()
                        results.append(FilePath(path=file_path, text=text))
                    except Exception as e:
                        logging.error(format_error(str(e), file_path, 0))
                        results.append(Stop())
        except Exception as e:
            logging.error(format_error(str(e), resolved, 0))
            return Stop()

        return results

    return traverse_path