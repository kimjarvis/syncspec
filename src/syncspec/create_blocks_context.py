from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class CreateBlocksContext:
	index: int
	top_directive: str
	text: str
	line_number: int
	name: str