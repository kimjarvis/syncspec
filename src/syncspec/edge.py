from dataclasses import dataclass

@dataclass
class Edge:
    directive_type: str
    key: str
    line_number: int
    name: str
