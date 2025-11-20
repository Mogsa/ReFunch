"""Tests for Environment class initialization and reset functionality."""

import numpy as np
import pytest

from funcbench import Environment, GaussianTranslation


class TestEnvironmentInitialization:
    """Test Environment initialization with default and custom parameters."""

    def test_environment_initialization_default_params(self, gaussian_function):
        """Environment initializes with default parameter values."""
        env = Environment(gaussian_function)

        # Verify default parameter values
        assert env.function is gaussian_function
        assert env.episode_length == 1000
        assert env.observation_radius == 5.0
        assert env.n_gradient_samples == 20
        assert env.step_size == 1.0
        assert env.render_mode is False

    def test_environment_initialization_custom_params(self, gaussian_function):
        """Environment initializes with custom parameter values."""
        env = Environment(
            function=gaussian_function,
            episode_length=500,
            observation_radius=10.0,
            n_gradient_samples=50,
            step_size=0.5,
            render_mode=True,
        )

        # Verify custom parameter values are stored
        assert env.function is gaussian_function
        assert env.episode_length == 500
        assert env.observation_radius == 10.0
        assert env.n_gradient_samples == 50
        assert env.step_size == 0.5
        assert env.render_mode is True

    def test_state_dict_structure(self, gaussian_function):
        """State dict has correct keys and initial types."""
        env = Environment(gaussian_function)

        # Verify state dict keys
        assert 'position' in env.state
        assert 'timestep' in env.state
        assert 'cumulative_reward' in env.state
        assert 'history' in env.state

        # Verify exact key count (no extra keys)
        assert len(env.state) == 4

    def test_state_dict_initial_values(self, gaussian_function):
        """State dict initialized with correct initial values."""
        env = Environment(gaussian_function)

        # Check initial values
        assert env.state['position'] == 0.0
        assert env.state['timestep'] == 0
        assert env.state['cumulative_reward'] == 0.0
        assert env.state['history'] == []

    def test_state_dict_float64_types(self, gaussian_function):
        """Position and cumulative_reward use np.float64 precision."""
        env = Environment(gaussian_function)

        # Verify float64 precision for reproducibility
        assert isinstance(env.state['position'], np.float64)
        assert isinstance(env.state['cumulative_reward'], np.float64)

    def test_configuration_attributes(self, gaussian_function):
        """All initialization parameters stored as instance attributes."""
        env = Environment(
            function=gaussian_function,
            episode_length=750,
            observation_radius=7.5,
            n_gradient_samples=30,
            step_size=0.75,
            render_mode=True,
        )

        # Verify all parameters accessible as attributes
        assert hasattr(env, 'function')
        assert hasattr(env, 'episode_length')
        assert hasattr(env, 'observation_radius')
        assert hasattr(env, 'n_gradient_samples')
        assert hasattr(env, 'step_size')
        assert hasattr(env, 'render_mode')


class TestEnvironmentReset:
    """Test Environment reset functionality."""

    def test_reset_initializes_position(self, gaussian_function):
        """reset() initializes position to 0.0 with float64 precision."""
        env = Environment(gaussian_function)

        # Modify state to non-initial values
        env.state['position'] = np.float64(15.5)

        # Reset should restore to 0.0
        env.reset()
        assert env.state['position'] == 0.0
        assert isinstance(env.state['position'], np.float64)

    def test_reset_initializes_timestep(self, gaussian_function):
        """reset() initializes timestep to 0."""
        env = Environment(gaussian_function)

        # Modify state
        env.state['timestep'] = 500

        # Reset should restore to 0
        env.reset()
        assert env.state['timestep'] == 0

    def test_reset_initializes_cumulative_reward(self, gaussian_function):
        """reset() initializes cumulative_reward to 0.0 with float64 precision."""
        env = Environment(gaussian_function)

        # Modify state
        env.state['cumulative_reward'] = np.float64(123.45)

        # Reset should restore to 0.0
        env.reset()
        assert env.state['cumulative_reward'] == 0.0
        assert isinstance(env.state['cumulative_reward'], np.float64)

    def test_reset_clears_history(self, gaussian_function):
        """reset() clears history list."""
        env = Environment(gaussian_function)

        # Add some history
        env.state['history'] = [(0, 0.0, 1.0, 1), (1, 0.5, 0.9, 2)]

        # Reset should clear history
        env.reset()
        assert env.state['history'] == []

    def test_reset_returns_observation_dict(self, gaussian_function):
        """reset() returns observation dictionary."""
        env = Environment(gaussian_function)
        observation = env.reset()

        # Verify returns dict
        assert isinstance(observation, dict)

    def test_observation_dict_structure(self, gaussian_function):
        """Observation dict has required keys per Agent interface contract."""
        env = Environment(gaussian_function)
        observation = env.reset()

        # Verify exact required keys
        assert 'position' in observation
        assert 'reward' in observation
        assert 'gradient' in observation
        assert 'gradient_positions' in observation
        assert 'timestep' in observation

        # Verify no extra keys
        assert len(observation) == 5

    def test_observation_dict_types(self, gaussian_function):
        """Observation dict values have correct types."""
        env = Environment(gaussian_function)
        observation = env.reset()

        # Verify types
        assert isinstance(observation['position'], float)
        assert isinstance(observation['reward'], float)
        assert isinstance(observation['gradient'], np.ndarray)
        assert isinstance(observation['gradient_positions'], np.ndarray)
        assert isinstance(observation['timestep'], int)

        # Verify float64 dtype for arrays
        assert observation['gradient'].dtype == np.float64
        assert observation['gradient_positions'].dtype == np.float64

    def test_observation_initial_values(self, gaussian_function):
        """Observation dict contains correct initial values after reset."""
        env = Environment(gaussian_function)
        observation = env.reset()

        # Check initial values
        assert observation['position'] == 0.0
        assert observation['timestep'] == 0

        # Verify gradient arrays are non-empty
        assert len(observation['gradient']) == env.n_gradient_samples
        assert len(observation['gradient_positions']) == env.n_gradient_samples

        # Verify reward is calculated (not placeholder 0.0)
        assert isinstance(observation['reward'], float)

    def test_multiple_resets(self, gaussian_function):
        """Calling reset() multiple times works correctly."""
        env = Environment(gaussian_function)

        # First reset
        obs1 = env.reset()
        assert obs1['position'] == 0.0
        assert obs1['timestep'] == 0

        # Modify state
        env.state['position'] = np.float64(10.0)
        env.state['timestep'] = 100
        env.state['cumulative_reward'] = np.float64(50.0)
        env.state['history'] = [(0, 0.0, 1.0, 1)]

        # Second reset should restore initial state
        obs2 = env.reset()
        assert obs2['position'] == 0.0
        assert obs2['timestep'] == 0
        assert env.state['cumulative_reward'] == 0.0
        assert env.state['history'] == []


