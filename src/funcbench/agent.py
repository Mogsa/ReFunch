"""Agent interface and action constants for FuncBench.

This module defines the abstract base class for all agent implementations
and the standard action space constants used throughout the system.
"""

# Standard library
from abc import ABC, abstractmethod

# Third-party
import numpy as np

# Action constants (discrete action space)
ACTION_LEFT = 0   # Move left by step_size
ACTION_STAY = 1   # Stay at current position
ACTION_RIGHT = 2  # Move right by step_size


class Agent(ABC):
    """Abstract base class for all agent implementations.

    The Agent interface enforces a standardized contract for all AI implementations,
    enabling easy swapping between different approaches (random, greedy, learning-based,
    LLM-based, etc.). All agents receive the same observation structure and must return
    actions from the discrete action space.

    This interface ensures fair comparison across different agent architectures by
    enforcing identical observation constraints and action spaces.

    Examples
    --------
    >>> class MyAgent(Agent):
    ...     def get_action(self, observation):
    ...         # Custom logic here
    ...         return ACTION_RIGHT
    ...
    >>> agent = MyAgent()
    >>> obs = {'position': 0.0, 'reward': 1.0, 'gradient': np.array([...]),
    ...        'gradient_positions': np.array([...]), 'timestep': 0}
    >>> action = agent.get_action(obs)
    >>> assert action in [0, 1, 2]
    """

    @abstractmethod
    def get_action(self, observation: dict) -> int:
        """Choose action based on current observation.

        This method must be implemented by all subclasses. The agent processes
        the observation dict and returns one of the three discrete actions.

        The observation provides local information within the observation radius
        (fog-of-war constraint), including the agent's current position, reward,
        and gradient samples of the function within the visible window.

        Parameters
        ----------
        observation : dict
            Current observation containing the following keys:

            - 'position' : float
                Agent's current x-coordinate in 1D space
            - 'reward' : float
                Current reward value at agent's position and time
            - 'gradient' : np.ndarray
                Array of function values sampled within observation radius.
                Shape: (n_gradient_samples,). Provides local gradient information
                for decision-making.
            - 'gradient_positions' : np.ndarray
                Array of x-coordinates where gradient samples were taken.
                Shape: (n_gradient_samples,). Corresponds to gradient array.
            - 'timestep' : int
                Current timestep in episode (0 to episode_length-1)

        Returns
        -------
        int
            Action code from discrete action space:

            - 0 : ACTION_LEFT - Move left by step_size
            - 1 : ACTION_STAY - Remain at current position
            - 2 : ACTION_RIGHT - Move right by step_size

        Raises
        ------
        NotImplementedError
            This method must be implemented by subclass

        Notes
        -----
        The agent interface enforces partial observability through the observation
        radius constraint. Agents cannot see the full function surface - only local
        samples within their observation window. This "fog-of-war" constraint ensures
        the benchmark tests temporal pattern learning rather than simple optimization
        with full information.

        The discrete action space (3 actions) keeps the problem simple while allowing
        rich exploration strategies. Continuous action spaces are not supported in
        Phase 1.

        Examples
        --------
        >>> class GreedyAgent(Agent):
        ...     def get_action(self, observation):
        ...         # Follow local gradient
        ...         gradient = observation['gradient']
        ...         peak_idx = np.argmax(gradient)
        ...         peak_pos = observation['gradient_positions'][peak_idx]
        ...         if peak_pos < observation['position']:
        ...             return ACTION_LEFT
        ...         elif peak_pos > observation['position']:
        ...             return ACTION_RIGHT
        ...         else:
        ...             return ACTION_STAY
        """
        pass


