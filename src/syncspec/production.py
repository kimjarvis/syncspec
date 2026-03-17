import inspect
from typing import get_type_hints

def build_rules(rule_functions):
    return [
        (get_type_hints(fn).get(next(iter(inspect.signature(fn).parameters)), object), fn)
        for fn in rule_functions
    ]

def production(facts, rules):
    for rule_type, fn in rules:
        new_facts = []
        for fact in facts:
            if isinstance(fact, rule_type):
                res = fn(fact)
                new_facts.extend(res) if isinstance(res, (list, tuple)) else new_facts.append(res)
            else:
                new_facts.append(fact)
        # print(facts)
        facts = new_facts
    return facts