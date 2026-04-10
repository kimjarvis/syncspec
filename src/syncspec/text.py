from dataclasses import dataclass
from pathlib import Path

@dataclass
class Text:
    path: Path
    text: str
    line_number: int