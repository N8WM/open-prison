"""Run the game"""

from pdilem.actors import HumanActor, TFTActor
from pdilem.actors.abstracts import Actor
from pdilem.game import Game

if __name__ == "__main__":
    actors: list[type[Actor]] = [HumanActor, TFTActor]
    actors_dict = {a.name: a for a in actors}
    print(f"Available actors: {', '.join([a.name for a in actors])}")
    actor1: type[Actor] | None = None
    while actor1 is None or not issubclass(actor1, Actor):
        actor1 = actors_dict.get(input("Actor1: "), None)
        if actor1 is None:
            print("Invalid actor. Please choose an actor from the ones listed above.")
    actor2: type[Actor] | None = None
    while actor2 is None or not issubclass(actor2, Actor):
        actor2 = actors_dict.get(input("Actor2: "), None)
        if actor2 is None:
            print("Invalid actor. Please choose an actor from the ones listed above.")
    game = Game(actor1(), actor2())
    try:
        game.run(5)
    except KeyboardInterrupt:
        print("\nGame interrupted")
