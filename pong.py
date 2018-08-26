"""Pong implemented with pyxel.

This is the game of pong implemented in pyxel!

Controls are the arrow keys ↑ & ↓ or w & s

Q: Quit the game
R: Restart the game

Todo:
- [x] Fix collision detection
- [x] Replace namedtuple with classes
- [ ] Replace music
- [x] Change colour palette
- [ ] Make smoother
- [x] Add scoring
- [x] Add scores
- [x] Add finish screen
- [ ] Add different rebounds

Created by Marcus Croucher in 2018.
"""

from collections import namedtuple
import pyxel

Point = namedtuple("Point", ["x", "y"])  # Convenience class for coordinates

#############
# Constants #
#############

COL_BACKGROUND = 5
COL_PADDLE = 6
COL_BALL = 9
COL_SCORE = 13
COL_FINISH = 13
COL_FINISH_TEXT = 14

WIDTH = 80
HEIGHT = 50

PADDLE_HEIGHT = 10
PADDLE_WIDTH = 2
PADDLE_SIDE = 2
PADDLE_MOVE_SPEED = 1

BALL_X_VELOCITY = 0.5
BALL_SIDE = 2

WIN_CONDITION = 7

TEXT_FINISH = ["The winner is:", "", "(Q)UIT", "(R)ESTART"]
HEIGHT_FINISH = 6

SPEED_PERIOD = 100
SPEED_AMOUNT = 0.1

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

#######################
# Classes definitions #
#######################


class Paddle:
    """Class for the paddles.

    Controls the movement and display of the paddles."""

    def __init__(self, coordinates, colour, width, height, control_up, control_down):
        """Set up key paddle variables."""
        self.control_up = control_up
        self.control_down = control_down
        self.colour = colour
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.width = width
        self.height = height

    def update(self):
        """Move the paddle up and down."""
        if pyxel.btn(self.control_up):
            self.y -= PADDLE_MOVE_SPEED
        elif pyxel.btn(self.control_down):
            self.y += PADDLE_MOVE_SPEED

        if self.y < 0:
            self.y = 0
        elif self.y + self.height > HEIGHT:
            self.y = HEIGHT - self.height

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

    def __init__(self, coordinates, colour, width, height, initial_velocity):
        """Set up initial variables."""
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.x_vol = self.y_vol = initial_velocity
        self.colour = colour
        self.width = width
        self.height = height

    def update(self):
        """Update position of ball and check if hitting side of board."""
        self.x += self.x_vol
        self.y += self.y_vol

        if self.x < 0:
            return "l"
        elif self.x + self.width > WIDTH:
            return "r"

        if self.y < 0:
            self.y = -self.y
            self.y_vol = -self.y_vol
        elif self.y + self.height > HEIGHT:
            self.y = 2 * HEIGHT - self.y - 2 * self.height
            self.y_vol = -self.y_vol

    def check_collision(self, paddles):
        """Check if the ball is hitting a paddle and react accordingly."""
        for paddle in paddles:
            if not is_overlap(self, paddle):
                continue

            self.x_vol = -self.x_vol

            ball_center = self.x + self.width / 2
            paddle_center = paddle.x + paddle.width / 2

            if ball_center > paddle_center:
                self.x = paddle.x + paddle.width
            else:
                self.x = paddle.x - self.width

    def display(self):
        """Display the ball."""
        pyxel.rect(
            x1=self.x,
            y1=self.y,
            x2=self.x + self.width - 1,
            y2=self.y + self.height - 1,
            col=self.colour,
        )


###################
# The game itself #
###################


