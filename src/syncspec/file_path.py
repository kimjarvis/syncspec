from dataclasses import dataclass
from pathlib import Path

@dataclass
class FilePath:
    path: Path
    text: str
