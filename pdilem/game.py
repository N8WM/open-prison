"""Classes for Prisoner's Dilemma"""

import enum
from abc import ABC, abstractmethod

from typing import Tuple


class Move(enum.Enum):
    """An actor's chosen move in a Prisoner's Dilemma game (cooperate or defect)"""
    COOPERATE = 1
    DEFECT = 2
    def score(self, other: 'Move') -> int:
        """Return the score for this move against the other move"""
        if self == Move.COOPERATE:
            if other == Move.COOPERATE:
                return 1
            return 3
        if other == Move.COOPERATE:
            return 0
        return 2


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


class Game:
    """A Prisoner's Dilemma game"""
    def __init__(self, actor1: Actor, actor2: Actor) -> None:
        """Initialize a new game"""
        self.actor1 = actor1
        self.actor2 = actor2
        self.total_score1 = 0
        self.total_score2 = 0

    def reset(self) -> None:
        """Reset the game and actors"""
        self.actor1.reset()
        self.actor2.reset()
        self.total_score1 = 0
        self.total_score2 = 0

    def next_round(self) -> Tuple[Move, Move, int, int]:
        """Play a round of the game, returns moves and scores"""
        move1 = self.actor1.move()
        move2 = self.actor2.move()
        score1 = move1.score(move2)
        score2 = move2.score(move1)
        self.actor1.result(move2, score1)
        self.actor2.result(move1, score2)
        self.total_score1 += score1
        self.total_score2 += score2
        return move1, move2, score1, score2

    def run(self, rounds: int):
        """Run the game iteratively, first resetting the game and actors"""
        self.reset()
        for _ in range(rounds):
            self.next_round()
        return self.total_score1, self.total_score2
