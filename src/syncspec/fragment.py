from dataclasses import dataclass
from pathlib import Path

@dataclass
class Fragment:
    path: Path
    text: str
    line_number: int
