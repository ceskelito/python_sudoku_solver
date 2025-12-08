import sys

def check_square(board, row, column):
    for col in range(column):
        if board[col] == row or \
        board[col] - row == column - col or \
        board[col] - row == col - column:
            return -1
    return 0

def print_board(board, nqueens):
    for row in range(nqueens):
        for col in range(nqueens):
            if (board[row] == col):
                print('*', end=' ')
            else:
                print('#', end=' ')
        print('')

def place_queens(board, nqueens, column):
    
    if (column == nqueens):
        print_board(board, nqueens)
        print("\n")
        return

    for row in range(nqueens):
        if (check_square(board, row, column) == 0):
            board[column] = row
            place_queens(board, nqueens, column + 1)

def main():

    if (len(sys.argv) != 2):
        return 1

    nqueens = int(sys.argv[1])
    board = [0] * nqueens
    column = 0

    # print(board)

    place_queens(board, nqueens, column)

if __name__ == "__main__":
    main()
