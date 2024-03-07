"""Abstract classes for PD actors"""

from abc import ABC, abstractmethod
from enum import IntEnum


class InvalidActionError(Exception):
    """Raised when an invalid action is taken"""


class Move(IntEnum):
    """An actor's chosen move in a Prisoner's Dilemma game (cooperate or defect)"""

    COOPERATE = 0
    DEFECT = 1

    def score(self, other: "Move") -> int:
        """Return the score for this move against the other move"""
        if self == Move.COOPERATE:
            if other == Move.COOPERATE:
                return 2
            return 0
        if other == Move.COOPERATE:
            return 3
        return 1

    def to_int(self) -> int:
        """Return the integer value of the move"""
        return int(self)

    @staticmethod
    def from_int(value: int) -> "Move":
        """Return the Move corresponding to the given integer value"""
        if value == 0:
            return Move.COOPERATE
        if value == 1:
            return Move.DEFECT
        raise InvalidActionError(f"Invalid move value: {value}")

    def meaning(self) -> str:
        """Return the string description of a particular move"""
        if self == Move.COOPERATE:
            return "cooperate"
        return "defect"


class Actor(ABC):
    """An actor in a Prisoner's Dilemma game"""

    name: str
    verbose: bool

    def __init__(self, name: str = "Actor", verbose: bool = False):
        """Initialize a new actor"""
        self.name = name
        self.verbose = verbose
        self.total_score = 0

    @abstractmethod
    def move(self) -> Move:
        """Return the actor's next move"""

    @abstractmethod
    def result(self, other: Move, delta_score: int):
        """Tell the actor what happened in the last round"""

    @abstractmethod
    def reset(self) -> None:
        """Reset the actor's state"""

    def print_label(self, label: str) -> None:
        """Conditionally print a label for the actor"""
        if self.verbose:
            print(f"{label}: {self.name}")
