# {{ spec_name }} 

## Functional specification

### Implement the unary function {{ spec_name }}

In the file `src/syncspec/{{spec_file}}.py`.

Define a unary function with signature:

```python
def {{ spec_file }}(parameter: Parameters) -> Response | Error:
```

### Ensure that

- Rule

### Assume that

- Assumption

## Test the unary function  

In the file `tests/test_{{spec_file}}.py`.

- Write pytests to verify the functionality.
- Tests should be individual functions. Do not define a test class.    
- Use `@pytest.mark.parametrize` to create concise tests.  

## Explain the solution  

- Describe any logical inconsistencies in the function specification and suggest improvements. 
- Describe any assumptions that are not explicitly stated in this function specification.

