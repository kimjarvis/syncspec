from dataclasses import dataclass
import inspect
from typing import get_type_hints

@dataclass
class A: id: str = "A"
@dataclass
class B: id: str = "B"
@dataclass
class C: id: str = "C"

def f(x: A): return B()

def g(x: B):
    g.calls.append(x.id)
    return C()
g.calls = []

def build_pipeline(funcs):
    get_in = lambda fn: get_type_hints(fn)[next(iter(inspect.signature(fn).parameters))]
    return [(get_in(fn), fn) for fn in funcs]

def transform(item, pipeline):
    for in_type, fn in pipeline:
        if isinstance(item, in_type):
            res = fn(item)
            return res if isinstance(res, (list, tuple)) else [res]
    return [item]

def main():
    items = [A(), A()]
    pipeline = build_pipeline([f, g])

    for _ in range(10):
        new_items = [res for i in items for res in transform(i, pipeline)]
        if new_items == items:
            break
        items = new_items
    else:
        raise RuntimeError("Exceeded 10 iterations without stabilization")

    print(f"Final items: {items}")
    print(f"g call count: {len(g.calls)} (ids: {g.calls})")

if __name__ == "__main__":
    main()