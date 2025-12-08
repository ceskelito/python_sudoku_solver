import sys
import numpy as np
from .get_grid_from_file import get_grid
# import readline

nvalues = 9


def main():

    if len(sys.argv) < 2:
        print("Please give an input file")
        return 1
    if len(sys.argv) > 2:
        print("The program accept only 1 argument")
        return 1

    grid = get_grid(sys.argv[1], nvalues)

    print(np.matrix(grid))


if __name__ == "__main__":
    main()
