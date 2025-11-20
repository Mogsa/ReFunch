"""
Unit tests for temporal function evaluation and perfect score calculation.

Tests verify correctness, reproducibility, and performance of Function2D
implementations, particularly GaussianTranslation.
"""

import numpy as np
import pytest
from funcbench.function import Function2D, GaussianTranslation


class TestGaussianEvaluation:
    """Test suite for GaussianTranslation.evaluate() method."""

    def test_gaussian_evaluation(self):
        """Test function evaluates correctly at known points."""
        func = GaussianTranslation(
            mean_start=-10.0,
            velocity=0.1,
            sigma=1.0,
            amplitude=1.0
        )

        # Test 1: Evaluate at peak position (t=0, x=-10.0)
        # Peak is at mean_start at t=0
        reward = func.evaluate(np.array([-10.0]), t=0.0)
        assert np.isclose(reward[0], 1.0), "Peak value should equal amplitude"

        # Test 2: Evaluate at translated peak (t=100, x=0.0)
        # Peak moves to mean_start + velocity * t = -10.0 + 0.1 * 100 = 0.0
        reward = func.evaluate(np.array([0.0]), t=100.0)
        assert np.isclose(reward[0], 1.0), "Translated peak should equal amplitude"

        # Test 3: Evaluate away from peak
        # At t=0, peak is at -10.0, evaluate at -12.0 (2 sigma away)
        reward = func.evaluate(np.array([-12.0]), t=0.0)
        # Gaussian value at 2 sigma from mean: exp(-4/2) = exp(-2) ≈ 0.1353
        expected = np.exp(-2.0)
        assert np.isclose(reward[0], expected, rtol=1e-5), \
            f"Expected {expected}, got {reward[0]}"

    def test_result_shape_matches_input(self):
        """Test that result shape matches input shape."""
        func = GaussianTranslation()

        # Single point
        x_single = np.array([0.0])
        result = func.evaluate(x_single, t=0.0)
        assert result.shape == x_single.shape, \
            f"Expected shape {x_single.shape}, got {result.shape}"

        # Multiple points
        x_multi = np.linspace(-20, 20, 50)
        result = func.evaluate(x_multi, t=0.0)
        assert result.shape == x_multi.shape, \
            f"Expected shape {x_multi.shape}, got {result.shape}"

    def test_result_dtype_is_float64(self):
        """Test that result dtype is float64."""
        func = GaussianTranslation()
        x = np.array([0.0, 1.0, 2.0])
        result = func.evaluate(x, t=0.0)
        assert result.dtype == np.float64, \
            f"Expected dtype float64, got {result.dtype}"

    def test_peak_value_equals_amplitude(self):
        """Test peak value equals amplitude when x = mean_t."""
        # Test with non-default amplitude
        amplitude = 2.5
        func = GaussianTranslation(
            mean_start=5.0,
            velocity=0.2,
            amplitude=amplitude
        )

        # At t=10, peak is at 5.0 + 0.2 * 10 = 7.0
        reward = func.evaluate(np.array([7.0]), t=10.0)
        assert np.isclose(reward[0], amplitude), \
            f"Peak should equal amplitude {amplitude}, got {reward[0]}"


class TestPerfectScoreCalculation:
    """Test suite for GaussianTranslation.get_perfect_score() method."""

    def test_perfect_score_calculation(self):
        """Test perfect score equals amplitude * episode_length."""
        func = GaussianTranslation(amplitude=1.0)
        episode_length = 100

        perfect_score = func.get_perfect_score(episode_length)
        expected = func.amplitude * episode_length

        assert np.isclose(perfect_score, expected), \
            f"Expected {expected}, got {perfect_score}"

    def test_perfect_score_with_custom_amplitude(self):
        """Test perfect score with non-default amplitude."""
        amplitude = 3.5
        episode_length = 50
        func = GaussianTranslation(amplitude=amplitude)

        perfect_score = func.get_perfect_score(episode_length)
        expected = amplitude * episode_length

        assert np.isclose(perfect_score, expected), \
            f"Expected {expected}, got {perfect_score}"

    def test_perfect_score_is_deterministic(self):
        """Test score is deterministic (same inputs = same output)."""
        func = GaussianTranslation(amplitude=1.5)
        episode_length = 75

        # Call multiple times with same inputs
        score1 = func.get_perfect_score(episode_length)
        score2 = func.get_perfect_score(episode_length)
        score3 = func.get_perfect_score(episode_length)

        assert score1 == score2 == score3, \
            "Perfect score should be deterministic"

    def test_perfect_score_dtype_is_float(self):
        """Test result dtype is float."""
        func = GaussianTranslation()
        perfect_score = func.get_perfect_score(100)

        assert isinstance(perfect_score, (float, np.floating)), \
            f"Expected float type, got {type(perfect_score)}"


