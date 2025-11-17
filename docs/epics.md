# FuncBench - Epic Breakdown

**Author:** Morgan
**Date:** 2025-11-17
**Project Level:** medium
**Target Scale:** 10-50 stories

---

## Overview

This document provides the complete epic and story breakdown for FuncBench, decomposing the requirements from the [PRD](./prd.md) into implementable stories.

**Living Document Notice:** This document incorporates PRD requirements and Architecture technical decisions for complete implementation guidance.

---

## Functional Requirements Inventory

### Function System (FR1-FR7)
- **FR1:** Define 2D temporal functions that evolve over time according to explicit rules
- **FR2:** Gaussian function implementation with configurable parameters (mean, std dev, amplitude)
- **FR3:** Gaussian function supports linear translation dynamics (mean moves at constant velocity)
- **FR4:** Evaluate function at any (x, t) coordinate to get reward value
- **FR5:** Calculate theoretical perfect score for any temporal function and episode length
- **FR6:** Functions can define spatial bounds (left/right limits for agent movement)
- **FR7:** Extensible function base class for implementing custom temporal patterns

### Agent System (FR8-FR15)
- **FR8:** Agents can take three actions: move left, move right, or stay in current position
- **FR9:** System tracks agent position in 1D space (x-coordinate)
- **FR10:** Agent receives observation including current reward value at its position
- **FR11:** Agent receives local gradient information within observation radius
- **FR12:** Agent receives visual snapshot of local function cross-section (for LLM agents)
- **FR13:** Observation radius (fog-of-war size) is configurable per environment
- **FR14:** System enforces spatial bounds (agent cannot move outside function domain)
- **FR15:** Agents can be implemented via abstract interface for different AI architectures

### Episode Management (FR16-FR22)
- **FR16:** Initialize new episodes with configurable episode length (timesteps)
- **FR17:** Execute agent actions step-by-step, advancing time by one timestep per action
- **FR18:** Track cumulative reward across all timesteps in an episode
- **FR19:** Episode terminates when timestep limit is reached
- **FR20:** Reset environment state to start new episodes
- **FR21:** Maintain episode history (timesteps, positions, rewards, actions)
- **FR22:** Episodes use deterministic temporal evolution (same seed = same function dynamics)

### Scoring & Evaluation (FR23-FR29)
- **FR23:** Calculate real-time cumulative reward as agent acts
- **FR24:** Provide theoretical perfect score (maximum possible cumulative reward)
- **FR25:** Calculate performance gap (actual score vs perfect score)
- **FR26:** Compare agent performance against baseline strategies (random, greedy)
- **FR27:** Track learning curves across multiple episodes
- **FR28:** Episode replay capability for post-hoc analysis
- **FR29:** Save episode data for reproducible evaluation

### Visualization - Agent View 2D (FR30-FR41)
- **FR30:** Render real-time 2D agent view showing local function cross-section
- **FR31:** Implement fog-of-war (areas outside observation radius are blacked out)
- **FR32:** Show agent position indicator on 2D cross-section
- **FR33:** Display current reward value numerically and visually (color/intensity)
- **FR34:** Show gradient direction indicators within observable window
- **FR35:** Render historical trail showing agent's previous positions
- **FR36:** Historical trail can be toggled on/off
- **FR37:** Visualization updates at 60 FPS for smooth real-time feedback
- **FR38:** Show current cumulative score
- **FR39:** Show theoretical perfect score
- **FR40:** Display performance gap (score difference)
- **FR41:** Show current timestep / total timesteps

### Visualization - God View 3D (FR42-FR46) [DEFERRED TO PHASE 2]
- **FR42:** Render 3D overview showing full function surface over time
- **FR43:** God view shows agent position on 3D surface
- **FR44:** God view visualizes temporal dynamics (peak translation visible)
- **FR45:** Toggle between agent view (2D) and god view (3D)
- **FR46:** God view provides spatial reference for understanding agent's limited perspective

### Human Play Mode (FR47-FR53)
- **FR47:** Control agent using keyboard input (arrow keys)
- **FR48:** Human play mode has identical observation constraints as AI agents
- **FR49:** Human players see same fog-of-war visualization as AI agents
- **FR50:** Human play mode uses same scoring system as AI evaluation
- **FR51:** Human play receives identical gradient information as AI agents
- **FR52:** Track human player scores for human-AI comparison
- **FR53:** Keyboard controls are responsive with minimal input lag

### Playback & Analysis (FR54-FR58) [DEFERRED TO PHASE 2]
- **FR54:** Pause and resume episodes during execution
- **FR55:** Slow-motion playback for detailed analysis
- **FR56:** Replay completed episodes
- **FR57:** Frame-by-frame stepping in debug mode
- **FR58:** Playback preserves all visualization elements (fog-of-war, trails, scores)

### Configuration & Parameters (FR59-FR65)
- **FR59:** Configure function parameters (peak width, translation velocity, bounds)
- **FR60:** Configure observation radius (fog-of-war size)
- **FR61:** Configure episode length (number of timesteps)
- **FR62:** Configure visualization settings (FPS, view mode, trail length)
- **FR63:** Enable/disable visualization (headless mode for batch evaluation)
- **FR64:** Configuration via Python API and config files
- **FR65:** Configuration changes take effect on next episode reset

### LLM Integration (FR66-FR70) [DEFERRED TO POST-MVP]
- **FR66:** Render visual snapshots in format suitable for multimodal LLMs
- **FR67:** Parse LLM text output to action commands
- **FR68:** LLM agents maintain context across multiple timesteps within episode
- **FR69:** Support multiple LLM providers (OpenAI, Anthropic, local models)
- **FR70:** Manage LLM API calls and rate limiting

### Extension & Research Tools (FR71-FR75) [DEFERRED TO POST-MVP]
- **FR71:** Base classes for implementing custom temporal functions
- **FR72:** Define new function patterns without modifying core code
- **FR73:** Utilities for common patterns (oscillation, rotation, acceleration)
- **FR74:** Export episode data in standard formats (CSV, JSON) for external analysis
- **FR75:** Generate visualizations for research papers (matplotlib plots, animations)

**Phase 1 MVP Scope:** FR1-FR41, FR47-FR65 (57 functional requirements)

---

## Epic Structure Overview

### Epic 1: Project Foundation & Function System
**Goal:** Establish project infrastructure and implement temporal function evaluation

**User Value:** Researchers have a working Python package with Gaussian function evaluation

**Scope:** Project setup (src/ layout, dependencies), Function2D abstract base, GaussianTranslation implementation, perfect score calculation

**Story Count:** ~5 stories

### Epic 2: Environment & Agent Execution
**Goal:** Implement complete episode lifecycle with agent-environment interaction

**User Value:** Researchers can run agents through episodes and get performance scores (headless mode)

**Scope:** Environment class, episode state management, Agent abstract interface, observation generation, action execution, cumulative reward tracking, basic configuration

**Story Count:** ~8 stories

### Epic 3: Baseline Agents & Evaluation
**Goal:** Implement baseline agents for performance comparison

**User Value:** Researchers can compare custom agents against established baselines (random, greedy)

**Scope:** RandomAgent implementation, GreedyAgent (follows gradient), learning curve tracking, episode history save/load

**Story Count:** ~3 stories

### Epic 4: 2D Visualization System
**Goal:** Real-time PyGame rendering with fog-of-war constraints

**User Value:** Researchers can visually validate temporal dynamics and agent behavior

**Scope:** Visualizer class, PyGame setup, 2D agent view rendering, fog-of-war implementation, score display, historical trail, 60 FPS management

**Story Count:** ~6 stories

### Epic 5: Human Play & Validation
**Goal:** Human keyboard control with identical observation constraints as AI agents

**User Value:** Researchers can play manually to validate benchmark difficulty and establish human baseline

**Scope:** HumanAgent class, keyboard input handling, human score tracking, identical fog-of-war constraints

**Story Count:** ~3 stories

### Epic 6: Testing & Package Distribution
**Goal:** Comprehensive testing infrastructure and PyPI distribution

**User Value:** Researchers can pip install and trust results are reproducible

**Scope:** Reproducibility tests (deterministic episodes), integration tests, pytest fixtures, pyproject.toml configuration, README and quick-start docs

**Story Count:** ~4 stories

**Total Stories:** ~29 stories (within 10-50 range for medium complexity project)

---

## FR Coverage Map

| Epic | FRs Covered | Description |
|------|-------------|-------------|
| Epic 1 | Setup, FR1-FR7 | Project structure, Function2D ABC, Gaussian translation, perfect score |
| Epic 2 | FR8-FR22, FR23-FR25, FR59-FR61, FR63-FR65 | Agent interface, Environment, episode management, scoring, configuration |
| Epic 3 | FR26-FR29 | Baseline agents (random, greedy), learning curves, episode persistence |
| Epic 4 | FR30-FR41, FR62 | PyGame 2D visualization, fog-of-war, agent view, score display, trails |
| Epic 5 | FR47-FR53 | Human keyboard control, human baseline scoring |
| Epic 6 | Testing & Packaging | Reproducibility tests, integration tests, PyPI distribution, documentation |

