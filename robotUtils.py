def print_matrix(matrix_size, robot_pos, landed_positions):
    ROBOT = "🤖"
    NOT_LANDED = "🟩"
    LANDED = "🔴"
    for row in range(matrix_size):
        line = ""
        for col in range(matrix_size):
            if (row, col) == robot_pos:
                line += ROBOT + " "
            elif (row, col) in landed_positions:
                line += LANDED + " "
            else:
                line += NOT_LANDED + " "
        print(line.rstrip())