class TestVectorizedEvaluation:
    """Test suite for vectorized operations."""

    def test_single_point_evaluation(self):
        """Test single point evaluation: x=np.array([0.0])."""
        func = GaussianTranslation()
        x = np.array([0.0])
        result = func.evaluate(x, t=0.0)

        assert isinstance(result, np.ndarray), \
            f"Expected np.ndarray, got {type(result)}"
        assert result.shape == (1,), \
            f"Expected shape (1,), got {result.shape}"
        assert result.dtype == np.float64, \
            f"Expected dtype float64, got {result.dtype}"

    def test_multiple_points_evaluation(self):
        """Test multiple points: x=np.linspace(-10, 10, 100)."""
        func = GaussianTranslation()
        x = np.linspace(-10, 10, 100)
        result = func.evaluate(x, t=0.0)

        assert isinstance(result, np.ndarray), \
            f"Expected np.ndarray, got {type(result)}"
        assert result.shape == (100,), \
            f"Expected shape (100,), got {result.shape}"
        assert result.dtype == np.float64, \
            f"Expected dtype float64, got {result.dtype}"

    def test_vectorized_performance(self):
        """Test vectorized evaluation completes quickly."""
        import time

        func = GaussianTranslation()
        x = np.linspace(-20, 20, 1000)

        # Warm up
        func.evaluate(x, t=0.0)

        # Measure performance
        start = time.perf_counter()
        for _ in range(100):
            func.evaluate(x, t=0.0)
        elapsed_ms = (time.perf_counter() - start) * 1000 / 100

        # Should be very fast with vectorization
        assert elapsed_ms < 1.0, \
            f"Vectorized evaluation should be < 1ms, took {elapsed_ms:.3f}ms"

    def test_results_are_numpy_arrays(self):
        """Test results are numpy arrays with correct shapes."""
        func = GaussianTranslation()

        # Test various input sizes
        test_cases = [
            np.array([0.0]),
            np.linspace(-10, 10, 10),
            np.linspace(-20, 20, 100),
            np.array([-5.0, 0.0, 5.0]),
        ]

        for x in test_cases:
            result = func.evaluate(x, t=0.0)
            assert isinstance(result, np.ndarray), \
                "Result must be numpy array"
            assert result.shape == x.shape, \
                f"Shape mismatch: input {x.shape}, output {result.shape}"


class TestSpatialBounds:
    """Test suite for bounds property."""

    def test_bounds_tuple_accessible(self):
        """Test bounds tuple is accessible."""
        func = GaussianTranslation()
        bounds = func.bounds

        assert bounds is not None, "Bounds should not be None"
        assert isinstance(bounds, tuple), \
            f"Bounds should be tuple, got {type(bounds)}"

    def test_bounds_contain_valid_floats(self):
        """Test bounds contain valid float values."""
        func = GaussianTranslation(bounds=(-20.0, 20.0))
        bounds = func.bounds

        assert len(bounds) == 2, \
            f"Bounds should have 2 elements, got {len(bounds)}"

        left, right = bounds
        assert isinstance(left, (float, np.floating)), \
            f"Left bound should be float, got {type(left)}"
        assert isinstance(right, (float, np.floating)), \
            f"Right bound should be float, got {type(right)}"

        assert left < right, \
            f"Left bound ({left}) should be less than right bound ({right})"

    def test_custom_bounds(self):
        """Test custom bounds are stored correctly."""
        custom_bounds = (-50.0, 50.0)
        func = GaussianTranslation(bounds=custom_bounds)

        left, right = func.bounds
        assert np.isclose(left, custom_bounds[0]), \
            f"Left bound mismatch: expected {custom_bounds[0]}, got {left}"
        assert np.isclose(right, custom_bounds[1]), \
            f"Right bound mismatch: expected {custom_bounds[1]}, got {right}"

    def test_default_bounds(self):
        """Test default bounds are (-20.0, 20.0)."""
        func = GaussianTranslation()
        left, right = func.bounds

        assert np.isclose(left, -20.0), \
            f"Default left bound should be -20.0, got {left}"
        assert np.isclose(right, 20.0), \
            f"Default right bound should be 20.0, got {right}"