class Pong:
    """The class that sets up and runs the game."""

    def __init__(self):
        """Initiate pyxel, set up initial game variables, and run."""

        pyxel.init(WIDTH, HEIGHT, caption="Pong!", scale=8, fps=50)
        self.music = Music()
        self.music.start_music()
        self.reset_game()
        pyxel.run(self.update, self.draw)


    def reset_game(self):
        """Reset score and position."""

        self.l_score = 0
        self.r_score = 0
        self.finish = False
        self.reset_after_score()

        self.l_paddle = Paddle(
            coordinates=(PADDLE_SIDE, (HEIGHT - PADDLE_HEIGHT) // 2),
            colour=COL_PADDLE,
            width=PADDLE_WIDTH,
            height=PADDLE_HEIGHT,
            control_up=pyxel.KEY_W,
            control_down=pyxel.KEY_S,
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
        )


    def reset_after_score(self):
        """Reset paddles and ball."""
        self.start = pyxel.frame_count + 50
        self.speed_up = self.start + SPEED_PERIOD

        self.ball = Ball(
            coordinates=(WIDTH // 2, HEIGHT // 2),
            colour=COL_BALL,
            width=BALL_SIDE,
            height=BALL_SIDE,
            initial_velocity=BALL_X_VELOCITY,
        )

    ##############
    # Game logic #
    ##############

    def update(self):
        """Update logic of game. Updates the snake and checks for scoring/win condition."""

        if pyxel.frame_count > self.start:
            self.l_paddle.update()
            self.r_paddle.update()
            outcome = self.ball.update()
            if outcome:
                self.score(outcome)
            self.check_speed()
            self.ball.check_collision([self.l_paddle, self.r_paddle])

        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_R):
            self.reset_game()

    def check_speed(self):
        if pyxel.frame_count > self.speed_up:
            self.speed_up += SPEED_PERIOD
            self.ball.x_vol += SPEED_AMOUNT * sign(self.ball.x_vol)
            self.ball.y_vol += SPEED_AMOUNT * sign(self.ball.y_vol)
            print("speedup", self.ball.x_vol)

    def score(self, outcome):
        self.music.sfx_score()
        if outcome == "l":
            self.l_score += 1
        elif outcome == "r":
            self.r_score += 1

        if (self.l_score >= WIN_CONDITION or self.r_score >= WIN_CONDITION):
            self.win_event()

        self.reset_after_score()

    def win_event(self):
        self.finish = True
        self.music.sfx_finish()



    ##############
    # Draw logic #
    ##############

    def draw(self):
        """Draw the paddles and ball OR the end screen."""
        if self.finish:
            self.draw_end_screen()
        else:
            pyxel.cls(COL_BACKGROUND)
            self.l_paddle.display()
            self.r_paddle.display()
            self.ball.display()
            self.draw_score()   

    def draw_score(self):
        """Draw the score at the top."""

        l_score = "{:01}".format(self.l_score)
        r_score = "{:01}".format(self.r_score)

        buffer = PADDLE_SIDE + PADDLE_WIDTH + 2
        r_x_position = WIDTH - pyxel.constants.FONT_WIDTH - buffer

        pyxel.text(x=buffer, y=2, s=l_score, col=COL_SCORE)
        pyxel.text(x=r_x_position, y=2, s=r_score, col=COL_SCORE)

    def draw_end_screen(self):
        pyxel.cls(col=COL_FINISH)

        display_text = TEXT_FINISH[:]

        if self.l_score >= WIN_CONDITION:
            winner = "The LEFT player!"
        else:
            winner = "The RIGHT player!"
        display_text.insert(1, winner)
        for i, text in enumerate(display_text):
            y_offset = (pyxel.constants.FONT_HEIGHT + 2) * i
            text_x = self.center_text(text, WIDTH)
            pyxel.text(text_x, HEIGHT_FINISH + y_offset, text, COL_FINISH_TEXT)


    @staticmethod
    def center_text(text, page_width, char_width=pyxel.constants.FONT_WIDTH):
        """Helper function for calcuating the start x value for centered text."""

        text_width = len(text) * char_width
        return (page_width - text_width) // 2


###########################
# Music and sound effects #
###########################


class Music:
    def __init__(self):
        """Define sound and music."""

        # Sound effects
        pyxel.sound(0).set(
            note="c3e3g3c4c4", tone="s", volume="4", effect=("n" * 4 + "f"), speed=7
        )
        pyxel.sound(1).set(
            note="f3 b2 f2 b1  f1 f1 f1 f1",
            tone="p",
            volume=("4" * 4 + "4321"),
            effect=("n" * 7 + "f"),
            speed=9,
        )

        melody1 = (
            "c3 c3 c3 d3 e3 r e3 r"
            + ("r" * 8)
            + "e3 e3 e3 f3 d3 r c3 r"
            + ("r" * 8)
            + "c3 c3 c3 d3 e3 r e3 r"
            + ("r" * 8)
            + "b2 b2 b2 f3 d3 r c3 r"
            + ("r" * 8)
        )

        melody2 = (
            "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
            + "a2a2a2a2 c3c3c3c3 d3d3d3d3 e3e3e3e3"
            + "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
            + "a2a2a2a2 g2g2g2g2 c3c3c3c3 g2g2a2a2"
            + "rrrr e3e3e3e3 d3d3c3c3 b2b2c3c3"
            + "a2a2a2a2 c3c3c3c3 d3d3d3d3 e3e3e3e3"
            + "f3f3f3a3 a3a3a3a3 g3g3g3b3 b3b3b3b3"
            + "b3b3b3b4 rrrr e3d3c3g3 a2g2e2d2"
        )

        # Music
        pyxel.sound(2).set(
            note=melody1 * 2 + melody2 * 2,
            tone="s",
            volume=("3"),
            effect=("nnnsffff"),
            speed=20,
        )

        harmony1 = (
            "a1 a1 a1 b1  f1 f1 c2 c2"
            "c2 c2 c2 c2  g1 g1 b1 b1" * 3
            + "f1 f1 f1 f1 f1 f1 f1 f1 g1 g1 g1 g1 g1 g1 g1 g1"
        )
        harmony2 = (
            ("f1" * 8 + "g1" * 8 + "a1" * 8 + ("c2" * 7 + "d2")) * 3
            + "f1" * 16
            + "g1" * 16
        )

        pyxel.sound(3).set(
            note=harmony1 * 2 + harmony2 * 2, tone="t", volume="5", effect="f", speed=20
        )
        pyxel.sound(4).set(
            note=("f0 r a4 r  f0 f0 a4 r" "f0 r a4 r   f0 f0 a4 f0"),
            tone="n",
            volume="6622 6622 6622 6426",
            effect="f",
            speed=20,
        )

    def sfx_score(self):
        """Play apple collection sound."""
        pyxel.play(ch=0, snd=0)

    def sfx_finish(self):
        """Play death collection sound."""
        pyxel.play(ch=0, snd=1)

    def start_music(self):
        """Start all music tracks (channels 1 - 3)."""
        music_tracks = [2, 3, 4]
        for ch, snd in enumerate(music_tracks):
            pyxel.play(ch=(ch + 1), snd=snd, loop=True)

    def stop_music(self):
        """Stop all music tracks (channels 1 - 3)."""
        for ch in range(1, 4):
            pyxel.stop(ch=ch)


if __name__ == "__main__":
    Pong()
