# FuncBench - Product Requirements Document

**Author:** Morgan
**Date:** 2025-11-17
**Version:** 1.0

---

## Executive Summary

FuncBench is a first-principles AI reasoning benchmark that tests whether AI agents (particularly LLMs) can learn temporal patterns and build internal predictive models. Unlike arbitrary grid-world benchmarks (ARC, Authmn), FuncBench strips reasoning to its essence: can an agent discover and exploit an underlying temporal rule in a continuous optimization task?

The first experiment tests the simplest temporal pattern: a 1D agent tracking a reward peak that translates linearly over time. The agent sees only local gradient information and must infer the global temporal dynamics to maximize cumulative reward.

### What Makes This Special

**Theoretical Elegance Over Arbitrary Complexity**: Current reasoning benchmarks use grid worlds that are simple but fundamentally arbitrary. FuncBench takes a first-principles approach - the simplest possible test of temporal reasoning using continuous functions with explicit temporal rules. If agents can't solve linear translation, more complex patterns won't work. If they can, we have a foundation for scaling complexity systematically.

**Testing LLMs on Visual-Temporal Reasoning**: This benchmark tests whether multimodal LLMs can extract temporal patterns from sequential visual observations and form internal predictive models - a capability we don't yet understand well.

---

## Project Classification

**Technical Type:** developer_tool
**Domain:** scientific
**Complexity:** medium

FuncBench is a Python research library for AI reasoning evaluation. It provides a controlled environment for testing temporal pattern learning with visual observations, reproducible evaluation metrics, and extensible function patterns.

**Domain Context - Scientific Computing Requirements:**
- Reproducibility: Deterministic function evolution, seeded randomness, version-locked dependencies
- Validation methodology: Theoretical perfect score provides ground truth, clear performance gaps
- Computational requirements: Real-time visualization (60 FPS), efficient function evaluation
- Publication standards: Clear metrics, baseline comparisons, open-source implementation

---

## Success Criteria

**Research Validation Success:**
- LLM agents demonstrate measurable learning (score improves over episodes)
- Clear performance gap between pattern-learning agents and baselines (random, greedy)
- Consistent scoring after learning period (agent has internalized the rule)
- Theoretical perfect score provides upper bound for performance comparison

**Usability Success:**
- Researchers can run experiments in minutes, not hours
- Visual output makes it immediately clear if agent "gets it" or not
- Simple pip install setup, no complex dependencies
- Easy to extend with new temporal patterns

**Benchmark Validation:**
- Linear translation experiment proves/disproves the approach
- If successful: foundation for more complex temporal patterns
- If unsuccessful: clear failure mode indicates what's missing

---

## Product Scope

### MVP - Minimum Viable Product

**Core Engine:**
- 2D Gaussian function with temporal dynamics (mean translation)
- 1D agent with left/right/stay actions
- Local observation window (gradient snapshot + current reward)
- Episode management (timesteps, scoring, reset)
- Theoretical perfect score calculation

**Visualization:**
- Real-time PyGame rendering (60 FPS target)
- 2D agent view: cross-section showing local gradient
- 3D overview: god-mode view of full function over time
- Visual indicators: agent position, current score, perfect score gap

**Linear Translation Pattern:**
- Gaussian peak starts at left
- Translates right at constant velocity
- Configurable: peak width, translation speed, episode length

**Evaluation Framework:**
- Cumulative reward tracking
- Score vs perfect score comparison
- Learning curve visualization
- Episode replay capability

**Human Playability:**
- Keyboard controls (arrow keys) to validate game feel
- Score display during play
- Visual feedback for reward and gradient

### Growth Features (Post-MVP)

**Function Zoo:**
- Oscillating peak (sine wave)
- Accelerating translation (non-linear)
- Multiple peaks with different dynamics
- Chaotic/unpredictable patterns

**LLM Integration:**
- Visual snapshot rendering for LLM input
- LLM action parsing (text to action)
- Multi-episode learning support
- Memory/context management for LLM

**Advanced Metrics:**
- Pattern discovery detection (did agent learn the rule?)
- Convergence time measurement
- Transfer learning tests (pattern A → pattern B)
- Ablation studies (remove observation radius, remove gradient info)

**Curriculum Learning:**
- Difficulty progression (slow → fast translation)
- Pattern complexity ladder (linear → oscillating → chaotic)
- Auto-difficulty adjustment