class TestGaussianTranslationEdgeCases:
    """Test edge cases and special scenarios."""

    def test_zero_velocity(self):
        """Test function with zero velocity (stationary peak)."""
        func = GaussianTranslation(mean_start=0.0, velocity=0.0)

        # Peak should stay at x=0 for all t
        reward_t0 = func.evaluate(np.array([0.0]), t=0.0)
        reward_t100 = func.evaluate(np.array([0.0]), t=100.0)

        assert np.isclose(reward_t0[0], reward_t100[0]), \
            "Zero velocity should keep peak stationary"

    def test_negative_velocity(self):
        """Test function with negative velocity (leftward translation)."""
        func = GaussianTranslation(mean_start=10.0, velocity=-0.1)

        # At t=100, peak should be at 10.0 - 0.1 * 100 = 0.0
        reward = func.evaluate(np.array([0.0]), t=100.0)
        assert np.isclose(reward[0], func.amplitude), \
            "Negative velocity should translate peak leftward"

    def test_different_sigma_values(self):
        """Test function with different sigma (peak width) values."""
        # Narrow peak
        func_narrow = GaussianTranslation(sigma=0.5)
        # Wide peak
        func_wide = GaussianTranslation(sigma=2.0)

        # Both should have same value at peak
        narrow_peak = func_narrow.evaluate(np.array([-10.0]), t=0.0)
        wide_peak = func_wide.evaluate(np.array([-10.0]), t=0.0)

        assert np.isclose(narrow_peak[0], wide_peak[0]), \
            "Peak value should be same regardless of sigma"

        # But different values away from peak
        narrow_away = func_narrow.evaluate(np.array([-11.0]), t=0.0)
        wide_away = func_wide.evaluate(np.array([-11.0]), t=0.0)

        assert narrow_away[0] < wide_away[0], \
            "Narrower peak should decay faster away from center"

    def test_reproducibility_with_seed(self):
        """Test that same seed produces same results."""
        func1 = GaussianTranslation(seed=42)
        func2 = GaussianTranslation(seed=42)

        x = np.linspace(-20, 20, 100)
        result1 = func1.evaluate(x, t=50.0)
        result2 = func2.evaluate(x, t=50.0)

        np.testing.assert_array_equal(result1, result2,
            "Same seed should produce identical results")


