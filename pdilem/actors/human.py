"""Human actor"""

from pdilem.actors.abstracts import Actor, Move


class HumanActor(Actor):
    """Human actor implementation"""

    name = "Human"

    def __init__(self, name=None, verbose=True):
        if name is not None:
            self.name = name
        super().__init__(self.name, verbose)

    def move(self):
        response = input("\tCooperate or Defect? (c/d): ").strip().lower()

        while response not in ("c", "d"):
            response = input("\tInvalid response. Please enter 'c' or 'd': ")

        return Move(response == "d")

    def result(self, other, delta_score):
        pass

    def reset(self) -> None:
        pass