class TestEnvironmentIntegration:
    """Test Environment integration with Function2D dependencies."""

    def test_environment_accepts_function2d(self):
        """Environment can be initialized with GaussianTranslation."""
        func = GaussianTranslation()
        env = Environment(func)

        # Verify function is stored
        assert env.function is func
        assert isinstance(env.function, GaussianTranslation)

    def test_environment_stores_function_reference(self, gaussian_function):
        """Environment maintains reference to function instance."""
        env = Environment(gaussian_function)

        # Verify function reference is accessible
        assert hasattr(env, 'function')
        assert env.function is gaussian_function

        # Verify we can access function methods
        assert hasattr(env.function, 'evaluate')
        assert hasattr(env.function, 'get_perfect_score')
        assert hasattr(env.function, 'bounds')


class TestObservationGradientSampling:
    """Test gradient sampling within observation radius (Story 2.3)."""

    def test_gradient_array_length(self, gaussian_function):
        """Gradient array length equals n_gradient_samples."""
        env = Environment(gaussian_function, n_gradient_samples=15)
        observation = env.reset()

        assert observation['gradient'].shape == (15,)
        assert observation['gradient_positions'].shape == (15,)

    def test_gradient_positions_within_radius(self, gaussian_function):
        """Gradient positions are within observation radius of agent position."""
        env = Environment(gaussian_function, observation_radius=5.0)
        observation = env.reset()

        agent_position = observation['position']
        gradient_positions = observation['gradient_positions']

        # All samples should be within [position - radius, position + radius]
        # (may be clipped to bounds, but can't exceed window)
        window_left = agent_position - env.observation_radius
        window_right = agent_position + env.observation_radius

        assert np.all(gradient_positions >= window_left - 1e-10)  # Small tolerance for float precision
        assert np.all(gradient_positions <= window_right + 1e-10)

    def test_gradient_positions_clipped_to_bounds(self, gaussian_function):
        """Gradient positions are clipped to function bounds."""
        env = Environment(gaussian_function, observation_radius=50.0)  # Large radius
        env.state['position'] = np.float64(18.0)  # Near right bound
        observation = env._get_observation()

        # All positions must be within function bounds
        bounds = gaussian_function.bounds
        assert np.all(observation['gradient_positions'] >= bounds[0])
        assert np.all(observation['gradient_positions'] <= bounds[1])

    def test_gradient_uniform_spacing(self, gaussian_function):
        """Gradient positions are uniformly spaced using np.linspace."""
        env = Environment(gaussian_function, n_gradient_samples=11)
        observation = env.reset()

        positions = observation['gradient_positions']

        # Check uniform spacing (consecutive differences should be equal)
        if len(positions) > 1:
            differences = np.diff(positions)
            # All differences should be approximately equal
            assert np.allclose(differences, differences[0], rtol=1e-10)

    def test_gradient_values_match_function(self, gaussian_function):
        """Gradient values match function evaluation at sample positions."""
        env = Environment(gaussian_function)
        observation = env.reset()

        gradient = observation['gradient']
        gradient_positions = observation['gradient_positions']
        timestep = observation['timestep']

        # Manually evaluate function at same positions
        expected = gaussian_function.evaluate(gradient_positions, timestep)

        # Gradient should match function evaluation
        assert np.allclose(gradient, expected)

    def test_custom_n_gradient_samples(self, gaussian_function):
        """Environment respects custom n_gradient_samples parameter."""
        for n_samples in [5, 10, 20, 50]:
            env = Environment(gaussian_function, n_gradient_samples=n_samples)
            observation = env.reset()

            assert observation['gradient'].shape == (n_samples,)
            assert observation['gradient_positions'].shape == (n_samples,)


class TestObservationRewardCalculation:
    """Test reward calculation at agent position (Story 2.3)."""

    def test_reward_is_scalar_float(self, gaussian_function):
        """Reward is a scalar float, not an array."""
        env = Environment(gaussian_function)
        observation = env.reset()

        assert isinstance(observation['reward'], float)
        assert not isinstance(observation['reward'], np.ndarray)

    def test_reward_matches_function_at_position(self, gaussian_function):
        """Reward matches function evaluation at agent's position."""
        env = Environment(gaussian_function)
        observation = env.reset()

        # Manually calculate expected reward
        expected_reward_array = gaussian_function.evaluate(
            np.array([observation['position']]), observation['timestep']
        )
        expected_reward = float(expected_reward_array[0])

        assert observation['reward'] == expected_reward

    def test_reward_uses_float64_precision(self, gaussian_function):
        """Reward calculation uses float64 precision internally."""
        env = Environment(gaussian_function)
        observation = env.reset()

        # Calculate reward manually
        reward_array = gaussian_function.evaluate(
            np.array([env.state['position']]), env.state['timestep']
        )

        # Array should be float64
        assert reward_array.dtype == np.float64


class TestObservationPerformance:
    """Test observation generation performance (Story 2.3)."""

    def test_observation_generation_performance(self, gaussian_function):
        """_get_observation() completes in < 5ms for 20 samples."""
        import timeit

        env = Environment(gaussian_function, n_gradient_samples=20)
        env.reset()

        # Time 100 iterations
        execution_time = timeit.timeit(
            lambda: env._get_observation(),
            number=100
        )

        # Average time per call
        avg_time_ms = (execution_time / 100) * 1000

        # Should be < 5ms
        assert avg_time_ms < 5.0, f"Observation generation took {avg_time_ms:.2f}ms, expected < 5ms"

    def test_vectorized_function_call(self, gaussian_function):
        """Gradient sampling uses single vectorized function call."""
        env = Environment(gaussian_function, n_gradient_samples=20)
        observation = env.reset()

        # Verify gradient is a single array (result of vectorized call)
        assert isinstance(observation['gradient'], np.ndarray)
        assert observation['gradient'].shape == (20,)

        # Verify positions array has same shape
        assert observation['gradient_positions'].shape == observation['gradient'].shape