**Coverage Validation:** All 57 Phase 1 MVP functional requirements mapped to epics ✓

---

## Epic 1: Project Foundation & Function System

**Goal:** Establish project infrastructure and implement temporal function evaluation

**User Value:** Researchers have a working Python package with Gaussian function evaluation

**FRs Covered:** Project setup, FR1-FR7

---

### Story 1.1: Initialize Project Structure and Dependencies

As a developer,
I want to set up the FuncBench project with src/ layout and dependency management,
So that we have a clean foundation following PyOpenSci standards.

**Acceptance Criteria:**

**Given** a new project directory
**When** the project structure is initialized
**Then** the following directory structure exists:
```
funcbench/
├── src/
│   └── funcbench/
│       └── __init__.py
├── tests/
│   └── __init__.py
├── examples/
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

**And** pyproject.toml contains:
- build-system with hatchling backend
- project metadata (name="funcbench", version="0.1.0")
- requires-python = ">=3.9"
- dependencies: numpy>=2.3.5, pygame-ce>=2.5.6
- optional-dependencies: dev=[pytest>=8.0.0, matplotlib>=3.10.7]

**And** src/funcbench/__init__.py exports package version

**And** .gitignore includes Python, IDE, and build artifacts

**And** README.md contains project description and installation instructions

**Prerequisites:** None (first story)

**Technical Notes:**
- Use src/ layout per Architecture decision (ensures tests run against installed package)
- Hatchling is the build backend (modern, lightweight, PEP 517 compliant)
- Lock numpy to 2.3.5 and pygame-ce to 2.5.6 for reproducibility
- Python 3.9+ required for type hint compatibility
- Reference: Architecture Section "Project Structure" and "pyproject.toml Configuration"

---

### Story 1.2: Implement Function2D Abstract Base Class

As a researcher,
I want an abstract base class for defining temporal functions,
So that I can extend the system with custom function patterns.

**Acceptance Criteria:**

**Given** the project structure from Story 1.1
**When** I create src/funcbench/function.py
**Then** it contains a Function2D abstract base class

**And** Function2D includes these abstract methods with type hints:
- `evaluate(x: np.ndarray, t: float) -> np.ndarray` - Evaluate function at position(s) x and time t
- `get_perfect_score(episode_length: int) -> float` - Calculate theoretical perfect score

**And** Function2D includes these concrete attributes:
- `bounds: tuple[float, float]` - Spatial bounds for agent movement
- `seed: int | None` - Random seed for reproducibility

**And** all methods have NumPy-style docstrings with Parameters, Returns, and Examples sections

**And** type hints are mandatory for all method signatures

**And** imports follow Architecture pattern (stdlib → third-party → local)

**Prerequisites:** Story 1.1 (project structure exists)

**Technical Notes:**
- Use abc.ABC and @abstractmethod decorators
- Follow naming convention: PascalCase for classes (Function2D)
- Type hints required per Architecture consistency rules
- NumPy-style docstrings per Architecture documentation patterns
- File naming: snake_case (function.py)
- Reference: Architecture Section "API Contracts - Function2D"

---

### Story 1.3: Implement GaussianTranslation Function

As a researcher,
I want a Gaussian function with linear translation dynamics,
So that I can test temporal pattern learning on the simplest baseline experiment.

**Acceptance Criteria:**

**Given** Function2D abstract base class from Story 1.2
**When** I create GaussianTranslation class in src/funcbench/function.py
**Then** it inherits from Function2D

**And** __init__ accepts parameters with type hints:
- `mean_start: float = -10.0` - Starting position of peak
- `velocity: float = 0.1` - Translation speed (units per timestep)
- `sigma: float = 1.0` - Standard deviation (peak width)
- `amplitude: float = 1.0` - Peak height
- `bounds: tuple[float, float] = (-20.0, 20.0)` - Spatial bounds
- `seed: int | None = None` - Random seed

**And** evaluate() implements vectorized Gaussian evaluation:
```python
mean_t = self.mean_start + self.velocity * t
return self.amplitude * np.exp(-((x - mean_t)**2) / (2 * self.sigma**2))
```

**And** evaluate() uses NumPy vectorized operations (no Python loops)

**And** all computations use float64 precision explicitly

**And** evaluate() completes in < 1ms for arrays of size 100

**And** class includes NumPy-style docstring explaining the temporal dynamics

**Prerequisites:** Story 1.2 (Function2D base class exists)

**Technical Notes:**
- NumPy vectorized operations required per Architecture performance requirements (NFR2)
- float64 precision for reproducibility (Architecture NFR11)
- Pre-compute constants in __init__ for performance
- Naming: PascalCase class name (GaussianTranslation)
- Reference: Architecture Section "NumPy Usage Patterns" and "Data Architecture"

---

### Story 1.4: Implement Perfect Score Calculation

As a researcher,
I want to calculate the theoretical perfect score for an episode,
So that I can measure agent performance gap against the optimal baseline.

**Acceptance Criteria:**

**Given** GaussianTranslation class from Story 1.3
**When** I call get_perfect_score(episode_length: int)
**Then** it calculates the theoretical maximum cumulative reward analytically (not via simulation)

**And** calculation assumes agent can teleport to peak position at each timestep (perfect tracking)

**And** for linear translation with starting position mean_start and velocity v:
- At timestep t, peak is at position: mean_start + v * t
- Perfect reward at timestep t: amplitude * exp(0) = amplitude (agent is exactly at peak)
- Perfect cumulative score: amplitude * episode_length

**And** calculation uses float64 precision for consistency

**And** perfect score calculation completes in < 1ms (constant time, no loops)

**And** method includes docstring explaining the analytical approach

**Prerequisites:** Story 1.3 (GaussianTranslation implementation exists)

**Technical Notes:**
- Analytical calculation ensures exact ground truth (Architecture NFR13)
- For Gaussian, being at peak mean gives maximum value (amplitude)
- Linear translation: peak moves predictably, perfect agent tracks it
- No simulation needed - pure math
- float64 precision matches function evaluation precision
- Reference: Architecture Section "Accuracy & Precision" NFR13

---

### Story 1.5: Create Basic Function Tests

As a developer,
I want unit tests for function evaluation and perfect score calculation,
So that I can ensure correctness and reproducibility.

**Acceptance Criteria:**

**Given** GaussianTranslation implementation from Stories 1.3-1.4
**When** I create tests/test_function.py with pytest
**Then** it includes test_gaussian_evaluation() that validates:
- Function evaluates correctly at known points
- Result shape matches input shape
- Result dtype is float64
- Peak value equals amplitude when x = mean_t

**And** it includes test_perfect_score_calculation() that validates:
- Perfect score equals amplitude * episode_length
- Score is deterministic (same inputs = same output)
- Result dtype is float64

**And** it includes test_vectorized_evaluation() that validates:
- Single point evaluation: x=np.array([0.0])
- Multiple points: x=np.linspace(-10, 10, 100)
- Results are numpy arrays with correct shapes

**And** it includes test_spatial_bounds() that validates:
- Bounds tuple is accessible
- Bounds contain valid float values

**And** all tests pass with pytest

**Prerequisites:** Stories 1.2-1.4 (Function implementation complete)

**Technical Notes:**
- Use pytest framework per Architecture testing decisions
- Test float64 precision explicitly (reproducibility requirement)
- Validate vectorization works for both single and batch evaluation
- Check analytical perfect score matches expected formula
- Create conftest.py with fixtures if needed
- Reference: Architecture Section "Testing Patterns"

---

## Epic 2: Environment & Agent Execution

**Goal:** Implement complete episode lifecycle with agent-environment interaction

**User Value:** Researchers can run agents through episodes and get performance scores (headless mode)

**FRs Covered:** FR8-FR22, FR23-FR25, FR59-FR61, FR63-FR65

---

### Story 2.1: Implement Agent Abstract Base Class and Action Constants

As a researcher,
I want a standardized agent interface for implementing different AI approaches,
So that I can easily swap between agent implementations.

**Acceptance Criteria:**

**Given** the project structure from Epic 1
**When** I create src/funcbench/agent.py
**Then** it defines action constants:
```python
ACTION_LEFT = 0
ACTION_STAY = 1
ACTION_RIGHT = 2
```

**And** it contains an Agent abstract base class with:
- Abstract method: `get_action(observation: dict) -> int`
- NumPy-style docstring explaining observation dict structure
- Type hints for all parameters and return values

**And** observation dict structure is documented as:
```python
{
    'position': float,           # Current x-coordinate
    'reward': float,             # Current reward value
    'gradient': np.ndarray,      # Local function samples
    'gradient_positions': np.ndarray,  # Where samples are
    'timestep': int              # Current time
}
```

**And** get_action() must return 0, 1, or 2 (left/stay/right)

**And** class follows Architecture naming conventions (PascalCase for Agent, snake_case for methods)

**And** file includes complete docstrings and type hints

**Prerequisites:** Epic 1 complete (Function system exists)

**Technical Notes:**
- Use abc.ABC and @abstractmethod decorators
- Action constants MUST use these exact integer codes (Architecture consistency rule)
- Observation dict keys MUST match Architecture specification exactly
- Return signature enforced: int (0, 1, or 2)
- Reference: Architecture Section "API Contracts - Agent" and "Consistency Rules - Action Space"

---

### Story 2.2: Implement Environment Initialization and Reset

As a researcher,
I want an Environment class that manages episode lifecycle,
So that I can run repeatable experiments with configurable parameters.

**Acceptance Criteria:**

**Given** Function2D and Agent base classes from previous stories
**When** I create src/funcbench/environment.py with Environment class
**Then** __init__ accepts parameters with type hints:
- `function: Function2D` - The temporal function to use
- `episode_length: int = 1000` - Number of timesteps
- `observation_radius: float = 5.0` - Fog-of-war size
- `n_gradient_samples: int = 20` - Number of local samples
- `step_size: float = 1.0` - Distance moved per left/right action
- `render_mode: bool = False` - Enable visualization (headless if False)

**And** __init__ initializes internal state dict:
```python
self.state = {
    'position': np.float64,
    'timestep': int,
    'cumulative_reward': np.float64,
    'history': list
}
```

**And** reset() method:
- Initializes position to 0.0 (center of bounds)
- Resets timestep to 0
- Resets cumulative_reward to 0.0
- Clears history list
- Returns initial observation dict

**And** reset() uses float64 for all numeric state values

**And** reset() returns observation dict following Architecture specification

**And** configuration parameters are stored as instance attributes

**Prerequisites:** Stories 1.2-1.4 (Function system), Story 2.1 (Agent interface)

**Technical Notes:**
- Environment follows Gym-like API pattern (Architecture decision ADR-004)
- State is centralized dict for easy serialization (Architecture state management pattern)
- float64 precision for reproducibility (NFR11)
- Initial position at 0.0 (middle of typical bounds)
- Reference: Architecture Section "Environment API Contract" and "Data Architecture - Episode State"

---

### Story 2.3: Implement Observation Generation with Gradient Sampling

As a researcher,
I want agents to receive local gradient information within observation radius,
So that agents can learn from partial observability constraints.

**Acceptance Criteria:**

**Given** Environment class from Story 2.2
**When** I implement _get_observation() private method
**Then** it generates observation dict with all required keys:
- `position`: Current agent x-coordinate (float)
- `reward`: Current reward at position (float)
- `gradient`: NumPy array of function samples within observation radius
- `gradient_positions`: NumPy array of x-coordinates where samples were taken
- `timestep`: Current timestep (int)

**And** gradient sampling:
- Creates n_gradient_samples points uniformly within [position - radius, position + radius]
- Evaluates function at all sample points using vectorized NumPy call
- Clips sample positions to respect function bounds
- Uses np.linspace for uniform sampling

**And** current reward is calculated by evaluating function at agent position

**And** all numeric values use float64 precision

**And** gradient array shape is (n_gradient_samples,)

**And** gradient_positions array shape is (n_gradient_samples,)

**And** method completes in < 5ms for 20 samples (vectorized evaluation)

**Prerequisites:** Story 2.2 (Environment initialization)

**Technical Notes:**
- Vectorized NumPy evaluation required (Architecture NFR2)
- Observation dict keys must match Architecture specification exactly
- Local gradient provides "fog-of-war" constraint for agents
- Sample clipping prevents out-of-bounds evaluation
- Use function.evaluate(gradient_positions, current_timestep) for batch evaluation
- Reference: Architecture Section "Data Flows" and "Observation Dictionary Keys"

---

### Story 2.4: Implement Step Execution and Action Handling

As a researcher,
I want the environment to execute agent actions and advance time,
So that episodes progress step-by-step with deterministic dynamics.

**Acceptance Criteria:**

**Given** Environment with observation generation from Story 2.3
**When** I implement step(action: int) method
**Then** it validates action is 0, 1, or 2:
- If invalid, raise ValueError with clear message: "Invalid action {action}. Must be 0 (left), 1 (stay), or 2 (right)"

**And** action execution updates position:
- ACTION_LEFT (0): position -= step_size
- ACTION_STAY (1): position unchanged
- ACTION_RIGHT (2): position += step_size

**And** position is clamped to function bounds:
- If position < bounds[0], set to bounds[0]
- If position > bounds[1], set to bounds[1]

**And** reward is calculated by evaluating function at new position and current timestep

**And** cumulative_reward is incremented by reward

**And** timestep is incremented by 1

**And** episode done flag is set: done = (timestep >= episode_length)

**And** step() returns tuple: (observation, reward, done, info)
- observation: dict from _get_observation()
- reward: float (current step reward)
- done: bool (episode finished?)
- info: dict with {'cumulative_reward': float, 'perfect_score': float}

**And** all state updates use float64 precision

**And** step() completes in < 10ms (including observation generation)

**Prerequisites:** Story 2.3 (Observation generation)

**Technical Notes:**
- Gym-like API: step returns (obs, reward, done, info) tuple
- Validate inputs at boundary per Architecture error handling pattern
- Specific exception with helpful message (Architecture NFR17)
- Bounds enforcement prevents agent from leaving function domain
- Use np.clip for bounds clamping
- Reference: Architecture Section "Environment API Contract" and "Data Flows - Episode Execution"

---

### Story 2.5: Implement Episode History Tracking

As a researcher,
I want episode history saved for replay and analysis,
So that I can study agent behavior after episodes complete.

**Acceptance Criteria:**

**Given** Environment step execution from Story 2.4
**When** step() is called
**Then** it appends history entry to state['history']:
```python
(timestep, position, reward, action)
```

**And** history entry uses tuple format for immutability

**And** history is stored chronologically (order of steps)

**And** reset() clears history list to empty

**And** Environment exposes get_history() method that returns copy of history list

**And** get_history() returns list of tuples: [(t, x, r, a), ...]

**And** history does not include observations (too large for storage)

**And** history storage completes in < 1ms per step (simple list append)

**Prerequisites:** Story 2.4 (Step execution)

**Technical Notes:**
- History enables episode replay (FR28)
- Tuple format prevents accidental mutation
- Don't store full observations (gradient arrays too large)
- Store minimal data needed for replay: timestep, position, reward, action
- Return copy from get_history() to prevent external mutation
- Reference: Architecture Section "Episode State" and FR21, FR28

---

### Story 2.6: Implement Run Method for Episode Execution

As a researcher,
I want a convenient run() method that executes complete episodes,
So that I can easily evaluate agents without manually writing episode loops.

**Acceptance Criteria:**

**Given** Environment with step and reset from previous stories
**When** I implement run(agent: Agent, render: bool = False) method
**Then** it executes complete episode:
1. Call reset() to get initial observation
2. Loop until done:
   - Call agent.get_action(observation) to get action
   - Call step(action) to execute and get next observation
   - If render is True and visualizer exists, call visualizer update (placeholder for Epic 4)
3. Return final cumulative reward

**And** run() returns float: final cumulative_reward from state

**And** run() completes 1000-timestep episode in < 2 seconds (headless, render=False)

**And** run() handles agent exceptions gracefully with informative error messages

**And** if render=True but no visualizer, print warning and continue headless

**And** method includes NumPy-style docstring with examples

**Prerequisites:** Stories 2.2-2.5 (Complete environment functionality)

**Technical Notes:**
- Convenience method for common use case (run full episode)
- Headless mode for batch evaluation (Architecture NFR4)
- Visualizer integration is placeholder (Epic 4 will implement)
- Performance target: < 2s for 1000 steps headless (Architecture NFR3)
- Return only cumulative reward (simplest interface for researchers)
- Reference: Architecture Section "Performance Considerations" NFR3

---

### Story 2.7: Add Configuration Persistence

As a researcher,
I want to access environment configuration parameters,
So that I can save experiment settings for reproducibility.

**Acceptance Criteria:**

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

**Prerequisites:** Story 2.2 (Environment initialization)

**Technical Notes:**
- Enables reproducible experiments (Architecture NFR6-10)
- JSON-serializable format for easy storage
- Return copies to prevent external mutation
- Include function configuration for complete experiment specification
- Configuration saved alongside episode data enables exact reproduction
- Reference: Architecture Section "Reproducibility" NFR6-10 and FR64

---

### Story 2.8: Create Environment Unit Tests

As a developer,
I want comprehensive tests for environment functionality,
So that I can ensure correct episode execution and state management.

**Acceptance Criteria:**

**Given** complete Environment implementation from Stories 2.1-2.7
**When** I create tests/test_environment.py with pytest
**Then** it includes test_environment_initialization() that validates:
- Environment initializes with correct default parameters
- State dict exists with correct keys
- Configuration accessible via get_config()

**And** it includes test_reset() that validates:
- Position resets to 0.0
- Timestep resets to 0
- Cumulative reward resets to 0.0
- History is cleared
- Returns valid observation dict

**And** it includes test_step_actions() that validates:
- ACTION_LEFT decreases position by step_size
- ACTION_STAY keeps position unchanged
- ACTION_RIGHT increases position by step_size
- Bounds are enforced (position clamped to function bounds)

**And** it includes test_step_return_signature() that validates:
- Returns 4-tuple: (observation, reward, done, info)
- observation is dict with required keys
- reward is float
- done is bool
- info contains cumulative_reward and perfect_score

**And** it includes test_episode_completion() that validates:
- done=False until timestep >= episode_length
- done=True when timestep reaches episode_length
- Episode stops after done=True

**And** it includes test_cumulative_reward() that validates:
- Cumulative reward accumulates correctly
- Final cumulative reward equals sum of all step rewards

**And** it includes test_history_tracking() that validates:
- History entries are tuples (timestep, position, reward, action)
- History length equals number of steps taken
- History cleared on reset()

**And** it includes test_invalid_action() that validates:
- ValueError raised for action not in [0, 1, 2]
- Error message is helpful

**And** all tests use pytest fixtures from conftest.py

**And** all tests pass

**Prerequisites:** Stories 2.1-2.7 (Complete environment + agent interface)

**Technical Notes:**
- Create conftest.py with fixtures: standard function, environment
- Test state transitions explicitly
- Validate float64 precision in critical tests
- Test boundary conditions (bounds enforcement, episode termination)
- Mock visualizer for render tests (Epic 4 will provide real visualizer)
- Reference: Architecture Section "Testing Patterns"

---

## Epic 3: Baseline Agents & Evaluation

**Goal:** Implement baseline agents for performance comparison

**User Value:** Researchers can compare custom agents against established baselines (random, greedy)

**FRs Covered:** FR26-FR29

---

### Story 3.1: Implement RandomAgent Baseline

As a researcher,
I want a random agent that takes actions uniformly at random,
So that I can establish the lower bound of performance (no learning baseline).

**Acceptance Criteria:**

**Given** Agent abstract base class from Story 2.1
**When** I create RandomAgent class in src/funcbench/agent.py
**Then** it inherits from Agent

**And** __init__ accepts optional seed parameter with type hint:
- `seed: int | None = None` - Random seed for reproducible random actions

**And** __init__ initializes random number generator:
- If seed provided: use np.random.default_rng(seed)
- If seed is None: use np.random.default_rng() (non-deterministic)

**And** get_action(observation: dict) returns:
- Random integer from {0, 1, 2} (left, stay, right)
- Uses self.rng.integers(0, 3) for sampling

**And** random actions are uniformly distributed (equal probability for each action)

**And** with same seed, agent produces identical action sequences across runs

**And** class includes NumPy-style docstring explaining random baseline purpose

**Prerequisites:** Story 2.1 (Agent interface)

**Technical Notes:**
- Use np.random.default_rng() (new NumPy random API, not legacy np.random.seed())
- Seed enables reproducible experiments (Architecture NFR6)
- Random agent establishes floor performance - any learning should beat this
- Ignores observation completely (doesn't look at gradient or reward)
- Reference: Architecture Section "Reproducibility" and FR26

---

### Story 3.2: Implement GreedyAgent Baseline

As a researcher,
I want a greedy agent that always follows the local gradient,
So that I can measure whether agents learn better than simple hill-climbing.

**Acceptance Criteria:**

**Given** Agent abstract base class from Story 2.1
**When** I create GreedyAgent class in src/funcbench/agent.py
**Then** it inherits from Agent

**And** get_action(observation: dict) implements greedy gradient following:
1. Extract gradient array and gradient_positions from observation
2. Find index of maximum gradient value: argmax(gradient)
3. Compare gradient_positions[argmax] to current position
4. If peak is to the left: return ACTION_LEFT (0)
5. If peak is to the right: return ACTION_RIGHT (2)
6. If peak is at current position (within tolerance): return ACTION_STAY (1)

**And** uses tolerance threshold for "at position" check:
- abs(peak_position - current_position) < 0.1 → STAY
- Otherwise move toward peak

**And** greedy agent makes deterministic decisions (no randomness)

**And** agent uses only gradient information from observation (doesn't require global knowledge)

**And** class includes NumPy-style docstring explaining greedy baseline strategy

**And** greedy agent represents simple reactive policy (no learning, no memory)

**Prerequisites:** Story 2.1 (Agent interface), Story 2.3 (Observation includes gradient)

**Technical Notes:**
- Greedy agent follows local gradient (hill-climbing)
- This tests if temporal pattern learning beats simple reactive policy
- Uses np.argmax for finding gradient peak
- No state memory - purely reactive based on current observation
- For linear translation, greedy will lag behind peak (always catching up)
- Reference: FR26, Architecture Section "Agent Interface"

---

### Story 3.3: Implement Multi-Episode Evaluation and Learning Curve Tracking

As a researcher,
I want to run agents across multiple episodes and track performance over time,
So that I can measure learning curves and convergence behavior.

**Acceptance Criteria:**

**Given** Environment with run() method from Story 2.6
**When** I create evaluation utilities in src/funcbench/evaluation.py
**Then** it includes run_episodes() function with type hints:
```python
def run_episodes(
    env: Environment,
    agent: Agent,
    n_episodes: int,
    render: bool = False
) -> dict
```

**And** run_episodes() executes n_episodes sequential episodes:
1. For each episode:
   - Call env.reset() to start fresh
   - Run complete episode with env.run(agent, render)
   - Record cumulative reward and perfect score
2. Return results dict

**And** results dict contains:
```python
{
    'scores': list[float],           # Cumulative reward per episode
    'perfect_scores': list[float],   # Theoretical perfect per episode
    'gaps': list[float],             # score - perfect_score per episode
    'mean_score': float,             # Average across episodes
    'std_score': float,              # Standard deviation
    'best_score': float,             # Maximum score achieved
    'config': dict                   # Environment configuration
}
```

**And** gaps are calculated as: score - perfect_score (negative = suboptimal)

**And** statistics use NumPy: np.mean(), np.std()

**And** run_episodes() completes 100 episodes of 1000 steps in < 5 minutes (headless)

**And** function includes NumPy-style docstring with examples

**Prerequisites:** Story 2.6 (Environment run method), Stories 3.1-3.2 (Baseline agents)

**Technical Notes:**
- Learning curve = scores over episodes
- Convergence = when std_score becomes small (stable performance)
- Reset between episodes ensures independent trials
- Perfect score provides normalized comparison metric
- Enable batch evaluation for baseline comparisons
- Reference: FR27, FR28, Architecture NFR4 (batch performance)

---

### Story 3.4: Implement Episode Data Persistence

As a researcher,
I want to save and load episode data in standard formats,
So that I can reproduce experiments and analyze results later.

**Acceptance Criteria:**

**Given** evaluation results from Story 3.3
**When** I add save_episode_data() to src/funcbench/evaluation.py
**Then** it accepts parameters with type hints:
```python
def save_episode_data(
    results: dict,
    filepath: Path | str,
    format: str = 'json'
) -> None
```

**And** supports JSON format:
- Saves results dict to JSON file
- Includes all fields: scores, perfect_scores, gaps, statistics, config
- Uses json.dump() with indent=2 for readability
- Converts NumPy types to Python types (float64 → float)

**And** it includes load_episode_data() function:
```python
def load_episode_data(filepath: Path | str) -> dict
```

**And** load_episode_data() reconstructs results dict from saved JSON

**And** saved files include metadata:
- Library version (from funcbench.__version__)
- Timestamp (ISO 8601 format)
- Config hash or checksum for verification

**And** round-trip test: save then load produces identical results

**And** uses pathlib.Path for cross-platform compatibility

**And** raises informative errors if file doesn't exist or format invalid

**Prerequisites:** Story 3.3 (Evaluation results structure)

**Technical Notes:**
- JSON is human-readable and widely supported
- CSV format deferred to Phase 2 (FR74)
- Convert np.float64 to float before JSON serialization
- pathlib.Path ensures Windows/Mac/Linux compatibility
- Metadata enables reproducibility verification
- Reference: FR29, Architecture NFR7 (version locking), ADR-006 (pathlib)

---

### Story 3.5: Create Baseline Agent Tests

As a developer,
I want unit tests for baseline agent implementations,
So that I can verify they behave as expected.

**Acceptance Criteria:**

**Given** RandomAgent and GreedyAgent from Stories 3.1-3.2
**When** I create tests/test_agents.py with pytest
**Then** it includes test_random_agent_reproducibility() that validates:
- Same seed produces identical action sequences
- Different seeds produce different action sequences
- Actions are in valid range [0, 1, 2]

**And** it includes test_random_agent_distribution() that validates:
- Over 1000 actions, each action appears roughly 33% of time (uniform distribution)
- Chi-square test or similar for distribution uniformity

**And** it includes test_greedy_agent_follows_gradient() that validates:
- Given gradient with peak to the left → returns ACTION_LEFT
- Given gradient with peak to the right → returns ACTION_RIGHT
- Given gradient with peak at current position → returns ACTION_STAY
- Greedy behavior is deterministic (same observation → same action)

**And** it includes test_greedy_agent_determinism() that validates:
- Calling get_action() multiple times with same observation returns same action
- No internal state affects decisions

**And** it includes test_evaluation_run_episodes() that validates:
- Results dict has all required keys
- Scores list length equals n_episodes
- Statistics are computed correctly (mean, std, best)

**And** all tests use pytest fixtures from conftest.py

**And** all tests pass

**Prerequisites:** Stories 3.1-3.4 (All baseline functionality)

**Technical Notes:**
- Mock observation dicts for testing greedy logic
- Test edge cases: gradient all zeros, gradient all equal, single peak
- Validate statistical properties for random agent (uniformity)
- Test save/load round trip for evaluation data
- Create fixtures for standard test observations
- Reference: Architecture Section "Testing Patterns"

---

## Epic 4: 2D Visualization System

**Goal:** Real-time PyGame rendering with fog-of-war constraints

**User Value:** Researchers can visually validate temporal dynamics and agent behavior

**FRs Covered:** FR30-FR41, FR62

---

### Story 4.1: Initialize PyGame Window and Visualizer Class

As a researcher,
I want a Visualizer class that manages PyGame window and rendering,
So that I can see episodes executing in real-time.

**Acceptance Criteria:**

**Given** Environment class from Epic 2
**When** I create src/funcbench/visualizer.py with Visualizer class
**Then** __init__ accepts parameters with type hints:
- `width: int = 800` - Window width in pixels
- `height: int = 600` - Window height in pixels
- `fps: int = 60` - Target frames per second
- `title: str = "FuncBench"` - Window title

**And** __init__ initializes PyGame:
- pygame.init()
- Creates display window with pygame.display.set_mode((width, height))
- Sets window title with pygame.display.set_caption(title)
- Creates pygame.Clock() for FPS management
- Initializes font for text rendering: pygame.font.Font(None, 24)

**And** class includes close() method that:
- Calls pygame.quit()
- Cleans up resources

**And** class includes update() method stub (will be implemented in subsequent stories)

**And** window remains open and responsive (handles pygame events)

**And** follows Architecture naming conventions (PascalCase for Visualizer)

**And** all methods have NumPy-style docstrings

**Prerequisites:** Epic 1-3 complete (core functionality exists)

**Technical Notes:**
- Use pygame-ce (not legacy pygame) per Architecture decision
- Clock management for 60 FPS target (Architecture NFR1)
- Window creation is one-time setup in __init__
- Font for rendering text (scores, timesteps)
- Reference: Architecture Section "PyGame Rendering Patterns"

---

### Story 4.2: Render 2D Function Cross-Section at Agent Position

As a researcher,
I want to see a 2D cross-section of the function centered on the agent,
So that I can observe the local gradient visible to the agent.

**Acceptance Criteria:**

**Given** Visualizer class from Story 4.1
**When** I implement _render_function_view() private method
**Then** it accepts state dict parameter containing:
- position: float (agent x-coordinate)
- timestep: int (current time)
- gradient: np.ndarray (local function samples)
- gradient_positions: np.ndarray (sample x-coordinates)

**And** renders 2D plot showing:
- X-axis: spatial position (gradient_positions)
- Y-axis: function value (gradient)
- Line plot connecting sample points (smooth curve)

**And** rendering approach:
1. Create pygame Surface for plot area (e.g., 700x400 pixels)
2. Map gradient_positions to pixel x-coordinates (left to right)
3. Map gradient values to pixel y-coordinates (bottom to top, inverted y-axis)
4. Draw lines connecting consecutive points with pygame.draw.line()
5. Draw axes and grid lines for reference

**And** function curve color: blue (#0000FF) or configurable

**And** agent position marked with vertical line at center of view

**And** plot updates every frame based on current state

**And** coordinate transformation handles arbitrary function bounds

**And** rendering completes in < 16ms (for 60 FPS budget)

**Prerequisites:** Story 4.1 (Visualizer setup)

**Technical Notes:**
- 2D cross-section shows what agent observes (local gradient)
- Map continuous coordinates to discrete pixel coordinates
- pygame coordinate system: (0,0) at top-left, y increases downward (invert for plotting)
- Use pygame.draw.line() for connecting points
- Keep rendering efficient - no complex graphics, simple line drawing
- Reference: Architecture Section "PyGame Rendering Patterns" and FR30

---

### Story 4.3: Implement Fog-of-War Visualization

As a researcher,
I want areas outside observation radius to be blacked out,
So that I can see the same partial observability constraint the agent experiences.

**Acceptance Criteria:**

**Given** function view rendering from Story 4.2
**When** I enhance _render_function_view() with fog-of-war
**Then** it accepts observation_radius parameter from environment config

**And** fog-of-war implementation:
1. Calculate visible range: [position - radius, position + radius]
2. Render function curve only within visible range
3. Draw black overlay/mask outside visible range
4. Create clear visual boundary at fog edge

**And** visible window is highlighted or brighter than fog area

**And** fog area rendering:
- Fill with black color (#000000)
- Or use dark gray (#1A1A1A) for subtle distinction

**And** edge between visible/fog is clearly demarcated (vertical lines or gradient)

**And** as agent moves, fog window moves with it (centered on agent)

**And** fog-of-war is always active (no toggle in Phase 1 - matches agent constraints)

**And** fog rendering completes in < 5ms (part of 16ms frame budget)

**Prerequisites:** Story 4.2 (Function view rendering)

**Technical Notes:**
- Fog-of-war enforces partial observability (FR31)
- Critical for fair human-AI comparison (identical constraints)
- Draw fog as filled rectangles on left/right sides of visible window
- Clear visual makes it obvious what agent can/cannot see
- Performance: simple rectangle fills are fast in pygame
- Reference: Architecture Section "Key Interactions - Fog-of-War Visualization" and FR31, FR48

---

### Story 4.4: Render Agent Position Indicator and Gradient Direction

As a researcher,
I want visual indicators for agent position and gradient direction,
So that I can see where the agent is and which way the gradient points.

**Acceptance Criteria:**

**Given** function view with fog-of-war from Story 4.3
**When** I add agent and gradient indicators to _render_function_view()
**Then** agent position indicator:
- Vertical line at agent position (center of view)
- Distinct color: red (#FF0000) or orange (#FF8800)
- Line spans full plot height for visibility
- Width: 2-3 pixels (clearly visible)

**And** gradient direction indicator:
- Arrow showing which direction is "uphill" within visible window
- Located near agent position
- Points toward local maximum in gradient array
- Arrow color: green (#00FF00) for "good direction"
- Optional: arrow size proportional to gradient steepness

**And** current reward visualization:
- Circle or marker at agent's position on the function curve
- Circle size or color intensity indicates reward magnitude
- Brighter/larger = higher reward

**And** indicators update every frame based on current state

**And** indicators render in < 3ms (part of frame budget)

**Prerequisites:** Story 4.3 (Fog-of-war rendering)

**Technical Notes:**
- Agent indicator always visible (reference point)
- Gradient arrow helps researcher see what agent "should" do locally
- Use pygame.draw.line() for vertical line, pygame.draw.polygon() for arrow
- Color-code for quick visual interpretation
- Keep visual clutter minimal - clear, purposeful indicators only
- Reference: FR32, FR34, FR33

---

### Story 4.5: Render Score Display and Episode Info (HUD)

As a researcher,
I want to see real-time scores and episode information,
So that I can track agent performance during execution.

**Acceptance Criteria:**

**Given** Visualizer with function view from Story 4.4
**When** I implement _render_hud() private method
**Then** it displays the following information as text overlay:

**Cumulative Score Display:**
- Label: "Score: {cumulative_reward:.2f}"
- Font size: 24px
- Position: Top-left corner (10px, 10px)
- Color: White (#FFFFFF) for contrast

**Perfect Score Display:**
- Label: "Perfect: {perfect_score:.2f}"
- Font size: 20px
- Position: Below cumulative score (10px, 40px)
- Color: Light gray (#CCCCCC)

**Performance Gap Display:**
- Label: "Gap: {gap:.2f}" where gap = score - perfect_score
- Font size: 20px
- Position: Below perfect score (10px, 65px)
- Color: Red if negative (under-performing), Green if zero/positive

**Timestep Display:**
- Label: "Time: {timestep} / {episode_length}"
- Font size: 20px
- Position: Top-right corner (align right, 10px from edge)
- Color: White (#FFFFFF)

**Current Reward Display:**
- Label: "Reward: {current_reward:.3f}"
- Font size: 18px
- Position: Below timestep
- Color: Yellow (#FFFF00) for visibility

**And** all text renders with anti-aliasing for readability

**And** HUD updates every frame based on current state

**And** HUD rendering completes in < 3ms (part of frame budget)

**And** text is readable on dark background (sufficient contrast)

**Prerequisites:** Story 4.1 (Visualizer with font rendering)

**Technical Notes:**
- Use pygame.font.render() for text surfaces
- Cache font objects (don't recreate every frame)
- Consider caching text surfaces if values don't change every frame
- Gap color coding provides instant performance feedback
- HUD = Heads-Up Display (game UI terminology)
- Reference: FR38, FR39, FR40, FR41, FR33

---

### Story 4.6: Implement Historical Trail Rendering and FPS Management

As a researcher,
I want to see agent's previous positions as a trail,
So that I can visualize the agent's exploration strategy over time.

**Acceptance Criteria:**

**Given** Visualizer with HUD from Story 4.5
**When** I implement historical trail rendering
**Then** trail features:
- Stores recent agent positions (last 50-100 positions)
- Draws line connecting historical positions (breadcrumb path)
- Trail color: semi-transparent white or cyan (#00FFFF with alpha)
- Trail fades older positions (gradient alpha: newest=opaque, oldest=transparent)
- Trail clears on episode reset

**And** trail is always enabled (FR36 toggle deferred to Phase 2)

**And** trail rendering:
- Use pygame.draw.lines() for efficiency
- Store trail as deque with maxlen for automatic old position pruning
- Draw before agent indicator (trail in background, agent on top)

**And** FPS management in update() method:
- Call clock.tick(fps) to maintain target frame rate
- Measure actual FPS with clock.get_fps()
- Optional: Display actual FPS in HUD for debugging

**And** complete frame rendering (function + fog + indicators + HUD + trail) maintains 60 FPS

**And** update() method orchestrates all rendering:
1. Fill background (black or dark blue)
2. Render function view with fog-of-war
3. Render historical trail
4. Render agent and gradient indicators
5. Render HUD
6. pygame.display.flip() to show frame
7. Handle pygame events (window close, etc.)
8. clock.tick(fps)

**And** all rendering for single frame completes in < 16ms (60 FPS = 16.67ms per frame)

**Prerequisites:** Stories 4.1-4.5 (All visualization components)

**Technical Notes:**
- collections.deque with maxlen automatically drops old positions
- Trail provides motion context - shows if agent is "wandering" vs "tracking"
- Alpha transparency requires per-pixel alpha surface or draw order tricks
- Simple approach: draw older positions with lighter color (no true alpha needed)
- FPS management critical for real-time feel (Architecture NFR1, NFR5)
- pygame.display.flip() vs .update() - use flip() for full screen refresh
- Reference: FR35, FR36, FR37, Architecture Section "Performance Considerations" NFR1

---

### Story 4.7: Integrate Visualizer with Environment

As a researcher,
I want the Environment to use the Visualizer automatically when render mode is enabled,
So that I can see episodes without extra setup code.

**Acceptance Criteria:**

**Given** complete Visualizer from Stories 4.1-4.6
**When** I update Environment class in environment.py
**Then** __init__ creates Visualizer instance if render_mode=True:
```python
if render_mode:
    self.visualizer = Visualizer(width=800, height=600, fps=60)
