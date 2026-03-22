from dataclasses import dataclass

@dataclass
class AddGraphNodesParameter:
    directive_type: str
    key: str
    line_number: int
    name: str