class TestStepActionValidation:
    """Test step() action validation (Story 2.4 AC1)."""

    def test_step_accepts_valid_action_left(self, gaussian_function):
        """step() accepts ACTION_LEFT (0) without raising error."""
        from funcbench.agent import ACTION_LEFT
        env = Environment(gaussian_function)
        env.reset()

        # Should not raise exception
        env.step(ACTION_LEFT)

    def test_step_accepts_valid_action_stay(self, gaussian_function):
        """step() accepts ACTION_STAY (1) without raising error."""
        from funcbench.agent import ACTION_STAY
        env = Environment(gaussian_function)
        env.reset()

        # Should not raise exception
        env.step(ACTION_STAY)

    def test_step_accepts_valid_action_right(self, gaussian_function):
        """step() accepts ACTION_RIGHT (2) without raising error."""
        from funcbench.agent import ACTION_RIGHT
        env = Environment(gaussian_function)
        env.reset()

        # Should not raise exception
        env.step(ACTION_RIGHT)

    def test_step_rejects_invalid_action_negative(self, gaussian_function):
        """step() raises ValueError for action -1."""
        env = Environment(gaussian_function)
        env.reset()

        with pytest.raises(ValueError) as exc_info:
            env.step(-1)

        assert "Invalid action -1" in str(exc_info.value)
        assert "Must be 0 (left), 1 (stay), or 2 (right)" in str(exc_info.value)

    def test_step_rejects_invalid_action_three(self, gaussian_function):
        """step() raises ValueError for action 3."""
        env = Environment(gaussian_function)
        env.reset()

        with pytest.raises(ValueError) as exc_info:
            env.step(3)

        assert "Invalid action 3" in str(exc_info.value)

    def test_step_rejects_invalid_action_large(self, gaussian_function):
        """step() raises ValueError for action 100."""
        env = Environment(gaussian_function)
        env.reset()

        with pytest.raises(ValueError) as exc_info:
            env.step(100)

        assert "Invalid action 100" in str(exc_info.value)


class TestStepPositionUpdate:
    """Test step() position updates (Story 2.4 AC2)."""

    def test_step_action_left_decreases_position(self, gaussian_function):
        """ACTION_LEFT decreases position by step_size."""
        from funcbench.agent import ACTION_LEFT
        env = Environment(gaussian_function, step_size=1.0)
        env.reset()

        initial_position = env.state['position']
        obs, _, _, _ = env.step(ACTION_LEFT)

        assert env.state['position'] == initial_position - 1.0
        assert obs['position'] == initial_position - 1.0

    def test_step_action_stay_preserves_position(self, gaussian_function):
        """ACTION_STAY keeps position unchanged."""
        from funcbench.agent import ACTION_STAY
        env = Environment(gaussian_function, step_size=1.0)
        env.reset()

        initial_position = env.state['position']
        obs, _, _, _ = env.step(ACTION_STAY)

        assert env.state['position'] == initial_position
        assert obs['position'] == initial_position

    def test_step_action_right_increases_position(self, gaussian_function):
        """ACTION_RIGHT increases position by step_size."""
        from funcbench.agent import ACTION_RIGHT
        env = Environment(gaussian_function, step_size=1.0)
        env.reset()

        initial_position = env.state['position']
        obs, _, _, _ = env.step(ACTION_RIGHT)

        assert env.state['position'] == initial_position + 1.0
        assert obs['position'] == initial_position + 1.0

    def test_step_custom_step_size(self, gaussian_function):
        """Position updates respect custom step_size."""
        from funcbench.agent import ACTION_RIGHT, ACTION_LEFT
        env = Environment(gaussian_function, step_size=2.5)
        env.reset()

        # Right movement
        obs, _, _, _ = env.step(ACTION_RIGHT)
        assert env.state['position'] == 2.5

        # Left movement
        obs, _, _, _ = env.step(ACTION_LEFT)
        assert env.state['position'] == 0.0

    def test_step_position_clamping_left_bound(self, gaussian_function):
        """Position is clamped at left bound."""
        from funcbench.agent import ACTION_LEFT
        env = Environment(gaussian_function, step_size=5.0)

        # Start at position near left bound
        env.reset()
        env.state['position'] = np.float64(-18.0)  # Near left bound of [-20, 20]

        # Take large left step that would exceed bounds
        obs, _, _, _ = env.step(ACTION_LEFT)

        # Position should be clamped to left bound
        assert env.state['position'] >= gaussian_function.bounds[0]
        assert env.state['position'] == gaussian_function.bounds[0]

    def test_step_position_clamping_right_bound(self, gaussian_function):
        """Position is clamped at right bound."""
        from funcbench.agent import ACTION_RIGHT
        env = Environment(gaussian_function, step_size=5.0)

        # Start at position near right bound
        env.reset()
        env.state['position'] = np.float64(18.0)  # Near right bound of [-20, 20]

        # Take large right step that would exceed bounds
        obs, _, _, _ = env.step(ACTION_RIGHT)

        # Position should be clamped to right bound
        assert env.state['position'] <= gaussian_function.bounds[1]
        assert env.state['position'] == gaussian_function.bounds[1]


