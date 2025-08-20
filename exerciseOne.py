# receber a entrada do usuário de X tamanho da matriz
# receber a posição de inicio do robo
# deslocar para direita primeiro até bater na parede, printar no console a coordenada percorrida, se bater na parede informar e ir pra proxima instrução
# dps pra baixo até bater na parede, printar no console a coordenada percorrida, se bater na parede informar e ir pra proxima instrução
# dps pra esquerda até bater na parede, printar no console a coordenada percorrida, se bater na parede informar e ir pra proxima instrução
# dps pra cimaaté bater na parede, printar no console a coordenada percorrida, se bater na parede informar e ir pra proxima instrução
# quanto achar as 4 paredes informar que achou e quais foram as coordenadas antes de bater

from robotUtils import print_matrix

matrixSize = int(input("Type matrix size: "))

def get_valid_robot_position(matrix_size):
    while True:
        row = int(input("Type robot start position (row): "))
        col = int(input("Type robot start position (column): "))
        if 0 <= row < matrix_size and 0 <= col < matrix_size:
            return (row, col)
        else:
            print(f"Invalid position! Please enter values between 0 and {matrix_size - 1}.")

robotStartPos = get_valid_robot_position(matrixSize)

def move_robot(matrix_size, start_pos):
    directions = [
        (0, 1, "right"),
        (1, 0, "down"),
        (0, -1, "left"),
        (-1, 0, "up")
    ]
    pos = list(start_pos)
    wall_hits = []
    landed_positions = set()
    landed_positions.add(tuple(pos))
    for dr, dc, name in directions:
        print(f"Moving {name}:")
        while True:
            next_row = pos[0] + dr
            next_col = pos[1] + dc
            if 0 <= next_row < matrix_size and 0 <= next_col < matrix_size:
                pos[0], pos[1] = next_row, next_col
                landed_positions.add(tuple(pos))
                print(f"Robot at position: ({pos[0]}, {pos[1]})")
            else:
                print(f"Hit the wall while moving {name} at ({pos[0]}, {pos[1]})! Going to next direction.")
                wall_hits.append((name, (pos[0], pos[1])))
                break
    print_matrix(matrix_size, tuple(pos), landed_positions)
    print("\nRobot found all 4 walls.")
    for direction, coord in wall_hits:
        print(f"Before hitting the {direction} wall, robot was at: {coord}")

move_robot(matrixSize, robotStartPos)