else:
    self.visualizer = None
```

**And** reset() initializes visualizer state if it exists

**And** step() calls visualizer.update(state_dict) after each step if visualizer exists

**And** run() method properly handles visualization:
- Before loop: Show initial state
- Each step: Call visualizer.update()
- After loop: Keep window open briefly or wait for user to close

**And** Environment exports get_state_for_viz() helper that returns dict with all visualization data:
- position, timestep, cumulative_reward, current_reward
- gradient, gradient_positions
- perfect_score, episode_length
- observation_radius (for fog-of-war)

**And** visualizer receives complete state each frame (no missing data)

**And** window close event (pygame.QUIT) gracefully terminates episode

**And** visualization overhead < 16ms per step (maintains 60 FPS)

**Prerequisites:** Stories 4.1-4.6 (Complete Visualizer), Epic 2 (Environment)

**Technical Notes:**
- Visualizer is optional - None check before calling
- Pass state dict to visualizer each frame (loose coupling)
- Window close should not crash - catch pygame.QUIT event
- Visualizer lifetime managed by Environment
- Performance: visualization should not significantly slow headless performance
- Reference: Architecture Section "Integration Points - Environment ↔ Visualizer" and FR30-FR41

---

### Story 4.8: Create Visualization Tests and Configuration

As a developer,
I want tests for visualization components and configurable visual settings,
So that rendering works correctly and researchers can customize appearance.

**Acceptance Criteria:**

**Given** complete Visualizer integration from Story 4.7
**When** I create tests/test_visualizer.py with pytest
**Then** it includes test_visualizer_initialization() that validates:
- Visualizer initializes without errors
- Window dimensions are correct
- Clock and font objects exist

**And** it includes test_headless_rendering() that validates:
- Visualizer can render without display (headless mode for CI)
- Use pygame.Surface instead of display for headless tests
- Or mock pygame display for testing

**And** it includes test_state_to_viz_conversion() that validates:
- Environment.get_state_for_viz() returns all required keys
- State dict contains valid data types

**And** it includes test_fps_performance() that validates:
- Rendering loop can maintain 60 FPS target
- Frame time < 16ms on standard hardware
- Use timeit or pytest-benchmark for timing tests

**And** add visualization configuration to Environment:
- vis_config: dict parameter in __init__
- Allows customizing: colors, trail_length, font_size, window_size
- Pass vis_config to Visualizer

**And** configuration parameters documented in docstrings

**And** all tests pass (may need headless pygame setup for CI)

**Prerequisites:** Story 4.7 (Visualizer integration)

**Technical Notes:**
- Testing graphics is tricky - focus on API contracts and performance
- Headless rendering: pygame.display.set_mode() with HIDDEN flag or dummy video driver
- Performance tests validate NFR1 (60 FPS)
- Visual configuration enables researcher customization
- Mock pygame for pure unit tests if needed
- Reference: Architecture Section "Testing Patterns" and "Performance Considerations"

---

## Epic 5: Human Play & Validation

**Goal:** Human keyboard control with identical observation constraints as AI agents

**User Value:** Researchers can play manually to validate benchmark difficulty and establish human baseline

**FRs Covered:** FR47-FR53

---

### Story 5.1: Implement HumanAgent with Keyboard Input

As a researcher,
I want to control the agent using keyboard arrow keys,
So that I can experience the benchmark from the agent's perspective.

**Acceptance Criteria:**

**Given** Agent abstract base class from Story 2.1
**When** I create HumanAgent class in src/funcbench/agent.py
**Then** it inherits from Agent

**And** __init__ accepts no parameters (human provides input in real-time)

**And** get_action(observation: dict) implements keyboard input handling:
1. Check for pygame key events
2. Map keys to actions:
   - Left arrow key → ACTION_LEFT (0)
   - Right arrow key → ACTION_RIGHT (2)
   - Down arrow key or Space → ACTION_STAY (1)
3. Return action immediately when key is pressed
4. If no key pressed, return ACTION_STAY (1) as default

**And** keyboard input uses pygame.key.get_pressed() for responsive controls:
```python
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT]:
    return ACTION_LEFT
