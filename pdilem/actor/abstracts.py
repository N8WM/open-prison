"""Abstract classes for PD actors"""

from abc import ABC, abstractmethod
from enum import Enum


class Move(Enum):
    """An actor's chosen move in a Prisoner's Dilemma game (cooperate or defect)"""

    COOPERATE = 0
    DEFECT = 1

    def score(self, other: "Move") -> int:
        """Return the score for this move against the other move"""
        if self == Move.COOPERATE:
            if other == Move.COOPERATE:
                return -1
            return -3
        if other == Move.COOPERATE:
            return 0
        return -2


class Actor(ABC):
    """An actor in a Prisoner's Dilemma game"""

    @abstractmethod
    def move(self) -> Move:
        """Return the actor's next move"""

    @abstractmethod
    def result(self, other: Move, score: int):
        """Tell the actor what happened in the last round"""

    @abstractmethod
    def reset(self) -> None:
        """Reset the actor's state"""
