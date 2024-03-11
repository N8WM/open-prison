"""Define the environment for the Prisoner's Dilemma game"""

import random
from typing import Any

import gymnasium as gym
import numpy as np
from gymnasium import spaces

from pdilem.actors.abstracts import Actor, Move


class PDEnv(gym.Env):
    """Environment for the Prisoner's Dilemma game"""

    def __init__(
        self,
        opponents: list[Actor] | Actor,
        episode_len: int = 50,
        lookahead_depth: int | None = 0,
    ):
        """
        Initialize the environment

        Args:
            - opponents (list | Actor): Pre-initialized opponent selection
            - episode_len (int): Number of steps per episode
            - lookahead_depth (int | None): Number of steps to look ahead,
            or None for full lookahead, or 0 for no lookahead
        """
        super(PDEnv, self).__init__()
        # 2 options - {0: cooperate, 1: defect}
        self.action_space = spaces.Discrete(2)
        # 3 options - {0: cooperate, 1: defect, 2: start (no move yet)}
        self.observation_space = spaces.Discrete(3)
        self._step_num = 0
        self._total_steps = episode_len
        self._total_score = 0
        self._chosen_move: Move = Move.COOPERATE
        self._opponent_move: Move | None = None
        self._opponent_actors = (
            opponents if isinstance(opponents, list) else [opponents]
        )
        self._opponent_actor = random.choice(self._opponent_actors)
        self._lookahead_depth = lookahead_depth

    def _get_obs(self):
        """
        Return the current observation

        Returns:
            - int: The current observation, one of:
                - 0: cooperate
                - 1: defect
                - 2: start (no move yet)
        """
        return np.array(
            [[self._opponent_move.to_int() if self._opponent_move is not None else 2]]
        )

    def _get_info(self):
        """
        Return the current info

        Returns:
            - dict: The current info:
                - delta (int): The increase in score from the last step
                - optimal_ad (int): The optimal achievable additional score
        """
        return {
            "delta": (
                self._chosen_move.score(self._opponent_move)
                if self._opponent_move is not None
                else 0
            ),
            "optimal_ad": self._optimal_ad_score() or 0,
        }

    def _calc_reward(self) -> int:
        """Calculate the reward for the current step"""
        info = self._get_info()
        return info["delta"] + info["optimal_ad"]

    def _optimal_ad_score(
        self,
        _cur_iter: int | None = None,
        _cur_opponent: Actor | None = None,
    ) -> int | None:
        """
        Find the optimal achievable additional score at the current state
        (computationally expensive lookahead)

        Arguments are used for recursive calls, do not set them

        Returns:
            - int | None: The best achievable score if the opponent is
            cloneable and lookahead should be performed, None otherwise
        """
        if not self._opponent_actor.cloneable or self._lookahead_depth == 0:
            return None

        if _cur_iter is None:
            _cur_iter = 0

        if _cur_opponent is None:
            _cur_opponent = self._opponent_actor

        iter_obj = self._lookahead_depth or self._total_steps

        if _cur_iter >= iter_obj:
            return 0

        clone_a = _cur_opponent.clone()
        clone_b = _cur_opponent.clone()

        self_move_a = Move.COOPERATE
        self_move_b = Move.DEFECT
        clone_move_a = clone_a.move()
        clone_move_b = clone_b.move()

        self_score_a = self_move_a.score(clone_move_a)
        self_score_b = self_move_b.score(clone_move_b)
        clone_score_a = clone_move_a.score(self_move_a)
        clone_score_b = clone_move_b.score(self_move_b)

        clone_a.result(self_move_a, clone_score_a)
        clone_b.result(self_move_b, clone_score_b)

        total_score_a = self_score_a + (
            self._optimal_ad_score(_cur_iter + 1, clone_a) or 0
        )
        total_score_b = self_score_b + (
            self._optimal_ad_score(_cur_iter + 1, clone_b) or 0
        )

        return max(total_score_a, total_score_b)

    def reset(
        self,
        *args,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
        train_iterations: int | None = None,
    ):
        """
        Reset the environment to the initial state, choosing a new opponent
        Important: the observation must be a numpy array

        Args:
            - args (tuple): Arguments for the environment
            - seed (int | None): Random seed for the environment
            - options (dict | None): Options for the environment
            - episode_len (int | None): Number of steps for the next episode

        Returns:
            - np.ndarray: The initial observation
        """
        super().reset(*args, seed=seed, options=options)

        self._step_num = 0
        self._total_steps = train_iterations or self._total_steps
        self._total_score = 0

        self._chosen_move = Move.COOPERATE
        self._opponent_move = None

        if self._opponent_actors and self._opponent_actor:
            self._opponent_actor.reset()
            self._opponent_actor = random.choice(self._opponent_actors)

        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def step(self, action: int):
        """
        Take a step in the environment

        Args:
            - action (int): The action to take

        Returns:
            - tuple: step information:
                - observation (np.ndarray): The new observation
                - reward (int): The reward for the step
                - terminated (bool): Whether the episode is terminated
                - truncated (bool): (always False for this environment)
                - info (dict): The step info
        """
        self._step_num += 1
        self._chosen_move = Move.from_int(action)

        self._opponent_move = self._opponent_actor.move()
        self._opponent_actor.total_score += self._opponent_move.score(self._chosen_move)
        self._opponent_actor.result(
            self._chosen_move, self._opponent_move.score(self._chosen_move)
        )

        info = self._get_info()
        observation = self._get_obs()

        self._total_score += info["delta"]  # set before reward calculation

        reward = self._calc_reward()
        terminated = self._step_num >= self._total_steps

        return observation, reward, terminated, False, info

    def render(self):
        """Not supported"""
