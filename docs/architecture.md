# FuncBench Architecture

## Executive Summary

FuncBench is a Python research library testing whether AI agents can learn temporal patterns through visual observation. The architecture follows a **phased validation approach**: Phase 1 validates the core concept with minimal complexity (PyGame 2D visualization only), then Phase 2 adds advanced features (3D ModernGL rendering, comprehensive analysis tools) only after the benchmark proves viable.

**Key Architectural Principles:**
- **Reproducibility First**: Deterministic function evolution, float64 precision, platform-independent results
- **Performance Critical**: Real-time 60 FPS visualization, < 1ms function evaluation
- **Validation Before Scale**: Simple MVP structure to prove concept, then expand
- **Scientific Rigor**: NumPy-based computation, comprehensive testing, theoretical perfect score validation

## Phased Development Strategy

### Phase 1: Core Validation (Initial Implementation)
**Goal:** Prove the benchmark concept works - humans can learn it, random agents fail, visualization is clear

**Scope:**
- 2D Gaussian translation function
- Simple episode management (position, time, score tracking)
- PyGame 2D agent view with fog-of-war
- Human keyboard control
- Random baseline agent
- Basic reproducibility tests

**Success Criteria:**
- Humans can play and improve score over time
- Random agent performance << human performance
- Visualization clearly shows peak translation
- Deterministic results (same seed = same score)

**If Phase 1 fails:** Benchmark concept doesn't work, investigate why before building more complexity

### Phase 2: Full Research Tool (After Validation)
**Scope:**
- 3D ModernGL god view (full function surface)
- Additional baselines (greedy, perfect agents)
- LLM integration (visual snapshots, action parsing)
- Comprehensive analysis (learning curves, replay, export)
- Advanced metrics (pattern discovery detection, convergence time)
- Function zoo (oscillating, accelerating patterns)

**Only proceed to Phase 2 if Phase 1 validates the approach**

## Decision Summary

| Category | Decision | Version | Affects FRs | Rationale |
| -------- | -------- | ------- | ----------- | --------- |
| **Core Stack** |
| Package Structure | src/ layout | - | All | PyOpenSci standard, ensures tests run against installed package |
| Build Backend | Hatchling | - | All | Modern, lightweight, PEP 517 compliant, scientific Python standard |
| Rendering (Phase 1) | pygame-ce 2D | 2.5.6 | FR30-41 | Actively maintained fork, simple 2D visualization for validation |
| Rendering (Phase 2) | pygame-ce + ModernGL | 5.12.0 | FR42-46 | High-performance 3D, modern OpenGL binding |
| **Computation** |
| Function Evaluation | NumPy vectorized | 2.3.5 | FR1-7 | float64 precision, vectorized performance, < 1ms evaluation |
| Numerical Precision | float64 (NumPy default) | - | NFR11-14 | Reproducibility requirement, minimize floating-point error |
| **Episode Management** |
| State Pattern | Centralized dict in Environment | - | FR16-22 | Gym-like API, explicit state, easy serialization for replay |
| Agent Interface | Abstract base class | - | FR8-15 | Enforces contract, dict observations (extensible for LLM) |
| Observation Pattern | Sampled gradient array | - | FR10-12 | Rich local information, vectorized evaluation, supports fog-of-war viz |
| **Testing** |
| Test Framework | pytest | latest | All | Scientific Python standard, excellent fixtures |
| Test Structure | Organized modules | - | All | Reproducibility tests critical for research use |
| **Dependencies (Phase 1)** |
| Core Compute | numpy | 2.3.5 | FR1-29 | Scientific computation, vectorized operations |
| Visualization | pygame-ce | 2.5.6 | FR30-53 | 2D rendering, event handling, actively maintained |
| Testing | pytest | latest | - | Test framework |
| Optional Analysis | matplotlib | 3.10.7 | FR74-75 | Plotting learning curves (optional dependency) |
| **Dependencies (Phase 2)** |
| 3D Rendering | moderngl | 5.12.0 | FR42-46 | High-performance OpenGL, C++ implementation |
| 3D Integration | moderngl-window | latest | FR45 | Simplifies pygame-moderngl integration |

