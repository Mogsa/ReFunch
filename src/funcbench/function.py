"""
Temporal function definitions for FuncBench.

This module provides abstract base classes and concrete implementations
for 2D temporal functions that evolve over time according to explicit rules.
"""

from abc import ABC, abstractmethod
import numpy as np


class Function2D(ABC):
    """
    Abstract base class for 2D temporal functions.

    Temporal functions define reward landscapes that evolve over time
    according to explicit mathematical rules. Agents navigate these
    functions to maximize cumulative reward across episodes.

    All concrete implementations must define:
    - evaluate(): Calculate reward values at spatial positions and timesteps
    - get_perfect_score(): Calculate theoretical maximum achievable reward
    - bounds: Define valid spatial domain for agent movement
    """

    @abstractmethod
    def evaluate(self, x: np.ndarray, t: float) -> np.ndarray:
        """
        Evaluate the function at given spatial positions and timestep.

        Parameters
        ----------
        x : np.ndarray
            Spatial positions (x-coordinates) where function is evaluated.
            Shape: (N,) for N positions, or scalar value.
        t : float
            Temporal coordinate (timestep). Function evolves over time.

        Returns
        -------
        np.ndarray
            Reward values at each position. Same shape as input x.
            Values represent the reward landscape at time t.

        Notes
        -----
        - Implementations should use NumPy vectorized operations
        - All computations should use float64 precision
        - Function should be deterministic (same inputs = same outputs)
        """
        pass

    @abstractmethod
    def get_perfect_score(self, episode_length: int) -> float:
        """
        Calculate theoretical perfect score for this function.

        The perfect score represents the maximum cumulative reward
        achievable by an omniscient agent with perfect knowledge of
        the function's temporal dynamics.

        Parameters
        ----------
        episode_length : int
            Number of timesteps in the episode.

        Returns
        -------
        float
            Maximum possible cumulative reward over the episode.
            Used as baseline for evaluating agent performance.

        Notes
        -----
        - Assumes agent can teleport to optimal position each timestep
        - Does not account for movement constraints or fog-of-war
        - Provides upper bound for performance evaluation
        """
        pass

    @property
    @abstractmethod
    def bounds(self) -> tuple[float, float]:
        """
        Get spatial bounds for agent movement.

        Returns
        -------
        tuple[float, float]
            (left_bound, right_bound) defining valid x-coordinate range.
            Agents cannot move outside these bounds.

        Notes
        -----
        - Bounds are enforced by the environment
        - Functions may be defined outside bounds, but agents cannot access
        """
        pass
