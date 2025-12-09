import numpy as np
from sudoku_classes import Sudoku, SudokuCell, SudokuRegion

def	get_mrv_cell(grid: list[list[SudokuCell]]) -> SudokuCell:
	mrv: SudokuCell	= grid[0][0]

	for row in grid:
		for cell in row:
			# print(f"Cell: {cell.row.id}:{cell.col.id}")
			# print(f"Candidates: {cell.candidates}")
			# print()
			if cell.value == 0 and len(cell.candidates) < len(mrv.candidates):
				mrv = cell
	return mrv
            
		
def solve_sudoku(sudoku: Sudoku) -> int:
	mrv: SudokuCell
 
	status = sudoku.get_status()
	if status != 0:
		return status
	
	mrv = get_mrv_cell(sudoku.grid)
	# print(f"{mrv.row.id} : {mrv.col.id}")
	# print(f"range: {mrv.candidates}")
	# print(f"len: {len(mrv.candidates)}")
	
	# return -1

	for i in range(len(mrv.candidates)):
		value = mrv.candidates.pop()
		if not value in mrv.row.values(): #all(mrv.row.values(), mrv.col.values, mrv.block.values()):
			mrv.assign(value)
			solve_sudoku(sudoku)
		else:
			mrv.candidates.add(value)