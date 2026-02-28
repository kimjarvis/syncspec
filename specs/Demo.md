Extend the demo, which is a map operation. 


Function f transforms A() into B().

I want a function h that transform pairs A(), B() into D()

For example:

items = [A(), B(), A(), A(), B()]  
pipeline = build_pipeline([h])

Prints

[D(), A(), D()]  