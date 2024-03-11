"""Grim trigger algorithm"""

from pdilem.actors.abstracts import Actor, Move


class GTActor(Actor):
    """Grim trigger implementation"""

    name = "GT"
    verbose = False
    cloneable = True

    def __init__(self, name: str | None = None, verbose: bool | None = None):
        if name is not None:
            self.name = name
        if verbose is not None:
            self.verbose = verbose
        super().__init__()
        self.triggered = False

    def move(self):
        return Move.COOPERATE if not self.triggered else Move.DEFECT

    def result(self, other, delta_score):
        self.triggered = self.triggered or other == Move.DEFECT

    def reset(self):
        self.triggered = False

    def clone(self):
        cloned = super().clone()
        cloned.triggered = self.triggered
        return cloned
