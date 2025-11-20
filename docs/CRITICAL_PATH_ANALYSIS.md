# FuncBench - Critical Path Analysis
**Date:** 2025-11-18
**Purpose:** Identify which stories are critical to develop NOW vs. which can be deferred

---

## Current Status Summary

| Epic | Status | Stories Done | Stories Total | Completion |
|------|--------|--------------|---------------|------------|
| Epic 1: Foundation & Functions | ✅ COMPLETE | 5/5 | 5 | 100% |
| Epic 2: Environment & Agents | 🟡 NEARLY DONE | 7/8 | 8 | 87.5% |
| Epic 3: Baseline Agents | ❌ NOT STARTED | 0/5 | 5 | 0% |
| Epic 4: Visualization | ❌ NOT STARTED | 0/8 | 8 | 0% |
| Epic 5: Human Play | ❌ NOT STARTED | 0/3 | 3 | 0% |
| Epic 6: Testing & Distribution | ❌ NOT STARTED | 0/5 | 5 | 0% |

**Total Progress:** 12/34 stories (35%)

---

## CRITICAL ISSUE: You Cannot Test the Benchmark Yet! 🚨

**Why?** You have the environment system (Epic 2) but **ZERO concrete agents** to run.

**What's Missing:**
- Story 2.1 only provides the `Agent` **abstract base class** (ABC)
- You cannot call `env.run()` without a concrete agent implementation
- Epic 3 contains the agent implementations, but they're all in "backlog" status

---

## CRITICAL PATH: Minimum Viable Testing (3 Stories) 🎯

### **TIER 0: ABSOLUTELY CRITICAL (Cannot test without these)**

#### Story 3.1: Implement RandomAgent ⭐⭐⭐⭐⭐
**Priority:** URGENT - BLOCKING ALL TESTING
**Effort:** Small (~30-45 minutes)
**Why Critical:**
- This is the ONLY way to actually run an episode right now
- You literally cannot call `env.run(agent)` without a concrete agent
- Provides the simplest possible baseline (random actions)
- Enables end-to-end validation of the entire system

**What You'll Be Able to Do:**
```python
from funcbench import GaussianTranslation, Environment, RandomAgent

func = GaussianTranslation(velocity=0.1, seed=42)
env = Environment(func, episode_length=1000)
agent = RandomAgent(seed=42)

# FINALLY RUN THE BENCHMARK!
score = env.run(agent)
print(f"Score: {score:.2f}")
history = env.get_history()
print(f"Episode executed {len(history)} steps")
```

**Dependencies:** None (only needs Epic 2 which is done)

---

### **TIER 1: HIGHLY RECOMMENDED (For meaningful testing)**

#### Story 3.2: Implement GreedyAgent ⭐⭐⭐⭐
**Priority:** HIGH
**Effort:** Small (~45-60 minutes)
**Why Important:**
- Provides intelligent baseline for comparison
- Tests if agents can beat simple hill-climbing
- Validates that gradient observation is useful
- Enables comparative analysis (random vs. greedy vs. custom agents)

**What This Enables:**
```python
from funcbench import RandomAgent, GreedyAgent

random_agent = RandomAgent(seed=42)
greedy_agent = GreedyAgent()

random_score = env.run(random_agent)
greedy_score = env.run(greedy_agent)

print(f"Random: {random_score:.2f}")
print(f"Greedy: {greedy_score:.2f}")
print(f"Improvement: {greedy_score - random_score:.2f}")
```

**Dependencies:** Story 3.1 (for comparison)

---

#### Story 3.3: Multi-Episode Evaluation ⭐⭐⭐
**Priority:** MEDIUM-HIGH
**Effort:** Medium (~1-2 hours)
**Why Important:**
- Run multiple episodes automatically
- Get statistics (mean, std, best scores)
- Track learning curves over episodes
- Essential for rigorous benchmarking

**What This Enables:**
```python
from funcbench.evaluation import run_episodes

results = run_episodes(env, agent, n_episodes=100)
print(f"Mean Score: {results['mean_score']:.2f}")
print(f"Std Dev: {results['std_score']:.2f}")
print(f"Best: {results['best_score']:.2f}")
```

**Dependencies:** Stories 3.1, 3.2 (agents to evaluate)

---

## DEFERRED: Stories You DON'T Need Now

