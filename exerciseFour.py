import heapq
import matplotlib.pyplot as plt
import numpy as np
import random

ROWS, COLS = 11, 10
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

GRID_COSTS = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 3, 1, 1, 1, 1], [1, 1, 2, 2, 1, 3, 3, 2, 1, 1],
    [1, 1, 2, 1, 3, 3, 3, 2, 1, 1], [1, 1, 2, 2, 3, 3, 3, 2, 2, 1],
    [1, 1, 1, 2, 3, 1, 2, 2, 1, 1], [1, 1, 1, 1, 2, 3, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
])

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def generate_distant_nodes():
    """Generates random start and goal nodes that are far apart."""
    while True:
        start_node = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
        goal_node = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
        min_distance = (ROWS + COLS) // 2
        if start_node != goal_node and heuristic(start_node, goal_node) >= min_distance:
            return start_node, goal_node

def find_path_a_star(grid_costs, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = { (r, c): float('inf') for r in range(ROWS) for c in range(COLS) }
    g_score[start] = 0
    f_score = { (r, c): float('inf') for r in range(ROWS) for c in range(COLS) }
    f_score[start] = heuristic(start, goal)
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        for dr, dc in DIRECTIONS:
            neighbor = (current[0] + dr, current[1] + dc)
            if not (0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS):
                continue
            move_cost = grid_costs[neighbor[0], neighbor[1]]
            tentative_g_score = g_score[current] + move_cost
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return None

def animate_path(path, grid_costs, start_node, goal_node):
    plt.figure(figsize=(7, 8))
    terrain_colors = {1: '#2d6a4f', 2: '#fca311', 3: '#b21807'}
    path_color, robot_color, start_color, goal_color = '#a2d2ff', '#0077b6', '#52b788', '#e5383b'
    for position in path:
        color_grid = np.zeros((ROWS, COLS, 3))
        for r in range(ROWS):
            for c in range(COLS):
                hex_color = terrain_colors.get(grid_costs[r, c], '#FFFFFF').lstrip('#')
                color_grid[r, c] = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        for r, c in path:
            if (r, c) == position: break
            hex_color = path_color.lstrip('#')
            color_grid[r, c] = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        hex_start = start_color.lstrip('#')
        color_grid[start_node] = tuple(int(hex_start[i:i+2], 16) for i in (0, 2, 4))
        hex_goal = goal_color.lstrip('#')
        color_grid[goal_node] = tuple(int(hex_goal[i:i+2], 16) for i in (0, 2, 4))
        hex_robot = robot_color.lstrip('#')
        color_grid[position] = tuple(int(hex_robot[i:i+2], 16) for i in (0, 2, 4))
        plt.imshow((color_grid / 255.0))
        plt.title("Utility-Based Agent in Action (A* Search)")
        plt.grid(True, which='both', color='k', linewidth=0.5)
        plt.xticks(np.arange(-.5, COLS, 1), [])
        plt.yticks(np.arange(-.5, ROWS, 1), [])
        plt.pause(0.25)
    plt.title("Path Complete! Close the window to finish.")
    plt.show()

if __name__ == "__main__":
    start_node, goal_node = generate_distant_nodes()
    print("--- Stage 4: Fully Observable Environment ---")
    print(f"Objective: Find the minimum cost path from {start_node} to {goal_node}")
    found_path = find_path_a_star(GRID_COSTS, start_node, goal_node)
    if found_path:
        total_cost = sum(GRID_COSTS[r, c] for r, c in found_path[1:])
        print(f"✅ Path found!")
        print(f"  - Task Success: Yes")
        print(f"  - Total Path Cost: {total_cost}")
        print("\nStarting animation...")
        animate_path(found_path, GRID_COSTS, start_node, goal_node)
        print("Animation finished.")
    else:
        print(f"❌ Could not find a path.")