### Vision (Future)

**2D Agent Movement:**
- Agent moves in X-Y plane on 3D function surface
- 2D temporal patterns (rotation, spirals)
- More complex spatial-temporal reasoning

**Multi-Agent Scenarios:**
- Competition between agents
- Collaborative exploration
- Comparative evaluation across AI architectures

**Benchmark Suite:**
- Standardized pattern library with difficulty ratings
- Leaderboard for different AI approaches
- Reproducible evaluation protocol
- Publication-ready results format

**Real-World Applications:**
- Apply cognitive mapping insights to robotics navigation
- Transfer learning to actual temporal prediction tasks
- Use as pre-training task for reinforcement learning

---

## Innovation & Novel Patterns

**First-Principles Benchmark Design:**
FuncBench challenges the assumption that grid worlds are necessary for reasoning tests. By using continuous functions with explicit temporal rules, we get:
- Mathematical precision (theoretical perfect score)
- Systematic complexity scaling (start simple, add complexity methodically)
- Clear interpretation (did agent learn the rule or not?)

**Visual-Temporal Learning for LLMs:**
Testing whether LLMs can extract temporal patterns from sequential visual observations is novel. Current LLM benchmarks focus on language reasoning, not visual-temporal pattern discovery with partial observability.

**Cognitive Mapping Isolation:**
Most benchmarks conflate multiple capabilities. FuncBench isolates the specific capability of building and maintaining internal spatial-temporal models under partial observability - answering: "Can the agent answer: Where am I? What can I see? How is this changing? Where should I go?"

### Validation Approach

**Experiment 1 - Linear Translation (MVP):**
- If LLMs can't learn this simplest pattern → benchmark won't work for harder patterns
- If LLMs can learn it → we have proof of concept for scaling complexity
- Baseline comparison: random agent, greedy agent (follow gradient), perfect agent (knows the rule)

**Validation metrics:**
- Learning curve: score improvement over episodes
- Convergence: score stabilizes at consistent level
- Performance gap: distance from theoretical perfect score
- Visual validation: can researcher watch replay and see agent "tracking" the peak?

**Fallback strategy:**
If LLMs fail to learn even linear patterns with visual input:
- Test with simplified observations (explicit velocity hints)
- Test with traditional RL agents to validate the task itself is learnable
- Potentially indicates LLMs need different observation modality

---

## developer_tool Specific Requirements

**Package Distribution:**
- PyPI package: `pip install funcbench`
- Conda package for scientific Python users
- GitHub repository with examples and documentation

**Programming Interface:**
- Python 3.9+ compatibility
- Clear API for defining custom functions
- Easy agent interface (observation → action)
- Configurable environment parameters

**Documentation Needs:**
- Quick-start guide (5 minutes to first experiment)
- API reference (all classes, methods, parameters)
- Example gallery (different temporal patterns)
- Research paper companion (methodology, baselines, results)

**Code Quality:**
- Type hints throughout
- Comprehensive docstrings
- Unit tests for core functions
- Integration tests for full episodes

**Developer Experience:**
- Hot-reload for rapid experimentation
- Debug mode with verbose logging
- Configurable visualization (headless mode for batch runs)
- Easy extension points for custom patterns

### Language Support

**Primary:** Python 3.9+
- NumPy for function computation
- PyGame for visualization
- Matplotlib for plotting (optional, for analysis)

**Future consideration:** Julia for performance-critical computations

### Installation Methods

**PyPI (primary):**
```bash
pip install funcbench
```

**Development install:**
```bash
git clone https://github.com/username/funcbench
cd funcbench
pip install -e .
```

**Dependencies:**
- pygame>=2.5.0 (visualization)
- numpy>=1.24.0 (computation)
- matplotlib>=3.7.0 (optional, for analysis)

### API Surface

**Core classes:**
- `Function2D`: Base class for temporal 2D functions
- `GaussianTranslation`: Linear translation experiment
- `Agent`: Abstract agent interface
- `Environment`: Episode management and scoring
- `Visualizer`: Real-time rendering

**Key methods:**
- `env.reset()`: Start new episode
- `env.step(action)`: Execute action, get observation and reward
- `env.render()`: Update visualization
- `env.get_perfect_score()`: Theoretical maximum

