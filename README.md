# FuncBench

**First-principles AI reasoning benchmark for temporal pattern learning**

FuncBench is a minimalist benchmark environment designed to test AI agents' ability to reason about temporal dynamics with partial observability constraints. Agents navigate a 1D space tracking an evolving 2D reward function under fog-of-war conditions.

## Features

- **Temporal Functions**: Define reward functions that evolve over time with explicit dynamics
- **Partial Observability**: Fog-of-war constraints limit agent observations
- **Baseline Agents**: Random and greedy baselines for performance comparison
- **Human Play Mode**: Keyboard control for establishing human baselines
- **Real-time Visualization**: PyGame-based 2D rendering with fog-of-war visualization
- **Reproducible Results**: Deterministic evaluation with seed-based reproducibility

## Installation

```bash
pip install funcbench
```

## Quick Start

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

## Project Status

**Phase 1 MVP:** In Development

- ✅ Planning complete (PRD, Architecture, Epics)
- 🚧 Implementation in progress

## Documentation

- [Product Requirements](docs/prd.md)
- [Architecture](docs/architecture.md)
- [Epic Breakdown](docs/epics.md)

## Development

```bash
# Clone repository
git clone https://github.com/username/funcbench.git
cd funcbench

# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## Requirements

- Python >=3.9
- NumPy >=2.3.5
- PyGame-CE >=2.5.6

## License

MIT License - See [LICENSE](LICENSE) for details

## Citation

If you use FuncBench in your research, please cite:

```
@software{funcbench2025,
  author = {Morgan},
  title = {FuncBench: First-principles AI reasoning benchmark},
  year = {2025},
  url = {https://github.com/username/funcbench}
}
```
