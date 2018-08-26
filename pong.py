"""Pong implemented with pyxel.

This is the game of pong implemented in pyxel!

Controls are the arrow keys ↑ & ↓ or w & s

Q: Quit the game
R: Restart the game

Todo:
- [ ] Fix collision detection
- [ ] Replace namedtuple with classes
- [ ] Replace music
- [x] Change colour palette
- [ ] Make smoother
- [ ] Add scoring
- [ ] Add scores
- [ ] Add finish screen

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

WIDTH = 80
HEIGHT = 50

HEIGHT_SCORE = FONT_HEIGHT = pyxel.constants.FONT_HEIGHT
COL_SCORE = 6
COL_SCORE_BACKGROUND = 5

PADDLE_HEIGHT = 10
PADDLE_WIDTH = 2
PADDLE_SIDE = 2
PADDLE_MOVE_SPEED = 1

BALL_X_VELOCITY = 0.5
BALL_SIDE = 2


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

        ### This needs to be replaced with scoring code ###
        if self.x < 0:
            self.x = -self.x
            self.x_vol = -self.x_vol
        elif self.x + self.width > WIDTH:
            self.x = 2 * WIDTH - self.x - self.width
            self.x_vol = -self.x_vol
        ###################################################

        if self.y < 0:
            self.y = -self.y
            self.y_vol = -self.y_vol
        elif self.y + self.height > HEIGHT:
            self.y = 2 * HEIGHT - self.y - self.height
            self.y_vol = -self.y_vol


    def check_collision(self, paddles):
        """Check if the ball is hitting a paddle and react accordingly."""

        if self.ball.x < (PADDLE_SIDE + PADDLE_WIDTH):
            if self.l_paddle.y < self.ball.y < self.l_paddle.y + PADDLE_HEIGHT:
                self.ball = Point(
                    2 * (PADDLE_SIDE + PADDLE_WIDTH) - self.ball.x, self.ball.y
                )
                self.ball_velocity = Point(-self.ball_velocity.x, self.ball_velocity.y)
        if self.ball.x + BALL_SIDE > (WIDTH - PADDLE_SIDE - PADDLE_WIDTH):
            if self.r_paddle.y < self.ball.y < self.r_paddle.y + PADDLE_HEIGHT:
                self.ball = Point(
                    2 * (WIDTH - PADDLE_SIDE - PADDLE_WIDTH)
                    - (self.ball.x + BALL_SIDE),
                    self.ball.y,
                )
                self.ball_velocity = Point(-self.ball_velocity.x, self.ball_velocity.y)

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

        pyxel.init(WIDTH, HEIGHT, caption="Pong!", scale=8, fps=60)
        self.music = Music()
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        """Initiate key variables (direction, snake, apple, score, etc.)"""

        self.l_score = 0
        self.r_score = 0

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

        self.ball = Ball(
            coordinates=(WIDTH // 2, HEIGHT // 2),
            colour=COL_BALL,
            width=BALL_SIDE,
            height=BALL_SIDE,
            initial_velocity=BALL_X_VELOCITY,
        )

        self.music.start_music()

    ##############
    # Game logic #
    ##############

    def update(self):
        """Update logic of game. Updates the snake and checks for scoring/win condition."""

        if not self.death:
            self.l_paddle.update()
            self.r_paddle.update()
            self.ball.update()
            self.ball.check_collision([l_paddle, r_paddle])

        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_R):
            self.reset()

    ##############
    # Draw logic #
    ##############

    def draw(self):
        """Draw the background, snake, score, and apple OR the end screen."""
        pyxel.cls(COL_BACKGROUND)
        self.l_paddle.display()
        self.r_paddle.display()
        self.ball.display()
        # self.draw_score()

    def draw_score(self):
        """Draw the score at the top."""

        score = "{:04}".format(self.score)
        pyxel.rect(0, 0, WIDTH, HEIGHT_SCORE, COL_SCORE_BACKGROUND)
        pyxel.text(1, 1, score, COL_SCORE)

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

    def sfx_apple(self):
        """Play apple collection sound."""
        pyxel.play(ch=0, snd=0)

    def sfx_death(self):
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
