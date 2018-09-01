"""Special pickups!"""

from collections import namedtuple
from random import randint, choice
import pyxel
from utilities import is_overlap

Pickup = namedtuple("Point", "x y width height pickup_type")

PICKUP_TYPES = {"sparkle": 14}
PICKUP_INTERVAL = (500, 700)
PICKUP_WIDTH = 2
PICKUP_LENGTH = 300


class Pickups:
    def __init__(self, left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

        self.next_pickup = pyxel.frame_count + randint(*PICKUP_INTERVAL)

        self.pickups = []
        self.active_conditions = {}

    def check_pickup(self):
        if pyxel.frame_count > self.next_pickup:
            self.create_pickup()
            self.next_pickup = pyxel.frame_count + randint(*PICKUP_INTERVAL)

        for condition, end_frame in list(self.active_conditions.items()):
            if pyxel.frame_count > end_frame:
                del self.active_conditions[condition]


    def create_pickup(self):
        x = randint(self.left, self.right - PICKUP_WIDTH)
        y = randint(self.top, self.bottom - PICKUP_WIDTH)
        pickup_type = choice(list(PICKUP_TYPES.keys()))
        pickup = Pickup(
            x=x, y=y, width=PICKUP_WIDTH, height=PICKUP_WIDTH, pickup_type=pickup_type
        )
        self.pickups.append(pickup)

    def check_collision(self, ball):
        for i, pickup in enumerate(self.pickups.copy()):
            if is_overlap(pickup, ball):
                del self.pickups[i]
                self.active_conditions[pickup.pickup_type] = (
                    pyxel.frame_count + PICKUP_LENGTH
                )

    def display(self):
        for pickup in self.pickups:
            pyxel.rect(
                x1=pickup.x,
                y1=pickup.y,
                x2=pickup.x + pickup.width - 1,
                y2=pickup.y + pickup.height - 1,
                col=PICKUP_TYPES[pickup.pickup_type],
            )
