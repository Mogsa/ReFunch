# Story 2.7: Add Configuration Persistence

Status: done

## Story

As a researcher,
I want to access environment configuration parameters,
So that I can save experiment settings for reproducibility.

## Acceptance Criteria

**Given** Environment with configuration parameters from Story 2.2
**When** I implement get_config() method
**Then** it returns dict containing:
```python
{
    'episode_length': int,
    'observation_radius': float,
    'n_gradient_samples': int,
    'step_size': float,
    'function_params': dict,  # From function
    'bounds': tuple
}
```

**And** function_params includes function-specific configuration (velocity, sigma, amplitude, etc.)

**And** get_config() returns copy of configuration (not reference to internals)

**And** configuration dict is JSON-serializable for saving experiments

**And** method completes in < 1ms (simple dict construction)

## Tasks / Subtasks

- [x] Implement get_config() method signature (AC: #1)
  - [x] Add method to Environment class: `def get_config(self) -> dict:`
  - [x] Return type hint: -> dict
  - [x] Method is public (no underscore prefix)
  - [x] No parameters (returns current environment configuration)

- [x] Collect environment configuration parameters (AC: #1)
  - [x] Create dict with episode_length from self.episode_length
  - [x] Add observation_radius from self.observation_radius
  - [x] Add n_gradient_samples from self.n_gradient_samples
  - [x] Add step_size from self.step_size
  - [x] Add bounds from self.function.bounds
  - [x] Ensure all values are from instance attributes set in __init__

- [x] Collect function configuration (AC: #2)
  - [x] Check if function has get_config() method
  - [x] If function.get_config() exists: call it and store as function_params
  - [x] If function.get_config() doesn't exist: use empty dict for function_params
  - [x] Handle AttributeError gracefully if method not available
  - [x] Function params should include: velocity, sigma, amplitude, seed, etc.

- [x] Return configuration copy (AC: #3)
  - [x] Create new dict (not reference to internal state)
  - [x] Use dict literal construction: `{'key': value, ...}`
  - [x] Don't store config as instance attribute (generate fresh each call)
  - [x] Ensure returned dict is independent of internal state
  - [x] Modifications to returned dict should not affect environment

- [x] Ensure JSON serializability (AC: #4)
  - [x] Test all values are JSON-serializable types (int, float, str, bool, list, dict, None)
  - [x] Convert numpy types to Python types if needed (np.float64 -> float)
  - [x] Tuples (like bounds) are JSON-serializable via list conversion if needed
  - [x] Test: `json.dumps(env.get_config())` succeeds without errors
  - [x] Validate round-trip: json.loads(json.dumps(config)) preserves values

- [x] Add comprehensive NumPy-style docstring (AC: #1, #2, #3, #4, #5)
  - [x] One-line summary: "Get environment configuration parameters"
  - [x] Longer description explaining configuration dict structure
  - [x] Returns section with dict structure and field descriptions
  - [x] Notes section explaining JSON serializability
  - [x] Notes section explaining copy semantics (modifications don't affect environment)
  - [x] Examples section showing usage pattern
  - [x] Document that function_params may be empty dict if function doesn't support get_config()

- [x] Add unit tests (AC: #1, #2, #3, #4, #5)
  - [x] test_get_config_returns_dict: Verify return type is dict
  - [x] test_get_config_contains_required_keys: Verify all required keys present
  - [x] test_get_config_values_correct: Verify values match environment settings
  - [x] test_get_config_function_params: Verify function_params included
  - [x] test_get_config_returns_copy: Verify returned dict is copy (not reference)
  - [x] test_get_config_json_serializable: Verify json.dumps() succeeds
  - [x] test_get_config_json_round_trip: Verify round-trip preserves values
  - [x] test_get_config_performance: Verify completes in < 1ms
  - [x] test_get_config_multiple_calls: Verify multiple calls return same values
  - [x] Create mock function with get_config() for testing

- [x] Integration with function.get_config() (AC: #2)
  - [x] Test with GaussianTranslation (check if it has get_config())
  - [x] If GaussianTranslation doesn't have get_config(), implement it
  - [x] GaussianTranslation.get_config() should return: velocity, sigma, amplitude, mean_start, bounds, seed
  - [x] Test get_config() with function that has configuration
  - [x] Test get_config() with mock function without get_config() method

- [x] Validate configuration completeness (AC: #1, #2)
  - [x] Verify all environment constructor parameters included in config
  - [x] Verify bounds from function included
  - [x] Verify function-specific params included (if available)
  - [x] Config should enable exact environment reconstruction
  - [x] Document which parameters enable reproducibility

- [x] Run all tests and ensure they pass (AC: #1-#5)
  - [x] All new get_config() tests pass
  - [x] All existing environment tests still pass (regression check)
  - [x] Total test count increases by ~24 tests (10 function + 14 environment)
  - [x] Test coverage for get_config() method > 95%
  - [x] JSON serialization tests pass

## Dev Notes

### Requirements Context Summary

**From PRD FR64:**
- FR64: Configuration via Python API and config files
- System must expose configuration for reproducibility

**From Architecture:**
- Enables reproducible experiments (Architecture NFR6-10)
- JSON-serializable format for easy storage
- Return copies to prevent external mutation
- Include function configuration for complete experiment specification
- Configuration saved alongside episode data enables exact reproduction

**From Tech Spec Epic 2 (Story 2.7):**
- get_config() returns dict with episode_length, observation_radius, n_gradient_samples, step_size, function_params, bounds
- function_params includes function-specific configuration
- Returns copy of configuration (not reference)
- Configuration dict is JSON-serializable
- Method completes in < 1ms

### Project Structure Alignment

**Files Modified:**
- `src/funcbench/environment.py` - Add get_config() method
- `src/funcbench/function.py` - Potentially add get_config() to GaussianTranslation if not present
- `tests/test_environment.py` - Add get_config() tests

**Dependencies:**
- Environment.__init__() from Story 2.2 (config parameters stored as attributes)
- Function2D interface from Story 1.2
- GaussianTranslation from Story 1.3 (may need get_config() method)

**Integration Points:**
- JSON serialization (json module)
- Function configuration (function.get_config() if available)
- Experiment reproducibility (NFR6-10)

### Learnings from Previous Story

**From Story 2.6 (Status: drafted, just created)**

- **Story Pattern:**
  - Comprehensive acceptance criteria with And clauses
  - Detailed task breakdown with subtasks
  - Implementation pattern in Dev Notes
  - References to Architecture and Tech Spec

- **Testing Pattern:**
  - Unit tests for each AC
  - Integration tests for cross-component interaction
  - Performance validation
  - Comprehensive coverage (>90%)

- **Documentation Pattern:**
  - NumPy-style docstrings with examples
  - Type hints on all signatures
  - Notes sections explaining design decisions

**From Story 2.5 (Status: done)**

- **Copy Semantics Pattern:**
  - get_history() returns copy using `list(self.state['history'])`
  - Prevents external mutation of internal state
  - Test validates copy behavior (test_get_history_returns_copy)
  - Same pattern should apply to get_config()

- **Implementation Quality:**
  - Type hints on method signatures
  - Comprehensive NumPy-style docstrings (31 lines for get_history())
  - Performance validation via timeit tests
  - Defensive programming (copy semantics)

[Source: docs/sprint-artifacts/2-5-implement-episode-history-tracking.md#Dev-Agent-Record]
[Source: docs/sprint-artifacts/2-6-implement-run-method-for-episode-execution.md#Dev-Notes]

### Architecture Alignment

**API Contract (from Architecture Section "Reproducibility" NFR6-10):**
- get_config() enables reproducible experiments
- JSON-serializable format for easy storage
- Return copies to prevent external mutation
- Include all parameters needed to reconstruct environment

**Implementation Pattern:**
```python
def get_config(self) -> dict:
    """Get environment configuration parameters.

    Returns complete configuration as JSON-serializable dict,
    including environment settings and function parameters.
    Enables reproducible experiment setup.

    Returns
    -------
    dict
        Configuration dictionary with keys:
        - 'episode_length': int, number of timesteps per episode
        - 'observation_radius': float, fog-of-war window size
        - 'n_gradient_samples': int, number of local samples
        - 'step_size': float, distance moved per action
        - 'function_params': dict, function-specific configuration
        - 'bounds': tuple, spatial bounds from function

    Notes
    -----
    Returns a copy of configuration to prevent external modifications.
    All values are JSON-serializable for saving experiments.
    function_params may be empty dict if function doesn't support get_config().

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
```

**Consistency Rules:**
- Return new dict (not reference to internal state)
- All values JSON-serializable
- Include all constructor parameters
- Include function configuration if available

### Testing Strategy

**Unit Tests (this story):**
- Test get_config() returns dict
- Test all required keys present
- Test values match environment settings
- Test function_params included
- Test returned dict is copy (not reference)
- Test JSON serializability (json.dumps succeeds)
- Test JSON round-trip preserves values
- Test performance (< 1ms)
- Test multiple calls return same values

**Integration Tests:**
- Test with GaussianTranslation (has get_config())
- Test with mock function without get_config()
- Test configuration completeness (can reconstruct environment)
- Test configuration saved and loaded via JSON

**Performance Tests:**
- get_config() completes in < 1ms
- Simple dict construction (no complex operations)

### Performance Considerations

**Target:** get_config() completes in < 1ms

**Performance Budget:**
- Dict construction: < 0.1ms (6 key-value pairs)
- Function get_config() call: < 0.5ms (if exists)
- Total: < 1ms expected

**Optimization Notes:**
- Simple dict construction (no copying large data structures)
- Function get_config() should be fast (just returns stored params)
- No file I/O or network calls
- No complex computations

### GaussianTranslation.get_config() Implementation

If GaussianTranslation doesn't have get_config(), implement it:

```python
def get_config(self) -> dict:
    """Get function configuration parameters.

    Returns
    -------
    dict
        Configuration dictionary with function parameters
    """
    return {
        'mean_start': self.mean_start,
        'velocity': self.velocity,
        'sigma': self.sigma,
        'amplitude': self.amplitude,
        'bounds': self.bounds,
        'seed': self.seed
    }
```

This enables complete function reconstruction for reproducibility.

### References

- **Tech Spec Epic 2**: Story 2.7 - Configuration Persistence
- **Architecture.md**: Section "Reproducibility" NFR6-10, Section "Configuration"
- **Story 2.2**: Environment initialization (config parameters stored)
- **Story 1.3**: GaussianTranslation implementation
- **PRD**: FR64 (Configuration via Python API)

## Dev Agent Record

### Context Reference

- docs/sprint-artifacts/2-7-add-configuration-persistence.context.xml

### Agent Model Used

Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)

### Debug Log References

#### Implementation Plan
1. Implemented GaussianTranslation.get_config() method in src/funcbench/function.py
2. Implemented Environment.get_config() method in src/funcbench/environment.py
3. Added comprehensive test suite (24 new tests total)
4. Validated all acceptance criteria and performance requirements

#### Key Implementation Details
- GaussianTranslation.get_config() returns all constructor parameters (mean_start, velocity, sigma, amplitude, bounds, seed)
- Environment.get_config() collects environment and function configuration
- Used hasattr() to gracefully handle functions without get_config()
- Converted NumPy float64 types to Python float for JSON serialization
- Both methods use dict literal construction (creates copy, not reference)
- Performance validated: both methods complete in < 1ms

### Completion Notes List

**Story 2.7: Add Configuration Persistence - COMPLETE**

✅ **Implemented GaussianTranslation.get_config() (AC #2)**
- Added get_config() method to GaussianTranslation class (src/funcbench/function.py:269-317)
- Returns dict with all function parameters: mean_start, velocity, sigma, amplitude, bounds, seed
- Converts NumPy float64 types to Python float for JSON compatibility
- Comprehensive 47-line NumPy-style docstring with examples
- Method signature: `def get_config(self) -> dict:`

✅ **Implemented Environment.get_config() (AC #1, #3, #4, #5)**
- Added get_config() method to Environment class (src/funcbench/environment.py:431-493)
- Returns dict with 6 keys: episode_length, observation_radius, n_gradient_samples, step_size, function_params, bounds
- Uses hasattr() to gracefully handle functions without get_config() (returns empty dict)
- Creates new dict each call (copy semantics, not reference)
- 43-line NumPy-style docstring following project patterns
- Method signature: `def get_config(self) -> dict:`

✅ **Comprehensive Test Coverage (AC #1-5)**
- Added 10 tests for GaussianTranslation.get_config() in tests/test_function.py:308-483
  - test_get_config_returns_dict
  - test_get_config_contains_all_parameters
  - test_get_config_values_match_constructor
  - test_get_config_default_values
  - test_get_config_json_serializable
  - test_get_config_json_round_trip
  - test_get_config_python_types
  - test_get_config_with_none_seed
  - test_get_config_enables_reconstruction
  - test_get_config_performance (< 1ms validated)

- Added 14 tests for Environment.get_config() in tests/test_environment.py:1378-1600
  - test_get_config_returns_dict
  - test_get_config_contains_required_keys
  - test_get_config_values_correct
  - test_get_config_function_params_included
  - test_get_config_function_params_with_gaussian
  - test_get_config_without_function_get_config (mock function test)
  - test_get_config_bounds_included
  - test_get_config_returns_copy
  - test_get_config_multiple_calls_same_values
  - test_get_config_json_serializable
  - test_get_config_json_round_trip
  - test_get_config_performance (< 1ms validated)
  - test_get_config_with_default_params
  - test_get_config_completeness

✅ **All Tests Pass - Zero Regressions**
- Total tests: 140 passed in 0.18s
- Previous test count: 116 tests
- New tests added: 24 tests (10 function + 14 environment)
- No test failures or regressions
- Performance requirements validated: both get_config() methods < 1ms

✅ **All Acceptance Criteria Met**
- AC1: get_config() returns dict with all required keys ✓
- AC2: function_params includes GaussianTranslation configuration ✓
- AC3: Returns copy (not reference to internals) ✓
- AC4: Configuration dict is JSON-serializable ✓
- AC5: Method completes in < 1ms ✓

✅ **Code Quality**
- Followed copy semantics pattern from get_history() (Story 2.5)
- NumPy-style docstrings with comprehensive examples
- Type hints on all method signatures
- Graceful handling of missing function.get_config()
- JSON round-trip validated in tests

### File List

**Modified:**
- src/funcbench/function.py - Added GaussianTranslation.get_config() method (line 269-317)
- src/funcbench/environment.py - Added Environment.get_config() method (line 431-493)
- tests/test_function.py - Added TestGaussianTranslationGetConfig class (line 308-483)
- tests/test_environment.py - Added TestConfigPersistence class (line 1378-1600)

**Created:**
- None (all changes to existing files)
