import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import agent_pathfinding_env as env
import visualizer as vls
print("--- Setting Up Maps ---")

# 1. Small Map
small_map_string = env.generate_map_string(
    width=5, height=5,
    obstacle_density=0.1,
    start_pos=(0,0),
    goal_pos=(4,4)
)
small_grid = env.Grid.from_map_string(small_map_string)
print(f"\nSmall Map:\n{small_map_string}")

# 2. Medium Map
medium_map_string = env.generate_map_string(width=15, height=15, obstacle_density=0.2)
medium_grid = env.Grid.from_map_string(medium_map_string)
print("\nMedium Map Loaded")

# 3. Large Map
large_map_string = env.generate_map_string(width=25, height=25, obstacle_density=0.25)
large_grid = env.Grid.from_map_string(large_map_string)
print("\nLarge Map Loaded")

# 4. Dynamic Map
dynamic_map = """
S.X
.D.
.G.
"""
dynamic_grid = env.Grid.from_map_string(dynamic_map)

if dynamic_grid.dynamic_obstacles:
    dynamic_grid.dynamic_obstacles[0].movement_pattern = [(-1,0)]

print(f"\nDynamic Map:\n{dynamic_map}")

# ---------------- CONFIG ----------------
map_configs = [
    {'name': 'Small', 'map_string': small_map_string, 'start_pos': small_grid.start_pos, 'goal_pos': small_grid.goal_pos},
    {'name': 'Medium', 'map_string': medium_map_string, 'start_pos': medium_grid.start_pos, 'goal_pos': medium_grid.goal_pos},
    {'name': 'Large', 'map_string': large_map_string, 'start_pos': large_grid.start_pos, 'goal_pos': large_grid.goal_pos},
    {'name': 'Dynamic', 'map_string': dynamic_map, 'start_pos': dynamic_grid.start_pos, 'goal_pos': dynamic_grid.goal_pos}
]

algorithms = [
    {'name': 'BFS', 'function': env.bfs_search, 'heuristic': None},
    {'name': 'UCS', 'function': env.ucs_search, 'heuristic': None},
    {'name': 'A*', 'function': env.astar_search, 'heuristic': env.manhattan_distance_heuristic}
]

# ---------------- RUN EXPERIMENT ----------------
results_df = env.conduct_full_experiment(map_configs, algorithms)

print("\n--- RESULTS ---")
print(results_df)

# Save results
results_df.to_csv("results.csv", index=False)

# ---------------- PLOTS ----------------
plt.figure(figsize=(10,5))
sns.barplot(data=results_df, x='map_name', y='execution_time_ms', hue='algorithm')
plt.title("Execution Time")
plt.show()

plt.figure(figsize=(10,5))
sns.barplot(data=results_df, x='map_name', y='nodes_expanded', hue='algorithm')
plt.title("Nodes Expanded")
plt.show()

# ---------------- VISUAL SIMULATION ----------------
print("\n--- Visual Simulation ---")

grid = env.Grid.from_map_string(dynamic_map)

if grid.dynamic_obstacles:
    grid.dynamic_obstacles[0].movement_pattern = [(-1,0)]

agent = env.Agent(grid.start_pos)

sim = env.SimulationController(
    grid,
    agent,
    env.astar_search,
    env.manhattan_distance_heuristic
)

sim.plan_initial_path()

plt.figure()

for step in range(10):
    print(f"\nStep {step+1}")

    vls.draw_grid(
        grid,
        agent_pos=agent.position,
        path=sim.path,
        title=f"Step {step+1}"
    )

    if not sim.run_step():
        break

plt.close()

print("\nFinal Position:", agent.position)