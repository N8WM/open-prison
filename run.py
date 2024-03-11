"""Run the game"""

import os
import argparse

from pdilem.actors.abstracts import Actor
from pdilem.game import Game
from pdilem.actors import (
    ACActor,
    ADActor,
    DRLActor,
    GTActor,
    GTFTActor,
    HumanActor,
    RandActor,
    TFTActor,
)


class ActorClosure:
    def __init__(
        self, actor: type[Actor], name: str | None = None, model: str | None = None
    ):
        self.actor = actor
        self.name = name or actor.name
        self.model = model

    def __call__(self, *args, **kwargs):
        if not kwargs:
            kwargs = {"name": self.name}
            if self.model:
                kwargs["model"] = self.model
        return self.actor(*args, **kwargs)


class ActorPool:
    def __init__(self, actors: list[ActorClosure]):
        self.actors = actors

    def __getitem__(self, name: str):
        for actor in self.actors:
            if actor.name == name:
                return actor
        raise KeyError(f"Actor name {name} not found")

    def __iter__(self):
        return iter(self.actors)

    @property
    def names(self):
        return [actor.name for actor in self.actors]


model_dirs = ["test_models/", "saved_models/"]
model_paths = [
    os.path.join(d, f)
    for d in model_dirs
    if os.path.exists(os.path.join(d))
    for f in os.listdir(d)
    if os.path.isfile(os.path.join(d, f)) and f.endswith(".zip")
]
model_names = [os.path.basename(m).replace(".zip", "") for m in model_paths]

logic_actors: list[type[Actor]] = [
    HumanActor,
    TFTActor,
    GTFTActor,
    ACActor,
    ADActor,
    GTActor,
    RandActor,
]

default_opponent_actors: list[type[Actor]] = [
    TFTActor,
    GTFTActor,
    ADActor,
    ACActor,
    GTActor,
]

logic_pool = ActorPool([ActorClosure(actor) for actor in logic_actors])
drl_pool = ActorPool(
    [
        ActorClosure(DRLActor, name, model)
        for name, model in zip(model_names, model_paths)
    ]
)
combined_pool = ActorPool(logic_pool.actors + drl_pool.actors)
default_opponent_pool = ActorPool(
    [ActorClosure(actor) for actor in default_opponent_actors]
)


def train(
    model_name: str | None,
    existing_model_name: str | None,
    episode_len: int,
    total_timesteps: int,
    opponent_names: list[str],
):
    """Train a DRL model"""
    existing_model_path = None
    if existing_model_name:
        existing_model_path = drl_pool[existing_model_name].model
        assert existing_model_path is not None, "Model path is missing or corrupted"

    new_model_name = model_name or existing_model_name
    assert new_model_name is not None, "Model name is missing"
    save_path = os.path.join(model_dirs[0], f"{new_model_name}.zip")

    opponent_set = [combined_pool[name]() for name in opponent_names]

    new_drl_agent = DRLActor(
        new_model_name,
        model=existing_model_path,
        episode_len=episode_len,
        opponents=opponent_set,
    )
    new_drl_agent.train(save_path, total_timesteps)


def run(actor1_name: str, actor2_name: str, iterations: int):
    """Run a game with two actors"""
    actor1 = logic_pool[actor1_name]()
    actor2 = logic_pool[actor2_name]()

    game = Game(actor1, actor2)

    try:
        game.run(iterations)
    except KeyboardInterrupt:
        print("\nGame interrupted")


def main():
    """Main function"""

    parser = argparse.ArgumentParser(
        description="Train a DRL model or run an iterated prisoner's dilemma game with two actors"
    )
    group1 = parser.add_argument_group("Functional arguments (mutually exclusive)")
    group1e = group1.add_mutually_exclusive_group(required=True)
    group1e.add_argument(
        "-t",
        "--train",
        action="store_true",
        help="train a new/existing model in test_models/ with the PPO algorithm",
    )
    group1e.add_argument(
        "-r",
        "--run",
        nargs=2,
        type=str,
        metavar=("ACTOR1", "ACTOR2"),
        help="run a game with the two specified participating actors",
        choices=combined_pool.names,
    )
    group2 = parser.add_argument_group("Interchangeable running/training arguments")
    group2.add_argument(
        "-i",
        "--iterations",
        type=int,
        default=100,
        help="number of iterations in a game/episode (default: 100)",
    )
    group3 = parser.add_argument_group("Training arguments")
    group3.add_argument(
        "-m",
        "--model-name",
        type=str,
        help="optional name of model to continue training, overwritten if -s is not used",
        choices=drl_pool.names,
    )
    group3.add_argument(
        "-s",
        "--save-as",
        type=str,
        help="name to save the model as, (minus the .zip extension)",
    )
    group3.add_argument(
        "-T",
        "--total-timesteps",
        type=int,
        default=1_000_000,
        help="total number of timesteps to train the model for (default: 1,000,000)",
    )
    group3.add_argument(
        "-o",
        "--opponents",
        type=str,
        nargs="+",
        default=default_opponent_pool.names,
        help=f"opponents to train against (default: {', '.join(default_opponent_pool.names)})",
        choices=combined_pool.names,
    )

    args = parser.parse_args()

    train_: bool = args.train
    run_: tuple[str, str] | None = args.run
    iterations: int = args.iterations
    model_name: str | None = args.model_name
    save_as: str | None = args.save_as
    total_timesteps: int = args.total_timesteps
    opponents: list[str] = args.opponents

    if train_:
        if model_name is None and save_as is None:
            parser.error("at least one of -m or -s is required for training")
        train(save_as, model_name, iterations, total_timesteps, opponents)

    elif run_ is not None:
        actor1, actor2 = run_
        if model_name is not None or save_as is not None:
            parser.error("model name and save as are not required for running")
        run(actor1, actor2, iterations)


if __name__ == "__main__":
    main()
