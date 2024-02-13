"""Classes for Prisoner's Dilemma"""

from typing import Tuple

from pdilem.actors.abstracts import Actor, Move


class Game:
    """A Prisoner's Dilemma game"""

    def __init__(self, actor1: Actor, actor2: Actor) -> None:
        """Initialize a new game"""
        self.actor1 = actor1
        self.actor2 = actor2
        if actor1.name == actor2.name:
            actor1.name = f"{actor1.name}1"
            actor2.name = f"{actor2.name}2"

    def reset(self) -> None:
        """Reset the game and actors"""
        self.actor1.reset()
        self.actor2.reset()
        self.actor1.total_score = 0
        self.actor2.total_score = 0

    def next_round(self) -> Tuple[Move, Move, int, int]:
        """Play a round of the game, returns moves and scores"""
        self.print_status("Scores", key="total_score")
        self.actor1.print_label("INPUT")
        move1 = self.actor1.move()
        self.actor2.print_label("INPUT")
        move2 = self.actor2.move()
        score1 = move1.score(move2)
        score2 = move2.score(move1)
        self.actor1.total_score += score1
        self.actor2.total_score += score2
        self.actor1.result(move2, score1)
        self.actor2.result(move1, score2)
        self.print_status(
            "Results",
            value=(f"{move1.meaning()} ({score1})", f"{move2.meaning()} ({score2})"),
        )
        return move1, move2, score1, score2

    def run(self, rounds: int) -> tuple[int, int]:
        """Run the game iteratively, first resetting the game and actors"""
        self.reset()
        for i in range(rounds):
            self.print_divider(f"Round {i + 1}")
            self.next_round()
        self.print_divider("Game Over")
        self.print_status("Scores", key="total_score")
        return self.actor1.total_score, self.actor2.total_score

    def print_status(
        self, label: str, key: str | None = None, value: tuple[str, str] | None = None
    ) -> None:
        """Conditionally print the current total scores for each actor"""
        if self.actor1.verbose or self.actor2.verbose:
            print(f"\n{label}:")
            value_ = (
                value[0] if value else getattr(self.actor1, key) if key else None
            )
            print(f"\t{self.actor1.name}: {value_}")
            value_ = (
                value[1] if value else getattr(self.actor2, key) if key else None
            )
            print(f"\t{self.actor2.name}: {value_}")
            print()

    def print_divider(self, label: str | None = None) -> None:
        """Divider to print between round outputs"""
        if label is None:
            label = ""
        if self.actor1.verbose or self.actor2.verbose:
            print(f"{label:-^40s}")