**Configuration:**
- Function parameters (width, velocity, bounds)
- Observation radius (fog-of-war size)
- Episode length (timesteps)
- Visualization settings (FPS, view modes)

### Code Examples

**Example 1 - Human play:**
```python
from funcbench import GaussianTranslation, Environment, HumanAgent

func = GaussianTranslation(velocity=0.1)
env = Environment(func, episode_length=1000)
agent = HumanAgent()  # Keyboard control

env.run(agent, render=True)
```

**Example 2 - LLM evaluation:**
```python
from funcbench import GaussianTranslation, Environment, LLMAgent

func = GaussianTranslation(velocity=0.1)
env = Environment(func, episode_length=1000)
agent = LLMAgent(model="gpt-4-vision")

score = env.run(agent, render=False)
print(f"Score: {score}/{env.get_perfect_score()}")
```

**Example 3 - Custom function:**
```python
from funcbench import Function2D, Environment

class MyPattern(Function2D):
    def evaluate(self, x, t):
        # Your temporal function here
        return some_function(x, t)

env = Environment(MyPattern(), episode_length=500)
```

---

## User Experience Principles

**Design Philosophy: "Fair Comparison Through Constraint Parity"**

The visualization must provide identical information to human players and AI agents. This creates a valid human baseline for evaluating AI performance - if humans can learn the pattern with limited observability, AI agents should be able to as well.

**Visual Personality:**
Scientific but engaging. Clean visualization that makes temporal dynamics immediately obvious through smooth real-time animation. Researchers should be able to watch an episode and instantly see whether the agent has "learned" the pattern or is struggling.

**Core Principle - What You See Is What The Agent Sees:**
- Human play mode has identical constraints to AI agent mode
- Same observation radius (fog-of-war)
- Same gradient information
- Same reward visibility
- This validates the task difficulty and enables fair human-AI comparison

### Key Interactions

**1. Fog-of-War Visualization:**
- Everything outside observation radius is blacked out/invisible
- Only the local function window around agent is visible
- Makes partial observability constraint visually explicit
- Helps researchers understand agent's information limitations

**2. Observable Window:**
- Local 2D cross-section of function centered on agent
- Shows gradient/slope within observation radius
- Current reward value displayed numerically and visually (color intensity)
- Gradient direction indicators (arrows/visual cues showing which way is "uphill")

**3. Historical Trail:**
- Breadcrumb path showing agent's previous positions
- Helps visualize agent's exploration strategy
- Shows if agent is "wandering" vs "tracking" the peak
- Can be toggled on/off for clarity

**4. Dual View System:**
- **Agent View (2D)**: What the agent actually observes - fog-of-war active, limited visibility
- **God View (3D)**: Full function surface over time, for researcher analysis
- **Toggle between views** to compare agent's perspective with ground truth

**5. Real-Time Feedback:**
- Current cumulative reward counter
- Theoretical perfect score (running total)
- Performance gap: how far from optimal
- Time/timestep counter

**6. Playback Controls:**
- Pause/resume during human play
- Slow-motion for analysis
- Episode replay to study agent behavior
- Frame-by-frame step through (debug mode)

**7. Human Play Mode:**
- Arrow keys: ← (move left), → (move right), ↓ (stay)
- Identical observation constraints as AI agents
- Same scoring system
- Immediate visual feedback for gradient and reward changes

**Feel:**
Responsive and smooth. Real-time rendering at 60 FPS so movement feels natural and temporal dynamics are clear. Visual changes (gradient shifts, reward updates) should be smooth, not jumpy. The agent should feel like it's "surfing" the function landscape.

---

## Functional Requirements

### Function System

**FR1:** System can define 2D temporal functions that evolve over time according to explicit rules

**FR2:** System provides Gaussian function implementation with configurable parameters (mean, standard deviation, amplitude)

**FR3:** Gaussian function supports linear translation dynamics (mean moves at constant velocity)

**FR4:** System can evaluate function at any (x, t) coordinate to get reward value

**FR5:** System calculates theoretical perfect score for any temporal function and episode length

**FR6:** Functions can define spatial bounds (left/right limits for agent movement)

**FR7:** System supports extensible function base class for implementing custom temporal patterns

### Agent System

**FR8:** Agents can take one of three actions: move left, move right, or stay in current position

