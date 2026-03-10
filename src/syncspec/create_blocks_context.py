from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class CreateBlocksContext:
	index: int
	prefix: str
	text: str
	line_number: int
