import matplotlib.pyplot as plt
import numpy as np

def draw_grid(grid, agent_pos=None, path=None, title="Grid"):
    display = np.zeros((grid.height, grid.width))

    for x in range(grid.width):
        for y in range(grid.height):
            cell = grid.get_cell(x, y)

            if cell.is_obstacle:
                display[y][x] = -1   # obstacle
            else:
                display[y][x] = 0

    # Mark start and goal
    sx, sy = grid.start_pos
    gx, gy = grid.goal_pos
    display[sy][sx] = 2
    display[gy][gx] = 3

    # Mark path
    if path:
        for (x, y) in path:
            if (x, y) != grid.start_pos and (x, y) != grid.goal_pos:
                display[y][x] = 1

    # Mark agent
    if agent_pos:
        ax, ay = agent_pos
        display[ay][ax] = 4

    plt.imshow(display, cmap='viridis')
    plt.title(title)
    plt.colorbar()
    plt.pause(0.5)
    plt.clf()