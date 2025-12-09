from typing import TypeAlias, Set, List
from dataclasses import dataclass, field

@dataclass
class SudokuCell:
    row: int
    col: int
    value: int = 0
    static: bool = field(init=False)
    candidates: Set[int] = field(default_factory=set, init=False)

    def __post_init__(self):
        if self.value != 0:
            self.static = True
        else:
            self.static = False

    def get_candidates(self, grid_dim: int) -> Set[int]:
        if self.value == 0:
            return {cndt for cndt in range(1, grid_dim + 1)}
        return set()


@dataclass
class SudokuRegion:

    region_id: int
    cells: List[SudokuCell] = field(default_factory=list)

    def values(self) -> list[int]:
        assigned_values: list[int] = [cell.value for cell in self.cells if cell.value != 0]

        return assigned_values

    def is_valid(self) -> bool:
        assigned_values = self.values()

        return len(assigned_values) == len(set(assigned_values))

GridInt: TypeAlias = list[list[int]]
GridObj: TypeAlias = list[list[SudokuCell]]

class Sudoku:

    def __init__(self, int_grid: GridInt):
        self.dimension: int = len(int_grid)
        # self.block_dim: int = int(self.dimension ** 0.5)
        self.grid: GridObj = []
        self.init_grid(int_grid)
        self.rows: list[SudokuRegion] = []
        self.cols: list[SudokuRegion] = []
        self.blocks: list[SudokuRegion] = []
        self.init_regions()
    
    def init_grid(self, int_grid: GridInt):
        for i in range(self.dimension):
            new_row: list[SudokuCell] = []
            for j in range(self.dimension):
                new_cell = SudokuCell(
                    row = i,
                    col = j,
                    value = int_grid[i][j]
                )
                new_row.append(new_cell)
            self.grid.append(new_row)

        self.init_candidates()
    
    def init_candidates(self):
        for row in self.grid:
            for cell in row:
                if (cell.value == 0):
                    cell.candidates = {i for i in range(1, self.dimension + 1)}
                else:
                    cell.candidates = set()
    
    def init_regions(self):

        # rows
        for id in range(self.dimension):
            row = self.grid[id]
            self.rows[id] = SudokuRegion(id, row)
        
        # colons
        for id in range(self.dimension):
            col: list[SudokuCell] = []
            for r in range(self.dimension):
                col.append(self.grid[r][id])
            self.cols[id] = SudokuRegion(id, col)

        # blocks
        block_dim = int(self.dimension**0.5)

        for id in range(self.dimension):

            start_row = (id // block_dim) * block_dim
            start_col = (id % block_dim) * block_dim
            
            block: list[SudokuCell] = []
            for r in range(start_row, start_row + block_dim):
                for c in range(start_col, start_col + block_dim):
                    block.append(self.grid[r][c])

            self.blocks[id] = SudokuRegion(id, block) 


        



# class Sudoku:

#     dimension: int
#     grid: GridObj
#     subGrid: GridObj

#     def __init__(self, grid: GridInt):
#         self.dimension: int = len(grid)
#         self.grid: GridObj = self.create_grid(grid, self.dimension)

#     def create_grid(self, grid: GridInt, dim: int):
        
#         for i in range(dim):

#             new_row: list[SudokuCell]

#             for j in range(dim):

#                 value = grid[i][j]
#                 row = i
#                 col = j

#                 new_cell = SudokuCell(
#                     value,
#                     dim,
#                     row,
#                     col
#                 )
#                 new_row.append(new_cell)

#             self.grid.append(new_row)

#     def init_subGrid(self):

#          for row in self.grid:
#             for cell in row:
#                 n_subgrid = (3 * cell.row / 3) + (cell.row / 3)
#                 self.subGrid[n_subgrid].add(cell)