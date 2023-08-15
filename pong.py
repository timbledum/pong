"""Pong implemented with pyxel.

This is the game of pong implemented in pyxel!

Version 1.9.18

Controls are the arrow keys ↑ & ↓ or w & s

Q: Quit the game
R: Restart the game

Created by Marcus Croucher in 2018. Updated in 2023.
"""

import pyxel
from particle_emitter import ParticleEmitter
from objects import Paddle, Ball
from pickups import Pickups, PickupType
from music import Music
from utilities import sign

#############
# Constants #
#############

COL_BACKGROUND = 5
COL_PADDLE = 6
COL_PADDLE_SLOW = 8
COL_BALL = 9
COL_SCORE = 13
COL_FINISH = 13
COL_FINISH_TEXT = 14

WIDTH = 80
HEIGHT = 50
DIMENSIONS = WIDTH, HEIGHT

PADDLE_HEIGHT = 10
PADDLE_HEIGHT_EXPANDED = 15
PADDLE_WIDTH = 2
PADDLE_SIDE = 2
PADDLE_MOVE_SPEED = 1
PADDLE_MOVE_SPEED_SLOW = 0.5


BALL_INITIAL_VELOCITY = 0.4
BALL_SIDE = 2

WIN_CONDITION = 5

TEXT_FINISH = ["The winner is:", "", "(Q)UIT", "(R)ESTART"]
HEIGHT_FINISH = 6

SPEED_PERIOD = 150
SPEED_AMOUNT = 0.07


###################
# The game itself #
###################


