"""Train an agent to play the prisoners dilemma game using stable-baselines3"""

from stable_baselines3 import A2C

from pdilem.actors.always import ACActor, ADActor
from pdilem.actors.grimtrigger import GTActor
from pdilem.actors.random import RandActor
from pdilem.actors.tft import TFTActor, GTFTActor
from pdilem.prisoners_dilemma_env import PrisonersDilemmaEnv

# Create the environment
opponent_set_0 = [ADActor, TFTActor, TFTActor, RandActor]
opponent_set_1 = [
    TFTActor,
    TFTActor,
    TFTActor,
    ADActor,
    ACActor,
    RandActor,
    RandActor,
    GTActor,
]
opponent_set_2 = [TFTActor]
opponent_set_3 = [
    TFTActor,
    GTFTActor,
    ADActor,
    ACActor,
    GTActor,
]

MAX_STEPS = 20

env = PrisonersDilemmaEnv(max_steps=MAX_STEPS, opponent_actors=opponent_set_3)


def train(timesteps=100000) -> A2C:
    """Train the agent"""
    # Train the agent
    model = A2C(
        "MlpPolicy",
        env,
        verbose=1,
    ).learn(timesteps)

    # Save the trained model
    model.save("ppo_prisoners_dilemma")

    return model


def main():
    """Main function"""
    train()


if __name__ == "__main__":
    main()
