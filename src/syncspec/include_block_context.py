from dataclasses import dataclass, field
from typing import ClassVar, Dict, Any

@dataclass
class IncludeBlockContext:
    state: Dict[str, Any]
    open_delimiter: str
    close_delimiter: str