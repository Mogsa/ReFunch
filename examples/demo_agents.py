#!/usr/bin/env python
"""Mini demo comparing RandomAgent vs GreedyAgent on different scenarios.

This demo showcases the two baseline agents on various tasks to demonstrate:
1. Random baseline (lower bound - no intelligence)
2. Greedy baseline (upper reactive bound - hill climbing, no learning)

Run: python examples/demo_agents.py
"""

import numpy as np
from funcbench import GaussianTranslation, Environment, RandomAgent, GreedyAgent


def print_header(title):
    """Print formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_scenario(name):
    """Print formatted scenario name."""
    print(f"\n{'─' * 80}")
    print(f"📍 {name}")
    print("─" * 80)


def run_agent(agent, func, episode_length=50, show_steps=False):
    """Run an agent and return performance metrics."""
    env = Environment(func, episode_length=episode_length, render_mode=False)
    obs = env.reset()

    trajectory = []  # Track (timestep, position, peak_pos, reward)

    for step in range(episode_length):
        action = agent.get_action(obs)
        peak_pos = func.mean_start + func.velocity * obs['timestep']

        if show_steps and step < 10:  # Show first 10 steps
            action_name = ['←LEFT', '•STAY', 'RIGHT→'][action]
            print(f"  t={step:2d}: Agent@{obs['position']:6.2f} | "
                  f"Peak@{peak_pos:6.2f} | "
                  f"Reward={obs['reward']:.3f} | "
                  f"Action={action_name}")

        trajectory.append((obs['timestep'], obs['position'], peak_pos, obs['reward']))

        obs, reward, done, info = env.step(action)
        if done:
            break

    return {
        'score': info['cumulative_reward'],
        'perfect': info['perfect_score'],
        'percentage': info['cumulative_reward'] / info['perfect_score'] * 100,
        'trajectory': trajectory
    }


def compare_agents(scenario_name, func, episode_length=50, show_steps=False):
    """Compare RandomAgent vs GreedyAgent on a scenario."""
    print_scenario(scenario_name)

    # Run Random Agent
    random_agent = RandomAgent(seed=42)
    random_results = run_agent(random_agent, func, episode_length, show_steps)

    # Run Greedy Agent
    greedy_agent = GreedyAgent()
    greedy_results = run_agent(greedy_agent, func, episode_length, show_steps)

    # Print results
    print(f"\n📊 Results:")
    print(f"  RandomAgent: {random_results['score']:6.2f} / {random_results['perfect']:6.2f} "
          f"= {random_results['percentage']:5.1f}% of perfect")
    print(f"  GreedyAgent: {greedy_results['score']:6.2f} / {greedy_results['perfect']:6.2f} "
          f"= {greedy_results['percentage']:5.1f}% of perfect")

    advantage = greedy_results['score'] - random_results['score']
    print(f"  🏆 Winner: GreedyAgent by {advantage:.2f} points "
          f"({greedy_results['percentage'] - random_results['percentage']:.1f}% better)")

    return random_results, greedy_results


def visualize_trajectory(results, agent_name, num_steps=20):
    """Simple ASCII visualization of agent trajectory."""
    print(f"\n  {agent_name} Trajectory (first {num_steps} steps):")

    trajectory = results['trajectory'][:num_steps]

    # Find min/max positions for scaling
    all_positions = [p for _, p, peak, _ in trajectory] + [peak for _, _, peak, _ in trajectory]
    min_pos = min(all_positions)
    max_pos = max(all_positions)
    range_pos = max_pos - min_pos if max_pos > min_pos else 1.0

    for t, agent_pos, peak_pos, reward in trajectory:
        # Scale to 40 character width
        width = 40
        agent_idx = int((agent_pos - min_pos) / range_pos * width)
        peak_idx = int((peak_pos - min_pos) / range_pos * width)

        line = [' '] * (width + 1)
        line[peak_idx] = '▼'  # Peak marker
        line[agent_idx] = '●'  # Agent marker

        bar = ''.join(line)
        print(f"  t={t:2d}: [{bar}] R={reward:.2f}")


def main():
    """Run the demo."""
    print_header("FuncBench Agent Comparison Demo")
    print("\nComparing two baseline agents:")
    print("  • RandomAgent: Takes random actions (lower bound)")
    print("  • GreedyAgent: Follows local gradient (reactive baseline)")

    # ========================================================================
    # Scenario 1: Stationary Peak (Easy for Greedy)
    # ========================================================================
    print_header("SCENARIO 1: Stationary Peak")
    print("Peak stays at x=0.0 (no movement)")
    print("Expected: Greedy should find peak and stay there (~95%+)")
    print("Expected: Random should get occasional rewards (~30%)")

    func1 = GaussianTranslation(mean_start=0.0, velocity=0.0, sigma=2.0, seed=42)
    random1, greedy1 = compare_agents(
        "Stationary Peak (velocity=0.0)",
        func1,
        episode_length=50,
        show_steps=False
    )

    visualize_trajectory(greedy1, "GreedyAgent", num_steps=15)
    print("  Legend: ● = agent position, ▼ = peak position")
    print("  Notice: Greedy moves to peak (▼) and stays there!")

    # ========================================================================
    # Scenario 2: Slow Moving Peak (Greedy Still Good)
    # ========================================================================
    print_header("SCENARIO 2: Slowly Moving Peak")
    print("Peak starts at x=-3.0, moves right at 0.05 units/step")
    print("Expected: Greedy should track it well (~90%+)")
    print("Expected: Random should struggle (~10-20%)")

    func2 = GaussianTranslation(mean_start=-3.0, velocity=0.05, sigma=2.0, seed=42)
    random2, greedy2 = compare_agents(
        "Slow Moving Peak (velocity=0.05)",
        func2,
        episode_length=50,
        show_steps=False
    )

    visualize_trajectory(greedy2, "GreedyAgent", num_steps=15)
    print("  Notice: Greedy tracks the moving peak (▼) closely!")

    # ========================================================================
    # Scenario 3: Fast Moving Peak (Greedy Struggles)
    # ========================================================================
    print_header("SCENARIO 3: Fast Moving Peak")
    print("Peak starts at x=-10.0, moves right at 0.15 units/step")
    print("Expected: Greedy lags behind but still decent (~70-90%)")
    print("Expected: Random gets almost nothing (~0-5%)")

    func3 = GaussianTranslation(mean_start=-10.0, velocity=0.15, sigma=1.5, seed=42)
    random3, greedy3 = compare_agents(
        "Fast Moving Peak (velocity=0.15)",
        func3,
        episode_length=50,
        show_steps=True  # Show first 10 steps
    )

    visualize_trajectory(greedy3, "GreedyAgent", num_steps=20)
    print("  Notice: Greedy chases the peak but lags behind!")

    # ========================================================================
    # Summary
    # ========================================================================
    print_header("SUMMARY: Agent Performance Across Scenarios")

    scenarios = [
        ("Stationary (v=0.0)", random1, greedy1),
        ("Slow Moving (v=0.05)", random2, greedy2),
        ("Fast Moving (v=0.15)", random3, greedy3),
    ]

    print(f"\n{'Scenario':>25} | {'Random %':>10} | {'Greedy %':>10} | {'Gap':>10}")
    print("-" * 80)
    for name, rand_res, greedy_res in scenarios:
        gap = greedy_res['percentage'] - rand_res['percentage']
        print(f"{name:>25} | {rand_res['percentage']:9.1f}% | {greedy_res['percentage']:9.1f}% | {gap:9.1f}%")

    print("\n" + "=" * 80)
    print("KEY TAKEAWAYS")
    print("=" * 80)
    print("""
1. **RandomAgent (Lower Baseline):**
   - No intelligence, just random exploration
   - Gets 0-30% depending on luck
   - Establishes "floor" performance

2. **GreedyAgent (Upper Reactive Baseline):**
   - Hill-climbing strategy (follows gradient)
   - Gets 70-95% depending on scenario
   - Does NOT learn patterns - purely reactive
   - Lags behind on moving targets

3. **The Challenge for Learning Agents:**
   - Must beat RandomAgent (easy)
   - Should beat GreedyAgent (harder)
   - Ideal: Learn temporal pattern and PREDICT where peak will be
   - Target: >95% on moving peaks = learned the pattern!

4. **Why Moving Peaks Are Hard for Greedy:**
   - Greedy looks at gradient NOW
   - Peak has moved by the time greedy arrives
   - Always "one step behind"
   - Learning agent should anticipate and move ahead!
""")

    print("=" * 80)
    print("✅ Demo Complete! Try modifying parameters in the code to experiment.")
    print("=" * 80)


if __name__ == "__main__":
    main()
