Import this class from file `src/syncspec/combine_nodes_context.py`:
<!-- {= "source": "combine_nodes_context", "head": 1, "tail": 1 =} -->
from dataclasses import dataclass, field
from typing import Any, Dict
import networkx as nx

@dataclass
class CombineNodesContext:
	G: nx.DiGraph
<!-- {==} -->
