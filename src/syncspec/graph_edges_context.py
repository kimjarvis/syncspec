from dataclasses import dataclass, field
from typing import Any, Dict
import networkx as nx

@dataclass
class GraphEdgesContext:
	G: nx.DiGraph