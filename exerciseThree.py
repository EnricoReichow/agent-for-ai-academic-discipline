import random
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
from matplotlib.colors import ListedColormap

GRID_SIZE = 10
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

DEFINED_OBSTACLES = {
    (0, 5),
    (1, 4), (1, 7),
    (2, 3),
    (3, 3),
    (4, 3), (4, 6),
    (5, 8),
    (6, 4),
    (7, 3), (7, 5), (7, 6),
    (8, 6),
    (9, 5)
}

def find_path_bfs(start_node, goal_node, obstacles):
    """
    Finds the shortest path between 'start_node' and 'goal_node' using BFS.
    Returns a list of tuples representing the path, or None if no path exists.
    """
    if start_node == goal_node:
        return [start_node]

    queue = deque([start_node])
    predecessors = {start_node: None}

    while queue:
        current_node = queue.popleft()

        if current_node == goal_node:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = predecessors[current_node]
            path.reverse()
            return path

        for dx, dy in DIRECTIONS:
            neighbor_x, neighbor_y = current_node[0] + dx, current_node[1] + dy
            neighbor = (neighbor_x, neighbor_y)

            if (0 <= neighbor_x < GRID_SIZE and 0 <= neighbor_y < GRID_SIZE and
                    neighbor not in obstacles and
                    neighbor not in predecessors):
                predecessors[neighbor] = current_node
                queue.append(neighbor)
    
    return None

def animate_path(path, start_node, goal_node, obstacles):
    """
    Animates the robot's movement, showing the traversed path, and waits for user input to close.
    """
    plt.figure(figsize=(7, 7))
    
    cmap = ListedColormap(['#FFFFFF', '#6c757d', '#d00000', '#52b788', '#a2d2ff', '#0077b6'])

    visited_path = set()

    for position in path:
        visited_path.add(position)
        grid = np.zeros((GRID_SIZE, GRID_SIZE))

        for obs in obstacles:
            grid[obs] = 1
        
        for visited_pos in visited_path:
            grid[visited_pos] = 4
        
        grid[start_node] = 3
        grid[goal_node] = 2
        grid[position] = 5

        plt.imshow(grid, cmap=cmap)
        plt.title("Goal-Based Agent in Action")
        plt.grid(True, which='both', color='k', linewidth=0.5)
        plt.xticks(np.arange(-.5, GRID_SIZE, 1), [])
        plt.yticks(np.arange(-.5, GRID_SIZE, 1), [])
        plt.pause(0.4) 
        plt.clf()

    final_grid = np.zeros((GRID_SIZE, GRID_SIZE))
    for obs in obstacles:
        final_grid[obs] = 1
    
    for pos in path:
        final_grid[pos] = 4
    
    final_grid[start_node] = 3
    final_grid[goal_node] = 2
    
    plt.imshow(final_grid, cmap=cmap)
    plt.title("Path Complete! Close the window to continue.")
    plt.grid(True, which='both', color='k', linewidth=0.5)
    plt.xticks(np.arange(-.5, GRID_SIZE, 1), [])
    plt.yticks(np.arange(-.5, GRID_SIZE, 1), [])
    
    plt.show()


def run_stage(with_obstacles):
    """
    Executes a phase, finds the path, and runs the animation.
    """
    if with_obstacles:
        print("--- Stage 2: Environment with Obstacles ---")
        obstacles = DEFINED_OBSTACLES
    else:
        print("--- Stage 1: Free Environment ---")
        obstacles = set()

    while True:
        start_node = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        goal_node = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        if start_node != goal_node and start_node not in obstacles and goal_node not in obstacles:
            break
            
    print(f"Objective: Go from {start_node} to {goal_node}")

    found_path = find_path_bfs(start_node, goal_node, obstacles)

    if found_path:
        success = "Yes"
        path_length = len(found_path) - 1
        print(f"Path found!")
        print("\nEvaluation Metrics:")
        print(f"  - Task Success: {success}")
        print(f"  - Path Length: {path_length} steps")
        print("\nStarting animation...")
        animate_path(found_path, start_node, goal_node, obstacles)
        print("Animation finished.")
    else:
        success = "No"
        path_length = "N/A"
        print(f"Could not find a path.")
        print("\nEvaluation Metrics:")
        print(f"  - Task Success: {success}")
        print(f"  - Path Length: {path_length} steps")


if __name__ == "__main__":
    run_stage(with_obstacles=False)
    print("\n" + "="*40 + "\n")
    run_stage(with_obstacles=True)