from dataclasses import dataclass

@dataclass
class Error:
    message: str
    name: str
    line: int