class Pong:
    """The class that sets up and runs the game."""

    def __init__(self):
        """Initiate pyxel, set up initial game variables, and run."""

        pyxel.init(WIDTH, HEIGHT, caption="Pong!", scale=8, fps=60)
        self.music = Music()
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        """Reset score and position."""

        self.l_score = 0
        self.r_score = 0
        self.finish = False
        self.music.start_music()

        self.l_paddle = Paddle(
            coordinates=(PADDLE_SIDE, (HEIGHT - PADDLE_HEIGHT) // 2),
            colour=COL_PADDLE,
            width=PADDLE_WIDTH,
            height=PADDLE_HEIGHT,
            control_up=pyxel.KEY_W,
            control_down=pyxel.KEY_S,
            move_speed=PADDLE_MOVE_SPEED,
            dimensions=DIMENSIONS,
        )

        self.r_paddle = Paddle(
            coordinates=(
                WIDTH - PADDLE_SIDE - PADDLE_WIDTH,
                (HEIGHT - PADDLE_HEIGHT) // 2,
            ),
            colour=COL_PADDLE,
            width=PADDLE_WIDTH,
            height=PADDLE_HEIGHT,
            control_up=pyxel.KEY_UP,
            control_down=pyxel.KEY_DOWN,
            move_speed=PADDLE_MOVE_SPEED,
            dimensions=DIMENSIONS,
        )

        self.ball = Ball(
            coordinates=(WIDTH // 2, HEIGHT // 2),
            colour=COL_BALL,
            width=BALL_SIDE,
            height=BALL_SIDE,
            initial_velocity=BALL_INITIAL_VELOCITY,
            dimensions=DIMENSIONS,
        )

        self.sparkler = ParticleEmitter(self.ball)

        pickup_types = {
            "sparkle": PickupType(14, self.sparkler.turn_on, self.sparkler.turn_off),
            "expand": PickupType(12, self.expand_paddle, self.contract_paddle),
            "slow": PickupType(8, self.slow_paddle, self.speed_paddle),
            "bounce": PickupType(11, self.ball.bounce_on, self.ball.bounce_off),
            "giantball": PickupType(10, self.ball.giant_on, self.ball.giant_off),
        }
        self.expand_stack = []
        self.speed_stack = []
        pickup_side_buffer = PADDLE_WIDTH + PADDLE_SIDE + 2
        self.pickups = Pickups(
            pickup_types, self.music, pickup_side_buffer, WIDTH - pickup_side_buffer, 0, HEIGHT
        )

        self.reset_after_score()

    def reset_after_score(self):
        """Reset paddles and ball."""
        self.start = pyxel.frame_count + 50
        self.speed_up = self.start + SPEED_PERIOD
        self.ball.reset()

    ##############
    # Game logic #
    ##############

    def update(self):
        """Update logic of game. Updates the paddles, ball, and checks for scoring/win condition."""

        self.l_paddle.update()
        self.r_paddle.update()
        self.sparkler.sparkle()

        if pyxel.frame_count > self.start and not self.finish:
            outcome = self.ball.update()
            if outcome:
                self.score(outcome)
            self.check_speed()
            if self.ball.check_collision([self.l_paddle, self.r_paddle]):
                self.music.sfx_hit()
            self.pickups.check_pickup()
            self.pickups.check_collision(self.ball)

        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_R):
            self.reset_game()

    def check_speed(self):
        """Adds velocity to the ball periodically."""

        if pyxel.frame_count > self.speed_up:
            self.speed_up += SPEED_PERIOD
            self.ball.x_vol += SPEED_AMOUNT * sign(self.ball.x_vol)
            self.ball.y_vol += SPEED_AMOUNT * sign(self.ball.y_vol)

    def score(self, outcome):
        """Adds to the score if the ball hits the side. Check win condition."""

        self.music.sfx_score()
        if outcome == "l":
            self.l_score += 1
        elif outcome == "r":
            self.r_score += 1

        if self.l_score >= WIN_CONDITION or self.r_score >= WIN_CONDITION:
            self.win_event()

        self.reset_after_score()

    def win_event(self):
        """What happens when someone wins the game!"""

        self.finish = True
        self.music.stop_music()
        self.music.sfx_finish()

    ######################
    # Pickup controllers #
    ######################

    def expand_paddle(self):
        """Expand the pandle temporarily."""

        if self.ball.x_vol > 0:
            paddle = self.l_paddle
        else:
            paddle = self.r_paddle

        paddle.height = PADDLE_HEIGHT_EXPANDED
        paddle.y -= (PADDLE_HEIGHT_EXPANDED - PADDLE_HEIGHT) // 2
        self.expand_stack.append(paddle)

    def contract_paddle(self):
        """Revert paddle side to normal."""

        paddle = self.expand_stack.pop(0)
        if paddle not in self.expand_stack:
            paddle.height = PADDLE_HEIGHT
            paddle.y += (PADDLE_HEIGHT_EXPANDED - PADDLE_HEIGHT) // 2

    def slow_paddle(self):
        """Slow the pandle temporarily."""

        if self.ball.x_vol > 0:
            paddle = self.l_paddle
        else:
            paddle = self.r_paddle

        paddle.move_speed = PADDLE_MOVE_SPEED_SLOW
        paddle.colour = COL_PADDLE_SLOW
        self.speed_stack.append(paddle)

    def speed_paddle(self):
        """Speed the paddle back up to normal speed."""

        paddle = self.speed_stack.pop(0)
        if paddle not in self.speed_stack:
            paddle.move_speed = PADDLE_MOVE_SPEED
            paddle.colour = COL_PADDLE

    ##############
    # Draw logic #
    ##############

    def draw(self):
        """Draw the paddles and ball OR the end screen."""

        if self.finish:
            self.draw_end_screen()
        else:
            pyxel.cls(COL_BACKGROUND)
            self.sparkler.display()
            self.l_paddle.display()
            self.r_paddle.display()
            self.pickups.display()
            self.ball.display()
            self.draw_score()

    def draw_score(self):
        """Draw the score at the top."""

        l_score = "{:01}".format(self.l_score)
        r_score = "{:01}".format(self.r_score)

        buffer = PADDLE_SIDE + PADDLE_WIDTH + 2
        r_x_position = WIDTH - pyxel.FONT_WIDTH - buffer

        pyxel.text(x=buffer, y=2, s=l_score, col=COL_SCORE)
        pyxel.text(x=r_x_position, y=2, s=r_score, col=COL_SCORE)

    def draw_end_screen(self):
        """Draw the final screen with the winner!"""

        pyxel.cls(col=COL_FINISH)

        display_text = TEXT_FINISH[:]

        if self.l_score >= WIN_CONDITION:
            winner = "The LEFT player!"
        else:
            winner = "The RIGHT player!"
        display_text.insert(1, winner)
        for i, text in enumerate(display_text):
            y_offset = (pyxel.FONT_HEIGHT + 2) * i
            text_x = self.center_text(text, WIDTH)
            pyxel.text(text_x, HEIGHT_FINISH + y_offset, text, COL_FINISH_TEXT)

    @staticmethod
    def center_text(text, page_width, char_width=pyxel.FONT_WIDTH):
        """Helper function for calcuating the start x value for centered text."""

        text_width = len(text) * char_width
        return (page_width - text_width) // 2


if __name__ == "__main__":
    Pong()
