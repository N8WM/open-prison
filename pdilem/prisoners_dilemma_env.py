import numpy as np
import gymnasium as gym
from gymnasium import spaces
import random
from pdilem.actors.abstracts import Actor, Move
from pdilem.actors.tft import TFTActor
from pdilem.actors.randomActor import RandomActor

class PrisonersDilemmaEnv(gym.Env):

    metadata = {"render_modes": ["console"]}


    def __init__(self, max_steps=10, opponent_actors=[TFTActor]):
        self.action_space = spaces.Discrete(2)  # 0 for cooperate, 1 for defect
        self.observation_space = spaces.MultiDiscrete([2] * 2)

        self.steps_taken = 0
        self.max_steps = max_steps  # Define the maximum number of steps in an episode

        self.opponent_actors = opponent_actors
        chosenActor = random.choice(self.opponent_actors)
        self.opponent_actor = chosenActor()
        self.opponent_actor.reset()

    def reset(self, seed=None, options=None):
        """
        Important: the observation must be a numpy array
        :return: (np.array)
        """

        super().reset(seed=seed, options=options)

        self.steps_taken = 0

        chosenActor = random.choice(self.opponent_actors)
        self.opponent_actor = chosenActor()
        self.opponent_actor.reset()

        return np.array([0, 0]), {}  # empty info dict


    def step(self, action):

        self.steps_taken += 1

        action_decoded = Move.COOPERATE
        if (action == 0):
            action_decoded = Move.COOPERATE
        elif (action == 1):
            action_decoded = Move.DEFECT
        else:
            raise "action not valid" + str(action)
        self.opponent_actor.result(action_decoded, 0)

        opponent_action = self.opponent_actor.move()
        opponent_action_encoded = 0
        if (opponent_action == Move.COOPERATE):
            opponent_action_encoded = 0
        elif (opponent_action == Move.DEFECT):
            opponent_action_encoded = 1
        else:
            raise "opponent actor move not valid" + opponent_action
        

        # Define the rewards based on the actions
        if action_decoded == Move.COOPERATE:  # Cooperate
            if opponent_action == Move.COOPERATE:
                reward = 2  # Both players cooperate, both get a moderate reward
            else:
                reward = 0
        else:  # Defect
            if opponent_action == Move.COOPERATE:
                reward = 3  # One defects while the other cooperates, defector gets maximum payoff, cooperator gets minimum
            else:
                reward = 1  # Both defect, both get a lower payoff than mutual cooperation

        done = self.steps_taken >= self.max_steps  # Episode ends after a certain number of steps
        info = {}  # Additional information, not used in this example

        return np.array([action, opponent_action_encoded]), reward, done, done, info

    def render(self):
        pass


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

