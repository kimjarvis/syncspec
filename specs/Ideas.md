
The starting conditions in encode_parameters should produce a single object with the target and the delimiters.  State does not need to be injected.

Key value objects can be injected into the list by each chunk and then collected into a dictionary using a reduce operation.  A reference to the dictionary can then be propagated to all the objects in the list.

When the processing has finished the list should be a single object containing the text and the dictionary. 


Stop can be removed by specifying a final class in the main.