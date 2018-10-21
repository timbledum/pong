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

        #################
        # Sound effects #
        #################

        # Score
        pyxel.sound(0).set(
            note="c3e3g3c4c4", tone="s", volume="4", effect=("n" * 4 + "f"), speed=7
        )

        # Finish
        pyxel.sound(1).set(
            note="f3 b2 f2 b1  f1 f1 f1 f1",
            tone="p",
            volume=("4" * 4 + "4321"),
            effect=("n" * 7 + "f"),
            speed=9,
        )

        # Hit
        pyxel.sound(2).set(note="c3", tone="p", volume="4", effect=("n"), speed=7)

        # Pickup
        pyxel.sound(3).set(note="a2", tone="s", volume="4", effect="f", speed=40)

        #########
        # Music #
        #########

        speed = 30

        # Drums
        drum_sound = "b_s_bbs_" "b_s_bbsH" "b_s_bbs_" "b_s_bbsb"

        pyxel.sound(10).set(**self.convert_drums(drum_sound, speed=speed))

        # Harmony
        harmony = (
            "c1 c1 e1 g1 c0 c1 e1 g1"
            "c1 c1 e1 g1 c0 c1 e1 g1"
            "a0 a0 c1 e1 r  a0 c1 e1"
            "e1 e1 g1 b1 r  e1 g1 b1"
        )

        pyxel.sound(11).set(
            note=harmony, tone="t", volume=("4"), effect=("f"), speed=speed
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
        pyxel.play(ch=0, snd=3)

    def start_music(self):
        """Start all music tracks (channels 1 - 3)."""
        pyxel.play(ch=1, snd=10, loop=True)
        pyxel.play(ch=2, snd=11, loop=True)

    def stop_music(self):
        """Stop all music tracks (channels 1 - 3)."""
        for ch in range(1, 4):
            pyxel.stop(ch=ch)

    @staticmethod
    def standardise_length(sounds):
        """For a list of sound numbers, loop the shorter ones to fit the longer one."""
        max_length = max(len(pyxel.sound(snd).note) for snd in sounds)
        for snd in sounds:
            multiple = len(pyxel.sound(snd).note) / max_length
            if int(multiple) != multiple:
                raise ValueError("One of the sounds does not loop within the longest sound.")
        
        for snd in sounds:
            multiple = len(pyxel.sound(snd).note) / max_length
            pyxel.sound(snd).note = pyxel.sound(snd).note * int(multiple)
            


    @staticmethod
    def octave_shift(snd, octaves=1):
        """Shift the notes of the given sound by the given amount of octaves."""

        note_shift = 12 * octaves
        pyxel.sound(snd).note = [
            i + note_shift if i != -1 else -1 for i in pyxel.sound(snd).note
        ]

    @staticmethod
    def convert_drums(drum_string, speed=20):
        """Convert drum string to pyxel arguments to set a sound.
        
        Defines drum noises, and converts a simplified drum string into a full
        set of note, volume, tone, etc., which can be passed using the ** syntax
        to the pyxel.sound.set method.

        >>> convert_drums("b_s_ bbs_")
        {"note": "f0ra4rf0f0a4r",
         "tone": "n",
         "volume": "60206620",
         "effect": "f",
         "speed": 20}

        """

        noises = {}

        # Define drums

        noises["b"] = {"note": "f0", "tone": "n", "volume": "6", "effect": "f"}
        noises["s"] = {"note": "b3", "tone": "n", "volume": "2", "effect": "f"}
        noises["H"] = {"note": "b4", "tone": "n", "volume": "1", "effect": "n"}
        noises["h"] = {"note": "b4", "tone": "n", "volume": "1", "effect": "f"}
        noises["_"] = {"note": "r", "tone": "n", "volume": "0", "effect": "f"}

        # Construct output dict

        output = {"note": "", "tone": "", "volume": "", "effect": ""}

        for noise in drum_string.replace(" ", ""):
            for key in output:
                output[key] += noises[noise][key]

        output["speed"] = speed
        return output


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
        if pyxel.btnp(pyxel.KEY_4):
            music.sfx_pickup()
        if pyxel.btnp(pyxel.KEY_S):
            music.start_music()
        if pyxel.btnp(pyxel.KEY_F):
            music.stop_music()

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    pyxel.run(controls, lambda: None)
