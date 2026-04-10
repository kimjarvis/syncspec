import argparse
import sys
from pathlib import Path
from syncspec.context import Context
from syncspec.machine import machine

def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="SyncSpec CLI")
    parser.add_argument("input_path", type=Path, help="Valid input directory path.")
    parser.add_argument("--open_delimiter", default="{-", help="Open delimiter string (default: '{-').")
    parser.add_argument("--close_delimiter", default="-}", help="Close delimiter string (default: '-}').")
    parser.add_argument("--keyvalue", type=Path, default=None, help="Path to .json key-value file.")
    parser.add_argument("--ignore_rules", type=Path, default=None, help="Path to ignore rules file.")

    args = parser.parse_args(argv)

    if not args.input_path.is_dir():
        parser.error(f"input_path must be an existing directory: {args.input_path}")

    if args.keyvalue:
        if not args.keyvalue.exists():
            parser.error(f"--keyvalue file not found: {args.keyvalue}")
        if args.keyvalue.suffix.lower() != ".json":
            parser.error("--keyvalue must have a .json suffix.")

    if args.ignore_rules and not args.ignore_rules.exists():
        parser.error(f"--ignore_rules file not found: {args.ignore_rules}")

    return args

def main(argv=None):
    args = parse_args(argv)
    context = Context(
        open_delimiter=args.open_delimiter,
        close_delimiter=args.close_delimiter,
        keyvalue={},
        input_path=args.input_path.resolve(),
        keyvalue_file=args.keyvalue.resolve() if args.keyvalue else None,
        ignore_rules_file=args.ignore_rules.resolve() if args.ignore_rules else None,
    )
    machine(context)
    sys.exit(0)

if __name__ == "__main__":
    main()