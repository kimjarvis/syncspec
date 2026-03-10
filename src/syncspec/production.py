from src.syncspec.error import Error
from src.syncspec.stop import Stop
import inspect
from typing import get_type_hints


def build_rules(rule_functions):
    """Extracts the single input type hint for each unary rule."""
    rules = []
    for fn in rule_functions:
        hints = get_type_hints(fn)
        param_name = next(iter(inspect.signature(fn).parameters))
        rules.append((hints.get(param_name, object), fn))
    return rules


def apply_rules(facts, rules):
    """Applies the first matching unary rule to each fact."""
    new_facts = []
    for fact in facts:
        if isinstance(fact, (Error, Stop)):
            raise fact

        for match_type, fn in rules:
            if isinstance(fact, match_type):
                res = fn(fact)
                new_facts.extend(res) if isinstance(res, (list, tuple)) else new_facts.append(res)
                break
        else:
            new_facts.append(fact)
    return new_facts


def production(facts, rules):
    """Runs rules until stabilization or max iterations."""
    for _ in range(10):
        new_facts = apply_rules(facts, rules)
        if new_facts == facts:
            return facts
        facts = new_facts
    raise RuntimeError("Exceeded 10 iterations without stabilization")