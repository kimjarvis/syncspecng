import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Optional

from syncspec.context import Context
from syncspec.machine import machine


def error_exit(msg: str) -> None:
    sys.stderr.write(f"Error: {msg}\n")
    sys.exit(1)


def validate_path(path_str: str, must_exist: bool, is_dir: bool, suffix: Optional[str] = None) -> None:
    p = Path(path_str)
    if suffix and not p.name.endswith(suffix):
        error_exit(f"{path_str} must have suffix {suffix}")
    if must_exist:
        if is_dir and not p.is_dir():
            error_exit(f"{path_str} is not a valid directory")
        if not is_dir and not p.is_file():
            error_exit(f"{path_str} is not a valid file")
    elif not p.parent.is_dir():
        error_exit(f"Parent directory for {path_str} does not exist")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="SyncSpec CLI - Process templates with key-value substitutions"
    )
    parser.add_argument(
        "input_path",
        help="Existing directory path containing input files"
    )
    parser.add_argument(
        "keyvalue_file",
        help="Existing JSON file path containing key-value pairs for substitution"
    )
    parser.add_argument(
        "--open_delimiter",
        default="{{",
        help="Opening delimiter for template variables (default: '{{')"
    )
    parser.add_argument(
        "--close_delimiter",
        default="}}",
        help="Closing delimiter for template variables (default: '}}')"
    )
    parser.add_argument(
        "--log_file",
        help="Path to log file (must have .log suffix). Logs to console if not specified."
    )
    parser.add_argument(
        "--output_path_prefix",
        help="Existing directory path for output files. Defaults to input_path if not specified."
    )
    parser.add_argument(
        "--import_path_prefix",
        help="Existing directory path for import files. Defaults to input_path if not specified."
    )
    parser.add_argument(
        "--export_path_prefix",
        help="Existing directory path for export files. Defaults to input_path if not specified."
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    validate_path(args.input_path, must_exist=True, is_dir=True)
    validate_path(args.keyvalue_file, must_exist=True, is_dir=False, suffix=".json")

    try:
        with open(args.keyvalue_file) as f:
            keyvalue = json.load(f)
    except json.JSONDecodeError:
        error_exit(f"Invalid JSON in {args.keyvalue_file}")

    if args.log_file:
        validate_path(args.log_file, must_exist=False, is_dir=False, suffix=".log")

    for path in [args.output_path_prefix, args.import_path_prefix, args.export_path_prefix]:
        if path:
            validate_path(path, must_exist=True, is_dir=True)

    # Clear existing handlers to ensure basicConfig works
    logging.root.handlers = []

    log_config = {
        "level": logging.WARNING,
        "format": "%(levelname)s - %(message)s",
    }
    if args.log_file:
        log_config["filename"] = args.log_file
    logging.basicConfig(**log_config)

    # Emit a log message to ensure file handler is initialized
    logging.warning("CLI started")

    output_prefix = args.output_path_prefix or args.input_path
    import_prefix = args.import_path_prefix or args.input_path
    export_prefix = args.export_path_prefix or args.input_path

    context = Context(
        open_delimiter=args.open_delimiter,
        close_delimiter=args.close_delimiter,
        keyvalue_file=args.keyvalue_file,
        keyvalue=keyvalue,
        input_path=args.input_path,
        import_path_prefix=import_prefix,
        export_path_prefix=export_prefix,
        output_path_prefix=output_prefix,
    )

    machine(context)
    sys.exit(0)


if __name__ == "__main__":
    main()