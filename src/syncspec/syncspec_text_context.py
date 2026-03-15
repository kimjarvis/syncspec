from dataclasses import dataclass, field
from typing import Any, Dict
import networkx as nx

@dataclass
class SyncspecTextContext:
    open_delimiter: str
    close_delimiter: str
    log: str
    G: nx.DiGraph
    monad: Dict[str, Any]
    import_path: str