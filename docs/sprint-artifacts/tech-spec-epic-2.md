# Epic Technical Specification: Environment & Agent Execution

Date: 2025-11-17
Author: Morgan
Epic ID: 2
Status: Draft

---

## Overview

Epic 2 implements the complete agent-environment interaction system that enables episode execution, state management, and performance evaluation. Building on Epic 1's function foundation, this epic creates the core "game loop" that allows agents to observe local gradients, take actions, and accumulate rewards over time. This is the critical bridge between mathematical function definitions and actual AI agent evaluation - without this epic, there is no way to test whether agents can learn temporal patterns.

The primary goal is enabling headless (visualization-free) episode execution for batch evaluation, which is essential for scientific experimentation. Researchers need to run hundreds of episodes quickly to measure learning curves and compare agent performance against baselines.

## Objectives and Scope

**In Scope for Epic 2:**
- Agent abstract base class with standardized action interface (0=left, 1=stay, 2=right)
- Environment class managing episode lifecycle (reset, step, done detection)
- Observation generation with local gradient sampling (fog-of-war implementation)
- Action execution with position updates and bounds enforcement
- Cumulative reward tracking and perfect score comparison
- Episode history recording (timestep, position, reward, action tuples)
- Configuration persistence (get_config() for reproducible experiments)
- Complete unit test coverage for all environment functionality
- Headless mode support (render_mode=False) for batch evaluation

**Out of Scope for Epic 2:**
- Visualization rendering (deferred to Epic 4)
- Specific agent implementations beyond base class (Epic 3 covers RandomAgent, GreedyAgent)
- Multi-episode evaluation utilities (covered in Epic 3)
- Episode replay UI/controls (Epic 4)
- LLM integration (post-MVP)
- Advanced metrics and analysis tools (Epic 3 and post-MVP)

**Success Criteria:**
- Complete 1000-timestep episode executes in < 2 seconds (headless mode)
- State management is deterministic (same seed = identical episode outcomes)
- All 8 stories pass acceptance criteria and unit tests
- Environment API follows Gym-like pattern for researcher familiarity

## System Architecture Alignment

Epic 2 directly implements the **Environment API Contract** and **Episode State Management** patterns defined in the Architecture document.

**Key Architecture Components Realized:**
- **Environment class** (`environment.py`): Implements reset(), step(), run() methods per Architecture API specification
- **Agent interface** (`agent.py`): Abstract base class enforcing get_action(observation) → int contract
- **State centralization**: Single state dict pattern for easy serialization and testing
- **Gym-like API**: Step returns (observation, reward, done, info) tuple per ADR-004
- **Float64 precision**: All reward calculations use np.float64 per NFR11 (reproducibility)
- **Observation dict pattern**: Dict-based observations per ADR-005 for extensibility

**Performance Alignment:**
- NFR3: Fast episode execution (< 20s with viz, < 2s headless) → Implemented via efficient NumPy operations
- NFR2: Efficient function evaluation (< 1ms) → Leveraged from Epic 1's vectorized Gaussian implementation
- NFR4: Batch evaluation (100 episodes < 5 min) → Enabled by headless mode

**Data Flow Consistency:**
- Follows Architecture "Episode Execution Flow" exactly (reset → loop[get_action → step] → done)
- Observation dictionary uses exact keys from Architecture specification
- Action space uses exact integer codes from Architecture consistency rules

## Detailed Design

### Services and Modules

| Module | File | Responsibility | Key Methods | Owner |
|--------|------|----------------|-------------|-------|
| **Agent** | `src/funcbench/agent.py` | Abstract base class defining agent interface; enforces action contract | `get_action(observation) -> int` | Epic 2 |
| **Environment** | `src/funcbench/environment.py` | Episode lifecycle management, state tracking, agent-function coordination | `__init__()`, `reset()`, `step(action)`, `run(agent)`, `get_config()` | Epic 2 |
| **Environment._get_observation()** | `src/funcbench/environment.py` | Private method for observation generation with gradient sampling | `_get_observation() -> dict` | Epic 2 (Story 2.3) |

