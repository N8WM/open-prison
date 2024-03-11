"""Random algorithm"""

import random

from pdilem.actors.abstracts import Actor, Move


class RandActor(Actor):
    """Random implementation"""

    name = "Rand"
    verbose = False
    cloneable = True

    def __init__(
        self, name: str | None = None, verbose: bool | None = None, cprob: float = 0.5
    ):
        """
        Initialize the actor

        Args:
            - name (str | None): The name of the actor, or None to use the default name
            - verbose (bool | None): Whether to print prompts
            - cprob (float | str): Probability of cooperating [0.0, 1.0] (default: 0.5)
        """
        if name is not None:
            self.name = name
        if verbose is not None:
            self.verbose = verbose
        super().__init__()

        self.cprob = cprob

    def move(self):
        return Move.COOPERATE if random.random() < self.cprob else Move.DEFECT

    def result(self, other, delta_score):
        pass

    def reset(self):
        pass
