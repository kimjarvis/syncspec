from dataclasses import dataclass
from typing import ClassVar, Dict, Any

@dataclass
class Monad:
    state: ClassVar[Dict[str, Dict[str, Any]]] = {}
