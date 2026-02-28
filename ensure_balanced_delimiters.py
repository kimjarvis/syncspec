from dataclasses import dataclass
from encode_parameters import EncodeParameters
from error import Error


@dataclass
class EnsureBalancedDelimiters:
    data: str = ""
    open_delimiter: str = "{{"
    close_delimiter: str = "}}"


def ensure_balanced_delimiters(encode_parameters: EncodeParameters) -> EnsureBalancedDelimiters | Error:
    try:
        data = encode_parameters.data
        open_del = encode_parameters.open_delimiter
        close_del = encode_parameters.close_delimiter
        open_len, close_len = len(open_del), len(close_del)

        i, found_open = 0, False
        while i < len(data):
            if data[i:i + open_len] == open_del:
                if found_open:
                    raise ValueError("Delimiters are nested")
                found_open = True
                i += open_len
            elif data[i:i + close_len] == close_del:
                if not found_open:
                    raise ValueError("Delimiters are not matched")
                found_open = False
                i += close_len
            else:
                i += 1

        if found_open:
            raise ValueError("Delimiters are not matched")

        return EnsureBalancedDelimiters(data=data, open_delimiter=open_del, close_delimiter=close_del)
    except ValueError as e:
        return Error(message=str(e))