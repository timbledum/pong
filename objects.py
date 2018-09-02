"""
Define the paddle and the ball objects.
"""

import pyxel
from utilities import is_overlap, random_direction

PADDLE_MOVE_SPEED = 1
SPIN = 0.4



class Paddle:
    """Class for the paddles.

    Controls the movement and display of the paddles."""

    def __init__(
        self, coordinates, colour, width, height, control_up, control_down, dimensions
    ):
        """Set up key paddle variables."""
        self.control_up = control_up
        self.control_down = control_down
        self.colour = colour
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.width = width
        self.height = height
        self.dimensions = dimensions

    def update(self):
        """Move the paddle up and down."""
        if pyxel.btn(self.control_up):
            self.y -= PADDLE_MOVE_SPEED
        elif pyxel.btn(self.control_down):
            self.y += PADDLE_MOVE_SPEED

        if self.y < 0:
            self.y = 0
        elif self.y + self.height > self.dimensions[1]:
            self.y = self.dimensions[1] - self.height

    def display(self):
        """Display the paddle as a rect."""
        pyxel.rect(
            x1=self.x,
            y1=self.y,
            x2=self.x + self.width - 1,
            y2=self.y + self.height - 1,
            col=self.colour,
        )


class Ball:
    """Class for the ball.

    Moves and displays the ball."""

    def __init__(
        self, coordinates, colour, width, height, initial_velocity, dimensions
    ):
        """Set up initial variables."""
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.x_vol = initial_velocity * random_direction()
        self.y_vol = initial_velocity * random_direction()
        self.colour = colour
        self.width = width
        self.height = height
        self.dimensions = dimensions

    def update(self):
        """Update position of ball and check if hitting side of board."""
        self.x += self.x_vol
        self.y += self.y_vol

        if self.x < 0:
            return "r"  # Hit left side so right scores
        elif self.x + self.width > self.dimensions[0]:
            return "l"  # Hit right side so left scores

        if self.y < 0:
            self.y = -self.y
            self.y_vol = -self.y_vol
        elif self.y + self.height > self.dimensions[1]:
            self.y = 2 * self.dimensions[1] - self.y - 2 * self.height
            self.y_vol = -self.y_vol

    def check_collision(self, paddles):
        """Check if the ball is hitting a paddle and react accordingly."""
        for paddle in paddles:
            if not is_overlap(self, paddle):
                continue

            self.spin_ball(paddle)

            self.x_vol = -self.x_vol

            ball_center = self.x + self.width / 2
            paddle_center = paddle.x + paddle.width / 2

            if ball_center > paddle_center:
                self.x = paddle.x + paddle.width
            else:
                self.x = paddle.x - self.width
            return True
        return False

    def spin_ball(self, paddle):
        """Adds or substracts y velocity based on where the ball hit the paddle."""

        paddle_centre = paddle.height / 2
        ball_centre = self.y + self.height / 2

        hit_position = ball_centre - paddle.y
        hit_position_normalised = (hit_position - paddle_centre) / paddle_centre
        spin = hit_position_normalised * SPIN

        self.y_vol += spin

    def display(self):
        """Display the ball."""
        pyxel.rect(
            x1=self.x,
            y1=self.y,
            x2=self.x + self.width - 1,
            y2=self.y + self.height - 1,
            col=self.colour,
        )