### **Epic 2: Story 2.8 - Environment Unit Tests**
**Status:** ❌ SKIP FOR NOW
**Why Defer:**
- Environment already has 140 passing tests
- Just adds marginal test coverage
- Doesn't enable new functionality
- You need agents first, not more tests

**When to Revisit:** After Epic 3 is done, if you want 100% coverage

---

### **Epic 3: Stories 3.4-3.5 - Data Persistence & Tests**

#### Story 3.4: Episode Data Persistence
**Status:** ⏸️ DEFER
**Why Defer:**
- Save/load episode data to JSON
- Nice for research reproducibility
- But not needed for initial testing
- Can add later when publishing results

**When to Revisit:** When you want to save experiment results

#### Story 3.5: Baseline Agent Tests
**Status:** ⏸️ DEFER
**Why Defer:**
- More test coverage
- Not blocking functionality
- Can add as agents stabilize

**When to Revisit:** Before publishing the package

---

### **Epic 4: Visualization System (All 8 Stories)**
**Status:** ⏸️ DEFER ENTIRE EPIC
**Why Defer:**
- Visualization is for human understanding, not required for testing
- You can run episodes headless (`render_mode=False`)
- All 8 stories are significant work (~8-12 hours total)
- Benchmark works without visualization

**What This Epic Contains:**
- 4.1: PyGame window setup
- 4.2: 2D function cross-section rendering
- 4.3: Fog-of-war visualization
- 4.4: Agent position indicators
- 4.5: Score HUD display
- 4.6: Historical trail rendering
- 4.7: Environment integration
- 4.8: Visualization tests

**When to Revisit:**
- After Epic 3 is complete
- When you want to demo the benchmark visually
- When implementing human play mode (Epic 5)

**Note:** Story 2.6 already implemented `render_mode` parameter, so visualization infrastructure exists. Epic 4 just implements the actual rendering.

---

### **Epic 5: Human Play (All 3 Stories)**
**Status:** ⏸️ DEFER ENTIRE EPIC
**Why Defer:**
- Requires Epic 4 (visualization) to be useful
- Human play is for validation, not core testing
- Can test with AI agents first

**What This Epic Contains:**
- 5.1: HumanAgent with keyboard input
- 5.2: Human score tracking
- 5.3: Play example script

**When to Revisit:**
- After Epic 4 visualization is complete
- When you want human baseline scores
- When validating benchmark difficulty

---

### **Epic 6: Testing & Distribution (All 5 Stories)**
**Status:** ⏸️ DEFER ENTIRE EPIC
**Why Defer:**
- Package distribution for PyPI
- Comprehensive integration tests
- Documentation and examples
- Not needed for development/testing

**What This Epic Contains:**
- 6.1: Reproducibility test suite
- 6.2: Integration test suite
- 6.3: Package build configuration
- 6.4: README and documentation
- 6.5: Example scripts

**When to Revisit:**
- When preparing for public release
- When publishing research using the benchmark
- When sharing with collaborators

---

## Recommended Development Plan

### **Phase 1: Get to Testable State (TODAY)**
**Goal:** Run your first successful episode end-to-end

1. ✅ Skip Story 2.8 (environment tests)
2. 🎯 **Implement Story 3.1: RandomAgent** (~30-45 min)
3. 🎯 **Implement Story 3.2: GreedyAgent** (~45-60 min)
4. ✅ Test the benchmark with both agents

**Total Time:** ~1.5-2 hours
**Result:** You can run episodes and compare agent performance

---

### **Phase 2: Rigorous Evaluation (NEXT)**
**Goal:** Multi-episode evaluation and statistics

5. 🎯 **Implement Story 3.3: Multi-Episode Evaluation** (~1-2 hours)
6. ✅ Run 100-episode comparisons
7. ✅ Analyze results and validate benchmark

**Total Time:** 1-2 hours
**Result:** Statistical analysis of agent performance

---

### **Phase 3: Visualization (LATER)**
**Goal:** See the benchmark in action

8. 📊 Implement Epic 4 stories 4.1-4.7 (~8-12 hours)
9. 📊 Test visualization with existing agents

**Total Time:** 8-12 hours
**Result:** Real-time visualization of episodes

---

### **Phase 4: Human Play (LATER)**
**Goal:** Human baseline and validation

