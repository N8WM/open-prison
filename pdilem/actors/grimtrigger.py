"""Grim trigger algorithm"""

from pdilem.actors.abstracts import Actor, Move


class GTActor(Actor):
    """Grim trigger implementation"""

    name = "GT"

    def __init__(self, name=None, verbose=False):
        if name is not None:
            self.name = name
        super().__init__(self.name, verbose)
        self.triggered = False

    def move(self):
        return Move.COOPERATE if not self.triggered else Move.DEFECT

    def result(self, other, delta_score):
        self.triggered = self.triggered or other == Move.DEFECT

    def reset(self) -> None:
        self.triggered = False
