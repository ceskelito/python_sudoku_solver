from dataclasses import dataclass, field

@dataclass
class SudokuCell:
	"""Rappresenta una singola cella del Sudoku."""
	value: int = 0
	grid_dimension: int = 0
	candidates: set[int] = field(default_factory=set, init=False)
	row: 'SudokuRegion' = field(init=False)
	col: 'SudokuRegion' = field(init=False)
	block: 'SudokuRegion' = field(init=False)

	def __post_init__(self):
		self._init_candidates()

	def _init_candidates(self) -> None:
		self.candidates = set() if self.value != 0 else set(range(1, self.grid_dimension + 1))

	def _reinit_candidates(self) -> None:
		self._init_candidates()
		used_values = set(self.row.values()) | \
                      set(self.col.values()) | \
                      set(self.block.values())
		self.candidates = self.candidates - used_values

	def assign(self, value: int) -> None:
		"""Assegna un valore alla cella e svuota i candidati."""
		if (value <= 0):
			self.value = 0
			self._reinit_candidates()

			self.row.recalculate_constraints()
			self.col.recalculate_constraints()
			self.block.recalculate_constraints()
		else:
			self.value = value
			self.candidates = set()
			self.row.propagate_constraint(self.value)
			self.col.propagate_constraint(self.value)
			self.block.propagate_constraint(self.value)
	
@dataclass
class SudokuRegion:
	"""Represent a Sudokus's row, column or block."""
	id: int
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
			cell.candidates.discard(value)

	def recalculate_constraints(self) -> None:
		for cell in self.cells:
			if cell.value == 0:
				cell._reinit_candidates()

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
				SudokuCell(value=int_grid[i][j], grid_dimension=self.dimension)
				for j in range(self.dimension)
			]
			# for cell in row:
			# 	cell.init_candidates(self.dimension)
			grid.append(row)
		return grid

	def _init_regions(self) -> None:
		"""
		Inizializza gli oggetti SudokuRegion per righe, colonne e blocchi
		e assegna questi oggetti come attributi (row_region, col_region, block_region) a ogni cella.
		"""
		
		# Rows
		for id in range(self.dimension):
			row = self.grid[id]
			region = SudokuRegion(id, row)
			self.rows.append(region)
			
			for cell in row:
				cell.row = region
		

		# Columns
		for id in range(self.dimension):
			column = [self.grid[r][id] for r in range(self.dimension)]
			region = SudokuRegion(id, column)
			self.cols.append(region)
			
			for cell in column:
				cell.col = region
		

		# Blocks
		for id in range(self.dimension):
			start_row = (id // self.block_dim) * self.block_dim
			start_col = (id % self.block_dim) * self.block_dim
			
			block_cells = [
				self.grid[r][c]
				for r in range(start_row, start_row + self.block_dim)
				for c in range(start_col, start_col + self.block_dim)
			]
			region = SudokuRegion(id, block_cells)
			self.blocks.append(region)
			
			for cell in block_cells:
				cell.block = region
			
		# Propagate constraints for all the assigned cells
		for r in self.grid:
			for c in r:
				c.row.propagate_constraint(c.value)
				c.col.propagate_constraint(c.value)
				c.block.propagate_constraint(c.value)

	def print_grid(self):
		
		for i, row in enumerate(self.grid):
			if i % self.block_dim == 0 and i != 0:
				print("------+-------+------")
			row_output = ""
			for j, cell in enumerate(row):
				if j % self.block_dim == 0 and j != 0:
					row_output += "| "
				display_value = str(cell.value) if cell.value != 0 else "."
				row_output += display_value + " "
			print(row_output)

	def get_status(self) -> bool:
		"""
  		Return the status of the sudoku:
		1: Solved
		0: Uncomplete
		-1: Completed with conflicts
		"""
		for row in self.grid:
			for cell in row:
				if cell.value == 0:
					return 0
		all_regions = self.rows + self.cols + self.blocks
		is_valid = all(region.is_valid() for region in all_regions)
		if is_valid:
			return 1
		return -1