class RandomAgent(Agent):
    """Random baseline agent that takes actions uniformly at random.

    The RandomAgent provides the simplest possible baseline for performance
    comparison - it takes actions uniformly at random without considering the
    observation. This establishes the "floor" performance: any learning-based
    agent should significantly outperform random action selection.

    This baseline is critical for validating the benchmark: if random agents
    perform as well as sophisticated agents, the task may be too simple or
    the observation space may not contain sufficient information.

    Parameters
    ----------
    seed : int | None, optional
        Random seed for reproducible action generation. If provided, creates
        a deterministic random number generator that will produce identical
        action sequences across runs. If None (default), uses non-deterministic
        random number generation.

    Attributes
    ----------
    rng : np.random.Generator
        NumPy random number generator instance used for action sampling.

    Notes
    -----
    The RandomAgent uses NumPy's modern random API (np.random.default_rng)
    rather than the legacy global random state (np.random.seed). This provides
    better statistical properties and enables independent random streams across
    multiple agent instances.

    The uniform distribution over actions means:
    - P(ACTION_LEFT) = P(ACTION_STAY) = P(ACTION_RIGHT) = 1/3
    - Expected cumulative reward equals average function value in agent's trajectory
    - No learning or pattern recognition occurs

    For temporal functions like GaussianTranslation where the peak moves predictably,
    a random agent will consistently lag behind because it doesn't track movement.
    This makes it an excellent lower-bound baseline.

    Examples
    --------
    Create a deterministic random agent for reproducible experiments:

    >>> agent = RandomAgent(seed=42)
    >>> obs = {'position': 0.0, 'reward': 1.0, 'gradient': np.array([0.5, 1.0, 0.5]),
    ...        'gradient_positions': np.array([-1.0, 0.0, 1.0]), 'timestep': 0}
    >>> action = agent.get_action(obs)
    >>> assert action in [0, 1, 2]  # Always valid action

    Create a non-deterministic random agent:

    >>> agent = RandomAgent()  # No seed - different behavior each run
    >>> action = agent.get_action(obs)

    Verify reproducibility with seeding:

    >>> agent1 = RandomAgent(seed=42)
    >>> agent2 = RandomAgent(seed=42)
    >>> actions1 = [agent1.get_action(obs) for _ in range(100)]
    >>> actions2 = [agent2.get_action(obs) for _ in range(100)]
    >>> assert actions1 == actions2  # Identical sequences

    See Also
    --------
    Agent : Abstract base class for all agent implementations
    GreedyAgent : Baseline that follows local gradient (Phase 2)
    """

    def __init__(self, seed: int | None = None):
        """Initialize RandomAgent with optional seed for reproducibility.

        Parameters
        ----------
        seed : int | None, optional
            Random seed for deterministic action generation. If None, uses
            non-deterministic random number generation. Default is None.
        """
        self.rng = np.random.default_rng(seed)

    def get_action(self, observation: dict) -> int:
        """Choose action uniformly at random, ignoring observation.

        Samples uniformly from {ACTION_LEFT, ACTION_STAY, ACTION_RIGHT} with
        equal probability (1/3 each). The observation is ignored completely -
        this agent does not use gradient information, reward values, or any
        other environmental feedback.

        Parameters
        ----------
        observation : dict
            Current observation dict (ignored by random baseline).
            Expected keys: position, reward, gradient, gradient_positions, timestep.

        Returns
        -------
        int
            Random action code:
            - 0 (ACTION_LEFT) with probability 1/3
            - 1 (ACTION_STAY) with probability 1/3
            - 2 (ACTION_RIGHT) with probability 1/3

        Notes
        -----
        This method uses self.rng.integers(0, 3) which samples uniformly from
        {0, 1, 2}. The observation parameter is accepted to satisfy the Agent
        interface but is not used in the implementation.

        The random baseline intentionally ignores all environmental information.
        This simplicity makes it a robust lower-bound: any improvement over
        random must come from learning temporal patterns.

        Examples
        --------
        >>> agent = RandomAgent(seed=42)
        >>> obs = {'position': 0.0, 'reward': 1.0, 'gradient': np.array([1.0]),
        ...        'gradient_positions': np.array([0.0]), 'timestep': 0}
        >>> action = agent.get_action(obs)
        >>> assert action in [0, 1, 2]
        """
        return self.rng.integers(0, 3)


