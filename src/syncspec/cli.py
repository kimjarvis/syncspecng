import argparse
import json
import logging
import sys
from pathlib import Path
from typing import List, Optional

from syncspec.context import Context
from syncspec.machine import machine


def main(cli_args: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(
        description="Process input files with custom delimiters and key-value mappings."
    )
    parser.add_argument("--open_delimiter", default="{{", help="Opening delimiter")
    parser.add_argument("--close_delimiter", default="}}", help="Closing delimiter")
    parser.add_argument("--log_file", default=None, help="Log file path (must end with .log)")
    parser.add_argument("input_path", help="Path to the input directory")
    parser.add_argument("keyvalue_file", nargs="?", default=None, help="Optional JSON file (must exist, end with .json)")

    args = parser.parse_args(cli_args)

    # 1. Validate input_path
    input_path = Path(args.input_path)
    if not input_path.is_dir():
        print(f"Error: input_path '{input_path}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    # 2. Validate --log_file
    if args.log_file is not None:
        log_path = Path(args.log_file)
        if log_path.suffix.lower() != ".log":
            print(f"Error: --log_file must have a '.log' suffix, got '{log_path.suffix}'.", file=sys.stderr)
            sys.exit(1)

    # 3. Read & validate keyvalue_file
    keyvalue = {}
    if args.keyvalue_file is not None:
        kv_path = Path(args.keyvalue_file)
        if kv_path.suffix.lower() != ".json":
            print(f"Error: keyvalue_file must have a '.json' suffix, got '{kv_path.suffix}'.", file=sys.stderr)
            sys.exit(1)
        if not kv_path.is_file():
            print(f"Error: keyvalue_file '{kv_path}' does not exist.", file=sys.stderr)
            sys.exit(1)

        try:
            with open(kv_path, "r", encoding="utf-8") as f:
                keyvalue = json.load(f)
            if not isinstance(keyvalue, dict):
                raise ValueError("JSON root must be a dictionary.")
        except (json.JSONDecodeError, ValueError, OSError) as e:
            print(f"Error: Failed to read/validate JSON '{kv_path}': {e}", file=sys.stderr)
            sys.exit(1)

    # 4. Configure Logging
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    log_format = "%(levelname)s - %(message)s"
    if args.log_file:
        logging.basicConfig(filename=args.log_file, level=logging.WARNING, format=log_format)
    else:
        logging.basicConfig(level=logging.WARNING, format=log_format)

    logging.warning("CLI started")

    # 5. Create Context
    context = Context(
        open_delimiter=args.open_delimiter,
        close_delimiter=args.close_delimiter,
        keyvalue_file=args.keyvalue_file,
        keyvalue=keyvalue,
        input_path=str(input_path),
        import_path_prefix=None,
        export_path_prefix=None,
        output_path_prefix=None,
    )

    # 6. Execute
    machine(context)


if __name__ == "__main__":
    main()