from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class CombineBlocksContext:
    text: str
    open_delimiter: str
    close_delimiter: str