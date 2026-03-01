from dataclasses import dataclass
import inspect
from typing import get_type_hints
from functools import reduce
from itertools import chain

@dataclass
class A: id: str = "A"
@dataclass
class B: id: str = "B"
@dataclass
class C: id: str = "C"

def f(x: A): return B()
def g(x: B): return C()

def build_pipeline(funcs):
    get_in = lambda fn: get_type_hints(fn)[next(iter(inspect.signature(fn).parameters))]
    return list(map(lambda fn: (get_in(fn), fn), funcs))

def transform(item, pipeline):
    match = next(filter(lambda t_fn: isinstance(item, t_fn[0]), pipeline), None)
    res = match[1](item) if match else item
    return res if isinstance(res, (list, tuple)) else [res]

def main():
    items = [A(), A()]
    pipeline = build_pipeline([f, g])

    def step(state, _):
        items, stable = state
        if stable: return state
        new_items = list(chain.from_iterable(map(lambda i: transform(i, pipeline), items)))
        return (new_items, new_items == items)

    items, stable = reduce(step, range(10), (items, False))
    if not stable:
        raise RuntimeError("Exceeded 10 iterations without stabilization")
    print(items)

if __name__ == "__main__":
    main()