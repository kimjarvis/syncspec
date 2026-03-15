from dataclasses import dataclass

@dataclass
class Node:
    directive_type: str
    key: str
    line_number: int
    name: str