## Project Structure

### Phase 1: Core Validation Structure

```
funcbench/
├── src/
│   └── funcbench/
│       ├── __init__.py              # Package exports: GaussianTranslation, Environment, Agent
│       ├── function.py              # Function2D ABC, GaussianTranslation implementation
│       ├── environment.py           # Environment class with episode management
│       ├── agent.py                 # Agent ABC, HumanAgent, RandomAgent
│       └── visualizer.py            # PyGame 2D rendering with fog-of-war
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # pytest fixtures (environments, functions, agents)
│   ├── test_function.py             # Test Gaussian evaluation, perfect score calculation
│   ├── test_environment.py          # Test episode state, step logic, reset
│   └── test_reproducibility.py     # Test determinism with seeds
│
├── examples/
│   ├── play.py                      # Human keyboard control (arrow keys)
│   └── random_baseline.py           # Random agent for performance comparison
│
├── pyproject.toml                   # Project metadata, dependencies, build config
├── README.md                        # Quick-start guide, installation
├── LICENSE                          # MIT (or your choice)
└── .gitignore                       # Python, IDE, build artifacts
```

**Phase 1 File Count:** 13 files total
- 5 source files (< 200 lines each for simplicity)
- 3 test files
- 2 examples
- 3 config/docs

### Phase 2: Full Research Tool Structure (Future)

```
funcbench/
├── src/
│   └── funcbench/
│       ├── __init__.py
│       │
│       ├── core/
│       │   ├── __init__.py
│       │   ├── functions.py         # Function2D, GaussianTranslation, + function zoo
│       │   ├── environment.py       # Environment with replay support
│       │   └── types.py             # Shared types (Action enum, Observation dataclass)
│       │
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── base.py              # Agent ABC
│       │   ├── human.py             # HumanAgent
│       │   ├── baselines.py         # RandomAgent, GreedyAgent, PerfectAgent
│       │   └── llm.py               # LLMAgent with vision API integration
│       │
│       ├── visualization/
│       │   ├── __init__.py
│       │   ├── renderer.py          # Visualizer with view switching
│       │   ├── agent_view.py        # 2D PyGame rendering
│       │   ├── god_view.py          # 3D ModernGL rendering
│       │   └── shaders/
│       │       ├── surface_vertex.glsl
│       │       └── surface_fragment.glsl
│       │
│       ├── analysis/
│       │   ├── __init__.py
│       │   ├── metrics.py           # Learning curves, convergence detection
│       │   ├── replay.py            # Episode replay system
│       │   └── export.py            # CSV/JSON export
│       │
│       └── utils/
│           ├── __init__.py
│           └── config.py            # Configuration dataclasses
│
├── tests/
│   ├── test_functions.py            # All function types
│   ├── test_environment.py
│   ├── test_agents.py               # All agent types including LLM mocks
│   ├── test_visualization.py        # Headless rendering tests
│   ├── test_reproducibility.py
│   └── test_integration.py          # Full episode integration tests
│
├── examples/
│   ├── 01_human_play.py
│   ├── 02_baseline_comparison.py
│   ├── 03_llm_evaluation.py
│   ├── 04_custom_function.py
│   └── 05_batch_analysis.py
│
├── docs/
│   ├── index.md
│   ├── quickstart.md
│   ├── api/
│   └── research/
│
└── pyproject.toml
```

**Only expand to Phase 2 structure after Phase 1 validation succeeds**

## Functional Requirements to Architecture Mapping

### Phase 1 Implementation

