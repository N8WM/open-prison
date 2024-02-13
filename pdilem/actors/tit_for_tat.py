"""Tit-for-tat algorithm"""

from pdilem.actors.abstracts import Actor, Move


class TFTActor(Actor):
    """Tit-for-tat implementation"""

    name = "TFT"

    def __init__(self, name=None, verbose=False):
        if name is not None:
            self.name = name
        super().__init__(self.name, verbose)
        self.last_opponent_move: Move = Move.COOPERATE

    def move(self):
        return (
            Move.COOPERATE if self.last_opponent_move == Move.COOPERATE else Move.DEFECT
        )

    def result(self, other, delta_score):
        self.last_opponent_move = other

    def reset(self) -> None:
        self.last_opponent_move = Move.COOPERATE
