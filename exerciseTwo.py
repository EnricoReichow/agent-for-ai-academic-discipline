import random
import matplotlib.pyplot as plt
import numpy as np
import time
from collections import deque

N = 10
direcoes = [(0, 1), (1, 0), (0, -1), (-1, 0)]  

obstaculos = {
    (0, 5),
    (1, 7), (1, 4),
    (2, 3),
    (3, 3),
    (4, 3), (4, 6),
    (5, 8),
    (6, 4),
    (7, 3), (7, 5), (7, 6),
    (8, 6),
    (9, 5)
}

def plotar_grid(posicao, visitadas):
    """Exibe o grid com obstáculos, células visitadas e posição do robô"""
    grid = np.zeros((N, N))

    for (x, y) in obstaculos:
        grid[x, y] = -1 

    for (x, y) in visitadas:
        grid[x, y] = 1  

    grid[posicao] = 2 

    plt.imshow(grid, cmap="Blues")
    plt.grid(True)
    plt.xticks(np.arange(-.5, N, 1), [])
    plt.yticks(np.arange(-.5, N, 1), [])
    plt.pause(0.1)
    plt.clf()

def bfs(celula_inicial, visitadas):
    """Encontra a célula não visitada mais próxima usando BFS"""
    fila = deque([celula_inicial])
    predecessores = {celula_inicial: None}

    while fila:
        x, y = fila.popleft()

        if (x, y) not in visitadas:
            caminho = []
            atual = (x, y)
            while atual is not None:
                caminho.append(atual)
                atual = predecessores[atual]
            caminho.reverse()
            return caminho

        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            if (0 <= nx < N and 0 <= ny < N and
                (nx, ny) not in obstaculos and
                (nx, ny) not in predecessores):
                predecessores[(nx, ny)] = (x, y)
                fila.append((nx, ny))

    return None  

def mover_robo():
    while True:
        robo = (random.randint(0, N - 1), random.randint(0, N - 1))
        if robo not in obstaculos:
            break

    visitadas = set([robo])
    passos_totais = 0

    plt.figure(figsize=(6, 6))

    while True:
        plotar_grid(robo, visitadas)

        caminho = bfs(robo, visitadas)

        if caminho is None:
            break

        for proxima in caminho[1:]:
            robo = proxima
            visitadas.add(robo)
            passos_totais += 1
            plotar_grid(robo, visitadas)

    celulas_acessiveis = N * N - len(obstaculos)
    completude = len(visitadas) / celulas_acessiveis * 100

    plt.close()
    print("✅ Exploração concluída!")
    print(f"Total de células acessíveis: {celulas_acessiveis}")
    print(f"Células visitadas: {len(visitadas)}")
    print(f"Completude: {completude:.2f}%")
    print(f"Passos totais: {passos_totais}")
    print(f"Passos redundantes: {passos_totais - len(visitadas)}")
    print("Sucesso no desvio:", "Sim" if completude == 100 else "Não")

if __name__ == "__main__":
    mover_robo()