| FR Category | FRs | Module | Implementation Notes |
|-------------|-----|--------|---------------------|
| Function System | FR1-7 | `function.py` | Function2D ABC, GaussianTranslation class with NumPy vectorized evaluation |
| Agent System | FR8-15 | `agent.py` | Agent ABC, HumanAgent (keyboard), RandomAgent |
| Episode Management | FR16-22 | `environment.py` | Environment class with state dict, step/reset methods |
| Scoring & Evaluation | FR23-29 | `environment.py` | Cumulative reward tracking, perfect score calculation |
| Visualization - Agent View | FR30-41 | `visualizer.py` | PyGame 2D rendering, fog-of-war, score display |
| Human Play Mode | FR47-53 | `agent.py` | HumanAgent with pygame event handling |
| Configuration | FR59-65 | `environment.py` + examples | Constructor parameters, headless mode flag |

**Deferred to Phase 2:** FR42-46 (3D god view), FR54-58 (replay), FR66-70 (LLM), FR71-75 (advanced analysis)

### Phase 2 Expansion

| FR Category | FRs | Module | Implementation Notes |
|-------------|-----|--------|---------------------|
| Visualization - God View | FR42-46 | `visualization/god_view.py` | ModernGL 3D surface rendering with GLSL shaders |
| Playback & Analysis | FR54-58 | `analysis/replay.py` | Episode replay from saved history |
| LLM Integration | FR66-70 | `agents/llm.py` | Visual snapshot rendering, API integration |
| Extension Tools | FR71-75 | `analysis/` | Export utilities, plotting, custom function support |

## Technology Stack Details

### Phase 1: Core Dependencies

**Core Computation:**
- **NumPy 2.3.5** - Vectorized function evaluation, float64 precision
  - Used for: Gaussian evaluation, gradient sampling, perfect score calculation
  - Why: Industry standard for scientific Python, reproducible computation

**Visualization:**
- **pygame-ce 2.5.6** - 2D rendering, window management, event handling
  - Used for: Agent view rendering, keyboard input, fog-of-war visualization
  - Why: Community Edition is actively maintained (Oct 2025 release), simpler than OpenGL for 2D

**Testing:**
- **pytest** (latest) - Test framework with fixtures
  - Used for: Unit tests, integration tests, reproducibility validation
  - Why: Scientific Python standard, excellent fixture system

**Optional:**
- **matplotlib 3.10.7** - Plotting library
  - Used for: Learning curve plots, score analysis (post-experiment)
  - Why: Standard for scientific visualization

### Phase 2: Additional Dependencies

**3D Rendering:**
- **ModernGL 5.12.0** - Modern OpenGL binding
  - Used for: 3D god view, hardware-accelerated surface rendering
  - Why: High performance, C++ implementation, modern API

- **moderngl-window** (latest) - Integration helper
  - Used for: Simplified pygame-moderngl integration
  - Why: Handles context creation, reduces boilerplate

### Integration Points (Phase 1)

**NumPy ↔ PyGame:**
- NumPy arrays converted to PyGame surfaces for rendering
- Gradient data (np.ndarray) → pixel colors for visualization
- `pygame.surfarray` used for efficient array-to-surface conversion

**Environment ↔ Visualizer:**
- Environment provides state dict to visualizer each frame
- Visualizer reads position, reward, gradient for rendering
- No tight coupling - visualizer can be None for headless mode

**Agent ↔ Environment:**
- Standardized observation dict (position, reward, gradient, timestep)
- Simple integer actions (0=left, 1=stay, 2=right)
- Clean interface allows easy agent swapping

## Implementation Patterns

**These patterns ensure consistent implementation across all AI agents working on FuncBench:**

### Naming Conventions

**Files:**
- `snake_case.py` for all Python files
- Test files: `test_<module>.py`
- Example files: descriptive names (`play.py`, `random_baseline.py`)

**Classes:**
- `PascalCase` for all classes
- Abstract base classes end with base name (e.g., `Agent`, `Function2D`)
- Implementations are descriptive (e.g., `GaussianTranslation`, `HumanAgent`)