**Module Dependencies:**
- `agent.py` → No dependencies (pure abstract base)
- `environment.py` → Depends on `function.py` (Function2D from Epic 1)
- Test modules → Depend on both agent.py and environment.py

**Input/Output Summary:**
- **Agent.get_action()**: Input = observation dict, Output = action int (0/1/2)
- **Environment.reset()**: Input = none, Output = initial observation dict
- **Environment.step()**: Input = action int, Output = (observation, reward, done, info) tuple
- **Environment.run()**: Input = agent instance, Output = final cumulative reward float

### Data Models and Contracts

**Action Constants (src/funcbench/agent.py):**
```python
ACTION_LEFT = 0   # Move left by step_size
ACTION_STAY = 1   # Stay at current position
ACTION_RIGHT = 2  # Move right by step_size
```

**Environment State (internal to Environment class):**
```python
self.state = {
    'position': np.float64,         # Agent's current x-coordinate
    'timestep': int,                # Current time (0 to episode_length-1)
    'cumulative_reward': np.float64, # Running sum of rewards
    'history': list[tuple]          # [(timestep, position, reward, action), ...]
}
```

**Observation Dictionary (returned by Environment to Agent):**
```python
observation = {
    'position': float,               # Current agent x-coordinate
    'reward': float,                 # Reward at current position and time
    'gradient': np.ndarray,          # Array of n_gradient_samples function values
    'gradient_positions': np.ndarray, # Array of n_gradient_samples x-coordinates
    'timestep': int                  # Current timestep
}
```
- Keys MUST match Architecture specification exactly (consistency rule)
- gradient and gradient_positions are 1D numpy arrays of length n_gradient_samples
- All arrays use float64 dtype

**Info Dictionary (returned in step() tuple):**
```python
info = {
    'cumulative_reward': float,  # Running total reward
    'perfect_score': float       # Theoretical maximum for this episode
}
```

**Configuration Dictionary (returned by get_config()):**
```python
config = {
    'episode_length': int,           # Total timesteps per episode
    'observation_radius': float,     # Fog-of-war window size
    'n_gradient_samples': int,       # Number of local samples
    'step_size': float,              # Distance moved per action
    'function_params': dict,         # From function.get_config() if available
    'bounds': tuple[float, float]    # Spatial bounds from function
}
```

### APIs and Interfaces

**Agent Abstract Base Class:**
```python
from abc import ABC, abstractmethod

class Agent(ABC):
    """Abstract base for all agent implementations.

    Agents receive observations and return actions. This interface
    enables easy swapping between different AI architectures.
    """

    @abstractmethod
    def get_action(self, observation: dict) -> int:
        """Choose action based on current observation.

        Parameters
        ----------
        observation : dict
            Keys: 'position', 'reward', 'gradient', 'gradient_positions', 'timestep'

        Returns
        -------
        int
            Action code: 0 (left), 1 (stay), or 2 (right)

        Raises
        ------
        NotImplementedError
            Must be implemented by subclass
        """
        pass
```

**Environment Class (Public API):**
```python
class Environment:
    """Manages episode execution and agent-environment interaction."""

    def __init__(
        self,
        function: Function2D,
        episode_length: int = 1000,
        observation_radius: float = 5.0,
        n_gradient_samples: int = 20,
        step_size: float = 1.0,
        render_mode: bool = False
    ) -> None:
        """Initialize environment with function and configuration."""
        pass

    def reset(self) -> dict:
        """Start new episode, reset state, return initial observation."""
        pass

    def step(self, action: int) -> tuple[dict, float, bool, dict]:
        """Execute action, advance time, return (obs, reward, done, info)."""
        pass

    def run(self, agent: Agent, render: bool = False) -> float:
        """Run complete episode with agent, return final cumulative reward."""
        pass

    def get_config(self) -> dict:
        """Return environment configuration for reproducibility."""
        pass

    def get_history(self) -> list[tuple]:
        """Return copy of episode history."""
        pass

    # Private methods (internal use)
    def _get_observation(self) -> dict:
        """Generate observation dict from current state."""
        pass
```