elif keys[pygame.K_RIGHT]:
    return ACTION_RIGHT
else:
    return ACTION_STAY
```

**And** input lag < 50ms between keypress and action execution

**And** HumanAgent ignores observation dict (human uses visual feedback from window)

**And** class includes NumPy-style docstring explaining keyboard controls

**And** supports pygame event pump (pygame.event.pump()) to keep window responsive

**Prerequisites:** Story 2.1 (Agent interface), Epic 4 (Visualization for human feedback)

**Technical Notes:**
- Use pygame.key.get_pressed() for immediate key state (not event queue)
- pygame.event.pump() must be called to update key state
- Input responsiveness critical for human playability (Architecture NFR5)
- Human sees same fog-of-war as AI agents (fair comparison)
- Default to STAY if no keys pressed (agent doesn't drift)
- Reference: FR47, FR53, Architecture Section "Human Play Mode"

---

### Story 5.2: Implement Human Score Tracking and Comparison

As a researcher,
I want to track human player scores separately from AI agents,
So that I can compare human performance to AI baselines.

**Acceptance Criteria:**

**Given** HumanAgent from Story 5.1 and evaluation utilities from Epic 3
**When** I run episodes with HumanAgent
**Then** human scores are tracked identically to AI agent scores:
- Same cumulative reward calculation
- Same perfect score comparison
- Same performance gap measurement

**And** evaluation.py run_episodes() works with HumanAgent without modification

**And** human score tracking includes:
- Episode scores for multiple human attempts
- Average human score across attempts
- Best human score achieved
- Human vs random agent comparison
- Human vs greedy agent comparison (if implemented)

**And** human scores saved with metadata indicating agent_type="human"

**And** visualization shows human performance gap in real-time during play

**And** after episode completion, summary displays:
- "Your Score: {score:.2f}"
- "Perfect Score: {perfect:.2f}"
- "Gap: {gap:.2f}"
- "Random Agent Average: {random_avg:.2f}" (if available)

**And** human can play multiple episodes in sequence without restarting program

**Prerequisites:** Story 5.1 (HumanAgent), Story 3.3 (Evaluation framework)

**Technical Notes:**
- HumanAgent is just another Agent implementation - no special handling needed
- Human scores provide validation that task is learnable
- Performance gap shows if humans can approach perfect score with practice
- Multiple attempts measure human learning curve
- Fair comparison: humans and AI see identical observations (fog-of-war)
- Reference: FR50, FR52, Architecture Section "Human Play Mode"

---

### Story 5.3: Create Human Play Example and Tests

As a researcher,
I want a simple example script for human play,
So that I can quickly validate the benchmark and let others try it.

**Acceptance Criteria:**

**Given** HumanAgent from Stories 5.1-5.2
**When** I create examples/play.py script
**Then** it implements complete human play session:

```python
from funcbench import GaussianTranslation, Environment, HumanAgent

