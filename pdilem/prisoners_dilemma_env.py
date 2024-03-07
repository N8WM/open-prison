"""Define the environment for the Prisoner's Dilemma game"""

import random

import gymnasium as gym
import numpy as np
from gymnasium import spaces

from pdilem.actors.abstracts import Actor, Move
from pdilem.actors.tft import TFTActor


class PrisonersDilemmaEnv(gym.Env):
    """Environment for the Prisoner's Dilemma game"""

    metadata = {"render_modes": ["console"]}

    def __init__(self, max_steps=10, opponent_actors: list[type[Actor]] | None = None):
        """
        Initialize the environment

        Args:
            - max_steps (int): Maximum number of steps in an episode
            - opponent_actors (list): List of opponent actors to choose from
            at the start of each episode (default: [TFTActor])
        """
        self.action_space = spaces.Discrete(2)  # 0 for cooperate, 1 for defect
        self.observation_space = spaces.MultiDiscrete([2] * 2)

        self.steps_taken = 0
        self.max_steps = max_steps  # Define the maximum number of steps in an episode

        self.opponent_actors = opponent_actors or [TFTActor]
        chosen_actor = random.choice(self.opponent_actors)
        self.opponent_actor = chosen_actor()
        self.opponent_actor.reset()

    def reset(self, *args, seed=None, options=None):
        """
        Reset the environment to the initial state, choosing a new opponent
        Important: the observation must be a numpy array
        :return: (np.array)
        """

        super().reset(*args, seed=seed, options=options)

        self.steps_taken = 0

        chosen_actor = random.choice(self.opponent_actors)
        self.opponent_actor = chosen_actor()
        self.opponent_actor.reset()

        return np.array([0, 0]), {}  # empty info dict

    def step(self, action: int):
        """
        Take a step in the environment
        """
        self.steps_taken += 1
        action_decoded = Move.from_int(action)
        self.opponent_actor.result(action_decoded, 0)

        opponent_action = self.opponent_actor.move()
        opponent_action_encoded = opponent_action.to_int()

        # Define the rewards based on the actions
        reward = action_decoded.score(opponent_action)

        done = (
            self.steps_taken >= self.max_steps
        )  # Episode ends after a certain number of steps
        info = {}  # Additional information, not used in this example

        return np.array([action, opponent_action_encoded]), reward, done, done, info

    def render(self):
        """Unimplemented"""


# # env = PrisonersDilemmaEnv(memory_length=10, max_steps=30)
# env = PrisonersDilemmaEnv(memory_length=10, max_steps=30, opponent_actor=RandomActor)

# # Reset the environment to get the initial state
# state = env.reset()

# # Define a function to always cooperate
# def always_cooperate(observation):
#     return Move.COOPERATE  # Always return cooperate action (action 0)

# def random_move(observation):
#     return random.choice([0, 1])

# # Simulate the game for a certain number of steps
# num_steps = 30
# total_points = 0
# for _ in range(num_steps):
#     # Agent always cooperates
#     action = random_move(state)
#     # opponent_action = random_move(state)

#     # Take a step in the environment
#     next_state, reward, done, steps_taken, info = env.step(action)

#     total_points += reward

#     # Print the current state, action, reward, and whether the episode is done
#     print("State:", state, "Action:", action, "Reward:", reward, "Done:", done)
#     # print("Action:", action, "Opponent Action:", opponent_action, "Reward:", reward)

#     # Update the current state
#     state = next_state

#     # If the episode is done, break out of the loop
#     if done:
#         print(total_points)
#         break