10. 🎮 Implement Epic 5 stories 5.1-5.3 (~2-3 hours)
11. 🎮 Play the benchmark manually
12. 🎮 Compare human vs AI performance

**Total Time:** 2-3 hours
**Result:** Human baseline scores

---

### **Phase 5: Polish & Distribution (MUCH LATER)**
**Goal:** Package for publication

13. 📦 Implement Epic 6 stories 6.1-6.5 (~4-6 hours)
14. 📦 Publish to PyPI
15. 📦 Share with research community

**Total Time:** 4-6 hours
**Result:** Published Python package

---

## Critical Path Flowchart

```
Epic 1: Foundation ✅ (DONE)
    ↓
Epic 2: Environment ✅ (7/8 DONE, Story 2.8 SKIP)
    ↓
┌─────────────────────────────────────────┐
│ CRITICAL PATH - DO NOW (TODAY)          │
│                                          │
│ Story 3.1: RandomAgent  ⭐⭐⭐⭐⭐       │
│    ↓                                     │
│ Story 3.2: GreedyAgent  ⭐⭐⭐⭐         │
│    ↓                                     │
│ Story 3.3: Multi-Episode ⭐⭐⭐          │
│                                          │
│ RESULT: Testable Benchmark               │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│ DEFER - Do Later                         │
│                                          │
│ Epic 4: Visualization (8 stories)        │
│    ↓                                     │
│ Epic 5: Human Play (3 stories)           │
│    ↓                                     │
│ Epic 6: Distribution (5 stories)         │
│                                          │
│ RESULT: Polished Package                 │
└─────────────────────────────────────────┘
```

---

## Story-Level Breakdown

### Epic 1: Project Foundation & Function System ✅
| Story | Status | Critical? | Notes |
|-------|--------|-----------|-------|
| 1.1: Initialize Project Structure | ✅ DONE | ✅ Yes | Foundation complete |
| 1.2: Function2D Abstract Base Class | ✅ DONE | ✅ Yes | Core abstraction |
| 1.3: GaussianTranslation Function | ✅ DONE | ✅ Yes | Baseline function |
| 1.4: Perfect Score Calculation | ✅ DONE | ✅ Yes | Performance metric |
| 1.5: Basic Function Tests | ✅ DONE | ✅ Yes | Validation |

---

### Epic 2: Environment & Agent Execution 🟡
| Story | Status | Critical? | Notes |
|-------|--------|-----------|-------|
| 2.1: Agent Abstract Base Class | ✅ DONE | ✅ Yes | Agent interface |
| 2.2: Environment Initialization | ✅ DONE | ✅ Yes | Core environment |
| 2.3: Observation Generation | ✅ DONE | ✅ Yes | Fog-of-war |
| 2.4: Step Execution | ✅ DONE | ✅ Yes | Action handling |
| 2.5: Episode History Tracking | ✅ DONE | ✅ Yes | Data collection |
| 2.6: Run Method | ✅ DONE | ✅ Yes | Episode execution |
| 2.7: Configuration Persistence | ✅ DONE | ✅ Yes | Reproducibility |
| 2.8: Environment Unit Tests | 🔄 READY | ❌ SKIP | 140 tests already pass |

---

### Epic 3: Baseline Agents & Evaluation ❌
| Story | Status | Critical? | Effort | Notes |
|-------|--------|-----------|--------|-------|
| 3.1: RandomAgent | 📋 BACKLOG | 🎯 **TIER 0** | Small | **DO FIRST - BLOCKING** |
| 3.2: GreedyAgent | 📋 BACKLOG | 🎯 **TIER 1** | Small | **DO SECOND** |
| 3.3: Multi-Episode Evaluation | 📋 BACKLOG | 🎯 **TIER 1** | Medium | **DO THIRD** |
| 3.4: Episode Data Persistence | 📋 BACKLOG | ⏸️ DEFER | Small | Nice-to-have |
| 3.5: Baseline Agent Tests | 📋 BACKLOG | ⏸️ DEFER | Medium | More tests |

---

