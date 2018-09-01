"""Some utility functions."""

from random import choice

####################
# Helper functions #
####################


def is_overlap(object1, object2):
    """Detects overlap between two rectangles.

    Taking two objects, detects whether they overlap.
    Assumes the presence of the following attributes:
    - x
    - y
    - width
    - height
    
    Tests whether the rectangles are above/below each other, or
    left/right of each other, and if not, they are overlapping.

    This is greedy - includes collisions where the rectangles are only just touching.
    """

    if object1.x + object1.width < object2.x:
        return False
    if object2.x + object2.width < object1.x:
        return False
    if object1.y + object1.height < object2.y:
        return False
    if object2.y + object2.height < object1.y:
        return False
    return True


def sign(number):
    """Return the sign of a number."""
    return 1 if number >= 0 else -1


def random_direction():
    """Return a random direction as 1 or -1."""
    return choice((-1, 1))
