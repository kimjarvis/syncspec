from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class Block:
    directive: Dict[str, Any]
    prefix: Optional[str]
    suffix: str
    text: str
    line_number: int