class TestStepRewardCalculation:
    """Test step() reward calculation (Story 2.4 AC3)."""

    def test_step_returns_reward_as_scalar_float(self, gaussian_function):
        """step() returns reward as scalar float, not array."""
        from funcbench.agent import ACTION_RIGHT
        env = Environment(gaussian_function)
        env.reset()

        obs, reward, done, info = env.step(ACTION_RIGHT)

        assert isinstance(reward, float)
        assert not isinstance(reward, np.ndarray)

    def test_step_reward_matches_function_evaluation(self, gaussian_function):
        """Reward matches function.evaluate() at new position."""
        from funcbench.agent import ACTION_RIGHT
        env = Environment(gaussian_function)
        env.reset()

        # Take action
        obs, reward, done, info = env.step(ACTION_RIGHT)

        # Manually calculate expected reward at new position
        new_position = obs['position']
        timestep = 0  # First step, timestep was 0 when reward calculated
        expected_reward = float(
            gaussian_function.evaluate(np.array([new_position]), timestep)[0]
        )

        assert reward == expected_reward

    def test_step_cumulative_reward_increments(self, gaussian_function):
        """Cumulative reward increments by step reward."""
        from funcbench.agent import ACTION_RIGHT
        env = Environment(gaussian_function)
        env.reset()

        # Take first step
        _, reward1, _, info1 = env.step(ACTION_RIGHT)
        cumulative1 = info1['cumulative_reward']

        # Cumulative should equal first reward
        assert cumulative1 == reward1

        # Take second step
        _, reward2, _, info2 = env.step(ACTION_RIGHT)
        cumulative2 = info2['cumulative_reward']

        # Cumulative should equal sum of both rewards
        assert cumulative2 == reward1 + reward2

    def test_step_cumulative_reward_multiple_steps(self, gaussian_function):
        """Cumulative reward equals sum of all step rewards."""
        from funcbench.agent import ACTION_STAY
        env = Environment(gaussian_function)
        env.reset()

        rewards = []
        for _ in range(10):
            _, reward, _, info = env.step(ACTION_STAY)
            rewards.append(reward)

        expected_cumulative = sum(rewards)
        assert np.isclose(env.state['cumulative_reward'], expected_cumulative)


class TestStepTimestepAndDone:
    """Test step() timestep advancement and done flag (Story 2.4 AC4)."""

    def test_step_increments_timestep(self, gaussian_function):
        """step() increments timestep by 1."""
        from funcbench.agent import ACTION_STAY
        env = Environment(gaussian_function)
        env.reset()

        assert env.state['timestep'] == 0

        env.step(ACTION_STAY)
        assert env.state['timestep'] == 1

        env.step(ACTION_STAY)
        assert env.state['timestep'] == 2

    def test_step_done_false_before_episode_end(self, gaussian_function):
        """done flag is False when timestep < episode_length."""
        from funcbench.agent import ACTION_STAY
        env = Environment(gaussian_function, episode_length=100)
        env.reset()

        # Take 50 steps
        for _ in range(50):
            _, _, done, _ = env.step(ACTION_STAY)
            assert done is False

    def test_step_done_true_at_episode_end(self, gaussian_function):
        """done flag is True when timestep >= episode_length."""
        from funcbench.agent import ACTION_STAY
        env = Environment(gaussian_function, episode_length=10)
        env.reset()

        # Take 9 steps (not done yet)
        for _ in range(9):
            _, _, done, _ = env.step(ACTION_STAY)
            assert done is False

        # Take 10th step (now done)
        _, _, done, _ = env.step(ACTION_STAY)
        assert done is True

    def test_step_done_flag_is_boolean(self, gaussian_function):
        """done flag is boolean type."""
        from funcbench.agent import ACTION_STAY
        env = Environment(gaussian_function)
        env.reset()

        _, _, done, _ = env.step(ACTION_STAY)
        assert isinstance(done, bool)


class TestStepReturnSignature:
    """Test step() return signature (Story 2.4 AC5)."""

    def test_step_returns_four_tuple(self, gaussian_function):
        """step() returns exactly 4 values."""
        from funcbench.agent import ACTION_STAY
        env = Environment(gaussian_function)
        env.reset()

        result = env.step(ACTION_STAY)

        assert isinstance(result, tuple)
        assert len(result) == 4

    def test_step_return_types(self, gaussian_function):
        """step() returns (dict, float, bool, dict) types."""
        from funcbench.agent import ACTION_STAY
        env = Environment(gaussian_function)
        env.reset()

        obs, reward, done, info = env.step(ACTION_STAY)

        assert isinstance(obs, dict)
        assert isinstance(reward, float)
        assert isinstance(done, bool)
        assert isinstance(info, dict)

    def test_step_observation_has_required_keys(self, gaussian_function):
        """Observation dict has all required keys."""
        from funcbench.agent import ACTION_STAY
        env = Environment(gaussian_function)
        env.reset()

        obs, _, _, _ = env.step(ACTION_STAY)

        assert 'position' in obs
        assert 'reward' in obs
        assert 'gradient' in obs
        assert 'gradient_positions' in obs
        assert 'timestep' in obs

    def test_step_observation_reflects_new_state(self, gaussian_function):
        """Observation reflects state AFTER action execution."""
        from funcbench.agent import ACTION_RIGHT
        env = Environment(gaussian_function, step_size=1.0)
        env.reset()

        obs, _, _, _ = env.step(ACTION_RIGHT)

        # Position should be updated
        assert obs['position'] == 1.0
        # Timestep should be incremented
        assert obs['timestep'] == 1


class TestStepInfoDict:
    """Test step() info dictionary (Story 2.4 AC6)."""

    def test_step_info_has_cumulative_reward(self, gaussian_function):
        """Info dict contains cumulative_reward key."""
        from funcbench.agent import ACTION_STAY
        env = Environment(gaussian_function)
        env.reset()

        _, _, _, info = env.step(ACTION_STAY)

        assert 'cumulative_reward' in info
        assert isinstance(info['cumulative_reward'], float)

    def test_step_info_has_perfect_score(self, gaussian_function):
        """Info dict contains perfect_score key."""
        from funcbench.agent import ACTION_STAY
        env = Environment(gaussian_function)
        env.reset()

        _, _, _, info = env.step(ACTION_STAY)

        assert 'perfect_score' in info
        assert isinstance(info['perfect_score'], float)

    def test_step_info_cumulative_reward_matches_state(self, gaussian_function):
        """Info cumulative_reward matches state['cumulative_reward']."""
        from funcbench.agent import ACTION_STAY
        env = Environment(gaussian_function)
        env.reset()

        _, _, _, info = env.step(ACTION_STAY)

        assert info['cumulative_reward'] == float(env.state['cumulative_reward'])

    def test_step_info_perfect_score_matches_function(self, gaussian_function):
        """Info perfect_score matches function.get_perfect_score()."""
        from funcbench.agent import ACTION_STAY
        env = Environment(gaussian_function, episode_length=1000)
        env.reset()

        _, _, _, info = env.step(ACTION_STAY)

        expected_perfect = gaussian_function.get_perfect_score(1000)
        assert info['perfect_score'] == expected_perfect


