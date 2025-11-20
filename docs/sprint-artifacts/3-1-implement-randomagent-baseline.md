# Story 3.1: Implement RandomAgent Baseline

**Epic:** Epic 3 - Baseline Agents & Evaluation
**Story ID:** 3.1
**Status:** done
**Created:** 2025-11-18
**Assigned To:** Dev Agent

---

## Story

**As a** researcher,
**I want** a random agent that takes actions uniformly at random,
**So that** I can establish the lower bound of performance (no learning baseline).

---

## Acceptance Criteria

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

---

## Tasks

### Task 1: Implement RandomAgent Class
- [ ] Add RandomAgent class to src/funcbench/agent.py
- [ ] Inherit from Agent abstract base class
- [ ] Implement __init__ with optional seed parameter
- [ ] Initialize NumPy random number generator

### Task 2: Implement get_action Method
- [ ] Implement get_action(observation: dict) -> int
- [ ] Return random integer from {0, 1, 2}
- [ ] Use self.rng.integers(0, 3) for uniform sampling
- [ ] Ignore observation (random baseline doesn't use it)

### Task 3: Add Documentation
- [ ] Write comprehensive NumPy-style docstring for RandomAgent
- [ ] Document seed parameter and reproducibility
- [ ] Include usage examples in docstring
- [ ] Explain purpose as no-learning baseline

### Task 4: Create Tests
- [ ] Add tests to tests/test_agent.py or create new test file
- [ ] Test reproducibility with same seed
- [ ] Test different sequences with different seeds
- [ ] Test action distribution uniformity
- [ ] Verify actions are in valid range [0, 1, 2]

---

## Prerequisites

- Story 2.1: Implement Agent Abstract Base Class and Action Constants (DONE)

---

## Technical Notes

**Architecture References:**
- Use np.random.default_rng() (new NumPy random API, not legacy np.random.seed())
- Seed enables reproducible experiments (Architecture NFR6)
- Random agent establishes floor performance - any learning should beat this
- Ignores observation completely (doesn't look at gradient or reward)
- Reference: Architecture Section "Reproducibility" and FR26

**Implementation Guidance:**
- Follow naming conventions: PascalCase for class (RandomAgent), snake_case for methods
- Use type hints for all parameters and return values
- Keep implementation simple - no complex logic needed
- Random baseline should have equal probability for all three actions

**Testing Requirements:**
- Use pytest framework
- Test determinism with seed
- Validate uniform distribution over many samples (e.g., 1000 actions)
- Ensure all actions are valid (0, 1, or 2)

---

## Definition of Done

- [ ] RandomAgent class implemented in src/funcbench/agent.py
- [ ] Class inherits from Agent and implements get_action()
- [ ] Seed parameter enables reproducible random sequences
- [ ] NumPy-style docstring included
- [ ] Unit tests created and passing
- [ ] Tests verify reproducibility and uniform distribution
- [ ] Code follows project style and conventions
- [ ] All acceptance criteria met

---

## Dev Agent Record

**Context Reference:**
- docs/sprint-artifacts/3-1-implement-randomagent-baseline.context.xml

**Implementation Notes:**
- (To be added during development)

**Test Results:**
- (To be added after testing)
