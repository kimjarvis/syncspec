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

def h(a: A, b: B): return C()
def f(x: C): return D()

def build_pipeline(funcs):
    pipeline = []
    for fn in funcs:
        hints = get_type_hints(fn)
        params = list(inspect.signature(fn).parameters.keys())
        # Extract types for first two arguments if available
        t1 = hints.get(params[0]) if len(params) > 0 else None
        t2 = hints.get(params[1]) if len(params) > 1 else None
        pipeline.append((t1, t2, fn))
    return pipeline

def transform(items, pipeline):
    new_items = []
    i = 0
    while i < len(items):
        matched = False
        for t1, t2, fn in pipeline:
            # Check for pair transformation
            if t2 and i + 1 < len(items) and isinstance(items[i], t1) and isinstance(items[i+1], t2):
                new_items.append(fn(items[i], items[i+1]))
                i += 2
                matched = True
                break
            # Check for single transformation (fallback)
            elif not t2 and isinstance(items[i], t1):
                new_items.append(fn(items[i]))
                i += 1
                matched = True
                break
        if not matched:
            new_items.append(items[i])
            i += 1
    return new_items

def main():
    items = [A(), A(), B(), A(), A(), B()]
    pipeline = build_pipeline([h,f])

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