**Error Handling:**
- `step(action)` raises `ValueError` if action not in [0, 1, 2]
- Error message format: `"Invalid action {action}. Must be 0 (left), 1 (stay), or 2 (right)"`
- All validation happens at API boundaries (public methods)

### Workflows and Sequencing

**Episode Execution Sequence (primary workflow):**

```
1. Initialization (one-time setup)
   ┌─────────────────────────────────────┐
   │ env = Environment(func, config...)  │
   └─────────────────────────────────────┘
                    │
                    ▼
2. Episode Start
   ┌─────────────────────────────────────┐
   │ obs = env.reset()                    │
   │  └─ position = 0.0                   │
   │  └─ timestep = 0                     │
   │  └─ cumulative_reward = 0.0          │
   │  └─ history = []                     │
   │  └─ Generate initial observation     │
   └─────────────────────────────────────┘
                    │
                    ▼
3. Episode Loop (repeat until done)
   ┌─────────────────────────────────────┐
   │ action = agent.get_action(obs)       │
   │  └─ Agent processes observation      │
   │  └─ Returns 0, 1, or 2               │
   └─────────────────────────────────────┘
                    │
                    ▼
   ┌─────────────────────────────────────┐
   │ obs, reward, done, info = env.step(action) │
   │  ├─ Validate action                 │
   │  ├─ Update position:                │
   │  │   · LEFT: pos -= step_size       │
   │  │   · STAY: pos unchanged          │
   │  │   · RIGHT: pos += step_size      │
   │  ├─ Clamp position to bounds        │
   │  ├─ Evaluate reward at (pos, t)     │
   │  ├─ cumulative_reward += reward     │
   │  ├─ timestep += 1                   │
   │  ├─ Append to history               │
   │  ├─ done = (timestep >= length)     │
   │  └─ Generate new observation        │
   └─────────────────────────────────────┘
                    │
                    ▼
          done == True?
           /         \
         No          Yes
          │           │
          └─(loop)    ▼
                  Return cumulative_reward
```

**Observation Generation Flow (called by reset() and step()):**
```
_get_observation() internal workflow:
1. Get current position, timestep from state
2. Calculate observation window: [position - radius, position + radius]
3. Generate n_gradient_samples points uniformly in window using np.linspace()
4. Clip sample positions to function bounds
5. Evaluate function at all sample positions: func.evaluate(positions, timestep)
6. Evaluate reward at current position: func.evaluate(position, timestep)
7. Build observation dict with all required keys
8. Return observation dict
```

**Convenience run() Method Flow:**
```
run(agent, render=False):
1. obs = reset()
2. While not done:
   a. action = agent.get_action(obs)
   b. obs, reward, done, info = step(action)
   c. If render and visualizer exists: visualizer.update(state)
3. Return state['cumulative_reward']
```

**Data Flow Diagram (text notation):**
```
Agent          Environment         Function2D
  │                  │                  │
  │   observation    │                  │
  │◄─────────────────┤                  │
  │                  │                  │
  │     action       │                  │
  ├─────────────────►│                  │
  │                  │  evaluate(x, t)  │
  │                  ├─────────────────►│
  │                  │   reward value   │
  │                  │◄─────────────────┤
  │                  │                  │
  │  (obs,r,done,i)  │                  │
  │◄─────────────────┤                  │
  │                  │                  │
```

## Non-Functional Requirements

### Performance

