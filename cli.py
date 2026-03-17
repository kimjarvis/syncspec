#!/usr/bin/env python3
import argparse
import json
import logging
import sys
from pathlib import Path
from typing import List, Dict, Any

import networkx as nx

from src.syncspec.text import Text
from src.syncspec.file import File
from src.syncspec.syncspec_list_context import SyncspecListContext
from src.syncspec.syncspec_list import make_syncspec_list


def error_exit(message: str) -> None:
    """Print error message to stderr and terminate."""
    print(message, file=sys.stderr)
    sys.exit(1)


def validate_args(args: argparse.Namespace) -> None:
    """Validate command line arguments according to specification."""
    # --log_file
    if args.log_file:
        p = Path(args.log_file)
        if p.suffix != ".log":
            error_exit("Error: --log_file must have .log suffix.")
        if not p.parent.exists():
            error_exit("Error: --log_file parent directory must exist.")

    # --keyvalue_file
    if args.keyvalue_file:
        p = Path(args.keyvalue_file)
        if p.suffix != ".json":
            error_exit("Error: --keyvalue_file must have .json suffix.")
        if not p.parent.exists():
            error_exit("Error: --keyvalue_file parent directory must exist.")

    # --graph_file
    graph_path = Path(args.graph_file)
    if graph_path.suffix != ".dot":
        error_exit("Error: --graph_file must have .dot suffix.")
    if not graph_path.parent.exists():
        error_exit("Error: --graph_file parent directory must exist.")

    # --output
    if not Path(args.output).is_dir():
        error_exit("Error: --output must be an existing directory.")

    # path (positional)
    if not Path(args.path).is_dir():
        error_exit("Error: positional path must be an existing directory.")


def load_monad(args: argparse.Namespace) -> Dict[str, Any]:
    """Load monad dictionary from keyvalue file or default."""
    if args.keyvalue_file:
        input_path = Path(args.keyvalue_file)
        # If specified, file must exist to be read
        if not input_path.exists():
            error_exit(f"Error: Specified --keyvalue_file does not exist: {input_path}")
    else:
        input_path = Path("syncspec.json")
        # If default, missing file is acceptable (returns empty dict)
        if not input_path.exists():
            return {}

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not all(isinstance(k, str) for k in data.keys()):
                raise ValueError("JSON keys must be strings.")
            return data
    except (json.JSONDecodeError, ValueError, OSError) as e:
        error_exit(f"Error: Failed to load JSON from {input_path}: {e}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--open_delimiter", default="{{")
    parser.add_argument("--close_delimiter", default="}}")
    parser.add_argument("--log_file")
    parser.add_argument("--graph_file", default="syncspec.dot")
    parser.add_argument("--keyvalue_file")
    parser.add_argument("--output", required=True)
    parser.add_argument("--import_path")
    parser.add_argument("path")
    args = parser.parse_args()

    validate_args(args)

    # Setup Logging
    if args.log_file:
        logging.basicConfig(
            filename=args.log_file,
            level=logging.DEBUG,
            format="%(levelname)s - %(message)s"
        )
    else:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(levelname)s - %(message)s"
        )

    # Load Monad
    monad = load_monad(args)

    # Construct Context
    import_path = args.import_path if args.import_path else args.path
    context = SyncspecListContext(
        open_delimiter=args.open_delimiter,
        close_delimiter=args.close_delimiter,
        monad=monad,
        import_path=import_path
    )

    # Create Processor
    try:
        syncspec_list_func = make_syncspec_list(context)
    except ValueError as e:
        error_exit(f"Error: make_syncspec_list failed: {e}")

    # Traverse Input Directory
    text_objects: List[Text] = []
    root_path = Path(args.path)
    try:
        for md_file in root_path.rglob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            relative_name = str(md_file.relative_to(root_path))
            text_objects.append(Text(text=content, name=relative_name))
    except OSError as e:
        error_exit(f"Error: Failed to read markdown files: {e}")

    # Process
    try:
        files, graph, data_dict = syncspec_list_func(text_objects)
    except ValueError as e:
        error_exit(f"Error: syncspec_list failed: {e}")

    # Write Output Files
    output_path = Path(args.output)
    for file_obj in files:
        out_file = output_path / file_obj.name
        try:
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_text(file_obj.text, encoding="utf-8")
        except OSError as e:
            error_exit(f"Error: Failed to write {out_file}: {e}")

    # Write Graph
    try:
        nx.nx_pydot.write_dot(graph, args.graph_file)
    except Exception as e:
        error_exit(f"Error: Failed to write graph {args.graph_file}: {e}")

    # Write JSON State
    output_json_path = Path(args.keyvalue_file) if args.keyvalue_file else Path("syncspec.json")
    try:
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(data_dict, f)
    except Exception as e:
        error_exit(f"Error: Failed to write JSON to {output_json_path}: {e}")


if __name__ == "__main__":
    main()