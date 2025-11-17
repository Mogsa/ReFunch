# Brainstorming Session Results

**Session Date:** 2025-11-17
**Facilitator:** Brainstorming Coach
**Participant:** Morgan

## Session Start

**Project Context**: FuncBench - Python-based AI reasoning benchmark

**Core Innovation**: Quick benchmark testing cognitive mapping under temporal shift
- Tests if AI can build and maintain internal spatial-temporal models
- 2D function with evolving maximum + partial observability (fog-of-war)
- Forces agents to answer: "Where am I? What can I see? How is this changing? Where should I go?"

**Key Capabilities Tested**:
1. **Spatial Localization** - Build mental map from limited local observations
2. **Temporal Pattern Detection** - Recognize how the function evolves over time
3. **Memory & Prediction** - Remember past observations and anticipate future states
4. **Strategic Navigation** - Balance exploration vs exploitation with incomplete info

**Design Priorities**:
- Fast to run (minutes not hours)
- Easy to set up (pip install and go)
- Clear to interpret (obvious if AI "gets it")
- Simple to extend (configurable difficulty/patterns)

**First Principles Analysis Applied**:
- Separated core engine (headless API) from visualization layer
- Identified minimal viable components vs nice-to-haves
- Recognized unique value: isolating cognitive mapping in controlled environment
- Discovered extension opportunities: difficulty levels, function zoo, multi-agent, ablation testing

**Approach Selected**: Advanced Elicitation (First Principles) completed → Moving to brainstorming techniques

## Executive Summary

**Topic:** FuncBench AI Reasoning Benchmark - Dynamic optimization with pattern learning

**Session Goals:** Brainstorm features, technical approaches, visualization strategies, and benchmark design for an AI reasoning benchmark testing adaptive learning in non-stationary environments

**Techniques Used:** First Principles Analysis, Mind Mapping (brief)

**Total Ideas Generated:** 15+ architectural insights and design decisions

### Key Themes Identified:

1. **Simplicity First** - Build fast MVP, iterate from there rather than over-planning
2. **Performance Matters** - Real-time rendering is essential, matplotlib too slow
3. **Dual Perspective Design** - Agent's limited 2D view vs full 3D observation mode
4. **Game-First Approach** - Human playability validates fun factor before AI implementation
5. **Constraint-Based Movement** - Agent rides the function curve (X control, Y automatic)

## Technique Sessions

### Session 1: First Principles Analysis (Advanced Elicitation)

**Goal**: Break down FuncBench to fundamental truths and rebuild from core principles.

**Key Insights**:
- Identified core capabilities being tested: spatial localization, temporal pattern detection, memory/prediction, strategic navigation
- Separated minimal viable components from nice-to-haves
- Recognized unique value proposition: isolating cognitive mapping in controlled environment
- Discovered extension opportunities: difficulty levels, function zoo, multi-agent scenarios, ablation testing
- Clarified the four fundamental questions AI must answer: "Where am I? What can I see? How is this changing? Where should I go?"

**Design Decisions From Analysis**:
- Core engine should be headless/API-first
- Visualization layer should be pluggable/optional
- Fast execution critical (minutes not hours)
- Easy setup essential (pip install and go)
- Clear interpretability required (obvious if AI "gets it")

### Session 2: Mind Mapping (Brief)

**Goal**: Map system architecture and component relationships.

**Approach**: Started exploring primary branches but user identified readiness to build rather than continue brainstorming.

**Key Decision**: Pivot to action - build fast, iterate, learn by doing. Moved to convergent phase to identify immediate priorities.

## Idea Categorization

### Immediate Opportunities

_Ideas ready to implement now_

1. **Real-time rendering system** using PyGame/Pyglet instead of matplotlib
2. **Side-scroller movement model** - Agent controls X, Y follows f(x) automatically
3. **Human playability first** - Keyboard controls to validate game feel before AI
4. **Dual view prototype** - Simple 2D agent view + 3D overview window
5. **Basic sine wave test** - Simple periodic function to prove the concept
6. **Local observation radius** - Calculate visible neighborhood around agent
7. **Gradient indicators** - Show if agent is going uphill/downhill

### Future Innovations

_Ideas requiring development/research_

1. **Function zoo** - Library of temporal patterns with known difficulty levels
2. **Curriculum learning** - Progressive difficulty from easy to hard patterns
3. **Multi-agent competition** - Multiple AIs exploring same evolving function
4. **Ablation testing framework** - Remove capabilities to isolate what matters
5. **Transfer learning tests** - Train on one pattern family, test on another
6. **Configurable difficulty parameters** - Observation radius, change speed, pattern complexity
7. **Benchmark leaderboard** - Compare AI approaches systematically
8. **Replay system** - Record and playback agent behavior for analysis

### Moonshots

_Ambitious, transformative concepts_

1. **3D/nD function spaces** - Extend beyond 2D once concept proven
2. **Adversarial function generation** - Functions specifically designed to fool certain AI strategies
3. **Emergent behavior discovery** - What novel strategies do AIs develop?
4. **Human vs AI tournaments** - Competitive benchmark between human players and AI agents
5. **Real-world mapping** - Apply cognitive mapping insights to robotics/navigation

