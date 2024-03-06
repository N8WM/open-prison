"""Random algorithm"""
import random

from pdilem.actors.abstracts import Actor, Move

class RandomActor(Actor):
    """Generous tit-for-tat implementation"""

    name = "RA"

    def __init__(self, name=None, verbose=False):
        if name is not None:
            self.name = name
        super().__init__(self.name, verbose)
        self.last_opponent_move: Move = Move.COOPERATE

    def move(self):
        return random.choice([Move.COOPERATE, Move.COOPERATE, Move.COOPERATE, Move.COOPERATE, Move.DEFECT, Move.DEFECT, Move.DEFECT])

    def result(self, other, delta_score):
        self.last_opponent_move = other

    def reset(self) -> None:
        self.last_opponent_move = Move.COOPERATE