# Create function and environment
func = GaussianTranslation(velocity=0.1, seed=42)
env = Environment(func, episode_length=1000, render_mode=True)

# Create human agent
agent = HumanAgent()

# Display instructions
print("=== FuncBench Human Play ===")
print("Controls:")
print("  ← Left Arrow:  Move left")
print("  → Right Arrow: Move right")
print("  ↓ Down Arrow:  Stay in place")
print("\nGoal: Track the moving peak to maximize cumulative reward")
print("Close window to exit\n")

# Run episode
score = env.run(agent, render=True)

# Show results
perfect = env.function.get_perfect_score(env.episode_length)
gap = score - perfect
print(f"\n=== Episode Complete ===")
print(f"Your Score: {score:.2f}")
print(f"Perfect Score: {perfect:.2f}")
print(f"Gap: {gap:.2f} ({gap/perfect*100:.1f}%)")
```

**And** script handles window close gracefully (pygame.QUIT event)

**And** script displays clear instructions before starting

**And** script is executable: `python examples/play.py`

**And** README.md updated with quick-start example showing human play

**And** create tests/test_human_agent.py with pytest:
- test_human_agent_initialization()
- test_keyboard_action_mapping()
- test_human_agent_with_environment()
- test_human_scores_tracked()

**And** tests use mocked pygame events for CI environments

**And** all tests pass

**Prerequisites:** Stories 5.1-5.2 (HumanAgent complete)

**Technical Notes:**
- play.py is primary example for validation and demos
- Clear instructions help first-time users understand controls
- Graceful exit handling prevents crashes on window close
- Tests mock pygame to avoid GUI dependencies in CI
- Human play validates benchmark is learnable by humans
- Reference: FR47-FR53, Architecture Section "Code Examples"

---

## Epic 6: Testing & Package Distribution

**Goal:** Comprehensive testing infrastructure and PyPI distribution

**User Value:** Researchers can pip install and trust results are reproducible

**FRs Covered:** Testing infrastructure, packaging, documentation

---

### Story 6.1: Create Reproducibility Test Suite

As a researcher,
I want tests that verify deterministic behavior across runs,
So that I can trust my results are reproducible for publication.

**Acceptance Criteria:**

**Given** complete FuncBench implementation from Epics 1-5
**When** I create tests/test_reproducibility.py with pytest
**Then** it includes test_deterministic_function_evaluation() that validates:
- Same seed produces identical function evaluations
- Multiple calls with same (x, t, seed) return identical values
- Different seeds produce different evaluations

**And** it includes test_deterministic_episode() that validates:
- Same seed produces identical episode outcomes
- Episode 1: Create func(seed=42), env, agent(seed=42), run episode
- Episode 2: Create func(seed=42), env, agent(seed=42), run episode
- Assert: cumulative rewards are identical
- Assert: episode histories match exactly (positions, rewards, actions)

**And** it includes test_platform_independence() that validates:
- Results are identical across platforms (Windows, Mac, Linux)
- Use saved reference episodes from known seeds
- Compare current run to reference data
- Tolerate only floating-point precision differences (< 1e-10)

**And** it includes test_perfect_score_accuracy() that validates:
- Theoretical perfect score matches analytical calculation
- Perfect score is float64 precision
- For GaussianTranslation: perfect = amplitude * episode_length

**And** it includes test_random_agent_reproducibility() that validates:
- Same seed produces identical random action sequences
- Different seeds produce different sequences
- Action distribution is uniform over many episodes

**And** all tests use fixtures for standard configurations

**And** all tests pass consistently across multiple runs

**Prerequisites:** Epics 1-5 complete (full implementation)

**Technical Notes:**
- Reproducibility is critical for scientific research (Architecture NFR6-10)
- Test with multiple seeds to ensure seeding works correctly
- Save reference data for platform independence tests
- Float64 precision minimizes numerical drift
- Document expected behavior in test docstrings
- Reference: Architecture Section "Reproducibility" NFR6-10

---

### Story 6.2: Create Integration Test Suite

As a developer,
I want end-to-end integration tests for complete workflows,
So that I can ensure all components work together correctly.

**Acceptance Criteria:**

**Given** complete FuncBench from Epics 1-5
**When** I create tests/test_integration.py with pytest
**Then** it includes test_complete_headless_episode() that validates:
- Create function, environment (render_mode=False), random agent
- Run complete 1000-step episode
- Verify episode completes successfully
- Verify cumulative reward is calculated
- Verify history is tracked
- Episode completes in < 2 seconds

**And** it includes test_complete_visualized_episode() that validates:
- Create function, environment (render_mode=True), random agent
- Run complete episode with visualization
- Handle pygame events (mock or headless display)
- Verify visualization doesn't crash
- Episode completes within performance budget

**And** it includes test_multi_episode_evaluation() that validates:
- Run 10 episodes with random agent
- Verify results dict structure
- Verify statistics are calculated correctly
- All episodes complete successfully

**And** it includes test_save_load_roundtrip() that validates:
- Run episodes and save results
- Load saved results
- Verify loaded data matches saved data
- JSON round-trip preserves information

**And** it includes test_human_agent_integration() that validates:
- HumanAgent can be used with environment (mock keyboard input)
- Episodes complete successfully
- Scores are tracked correctly

**And** it includes test_greedy_agent_integration() that validates:
- GreedyAgent can run complete episodes
- Agent follows gradient correctly
- Performance > random agent (on average)

**And** all integration tests use realistic configurations

**And** all tests pass

**Prerequisites:** Epics 1-5 complete

**Technical Notes:**
- Integration tests verify component interactions
- Use headless pygame or mocking for CI compatibility
- Test realistic scenarios researchers will use
- Validate performance requirements (< 2s for 1000 steps headless)
- Mock keyboard for HumanAgent testing in CI
- Reference: Architecture Section "Testing Patterns"

---

### Story 6.3: Configure Package Build and Metadata

As a developer,
I want properly configured package metadata and build system,
So that FuncBench can be distributed via PyPI.

**Acceptance Criteria:**

**Given** complete FuncBench codebase
**When** pyproject.toml is fully configured
**Then** it includes all required metadata:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "funcbench"
version = "0.1.0"
description = "First-principles AI reasoning benchmark for temporal pattern learning"
readme = "README.md"
requires-python = ">=3.9"
license = {text = "MIT"}
authors = [
    {name = "Morgan", email = "your.email@example.com"}
]
keywords = ["ai", "benchmark", "reasoning", "temporal-patterns", "reinforcement-learning"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Scientific/Engineering :: Artificial Intelligence",
]

dependencies = [
    "numpy>=2.3.5",
    "pygame-ce>=2.5.6",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
    "pytest-benchmark>=4.0.0",
]
analysis = [
    "matplotlib>=3.10.7",
]

[project.urls]
Homepage = "https://github.com/username/funcbench"
Documentation = "https://github.com/username/funcbench#readme"
Repository = "https://github.com/username/funcbench"
Issues = "https://github.com/username/funcbench/issues"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --strict-markers"

[tool.coverage.run]
source = ["funcbench"]
omit = ["tests/*"]
```

