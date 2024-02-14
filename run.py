"""Run the game"""

import argparse

from pdilem.actors import ACActor, ADActor, GTActor, GTFTActor, HumanActor, TFTActor
from pdilem.actors.abstracts import Actor
from pdilem.game import Game

actors: list[type[Actor]] = [HumanActor, TFTActor, GTFTActor, ACActor, ADActor, GTActor]


def get_args() -> tuple[type[Actor], type[Actor], int]:
    """Get the arguments from the command line"""
    parser = argparse.ArgumentParser(description="Run the game")
    parser.add_argument(
        "actor1", help="The first actor", type=str, choices=[a.name for a in actors]
    )
    parser.add_argument(
        "actor2", help="The second actor", type=str, choices=[a.name for a in actors]
    )
    parser.add_argument(
        "-r", "--rounds", help="The number of rounds", type=int, default=5
    )

    args = parser.parse_args()

    actor_dict = {a.name: a for a in actors}
    actor1 = actor_dict[args.actor1]
    actor2 = actor_dict[args.actor2]
    rounds = args.rounds

    return actor1, actor2, rounds


if __name__ == "__main__":
    a1, a2, r = get_args()
    game = Game(a1(), a2())

    try:
        game.run(r)
    except KeyboardInterrupt:
        print("\nGame interrupted")