**Functions/Methods:**
- `snake_case` for all functions and methods
- Private methods prefixed with `_` (e.g., `_get_observation`)
- Boolean methods use `is_` or `has_` prefix (e.g., `is_done()`)

**Variables:**
- `snake_case` for variables
- Constants in `UPPER_SNAKE_CASE` (e.g., `ACTION_LEFT = 0`)
- NumPy arrays suffixed with `_array` when ambiguous (e.g., `gradient_array`)

### Code Organization Patterns

**Imports Order:**
```python
# Standard library
import random
from abc import ABC, abstractmethod

# Third-party
import numpy as np
import pygame

# Local
from funcbench.function import Function2D
```

**Class Structure:**
```python
class ClassName:
    """Docstring with one-line summary.

    Longer description if needed.
    """

    def __init__(self, ...):
        """Initialize with parameters."""
        # Public attributes first
        self.public_attr = value
        # Private attributes after
        self._private_attr = value

    # Public methods first
    def public_method(self):
        """Public method docstring."""
        pass

    # Private methods after
    def _private_method(self):
        """Private helper method."""
        pass
```

### Type Hints

**MANDATORY for all function signatures:**
```python
def evaluate(self, x: np.ndarray, t: float) -> np.ndarray:
    """Evaluate function at position(s) x and time t."""
    pass

def step(self, action: int) -> tuple[dict, float, bool, dict]:
    """Execute action, return (observation, reward, done, info)."""
    pass
```

### Docstring Format

**Use NumPy-style docstrings:**
```python
def method_name(param1: type1, param2: type2) -> return_type:
    """Short one-line summary.

    Longer description explaining behavior, edge cases, etc.

    Parameters
    ----------
    param1 : type1
        Description of param1
    param2 : type2
        Description of param2

    Returns
    -------
    return_type
        Description of return value

    Examples
    --------
    >>> func(value1, value2)
    expected_output
    """
```

### Error Handling

**Use specific exceptions:**
```python
# BAD - generic exception
if value < 0:
    raise Exception("Value must be positive")

# GOOD - specific exception with clear message
if value < 0:
    raise ValueError(f"Expected positive value, got {value}")
```

**Validate inputs at boundaries:**
```python
class Environment:
    def step(self, action: int) -> tuple:
        """Execute action."""
        if action not in [0, 1, 2]:
            raise ValueError(
                f"Invalid action {action}. Must be 0 (left), 1 (stay), or 2 (right)"
            )
        # ... rest of logic
```

### NumPy Usage Patterns

**Always use vectorized operations:**
```python
# BAD - Python loop
rewards = []
for x_val in x_array:
    rewards.append(self._eval_single(x_val, t))
return np.array(rewards)

# GOOD - NumPy vectorized
return self.amplitude * np.exp(-((x_array - mean_t)**2) / (2 * self.sigma**2))
```

**Use float64 explicitly for reproducibility:**
```python
# Ensure float64 precision
position = np.float64(0.0)
cumulative_reward = np.float64(0.0)
```

### PyGame Rendering Patterns

**Always convert surfaces for performance:**
```python
# BAD - no conversion
surface = pygame.Surface((width, height))

# GOOD - convert to display format
surface = pygame.Surface((width, height)).convert()
```

**Clock management:**
```python
clock = pygame.Clock()
while running:
    clock.tick(60)  # Lock to 60 FPS
    # ... render logic
```

### State Management

**Environment state is a dict:**
```python
self.state = {
    'position': np.float64(0.0),
    'timestep': 0,
    'cumulative_reward': np.float64(0.0),
    'history': []
}
```

**Never mutate state directly from outside:**
```python
# BAD - external mutation
env.state['position'] = 5.0

# GOOD - use methods
env.reset()  # Resets state internally
obs, reward, done, info = env.step(action)  # Updates state internally
```

### Testing Patterns

