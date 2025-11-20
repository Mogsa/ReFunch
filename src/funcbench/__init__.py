"""FuncBench: First-principles AI reasoning benchmark for temporal pattern learning."""

__version__ = "0.1.0"

from funcbench.agent import Agent, RandomAgent, GreedyAgent, ACTION_LEFT, ACTION_STAY, ACTION_RIGHT
from funcbench.environment import Environment
from funcbench.function import Function2D, GaussianTranslation

__all__ = [
    "ACTION_LEFT",
    "ACTION_RIGHT",
    "ACTION_STAY",
    "Agent",
    "RandomAgent",
    "GreedyAgent",
    "Environment",
    "Function2D",
    "GaussianTranslation",
]
