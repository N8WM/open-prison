import numpy as np
from stable_baselines3 import DQN, PPO, A2C
from stable_baselines3.common.env_util import make_vec_env
from pdilem.prisoners_dilemma_env import PrisonersDilemmaEnv
from pdilem.actors.tft import TFTActor
from pdilem.actors.grimtrigger import GTActor
from pdilem.actors.always import ACActor, ADActor
from pdilem.actors.random import RandActor

# Create the environment
opponent_set_0 = [ADActor, TFTActor, TFTActor, RandActor]
opponent_set_1 = [TFTActor, TFTActor, TFTActor, ADActor, ACActor, RandActor, RandActor, GTActor]
opponent_set_2 = [TFTActor]

MAX_STEPS = 20

env = PrisonersDilemmaEnv(max_steps=MAX_STEPS, opponent_actors=opponent_set_1)

tft_env = make_vec_env(PrisonersDilemmaEnv, n_envs=1, env_kwargs=dict(max_steps=MAX_STEPS, opponent_actors=[TFTActor]))
random_env = make_vec_env(PrisonersDilemmaEnv, n_envs=1, env_kwargs=dict(max_steps=MAX_STEPS, opponent_actors=[RandomActor]))

# Train the agent
model = A2C("MlpPolicy", env, verbose=1).learn(10000)

# Save the trained model
model.save("ppo_prisoners_dilemma")


# Test the trained agent
# using the vecenv
totalReward = 0
obs = random_env.reset() # the env here is the opponent of the model
n_steps = 50
n_runs = 0
for step in range(n_steps):
    action, _ = model.predict(obs, deterministic=True)
    #print(f"Step {step + 1}")
    obs, reward, done, info = random_env.step(action)

    print(f"Step {step + 1}", "obs=", obs, "reward=", reward)
    totalReward += reward
    n_runs += 1

print("Done!", "reward=", totalReward, " average score=", totalReward / n_runs)