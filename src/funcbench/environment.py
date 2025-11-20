"""Environment for managing episode lifecycle and agent-function interactions.

This module provides the Environment class that coordinates between temporal
functions and agents, managing episode state, observations, and execution flow.
"""

# Standard library
from typing import Dict

# Third-party
import numpy as np

# Local
from funcbench.function import Function2D
from funcbench.agent import ACTION_LEFT, ACTION_STAY, ACTION_RIGHT


class Environment:
    """Environment for managing episode lifecycle and agent-function interactions.

    The Environment class implements a Gym-like API for coordinating episode execution.
    It manages episode state (position, timestep, rewards, history), generates
    observations for agents within the observation radius constraint (fog-of-war),
    and handles action execution and state transitions.

    The environment follows a centralized state dict pattern for easy serialization
    and reproducible experiments. All numeric state values use float64 precision
    to ensure reproducibility across platforms.

    Parameters
    ----------
    function : Function2D
        The temporal function defining the reward landscape. Must implement
        evaluate() and get_perfect_score() methods.
    episode_length : int, default=1000
        Number of timesteps per episode. Episodes terminate after this many steps.
    observation_radius : float, default=5.0
        Fog-of-war radius defining the local observation window size.
        Agents can only observe function values within this radius around their
        current position.
    n_gradient_samples : int, default=20
        Number of spatial samples taken within the observation radius to provide
        gradient information to the agent.
    step_size : float, default=1.0
        Distance moved when agent takes ACTION_LEFT or ACTION_RIGHT.
    render_mode : bool, default=False
        Enable visualization (reserved for Epic 4 visualizer integration).
        When False, environment runs in headless mode for batch evaluation.

    Attributes
    ----------
    function : Function2D
        Reference to the temporal function instance.
    episode_length : int
        Maximum number of timesteps per episode.
    observation_radius : float
        Fog-of-war radius for local observations.
    n_gradient_samples : int
        Number of gradient samples within observation window.
    step_size : float
        Movement distance per action.
    render_mode : bool
        Visualization flag (Epic 4 integration point).
    state : dict
        Centralized state dictionary containing position, timestep,
        cumulative_reward, and history.

    Examples
    --------
    >>> from funcbench import GaussianTranslation, Environment
    >>> func = GaussianTranslation()
    >>> env = Environment(func, episode_length=1000)
    >>> observation = env.reset()
    >>> # observation contains: position, reward, gradient, gradient_positions, timestep

    Notes
    -----
    - All state initialization uses float64 precision for reproducibility (NFR11)
    - State is stored in centralized dict for easy serialization (ADR-005)
    - Follows Gym-like API pattern: reset(), step(), run() (ADR-004)
    - Initial position is 0.0 (center of typical bounds like [-20, 20])
    """

    def __init__(
        self,
        function: Function2D,
        episode_length: int = 1000,
        observation_radius: float = 5.0,
        n_gradient_samples: int = 20,
        step_size: float = 1.0,
        render_mode: bool = False,
    ) -> None:
        """Initialize Environment with configuration parameters.

        Parameters
        ----------
        function : Function2D
            Temporal function defining reward landscape
        episode_length : int, default=1000
            Number of timesteps per episode
        observation_radius : float, default=5.0
            Fog-of-war radius for observations
        n_gradient_samples : int, default=20
            Number of gradient samples in observation window
        step_size : float, default=1.0
            Movement distance per action
        render_mode : bool, default=False
            Enable visualization (Epic 4)
        """
        # Store configuration as instance attributes
        self.function = function
        self.episode_length = episode_length
        self.observation_radius = observation_radius
        self.n_gradient_samples = n_gradient_samples
        self.step_size = step_size
        self.render_mode = render_mode

        # Initialize centralized state dict with correct types
        # Using explicit np.float64 for reproducibility (NFR11)
        self.state: Dict = {
            'position': np.float64(0.0),        # Agent x-coordinate
            'timestep': 0,                      # Current time (0 to episode_length-1)
            'cumulative_reward': np.float64(0.0),  # Running sum of rewards
            'history': [],                      # Episode records: [(timestep, position, reward, action), ...]
        }

    def reset(self) -> dict:
        """Start new episode by resetting state and returning initial observation.

        Resets all state values to their initial conditions:
        - Position initialized to 0.0 (center of typical bounds)
        - Timestep reset to 0
        - Cumulative reward reset to 0.0
        - History cleared

        Returns
        -------
        dict
            Initial observation dictionary with keys:

            - 'position' : float
                Agent's initial x-coordinate (0.0)
            - 'reward' : float
                Initial reward at starting position
            - 'gradient' : np.ndarray
                Local function samples within observation radius
            - 'gradient_positions' : np.ndarray
                X-coordinates where gradient samples were taken
            - 'timestep' : int
                Current timestep (0 after reset)

        Notes
        -----
        - All numeric values use float64 precision for reproducibility
        - Observation dict structure is contractually required by Agent interface
        - Reset can be called multiple times to start new episodes
        - Full observation generation implemented in Story 2.3

        Examples
        --------
        >>> env = Environment(GaussianTranslation())
        >>> obs = env.reset()
        >>> obs['position']
        0.0
        >>> obs['timestep']
        0
        """
        # Reset position to center (0.0) using explicit float64
        self.state['position'] = np.float64(0.0)

        # Reset timestep to episode start
        self.state['timestep'] = 0

        # Reset cumulative reward to zero using explicit float64
        self.state['cumulative_reward'] = np.float64(0.0)

        # Clear history list
        self.state['history'] = []

        # Generate and return initial observation
        return self._get_observation()

    def _get_observation(self) -> dict:
        """Generate observation dict from current state.

        Creates the observation dictionary that agents receive, containing
        the agent's current position, reward, local gradient samples, and
        timestep information. This method enforces the observation contract
        required by the Agent interface.

        The gradient sampling implements the "fog-of-war" constraint by only
        providing local function information within the observation radius.
        Samples are uniformly distributed using np.linspace and clipped to
        function bounds to prevent out-of-bounds evaluation.

        Returns
        -------
        dict
            Observation dictionary with exact keys required by Agent interface:

            - 'position' : float
                Agent's current x-coordinate
            - 'reward' : float
                Reward at current position and timestep
            - 'gradient' : np.ndarray
                Local function samples within observation radius (shape: n_gradient_samples)
            - 'gradient_positions' : np.ndarray
                X-coordinates where gradient samples were taken (shape: n_gradient_samples)
            - 'timestep' : int
                Current timestep in episode

        Notes
        -----
        - Uses vectorized NumPy operations for performance (< 5ms target)
        - All arrays use float64 dtype for reproducibility (NFR11)
        - Gradient positions are clipped to function bounds
        - Single vectorized function call for all gradient samples (no loops)
        - Reward calculated at agent's exact position

        The observation dictionary keys are contractually required by the
        Agent interface and must not be changed without updating all agent
        implementations.

        Examples
        --------
        >>> env = Environment(GaussianTranslation(), n_gradient_samples=5)
        >>> env.reset()
        >>> obs = env._get_observation()
        >>> obs['gradient'].shape
        (5,)
        >>> obs['gradient_positions'].shape
        (5,)
        """
        # Calculate observation window: [position - radius, position + radius]
        window_left = self.state['position'] - self.observation_radius
        window_right = self.state['position'] + self.observation_radius

        # Generate n_gradient_samples points uniformly within window
        gradient_positions = np.linspace(
            window_left, window_right, self.n_gradient_samples
        )

        # Clip sample positions to function bounds to prevent out-of-bounds evaluation
        gradient_positions = np.clip(
            gradient_positions,
            self.function.bounds[0],
            self.function.bounds[1]
        )

        # Vectorized evaluation: single function call for all gradient samples
        gradient = self.function.evaluate(gradient_positions, self.state['timestep'])

        # Calculate reward at current agent position
        reward_array = self.function.evaluate(
            np.array([self.state['position']]), self.state['timestep']
        )
        reward = float(reward_array[0])  # Extract scalar from array

        # Build observation dictionary with all required keys
        return {
            'position': float(self.state['position']),
            'reward': reward,
            'gradient': gradient,
            'gradient_positions': gradient_positions,
            'timestep': self.state['timestep'],
        }

    def step(self, action: int) -> tuple[dict, float, bool, dict]:
        """Execute action and advance episode state.

        Executes the specified action to update the agent's position, evaluates
        the reward at the new position, increments timestep, and checks for
        episode completion. This method implements the core step logic of the
        Gym-like API.

        The step execution follows this sequence:
        1. Validate action is valid (0, 1, or 2)
        2. Update position based on action
        3. Clamp position to function bounds
        4. Calculate reward at new position
        5. Update cumulative reward
        6. Advance timestep
        7. Check if episode is done
        8. Generate new observation
        9. Build info dict
        10. Return 4-tuple

        Parameters
        ----------
        action : int
            Action to execute from discrete action space:

            - 0 : ACTION_LEFT - Move left by step_size
            - 1 : ACTION_STAY - Remain at current position
            - 2 : ACTION_RIGHT - Move right by step_size

        Returns
        -------
        observation : dict
            Agent's observation after action execution. Contains keys:
            'position', 'reward', 'gradient', 'gradient_positions', 'timestep'
        reward : float
            Reward value at new position and current timestep
        done : bool
            True if episode finished (timestep >= episode_length), False otherwise
        info : dict
            Additional information containing:

            - 'cumulative_reward' : float
                Running total of all rewards accumulated this episode
            - 'perfect_score' : float
                Theoretical maximum achievable cumulative reward

        Raises
        ------
        ValueError
            If action is not 0, 1, or 2

        Notes
        -----
        - All state updates are atomic (happen within this method)
        - Position is clamped to function.bounds using np.clip
        - Reward calculated using function.evaluate(position, timestep)
        - float64 precision maintained for cumulative_reward
        - info dict is JSON-serializable (numpy types converted to float)
        - Observation generated AFTER state updates to reflect new state

        Performance target is < 10ms per step including observation generation.

        Examples
        --------
        >>> env = Environment(GaussianTranslation())
        >>> obs = env.reset()
        >>> obs, reward, done, info = env.step(ACTION_RIGHT)
        >>> obs['position']  # Position increased by step_size
        1.0
        >>> done  # Not done on first step
        False
        >>> info['cumulative_reward']  # Equals reward on first step
        0.5
        """
        # 1. Validate action
        if action not in [0, 1, 2]:
            raise ValueError(
                f"Invalid action {action}. Must be 0 (left), 1 (stay), or 2 (right)"
            )

        # 2. Update position based on action
        if action == ACTION_LEFT:
            self.state['position'] -= self.step_size
        elif action == ACTION_RIGHT:
            self.state['position'] += self.step_size
        # ACTION_STAY: no change to position

        # 3. Clamp position to bounds
        self.state['position'] = np.clip(
            self.state['position'],
            self.function.bounds[0],
            self.function.bounds[1]
        )

        # 4. Calculate reward at new position
        reward_array = self.function.evaluate(
            np.array([self.state['position']]),
            self.state['timestep']
        )
        reward = float(reward_array[0])

        # 5. Update cumulative reward
        self.state['cumulative_reward'] += reward

        # 6. Advance timestep
        self.state['timestep'] += 1

        # 6.5. Append history entry (timestep, position, reward, action)
        self.state['history'].append((
            self.state['timestep'] - 1,  # Use timestep before increment (when action was taken)
            float(self.state['position']),
            reward,
            action
        ))

        # 7. Check if episode is done
        done = self.state['timestep'] >= self.episode_length

        # 8. Generate observation
        observation = self._get_observation()

        # 9. Build info dict
        info = {
            'cumulative_reward': float(self.state['cumulative_reward']),
            'perfect_score': self.function.get_perfect_score(self.episode_length)
        }

        return observation, reward, done, info

    def get_history(self) -> list[tuple[int, float, float, int]]:
        """Get copy of episode history.

        Returns episode history as list of tuples, where each tuple contains:
        (timestep, position, reward, action).

        Returns
        -------
        list of tuple
            List of (timestep: int, position: float, reward: float, action: int) tuples
            in chronological order (order of step execution).

        Notes
        -----
        Returns a copy of the internal history to prevent external modifications.
        History does not include observations (too large for storage).

        History tuple structure:
        - timestep (int): The timestep when the action was taken (0 to episode_length-1)
        - position (float): Agent's position after the action
        - reward (float): Reward received at that position and timestep
        - action (int): Action taken (0=left, 1=stay, 2=right)

        Examples
        --------
        >>> env = Environment(func, episode_length=1000)
        >>> obs = env.reset()
        >>> obs, reward, done, info = env.step(ACTION_RIGHT)
        >>> history = env.get_history()
        >>> print(history[0])  # First step
        (0, 1.0, 0.5, 2)  # (timestep, position, reward, action)
        """
        return list(self.state['history'])

    def get_config(self) -> dict:
        """Get environment configuration parameters.

        Returns complete environment configuration as JSON-serializable dictionary,
        including environment settings and function parameters. Enables reproducible
        experiment setup by providing all parameters needed to reconstruct the
        environment.

        Returns
        -------
        dict
            Configuration dictionary with keys:

            - 'episode_length' : int
                Number of timesteps per episode
            - 'observation_radius' : float
                Fog-of-war window size for local observations
            - 'n_gradient_samples' : int
                Number of local samples taken within observation radius
            - 'step_size' : float
                Distance moved per ACTION_LEFT or ACTION_RIGHT
            - 'function_params' : dict
                Function-specific configuration from function.get_config().
                Empty dict if function doesn't support get_config().
            - 'bounds' : tuple[float, float]
                Spatial bounds (left, right) from function

        Notes
        -----
        - Returns a copy of configuration to prevent external modifications
        - All values are JSON-serializable for saving experiments
        - function_params may be empty dict if function doesn't implement get_config()
        - Configuration enables exact environment reconstruction for reproducibility
        - Method completes in < 1ms (simple dict construction)

        Examples
        --------
        >>> from funcbench import GaussianTranslation, Environment
        >>> func = GaussianTranslation(velocity=0.1, seed=42)
        >>> env = Environment(func, episode_length=1000)
        >>> config = env.get_config()
        >>> print(config['episode_length'])
        1000
        >>> import json
        >>> json_str = json.dumps(config)  # Save configuration
        """
        # Get function configuration if available
        if hasattr(self.function, 'get_config'):
            function_params = self.function.get_config()
        else:
            function_params = {}

        # Build configuration dict (creates copy)
        config = {
            'episode_length': self.episode_length,
            'observation_radius': self.observation_radius,
            'n_gradient_samples': self.n_gradient_samples,
            'step_size': self.step_size,
            'function_params': function_params,
            'bounds': self.function.bounds
        }

        return config

    def run(self, agent, render: bool = False) -> float:
        """Run complete episode with given agent.

        Executes full episode by calling reset(), then looping agent.get_action()
        and step() until done. Convenience method for evaluating agents without
        manually writing episode loops.

        This method provides a simple interface for researchers to quickly evaluate
        agent performance. It handles the entire episode execution lifecycle and
        returns only the final cumulative reward for easy comparison.

        Parameters
        ----------
        agent : Agent
            Agent implementing get_action(observation) -> int interface.
            The agent will be called once per timestep to select actions.
        render : bool, default=False
            Enable visualization if visualizer exists (Epic 4 integration).
            If True but visualizer not initialized, prints warning and continues
            headless. Use False for batch evaluation and performance.

        Returns
        -------
        float
            Final cumulative reward at episode completion. This is the sum of
            all rewards obtained across the entire episode.

        Raises
        ------
        ValueError
            If agent raises exception during get_action(). The error message
            includes agent type, current timestep, and original exception for
            debugging.

        Notes
        -----
        - Visualizer integration is placeholder for Epic 4
        - If render=True but visualizer=None, prints warning and runs headless
        - Performance target: 1000-step episode in < 2 seconds (headless mode)
        - Agent exceptions are caught and re-raised with context for debugging
        - Episode state and history are preserved after run() completes

        The render parameter is prepared for future Epic 4 integration but
        currently only affects warning messages (visualizer not yet implemented).

        Examples
        --------
        >>> from funcbench import GaussianTranslation, Environment, RandomAgent
        >>> func = GaussianTranslation(velocity=0.1, seed=42)
        >>> env = Environment(func, episode_length=1000)
        >>> agent = RandomAgent(seed=42)
        >>> score = env.run(agent, render=False)
        >>> print(f"Final score: {score:.2f}")
        Final score: 450.32

        >>> # Multiple episodes with same agent
        >>> scores = [env.run(agent, render=False) for _ in range(10)]
        >>> avg_score = sum(scores) / len(scores)
        """
        # Get initial observation
        observation = self.reset()

        # Episode loop
        done = False
        while not done:
            try:
                # Get agent action
                action = agent.get_action(observation)
            except Exception as e:
                raise ValueError(
                    f"Agent {agent.__class__.__name__} raised exception at "
                    f"timestep {self.state['timestep']} during get_action(): {e}"
                ) from e

            # Execute action
            observation, reward, done, info = self.step(action)

            # Visualizer update (placeholder for Epic 4)
            if render:
                if hasattr(self, 'visualizer') and self.visualizer is not None:
                    # Epic 4 will implement visualizer.update()
                    self.visualizer.update(self.state)
                elif not hasattr(self, '_render_warning_shown'):
                    print("Visualization requested but visualizer not initialized. Running headless.")
                    self._render_warning_shown = True

        # Return final cumulative reward
        return self.state['cumulative_reward']
