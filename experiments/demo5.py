from dataclasses import dataclass
import inspect
from typing import get_type_hints

@dataclass
class A: id: str = "A"
@dataclass
class B: id: str = "B"
@dataclass
class C: id: str = "C"
@dataclass
class D: id: str = "D"
@dataclass
class E: id: str = "E"
@dataclass
class F: id: str = "F"
@dataclass
class G: id: str = "G"
@dataclass
class H: id: str = "H"

def f(x: D, y: B, z: B): return E()
def g(x: F): return [G(), H()]
def h(a: A, b: B): return C()

def build_pipeline(funcs):
    pipeline = []
    for fn in funcs:
        hints = get_type_hints(fn)
        params = inspect.signature(fn).parameters
        types = [hints[name] for name in params if name in hints]
        pipeline.append((types, fn))
    return pipeline

def transform(items, pipeline):
    new_items = []
    i = 0
    while i < len(items):
        for types, fn in pipeline:
            n = len(types)
            if i + n <= len(items) and all(isinstance(x, t) for x, t in zip(items[i:i+n], types)):
                new_items.append(fn(*items[i:i+n]))
                i += n
                break
        else:
            new_items.append(items[i])
            i += 1
    return new_items

def main():
    items = [A(), A(), B(), A(), A(), B(), D(), B(), B(), F()]
    pipeline = build_pipeline([h, f, g])

    for _ in range(10):
        new_items = transform(items, pipeline)
        if new_items == items:
            break
        items = new_items
    else:
        raise RuntimeError("Exceeded 10 iterations without stabilization")

    print(items)

if __name__ == "__main__":
    main()