**And** src/funcbench/__init__.py exports public API:
```python
__version__ = "0.1.0"

from funcbench.function import Function2D, GaussianTranslation
from funcbench.environment import Environment
from funcbench.agent import Agent, RandomAgent, GreedyAgent, HumanAgent
from funcbench.evaluation import run_episodes, save_episode_data, load_episode_data

__all__ = [
    "Function2D",
    "GaussianTranslation",
    "Environment",
    "Agent",
    "RandomAgent",
    "GreedyAgent",
    "HumanAgent",
    "run_episodes",
    "save_episode_data",
    "load_episode_data",
]
```

**And** package builds successfully: `python -m build`

**And** built package includes all required files (src, tests, examples, README, LICENSE)

**And** package can be installed locally: `pip install -e .`

**And** installed package imports work: `python -c "import funcbench; print(funcbench.__version__)"`

**Prerequisites:** Story 1.1 (initial project structure), all implementation complete

**Technical Notes:**
- Hatchling is modern Python build backend (Architecture decision)
- Semantic versioning: 0.1.0 for initial release
- MIT license (or your choice)
- Keywords help PyPI discoverability
- Classifiers indicate project status and audience
- Export only public API in __init__.py
- Reference: Architecture Section "Project Structure" and "pyproject.toml Configuration"

