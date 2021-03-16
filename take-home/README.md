# Simple in-memory database

## Take home assignment from Metabase

The code in this repository implements a simple in memory database in Python, according to the specs obtained from Metabase. This implementation was done as a part of the take-home challenge, during an interview process.

## Approach

The approach taken is to implement all the parts of the database as functional objects. There's no mutable state involved and thus somewhat functional (even though in Python). The proliferating `@property` serves to demonstrate the fact that the objects are just functional objects, and that they have no state. In production code, this would be `@lazyproperty` which is also idempotent.

## Implementation

There are a couple of important classes which implement the functionality:

- Expr is a base class for all expressions of the filter part of the query
- Filter is a class that performs filtering by evaluating each record for the filter expression
- Query is the main class that binds everything together

## Testing

Tests can be started by running `pytest` from the `take-home/` directory. Tests in the file `test_examples.py` represent the examples specified in the assignment itself, as obtained in the instructions. The tests in the file `test_for_tdd.py` served as the driving mechanism for the implementation.
