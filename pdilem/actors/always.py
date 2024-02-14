"""Always do X algorithms"""
from pdilem.actors.abstracts import Actor, Move


class ACActor(Actor):
    """Always cooperate implementation"""

    name = "AC"

    def __init__(self, name=None, verbose=False):
        if name is not None:
            self.name = name
        super().__init__(self.name, verbose)

    def move(self):
        return Move.COOPERATE

    def result(self, other, delta_score):
        pass

    def reset(self) -> None:
        pass


class ADActor(Actor):
    """Always defect implementation"""

    name = "AD"

    def __init__(self, name=None, verbose=False):
        if name is not None:
            self.name = name
        super().__init__(self.name, verbose)

    def move(self):
        return Move.DEFECT

    def result(self, other, delta_score):
        pass

    def reset(self) -> None:
        pass