class TestGaussianTranslationGetConfig:
    """Test suite for GaussianTranslation.get_config() method."""

    def test_get_config_returns_dict(self):
        """get_config() returns dict type."""
        func = GaussianTranslation()
        config = func.get_config()

        assert isinstance(config, dict), \
            f"get_config() should return dict, got {type(config)}"

    def test_get_config_contains_all_parameters(self):
        """get_config() contains all GaussianTranslation parameters."""
        func = GaussianTranslation()
        config = func.get_config()

        # Verify all required keys present
        required_keys = {
            'mean_start',
            'velocity',
            'sigma',
            'amplitude',
            'bounds',
            'seed'
        }
        assert set(config.keys()) == required_keys, \
            f"Missing keys: {required_keys - set(config.keys())}"

    def test_get_config_values_match_constructor(self):
        """get_config() values match constructor parameters."""
        func = GaussianTranslation(
            mean_start=-5.0,
            velocity=0.2,
            sigma=2.0,
            amplitude=0.5,
            bounds=(-15.0, 15.0),
            seed=123
        )
        config = func.get_config()

        # Verify all values match
        assert config['mean_start'] == -5.0
        assert config['velocity'] == 0.2
        assert config['sigma'] == 2.0
        assert config['amplitude'] == 0.5
        assert config['bounds'] == (-15.0, 15.0)
        assert config['seed'] == 123

    def test_get_config_default_values(self):
        """get_config() returns default values when not specified."""
        func = GaussianTranslation()
        config = func.get_config()

        # Verify default values
        assert config['mean_start'] == -10.0
        assert config['velocity'] == 0.1
        assert config['sigma'] == 1.0
        assert config['amplitude'] == 1.0
        assert config['bounds'] == (-20.0, 20.0)
        assert config['seed'] is None

    def test_get_config_json_serializable(self):
        """get_config() returns JSON-serializable dict."""
        import json

        func = GaussianTranslation(seed=42)
        config = func.get_config()

        # Verify JSON serialization succeeds
        json_str = json.dumps(config)
        assert isinstance(json_str, str)
        assert len(json_str) > 0

    def test_get_config_json_round_trip(self):
        """get_config() values preserved through JSON round-trip."""
        import json

        func = GaussianTranslation(
            mean_start=-7.5,
            velocity=0.15,
            sigma=1.5,
            amplitude=0.8,
            bounds=(-25.0, 25.0),
            seed=999
        )
        config = func.get_config()

        # Round-trip through JSON
        json_str = json.dumps(config)
        config_loaded = json.loads(json_str)

        # Verify all values preserved
        assert config_loaded['mean_start'] == -7.5
        assert config_loaded['velocity'] == 0.15
        assert config_loaded['sigma'] == 1.5
        assert config_loaded['amplitude'] == 0.8
        assert config_loaded['bounds'] == [-25.0, 25.0]  # JSON converts tuple to list
        assert config_loaded['seed'] == 999

    def test_get_config_python_types(self):
        """get_config() converts NumPy types to Python types."""
        func = GaussianTranslation()
        config = func.get_config()

        # Verify all numeric values are Python types (not NumPy)
        assert type(config['mean_start']) == float
        assert type(config['velocity']) == float
        assert type(config['sigma']) == float
        assert type(config['amplitude']) == float

        # bounds is tuple of floats
        assert isinstance(config['bounds'], tuple)
        assert type(config['bounds'][0]) == float
        assert type(config['bounds'][1]) == float

    def test_get_config_with_none_seed(self):
        """get_config() handles None seed correctly."""
        func = GaussianTranslation(seed=None)
        config = func.get_config()

        assert config['seed'] is None

    def test_get_config_enables_reconstruction(self):
        """Configuration from get_config() enables function reconstruction."""
        # Create original function
        original = GaussianTranslation(
            mean_start=-8.0,
            velocity=0.12,
            sigma=1.2,
            amplitude=0.9,
            bounds=(-30.0, 30.0),
            seed=456
        )

        # Get config
        config = original.get_config()

        # Reconstruct function from config
        reconstructed = GaussianTranslation(
            mean_start=config['mean_start'],
            velocity=config['velocity'],
            sigma=config['sigma'],
            amplitude=config['amplitude'],
            bounds=config['bounds'],
            seed=config['seed']
        )

        # Verify reconstructed function behaves identically
        x = np.linspace(-30, 30, 100)
        original_values = original.evaluate(x, t=50.0)
        reconstructed_values = reconstructed.evaluate(x, t=50.0)

        np.testing.assert_array_equal(
            original_values,
            reconstructed_values,
            err_msg="Reconstructed function should produce identical values"
        )

    def test_get_config_performance(self):
        """get_config() completes quickly (< 1ms)."""
        import timeit

        func = GaussianTranslation()

        # Time 1000 calls
        time_taken = timeit.timeit(
            lambda: func.get_config(),
            number=1000
        )

        # Average time per call
        avg_time = time_taken / 1000

        # Verify < 1ms (0.001 seconds)
        assert avg_time < 0.001, \
            f"get_config() took {avg_time*1000:.3f}ms, expected < 1ms"
