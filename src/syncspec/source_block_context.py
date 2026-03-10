from dataclasses import dataclass, field
from typing import ClassVar, Dict, Any

@dataclass
class SourceBlockContext:
    state: Dict[str, Any]
    open_delimiter: str
    close_delimiter: str