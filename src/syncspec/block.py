from dataclasses import dataclass
from pathlib import Path

@dataclass
class Block:
    prefix: str
    text: str
    suffix: str
    path: Path
    prefix_line_number: int
    text_line_number: int
    suffix_line_number: int
