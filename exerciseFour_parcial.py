import heapq
import matplotlib.pyplot as plt
import numpy as np
import random

ROWS, COLS = 11, 10
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

REAL_GRID_COSTS = np.array([
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

def find_path_a_star(known_costs, start, goal):
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
            if not (0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS): continue
            move_cost = known_costs[neighbor[0], neighbor[1]]
            tentative_g_score = g_score[current] + move_cost
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return None

def animate_partial_view(agent_pos, known_costs, path_taken, start_node, goal_node):
    terrain_colors = {0: '#cccccc', 1: '#2d6a4f', 2: '#fca311', 3: '#b21807'}
    path_color, robot_color, start_color, goal_color = '#a2d2ff', '#0077b6', '#52b788', '#e5383b'
    color_grid = np.zeros((ROWS, COLS, 3))
    for r in range(ROWS):
        for c in range(COLS):
            hex_color = terrain_colors.get(known_costs[r, c], '#FFFFFF').lstrip('#')
            color_grid[r, c] = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    for r, c in path_taken:
        hex_color = path_color.lstrip('#')
        color_grid[r, c] = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    hex_start = start_color.lstrip('#')
    color_grid[start_node] = tuple(int(hex_start[i:i+2], 16) for i in (0, 2, 4))
    hex_goal = goal_color.lstrip('#')
    color_grid[goal_node] = tuple(int(hex_goal[i:i+2], 16) for i in (0, 2, 4))
    hex_robot = robot_color.lstrip('#')
    color_grid[agent_pos] = tuple(int(hex_robot[i:i+2], 16) for i in (0, 2, 4))
    plt.imshow((color_grid / 255.0))
    plt.title("Partially Observable Environment")
    plt.grid(True, which='both', color='k', linewidth=0.5)
    plt.xticks(np.arange(-.5, COLS, 1), [])
    plt.yticks(np.arange(-.5, ROWS, 1), [])
    plt.pause(0.25)

if __name__ == "__main__":
    start_node, goal_node = generate_distant_nodes()
    
    known_grid_costs = np.zeros((ROWS, COLS), dtype=int)
    agent_pos = start_node
    path_taken = [agent_pos]
    total_cost_incurred = 0
    
    plt.figure(figsize=(7, 8))
    print("--- Stage 4: Partially Observable Environment ---")
    print(f"Objective: Find a path from {start_node} to {goal_node} with limited knowledge.")

    while agent_pos != goal_node:
        for dr, dc in DIRECTIONS + [(0,0)]:
            r, c = agent_pos[0] + dr, agent_pos[1] + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                known_grid_costs[r, c] = REAL_GRID_COSTS[r, c]
        
        plan_costs = np.where(known_grid_costs == 0, 1, known_grid_costs)
        planned_path = find_path_a_star(plan_costs, agent_pos, goal_node)

        if planned_path is None or len(planned_path) < 2:
            print("❌ Agent is trapped or cannot find a path based on current knowledge.")
            break
        
        next_step = planned_path[1]
        agent_pos = next_step
        path_taken.append(agent_pos)
        total_cost_incurred += REAL_GRID_COSTS[agent_pos]
        
        animate_partial_view(agent_pos, known_grid_costs, path_taken, start_node, goal_node)

    plt.title("Exploration Complete! Close window to finish.")
    plt.show()

    if agent_pos == goal_node:
        print("\n✅ Goal reached!")
        print(f"  - Task Success: Yes")
        print(f"  - Total Path Cost: {total_cost_incurred}")
    else:
        print("\n❌ Goal not reached.")