### Epic 4: 2D Visualization System ❌
| Story | Status | Critical? | Notes |
|-------|--------|-----------|-------|
| 4.1: PyGame Window Setup | 📋 BACKLOG | ⏸️ DEFER | Visualization infrastructure |
| 4.2: 2D Function Rendering | 📋 BACKLOG | ⏸️ DEFER | Visual cross-section |
| 4.3: Fog-of-War Visualization | 📋 BACKLOG | ⏸️ DEFER | Visual constraints |
| 4.4: Agent Indicators | 📋 BACKLOG | ⏸️ DEFER | Position markers |
| 4.5: Score HUD Display | 📋 BACKLOG | ⏸️ DEFER | Real-time metrics |
| 4.6: Historical Trail | 📋 BACKLOG | ⏸️ DEFER | Movement visualization |
| 4.7: Visualizer Integration | 📋 BACKLOG | ⏸️ DEFER | Connects to environment |
| 4.8: Visualization Tests | 📋 BACKLOG | ⏸️ DEFER | Graphics testing |

**ENTIRE EPIC: Defer until after Epic 3**

---

### Epic 5: Human Play & Validation ❌
| Story | Status | Critical? | Notes |
|-------|--------|-----------|-------|
| 5.1: HumanAgent Keyboard Input | 📋 BACKLOG | ⏸️ DEFER | Requires Epic 4 |
| 5.2: Human Score Tracking | 📋 BACKLOG | ⏸️ DEFER | Comparison metrics |
| 5.3: Human Play Example | 📋 BACKLOG | ⏸️ DEFER | Demo script |

**ENTIRE EPIC: Defer until after Epic 4**

---

### Epic 6: Testing & Package Distribution ❌
| Story | Status | Critical? | Notes |
|-------|--------|-----------|-------|
| 6.1: Reproducibility Test Suite | 📋 BACKLOG | ⏸️ DEFER | Research validation |
| 6.2: Integration Test Suite | 📋 BACKLOG | ⏸️ DEFER | End-to-end tests |
| 6.3: Package Build Config | 📋 BACKLOG | ⏸️ DEFER | PyPI distribution |
| 6.4: README & Documentation | 📋 BACKLOG | ⏸️ DEFER | User guides |
| 6.5: Example Scripts | 📋 BACKLOG | ⏸️ DEFER | Sample code |

**ENTIRE EPIC: Defer until preparing for public release**

---

## Summary: What to Do NOW

### ✅ SKIP
- ❌ Story 2.8: Environment Unit Tests (already have 140 tests)

### 🎯 IMPLEMENT TODAY (Critical Path)
1. ⭐⭐⭐⭐⭐ **Story 3.1: RandomAgent** (30-45 min)
2. ⭐⭐⭐⭐ **Story 3.2: GreedyAgent** (45-60 min)
3. ⭐⭐⭐ **Story 3.3: Multi-Episode Evaluation** (1-2 hours)

**Total Time:** 2-4 hours
**Result:** Working, testable benchmark with baseline comparisons

### ⏸️ DEFER TO LATER
- Epic 3: Stories 3.4-3.5 (data persistence, more tests)
- Epic 4: All 8 stories (visualization)
- Epic 5: All 3 stories (human play)
- Epic 6: All 5 stories (packaging, distribution)

---

## Questions Answered

**Q: Can I test the benchmark now?**
A: NO - You have no concrete agent to run. Need Story 3.1 (RandomAgent) first.

**Q: What's the minimum to get testing?**
A: Story 3.1 only (30-45 minutes). Then you can run `env.run(RandomAgent())`.

**Q: Do I need visualization to test?**
A: NO - Environment already supports headless mode (`render_mode=False`). Visualization is for demos/understanding, not testing.

**Q: Do I need Story 2.8 (more environment tests)?**
A: NO - Environment has 140 passing tests already. More tests don't enable new functionality.

**Q: When should I do Epic 4 (visualization)?**
A: After you've validated the benchmark with Epic 3 agents. Visualization is polish, not core functionality.

**Q: How long until I can test the benchmark?**
A: ~30-45 minutes if you implement Story 3.1 (RandomAgent) now.

---

## Recommendation

**Start with Story 3.1 (RandomAgent) immediately.**

This single story unblocks everything and lets you finally run end-to-end episodes. Once you have that working, you can decide if you want to add GreedyAgent for comparison or move to visualization.

**Do NOT waste time on:**
- Story 2.8 (more tests you don't need)
- Epic 4 (visualization can wait)
- Epic 5 (human play requires visualization)
- Epic 6 (packaging is premature)

**Bottom line:** You're 30-45 minutes away from a working benchmark. Focus there.
