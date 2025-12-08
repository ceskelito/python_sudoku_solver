from typing import TypeAlias


class SudokuCell:

    def __init__(self, value: int, nvalue: int):  # row: int, col: int,

        # self.row: int = row
        # self.col: int = col
        self.value: int = value
        self.static: bool = False

        self.candidates: set[int] = set()

        if (self.value != 0):
            self.static = True
        else:
            self.candidates = {cndt for cndt in range(1, nvalue + 1)}


GridInt: TypeAlias = list[list[int]]
GridObj: TypeAlias = list[list[SudokuCell]]


class Sudoku:

    def __init__(self, grid: GridInt):
        self.dimension: int = len(grid)
        self.grid: GridObj = self.create_grid(grid, self.dimension)

    def create_grid(self, grid: GridInt, dim: int) -> GridObj:

        new_grid: GridObj = []

        for i in range(dim):

            row: list[SudokuCell] = []

            for j in range(dim):

                value = grid[i][j]
                cell = SudokuCell(
                    # i,
                    # j,
                    value,
                    dim)
                row.append(cell)

            new_grid.append(row)

        return new_grid
