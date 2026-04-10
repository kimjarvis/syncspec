# Production

Implement a stateful production system.
## Core Components

Executes the rule engine:

1. Takes an initial list of facts
2. Applies each rule exactly once in registration order
3. Each rule scans all current facts and transforms those matching its expected type
4. Prints the fact list after each rule application
5. Returns the final transformed fact list
## Processing Model

This is a single-pass sequential system:

1. Rules fire exactly once per production run
2. Each rule sees the output of all previous rules
3. No iteration or fixpoint computation (rules don't re-fire)
## Key Characteristics

Type-Based Pattern Matching: Rules trigger based on Python type annotations rather than explicit patterns.

Monolithic Transformation: Each rule completely transforms the entire fact list before the next rule executes.

1:1 or 1:N Transformations: Rules can return:

- A single value (replaces the fact)
- A list/tuple (expands into multiple facts)

Singleton Class Encapsulation: The rule list is private and shared across all instances, allowing incremental rule registration.
### Last field injection

The closure should be able to tell whether it is the last item of its type in the list.

- Iterate through the facts to create a set containing all of the types.
- If the item has a field `last` then set its value to False.
- For each type in the set find the last item of that type in the list.
- Add or replace the field `last` with a boolean with the value True.

## Implementation

Use type hints:

```python
from typing import get_type_hints
```

For type-specific rules, use named functions with explicit type hints rather than lambdas.

<!-- {-  source="package" -} -->
## Package

- The function is part of the python package `src/syncspec` .   
- Imports from the package take the form `from syncspec.x import X`.
- Assume Python version 3.9.

<!-- {--} -->


<!-- {-  source="generate_tests" -} -->
## Write pytests to verify the functionality

- Write tests in a separate file.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

<!-- {--} -->

<!-- {-  source="explain_the_solution" -} -->
## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.

<!-- {--} -->
