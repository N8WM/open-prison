"""Human actor"""

from pdilem.actors.abstracts import Actor, Move


class HumanActor(Actor):
    """Human actor implementation"""

    name = "Human"
    verbose = True
    cloneable = False

    def __init__(self, name: str | None = None, verbose: bool | None = None):
        if name is not None:
            self.name = name
        if verbose is not None:
            self.verbose = verbose
        super().__init__()

    def move(self):
        response = input("\tCooperate or Defect? (c/d): ").strip().lower()

        while response not in ("c", "d"):
            response = input("\tInvalid response. Please enter 'c' or 'd': ")

        return Move(response == "d")

    def result(self, other, delta_score):
        pass

    def reset(self):
        pass