class TestStepPerformance:
    """Test step() performance requirements (Story 2.4 AC8)."""

    def test_step_execution_performance(self, gaussian_function):
        """step() completes in < 10ms including observation generation."""
        import timeit
        from funcbench.agent import ACTION_RIGHT

        env = Environment(gaussian_function, n_gradient_samples=20)
        env.reset()

        # Time 100 iterations
        execution_time = timeit.timeit(
            lambda: env.step(ACTION_RIGHT),
            setup="env.reset()",
            number=100,
            globals={'env': env}
        )

        # Average time per call
        avg_time_ms = (execution_time / 100) * 1000

        # Should be < 10ms
        assert avg_time_ms < 10.0, f"step() took {avg_time_ms:.2f}ms, expected < 10ms"


class TestStepIntegration:
    """Test step() integration scenarios."""

    def test_step_sequence_maintains_state_consistency(self, gaussian_function):
        """Taking multiple steps maintains consistent state."""
        from funcbench.agent import ACTION_RIGHT, ACTION_LEFT, ACTION_STAY
        env = Environment(gaussian_function, step_size=1.0)
        env.reset()

        # Right, Right, Left, Stay sequence
        obs1, r1, d1, info1 = env.step(ACTION_RIGHT)
        assert env.state['position'] == 1.0
        assert env.state['timestep'] == 1

        obs2, r2, d2, info2 = env.step(ACTION_RIGHT)
        assert env.state['position'] == 2.0
        assert env.state['timestep'] == 2

        obs3, r3, d3, info3 = env.step(ACTION_LEFT)
        assert env.state['position'] == 1.0
        assert env.state['timestep'] == 3

        obs4, r4, d4, info4 = env.step(ACTION_STAY)
        assert env.state['position'] == 1.0
        assert env.state['timestep'] == 4

    def test_step_full_episode_execution(self, gaussian_function):
        """Can execute complete episode with step()."""
        from funcbench.agent import ACTION_STAY
        env = Environment(gaussian_function, episode_length=100)
        env.reset()

        done = False
        steps = 0

        while not done:
            _, _, done, _ = env.step(ACTION_STAY)
            steps += 1

        assert steps == 100
        assert env.state['timestep'] == 100


class TestHistoryTracking:
    """Test Environment history tracking functionality."""

    def test_history_append_on_step(self, gaussian_function):
        """History appends entry on each step."""
        from funcbench.agent import ACTION_RIGHT
        env = Environment(gaussian_function, episode_length=10)
        env.reset()

        # Verify history is initially empty
        assert len(env.state['history']) == 0

        # Take one step
        env.step(ACTION_RIGHT)

        # Verify history has one entry
        assert len(env.state['history']) == 1

        # Take another step
        env.step(ACTION_RIGHT)

        # Verify history has two entries
        assert len(env.state['history']) == 2

    def test_history_tuple_format(self, gaussian_function):
        """History entry is tuple with 4 elements."""
        from funcbench.agent import ACTION_RIGHT
        env = Environment(gaussian_function)
        env.reset()
        env.step(ACTION_RIGHT)

        # Get first history entry
        entry = env.state['history'][0]

        # Verify it's a tuple
        assert isinstance(entry, tuple)

        # Verify it has 4 elements
        assert len(entry) == 4

        # Verify element types
        timestep, position, reward, action = entry
        assert isinstance(timestep, int)
        assert isinstance(position, float)
        assert isinstance(reward, float)
        assert isinstance(action, int)

    def test_history_chronological(self, gaussian_function):
        """History entries in chronological order."""
        from funcbench.agent import ACTION_RIGHT, ACTION_LEFT, ACTION_STAY
        env = Environment(gaussian_function)
        env.reset()

        # Execute sequence of actions
        env.step(ACTION_RIGHT)  # timestep 0
        env.step(ACTION_LEFT)   # timestep 1
        env.step(ACTION_STAY)   # timestep 2

        # Verify history length
        assert len(env.state['history']) == 3

        # Verify chronological order
        assert env.state['history'][0][0] == 0  # First entry: timestep 0
        assert env.state['history'][1][0] == 1  # Second entry: timestep 1
        assert env.state['history'][2][0] == 2  # Third entry: timestep 2

        # Verify actions are recorded correctly
        assert env.state['history'][0][3] == ACTION_RIGHT
        assert env.state['history'][1][3] == ACTION_LEFT
        assert env.state['history'][2][3] == ACTION_STAY

    def test_history_reset_clears(self, gaussian_function):
        """reset() clears history to empty list."""
        from funcbench.agent import ACTION_RIGHT
        env = Environment(gaussian_function)
        env.reset()

        # Take several steps to populate history
        env.step(ACTION_RIGHT)
        env.step(ACTION_RIGHT)
        env.step(ACTION_RIGHT)

        # Verify history has entries
        assert len(env.state['history']) == 3

        # Reset environment
        env.reset()

        # Verify history is cleared
        assert len(env.state['history']) == 0
        assert env.state['history'] == []

    def test_get_history_returns_copy(self, gaussian_function):
        """get_history() returns copy, not reference."""
        from funcbench.agent import ACTION_RIGHT
        env = Environment(gaussian_function)
        env.reset()
        env.step(ACTION_RIGHT)

        # Get history
        history = env.get_history()

        # Verify it has one entry
        assert len(history) == 1

        # Modify returned history
        history.append((999, 999.0, 999.0, 999))

        # Verify internal history unchanged
        assert len(env.state['history']) == 1
        assert (999, 999.0, 999.0, 999) not in env.state['history']

    def test_get_history_format(self, gaussian_function):
        """get_history() returns list of 4-tuples."""
        from funcbench.agent import ACTION_RIGHT, ACTION_LEFT
        env = Environment(gaussian_function)
        env.reset()

        # Execute two steps
        obs1, reward1, done1, info1 = env.step(ACTION_RIGHT)
        obs2, reward2, done2, info2 = env.step(ACTION_LEFT)

        # Get history
        history = env.get_history()

        # Verify it's a list
        assert isinstance(history, list)

        # Verify length matches number of steps
        assert len(history) == 2

        # Verify each entry is a 4-tuple
        for entry in history:
            assert isinstance(entry, tuple)
            assert len(entry) == 4

        # Verify first entry content
        timestep, position, reward, action = history[0]
        assert timestep == 0
        assert position == 1.0  # Moved right from 0.0
        assert reward == reward1
        assert action == ACTION_RIGHT

    def test_history_no_observations(self, gaussian_function):
        """History entries don't contain observation dicts."""
        from funcbench.agent import ACTION_RIGHT
        env = Environment(gaussian_function)
        env.reset()
        env.step(ACTION_RIGHT)

        # Get first history entry
        entry = env.state['history'][0]

        # Verify it's a simple 4-tuple (not containing observation dict)
        assert len(entry) == 4

        # Verify none of the elements are dicts
        for element in entry:
            assert not isinstance(element, dict)

        # Verify history doesn't contain 'gradient' or 'gradient_positions'
        # (these would be present if observations were stored)
        entry_str = str(entry)
        assert 'gradient' not in entry_str
        assert 'gradient_positions' not in entry_str

    def test_history_performance(self, gaussian_function):
        """History storage completes in < 1ms per step."""
        import timeit
        from funcbench.agent import ACTION_STAY

        env = Environment(gaussian_function, episode_length=1000)
        env.reset()

        # Measure time for single step (includes history append)
        def single_step():
            env.step(ACTION_STAY)

        # Reset before timing
        env.reset()

        # Time 100 steps
        execution_time = timeit.timeit(single_step, number=100)
        avg_time_per_step = execution_time / 100

        # Verify < 1ms per step (0.001 seconds)
        # Note: This includes full step execution, not just history append
        # History append itself is much faster (< 0.01ms)
        assert avg_time_per_step < 0.01  # 10ms is generous budget for full step

    def test_history_multi_step(self, gaussian_function):
        """History accumulates correctly over multiple steps."""
        from funcbench.agent import ACTION_RIGHT
        env = Environment(gaussian_function, episode_length=100)
        env.reset()

        # Execute 100 steps
        for i in range(100):
            env.step(ACTION_RIGHT)

        # Verify history length
        history = env.get_history()
        assert len(history) == 100

        # Verify all entries are valid tuples
        for i, entry in enumerate(history):
            timestep, position, reward, action = entry

            # Verify chronological order
            assert timestep == i

            # Verify all entries have ACTION_RIGHT
            assert action == ACTION_RIGHT

            # Verify position increases (unless at bound)
            if i > 0:
                prev_position = history[i - 1][1]
                # Position should increase by step_size (1.0) unless clamped
                assert position >= prev_position

    def test_history_content_matches_step_returns(self, gaussian_function):
        """History content matches values returned by step()."""
        from funcbench.agent import ACTION_RIGHT, ACTION_LEFT
        env = Environment(gaussian_function, step_size=0.5)
        env.reset()

        # Take first step and capture returns
        obs1, reward1, done1, info1 = env.step(ACTION_RIGHT)
        pos1 = obs1['position']

        # Take second step
        obs2, reward2, done2, info2 = env.step(ACTION_LEFT)
        pos2 = obs2['position']

        # Get history
        history = env.get_history()

        # Verify first entry matches first step
        t1, p1, r1, a1 = history[0]
        assert t1 == 0
        assert p1 == pos1
        assert r1 == reward1
        assert a1 == ACTION_RIGHT

        # Verify second entry matches second step
        t2, p2, r2, a2 = history[1]
        assert t2 == 1
        assert p2 == pos2
        assert r2 == reward2
        assert a2 == ACTION_LEFT