**FR9:** System tracks agent position in 1D space (x-coordinate)

**FR10:** Agent receives observation including current reward value at its position

**FR11:** Agent receives local gradient information within observation radius

**FR12:** Agent receives visual snapshot of local function cross-section (for LLM agents)

**FR13:** Observation radius (fog-of-war size) is configurable per environment

**FR14:** System enforces spatial bounds (agent cannot move outside function domain)

**FR15:** Agents can be implemented via abstract interface for different AI architectures

### Episode Management

**FR16:** System can initialize new episodes with configurable episode length (timesteps)

**FR17:** System executes agent actions step-by-step, advancing time by one timestep per action

**FR18:** System tracks cumulative reward across all timesteps in an episode

**FR19:** Episode terminates when timestep limit is reached

**FR20:** System can reset environment state to start new episodes

**FR21:** System maintains episode history (timesteps, positions, rewards, actions)

**FR22:** Episodes use deterministic temporal evolution (same seed = same function dynamics)

### Scoring & Evaluation

**FR23:** System calculates real-time cumulative reward as agent acts

**FR24:** System provides theoretical perfect score (maximum possible cumulative reward)

**FR25:** System calculates performance gap (actual score vs perfect score)

**FR26:** System can compare agent performance against baseline strategies (random, greedy)

**FR27:** System tracks learning curves across multiple episodes

**FR28:** System provides episode replay capability for post-hoc analysis

**FR29:** System can save episode data for reproducible evaluation

### Visualization - Agent View (2D)

**FR30:** System renders real-time 2D agent view showing local function cross-section

**FR31:** Visualization implements fog-of-war (areas outside observation radius are blacked out)

**FR32:** Visualization shows agent position indicator on 2D cross-section

**FR33:** Visualization displays current reward value numerically and visually (color/intensity)

**FR34:** Visualization shows gradient direction indicators within observable window

**FR35:** Visualization renders historical trail showing agent's previous positions

**FR36:** Historical trail can be toggled on/off

**FR37:** Visualization updates at 60 FPS for smooth real-time feedback

**FR38:** Visualization shows current cumulative score

**FR39:** Visualization shows theoretical perfect score

**FR40:** Visualization displays performance gap (score difference)

**FR41:** Visualization shows current timestep / total timesteps

### Visualization - God View (3D)

**FR42:** System renders 3D overview showing full function surface over time

**FR43:** God view shows agent position on the 3D surface

**FR44:** God view visualizes temporal dynamics (peak translation visible)

**FR45:** Users can toggle between agent view (2D) and god view (3D)

**FR46:** God view provides spatial reference for understanding agent's limited perspective

### Human Play Mode

**FR47:** Users can control agent using keyboard input (arrow keys)

**FR48:** Human play mode has identical observation constraints as AI agents

**FR49:** Human players see same fog-of-war visualization as AI agents

**FR50:** Human play mode uses same scoring system as AI evaluation

**FR51:** Human play receives identical gradient information as AI agents

**FR52:** System tracks human player scores for human-AI comparison

**FR53:** Keyboard controls are responsive with minimal input lag

### Playback & Analysis

**FR54:** System can pause and resume episodes during execution

**FR55:** System supports slow-motion playback for detailed analysis

**FR56:** System can replay completed episodes

**FR57:** System supports frame-by-frame stepping in debug mode

**FR58:** Playback preserves all visualization elements (fog-of-war, trails, scores)

### Configuration & Parameters

**FR59:** Users can configure function parameters (peak width, translation velocity, bounds)

**FR60:** Users can configure observation radius (fog-of-war size)

**FR61:** Users can configure episode length (number of timesteps)

**FR62:** Users can configure visualization settings (FPS, view mode, trail length)

**FR63:** Users can enable/disable visualization (headless mode for batch evaluation)

**FR64:** System supports configuration via Python API and config files

**FR65:** Configuration changes take effect on next episode reset

### LLM Integration (Post-MVP)

**FR66:** System can render visual snapshots in format suitable for multimodal LLMs

**FR67:** System can parse LLM text output to action commands

**FR68:** LLM agents can maintain context across multiple timesteps within episode

**FR69:** System supports multiple LLM providers (OpenAI, Anthropic, local models)

**FR70:** System manages LLM API calls and rate limiting

### Extension & Research Tools

