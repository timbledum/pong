"""Pong implemented with pyxel.

This is the game of pong implemented in pyxel!

Controls are the arrow keys ↑ & ↓ or w & s

Q: Quit the game
R: Restart the game

Todo:
- [ ] Fix collision detection
- [ ] Replace namedtuple with classes
- [ ] Replace music
- [ ] Change colour palette
- [ ] Make smoother
- [ ] ???
- [ ] Profit

Created by Marcus Croucher in 2018.
"""

from collections import namedtuple
import pyxel

Point = namedtuple("Point", ["x", "y"])  # Convenience class for coordinates

#############
# Constants #
#############

COL_BACKGROUND = 3
COL_PADDLE = 11
COL_DEATH = 8
COL_BALL = 8

TEXT_DEATH = ["GAME OVER", "(Q)UIT", "(R)ESTART"]
COL_TEXT_DEATH = 0
HEIGHT_DEATH = 5

WIDTH = 80
HEIGHT = 50

HEIGHT_SCORE = FONT_HEIGHT = pyxel.constants.FONT_HEIGHT
COL_SCORE = 6
COL_SCORE_BACKGROUND = 5

PADDLE_HEIGHT = 10
PADDLE_WIDTH = 2
PADDLE_SIDE = 2

BALL_X_VELOCITY = 0.5
BALL_SIDE = 2

UP = Point(0, -1)
DOWN = Point(0, 1)
RIGHT = Point(1, 0)
LEFT = Point(-1, 0)


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

        self.l_paddle = Point(PADDLE_SIDE, (HEIGHT - PADDLE_HEIGHT) // 2)
        self.r_paddle = Point(
            WIDTH - PADDLE_SIDE - PADDLE_WIDTH + 1, (HEIGHT - PADDLE_HEIGHT) // 2
        )
        self.ball = Point(WIDTH // 2, HEIGHT // 2)
        self.ball_velocity = Point(BALL_X_VELOCITY, BALL_X_VELOCITY)

        self.death = False
        self.music.start_music()

    ##############
    # Game logic #
    ##############

    def update(self):
        """Update logic of game. Updates the snake and checks for scoring/win condition."""

        if not self.death:
            self.update_paddles()
            self.update_ball()
            self.check_collision()

        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_R):
            self.reset()

    def update_paddles(self):
        """Watch the keys and change direction."""

        if pyxel.btn(pyxel.KEY_W):
            self.l_paddle = Point(self.l_paddle.x + UP.x, self.l_paddle.y + UP.y)
        elif pyxel.btn(pyxel.KEY_S):
            self.l_paddle = Point(self.l_paddle.x + DOWN.x, self.l_paddle.y + DOWN.y)

        if self.l_paddle.y < 0:
            self.l_paddle = Point(self.l_paddle.x, 0)
        elif self.l_paddle.y + PADDLE_HEIGHT > HEIGHT:
            self.l_paddle = Point(self.l_paddle.x, HEIGHT - PADDLE_HEIGHT)

        if pyxel.btn(pyxel.KEY_UP):
            self.r_paddle = Point(self.r_paddle.x + UP.x, self.r_paddle.y + UP.y)
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.r_paddle = Point(self.r_paddle.x + DOWN.x, self.r_paddle.y + DOWN.y)

        if self.r_paddle.y < 0:
            self.r_paddle = Point(self.r_paddle.x, 0)
        elif self.r_paddle.y + PADDLE_HEIGHT > HEIGHT:
            self.r_paddle = Point(self.r_paddle.x, HEIGHT - PADDLE_HEIGHT)

    def update_ball(self):
        self.ball = Point(
            self.ball.x + self.ball_velocity.x, self.ball.y + self.ball_velocity.y
        )

        if self.ball.x < 0:
            self.ball = Point(-self.ball.x, self.ball.y)
            self.ball_velocity = Point(-self.ball_velocity.x, self.ball_velocity.y)
        elif self.ball.x + BALL_SIDE > WIDTH:
            self.ball = Point(2 * WIDTH - self.ball.x - BALL_SIDE, self.ball.y)
            self.ball_velocity = Point(-self.ball_velocity.x, self.ball_velocity.y)
        if self.ball.y < 0:
            self.ball = Point(self.ball.x, -self.ball.y)
            self.ball_velocity = Point(self.ball_velocity.x, -self.ball_velocity.y)
        elif self.ball.y + BALL_SIDE > HEIGHT:
            self.ball = Point(self.ball.x, 2 * HEIGHT - self.ball.y - BALL_SIDE)
            self.ball_velocity = Point(self.ball_velocity.x, -self.ball_velocity.y)


    def check_collision(self):
        if self.ball.x < (PADDLE_SIDE + PADDLE_WIDTH):
            if self.l_paddle.y < self.ball.y < self.l_paddle.y + PADDLE_HEIGHT:
                self.ball = Point(2 * (PADDLE_SIDE + PADDLE_WIDTH) - self.ball.x, self.ball.y)
                self.ball_velocity = Point(-self.ball_velocity.x, self.ball_velocity.y)
        if self.ball.x + BALL_SIDE > (WIDTH - PADDLE_SIDE - PADDLE_WIDTH):
            if self.r_paddle.y < self.ball.y < self.r_paddle.y + PADDLE_HEIGHT:
                self.ball = Point(2 * (WIDTH - PADDLE_SIDE - PADDLE_WIDTH) - (self.ball.x  + BALL_SIDE), self.ball.y)
                self.ball_velocity = Point(-self.ball_velocity.x, self.ball_velocity.y)


    def check_death(self):
        """Check whether the snake has died (out of bounds or doubled up.)"""

        head = self.snake[0]
        if head.x < 0 or head.y <= HEIGHT_SCORE or head.x >= WIDTH or head.y >= HEIGHT:
            self.death_event()
        elif len(self.snake) != len(set(self.snake)):
            self.death_event()

    def death_event(self):
        """Kill the game (bring up end screen)."""
        self.music.sfx_death()
        self.music.stop_music()
        self.death = True  # Check having run into self

    ##############
    # Draw logic #
    ##############

    def draw(self):
        """Draw the background, snake, score, and apple OR the end screen."""
        pyxel.cls(COL_BACKGROUND)
        self.draw_paddles()
        self.draw_ball()
        # self.draw_score()

    def draw_paddles(self):
        for paddle in self.l_paddle, self.r_paddle:

            pyxel.rect(
                x1=paddle.x,
                y1=paddle.y,
                x2=paddle.x + PADDLE_WIDTH - 1,
                y2=paddle.y + PADDLE_HEIGHT - 1,
                col=COL_PADDLE,
            )


    def draw_ball(self):
            pyxel.rect(
                x1=self.ball.x,
                y1=self.ball.y,
                x2=self.ball.x + BALL_SIDE - 1,
                y2=self.ball.y + BALL_SIDE - 1,
                col=COL_BALL,
            )

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
