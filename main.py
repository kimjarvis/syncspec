import argparse
import sys
from pathlib import Path
from src.syncspec.syncspec import make_syncspec
from src.syncspec.syncspec_context import SyncspecContext
from src.syncspec.text import Text


def err(msg):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--open_delimiter', default="{{")
    p.add_argument('--close_delimiter', default="}}")
    p.add_argument('--log_file', default="log.txt")
    p.add_argument('--graph_file', default="graph.dot")
    p.add_argument('--output', required=True)
    p.add_argument('--import_path')
    p.add_argument('path')
    args = p.parse_args()

    if Path(args.log_file).exists(): err(f"log_file {args.log_file} exists.")
    if Path(args.graph_file).exists(): err(f"graph_file {args.graph_file} exists.")
    if Path(args.graph_file).suffix != '.dot': err(f"graph_file {args.graph_file} needs .dot suffix.")
    if not Path(args.output).is_dir(): err(f"output {args.output} is not a directory.")
    if not Path(args.path).is_dir(): err(f"path {args.path} is not a directory.")

    import_path = args.import_path if args.import_path else args.path
    if not Path(import_path).is_dir(): err(f"import_path {import_path} is not a directory.")

    ctx = SyncspecContext(
        open_delimiter=args.open_delimiter,
        close_delimiter=args.close_delimiter,
        log_file=args.log_file,
        graph_file=args.graph_file,
        import_path=import_path
    )

    syncspec = make_syncspec(ctx)
    root = Path(args.path)
    texts = [Text(text=f.read_text(), name=str(f.relative_to(root))) for f in root.rglob("*.md")]

    for file in syncspec(texts):
        out = Path(args.output) / file.name
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(file.text)


if __name__ == "__main__":
    main()