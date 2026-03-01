import re
from dataclasses import dataclass
from ensure_balanced_delimiters import EnsureBalancedDelimiters

@dataclass
class Segment:
    text: str # text content between delimiters
    open_delimiter: str # copied
    close_delimiter: str

def parse_segments(ensure_balanced_delimiters: EnsureBalancedDelimiters) -> list[Segment]:
    pattern = f"{re.escape(ensure_balanced_delimiters.open_delimiter)}|{re.escape(ensure_balanced_delimiters.close_delimiter)}"
    texts = re.split(pattern, ensure_balanced_delimiters.text)
    return [Segment(t, ensure_balanced_delimiters.open_delimiter, ensure_balanced_delimiters.close_delimiter) for t in texts]