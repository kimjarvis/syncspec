import argparse
import sys
from pathlib import Path
from src.syncspec.syncspec_context import SyncspecContext
from src.syncspec.text import Text
from src.syncspec.syncspec import make_syncspec


def validate(args):
    log_path = Path(args.log_file)
    if log_path.exists():
        sys.exit(f"Error: Log file '{args.log_file}' already exists.")

    graph_path = Path(args.graph_file)
    if graph_path.suffix != '.dot':
        sys.exit(f"Error: Graph file '{args.graph_file}' must have .dot suffix.")
    if graph_path.exists():
        sys.exit(f"Error: Graph file '{args.graph_file}' already exists.")

    if not Path(args.output).is_dir():
        sys.exit(f"Error: Output '{args.output}' is not an existing directory.")
    if not Path(args.path).is_dir():
        sys.exit(f"Error: Path '{args.path}' is not an existing directory.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--open_delimiter', default="{{")
    parser.add_argument('--close_delimiter', default="}}")
    parser.add_argument('--log_file', default="log.txt")
    parser.add_argument('--graph_file', default="graph.dot")
    parser.add_argument('--output', required=True)
    parser.add_argument('path')
    args = parser.parse_args()

    validate(args)

    context = SyncspecContext(
        open_delimiter=args.open_delimiter,
        close_delimiter=args.close_delimiter,
        log_file=args.log_file,
        graph_file=args.graph_file
    )

    syncspec = make_syncspec(context)
    base_path = Path(args.path)

    texts = [
        Text(text=p.read_text(encoding='utf-8'), name=str(p.relative_to(base_path)))
        for p in base_path.rglob('*.md')
    ]
    files = syncspec(texts)
    out_path = Path(args.output)

    for f in files:
        dest = out_path / f.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(f.text, encoding='utf-8')


if __name__ == "__main__":
    main()