**Fixture-based test setup:**
```python
# conftest.py
@pytest.fixture
def gaussian_function():
    """Standard Gaussian for testing."""
    return GaussianTranslation(
        velocity=0.1,
        sigma=1.0,
        amplitude=1.0,
        seed=42
    )

# test_function.py
def test_evaluation(gaussian_function):
    """Test function evaluation."""
    result = gaussian_function.evaluate(np.array([0.0]), t=0.0)
    assert result.shape == (1,)
    assert isinstance(result[0], np.float64)
```

**Reproducibility testing:**
```python
def test_deterministic_episode():
    """Same seed produces identical results."""
    func1 = GaussianTranslation(seed=42)
    env1 = Environment(func1, episode_length=100)
    agent1 = RandomAgent(seed=42)

    func2 = GaussianTranslation(seed=42)
    env2 = Environment(func2, episode_length=100)
    agent2 = RandomAgent(seed=42)

    score1 = env1.run(agent1, render=False)
    score2 = env2.run(agent2, render=False)

    assert score1 == score2, "Same seeds must produce identical scores"
```

## Consistency Rules

### Action Space

**ALWAYS use these integer codes:**
```python
ACTION_LEFT = 0
ACTION_STAY = 1
ACTION_RIGHT = 2
```

### Observation Dictionary Keys

**ALWAYS use these exact keys:**
```python
observation = {
    'position': float,           # Current x-coordinate
    'reward': float,             # Current reward value
    'gradient': np.ndarray,      # Local function samples
    'gradient_positions': np.ndarray,  # Where samples are
    'timestep': int              # Current time
}
```

### Return Signatures

**Environment.step() ALWAYS returns:**
```python
(observation: dict, reward: float, done: bool, info: dict)
```

**Agent.get_action() ALWAYS returns:**
```python
action: int  # 0, 1, or 2
```

### File Paths

**Use pathlib for cross-platform compatibility:**
```python
from pathlib import Path

# GOOD
data_path = Path("data") / "episodes" / "episode_001.json"

# BAD
data_path = "data/episodes/episode_001.json"  # Breaks on Windows
```

## Data Architecture

### Core Data Models

**Function State (GaussianTranslation):**
```python
{
    'mean_start': float,      # Starting position of peak
    'velocity': float,        # Translation speed (units/timestep)
    'sigma': float,           # Standard deviation (peak width)
    'amplitude': float,       # Peak height
    'bounds': tuple[float, float],  # (min_x, max_x)
    'seed': int | None        # Random seed for reproducibility
}
```

**Episode State (Environment):**
```python
{
    'position': np.float64,         # Agent x-coordinate
    'timestep': int,                # Current time
    'cumulative_reward': np.float64,  # Running total
    'history': list[tuple]          # [(t, x, reward, action), ...]
}
```

**Observation:**
```python
{
    'position': float,               # Current x-coordinate
    'reward': float,                 # Current reward value
    'gradient': np.ndarray,          # Local function samples (shape: [n_samples])
    'gradient_positions': np.ndarray,  # Where samples are (shape: [n_samples])
    'timestep': int                  # Current time
}
```

### Data Flows

**Episode Execution Flow:**
```
1. env.reset()
   → Initialize state {'position': 0.0, 'timestep': 0, ...}
   → Return initial observation

2. Loop until done:
   a. agent.get_action(observation) → action (int)
   b. env.step(action)
      → Update position based on action
      → Evaluate reward = function.evaluate(position, timestep)
      → Increment timestep
      → Add to history
      → Generate new observation
      → Return (obs, reward, done, info)

3. Episode ends when timestep >= episode_length
```

## API Contracts

### Function2D (Abstract Base Class)