**NFR3: Fast Episode Execution (< 20s with visualization, < 2s headless)**
- **Target for Epic 2 (headless):** Complete 1000-timestep episode in < 2 seconds without rendering
- **Implementation:**
  - Efficient state updates using direct dict assignment (no copying)
  - NumPy vectorized gradient sampling (single function call for all samples)
  - Minimal object creation in hot path (reuse observation dict structure)
- **Measurement:** Use pytest-benchmark or timeit to validate 1000-step episodes
- **Story Coverage:** Story 2.6 implements run() method with performance validation

**NFR2: Efficient Function Evaluation (< 1ms)**
- **Dependency:** Relies on Epic 1's vectorized GaussianTranslation implementation
- **Epic 2 Usage:** Called twice per step - once for reward, once for gradient samples
- **Batch Efficiency:** Gradient sampling evaluates 20 points in single vectorized call (< 1ms total)

**NFR4: Batch Performance (100 episodes < 5 minutes headless)**
- **Epic 2 Enabler:** Headless mode (render_mode=False) disables all visualization overhead
- **Expected Performance:** 2s per episode × 100 = 200s = 3.3 minutes (within budget)
- **Story Coverage:** Story 2.2 implements render_mode flag

**Step Execution Performance:**
- **Target:** Single step() call completes in < 10ms (including observation generation)
- **Breakdown:**
  - Action validation: < 0.1ms (simple integer check)
  - Position update: < 0.1ms (arithmetic + np.clip)
  - Reward evaluation: < 1ms (single function call)
  - Gradient sampling: < 1ms (vectorized evaluation of 20 points)
  - Observation dict construction: < 0.5ms (dict creation)
  - History append: < 0.1ms (list append)
  - Total budget: ~3ms per step, well under 10ms target

### Security

**Not Applicable for Epic 2 (Research Library):**
- No authentication/authorization - local Python library
- No network communication - all computation local
- No user data handling - research experiments only
- No PII or sensitive data storage

**Input Validation (only security-relevant aspect):**
- Validate action is integer in range [0, 1, 2] to prevent undefined behavior
- ValueError raised with clear message if invalid action provided
- No SQL injection, XSS, or web-related vulnerabilities (not a web service)

### Reliability/Availability

**Deterministic Behavior (Critical for Scientific Reproducibility):**
- **NFR6: Deterministic Evolution** - Same seed produces identical episodes
- **Implementation:**
  - Function evolution uses seed from Epic 1 (GaussianTranslation constructor)
  - No random number generation in Environment class itself
  - State transitions are pure functions of (current_state, action)
  - float64 precision minimizes floating-point drift
- **Testing:** Story 2.8 includes determinism tests (same seed = same history)

**State Consistency:**
- State dict is single source of truth - never allow inconsistent state
- All state updates happen atomically within step() method
- No external mutation of state (return copies from get_history())
- Reset always returns to clean initial state (position=0, timestep=0, reward=0)

**Error Handling:**
- Invalid actions raise ValueError immediately (fail-fast)
- Clear error messages guide users to fix (Architecture NFR17)
- No silent failures or undefined behavior
- Episode cannot enter invalid state (done flag prevents post-episode steps)

**Graceful Degradation:**
- If render_mode=True but visualizer not available: warn user, continue headless
- Missing function.get_config() method: return empty dict for function_params
- No crash on edge cases (agent at bounds, episode_length=0, etc.)

### Observability

**Episode History Tracking (FR21):**
- **What:** Every step records (timestep, position, reward, action) tuple
- **Purpose:** Enables post-hoc analysis and replay without re-running episodes
- **Access:** get_history() returns complete episode history
- **Storage:** List of tuples in state['history'], cleared on reset()
- **Story Coverage:** Story 2.5 implements history tracking

**Configuration Accessibility (FR64):**
- **What:** get_config() exposes all environment parameters
- **Purpose:** Save experiment configuration for reproducible research
- **Format:** JSON-serializable dict for easy export
- **Includes:** episode_length, observation_radius, n_gradient_samples, step_size, function_params, bounds
- **Story Coverage:** Story 2.7 implements get_config()