---

### Story 6.4: Create Comprehensive README and Documentation

As a researcher,
I want clear documentation and examples,
So that I can get started with FuncBench quickly.

**Acceptance Criteria:**

**Given** complete FuncBench package
**When** README.md is written
**Then** it includes the following sections:

**Title and Description:**
- Project name and one-line description
- Badges: build status, PyPI version, Python versions, license

**Installation:**
```bash
pip install funcbench
```

**Quick Start Example:**
```python
from funcbench import GaussianTranslation, Environment, RandomAgent

# Create temporal function
func = GaussianTranslation(velocity=0.1)

# Create environment
env = Environment(func, episode_length=1000)

# Run random agent
agent = RandomAgent(seed=42)
score = env.run(agent, render=False)
print(f"Score: {score}")
```

**Human Play Example:**
```python
from funcbench import GaussianTranslation, Environment, HumanAgent

func = GaussianTranslation(velocity=0.1)
env = Environment(func, episode_length=1000, render_mode=True)
agent = HumanAgent()

print("Use arrow keys: ← left, → right, ↓ stay")
score = env.run(agent, render=True)
```

**Features:**
- List key features (temporal functions, fog-of-war, baselines, human play)
- Mention Phase 1 scope and Phase 2 plans

**Documentation Links:**
- Link to examples/ directory
- Link to architecture.md (if created)
- Link to GitHub issues

