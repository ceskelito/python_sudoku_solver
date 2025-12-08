from sudoku import sudoku_solver 

def main():

    # if (len(sys.argv) != 2):
    #     return 1

    # nqueens = int(sys.argv[1])
    nsqaure = 9
    board = [[-1] * nsqaure for _ in range(nsqaure)]
    column = 0
    depth = 0

    sudoku_solver(board, nsqaure, column, depth)
    # print_board(board[0], nsqaure);

if __name__ == "__main__":
    main()