**State Introspection:**
- Public state dict accessible as env.state for debugging
- Current position, timestep, cumulative_reward visible at any time
- Facilitates debugging agent behavior and validating episodes

**No Traditional Logging (Intentional):**
- Research library doesn't need application logs
- History tracking serves as event log
- Pytest captures test output for debugging
- Users can add custom logging in their agent implementations if needed

## Dependencies and Integrations

**Core Dependencies (from pyproject.toml):**

| Dependency | Version | Purpose | Used By |
|------------|---------|---------|---------|
| **numpy** | >=2.3.5 | Numerical computation, vectorized operations, float64 precision | `environment.py` (gradient sampling, position tracking, reward calculation) |
| **pygame-ce** | >=2.5.6 | Event handling (deferred to Epic 4 for rendering) | Future: `visualizer.py` integration (Story 2.2 sets up render_mode flag) |
| **Python** | >=3.9 | Runtime environment | All modules (type hints require 3.9+) |

**Development Dependencies:**
| Dependency | Version | Purpose |
|------------|---------|---------|
| **pytest** | >=8.0.0 | Test framework |
| **matplotlib** | >=3.10.7 | Optional analysis/plotting (not used in Epic 2) |

**Internal Module Dependencies (within FuncBench):**

```
Epic 2 Modules:
├── agent.py (no dependencies - pure ABC)
└── environment.py
    └── Depends on: function.py (from Epic 1)
        └── Requires: Function2D abstract base, evaluate() and get_perfect_score() methods

Test Modules:
├── test_environment.py
│   └── Depends on: environment.py, agent.py, function.py
└── conftest.py
    └── Provides fixtures: gaussian_function, environment, mock_agent
```

**Integration Points:**

**Epic 1 → Epic 2 Integration:**
- **Function2D interface**: Environment calls `function.evaluate(x, t)` for reward and gradient sampling
- **Perfect score**: Environment uses `function.get_perfect_score(episode_length)` for info dict
- **Bounds**: Environment uses `function.bounds` to clamp agent position
- **Contract**: Function must support vectorized evaluation (np.ndarray input)

**Epic 2 → Epic 4 Integration (Prepared but Not Implemented):**
- **render_mode flag**: Environment.__init__() accepts render_mode parameter
- **Visualizer placeholder**: Environment.run() has conditional visualizer.update() call
- **State exposure**: Environment can provide state dict for visualization
- **Actual integration**: Deferred to Epic 4 (Stories 4.7)

**Epic 2 → Epic 3 Integration (Interface Ready):**
- **Agent interface**: Epic 3 will implement RandomAgent, GreedyAgent using Agent ABC
- **Evaluation ready**: Environment.run() already supports any Agent implementation
- **History access**: get_history() enables Epic 3 analysis utilities

**No External API Dependencies:**
- No REST APIs, no database connections, no network calls
- Pure local Python computation
- No configuration files required (all config via constructor params)

## Acceptance Criteria (Authoritative)

**AC1: Agent Abstract Base Class Implemented**
- Agent ABC exists in `src/funcbench/agent.py`
- Contains abstract method `get_action(observation: dict) -> int`
- Action constants defined: ACTION_LEFT=0, ACTION_STAY=1, ACTION_RIGHT=2
- Type hints present on all method signatures
- NumPy-style docstrings explain observation dict structure

**AC2: Environment Initialization**
- Environment class exists in `src/funcbench/environment.py`
- __init__ accepts: function, episode_length, observation_radius, n_gradient_samples, step_size, render_mode
- Stores configuration as instance attributes
- Initializes internal state dict with position, timestep, cumulative_reward, history
- Default parameter values match Architecture specification

**AC3: Reset Functionality**
- reset() method returns initial observation dict
- Position initialized to 0.0 (center of typical bounds)
- Timestep initialized to 0
- Cumulative reward initialized to 0.0
- History list cleared to empty
- Observation dict contains all required keys: position, reward, gradient, gradient_positions, timestep

