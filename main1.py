import argparse
from pathlib import Path
from src.syncspec.syncspec import make_syncspec
from src.syncspec.syncspec_context import SyncspecContext
from src.syncspec.text import Text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--open_delimiter", default="{{")
    parser.add_argument("--close_delimiter", default="}}")
    parser.add_argument("--log_file", default="log.txt")
    parser.add_argument("--graph_file", default="graph.dot")
    parser.add_argument("--output", required=True)
    parser.add_argument("path")
    args = parser.parse_args()

    out_path = Path(args.output)
    src_path = Path(args.path)

    if not out_path.is_dir(): raise FileNotFoundError(f"Output dir not found: {out_path}")
    if not src_path.is_dir(): raise FileNotFoundError(f"Source dir not found: {src_path}")

    ctx = SyncspecContext(args.open_delimiter, args.close_delimiter, args.log_file, args.graph_file)
    syncspec = make_syncspec(ctx)

    texts = []
    for file in src_path.rglob("*.md"):
        texts.append(Text(name=str(file.relative_to(src_path)), text=file.read_text()))

    print(texts)
    results = syncspec(texts)
    print(results)

    for res in results:
        dest = out_path / res.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(res.text)


if __name__ == "__main__":
    main()