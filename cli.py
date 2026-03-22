#!/usr/bin/env python3
import argparse
import json
import logging
import sys
from pathlib import Path
from typing import List, Dict, Any

import networkx as nx

from src.syncspec.text import Text
from src.syncspec.parameter_file import File
from src.syncspec.syncspec_list_context import SyncspecListContext
from src.syncspec.syncspec_list import make_syncspec_list


def validate_delimiters(open_del: str, close_del: str) -> None:
    if not open_del or not close_del:
        sys.exit("Error: Delimiters cannot be empty strings.")
    if "\n" in open_del or "\n" in close_del:
        sys.exit("Error: Delimiters cannot contain newlines.")
    if open_del == close_del:
        sys.exit("Error: Delimiters must be distinct.")
    if open_del in close_del or close_del in open_del:
        sys.exit("Error: Delimiters cannot overlap structurally.")


def validate_path_suffix(path: Path, suffix: str, label: str) -> None:
    if path.suffix != suffix:
        sys.exit(f"Error: {label} must have suffix {suffix}.")
    if not path.parent.exists():
        sys.exit(f"Error: Parent directory for {label} does not exist.")


def validate_dir(path: Path, label: str) -> None:
    if not path.exists() or not path.is_dir():
        sys.exit(f"Error: {label} must be an existing directory.")


def load_json_state(path: Path) -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            sys.exit("Error: State file must contain a JSON object.")
        if not all(isinstance(k, str) for k in data.keys()):
            sys.exit("Error: State file keys must be strings.")
        return data
    except json.JSONDecodeError as e:
        sys.exit(f"Error: Invalid JSON in state file: {e}")
    except Exception as e:
        sys.exit(f"Error: Failed to read state file: {e}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--open_delimiter", default="{{")
    parser.add_argument("--close_delimiter", default="}}")
    parser.add_argument("--log_file", type=Path)
    parser.add_argument("--graph_file", type=Path, default=Path("syncspec.dot"))
    parser.add_argument("--keyvalue_file", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--import_path", type=Path)
    parser.add_argument("path", type=Path)

    args = parser.parse_args()

    # Validate Delimiters
    try:
        validate_delimiters(args.open_delimiter, args.close_delimiter)
    except SystemExit:
        raise
    except Exception as e:
        sys.exit(f"Error: Delimiter validation failed: {e}")

    # Validate Paths
    validate_dir(args.output, "--output")
    validate_dir(args.path, "path")

    if args.log_file:
        validate_path_suffix(args.log_file, ".log", "--log_file")

    validate_path_suffix(args.graph_file, ".dot", "--graph_file")

    if args.keyvalue_file:
        validate_path_suffix(args.keyvalue_file, ".json", "--keyvalue_file")

    # Setup Logging
    log_handlers = []
    if args.log_file:
        log_handlers.append(logging.FileHandler(args.log_file, encoding="utf-8"))
    else:
        log_handlers.append(logging.StreamHandler())

    logging.basicConfig(
        handlers=log_handlers,
        format="%(levelname)s - %(message)s",
        level=logging.WARNING
    )

    # Load State
    state_dict = {}
    if args.keyvalue_file:
        state_dict = load_json_state(args.keyvalue_file)
    else:
        default_state = Path("syncspec.json")
        if default_state.exists():
            state_dict = load_json_state(default_state)

    # Construct Context
    import_path = args.import_path if args.import_path else args.path
    context = SyncspecListContext(
        open_delimiter=args.open_delimiter,
        close_delimiter=args.close_delimiter,
        monad=state_dict,
        import_path=str(import_path)
    )

    # Traverse Markdown Files
    text_objects: List[Text] = []
    try:
        for md_file in args.path.rglob("*.md"):
            if md_file.is_file():
                content = md_file.read_text(encoding="utf-8")
                rel_name = str(md_file.relative_to(args.path))
                text_objects.append(Text(text=content, name=rel_name))
    except Exception as e:
        sys.exit(f"Error: Failed to traverse directory: {e}")

    # Execute Syncspec
    try:
        syncspec_fn = make_syncspec_list(context)
        files, graph, new_state = syncspec_fn(text_objects)
    except ValueError as e:
        sys.exit(f"Error: Syncspec execution failed: {e}")
    except Exception as e:
        sys.exit(f"Error: Unexpected error during syncspec: {e}")

    # Write Output Files
    try:
        for file_obj in files:
            out_path = args.output / file_obj.name
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(file_obj.text, encoding="utf-8")
    except Exception as e:
        sys.exit(f"Error: Failed to write output files: {e}")

    # Write Graph
    try:
        nx.nx_pydot.write_dot(graph, args.graph_file)
    except Exception as e:
        sys.exit(f"Error: Failed to write graph file: {e}")

    # Write State
    try:
        if not all(isinstance(k, str) for k in new_state.keys()):
            sys.exit("Error: Output state keys must be strings.")

        out_state_path = args.keyvalue_file if args.keyvalue_file else Path("syncspec.json")
        with open(out_state_path, "w", encoding="utf-8") as f:
            json.dump(new_state, f)
    except Exception as e:
        sys.exit(f"Error: Failed to write state file: {e}")


if __name__ == "__main__":
    main()