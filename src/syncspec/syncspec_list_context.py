from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class SyncspecListContext:
    open_delimiter: str
    close_delimiter: str
    monad: Dict[str, Any]
    import_path: str