import argparse
import json
import sys
from pathlib import Path

import networkx as nx

from src.syncspec.text import Text
from src.syncspec.syncspec_list_context import SyncspecListContext
from src.syncspec.syncspec_list import make_syncspec_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=str)
    parser.add_argument("--open_delimiter", default="{{")
    parser.add_argument("--close_delimiter", default="}}")
    parser.add_argument("--log_file", default="log.txt")
    parser.add_argument("--graph_file", default="graph.dot")
    parser.add_argument("--keyvalue_file", default="keyvalue.json")
    parser.add_argument("--output", required=True)
    parser.add_argument("--import_path", default=None)

    args = parser.parse_args()

    # Validate paths
    path = Path(args.path)
    if not path.is_dir():
        print(f"Error: path '{args.path}' is not an existing directory.")
        sys.exit(1)

    output = Path(args.output)
    if not output.is_dir():
        print(f"Error: output '{args.output}' is not an existing directory.")
        sys.exit(1)

    log_file = Path(args.log_file)
    graph_file = Path(args.graph_file)
    keyvalue_file = Path(args.keyvalue_file)

    for f_path, name in [(log_file, "log_file"), (keyvalue_file, "keyvalue_file"), (graph_file, "graph_file")]:
        if not f_path.parent.exists():
            print(f"Error: {name} parent directory does not exist.")
            sys.exit(1)
        if name == "graph_file" and f_path.suffix != ".dot":
            print(f"Error: graph_file must have .dot suffix.")
            sys.exit(1)
        f_path.touch()

    import_path = args.import_path if args.import_path else args.path

    try:
        context = SyncspecListContext(
            open_delimiter=args.open_delimiter,
            close_delimiter=args.close_delimiter,
            log_file=args.log_file,
            graph_file=args.graph_file,
            import_path=import_path
        )
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    try:
        syncspec_list = make_syncspec_list(context)

        texts = []
        for md_file in path.rglob("*.md"):
            texts.append(Text(text=md_file.read_text(encoding="utf-8"), name=str(md_file.relative_to(path))))

        files, log_str, graph, kv_dict = syncspec_list(texts)

        for file_obj in files:
            out_path = output / file_obj.name
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(file_obj.text, encoding="utf-8")

        log_file.write_text(log_str, encoding="utf-8")
        nx.nx_pydot.write_dot(graph, str(graph_file))

        try:
            keyvalue_file.write_text(json.dumps(kv_dict), encoding="utf-8")
        except Exception as e:
            print(f"Error: JSON conversion failed - {e}")
            sys.exit(1)

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()