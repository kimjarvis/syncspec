
<!-- {- import="../src/syncspec/production.py",  head=2,  tail=2 -} -->
```python
import inspect
from typing import Any, Callable, List, Sequence, Tuple, get_type_hints
from collections import Counter
from syncspec.stop import Stop


def build_rules(rule_functions: Sequence[Callable[[Any], Any]]) -> List[Tuple[type, Callable[[Any], Any]]]:
    return [
        (get_type_hints(fn).get(next(iter(inspect.signature(fn).parameters)), object), fn)
        for fn in rule_functions
    ]


def _update_state(fn: Callable, key: str, value: Any) -> None:
    if hasattr(fn, '__closure__') and fn.__closure__:
        for cell in fn.__closure__:
            try:
                content = cell.cell_contents
                if isinstance(content, dict) and key in content:
                    content[key] = value
                    return
            except ValueError:
                pass


def production(facts: List[Any], rules: List[Tuple[type, Callable[[Any], Any]]]) -> List[Any]:
    for rule_type, fn in rules:
        new_facts: List[Any] = []
        matches = [f for f in facts if isinstance(f, rule_type)]
        match_counts = Counter(type(f) for f in matches)
        current_counts = Counter()

        facts = [f for f in facts if f is not None]
        for fact in facts:
            if isinstance(fact, rule_type):
                current_counts[type(fact)] += 1
                is_last = current_counts[type(fact)] == match_counts[type(fact)]
                _update_state(fn, 'last', is_last)

                res = fn(fact)
                new_facts.extend(res) if isinstance(res, (list, tuple)) else new_facts.append(res)
            else:
                new_facts.append(fact)
        facts = new_facts
        if any(isinstance(fact, Stop) for fact in facts):
            break
    return facts
```
<!-- {--} -->

```python
def make_example_coroutine(context: Context):
    state = {'index': 0, 'last': False}

    def example_coroutine(fact: Dummy) -> Dummy:
        state['index'] += 1
        print(state['index'])
        if state['last']:
            print("last")
        return Dummy()

    return example_coroutine
```

Modify `production` to set `state.last` to True when:

The fact is the last item, of its type, in the list of facts.   For example if the initial facts are:
`[Dummy(),Freddy(),Dummy()]` Then `state.last==True` in the object of type Freddy and the last object of type Dummy in the list.  It is False in the first item of type Dummy.

This shall be done on each iteration of the loop through the rules.


<!-- {-  include="explain_the_solution" -} -->
## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.

<!-- {--} -->
