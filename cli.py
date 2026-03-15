#!/usr/bin/env python3
import argparse
import json
import logging
import sys
from pathlib import Path
from typing import List

import networkx as nx

from src.syncspec.text import Text
from src.syncspec.file import File
from src.syncspec.syncspec_list_context import SyncspecListContext
from src.syncspec.syncspec_list import make_syncspec_list

def fail(msg: str):
    print(msg)
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--open_delimiter', default="{{")
    parser.add_argument('--close_delimiter', default="}}")
    parser.add_argument('--log_file', default="syncspec.log")
    parser.add_argument('--log_level', default="warning")
    parser.add_argument('--graph_file', default="graph.dot")
    parser.add_argument('--keyvalue_file', default="keyvalue.json")
    parser.add_argument('--output', required=True)
    parser.add_argument('--import_path')
    parser.add_argument('path')
    args = parser.parse_args()

    # Validate log_level
    valid_levels = ["debug", "info", "warning", "error", "critical"]
    if args.log_level.lower() not in valid_levels:
        fail(f"Invalid log_level: {args.log_level}")
    log_level = getattr(logging, args.log_level.upper())

    # Validate paths
    log_path = Path(args.log_file)
    graph_path = Path(args.graph_file)
    kv_path = Path(args.keyvalue_file)
    output_path = Path(args.output)
    root_path = Path(args.path)

    if not log_path.parent.exists(): fail(f"Invalid log_file path: {args.log_file}")
    if not kv_path.parent.exists(): fail(f"Invalid keyvalue_file path: {args.keyvalue_file}")
    if not graph_path.parent.exists(): fail(f"Invalid graph_file path: {args.graph_file}")
    if not args.graph_file.endswith('.dot'): fail("graph_file must end with .dot")
    if not output_path.is_dir(): fail(f"output is not a directory: {args.output}")
    if not root_path.is_dir(): fail(f"path is not a directory: {args.path}")

    # Create empty files
    log_path.write_text('', encoding='utf-8')
    kv_path.write_text('', encoding='utf-8')
    graph_path.write_text('', encoding='utf-8')

    # Setup logging
    logging.basicConfig(filename=args.log_file, level=log_level, format="%(levelname)s - %(message)s", filemode='w')

    # Context
    import_path = args.import_path if args.import_path else args.path
    context = SyncspecListContext(
        open_delimiter=args.open_delimiter,
        close_delimiter=args.close_delimiter,
        log_file=args.log_file,
        graph_file=args.graph_file,
        import_path=import_path
    )

    # Factory
    try:
        processor = make_syncspec_list(context)
    except ValueError as e:
        fail(str(e))

    # Traverse
    texts: List[Text] = []
    for md_file in root_path.rglob('*.md'):
        texts.append(Text(
            text=md_file.read_text(encoding='utf-8'),
            name=str(md_file.relative_to(root_path))
        ))

    # Process
    try:
        files, _, graph, kv = processor(texts)
    except ValueError as e:
        fail(str(e))

    # Write Files
    for f in files:
        dest = output_path / f.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(f.text, encoding='utf-8')

    # Write Graph
    nx.nx_pydot.write_dot(graph, args.graph_file)

    # Write JSON
    try:
        with open(args.keyvalue_file, 'w', encoding='utf-8') as f:
            json.dump(kv, f)
    except Exception as e:
        fail(f"JSON conversion failed: {e}")

if __name__ == "__main__":
    main()