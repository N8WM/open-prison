"""Tit-for-tat algorithms"""

import random

from pdilem.actors.abstracts import Actor, Move


class TFTActor(Actor):
    """Tit-for-tat implementation"""

    name = "TFT"
    verbose = False
    cloneable = True

    def __init__(self, name: str | None = None, verbose: bool | None = None):
        if name is not None:
            self.name = name
        if verbose is not None:
            self.verbose = verbose
        super().__init__()
        self.last_opponent_move: Move = Move.COOPERATE

    def move(self):
        return (
            Move.COOPERATE if self.last_opponent_move == Move.COOPERATE else Move.DEFECT
        )

    def result(self, other, delta_score):
        self.last_opponent_move = other

    def reset(self):
        self.last_opponent_move = Move.COOPERATE

    def clone(self):
        cloned = super().clone()
        cloned.last_opponent_move = self.last_opponent_move
        return cloned


class GTFTActor(Actor):
    """Generous tit-for-tat implementation"""

    name = "GTFT"
    verbose = False
    cloneable = True

    def __init__(self, name: str | None = None, verbose: bool | None = None):
        if name is not None:
            self.name = name
        if verbose is not None:
            self.verbose = verbose
        super().__init__()
        self.last_opponent_move: Move = Move.COOPERATE

    def move(self):
        if random.randint(0, 9) == 0:
            return Move.COOPERATE
        return (
            Move.COOPERATE if self.last_opponent_move == Move.COOPERATE else Move.DEFECT
        )

    def result(self, other, delta_score):
        self.last_opponent_move = other

    def reset(self):
        self.last_opponent_move = Move.COOPERATE

    def clone(self):
        cloned = super().clone()
        cloned.last_opponent_move = self.last_opponent_move
        return cloned
