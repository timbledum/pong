"""A module to provide

###########################
# Music and sound effects #
###########################

"""

import pyxel

class Music:
    """A class to contain music and sound effects."""

    def __init__(self):
        """Define sound and music."""

        # Sound effects
        pyxel.sound(0).set(  # Score
            note="c3e3g3c4c4", tone="s", volume="4", effect=("n" * 4 + "f"), speed=7
        )

        pyxel.sound(1).set(  # Finish
            note="f3 b2 f2 b1  f1 f1 f1 f1",
            tone="p",
            volume=("4" * 4 + "4321"),
            effect=("n" * 7 + "f"),
            speed=9,
        )

        pyxel.sound(2).set(  # Hit
            note="a3", tone="s", volume="4", effect=("n"), speed=7
        )

    def sfx_score(self):
        """Play scoring sound."""
        pyxel.play(ch=0, snd=0)

    def sfx_finish(self):
        """Play finish sound."""
        pyxel.play(ch=0, snd=1)

    def sfx_hit(self):
        """Play sound for when ball hits paddle."""
        pyxel.play(ch=0, snd=2)

    def sfx_pickup(self):
        """Play sound for when ball hits a pickup."""
        pyxel.play(ch=0, snd=3)

    def start_music(self):
        """Start all music tracks (channels 1 - 3)."""
        pass  # To be implemented

    def stop_music(self):
        """Stop all music tracks (channels 1 - 3)."""
        for ch in range(1, 4):
            pyxel.stop(ch=ch)


if __name__ == "__main__":
    pyxel.init(50, 50)
    music = Music()

    def controls():
        if pyxel.btnp(pyxel.KEY_1):
            music.sfx_hit()
        if pyxel.btnp(pyxel.KEY_2):
            music.sfx_score()
        if pyxel.btnp(pyxel.KEY_3):
            music.sfx_finish()
        if pyxel.btnp(pyxel.KEY_S):
            music.start_music()
        if pyxel.btnp(pyxel.KEY_F):
            music.stop_music()

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    pyxel.run(controls, lambda: None)