"""Basic tests for Agent abstract base class and action constants.

Note: Comprehensive agent tests will be added in Story 2.8 (Create Environment Unit Tests).
This module provides initial validation that the Agent interface is correctly defined.
"""

import inspect
import pytest
import numpy as np
from funcbench.agent import Agent, RandomAgent, GreedyAgent, ACTION_LEFT, ACTION_STAY, ACTION_RIGHT


class TestActionConstants:
    """Test action constant values."""

    def test_action_constants_values(self):
        """Action constants have correct integer values."""
        assert ACTION_LEFT == 0
        assert ACTION_STAY == 1
        assert ACTION_RIGHT == 2

    def test_action_constants_types(self):
        """Action constants are integers, not floats or strings."""
        assert isinstance(ACTION_LEFT, int)
        assert isinstance(ACTION_STAY, int)
        assert isinstance(ACTION_RIGHT, int)


class TestAgentInterface:
    """Test Agent abstract base class interface."""

    def test_agent_is_abstract(self):
        """Agent cannot be instantiated directly (abstract base class)."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            Agent()

    def test_agent_requires_get_action(self):
        """Subclass without get_action() cannot be instantiated."""
        class IncompleteAgent(Agent):
            pass

        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            IncompleteAgent()

    def test_agent_subclass_with_get_action_works(self):
        """Subclass with get_action() can be instantiated."""
        class MockAgent(Agent):
            def get_action(self, observation: dict) -> int:
                return ACTION_RIGHT

        # Should not raise - complete implementation
        agent = MockAgent()
        assert isinstance(agent, Agent)

    def test_get_action_signature(self):
        """get_action() has correct type hints."""
        import inspect

        # Get the get_action method signature from Agent
        sig = inspect.signature(Agent.get_action)

        # Check parameter: observation should be dict
        assert 'observation' in sig.parameters
        assert sig.parameters['observation'].annotation == dict

        # Check return type should be int
        assert sig.return_annotation == int

    def test_mock_agent_returns_valid_action(self):
        """Mock agent implementation returns valid action codes."""
        class MockAgent(Agent):
            def get_action(self, observation: dict) -> int:
                return ACTION_LEFT

        agent = MockAgent()
        obs = {
            'position': 0.0,
            'reward': 1.0,
            'gradient': np.array([0.5, 1.0, 0.5]),
            'gradient_positions': np.array([-1.0, 0.0, 1.0]),
            'timestep': 0
        }

        action = agent.get_action(obs)
        assert action in [ACTION_LEFT, ACTION_STAY, ACTION_RIGHT]
        assert action == ACTION_LEFT

    def test_agent_has_docstring(self):
        """Agent class has docstring documentation."""
        assert Agent.__doc__ is not None
        assert len(Agent.__doc__) > 50  # Should have substantial documentation

    def test_get_action_has_docstring(self):
        """get_action method has comprehensive docstring."""
        assert Agent.get_action.__doc__ is not None
        assert 'observation' in Agent.get_action.__doc__.lower()
        assert 'action' in Agent.get_action.__doc__.lower()

    def test_observation_dict_structure_documented(self):
        """Docstring documents observation dict structure."""
        docstring = Agent.get_action.__doc__
        required_keys = ['position', 'reward', 'gradient', 'gradient_positions', 'timestep']

        for key in required_keys:
            assert key in docstring, f"Observation key '{key}' should be documented"

    def test_action_values_documented(self):
        """Docstring documents action return values (0, 1, 2)."""
        docstring = Agent.get_action.__doc__
        assert '0' in docstring  # ACTION_LEFT
        assert '1' in docstring  # ACTION_STAY
        assert '2' in docstring  # ACTION_RIGHT


class TestRandomAgent:
    """Test RandomAgent baseline implementation (Story 3.1)."""

    def test_random_agent_reproducibility(self):
        """Same seed produces identical action sequences (AC2, AC3, AC6)."""
        # Create two agents with same seed
        agent1 = RandomAgent(seed=42)
        agent2 = RandomAgent(seed=42)

        # Mock observation dict
        obs = {
            'position': 0.0,
            'reward': 1.0,
            'gradient': np.array([0.5, 1.0, 0.5]),
            'gradient_positions': np.array([-1.0, 0.0, 1.0]),
            'timestep': 0
        }

        # Generate 100 actions from each agent
        actions1 = [agent1.get_action(obs) for _ in range(100)]
        actions2 = [agent2.get_action(obs) for _ in range(100)]

        # Assert sequences are identical
        assert actions1 == actions2, "Same seed must produce identical action sequences"

    def test_different_seeds_produce_different_sequences(self):
        """Different seeds produce different action sequences (AC2, AC3, AC6)."""
        # Create two agents with different seeds
        agent1 = RandomAgent(seed=42)
        agent2 = RandomAgent(seed=99)

        # Mock observation
        obs = {
            'position': 0.0,
            'reward': 1.0,
            'gradient': np.array([0.5, 1.0, 0.5]),
            'gradient_positions': np.array([-1.0, 0.0, 1.0]),
            'timestep': 0
        }

        # Generate 100 actions from each
        actions1 = [agent1.get_action(obs) for _ in range(100)]
        actions2 = [agent2.get_action(obs) for _ in range(100)]

        # Assert sequences differ
        assert actions1 != actions2, "Different seeds should produce different sequences"

    def test_actions_in_valid_range(self):
        """All actions are in valid range {0, 1, 2} (AC4, AC5)."""
        agent = RandomAgent(seed=42)
        obs = {
            'position': 0.0,
            'reward': 1.0,
            'gradient': np.array([1.0]),
            'gradient_positions': np.array([0.0]),
            'timestep': 0
        }

        # Generate 1000 actions
        actions = [agent.get_action(obs) for _ in range(1000)]

        # Verify all actions are valid
        for action in actions:
            assert action in [0, 1, 2], f"Invalid action: {action}"
            assert isinstance(action, (int, np.integer)), "Action must be integer type"

    def test_uniform_distribution(self):
        """Actions follow uniform distribution (AC5)."""
        agent = RandomAgent(seed=42)
        obs = {
            'position': 0.0,
            'reward': 1.0,
            'gradient': np.array([1.0]),
            'gradient_positions': np.array([0.0]),
            'timestep': 0
        }

        # Generate large sample (3000 actions)
        n_samples = 3000
        actions = [agent.get_action(obs) for _ in range(n_samples)]

        # Count occurrences of each action
        counts = {0: 0, 1: 0, 2: 0}
        for action in actions:
            counts[action] += 1

        # Expected count for each action (uniform distribution)
        expected = n_samples / 3  # 1000

        # Allow 10% tolerance for randomness
        tolerance = expected * 0.1

        # Verify each action appears approximately expected times
        for action_code, count in counts.items():
            assert abs(count - expected) < tolerance, \
                f"Action {action_code} count {count} deviates too much from expected {expected}"

    def test_random_agent_inherits_from_agent(self):
        """RandomAgent is instance of Agent (AC1, AC4)."""
        agent = RandomAgent()
        assert isinstance(agent, Agent), "RandomAgent must inherit from Agent"
        assert isinstance(agent, RandomAgent), "Agent must be instance of RandomAgent"

    def test_get_action_signature(self):
        """get_action has correct type hints (AC4)."""
        # Get the get_action method signature from RandomAgent
        sig = inspect.signature(RandomAgent.get_action)

        # Check parameter: observation should be dict
        assert 'observation' in sig.parameters
        assert sig.parameters['observation'].annotation == dict, \
            "observation parameter must have type hint 'dict'"

        # Check return type should be int
        assert sig.return_annotation == int, "Return type must be 'int'"

    def test_random_agent_has_docstring(self):
        """RandomAgent and get_action have comprehensive docstrings (AC7)."""
        # Check class docstring
        assert RandomAgent.__doc__ is not None, "RandomAgent must have docstring"
        assert len(RandomAgent.__doc__) > 50, "Docstring should be comprehensive"

        class_doc = RandomAgent.__doc__.lower()
        assert 'random' in class_doc, "Docstring should mention 'random'"
        assert 'baseline' in class_doc, "Docstring should mention 'baseline'"
        assert 'seed' in class_doc, "Docstring should mention 'seed'"

        # Check get_action docstring
        assert RandomAgent.get_action.__doc__ is not None, "get_action must have docstring"
        method_doc = RandomAgent.get_action.__doc__.lower()
        assert 'observation' in method_doc, "Docstring should document observation parameter"
        assert 'action' in method_doc or 'return' in method_doc, "Docstring should document return value"

    def test_ignores_observation(self):
        """RandomAgent ignores observation dict content (AC4)."""
        agent = RandomAgent(seed=42)

        # Create two different observations
        obs1 = {
            'position': 0.0,
            'reward': 1.0,
            'gradient': np.array([0.5, 1.0, 0.5]),
            'gradient_positions': np.array([-1.0, 0.0, 1.0]),
            'timestep': 0
        }

        obs2 = {
            'position': 100.0,
            'reward': 0.0,
            'gradient': np.array([0.0, 0.0, 0.0]),
            'gradient_positions': np.array([99.0, 100.0, 101.0]),
            'timestep': 999
        }

        # Generate actions with same seed but different observations
        agent1 = RandomAgent(seed=42)
        agent2 = RandomAgent(seed=42)

        actions1 = [agent1.get_action(obs1) for _ in range(50)]
        actions2 = [agent2.get_action(obs2) for _ in range(50)]

        # Actions should be identical (depends only on seed, not observation)
        assert actions1 == actions2, \
            "RandomAgent should ignore observation content - actions depend only on seed"

    def test_random_agent_initialization_with_seed(self):
        """RandomAgent initializes with seed parameter (AC2)."""
        agent = RandomAgent(seed=42)
        assert hasattr(agent, 'rng'), "Agent should have rng attribute"
        assert isinstance(agent.rng, np.random.Generator), \
            "rng should be numpy.random.Generator instance"

    def test_random_agent_initialization_without_seed(self):
        """RandomAgent initializes without seed (non-deterministic) (AC2, AC3)."""
        agent = RandomAgent()
        assert hasattr(agent, 'rng'), "Agent should have rng attribute"
        assert isinstance(agent.rng, np.random.Generator), \
            "rng should be numpy.random.Generator instance"

        # Without seed, two agents should produce different sequences
        agent1 = RandomAgent()
        agent2 = RandomAgent()

        obs = {
            'position': 0.0,
            'reward': 1.0,
            'gradient': np.array([1.0]),
            'gradient_positions': np.array([0.0]),
            'timestep': 0
        }

        actions1 = [agent1.get_action(obs) for _ in range(100)]
        actions2 = [agent2.get_action(obs) for _ in range(100)]

        # Very unlikely (but not impossible) that random sequences match
        # We test this to demonstrate non-determinism
        # Note: This test could theoretically fail by chance, but probability is extremely low
        assert actions1 != actions2, \
            "Without seed, different agents should produce different sequences (non-deterministic)"


class TestGreedyAgent:
    """Test GreedyAgent baseline implementation (Story 3.2)."""

    def test_greedy_agent_inherits_from_agent(self):
        """GreedyAgent is instance of Agent (AC1)."""
        agent = GreedyAgent()
        assert isinstance(agent, Agent), "GreedyAgent must inherit from Agent"
        assert isinstance(agent, GreedyAgent), "Agent must be instance of GreedyAgent"

    def test_greedy_moves_left_when_peak_is_left(self):
        """GreedyAgent moves left when gradient peak is to the left (AC2)."""
        agent = GreedyAgent()

        # Peak is at index 0 (position -1.0), left of current position (0.0)
        obs = {
            'position': 0.0,
            'reward': 0.5,
            'gradient': np.array([0.9, 0.5, 0.3]),  # Descending left to right
            'gradient_positions': np.array([-1.0, 0.0, 1.0]),
            'timestep': 0
        }

        action = agent.get_action(obs)
        assert action == ACTION_LEFT, "Should move left toward peak"

    def test_greedy_moves_right_when_peak_is_right(self):
        """GreedyAgent moves right when gradient peak is to the right (AC2)."""
        agent = GreedyAgent()

        # Peak is at index 2 (position 1.0), right of current position (0.0)
        obs = {
            'position': 0.0,
            'reward': 0.5,
            'gradient': np.array([0.3, 0.5, 0.9]),  # Ascending left to right
            'gradient_positions': np.array([-1.0, 0.0, 1.0]),
            'timestep': 0
        }

        action = agent.get_action(obs)
        assert action == ACTION_RIGHT, "Should move right toward peak"

    def test_greedy_stays_when_peak_is_at_position(self):
        """GreedyAgent stays when gradient peak is at current position (AC2)."""
        agent = GreedyAgent()

        # Peak is at index 1 (position 0.0), at current position (0.0)
        obs = {
            'position': 0.0,
            'reward': 1.0,
            'gradient': np.array([0.6, 1.0, 0.6]),  # Peak in middle
            'gradient_positions': np.array([-1.0, 0.0, 1.0]),
            'timestep': 0
        }

        action = agent.get_action(obs)
        assert action == ACTION_STAY, "Should stay at peak"

    def test_tolerance_threshold_stay(self):
        """GreedyAgent uses tolerance threshold for STAY decision (AC3)."""
        agent = GreedyAgent()

        # Peak at position 0.05 (within 0.1 tolerance of current position 0.0)
        obs = {
            'position': 0.0,
            'reward': 0.95,
            'gradient': np.array([0.6, 0.9, 1.0, 0.9, 0.6]),
            'gradient_positions': np.array([-0.2, -0.1, 0.05, 0.1, 0.2]),
            'timestep': 0
        }

        action = agent.get_action(obs)
        assert action == ACTION_STAY, "Should stay when peak within tolerance (0.1)"

    def test_tolerance_threshold_move(self):
        """GreedyAgent moves when peak is beyond tolerance (AC3)."""
        agent = GreedyAgent()

        # Peak at position 0.15 (beyond 0.1 tolerance from current position 0.0)
        obs = {
            'position': 0.0,
            'reward': 0.8,
            'gradient': np.array([0.6, 0.8, 0.9, 1.0, 0.9]),
            'gradient_positions': np.array([-0.2, -0.1, 0.0, 0.15, 0.2]),
            'timestep': 0
        }

        action = agent.get_action(obs)
        assert action == ACTION_RIGHT, "Should move when peak beyond tolerance"

    def test_deterministic_behavior(self):
        """GreedyAgent makes deterministic decisions (AC4)."""
        agent1 = GreedyAgent()
        agent2 = GreedyAgent()

        obs = {
            'position': 0.0,
            'reward': 0.5,
            'gradient': np.array([0.3, 0.7, 0.5]),
            'gradient_positions': np.array([-1.0, 0.0, 1.0]),
            'timestep': 0
        }

        # Same observation should always produce same action
        actions1 = [agent1.get_action(obs) for _ in range(10)]
        actions2 = [agent2.get_action(obs) for _ in range(10)]

        assert actions1 == actions2, "Greedy must be deterministic"
        assert all(a == actions1[0] for a in actions1), "Same obs must give same action"

    def test_uses_only_local_gradient(self):
        """GreedyAgent uses only gradient information from observation (AC5)."""
        agent = GreedyAgent()

        # Different rewards and timesteps, same gradient pattern
        obs1 = {
            'position': 0.0,
            'reward': 0.1,  # Different reward
            'gradient': np.array([0.3, 0.5, 0.9]),
            'gradient_positions': np.array([-1.0, 0.0, 1.0]),
            'timestep': 0  # Different timestep
        }

        obs2 = {
            'position': 0.0,
            'reward': 0.9,  # Different reward
            'gradient': np.array([0.3, 0.5, 0.9]),  # Same gradient
            'gradient_positions': np.array([-1.0, 0.0, 1.0]),
            'timestep': 99  # Different timestep
        }

        action1 = agent.get_action(obs1)
        action2 = agent.get_action(obs2)

        assert action1 == action2, "Should only use gradient, ignore reward/timestep"
        assert action1 == ACTION_RIGHT, "Both should move right"

    def test_greedy_agent_has_docstring(self):
        """GreedyAgent has comprehensive docstring (AC6)."""
        assert GreedyAgent.__doc__ is not None, "GreedyAgent must have docstring"
        assert len(GreedyAgent.__doc__) > 100, "Docstring should be comprehensive"

        class_doc = GreedyAgent.__doc__.lower()
        assert 'greedy' in class_doc or 'gradient' in class_doc, "Should mention greedy/gradient"
        assert 'hill' in class_doc or 'climb' in class_doc, "Should mention hill-climbing"

        method_doc = GreedyAgent.get_action.__doc__
        assert method_doc is not None, "get_action must have docstring"
        assert 'gradient' in method_doc.lower(), "Should document gradient following"

    def test_stateless_agent(self):
        """GreedyAgent is stateless - no memory between calls (AC7)."""
        agent = GreedyAgent()

        # Sequence of different observations
        obs_left = {
            'position': 0.0,
            'gradient': np.array([0.9, 0.5, 0.3]),
            'gradient_positions': np.array([-1.0, 0.0, 1.0]),
            'reward': 0.5,
            'timestep': 0
        }

        obs_right = {
            'position': 0.0,
            'gradient': np.array([0.3, 0.5, 0.9]),
            'gradient_positions': np.array([-1.0, 0.0, 1.0]),
            'reward': 0.5,
            'timestep': 1
        }

        # Agent should respond to current observation only
        assert agent.get_action(obs_left) == ACTION_LEFT
        assert agent.get_action(obs_right) == ACTION_RIGHT
        assert agent.get_action(obs_left) == ACTION_LEFT  # No memory of previous obs_right

    def test_argmax_gradient_logic(self):
        """GreedyAgent correctly uses np.argmax on gradient array (AC2)."""
        agent = GreedyAgent()

        # Complex gradient with clear maximum
        obs = {
            'position': 0.0,
            'gradient': np.array([0.1, 0.3, 0.2, 0.8, 0.4, 0.6, 0.5]),
            'gradient_positions': np.array([-3.0, -2.0, -1.0, 0.5, 1.0, 2.0, 3.0]),
            'reward': 0.5,
            'timestep': 0
        }

        # Max is at index 3 (value 0.8, position 0.5)
        action = agent.get_action(obs)
        assert action == ACTION_RIGHT, "Should move right to position 0.5"

    def test_get_action_signature(self):
        """get_action has correct type hints."""
        sig = inspect.signature(GreedyAgent.get_action)

        assert 'observation' in sig.parameters
        assert sig.parameters['observation'].annotation == dict
        assert sig.return_annotation == int

    def test_greedy_outperforms_random_on_stationary_peak(self):
        """GreedyAgent significantly outperforms RandomAgent on stationary peak."""
        from funcbench import GaussianTranslation, Environment

        # Stationary peak at origin
        func = GaussianTranslation(mean_start=0.0, velocity=0.0, sigma=2.0, seed=42)
        env = Environment(func, episode_length=50, render_mode=False)

        # Test greedy agent
        greedy = GreedyAgent()
        obs = env.reset()
        greedy_rewards = []
        for _ in range(50):
            action = greedy.get_action(obs)
            obs, reward, done, info = env.step(action)
            greedy_rewards.append(reward)
            if done:
                break
        greedy_score = info['cumulative_reward']

        # Test random agent
        from funcbench import RandomAgent
        env2 = Environment(GaussianTranslation(mean_start=0.0, velocity=0.0, sigma=2.0, seed=42),
                          episode_length=50, render_mode=False)
        random = RandomAgent(seed=42)
        obs = env2.reset()
        for _ in range(50):
            action = random.get_action(obs)
            obs, reward, done, info = env2.step(action)
            if done:
                break
        random_score = info['cumulative_reward']

        # Greedy should significantly outperform random
        assert greedy_score > random_score, \
            f"Greedy ({greedy_score:.2f}) should beat random ({random_score:.2f})"

        # Greedy should achieve high percentage of perfect (>80% on stationary)
        perfect_score = info['perfect_score']
        greedy_percentage = greedy_score / perfect_score * 100
        assert greedy_percentage > 80, \
            f"Greedy should get >80% of perfect on stationary peak, got {greedy_percentage:.1f}%"
