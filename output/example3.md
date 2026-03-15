Include file `sub/error.py`:
Before{{"import": "sub/error.py", "head": 2, "tail": 2}}
```python
from dataclasses import dataclass

@dataclass
class Error:
    message: str
    name: str
    line_number: int
```
 {{}}After
Last