```python
from abc import ABC, abstractmethod
import numpy as np

class Function2D(ABC):
    """Abstract base for 2D temporal functions."""

    @abstractmethod
    def evaluate(self, x: np.ndarray, t: float) -> np.ndarray:
        """Evaluate function at position(s) x and time t.

        Parameters
        ----------
        x : np.ndarray
            Position(s) to evaluate (1D array)
        t : float
            Time coordinate

        Returns
        -------
        np.ndarray
            Function values at given positions
        """
        pass

    @abstractmethod
    def get_perfect_score(self, episode_length: int) -> float:
        """Calculate theoretical perfect score.

        Parameters
        ----------
        episode_length : int
            Number of timesteps

        Returns
        -------
        float
            Maximum achievable cumulative reward
        """
        pass
```

### Environment

```python
class Environment:
    """Episode management and agent-function interaction."""

    def __init__(
        self,
        function: Function2D,
        episode_length: int = 1000,
        observation_radius: float = 5.0,
        n_gradient_samples: int = 20
    ):
        """Initialize environment."""
        pass

    def reset(self) -> dict:
        """Start new episode.

        Returns
        -------
        dict
            Initial observation
        """
        pass

    def step(self, action: int) -> tuple[dict, float, bool, dict]:
        """Execute action and advance time.

        Parameters
        ----------
        action : int
            0 (left), 1 (stay), or 2 (right)

        Returns
        -------
        observation : dict
            Agent's new observation
        reward : float
            Reward at new position
        done : bool
            True if episode finished
        info : dict
            Additional info (perfect_score, etc.)
        """
        pass

    def render(self) -> None:
        """Update visualization if enabled."""
        pass
```

### Agent (Abstract Base Class)

```python
from abc import ABC, abstractmethod

class Agent(ABC):
    """Abstract base for all agents."""

    @abstractmethod
    def get_action(self, observation: dict) -> int:
        """Choose action based on observation.

        Parameters
        ----------
        observation : dict
            Contains 'position', 'reward', 'gradient', 'gradient_positions', 'timestep'

        Returns
        -------
        int
            Action: 0 (left), 1 (stay), or 2 (right)
        """
        pass
```

## Performance Considerations

### Critical Performance Requirements