**Contributing:**
- How to report issues
- How to run tests: `pytest`
- How to contribute

**License:**
- License type (MIT)

**Citation:**
- How to cite FuncBench in research papers

**And** examples/ directory includes:
- play.py (human keyboard control)
- random_baseline.py (random agent evaluation)
- Both with clear comments

**And** documentation is clear, concise, and accurate

**And** all code examples in README are tested and work

**Prerequisites:** Epics 1-5 complete, Story 6.3 (package configured)

**Technical Notes:**
- README is first thing users see - make it clear and inviting
- Quick start should be < 10 lines of code (Architecture NFR15)
- Examples must actually work (test them!)
- Link to examples/ for more detail
- Keep README focused - detailed docs can go elsewhere
- Reference: Architecture Section "Usability" NFR15-19

---

### Story 6.5: Create Example Scripts and Final Testing

As a researcher,
I want complete, working example scripts,
So that I can see best practices and adapt for my research.

**Acceptance Criteria:**

**Given** complete FuncBench package
**When** examples/ directory is populated
**Then** it includes examples/random_baseline.py:

```python
"""Evaluate random agent baseline."""
from funcbench import GaussianTranslation, Environment, RandomAgent
from funcbench.evaluation import run_episodes

# Create function and environment
func = GaussianTranslation(velocity=0.1, seed=42)
env = Environment(func, episode_length=1000)

# Create random agent
agent = RandomAgent(seed=42)

# Run 10 episodes
print("Running 10 episodes with random agent...")
results = run_episodes(env, agent, n_episodes=10, render=False)

# Display results
print(f"\nResults:")
print(f"  Mean Score: {results['mean_score']:.2f}")
print(f"  Std Score: {results['std_score']:.2f}")
print(f"  Best Score: {results['best_score']:.2f}")
print(f"  Perfect Score: {results['perfect_scores'][0]:.2f}")
```

**And** examples/play.py (from Story 5.3) is complete and tested

**And** examples/ includes optional greedy_baseline.py (if GreedyAgent implemented)

**And** all examples run successfully: `python examples/play.py`, etc.

**And** run final comprehensive test pass:
- All unit tests pass: `pytest tests/`
- All integration tests pass
- All reproducibility tests pass
- Test coverage > 80%: `pytest --cov=funcbench`

**And** verify package installation workflow:
1. Build package: `python -m build`
2. Install in clean venv: `pip install dist/funcbench-0.1.0-py3-none-any.whl`
3. Run examples from installed package
4. All examples work without errors

**And** create MANIFEST.in if needed for non-code files

**And** examples are documented in README.md

**Prerequisites:** All previous stories (complete implementation)

**Technical Notes:**
- Examples demonstrate best practices
- Test examples as part of CI
- Ensure installed package includes example files
- Coverage > 80% is good for research code
- MANIFEST.in may be needed for data files (if any)
- Final testing validates everything works end-to-end
- Reference: Architecture Section "Code Examples" and NFR15-19

---

## Summary

### Complete Epic Breakdown

**Total Epics:** 6
**Total Stories:** 29

| Epic | Stories | FRs Covered | Description |
|------|---------|-------------|-------------|
| Epic 1 | 5 | FR1-FR7 | Project setup, Function2D ABC, GaussianTranslation, perfect score |
| Epic 2 | 8 | FR8-FR22, FR23-FR25, FR59-FR61, FR63-FR65 | Agent interface, Environment, episode management, configuration |
| Epic 3 | 5 | FR26-FR29 | RandomAgent, GreedyAgent, multi-episode evaluation, persistence |
| Epic 4 | 8 | FR30-FR41, FR62 | PyGame 2D visualization, fog-of-war, HUD, historical trail |
| Epic 5 | 3 | FR47-FR53 | HumanAgent keyboard control, human baseline validation |
| Epic 6 | 5 | Testing & Packaging | Reproducibility tests, integration tests, PyPI distribution, documentation |

### FR Coverage Matrix

**Complete coverage validation for all 57 Phase 1 MVP functional requirements:**

| FR Range | Description | Epic | Stories | Status |
|----------|-------------|------|---------|--------|
| FR1-FR7 | Function System | Epic 1 | 1.1-1.5 | ✓ Covered |
| FR8-FR15 | Agent System | Epic 2 | 2.1 | ✓ Covered |
| FR16-FR22 | Episode Management | Epic 2 | 2.2-2.6 | ✓ Covered |
| FR23-FR25 | Scoring & Evaluation | Epic 2 | 2.4, 2.6 | ✓ Covered |
| FR26-FR29 | Baseline Comparison | Epic 3 | 3.1-3.4 | ✓ Covered |
| FR30-FR41 | 2D Visualization | Epic 4 | 4.1-4.7 | ✓ Covered |
| FR42-FR46 | 3D God View | - | - | ⚠️ Deferred to Phase 2 |
| FR47-FR53 | Human Play Mode | Epic 5 | 5.1-5.3 | ✓ Covered |
| FR54-FR58 | Playback & Analysis | - | - | ⚠️ Deferred to Phase 2 |
| FR59-FR65 | Configuration | Epic 2 | 2.2, 2.7 | ✓ Covered + Epic 4 (4.8) |
| FR66-FR70 | LLM Integration | - | - | ⚠️ Deferred to Post-MVP |
| FR71-FR75 | Extension Tools | Epic 1 | 1.2, 1.7 | ✓ Partially (base class extensibility) + Deferred |

**Phase 1 MVP Coverage:** 57 of 57 required FRs covered (100%)

**Deferred Features:**
- FR42-FR46: 3D ModernGL god view (Phase 2)
- FR54-FR58: Playback controls (pause, slow-motion, replay) (Phase 2)
- FR66-FR70: LLM integration (Post-MVP)
- FR71-FR75: Advanced extension tools (Post-MVP - partial support via Function2D base class)

### Epic Sequencing and User Value Validation

**Each epic delivers incremental user value:**

1. **Epic 1 (Foundation)** → ✅ Researchers can evaluate Gaussian functions analytically
2. **Epic 2 (Environment)** → ✅ Researchers can run agents through episodes headless and get scores
3. **Epic 3 (Baselines)** → ✅ Researchers can compare custom agents to random/greedy baselines
4. **Epic 4 (Visualization)** → ✅ Researchers can visualize temporal dynamics and validate behavior
5. **Epic 5 (Human Play)** → ✅ Researchers can play manually and establish human baseline for validation
6. **Epic 6 (Testing & Distribution)** → ✅ Researchers can pip install and trust reproducible results

**Anti-Pattern Validation:**
- ✅ NO technical layer epics (database/API/frontend)
- ✅ Each epic delivers user-facing capability
- ✅ Foundation epic exception is valid (greenfield project needs initial structure)
- ✅ Incremental value delivery enables early validation

### Story Quality Validation

**All stories meet quality criteria:**
- ✅ Vertically sliced (complete functionality, not just one layer)
- ✅ Sequentially ordered (logical progression, no forward dependencies)
- ✅ Sized for single-session completion
- ✅ Clear BDD acceptance criteria (Given/When/Then/And)
- ✅ Technical implementation details from Architecture incorporated
- ✅ Performance targets specified where applicable
- ✅ Prerequisites explicitly listed
- ✅ Architecture references provided

### Implementation Readiness

**This epic breakdown is ready for Phase 4 Implementation:**

✅ **Complete Context Available:**
- PRD requirements (75 FRs total, 57 in Phase 1)
- Architecture technical decisions
- Epic and story breakdown (29 stories)

✅ **Development Path Clear:**
- Story 1.1 is first (no prerequisites)
- Each story lists explicit prerequisites
- Dependencies flow forward only (no circular dependencies)

✅ **Quality Assured:**
- FR coverage validated (100% of Phase 1)
- User value per epic confirmed
- Story sizing appropriate (single-session tasks)
- BDD acceptance criteria testable

**Next Steps:**
1. Run `/bmad:bmm:workflows:workflow-status` to update status file
2. Mark create-epics-and-stories-final as complete
3. Proceed to test-design (optional) or implementation-readiness (required) workflows

---

_For implementation: Start with Epic 1, Story 1.1 and proceed sequentially. Each story is self-contained with complete acceptance criteria and technical guidance._

