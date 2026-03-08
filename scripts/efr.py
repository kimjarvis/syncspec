#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
from jinja2 import Template

# Base path defined globally to allow patching in tests
BASE = Path("/home/kim/syncspec")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="efr.py")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--add", action="store_true", help="Add spec files")
    group.add_argument("--remove", action="store_true", help="Remove spec files")
    parser.add_argument("spec_name", help="Specification name")

    args = parser.parse_args(argv)

    # Validate spec_name
    forbidden_chars = ['.', '/', '\n']
    if any(c in args.spec_name for c in forbidden_chars):
        raise ValueError(f"Invalid spec_name: contains forbidden characters {forbidden_chars}")

    spec_file = args.spec_name.lower().replace(" ", "_")

    # Define paths
    dir_specs = BASE / "specs"
    dir_src = BASE / "src" / "syncspec"
    dir_tests = BASE / "tests"
    dir_scripts = BASE / "scripts"

    file_template = dir_scripts / "template.md"
    file_specs_md = dir_specs / f"{args.spec_name}.md"
    file_src_py = dir_src / f"{spec_file}.py"
    file_tests_py = dir_tests / f"test_{spec_file}.py"

    # Verify common directories exist
    for d in [dir_specs, dir_src, dir_tests]:
        if not d.is_dir():
            raise FileNotFoundError(f"Directory missing: {d}")

    if args.add:
        # Verify template exists
        if not file_template.is_file():
            raise FileNotFoundError(f"Template missing: {file_template}")

        # Atomic Check: Verify targets do NOT exist
        targets = [file_specs_md, file_src_py, file_tests_py]
        for f in targets:
            if f.exists():
                raise FileExistsError(f"File already exists: {f}")

        # Render template
        template_content = file_template.read_text()
        jinja_template = Template(template_content)
        rendered_md = jinja_template.render(spec_name=args.spec_name, spec_file=spec_file)

        # Atomic Write: Create all files
        file_specs_md.write_text(rendered_md)
        file_src_py.touch()
        file_tests_py.touch()

    elif args.remove:
        # Note: Prompt specified tests/{spec_file}.py for remove, but tests/test_{spec_file}.py for add.
        # We align to test_{spec_file}.py for consistency so remove actually removes what add created.
        targets = [file_src_py, file_tests_py]

        # Atomic Check: Verify targets EXISTS
        for f in targets:
            if not f.exists():
                raise FileNotFoundError(f"File missing for removal: {f}")

        # Atomic Delete: Remove all files
        for f in targets:
            f.unlink()


if __name__ == "__main__":
    try:
        main()
    except (ValueError, FileNotFoundError, FileExistsError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)