class GreedyAgent(Agent):
    """Greedy baseline agent that follows the local gradient.

    The GreedyAgent implements a simple hill-climbing strategy: it always moves
    toward the highest point in its local observation window. This represents a
    purely reactive policy that uses gradient information but has no memory or
    temporal pattern learning.

    This baseline is critical for evaluating whether agents learn temporal dynamics:
    - For stationary peaks: Greedy reaches optimal performance (finds and stays at peak)
    - For moving peaks: Greedy lags behind, always chasing (suboptimal)
    - Any temporal pattern learning should significantly outperform greedy on moving targets

    The greedy agent demonstrates the limitations of reactive policies and validates
    that the benchmark requires understanding temporal dynamics to achieve near-optimal
    performance.

    Attributes
    ----------
    None
        GreedyAgent is stateless - decisions depend only on current observation.

    Notes
    -----
    The GreedyAgent uses a simple tolerance-based decision rule:
    1. Find the position of maximum gradient value within observation window
    2. If peak is LEFT of current position (beyond tolerance): move LEFT
    3. If peak is RIGHT of current position (beyond tolerance): move RIGHT
    4. If peak is AT current position (within tolerance 0.1): STAY

    The tolerance threshold prevents oscillation when the agent is very close to
    the local maximum. Without this, the agent might alternate between moving
    left and right when nearly centered on the peak.

    **Greedy Limitations on Temporal Functions:**
    - **Stationary peaks**: Optimal performance (reaches peak in ~10 steps, stays there)
    - **Linear translation**: Lags behind by roughly (velocity / step_size) units
    - **Accelerating peaks**: Increasing lag, eventually loses track
    - **Oscillating peaks**: Constantly chasing, phase-shifted

    For GaussianTranslation with velocity=0.1 and step_size=1.0, the greedy agent
    will typically trail 1-2 units behind the moving peak, achieving ~60-80% of
    perfect score depending on the Gaussian width.

    Examples
    --------
    Create and use a greedy agent:

    >>> agent = GreedyAgent()
    >>> obs = {
    ...     'position': 0.0,
    ...     'reward': 0.5,
    ...     'gradient': np.array([0.3, 0.8, 0.6]),  # Peak at index 1
    ...     'gradient_positions': np.array([-1.0, 0.0, 1.0]),
    ...     'timestep': 0
    ... }
    >>> action = agent.get_action(obs)
    >>> assert action == ACTION_STAY  # Peak is at current position (0.0)

    Example where peak is to the right:

    >>> obs = {
    ...     'position': 0.0,
    ...     'gradient': np.array([0.3, 0.5, 0.9]),  # Peak at index 2
    ...     'gradient_positions': np.array([-1.0, 0.0, 1.0]),  # Peak at x=1.0
    ...     'timestep': 0
    ... }
    >>> action = agent.get_action(obs)
    >>> assert action == ACTION_RIGHT  # Move toward peak at x=1.0

    Compare greedy to random on stationary peak:

    >>> from funcbench import GaussianTranslation, Environment
    >>> func = GaussianTranslation(mean_start=0.0, velocity=0.0)  # Stationary
    >>> env = Environment(func, episode_length=100)
    >>>
    >>> greedy_agent = GreedyAgent()
    >>> greedy_score = env.run(greedy_agent)  # Should approach perfect score
    >>>
    >>> from funcbench import RandomAgent
    >>> random_agent = RandomAgent(seed=42)
    >>> random_score = env.run(random_agent)  # Much lower
    >>>
    >>> assert greedy_score > random_score  # Greedy significantly better

    See Also
    --------
    Agent : Abstract base class for all agent implementations
    RandomAgent : Random baseline (lower bound)
    """

    def get_action(self, observation: dict) -> int:
        """Choose action by following local gradient (hill-climbing).

        Finds the position of maximum gradient value within the observation window
        and moves toward it. Uses a tolerance threshold to avoid oscillation when
        very close to the peak.

        Decision logic:
        1. Find index of maximum gradient: argmax(observation['gradient'])
        2. Get position of that maximum: gradient_positions[argmax_index]
        3. Compare to current position:
           - If peak_position < current_position - 0.1: move LEFT
           - If peak_position > current_position + 0.1: move RIGHT
           - Otherwise (within tolerance): STAY

        Parameters
        ----------
        observation : dict
            Current observation containing:
            - 'position' : float - Agent's current x-coordinate
            - 'gradient' : np.ndarray - Function values sampled within observation radius
            - 'gradient_positions' : np.ndarray - x-coordinates of gradient samples
            - 'reward' : float - Current reward (not used by greedy)
            - 'timestep' : int - Current timestep (not used by greedy)

        Returns
        -------
        int
            Action code:
            - 0 (ACTION_LEFT) if local maximum is to the left
            - 1 (ACTION_STAY) if local maximum is at current position (within tolerance)
            - 2 (ACTION_RIGHT) if local maximum is to the right

        Notes
        -----
        This is a purely reactive policy - the agent has no memory of previous
        observations or actions. Decisions depend only on the current gradient.

        The tolerance threshold (0.1) is chosen to be smaller than step_size (1.0)
        to prevent oscillation while still ensuring the agent moves when needed.

        For temporal functions where the peak moves:
        - If velocity > step_size: Greedy cannot keep up, will fall behind
        - If velocity < step_size: Greedy trails behind by roughly velocity/step_size units
        - If velocity = 0: Greedy reaches optimal (finds peak and stays)

        Examples
        --------
        >>> agent = GreedyAgent()
        >>>
        >>> # Peak to the left
        >>> obs_left = {
        ...     'position': 0.0,
        ...     'gradient': np.array([0.9, 0.5, 0.3]),
        ...     'gradient_positions': np.array([-1.0, 0.0, 1.0]),
        ...     'reward': 0.5,
        ...     'timestep': 0
        ... }
        >>> agent.get_action(obs_left)
        0  # ACTION_LEFT
        >>>
        >>> # Peak to the right
        >>> obs_right = {
        ...     'position': 0.0,
        ...     'gradient': np.array([0.3, 0.5, 0.9]),
        ...     'gradient_positions': np.array([-1.0, 0.0, 1.0]),
        ...     'reward': 0.5,
        ...     'timestep': 0
        ... }
        >>> agent.get_action(obs_right)
        2  # ACTION_RIGHT
        >>>
        >>> # Peak at current position
        >>> obs_stay = {
        ...     'position': 0.0,
        ...     'gradient': np.array([0.6, 1.0, 0.6]),
        ...     'gradient_positions': np.array([-1.0, 0.0, 1.0]),
        ...     'reward': 1.0,
        ...     'timestep': 0
        ... }
        >>> agent.get_action(obs_stay)
        1  # ACTION_STAY
        """
        # Extract gradient information from observation
        gradient = observation['gradient']
        gradient_positions = observation['gradient_positions']
        current_position = observation['position']

        # Find position of maximum gradient value
        max_gradient_index = np.argmax(gradient)
        peak_position = gradient_positions[max_gradient_index]

        # Tolerance for considering peak "at" current position
        tolerance = 0.1

        # Decide action based on where peak is relative to current position
        if peak_position < current_position - tolerance:
            # Peak is to the left
            return ACTION_LEFT
        elif peak_position > current_position + tolerance:
            # Peak is to the right
            return ACTION_RIGHT
        else:
            # Peak is at current position (within tolerance)
            return ACTION_STAY
