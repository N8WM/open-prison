"""Grim trigger algorithm"""

import os
import sys
import time
import numpy as np

from sb3_contrib import RecurrentPPO

from pdilem.actors.abstracts import Actor, Move
from pdilem.env import PDEnv


class DRLActor(Actor):
    """DRL implementation"""

    name = "DRL"
    verbose = False
    cloneable = False

    def __init__(
        self,
        name: str | None = None,
        verbose: bool | None = None,
        model: RecurrentPPO | str | None = None,
        *args,
        **kwargs,
    ):
        """
        Initialize the actor

        Args:
            - name (str | None): The name of the actor, or None to use the default name
            - verbose (bool | None): Whether to print prompts
            - model (RecurrentPPO | str | None): The model to use, a path to load from,
            or None if a new model will be trained
            - args (tuple): Arguments for the environment
            - kwargs (dict): Keyword arguments for the environment
        """
        if name is not None:
            self.name = name
        if verbose is not None:
            self.verbose = verbose
        super().__init__()

        self.args = args
        self.kwargs = kwargs

        self.env = None
        self.load_path = None

        if isinstance(model, str):
            self.load_path = model
            try:
                model = RecurrentPPO.load(model)
            except FileNotFoundError:
                print(f"Could not load model from {model}")
                sys.exit(1)

        self.model = model
        self.lstm_states = None
        self.observation = np.array([2])

    def _generate_env(self) -> None:
        """Generate the environment if it does not exist"""
        if self.env is not None:
            return
        self.env = PDEnv(*self.args, **self.kwargs)

    def train(
        self, save_as: str | None = None, timesteps: int = 100000
    ) -> RecurrentPPO:
        """
        Train a model
        - If there is a provided model, continue training it
        - If there is no provided model, train a new model

        Args:
            - save_as (str | None): The path to save the model as, or None to save it
            using the path provided to originally load the model at initialization

        Returns:
            - RecurrentPPO: The trained model
        """
        self._generate_env()  # Ensure the environment exists
        assert self.env is not None, "No environment provided for training"

        save_path = save_as or self.load_path
        assert save_path, "No path provided to save the model"

        if self.model is None:
            print(f"Training new model and saving to `{save_path}`")
            self.model = RecurrentPPO("MlpLstmPolicy", self.env, verbose=1)
        else:
            print(f"Continuing training of existing model and saving to `{save_path}`")
            self.model.set_env(self.env)

        self.model.set_random_seed(time.time_ns() % 2**32)

        try:
            self.model.learn(timesteps, progress_bar=True)
        except KeyboardInterrupt:
            print("Interrupted by user, saving model")
        finally:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            self.model.save(save_path)
            print(f"Model saved to `{save_path}`")

        print("Done.")

        return self.model

    def move(self):
        assert self.model is not None, "No model provided for prediction"
        episode_starts = np.ones((1,), dtype=bool)
        action, self.lstm_states = self.model.predict(
            self.observation,
            state=self.lstm_states,
            episode_start=episode_starts,
            deterministic=True,
        )
        return Move.from_int(action[0])

    def result(self, other, delta_score):
        self.observation = np.array([other.to_int()])

    def reset(self):
        self.observation = np.array([2])
        self.lstm_states = None
