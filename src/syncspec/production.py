from src.syncspec.error import Error
from src.syncspec.stop import Stop
import inspect
from typing import get_type_hints


def build_rules(rule_functions):
    rules = []
    for fn in rule_functions:
        hints = get_type_hints(fn)
        params = inspect.signature(fn).parameters
        types = [hints[name] for name in params if name in hints]
        rules.append((types, fn))
    return rules


def apply_rules(facts, rules):
    for f in facts:
        if isinstance(f, (Error, Stop)):
            raise f

    new_facts = []
    i = 0
    # Removed: context.state["length"] = len(facts)

    while i < len(facts):
        # Removed: context.state["index"] = i

        for types, fn in rules:
            n = len(types)
            if i + n <= len(facts) and all(isinstance(x, t) for x, t in zip(facts[i:i + n], types)):
                res = fn(*facts[i:i + n])
                new_facts.extend(res) if isinstance(res, (list, tuple)) else new_facts.append(res)
                i += n
                break
        else:
            new_facts.append(facts[i])
            i += 1
    return new_facts


def production(facts, rules, halt=Stop):
    # Removed: context argument
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
    # except (Error, halt) as e:
    #     print(f"{type(e).__name__}: {e.message}")
    #     return facts
    except Exception as e:
        print(f"Error: {e}")
        return facts