**AC4: Observation Generation**
- _get_observation() generates gradient samples within observation_radius
- Uses np.linspace for uniform sampling of n_gradient_samples points
- Clips sample positions to function bounds
- Evaluates function at all sample positions in single vectorized call
- Returns dict with position, reward, gradient, gradient_positions, timestep keys
- Gradient array shape is (n_gradient_samples,)
- All numeric values use float64 precision

**AC5: Step Execution**
- step(action) validates action is 0, 1, or 2 (raises ValueError otherwise)
- ACTION_LEFT: position decreases by step_size
- ACTION_STAY: position unchanged
- ACTION_RIGHT: position increases by step_size
- Position clamped to function bounds using np.clip
- Reward calculated at new position and current timestep
- Cumulative reward incremented by step reward
- Timestep incremented by 1
- Returns 4-tuple: (observation, reward, done, info)
- done=True when timestep >= episode_length
- info dict contains cumulative_reward and perfect_score

**AC6: Episode History Tracking**
- step() appends (timestep, position, reward, action) tuple to history
- History entries use immutable tuple format
- History stored in chronological order
- get_history() returns copy of history list (not reference)
- reset() clears history to empty list

**AC7: Run Method**
- run(agent, render) executes complete episode
- Calls reset() to initialize
- Loops calling agent.get_action() and step() until done
- Returns final cumulative_reward as float
- Completes 1000-step episode in < 2 seconds (headless mode)
- Handles agent exceptions gracefully with informative errors
- Placeholder for visualizer.update() when render=True

**AC8: Configuration Persistence**
- get_config() returns dict with episode_length, observation_radius, n_gradient_samples, step_size, function_params, bounds
- Returns copy of configuration (not mutable reference)
- Dict is JSON-serializable
- Function_params obtained from function if available

**AC9: Unit Tests Pass**
- test_environment_initialization validates constructor
- test_reset validates state reset
- test_step_actions validates all three actions (left, stay, right)
- test_step_return_signature validates 4-tuple return
- test_episode_completion validates done flag behavior
- test_cumulative_reward validates reward accumulation
- test_history_tracking validates history format and content
- test_invalid_action validates ValueError raised
- All tests pass with pytest
- Test coverage > 80% for environment.py

**AC10: Performance Targets Met**
- Single step() completes in < 10ms
- 1000-step episode (headless) completes in < 2 seconds
- Observation generation (gradient sampling) < 5ms
- All targets validated with pytest-benchmark or timeit

## Traceability Mapping

| AC | PRD FR(s) | Epic Story | Component/Module | Test Case |
|----|-----------|------------|------------------|-----------|
| AC1 | FR8-15 | 2.1 | Agent ABC in agent.py | test_agents.py::test_agent_interface |
| AC2 | FR16, FR59-61, FR63 | 2.2 | Environment.__init__ | test_environment.py::test_environment_initialization |
| AC3 | FR16, FR20 | 2.2 | Environment.reset() | test_environment.py::test_reset |
| AC4 | FR10-13 | 2.3 | Environment._get_observation() | test_environment.py::test_observation_generation |
| AC5 | FR8-9, FR14, FR17-19 | 2.4 | Environment.step() | test_environment.py::test_step_actions, test_step_return_signature |
| AC6 | FR21 | 2.5 | Environment history tracking | test_environment.py::test_history_tracking |
| AC7 | FR16-19 | 2.6 | Environment.run() | test_environment.py::test_run_method, test_integration.py::test_complete_episode |
| AC8 | FR64 | 2.7 | Environment.get_config() | test_environment.py::test_get_config |
| AC9 | Testing requirement | 2.8 | All test modules | pytest run (all tests) |
| AC10 | NFR2-4 | 2.4, 2.6 | Performance validation | test_environment.py::test_performance_targets |

