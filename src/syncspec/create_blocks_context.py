from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class CreateBlocksContext:
	index: int
	prefix: str
	prefix_line_number: int
	prefix_valid: bool
	directive: Dict[str, Any]
	text: str
	open_delimiter: str
	close_delimiter: str