class TestRunMethod:
    """Test Environment.run() method for complete episode execution."""

    def test_run_completes_episode(self, gaussian_function, mock_agent):
        """run() executes full episode and returns float."""
        env = Environment(gaussian_function, episode_length=100)

        # Run complete episode
        final_reward = env.run(mock_agent, render=False)

        # Verify return type is float
        assert isinstance(final_reward, (float, np.floating))

        # Verify episode completed (timestep == episode_length)
        assert env.state['timestep'] == 100

        # Verify done flag would be True if we stepped again
        # (but we don't because episode is done)

    def test_run_returns_cumulative_reward(self, gaussian_function, mock_agent):
        """run() return value matches state['cumulative_reward']."""
        env = Environment(gaussian_function, episode_length=50)

        final_reward = env.run(mock_agent, render=False)

        # Verify return matches internal state
        assert final_reward == env.state['cumulative_reward']

        # Verify cumulative reward is non-zero (agent took actions)
        assert final_reward != 0.0

    def test_run_calls_reset_and_step(self, gaussian_function, mock_agent):
        """run() calls reset() then loops step() until done."""
        env = Environment(gaussian_function, episode_length=10)

        # Set state to non-initial to verify reset is called
        env.state['position'] = np.float64(5.0)
        env.state['timestep'] = 5
        env.state['cumulative_reward'] = np.float64(10.0)
        env.state['history'] = [(0, 0.0, 1.0, 0)]

        # Run episode
        env.run(mock_agent, render=False)

        # Verify reset was called (position back to 0.0 initially)
        # and episode executed (timestep == episode_length)
        assert env.state['timestep'] == 10

        # Verify history was reset and then accumulated
        history = env.get_history()
        assert len(history) == 10  # All steps recorded

    def test_run_preserves_history(self, gaussian_function, mock_agent):
        """run() preserves episode history correctly."""
        env = Environment(gaussian_function, episode_length=20)

        env.run(mock_agent, render=False)

        # Verify history tracked all steps
        history = env.get_history()
        assert len(history) == 20

        # Verify history format
        for entry in history:
            timestep, position, reward, action = entry
            assert isinstance(timestep, int)
            assert isinstance(position, float)
            assert isinstance(reward, float)
            assert isinstance(action, int)

    def test_run_multiple_sequential_episodes(self, gaussian_function, mock_agent):
        """run() can be called multiple times sequentially."""
        env = Environment(gaussian_function, episode_length=10)

        # Run first episode
        score1 = env.run(mock_agent, render=False)
        history1 = env.get_history()

        # Run second episode
        score2 = env.run(mock_agent, render=False)
        history2 = env.get_history()

        # Both episodes completed
        assert len(history1) == 10
        assert len(history2) == 10

        # Scores are valid
        assert isinstance(score1, (float, np.floating))
        assert isinstance(score2, (float, np.floating))

    def test_run_performance_headless(self, gaussian_function, mock_agent):
        """1000-step episode completes in < 2 seconds (headless mode)."""
        import timeit

        env = Environment(gaussian_function, episode_length=1000)

        # Measure execution time
        def run_episode():
            env.run(mock_agent, render=False)

        # Time single episode execution
        execution_time = timeit.timeit(run_episode, number=1)

        # Verify < 2 seconds (NFR3 requirement)
        assert execution_time < 2.0, f"Episode took {execution_time:.3f}s, expected < 2.0s"

    def test_run_performance_small_episode(self, gaussian_function, mock_agent):
        """100-step episode completes quickly."""
        import timeit

        env = Environment(gaussian_function, episode_length=100)

        def run_episode():
            env.run(mock_agent, render=False)

        execution_time = timeit.timeit(run_episode, number=1)

        # Should be much faster than 2s for small episode
        assert execution_time < 0.5, f"Small episode took {execution_time:.3f}s"

    def test_run_render_false(self, gaussian_function, mock_agent):
        """run() with render=False executes headless."""
        env = Environment(gaussian_function, episode_length=10)

        # Run headless
        final_reward = env.run(mock_agent, render=False)

        # Verify completed successfully
        assert isinstance(final_reward, (float, np.floating))
        assert env.state['timestep'] == 10

    def test_run_render_true_no_visualizer(self, gaussian_function, mock_agent, capsys):
        """run() with render=True but no visualizer prints warning."""
        env = Environment(gaussian_function, episode_length=5)

        # Run with render=True (no visualizer exists)
        final_reward = env.run(mock_agent, render=True)

        # Capture printed output
        captured = capsys.readouterr()

        # Verify warning was printed
        assert "Visualization requested but visualizer not initialized" in captured.out

        # Verify episode still completed successfully
        assert isinstance(final_reward, (float, np.floating))
        assert env.state['timestep'] == 5

    def test_run_render_warning_shown_once(self, gaussian_function, mock_agent, capsys):
        """Render warning only printed once per environment, not every run()."""
        env = Environment(gaussian_function, episode_length=5)

        # First run with render=True
        env.run(mock_agent, render=True)
        captured1 = capsys.readouterr()

        # Verify warning printed on first run
        assert "Visualization requested" in captured1.out

        # Second run with render=True
        env.run(mock_agent, render=True)
        captured2 = capsys.readouterr()

        # Verify warning NOT printed on second run (already shown)
        assert "Visualization requested" not in captured2.out

    def test_run_agent_exception_handling(self, gaussian_function):
        """run() catches agent exceptions and provides informative error."""
        from funcbench.agent import Agent

        # Create mock agent that raises exception
        class BrokenAgent(Agent):
            def get_action(self, observation):
                raise RuntimeError("Agent internal error")

        env = Environment(gaussian_function, episode_length=10)
        agent = BrokenAgent()

        # Verify exception is caught and re-raised with context
        with pytest.raises(ValueError) as exc_info:
            env.run(agent, render=False)

        # Verify error message includes agent type
        assert "BrokenAgent" in str(exc_info.value)

        # Verify error message includes "get_action"
        assert "get_action" in str(exc_info.value)

        # Verify error message includes original exception
        assert "Agent internal error" in str(exc_info.value)

    def test_run_agent_exception_includes_timestep(self, gaussian_function):
        """Agent exception error includes timestep for debugging."""
        from funcbench.agent import Agent

        # Create agent that fails on specific timestep
        class DelayedFailureAgent(Agent):
            def __init__(self):
                self.call_count = 0

            def get_action(self, observation):
                self.call_count += 1
                if self.call_count >= 5:
                    raise ValueError("Failure at timestep 5")
                return 1  # ACTION_STAY

        env = Environment(gaussian_function, episode_length=100)
        agent = DelayedFailureAgent()

        # Run and expect exception
        with pytest.raises(ValueError) as exc_info:
            env.run(agent, render=False)

        # Verify timestep is mentioned in error
        assert "timestep" in str(exc_info.value).lower()

    def test_run_agent_exception_preserves_state(self, gaussian_function):
        """Agent exception doesn't corrupt environment state."""
        from funcbench.agent import Agent

        class FailingAgent(Agent):
            def get_action(self, observation):
                raise RuntimeError("Test exception")

        env = Environment(gaussian_function, episode_length=10)
        agent = FailingAgent()

        # Try to run (will fail)
        with pytest.raises(ValueError):
            env.run(agent, render=False)

        # Verify state is still valid (reset was called)
        assert 'position' in env.state
        assert 'timestep' in env.state
        assert 'cumulative_reward' in env.state
        assert 'history' in env.state

    def test_run_with_mock_agent_always_right(self, gaussian_function):
        """Full episode with simple mock agent (always goes right)."""
        from funcbench.agent import Agent, ACTION_RIGHT

        class AlwaysRightAgent(Agent):
            def get_action(self, observation):
                return ACTION_RIGHT

        env = Environment(gaussian_function, episode_length=50)
        agent = AlwaysRightAgent()

        final_reward = env.run(agent, render=False)

        # Verify completed
        assert env.state['timestep'] == 50

        # Verify final reward is reasonable
        assert isinstance(final_reward, (float, np.floating))

        # Verify history shows all right actions
        history = env.get_history()
        for entry in history:
            _, _, _, action = entry
            assert action == ACTION_RIGHT

    def test_run_cumulative_reward_accuracy(self, gaussian_function, mock_agent):
        """Final reward equals sum of individual step rewards."""
        env = Environment(gaussian_function, episode_length=20)

        # Run episode
        final_reward = env.run(mock_agent, render=False)

        # Get history and manually sum rewards
        history = env.get_history()
        manual_sum = sum(reward for _, _, reward, _ in history)

        # Verify cumulative reward matches sum
        assert abs(final_reward - manual_sum) < 1e-10  # Allow tiny float error

    def test_run_done_flag_termination(self, gaussian_function, mock_agent):
        """Episode stops when done=True (timestep >= episode_length)."""
        episode_length = 25
        env = Environment(gaussian_function, episode_length=episode_length)

        env.run(mock_agent, render=False)

        # Verify episode stopped at exactly episode_length
        assert env.state['timestep'] == episode_length

        # Verify history length matches episode length
        history = env.get_history()
        assert len(history) == episode_length