**FR71:** System provides base classes for implementing custom temporal functions

**FR72:** Researchers can define new function patterns without modifying core code

**FR73:** System provides utilities for common patterns (oscillation, rotation, acceleration)

**FR74:** System exports episode data in standard formats (CSV, JSON) for external analysis

**FR75:** System generates visualizations for research papers (matplotlib plots, animations)

---

## Non-Functional Requirements

### Performance

**Why it matters:** Real-time visualization is essential for validating that agents have learned the pattern. Researchers need smooth, responsive feedback to understand agent behavior.

**NFR1: Real-Time Rendering** - Visualization maintains 60 FPS during episode execution on standard research hardware (M1 MacBook, modern Linux workstation)

**NFR2: Efficient Function Evaluation** - System evaluates function at any (x, t) coordinate in < 1ms to support real-time queries

**NFR3: Fast Episode Execution** - Complete 1000-timestep episode in < 20 seconds with visualization enabled

**NFR4: Headless Performance** - Batch evaluation of 100 episodes completes in < 5 minutes with visualization disabled

**NFR5: Responsive Controls** - Human keyboard input has < 50ms latency between keypress and visual feedback

### Reproducibility

**Why it matters:** Scientific research requires reproducible results. Different researchers must be able to replicate experiments exactly.

**NFR6: Deterministic Evolution** - Given same random seed, function dynamics are identical across runs and platforms

**NFR7: Version Locking** - Episode data includes library version, function parameters, and random seed for exact reproduction

**NFR8: Platform Independence** - Results are numerically identical on macOS, Linux, and Windows (no platform-specific behaviors)

**NFR9: Dependency Pinning** - Package specifies exact dependency versions that guarantee reproducible computation

**NFR10: Episode Serialization** - Complete episode state can be saved and reloaded for exact replay

### Accuracy & Precision

**Why it matters:** Theoretical perfect score provides ground truth for evaluation. Numerical errors would invalidate performance comparisons.

**NFR11: Numerical Precision** - Function evaluations use float64 precision to minimize cumulative error over long episodes

**NFR12: Gradient Accuracy** - Gradient calculations accurate to within 0.1% of analytical gradient

**NFR13: Perfect Score Calculation** - Theoretical perfect score calculated analytically (not via simulation) for exact ground truth

**NFR14: Score Consistency** - Cumulative reward calculation has < 0.01% floating-point error over 10,000 timesteps

### Usability

**Why it matters:** Research tool must be accessible to AI researchers who may not be software engineering experts. Lower barrier to entry = broader adoption.

**NFR15: Fast Setup** - From `pip install funcbench` to running first episode < 5 minutes (including reading quick-start)

**NFR16: Clear API** - Core API uses intuitive naming and requires < 10 lines of code for basic usage

**NFR17: Helpful Errors** - Error messages specify the problem, the cause, and how to fix it (no cryptic stack traces)

**NFR18: Documentation Coverage** - All public APIs have docstrings with examples; quick-start guide exists

**NFR19: Example Quality** - Example gallery covers common use cases (human play, LLM evaluation, custom functions)

### Extensibility

**Why it matters:** Researchers need to test their own temporal patterns. System must support custom functions without core modifications.

**NFR20: Plugin Architecture** - New function patterns can be added by subclassing `Function2D` without modifying library code

**NFR21: Configuration Flexibility** - All environment parameters (bounds, radius, episode length) are configurable

**NFR22: Agent Interface** - Custom agents can be implemented via simple abstract interface (`get_action(observation)`)

**NFR23: Visualization Hooks** - Custom visualization layers can be added without modifying rendering core

### Compatibility

**NFR24: Python Version Support** - Compatible with Python 3.9, 3.10, 3.11, 3.12

**NFR25: Operating Systems** - Runs on macOS, Linux (Ubuntu 20.04+), Windows 10+

**NFR26: Dependency Minimalism** - Core functionality requires only numpy and pygame (matplotlib optional)

---

_This PRD captures the essence of FuncBench - a first-principles approach to testing whether AI agents can learn temporal patterns through visual observation. By starting with the simplest possible experiment (linear Gaussian translation), we validate the benchmark concept before investing in more complex patterns. The human-AI comparison through identical constraints ensures we're testing real reasoning capability, not just optimization._

_Created through collaborative discovery between Morgan and AI facilitator._

