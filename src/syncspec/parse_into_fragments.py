from dataclasses import dataclass
from typing import Union
import re
from src.syncspec.ensure_balanced_delimiters import BalancedDelimitersEnsured

@dataclass
class Error:
    message: str

@dataclass
class Fragment:
    text: str
    name: str
    open_delimiter: str
    close_delimiter: str

def parse_into_fragments(ensure_balanced_delimiters: BalancedDelimitersEnsured) -> Union[list[Fragment], Error]:
    try:
        pattern = f"{re.escape(ensure_balanced_delimiters.open_delimiter)}|{re.escape(ensure_balanced_delimiters.close_delimiter)}"
        parts = re.split(pattern, ensure_balanced_delimiters.text)
        return [
            Fragment(
                text=part,
                name=ensure_balanced_delimiters.name,
                open_delimiter=ensure_balanced_delimiters.open_delimiter,
                close_delimiter=ensure_balanced_delimiters.close_delimiter
            )
            for part in parts if part
        ]
    except Exception as e:
        return Error(message=str(e))