**NFR1: Real-Time Rendering (60 FPS)**
- **Target:** Maintain 60 FPS during human play
- **Implementation:**
  - Use `pygame.Clock.tick(60)` for frame locking
  - Call `.convert()` on all surfaces
  - Only update changed regions (dirty rect optimization)
  - Cache rendered text (don't re-render score every frame)

**NFR2: Function Evaluation (< 1ms)**
- **Target:** Evaluate Gaussian at any (x, t) in < 1ms
- **Implementation:**
  - NumPy vectorized operations
  - Pre-compute constants in `__init__`
  - float64 precision doesn't impact performance significantly

**NFR3: Episode Execution (< 20s for 1000 steps with viz)**
- **Target:** Full episode in < 20 seconds with visualization
- **Implementation:**
  - Efficient observation generation (vectorized gradient sampling)
  - Minimal state copying
  - Direct dict updates instead of creating new dicts

### Optimization Strategy

**Phase 1 Optimizations:**
1. NumPy vectorization for all array operations
2. PyGame surface conversion (`.convert()`)
3. Dirty rect rendering (only update changed areas)
4. Profile with `cProfile` if performance issues arise

**Phase 2 Optimizations (if needed):**
1. ModernGL for 3D (hardware-accelerated)
2. Numba JIT compilation for hot paths
3. Parallel episode execution for batch evaluation

## Deployment Architecture

### Phase 1: PyPI Package

**Installation:**
```bash
pip install funcbench
```

**Package Distribution:**
- Built with Hatchling
- Published to PyPI
- Version follows semantic versioning (0.1.0 for Phase 1)

**Supported Platforms:**
- macOS (Intel + Apple Silicon)
- Linux (Ubuntu 20.04+)
- Windows 10+

**Python Versions:**
- Python 3.9+
- Tested on 3.9, 3.10, 3.11, 3.12

### No Server Infrastructure

FuncBench is a local Python library, not a web service:
- No deployment servers needed
- No databases to manage
- No API endpoints to host
- Runs entirely on researcher's local machine

## Development Environment

### Prerequisites

**Required:**
- Python 3.9 or higher
- pip (comes with Python)
- Git (for development)

**Optional:**
- Virtual environment tool (venv, conda)
- Code editor with Python support (VS Code, PyCharm)

### Setup Commands (Phase 1)

**For Users (Install from PyPI):**
```bash
pip install funcbench
```

**For Developers (Local Development):**
```bash
# Clone repository
git clone https://github.com/username/funcbench.git
cd funcbench

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run example
python examples/play.py
```

### pyproject.toml Configuration

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
dependencies = [
    "numpy>=2.3.5",
    "pygame-ce>=2.5.6",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
    "matplotlib>=3.10.7",
]

[project.urls]
Homepage = "https://github.com/username/funcbench"
Documentation = "https://github.com/username/funcbench#readme"
Repository = "https://github.com/username/funcbench"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

## Architecture Decision Records (ADRs)

### ADR-001: Phased Development Approach

**Status:** Accepted

**Context:** FuncBench is a research benchmark - it's uncertain if the concept works until validated.

**Decision:** Implement Phase 1 (minimal validation) before investing in Phase 2 (full features).

**Consequences:**
- ✅ Fast validation of core concept
- ✅ Avoid wasted effort if benchmark doesn't work
- ✅ Simpler codebase to start
- ⚠️ Need to refactor if expanding to Phase 2

### ADR-002: NumPy Vectorized Function Evaluation

**Status:** Accepted

**Context:** Need < 1ms function evaluation with float64 precision for reproducibility.

**Decision:** Use NumPy vectorized operations for all function evaluations.

**Consequences:**
- ✅ Meets performance requirement easily
- ✅ float64 precision built-in
- ✅ Can evaluate multiple points simultaneously (visualization efficiency)
- ✅ Industry standard for scientific Python

### ADR-003: PyGame-CE for Phase 1 Visualization

**Status:** Accepted

**Context:** Need 2D visualization with fog-of-war. Full 3D is nice-to-have but not critical for validation.

**Decision:** Use pygame-ce for Phase 1, defer ModernGL 3D to Phase 2.

**Consequences:**
- ✅ Simpler implementation (pure 2D, no shaders)
- ✅ pygame-ce actively maintained (2025 releases)
- ✅ Faster development for validation
- ⚠️ No 3D god view in Phase 1
- ✅ Can add ModernGL later without major refactor

### ADR-004: Gym-Like Environment API

**Status:** Accepted

**Context:** Need standardized interface for episode management.

**Decision:** Use OpenAI Gym/Gymnasium-style API (reset, step returning obs/reward/done/info).

**Consequences:**
- ✅ Familiar to AI researchers
- ✅ Easy to integrate with RL libraries later
- ✅ Clear contract for environment-agent interaction
- ✅ Well-documented pattern

### ADR-005: Dict-Based Observations

**Status:** Accepted

**Context:** Observations need to be extensible (future: add visual snapshots for LLMs).

**Decision:** Use dict observations with explicit keys, not dataclasses.

**Consequences:**
- ✅ Easy to extend (add 'visual_snapshot' key later)
- ✅ Easy to serialize for LLM APIs (JSON-compatible)
- ✅ Flexible for different agent types
- ⚠️ Less type-safe than dataclasses (but we have type hints on functions)

### ADR-006: Src/ Layout Package Structure

**Status:** Accepted

**Context:** Need package structure that ensures tests run against installed code.

**Decision:** Use src/ layout as recommended by PyOpenSci.

**Consequences:**
- ✅ Tests run against installed package (catches real issues)
- ✅ Industry standard for scientific Python
- ✅ Prevents accidental imports from development directory
- ✅ Clean separation of source and tests

---

_Generated by BMAD Decision Architecture Workflow_
_Date: 2025-11-17_
_For: Morgan_
_Architecture Version: 1.0 (Phase 1 Validation)_