**FR Coverage Summary for Epic 2:**
- FR8-FR15: Agent system ✓ (Story 2.1)
- FR16-FR22: Episode management ✓ (Stories 2.2-2.6)
- FR23-FR25: Scoring & evaluation ✓ (Stories 2.4, 2.6)
- FR59-FR61: Configuration (episode params) ✓ (Story 2.2)
- FR63-FR65: Configuration (headless mode, API) ✓ (Stories 2.2, 2.7)

**Story → AC → Test Traceability:**

| Story | Acceptance Criteria | Test Files |
|-------|---------------------|------------|
| 2.1 Agent Interface | AC1 | test_agents.py |
| 2.2 Environment Init/Reset | AC2, AC3 | test_environment.py |
| 2.3 Observation Generation | AC4 | test_environment.py |
| 2.4 Step Execution | AC5, AC10 | test_environment.py |
| 2.5 History Tracking | AC6 | test_environment.py |
| 2.6 Run Method | AC7, AC10 | test_environment.py, test_integration.py |
| 2.7 Configuration | AC8 | test_environment.py |
| 2.8 Unit Tests | AC9 | All test files |

## Risks, Assumptions, Open Questions

**Risks:**

**R1: Performance Degradation with Large Observation Radius**
- **Risk:** If observation_radius is very large, gradient sampling could slow down step execution
- **Likelihood:** Low (default is 20 samples, reasonable radius)
- **Impact:** Medium (violates NFR3 performance target)
- **Mitigation:** Document recommended observation_radius range (5-20), add performance tests for edge cases

**R2: Float64 Precision Drift Over Long Episodes**
- **Risk:** Cumulative reward could accumulate floating-point errors over 10,000+ timesteps
- **Likelihood:** Low (float64 has high precision)
- **Impact:** Low (NFR14 allows < 0.01% error over 10k steps)
- **Mitigation:** Use np.float64 explicitly, test with long episodes (10k steps)

**R3: Agent Implementation Errors Breaking Episode Loop**
- **Risk:** Poorly implemented agents could raise exceptions and crash episodes
- **Likelihood:** Medium (user-implemented agents)
- **Impact:** Medium (bad user experience)
- **Mitigation:** run() method catches agent exceptions, provides helpful error messages (AC7)

**Assumptions:**

**A1: Function Evaluation is Fast**
- **Assumption:** Function.evaluate() completes in < 1ms as implemented in Epic 1
- **Validation:** Epic 1 tests validate this, Epic 2 depends on it
- **Impact if False:** Cannot meet NFR3 (< 2s episodes)

**A2: Agents Don't Need Internal State Persistence**
- **Assumption:** Agent state lives in agent instance, not in Environment
- **Validation:** Agent interface is stateless from Environment perspective
- **Impact if False:** Would need to modify Agent interface to support save/load

**A3: 20 Gradient Samples is Sufficient Information**
- **Assumption:** 20 local function samples provide enough gradient information for learning
- **Validation:** Architecture decision, can be configured via n_gradient_samples
- **Impact if False:** Users can increase n_gradient_samples (configurable)

**A4: Headless Mode is Sufficient for Epic 2 Validation**
- **Assumption:** Visualization not needed to validate episode execution logic
- **Validation:** Unit tests cover all logic without rendering
- **Impact if False:** Would need Epic 4 visualization to complete Epic 2 (violates phased approach)

**Open Questions:**

**Q1: Should Environment Support Mid-Episode Serialization?**
- **Question:** Should we be able to save/load environment state mid-episode?
- **Current Decision:** No, out of scope for Epic 2
- **Deferred To:** Post-MVP if needed for advanced analysis
- **Rationale:** Episodes are fast enough to re-run, history tracking is sufficient

**Q2: Should Step Size be Configurable Per Action?**
- **Question:** Different step sizes for left vs right?
- **Current Decision:** No, single step_size parameter
- **Rationale:** Simplicity, symmetry, not required by PRD