### Insights and Learnings

_Key realizations from the session_

1. **Build velocity matters** - For dissertation timelines, working prototype beats perfect planning
2. **Game framing is powerful** - Making it playable immediately validates if the challenge is interesting
3. **Constraints create clarity** - X-only control with Y automatic is simpler and more elegant than free 2D movement
4. **Dual perspectives essential** - Agent's limited view (what AI sees) + god mode (what researchers see) both necessary
5. **Performance is non-negotiable** - Real-time visualization isn't optional, it's core to the benchmark value
6. **Cross-section insight** - 2D agent view as cross-section of 3D function is conceptually clean
7. **First principles pays off** - Breaking down to fundamentals revealed what's truly essential vs nice-to-have

## Action Planning

### Top 3 Priority Ideas

#### #1 Priority: Real-time Rendering System

- **Rationale**: Performance is critical - the benchmark needs smooth, continuous visualization to demonstrate agent behavior effectively. Matplotlib is too slow for real-time game-like experience.
- **Next steps**:
  1. Choose rendering library (PyGame, Pyglet, ModernGL, or similar)
  2. Implement continuous frame loop
  3. Render 2D function as heatmap/surface in real-time
  4. Test performance with dynamic function updates
- **Resources needed**: Python game/graphics library, basic game loop architecture
- **Timeline**: First working prototype with simple sine wave

#### #2 Priority: Dual View System (2D + 3D)

- **Rationale**: The 2D view represents agent's constrained perspective (cross-section of 3D function with limited radius). The 3D view provides "god mode" for researchers to understand what's happening. Both perspectives are essential.
- **Next steps**:
  1. Design 3D function surface renderer (full visibility)
  2. Design 2D cross-section view showing agent's local neighborhood
  3. Add gradient direction indicators in 2D view (uphill/downhill)
  4. Synchronize both views to same underlying function data
- **Resources needed**: 3D rendering capability, 2D heatmap/gradient visualization, view synchronization logic
- **Timeline**: Build after rendering system established

#### #3 Priority: Agent with Human Control

- **Rationale**: Human playability validates that the challenge is interesting and the game feel works BEFORE investing in AI agents. Simpler to test and iterate on game mechanics.
- **Next steps**:
  1. Define agent state (X position, Y = f(x) automatically)
  2. Implement Left/Right keyboard controls for X-axis movement
  3. Calculate local observation window (radius around current X)
  4. Show gradient perception (am I going uphill/downhill?)
  5. Constrain agent to function bounds
- **Resources needed**: Keyboard input handling, agent class/interface, observation calculation logic
- **Timeline**: Implement alongside dual view system

## Reflection and Follow-up

### What Worked Well

1. **First Principles approach** - Breaking down to fundamentals clarified what's essential vs nice-to-have
2. **Advanced Elicitation** - Deepening the initial concept before generating ideas prevented scope creep
3. **Action-oriented pivot** - Recognizing when to stop brainstorming and start building
4. **Constraint clarification** - The X-only movement model emerged through conversation, making design cleaner
5. **Focus on speed** - Keeping dissertation timeline in mind drove practical prioritization

### Areas for Further Exploration

1. **Specific rendering library choice** - Need to evaluate PyGame vs Pyglet vs alternatives for performance
2. **Function pattern design** - What temporal patterns best test cognitive mapping? (rotation, oscillation, chaotic?)
3. **Observation radius tuning** - What radius creates interesting challenge without being frustrating?
4. **Evaluation metrics** - How exactly do we score agent performance? Cumulative reward? Pattern learning speed?
5. **Baseline agents** - What simple strategies (random, greedy, predictive) make good comparisons?
6. **AI agent architecture** - What type of AI to test? RL? Transformer? Both?

### Recommended Follow-up Techniques

For future brainstorming sessions on FuncBench:
- **Morphological Analysis** - Systematically map difficulty parameters and function pattern variations
- **Journey Mapping** - Walk through researcher experience from pip install to results analysis
- **Devil's Advocate** - Challenge assumptions about what makes a good reasoning benchmark
- **SCAMPER** - Generate feature variations once MVP is working

### Questions That Emerged

1. What makes this benchmark meaningfully different from existing RL benchmarks?
2. How do we validate that it actually tests "reasoning" vs just optimization?
3. What's the minimal agent that should be able to solve the easiest version?
4. Should the function evolution be deterministic or stochastic?
5. How do we prevent overfitting to specific temporal patterns?
6. What publication venue would value this work? (NeurIPS? ICLR? CoRL?)

### Next Session Planning

- **Suggested topics**:
  - Technical architecture deep-dive (after building MVP)
  - Evaluation methodology and metrics design
  - Function pattern library design (easy → hard progression)
- **Recommended timeframe**: After MVP prototype is working and testable
- **Preparation needed**: Working prototype with at least one temporal pattern, initial human playtest results

---

_Session facilitated using the BMAD CIS brainstorming framework_
