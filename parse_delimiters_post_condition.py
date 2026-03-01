from dataclasses import dataclass
from ensure_balanced_delimiters import ensure_balanced_delimiters

@dataclass
class EnsureBalancedDelimiters:
    text: str
    open_delimiter: str
    close_delimiter: str

@dataclass
class ParseDelimiters:
    delimited_substring: str # delimited substring of text
    open_delimiter: str # copied
    close_delimiter: str

def parse_delimiters(x: EnsureBalancedDelimiters) -> list[ParseDelimiters]:
    pass

def test_parse_delimiters():
    e = EnsureBalancedDelimiters(text="A{{B}}C", open_delimiter="{{", close_delimiter="}}")
    p = [ParseDelimiters(delimited_substring="A", open_delimiter="{{", close_delimiter="}}"),
         ParseDelimiters(delimited_substring="B", open_delimiter="{{", close_delimiter="}}"),
         ParseDelimiters(delimited_substring="C", open_delimiter="{{", close_delimiter="}}")]
    assert(parse_delimiters(e)==p)
