from dataclasses import dataclass
from error import Error

@dataclass
class EncodeParameters:
    data: str = ""
    open_delimiter: str = "{{"
    close_delimiter: str = "}}"

    def __post_init__(self):
        if not self.open_delimiter or not self.close_delimiter:
            raise ValueError("Empty delimiter")
        if self.open_delimiter == self.close_delimiter:
            raise ValueError("Equal delimiters")

def encode_parameters(data: str, open_delimiter: str, close_delimiter: str) -> EncodeParameters | Error:
    try:
        return EncodeParameters(data, open_delimiter, close_delimiter)
    except ValueError as e:
        return Error(str(e))