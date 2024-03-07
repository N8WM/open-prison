import numpy as np
from stable_baselines3 import DQN, PPO, A2C
from stable_baselines3.common.env_util import make_vec_env
from pdilem.prisoners_dilemma_env import PrisonersDilemmaEnv
from pdilem.actors.tft import TFTActor
from pdilem.actors.grimtrigger import GTActor
from pdilem.actors.always import ACActor, ADActor
from pdilem.actors.random import RandActor
from pdilem.actors.randomActor import RandomActor

# Create the environment
opponent_set_0 = [ADActor, TFTActor, TFTActor, RandActor]
opponent_set_1 = [TFTActor, TFTActor, TFTActor, ADActor, ACActor, RandActor, RandActor, GTActor]
opponent_set_2 = [TFTActor]

MAX_STEPS = 20

env = PrisonersDilemmaEnv(max_steps=MAX_STEPS, opponent_actors=opponent_set_1)

# Train the agent
model = A2C("MlpPolicy", env, verbose=1).learn(100000)

# Save the trained model
model.save("ppo_prisoners_dilemma")


