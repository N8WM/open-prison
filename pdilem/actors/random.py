"""Random algorithm"""
import random

from pdilem.actors.abstracts import Actor, Move


class RandActor(Actor):
    """Random implementation"""

    name = "Rand"

    def __init__(self, name=None, verbose=False):
        if name is not None:
            self.name = name
        super().__init__(self.name, verbose)

    def move(self):
        return Move.COOPERATE if random.random() < 0.5 else Move.DEFECT

    def result(self, other, delta_score):
        pass

    def reset(self) -> None:
        pass
