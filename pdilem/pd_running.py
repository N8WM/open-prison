import numpy as np
from stable_baselines3 import DQN, PPO, A2C
from stable_baselines3.common.env_util import make_vec_env
from pdilem.prisoners_dilemma_env import PrisonersDilemmaEnv
from pdilem.actors.tft import TFTActor
from pdilem.actors.grimtrigger import GTActor
from pdilem.actors.always import ACActor, ADActor
from pdilem.actors.random import RandActor
from pdilem.actors.randomActor import RandomActor

model = PPO.load("ppo_prisoners_dilemma")

MAX_STEPS = 20

# Create the environment
opponent_set_0 = [ADActor, TFTActor, TFTActor, RandActor]
opponent_set_1 = [TFTActor, TFTActor, TFTActor, ADActor, ACActor, RandActor, RandActor, GTActor]
opponent_set_2 = [TFTActor]

tft_env = make_vec_env(PrisonersDilemmaEnv, n_envs=1, env_kwargs=dict(max_steps=MAX_STEPS, opponent_actors=[TFTActor]))
random_env = make_vec_env(PrisonersDilemmaEnv, n_envs=1, env_kwargs=dict(max_steps=MAX_STEPS, opponent_actors=[RandActor]))
random_env2 = make_vec_env(PrisonersDilemmaEnv, n_envs=1, env_kwargs=dict(max_steps=MAX_STEPS, opponent_actors=[RandomActor]))

# Test the trained agent
# using the vecenv
totalReward = 0
obs = random_env2.reset() # the env here is the opponent of the model
n_steps = 50
n_runs = 0
for step in range(n_steps):
    action, _ = model.predict(obs, deterministic=True)
    #print(f"Step {step + 1}")
    obs, reward, done, info = random_env2.step(action)

    print(f"Step {step + 1}", "obs=", obs, "reward=", reward)
    totalReward += reward
    n_runs += 1

print("Done!", "reward=", totalReward, " average score=", totalReward / n_runs)