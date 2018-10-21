"""Special pickups!

This module defines a class which keeps track of pickups and then their resulting effects.

It also defines mini containers to hold the pickup objects to display, and the
actual pickup types.

The module exposes the effects of pickups in three ways:
1. self.is_condition_active: check whether the condition is currently active
2. PickupType(enter=function): the function which is triggered when a pickup is picked up
3. PickupType(exit=function): the function which is triggered when the condition finishes
                              (usually to revert the state to normal)

"""

from collections import namedtuple
from random import randint, choice
import pyxel
from utilities import is_overlap


PICKUP_INTERVAL = (300, 900)
# PICKUP_INTERVAL = (100, 150)  # Super pickup mode
PICKUP_WIDTH = 3
PICKUP_LENGTH = 500

Pickup = namedtuple("Point", "x y width height pickup_type")

# Define a convenience container to hold a pickup type. Enter and exit need to be functions.
PickupType = namedtuple("PickupType", "colour enter exit", defaults=[None, None])


class Pickups:
    """A class for keeping track of displaying pickups, then tracking
    the condition of the pickups when they take effect."""

    def __init__(self, pickup_types, music, left, right, top, bottom):
        """Initiate with given types, and dimensions of the board where pickups are allowed."""
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

        self.music = music

        self.next_pickup = pyxel.frame_count + randint(*PICKUP_INTERVAL)

        self.pickup_types = pickup_types
        self.pickups = []
        self.active_conditions = []

    def check_pickup(self):
        """Checks whether to create a pickup, and also checks for the end of all active conditions."""

        if pyxel.frame_count > self.next_pickup:
            self.create_pickup()
            self.next_pickup = pyxel.frame_count + randint(*PICKUP_INTERVAL)

        for i, (condition, end_frame) in enumerate(self.active_conditions.copy()):
            if pyxel.frame_count > end_frame:
                del self.active_conditions[i]

                exit_function = self.pickup_types[condition].exit
                if exit_function:
                    exit_function()

    def is_condition_active(self, condition):
        """Convenience function to see whether a condition is active."""

        conditions = {c for c, _ in self.active_conditions}
        return condition in conditions

    def create_pickup(self):
        """Create a random pickup on the board."""

        x = randint(self.left, self.right - PICKUP_WIDTH)
        y = randint(self.top, self.bottom - PICKUP_WIDTH)
        pickup_type = choice(list(self.pickup_types.keys()))
        pickup = Pickup(
            x=x, y=y, width=PICKUP_WIDTH, height=PICKUP_WIDTH, pickup_type=pickup_type
        )
        self.pickups.append(pickup)

    def check_collision(self, ball):
        """Check whether the ball has hit a pickup."""

        for i, pickup in enumerate(self.pickups.copy()):
            if is_overlap(pickup, ball):
                self.music.sfx_pickup()
                del self.pickups[i]
                self.active_conditions.append(
                    (pickup.pickup_type, pyxel.frame_count + PICKUP_LENGTH)
                )

                enter_function = self.pickup_types[pickup.pickup_type].enter
                if enter_function:
                    enter_function()
                break

    def display(self):
        """Display all pickups."""

        for pickup in self.pickups:
            pyxel.rect(
                x1=pickup.x,
                y1=pickup.y,
                x2=pickup.x + pickup.width - 1,
                y2=pickup.y + pickup.height - 1,
                col=self.pickup_types[pickup.pickup_type].colour,
            )
