"""Always do X algorithms"""

from pdilem.actors.abstracts import Actor, Move


class ACActor(Actor):
    """Always cooperate implementation"""

    name = "AC"
    verbose = False
    cloneable = True

    def __init__(self, name: str | None = None, verbose: bool | None = None):
        if name is not None:
            self.name = name
        if verbose is not None:
            self.verbose = verbose
        super().__init__()

    def move(self):
        return Move.COOPERATE

    def result(self, other, delta_score):
        pass

    def reset(self):
        pass


class ADActor(Actor):
    """Always defect implementation"""

    name = "AD"
    verbose = False
    cloneable = True

    def __init__(self, name: str | None = None, verbose: bool | None = None):
        if name is not None:
            self.name = name
        if verbose is not None:
            self.verbose = verbose
        super().__init__()

    def move(self):
        return Move.DEFECT

    def result(self, other, delta_score):
        pass

    def reset(self):
        pass
