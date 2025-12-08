import sys
from math import sqrt

g_solution = 0

def check_row(board_mask, row, column):

    for col in range(column):
        if board_mask[col] == row:
            return -1
    return 0

def check_subgrid(board_mask, row, column, nsqaure):
    dim = 3 # math.sqrt(nsqaure)
    
    start_row = (row // dim) * dim
    start_col = (column // dim) * dim

    for c in range(start_col, column):
        
        if board_mask[c] == -1:
            continue
        if (start_row <= board_mask[c] < start_row + dim):
            return -1
                
    return 0

def square_is_empty(board, row, column, depth):

    for value in range(depth):
        if (board[value][column] == row):
            return -1
    return 0

def print_board(board, nsqaure):
    for col in range(nsqaure):
        for row in range(nsqaure):
            if (board[row] == col):
                print('*', end=' ')
            else:
                print('#', end=' ')
        print('')

def print_real_board(board, nsqaure): # Gemini 3
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

def sudoku_solver(board, nsqaure, column, depth):
    
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
        if (square_is_empty(board, row, column, depth) == 0 and 
            check_row(board_mask, row, column) == 0 and
            check_subgrid(board_mask, row, column, nsqaure) == 0):

            board_mask[column] = row

            sudoku_solver(board, nsqaure, column + 1, depth)

            if g_solution > 0: return

            board_mask[column] = -1
            

