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


class GaussianTranslation(Function2D):
    """
    2D Gaussian function with linear translation dynamics.

    The Gaussian peak translates at constant velocity along the x-axis,
    creating a simple temporal pattern where the reward maximum moves
    predictably over time. This provides the baseline temporal function
    for testing first-principles reasoning.

    Temporal Dynamics
    -----------------
    At each timestep t, the Gaussian peak is centered at:
        mean(t) = mean_start + velocity * t

    The agent must learn to track the moving peak to maximize cumulative
    reward. With perfect tracking (agent always at peak), the agent receives
    the maximum reward (amplitude) at every timestep.

    Mathematical Form
    -----------------
    reward(x, t) = amplitude * exp(-((x - mean(t))^2) / (2 * sigma^2))

    where mean(t) = mean_start + velocity * t

    Parameters
    ----------
    mean_start : float, default=-10.0
        Initial position of the Gaussian peak at t=0.
    velocity : float, default=0.1
        Translation speed (spatial units per timestep).
        Positive velocity moves peak to the right.
    sigma : float, default=1.0
        Standard deviation controlling peak width.
        Smaller sigma = narrower peak = harder to track.
    amplitude : float, default=1.0
        Peak height (maximum reward value at peak center).
    bounds : tuple[float, float], default=(-20.0, 20.0)
        Spatial bounds (left, right) defining valid agent movement range.
    seed : int or None, default=None
        Random seed for reproducibility. Currently unused but reserved
        for future stochastic function variants.

    Examples
    --------
    >>> # Create function with default parameters
    >>> func = GaussianTranslation()
    >>> # Evaluate at single position and time
    >>> reward = func.evaluate(np.array([0.0]), t=10.0)
    >>> # Peak is at mean_start + velocity * t = -10.0 + 0.1 * 10 = -9.0
    >>> # Evaluate at multiple positions
    >>> x = np.linspace(-20, 20, 100)
    >>> rewards = func.evaluate(x, t=50.0)

    Notes
    -----
    - All computations use float64 precision for reproducibility
    - Uses NumPy vectorized operations (no Python loops)
    - Evaluation is deterministic (same inputs always give same outputs)
    """

    def __init__(
        self,
        mean_start: float = -10.0,
        velocity: float = 0.1,
        sigma: float = 1.0,
        amplitude: float = 1.0,
        bounds: tuple[float, float] = (-20.0, 20.0),
        seed: int | None = None,
    ):
        """Initialize GaussianTranslation function with given parameters."""
        # Store parameters as float64 for precision
        self.mean_start = np.float64(mean_start)
        self.velocity = np.float64(velocity)
        self.sigma = np.float64(sigma)
        self.amplitude = np.float64(amplitude)
        self._bounds = (np.float64(bounds[0]), np.float64(bounds[1]))
        self.seed = seed

        # Pre-compute constants for performance
        self._two_sigma_squared = np.float64(2.0) * self.sigma ** 2

    def evaluate(self, x: np.ndarray, t: float) -> np.ndarray:
        """
        Evaluate Gaussian function at spatial positions x and timestep t.

        The Gaussian peak translates linearly over time. At timestep t,
        the peak is centered at (mean_start + velocity * t).

        Parameters
        ----------
        x : np.ndarray
            Spatial positions (x-coordinates) for evaluation.
            Shape: (N,) for N positions, or scalar.
        t : float
            Temporal coordinate (timestep). Peak location depends on t.

        Returns
        -------
        np.ndarray
            Reward values at each position. Same shape as x.
            Maximum reward (amplitude) occurs when x equals peak position.

        Examples
        --------
        >>> func = GaussianTranslation(mean_start=-10.0, velocity=0.1)
        >>> # At t=0, peak is at x=-10.0
        >>> func.evaluate(np.array([-10.0]), t=0.0)
        array([1.0])  # Maximum reward at peak
        >>> # At t=100, peak has moved to x=0.0
        >>> func.evaluate(np.array([0.0]), t=100.0)
        array([1.0])  # Maximum reward at new peak position

        Notes
        -----
        - Uses vectorized NumPy operations for performance
        - All computations use float64 precision
        - No Python loops - operates on entire arrays at once
        """
        # Convert inputs to float64
        x = np.asarray(x, dtype=np.float64)
        t = np.float64(t)

        # Calculate peak position at time t
        mean_t = self.mean_start + self.velocity * t

        # Vectorized Gaussian evaluation
        # reward(x, t) = amplitude * exp(-((x - mean_t)^2) / (2 * sigma^2))
        exponent = -((x - mean_t) ** 2) / self._two_sigma_squared
        return self.amplitude * np.exp(exponent)

    def get_perfect_score(self, episode_length: int) -> float:
        """
        Calculate theoretical perfect score for this function.

        For GaussianTranslation with linear dynamics, the perfect score
        assumes the agent can teleport to track the peak exactly at each
        timestep, receiving maximum reward (amplitude) every time.

        Parameters
        ----------
        episode_length : int
            Number of timesteps in the episode.

        Returns
        -------
        float
            Theoretical maximum cumulative reward.

        Notes
        -----
        Perfect score = amplitude * episode_length
        (This assumes perfect tracking of the moving peak)
        """
        # Perfect agent receives amplitude reward at every timestep
        return self.amplitude * np.float64(episode_length)

    @property
    def bounds(self) -> tuple[float, float]:
        """
        Get spatial bounds for agent movement.

        Returns
        -------
        tuple[float, float]
            (left_bound, right_bound) defining valid x-coordinate range.
        """
        return self._bounds
