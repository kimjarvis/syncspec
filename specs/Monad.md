When traversing a list it is necessary to know whether the function is acting on the last item in the list.  
The list length shall be available to each function in a key value store, which we call a monad.

It should not be necessary to explain the structure of the monad to AI.   

There are two ways of doing this, single memory copy or multiple memory copies.  Single is clearly the most efficient.

Each parameter class shall inherit from monad.  Monad shall point to a singleton ?

```
from dataclasses import dataclass
from typing import ClassVar, Dict, Any

@dataclass
class Monad:
    state: ClassVar[Dict[str, Dict[str, Any]]] = {}
```

## Error class

The class Error is special because its presence in the list stops the execution.

The aim of the Error class is to make unary functions responsible for catching their own errors.  

Exit the loop if the class Error is present in the list or is a parent of any of the classes in the list.