**Q3: How to Handle episode_length=0 or Negative Values?**
- **Current Decision:** Allow it, done=True immediately on reset
- **Alternative:** Validate and raise ValueError
- **Resolution Needed:** During Story 2.2 implementation

## Test Strategy Summary

**Unit Testing Approach:**

**Test Organization:**
- `tests/test_environment.py`: Core environment functionality (reset, step, run, config)
- `tests/test_agents.py`: Agent interface and base class validation
- `tests/conftest.py`: Shared fixtures (functions, environments, mock agents)

**Key Test Categories:**

1. **Interface Contract Tests** (AC1, AC2)
   - Agent ABC enforces get_action() signature
   - Environment constructor accepts all required parameters
   - Type hints present and correct

2. **State Management Tests** (AC3, AC6)
   - Reset initializes state correctly
   - State updates are atomic and consistent
   - History tracking captures all steps
   - get_history() returns copy (not reference)

3. **Action Execution Tests** (AC5)
   - ACTION_LEFT decreases position by step_size
   - ACTION_STAY preserves position
   - ACTION_RIGHT increases position by step_size
   - Invalid actions raise ValueError with clear message
   - Position clamped to bounds correctly

4. **Observation Tests** (AC4)
   - Observation dict has all required keys
   - Gradient sampling uses np.linspace correctly
   - Sample positions clipped to bounds
   - Vectorized function evaluation called once
   - float64 precision maintained

5. **Episode Lifecycle Tests** (AC7)
   - reset → step loop → done sequence works
   - done=False until timestep >= episode_length
   - done=True when episode completes
   - run() method executes full episode
   - Cumulative reward matches sum of step rewards

6. **Performance Tests** (AC10)
   - pytest-benchmark for step() timing (< 10ms)
   - timeit for 1000-step episode (< 2s headless)
   - Observation generation (< 5ms)
   - Performance regression detection

7. **Reproducibility Tests** (NFR6)
   - Same function seed produces identical results
   - Same sequence of actions produces identical state
   - Episode history is deterministic

**Test Fixtures (conftest.py):**
```python
@pytest.fixture
def gaussian_function():
    """Standard Gaussian for testing."""
    return GaussianTranslation(velocity=0.1, sigma=1.0, amplitude=1.0, seed=42)

@pytest.fixture
def environment(gaussian_function):
    """Standard environment with default config."""
    return Environment(gaussian_function, episode_length=100)

@pytest.fixture
def mock_agent():
    """Simple mock agent that always goes right."""
    class MockAgent(Agent):
        def get_action(self, observation):
            return ACTION_RIGHT
    return MockAgent()
```

**Coverage Target:**
- **Minimum:** 80% line coverage for environment.py
- **Goal:** 90% coverage including edge cases
- **Exclusions:** Error handling paths that are hard to trigger

**Edge Cases to Test:**
- Agent at left bound, action=LEFT (should stay at bound)
- Agent at right bound, action=RIGHT (should stay at bound)
- episode_length=1 (single-step episode)
- observation_radius larger than bounds (gradient samples clipped)
- Function with asymmetric bounds

**Integration Testing:**
- test_integration.py validates complete episode with real function and mock agent
- Validates environment + agent + function integration
- Tests run() convenience method with different configurations

**Test Execution:**
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=funcbench --cov-report=html tests/

# Run performance tests only
pytest -k performance tests/

# Run specific test file
pytest tests/test_environment.py -v
```

**Continuous Integration:**
- All tests must pass before merging story branches
- Performance tests run on consistent hardware for reproducibility
- Coverage reports generated automatically

**Test Data Strategy:**
- Use pytest fixtures for reusable test objects
- Seed all random operations for deterministic tests
- Test with multiple function configurations (different velocities, sigmas)
- Validate behavior across Python 3.9, 3.10, 3.11, 3.12
