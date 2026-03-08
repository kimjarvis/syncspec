from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class ValidateTextContext:
    name: str
    open_delimiter: str
    close_delimiter: str
    line_number: int