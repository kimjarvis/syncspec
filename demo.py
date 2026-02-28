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


def g(x: B): return C()


def build_pipeline(funcs):
    pipeline = []
    for fn in funcs:
        params = inspect.signature(fn).parameters
        in_type = get_type_hints(fn)[next(iter(params))]
        pipeline.append((in_type, fn))
    return pipeline


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
        print(items)
        new_items = []
        for i in items:
            new_items.extend(transform(i, pipeline))
        if new_items == items:
            break
        items = new_items
    else:
        raise RuntimeError("Exceeded 10 iterations without stabilization")


if __name__ == "__main__":
    main()