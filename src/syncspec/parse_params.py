import ast
import re


def parse_params(param_str: str) -> dict:
    params = {}
    # Matches: key="quoted", key=123, key=True
    pattern = re.compile(r'(\w+)\s*=\s*("(?:[^"\\]|\\.)*"|[^,]+)')

    for m in pattern.finditer(param_str):
        key, raw_val = m.group(1), m.group(2).strip()
        try:
            params[key] = ast.literal_eval(raw_val)
        except (ValueError, SyntaxError):
            params[key] = raw_val  # Fallback to raw string
    return params


# Example
s = 'import="../src/syncspec/context.py", head=2, eol=True'
print(parse_params(s))
# {'import': 'src/syncspec/context.py', 'head': 2, 'eol': True}
