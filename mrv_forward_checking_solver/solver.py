from sudoku_classes import Sudoku, SudokuCell, SudokuRegion

def	get_mrv_cell(grid: list[list[SudokuCell]]) -> SudokuCell | None:
	mrv: SudokuCell | None = None

	for row in grid:
		for cell in row:
			if cell.value == 0:
				if mrv is None or len(cell.candidates) < len(mrv.candidates):
					mrv = cell
	return mrv
			
		
def solve_sudoku(sudoku: Sudoku) -> int:
 
	status = sudoku.get_status()

	if status != 0:
		return status
	
	mrv: SudokuCell = get_mrv_cell(sudoku.grid)

	if mrv is None or len(mrv.candidates) == 0:
		return -1

	candidates_to_try = list(mrv.candidates).copy()

	for value_to_try in candidates_to_try:
		
	# Test the value
		mrv.assign(value_to_try)
		result = solve_sudoku(sudoku)

	# Sudoku Completed
		if result == 1:
			return 1
		
	# Invalid recursion path
		if result == -1:
			mrv.assign(value_to_try * -1)
			continue  # Test the next value

	return -1
