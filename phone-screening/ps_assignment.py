import pytest

# Making Change
# Given a number "x" and a sorted array of coins "coinset", write a function
# that returns the amounts for each coin in the coinset that sums up to X or
# indicate an error if there is no way to make change for that x with the given
# coinset. For example, with x=7 and a coinset of [1,5,10,25], a valid answer
# would be {1: 7} or {1: 2, 5: 1}. With x = 3 and a coinset of [2,4] it should
# indicate an error. Bonus points for optimality.

# Use the following examples to test it out

# A. x = 6 coinset = [1,5,10,25]
# B. x = 6, coinset = [3,4]
# C. x = 6, coinset = [1,3,4]
# D. x = 6, coinset = [5,7]


def make_change(x, coinset):
    """return dict(int, int) of coin values with corresponding repetitions."""

    if not coinset or x < 0:
        # --- Tackle the base case of wrong inputs
        return {}

    curr = coinset[0]
    if x % curr == 0:
        # --- This case terminates the recursion, essentially implementing the greedy
        # --- algorithm, since it terminates as soon as it meets the input criterion.
        reps = x // curr
        return {curr: reps}

    quot = x // curr  # max times we can stuff the current coin into remaining sum
    for i in range(1, quot + 1):
        # --- Decrease remaining sum by a multiple of current coin.
        remaining = x - i * curr
        # --- Then try the reduction of the remaining sum recursively
        # --- with remaining coins.
        reduced = make_change(remaining, coinset[1:])
        if not reduced:
            # --- Can't be reduced by remaining coins, try another multiple
            # --- of the current coin
            continue

        # --- Successfully reduced the remaining sum with remaining coins.
        # --- Combine that result with the multiple of the current coin.
        return {**{curr: i}, **reduced}

    return {}  # couldn't reduce, return empty dict


@pytest.mark.parametrize(
    "x, coins, expectation",
    (
        (0, [], {}),
        (-1, [1, 5, 10, 25], {}),
        (0, [1, 5, 10, 25], {1: 0}),
        (6, [1, 5, 10, 25], {1: 6}),
        (7, [2, 5, 10, 25], {2: 1, 5: 1}),
        (7, [2, 3, 10, 25], {2: 2, 3: 1}),
        (6, [3, 4], {3: 2}),
        (6, [1, 3, 4], {1: 6}),
        (6, [5, 7], {}),
        (9, [2, 3, 5], {2: 3, 3: 1}),
    ),
)
def test_make_change(x, coins, expectation):
    assert make_change(x, coins) == expectation
