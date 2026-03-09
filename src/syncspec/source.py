from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Source:
    directive: Dict[str, Any]
    text: str
    line_number: int