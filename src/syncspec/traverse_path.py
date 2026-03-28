import logging
import os
from pathlib import Path
from typing import Union, Iterator, Optional

from syncspec.context import Context
from syncspec.dummy import Dummy
from syncspec.stop import Stop
from syncspec.file_path import FilePath
from syncspec.utilities import format_error


def make_traverse_path(context: Context):
    iterator: Optional[Iterator[Path]] = None
    failed = False

    def traverse_path(fact: Dummy) -> Union[FilePath, Stop]:
        nonlocal iterator, failed
        if failed:
            return Stop()

        if iterator is None:
            input_path = Path(context.input_path)
            if not input_path.exists() or not input_path.is_dir() or input_path.is_symlink():
                logging.error(format_error("Invalid input path", "traverse_path", 0))
                failed = True
                return Stop()

            cwd = Path.cwd().resolve()
            resolved = input_path.resolve()
            if not input_path.is_absolute() and resolved != cwd and cwd not in resolved.parents:
                logging.error(format_error("Path outside cwd", "traverse_path", 0))
                failed = True
                return Stop()

            def gen():
                for root, dirs, files in os.walk(input_path, followlinks=False):
                    for f in files:
                        if f.endswith('.md'):
                            p = Path(root) / f
                            if not p.is_symlink():
                                yield p

            try:
                iterator = gen()
            except Exception as e:
                logging.error(format_error(str(e), "traverse_path", 0))
                failed = True
                return Stop()

        try:
            path = next(iterator)
            return FilePath(path=path, text=path.read_text())
        except StopIteration:
            return Stop()
        except Exception as e:
            logging.error(format_error(str(e), "traverse_path", 0))
            failed = True
            return Stop()

    return traverse_path