from dataclasses import dataclass
import inspect
from typing import get_type_hints
import pprint

from src.syncspec.ensure_balanced_delimiters import ensure_balanced_delimiters
from src.syncspec.encode_parameters import encode_parameters
from src.syncspec.parse_into_fragments import parse_into_fragments
from src.syncspec.fragments_to_tracker import fragments_to_tracker

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
    ep = encode_parameters("""A{{B}}C{{D}}E{{F}}G{{H}}I""", "test_name", "{{", "}}")
    print(ep)


    facts = [ep]
    rules = build_rules([ensure_balanced_delimiters,
                         parse_into_fragments,
                         fragments_to_tracker,
                         ])
    result = production(facts, rules)
    pprint.pp(result)

if __name__ == "__main__":
    main()