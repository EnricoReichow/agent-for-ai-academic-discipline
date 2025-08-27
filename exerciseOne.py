import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
import time

# Parâmetros do grid
N = 10  # tamanho do grid (NxN)

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class Grid:
    def __init__(self, size):
        self.size = size

    def has_wall(self, x, y, direction: Direction) -> bool:
        if direction == Direction.NORTH:
            return y == 0
        elif direction == Direction.SOUTH:
            return y == self.size - 1
        elif direction == Direction.WEST:
            return x == 0
        elif direction == Direction.EAST:
            return x == self.size - 1

class Agent:
    def __init__(self, start_x, start_y, direction=Direction.NORTH):
        self.x = start_x
        self.y = start_y
        self.direction = direction

        # Flags para saber se já tocou nas paredes
        self.hit_north = False
        self.hit_south = False
        self.hit_west = False
        self.hit_east = False

        self.visitadas = set()  # posições visitadas (para visualização)

    def has_discovered_all_walls(self) -> bool:
        return self.hit_north and self.hit_south and self.hit_west and self.hit_east

    def move(self, grid: Grid):
        # Marcar a posição atual como visitada
        self.visitadas.add((self.x, self.y))

        if grid.has_wall(self.x, self.y, self.direction):
            self._mark_wall_touched()
            self._turn_right()
        else:
            if self.direction == Direction.NORTH:
                self.y -= 1
            elif self.direction == Direction.SOUTH:
                self.y += 1
            elif self.direction == Direction.WEST:
                self.x -= 1
            elif self.direction == Direction.EAST:
                self.x += 1

    def _mark_wall_touched(self):
        if self.direction == Direction.NORTH:
            self.hit_north = True
        elif self.direction == Direction.SOUTH:
            self.hit_south = True
        elif self.direction == Direction.WEST:
            self.hit_west = True
        elif self.direction == Direction.EAST:
            self.hit_east = True

    def _turn_right(self):
        self.direction = Direction((self.direction.value + 1) % 4)

def plotar_grid(posicao, visitadas):
    grid = np.zeros((N, N))
    for (x, y) in visitadas:
        grid[y, x] = 1  # células visitadas
    grid[posicao[1], posicao[0]] = 2  # posição do robô
    plt.imshow(grid, cmap="Blues", origin="upper")
    plt.grid(True)
    plt.xticks(np.arange(-.5, N, 1), [])
    plt.yticks(np.arange(-.5, N, 1), [])
    plt.pause(0.1)
    plt.clf()

def run_simulation():
    grid = Grid(N)
    agent = Agent(start_x=0, start_y=0)
    steps = 0

    plt.figure(figsize=(5,5))

    while not agent.has_discovered_all_walls():
        agent.move(grid)
        steps += 1
        plotar_grid((agent.x, agent.y), agent.visitadas)

    plt.close()
    print(f"✅ Robô descobriu todos os limites em {steps} movimentos!")

if __name__ == "__main__":
    run_simulation()
