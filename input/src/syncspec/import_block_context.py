from dataclasses import dataclass, field
from typing import ClassVar, Dict, Any

@dataclass
class ImportBlockContext:
    import_path: str
    open_delimiter: str
    close_delimiter: str