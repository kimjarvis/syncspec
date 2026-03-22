from dataclasses import dataclass

@dataclass
class GraphNode:
    directive_type: str
    key: str
    line_number: int
    name: str
