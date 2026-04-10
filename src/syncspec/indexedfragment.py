from dataclasses import dataclass
from pathlib import Path

@dataclass
class IndexedFragment:
    path: Path
    text: str
    line_number: int
    index: int
