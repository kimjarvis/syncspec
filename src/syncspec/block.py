from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Block:
    text: str
    line_number: int