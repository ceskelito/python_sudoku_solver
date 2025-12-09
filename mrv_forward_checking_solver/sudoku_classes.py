from dataclasses import dataclass, field

@dataclass
class SudokuCell:
    """Rappresenta una singola cella del Sudoku."""
    row: int
    col: int
    value: int = 0
    static: bool = field(init=False)
    candidates: set[int] = field(default_factory=set, init=False)

    def __post_init__(self):
        self.static = self.value != 0

    def init_candidates(self, dimension: int) -> None:
        self.candidates = set() if self.value != 0 else set(range(1, dimension + 1))

    def assign(self, value: int) -> None:
        """Assegna un valore alla cella e svuota i candidati."""
        self.value = value
        self.candidates = set()

    def remove_candidate(self, value: int) -> bool:
        """Eventually remove a candidate. Return True if is removed"""
        if value in self.candidates:
            self.candidates.discard(value)
            return True
        return False


@dataclass
class SudokuRegion:
    """Represent a Sudokus's row, column or block."""
    region_id: int
    cells: list[SudokuCell] = field(default_factory=list)

    def values(self) -> list[int]:
        """Returs the values already assigned in the region."""
        return [cell.value for cell in self.cells if cell.value != 0]

    def is_valid(self) -> bool:
        """Check for duplicates in region. Return True if region has dups else False"""
        assigned = self.values()
        return len(assigned) == len(set(assigned))

    def propagate_constraint(self, value: int) -> None:
        for cell in self.cells:
            cell.remove_candidate(value)


GridInt = list[list[int]]
GridObj = list[list[SudokuCell]]


class Sudoku:

    def __init__(self, int_grid: GridInt):
        self.dimension: int = len(int_grid)
        self.block_dim: int = int(self.dimension ** 0.5)
        self.grid: GridObj = self._create_grid(int_grid)
        self.rows: list[SudokuRegion] = []
        self.cols: list[SudokuRegion] = []
        self.blocks: list[SudokuRegion] = []
        self._init_regions()

    def _create_grid(self, int_grid: GridInt) -> GridObj:
        """Create a grid of objects SudokuCell."""
        grid: GridObj = []
        for i in range(self.dimension):
            row = [
                SudokuCell(row=i, col=j, value=int_grid[i][j])
                for j in range(self.dimension)
            ]
            for cell in row:
                cell.init_candidates(self.dimension)
            grid.append(row)
        return grid

    def _init_regions(self) -> None:

        # Rows
        for id in range(self.dimension):
            row = self.grid[id]
            self.rows.append(SudokuRegion(id, row))

        # Columns
        for id in range(self.dimension):
            column = [self.grid[r][id] for r in range(self.dimension)]
            self.cols.append(SudokuRegion(id, column))

        # Blocks
        for id in range(self.dimension):
            start_row = (id // self. block_dim) * self.block_dim
            start_col = (id % self.block_dim) * self.block_dim
            
            block_cells = [
                self.grid[r][c]
                for r in range(start_row, start_row + self.block_dim)
                for c in range(start_col, start_col + self.block_dim)
            ]
            self.blocks.append(SudokuRegion(id, block_cells))

    # def get_cell(self, row: int, col:  int) -> SudokuCell:
    #     """Ritorna la cella alle coordinate specificate."""
    #     return self.grid[row][col]

    def get_status(self) -> bool:
        """Return the status of the sudoku:
            1: Solved
            0: Uncomplete
            -1: Completed with conflicts"""
        all_regions = self.rows + self.cols + self.blocks
        return all(region.is_valid() for region in all_regions)