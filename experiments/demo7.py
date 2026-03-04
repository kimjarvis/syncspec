from dataclasses import dataclass
import inspect
from typing import get_type_hints

@dataclass
class A: pass
class B(A): pass
class C(A): pass
class D(A): pass
class E(A): pass
class F(A): pass
class G(A): pass
class H(A): pass

def f(x: D, y: B, z: B): return E()
def g(x: F): return [G(), H()]
def h(a: A, b: B): return C()

def build_rules(rule_functions):
    rules = []
    for fn in rule_functions:
        hints = get_type_hints(fn)
        params = inspect.signature(fn).parameters
        types = [hints[name] for name in params if name in hints]
        rules.append((types, fn))
    return rules

def apply_rules(facts, rules):
    new_facts = []
    i = 0
    while i < len(facts):
        for types, fn in rules:
            n = len(types)
            if i + n <= len(facts) and all(isinstance(x, t) for x, t in zip(facts[i:i+n], types)):
                res = fn(*facts[i:i+n])
                new_facts.extend(res) if isinstance(res, (list, tuple)) else new_facts.append(res)
                i += n
                break
        else:
            new_facts.append(facts[i])
            i += 1
    return new_facts

def production(facts, rules):
    try:
        if not isinstance(facts, list):
            raise TypeError("facts must be a list")
        for _, fn in rules:
            if not callable(fn):
                raise TypeError("rules must be callable")

        for _ in range(10):
            new_facts = apply_rules(facts, rules)
            if new_facts == facts:
                break
            facts = new_facts
        else:
            raise RuntimeError("Exceeded 10 iterations without stabilization")

        return facts
    except Exception as e:
        print(f"Error: {e}")
        return facts

def main():
    facts = [A(), A(), B(), A(), A(), B(), D(), B(), B(), F()]
    rules = build_rules([h, f, g])
    result = production(facts, rules)
    print(result)

if __name__ == "__main__":
    main()