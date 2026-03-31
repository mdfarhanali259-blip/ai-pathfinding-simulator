import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import agent_pathfinding_env as env



st.set_page_config(layout="wide")

st.title("🚀 AI Pathfinding Simulator")
      
# ---------------- SIDEBAR ---------------
st.sidebar.header("Controls")

width = st.sidebar.slider("Grid Width", 5, 25, 10)
height = st.sidebar.slider("Grid Height", 5, 25, 10)
density = st.sidebar.slider("Obstacle Density", 0.0, 0.5, 0.2)

algo_choice = st.sidebar.selectbox(
    "Algorithm",
    ["BFS", "UCS", "A*"]
)

# ---------------- GENERATE MAP ----------------
if st.sidebar.button("Generate Map"):
    map_str = env.generate_map_string(width, height, density)
    st.session_state["map"] = map_str 

# ---------------- LOAD MAP ----------------
if "map" in st.session_state:
    grid = env.Grid.from_map_string(st.session_state["map"])

    # Select algorithm
    if algo_choice == "BFS":
        algo = env.bfs_search
        heuristic = None
    elif algo_choice == "UCS":
        algo = env.ucs_search
        heuristic = None
    else:
        algo = env.astar_search
        heuristic = env.manhattan_distance_heuristic

    agent = env.Agent(grid.start_pos)

    sim = env.SimulationController(
        grid,
        agent,
        algo,
        heuristic
    )

    sim.plan_initial_path()

    # ---------------- DRAW FUNCTION ----------------
def draw(grid, agent_pos=None, path=None):
    import matplotlib.pyplot as plt
    import numpy as np

    display = np.zeros((grid.height, grid.width, 3))

    # Colors (RGB)
    COLORS = {
        "empty": [1, 1, 1],        # white
        "obstacle": [0, 0, 0],     # black
        "start": [0, 1, 0],        # green
        "goal": [1, 0, 0],         # red
        "path": [0, 0, 1],         # blue
        "agent": [1, 1, 0]         # yellow
    }

    # Fill grid
    for x in range(grid.width):
        for y in range(grid.height):
            cell = grid.get_cell(x, y)
            if cell.is_obstacle:
                display[y][x] = COLORS["obstacle"]
            else:
                display[y][x] = COLORS["empty"]

    # Path
    if path:
        for (x, y) in path:
            if (x, y) != grid.start_pos and (x, y) != grid.goal_pos:
                display[y][x] = COLORS["path"]

    # Start & Goal
    sx, sy = grid.start_pos
    gx, gy = grid.goal_pos
    display[sy][sx] = COLORS["start"]
    display[gy][gx] = COLORS["goal"]

    # Agent    
    if agent_pos:
        ax, ay = agent_pos
        display[ay][ax] = COLORS["agent"]

    fig, ax = plt.subplots()
    ax.imshow(display)

    ax.set_xticks(range(grid.width))
    ax.set_yticks(range(grid.height))
    ax.grid(True)
    ax.set_title("Pathfinding Simulation")

    # LEGEND
    import matplotlib.patches as mpatches
    legend_items = [
        mpatches.Patch(color=COLORS["start"], label="Start"),
        mpatches.Patch(color=COLORS["goal"], label="Goal"),
        mpatches.Patch(color=COLORS["agent"], label="Agent"),
        mpatches.Patch(color=COLORS["path"], label="Path"),
        mpatches.Patch(color=COLORS["obstacle"], label="Obstacle"),
    ]
    ax.legend(handles=legend_items, bbox_to_anchor=(1.05, 1), loc='upper left')

    ax.set_xticklabels([])
    ax.set_yticklabels([])

    return fig

# ---------------- RUN SIMULATION ----------------
if st.button("▶️ Run Simulation"):
    steps = st.slider("Steps", 1, 20, 10)

    placeholder = st.empty()  # 🔥 KEY FIX

    for i in range(steps):
        sim.run_step()

        fig = draw(grid, agent.position, sim.path)

        placeholder.pyplot(fig)  
        
