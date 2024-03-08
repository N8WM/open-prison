import numpy as np
from stable_baselines3 import DQN, PPO, A2C
from stable_baselines3.common.env_util import make_vec_env
from pdilem.prisoners_dilemma_env import PrisonersDilemmaEnv
from pdilem.actors.tft import TFTActor
from pdilem.actors.grimtrigger import GTActor
from pdilem.actors.always import ACActor, ADActor
from pdilem.actors.random import RandActor
from pdilem.actors.randomActor import RandomActor

MAX_STEPS = 20

class OpponentEnv:
    """Selection of opponents"""
    TFTEnv = make_vec_env(
        PrisonersDilemmaEnv,
        n_envs=1,
        env_kwargs={"max_steps": MAX_STEPS, "opponent_actors": [TFTActor]},
    )

    RandEnv = make_vec_env(
        PrisonersDilemmaEnv,
        n_envs=1,
        env_kwargs={"max_steps": MAX_STEPS, "opponent_actors": [RandActor]},
    )

    RandDistEnv = make_vec_env(
        PrisonersDilemmaEnv,
        n_envs=1,
        env_kwargs={"max_steps": MAX_STEPS, "opponent_actors": [RandomActor]},
    )


def test(model: A2C, opponent) -> None:
    """Test the trained agent"""
    # Test the trained agent
    # using the vecenv
    total_reward = 0
    obs = opponent.reset()  # the env here is the opponent of the model
    n_steps = 50
    n_runs = 0
    for step in range(n_steps):
        action, _ = model.predict(obs, deterministic=True)
        # print(f"Step {step + 1}")
        obs, reward, _, _ = opponent.step(action)

        print(f"Step {step + 1}", "obs=", obs, "reward=", reward)
        total_reward += reward
        n_runs += 1

    print("Done!", "reward=", total_reward, " average score=", total_reward / n_runs)


def main():
    """Main function"""
    model = PPO.load("ppo_prisoners_dilemma")
    test(model, OpponentEnv.RandEnv)

if __name__ == "__main__":
    main()