"""Human actor"""

from pdilem.actor import Actor, Move


class HumanActor(Actor):
    """Human actor implementation"""

    def __init__(self, name: str):
        self.name = name
        self.total_score = 0

    def move(self) -> Move:
        print(f"{self.name}:")
        print(f"\tScore: {self.total_score}")
        response = input("\tCooperate or Defect? (c/d): ").strip().lower()

        while response not in ("c", "d"):
            response = input("\tInvalid response. Please enter 'c' or 'd': ")

        return Move(response == "d")

    def result(self, other: Move, score: int) -> None:
        self.total_score += score
        print(f"{self.name}:")
        print(f"\tOpponent chose to {'defect' if other.value else 'cooperate'} ({score})")
        print(f"\tScore: {self.total_score}")

    def reset(self) -> None:
        self.total_score = 0

    def __str__(self):
        return self.name