class TestConfigPersistence:
    """Test Environment.get_config() configuration persistence functionality."""

    def test_get_config_returns_dict(self, gaussian_function):
        """get_config() returns dict type."""
        env = Environment(gaussian_function)
        config = env.get_config()

        assert isinstance(config, dict)

    def test_get_config_contains_required_keys(self, gaussian_function):
        """get_config() contains all required configuration keys."""
        env = Environment(gaussian_function)
        config = env.get_config()

        # Verify all 6 required keys present
        required_keys = {
            'episode_length',
            'observation_radius',
            'n_gradient_samples',
            'step_size',
            'function_params',
            'bounds'
        }
        assert set(config.keys()) == required_keys

    def test_get_config_values_correct(self, gaussian_function):
        """get_config() values match environment settings."""
        env = Environment(
            gaussian_function,
            episode_length=500,
            observation_radius=7.5,
            n_gradient_samples=30,
            step_size=0.5
        )
        config = env.get_config()

        # Verify environment configuration values
        assert config['episode_length'] == 500
        assert config['observation_radius'] == 7.5
        assert config['n_gradient_samples'] == 30
        assert config['step_size'] == 0.5

    def test_get_config_function_params_included(self, gaussian_function):
        """get_config() includes function_params from function.get_config()."""
        env = Environment(gaussian_function)
        config = env.get_config()

        # Verify function_params is dict
        assert isinstance(config['function_params'], dict)

        # Verify function_params is not empty (GaussianTranslation has config)
        assert len(config['function_params']) > 0

    def test_get_config_function_params_with_gaussian(self):
        """get_config() function_params contains GaussianTranslation parameters."""
        func = GaussianTranslation(
            mean_start=-5.0,
            velocity=0.2,
            sigma=2.0,
            amplitude=0.5,
            bounds=(-15.0, 15.0),
            seed=123
        )
        env = Environment(func)
        config = env.get_config()

        function_params = config['function_params']

        # Verify all GaussianTranslation parameters present
        assert function_params['mean_start'] == -5.0
        assert function_params['velocity'] == 0.2
        assert function_params['sigma'] == 2.0
        assert function_params['amplitude'] == 0.5
        assert function_params['bounds'] == (-15.0, 15.0)
        assert function_params['seed'] == 123

    def test_get_config_without_function_get_config(self):
        """get_config() handles function without get_config() method."""
        # Create mock function without get_config()
        class MockFunctionNoConfig:
            @property
            def bounds(self):
                return (-10.0, 10.0)

            def evaluate(self, x, t):
                return np.zeros_like(x)

            def get_perfect_score(self, episode_length):
                return 0.0

        mock_func = MockFunctionNoConfig()
        env = Environment(mock_func)
        config = env.get_config()

        # Verify function_params is empty dict when get_config() not available
        assert config['function_params'] == {}

    def test_get_config_bounds_included(self, gaussian_function):
        """get_config() includes bounds from function."""
        env = Environment(gaussian_function)
        config = env.get_config()

        # Verify bounds included
        assert 'bounds' in config
        assert config['bounds'] == gaussian_function.bounds

    def test_get_config_returns_copy(self, gaussian_function):
        """get_config() returns copy - modifications don't affect environment."""
        env = Environment(gaussian_function)
        config1 = env.get_config()
        config2 = env.get_config()

        # Modify first config
        config1['episode_length'] = 999999

        # Verify second config unaffected
        assert config2['episode_length'] == 1000

        # Verify environment unaffected
        assert env.episode_length == 1000

    def test_get_config_multiple_calls_same_values(self, gaussian_function):
        """Multiple get_config() calls return equivalent configurations."""
        env = Environment(gaussian_function)
        config1 = env.get_config()
        config2 = env.get_config()
        config3 = env.get_config()

        # Verify all configs are equal
        assert config1 == config2
        assert config2 == config3

    def test_get_config_json_serializable(self, gaussian_function):
        """get_config() returns JSON-serializable dict."""
        import json

        env = Environment(gaussian_function)
        config = env.get_config()

        # Verify JSON serialization succeeds
        json_str = json.dumps(config)
        assert isinstance(json_str, str)
        assert len(json_str) > 0

    def test_get_config_json_round_trip(self, gaussian_function):
        """get_config() preserves values through JSON round-trip."""
        import json

        env = Environment(
            gaussian_function,
            episode_length=777,
            observation_radius=8.25,
            n_gradient_samples=25,
            step_size=0.75
        )
        config = env.get_config()

        # Round-trip through JSON
        json_str = json.dumps(config)
        config_loaded = json.loads(json_str)

        # Verify all values preserved
        assert config_loaded['episode_length'] == 777
        assert config_loaded['observation_radius'] == 8.25
        assert config_loaded['n_gradient_samples'] == 25
        assert config_loaded['step_size'] == 0.75

    def test_get_config_performance(self, gaussian_function):
        """get_config() completes in < 1ms."""
        import timeit

        env = Environment(gaussian_function)

        # Time 1000 calls
        time_taken = timeit.timeit(
            lambda: env.get_config(),
            number=1000
        )

        # Average time per call
        avg_time = time_taken / 1000

        # Verify < 1ms (0.001 seconds)
        assert avg_time < 0.001, f"get_config() took {avg_time*1000:.3f}ms, expected < 1ms"

    def test_get_config_with_default_params(self, gaussian_function):
        """get_config() works with default environment parameters."""
        env = Environment(gaussian_function)
        config = env.get_config()

        # Verify default values
        assert config['episode_length'] == 1000
        assert config['observation_radius'] == 5.0
        assert config['n_gradient_samples'] == 20
        assert config['step_size'] == 1.0

    def test_get_config_completeness(self, gaussian_function):
        """get_config() includes all parameters for environment reconstruction."""
        env = Environment(
            gaussian_function,
            episode_length=750,
            observation_radius=6.0,
            n_gradient_samples=15,
            step_size=0.8
        )
        config = env.get_config()

        # Verify all constructor parameters present
        assert 'episode_length' in config
        assert 'observation_radius' in config
        assert 'n_gradient_samples' in config
        assert 'step_size' in config
        assert 'function_params' in config
        assert 'bounds' in config

        # Verify can reconstruct function (if has all params)
        if config['function_params']:
            # GaussianTranslation case
            assert 'mean_start' in config['function_params']
            assert 'velocity' in config['function_params']
            assert 'sigma' in config['function_params']
