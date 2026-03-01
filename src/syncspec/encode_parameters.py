from dataclasses import dataclass
from src.syncspec.error import Error


@dataclass
class EncodedParameters:
    text: str
    name: str
    open_delimiter: str
    close_delimiter: str


def encode_parameters(
    text: str,
    name: str = "",
    open_delimiter: str = "{{",
    close_delimiter: str = "}}",
) -> EncodedParameters | Error:
    if not open_delimiter or not close_delimiter:
        return Error("Delimiters cannot be empty strings", name, 1)

    if open_delimiter == close_delimiter:
        return Error("Open and close delimiters must be distinct", name, 1)

    if open_delimiter in close_delimiter or close_delimiter in open_delimiter:
        return Error("Delimiters cannot structurally overlap", name, 1)

    return EncodedParameters(text, name, open_delimiter, close_delimiter)