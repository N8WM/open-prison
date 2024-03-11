"""Train an agent to play the prisoners dilemma game using stable-baselines3"""

from pdilem.actors.always import ACActor, ADActor
from pdilem.actors.grimtrigger import GTActor
from pdilem.actors.random import RandActor
from pdilem.actors.tft import TFTActor, GTFTActor
from pdilem.actors.drl import DRLActor

# Create the environment
opponent_set = [
    TFTActor(),
    GTFTActor(),
    ADActor(),
    ACActor(),
    GTActor(),
]

EPISODE_LEN = 100
TOTAL_TIMESTEPS = 500000


def main():
    """Main function"""
    fred = DRLActor("Fred", episode_len=EPISODE_LEN, opponents=opponent_set)
    fred.train("test_models/fred_1.1.zip", TOTAL_TIMESTEPS)


if __name__ == "__main__":
    main()
