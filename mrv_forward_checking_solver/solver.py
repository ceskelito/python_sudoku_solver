import numpy as np

def CheckRow(grid, row, value):

def CheckBox(grid, row, col, value):

def GetPossibleValues(grid, row, col, nvalues):

    count = 0

    for value in range(1, nvalues + 1):
            if CheckRow(grid, row, value) and \
                CheckBox(grid, row, col, value):
                PossibleValues[count] = value
                count += 1

def solve_grid(grid, row, col, nvalues):

    if (row == col == nvalues):
        print(np.matrix(grid))
        return
    
    for r in range(nvalues)
        for c in range(nvalues)
            if grid[r][c] == 0
                PossibleValues[r][c] = GetPossibleValues(grid, row, col)
                if len(PossibleValues) < MinRemainingValues
                    MinRemainingValues = len(PossibleValues)
        
                

