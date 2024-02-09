from pdilem.game import Game
from pdilem.actor.human import HumanActor

if __name__ == "__main__":
    game = Game(HumanActor("Player 1"), HumanActor("Player 2"))
    game.run(5)
