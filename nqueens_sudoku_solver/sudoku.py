import sys

g_solution = 0

def check_row(board_mask: list[list[int]], row: int, column: int) -> bool:

    for col in range(column):
        if board_mask[col] == row:
            return False
    return True

def check_subgrid(board_mask: list[list[int]], row: int, column: int, nsqaure: int) -> bool:
    dim = 3 # int(nsqaure ** 0.5)
    
    start_row = (row // dim) * dim
    start_col = (column // dim) * dim

    for c in range(start_col, column):
        
        if board_mask[c] == False:
            continue
        if (start_row <= board_mask[c] < start_row + dim):
            return False
                
    return True

def square_is_empty(board: list[list[int]], row: int, column: int, depth: int) -> bool:

    for value in range(depth):
        if (board[value][column] == row):
            return False
    return True

def print_board(board, nsqaure):
    for col in range(nsqaure):
        for row in range(nsqaure):
            if (board[row] == col):
                print('*', end=' ')
            else:
                print('#', end=' ')
        print('')

def print_real_board(board: list[list[int]], nsqaure: int) -> None: # Gemini 3
    # Converto la tua struttura dati (Valore -> Colonna -> Riga)
    # nella classica visualizzazione (Riga -> Colonna -> Valore)
    grid = [[0] * nsqaure for _ in range(nsqaure)]
    
    for val in range(nsqaure):
        for col in range(nsqaure):
            row = board[val][col]
            if row != -1:
                grid[row][col] = val + 1

    print("-" * 25)
    for r in range(nsqaure):
        if r % 3 == 0 and r != 0:
            print("-" * 25)
        for c in range(nsqaure):
            if c % 3 == 0 :#and c != 0:
                print("| ", end="")
            print(f"{grid[r][c]} ", end="")
        print("|", end="")
        print()
    print("-" * 25)

def sudoku_solver(board: list[list[int]], nsqaure: int, column: int, depth: int) -> None:
    
    global g_solution
    if g_solution > 0:
        return

    if (depth == nsqaure):
        print_real_board(board, nsqaure)
        g_solution = 1
        return

    if (column == nsqaure):
        sudoku_solver(board, nsqaure, 0, depth + 1)
        return

    board_mask = board[depth]

    for row in range(nsqaure):
        if (square_is_empty(board, row, column, depth) and 
            check_row(board_mask, row, column) and
            check_subgrid(board_mask, row, column, nsqaure)):

            board_mask[column] = row

            sudoku_solver(board, nsqaure, column + 1, depth)

            if g_solution > 0: return

            board_mask[column] = -1
            

