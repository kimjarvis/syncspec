import os
import logging
from typing import List, Union
from pathlib import Path
import pathspec

from syncspec.context import Context
from syncspec.dummy import Dummy
from syncspec.stop import Stop
from syncspec.file_path import FilePath
from syncspec.utilities import format_log_message

logger = logging.getLogger(__name__)

def make_traverse_path(context: Context):
    def traverse_path(fact: Dummy) -> Union[List[FilePath], Stop]:
        # Change 'gitwildmatch' to 'gitignore'
        spec = pathspec.PathSpec.from_lines('gitignore', [])
        if context.ignore_rules_file and context.ignore_rules_file.is_file():
            try:
                lines = context.ignore_rules_file.read_text().splitlines()
                # Manual syntax check for common gitignore errors that pathspec may silently accept
                for line in lines:
                    stripped = line.strip()
                    if stripped and not stripped.startswith('#'):
                        if '[' in stripped and ']' not in stripped:
                            raise ValueError(f"Invalid pattern syntax (unclosed bracket): {stripped}")
                # Change 'gitwildmatch' to 'gitignore'
                spec = pathspec.PathSpec.from_lines('gitignore', lines)
            except Exception as e:
                logger.error(format_log_message(f"Ignore rules compilation failed: {e}", context.ignore_rules_file, 0))
                return Stop()

        input_path = context.input_path.resolve()
        results: List[FilePath] = []

        for root, dirs, files in os.walk(input_path):
            root_p = Path(root).resolve()
            rel_root = root_p.relative_to(input_path)

            kept_dirs = []
            for d in dirs:
                d_p = (root_p / d).resolve()
                if not str(d_p).startswith(str(input_path)):
                    logger.error(format_log_message(f"Directory escapes boundary: {d}", d_p, 0))
                    return Stop()
                if not (spec.match_file(str(rel_root / d)) or spec.match_file(str(rel_root / d) + '/')):
                    kept_dirs.append(d)
            dirs[:] = kept_dirs

            for f in files:
                f_p = (root_p / f).resolve()
                rel_f = f_p.relative_to(input_path)

                if not str(f_p).startswith(str(input_path)):
                    logger.error(format_log_message(f"File escapes boundary: {f}", f_p, 0))
                    return Stop()

                if spec.match_file(str(rel_f)):
                    continue
                if not f_p.is_file() or not os.access(f_p, os.R_OK):
                    continue

                try:
                    with open(f_p, 'rb') as fb:
                        if b'\x00' in fb.read(8192):
                            continue
                except Exception:
                    continue

                try:
                    content = f_p.read_text(encoding='utf-8', errors='ignore')
                    if context.open_delimiter not in content and context.close_delimiter not in content:
                        continue
                except Exception:
                    continue

                results.append(FilePath(path=f_p, text=content))

        return results
    return traverse_path