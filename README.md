# open-prison

An investigation of agent-based learning for the classic game theory thought experiment, The Prisoner's Dilemma.

## What is the Prisoner's Dilemma?

The Wikipedia page for the [Prisoner's Dilemma](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma) is a great resource for learning more about the thought experiment.

William Poundstone's description from his book in 1993:

> Two members of a criminal gang are arrested and imprisoned. Each prisoner is in solitary confinement with no means of speaking to or exchanging messages with the other. The police admit they don't have enough evidence to convict the pair on the principal charge. They plan to sentence both to a year in prison on a lesser charge. Simultaneously, the police offer each prisoner a Faustian bargain. If he testifies against his partner, he will go free while the partner will get three years in prison on the main charge. Oh, yes, there is a catch ... If both prisoners testify against each other, both will be sentenced to two years in jail. The prisoners are given a little time to think this over, but in no case may either learn what the other has decided until he has irrevocably made his decision. Each is informed that the other prisoner is being offered the very same deal. Each prisoner is concerned only with his own welfare—with minimizing his own prison sentence.

This leads to four different possible outcomes for prisoners A and B:

1. If A and B both remain silent, they will each serve one year in prison.
2. If A testifies against B but B remains silent, A will be set free while B serves three years in prison.
3. If A remains silent but B testifies against A, A will serve three years in prison and B will be set free.
4. If A and B testify against each other, they will each serve two years.

## Prerequisites

- Python 3.10+
- pip

## Setup

1. Clone the repository with `git clone https://github.com/N8WM/open-prison.git`
2. (Recommended) Create a virtual environment with `python -m venv venv`
3. Install the required packages with `pip install -r requirements.txt`

## Usage

All available operations can be performed using the `run.py` script with the appropriate arguments: `python run.py [args]`

```text
usage: run.py
       [-h]
       (-t | -r ACTOR1 ACTOR2)
       [-i ITERATIONS]
       [-m MODEL_NAME]
       [-s SAVE_AS]
       [-T TOTAL_TIMESTEPS]
       [-o OPPONENT1 [OPPONENT2 ...]]

Train a DRL model or run an iterated prisoner's dilemma game with two actors

options:
  -h, --help            show this help message and exit

Functional arguments (mutually exclusive):
  -t, --train           train a new or existing model into test_models/ with the PPO algorithm
  -r ACTOR1 ACTOR2, --run ACTOR1 ACTOR2
                        run a game with the two specified participating actors

Interchangeable running/training arguments:
  -i ITERATIONS, --iterations ITERATIONS
                        number of iterations in a game/episode (default: 100)

Training arguments:
  -m MODEL_NAME, --model-name MODEL_NAME
                        optional name of model to continue training, overwritten if -s is not used
  -s SAVE_AS, --save-as SAVE_AS
                        name to save the model as, (minus the .zip extension)
  -T TOTAL_TIMESTEPS, --total-timesteps TOTAL_TIMESTEPS
                        total number of timesteps to train the model for (default: 1,000,000)
  -o OPPONENT1 [OPPONENT2 ...], --opponents OPPONENT1 [OPPONENT2 ...]
                        opponents to train against (default: TFT, GTFT, AD, AC, GT)
```
