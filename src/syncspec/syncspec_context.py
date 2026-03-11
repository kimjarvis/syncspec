from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class SyncspecContext:
    open_delimiter: str
    close_delimiter: str
    log_file: str
    graph_file: str