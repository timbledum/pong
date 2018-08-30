"""Class for sparkling the ball."""
import pyxel
from random import randint


class ParticleEmitter:
    def __init__(self, ball):
        self.ball = ball
        self.particles = []

    def sparkle(self):
        """Create the sparkles."""
        if pyxel.frame_count % 2 == 0:
            self.particles.append(
                {
                    "zero_frame": pyxel.frame_count,
                    "x": randint(int(self.ball.x) - 4, int(self.ball.x) + 4),
                    "y": randint(int(self.ball.y) - 4, int(self.ball.y) + 4),
                    "color": randint(8, 14),
                }
            )

    def display(self):
        """Sparkle the sparkles and disappear them over time."""
        for idx, particle in enumerate(self.particles):
            if pyxel.frame_count - particle["zero_frame"] >= 20:
                del self.particles[idx]
            else:
                pyxel.pix(particle["x"], particle["y"], particle["color"])
