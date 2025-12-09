
def get_grid(f_path, nvalues) -> list[list[int]]:

    grid: list[list[int]] = [[0] * nvalues for _ in range(nvalues)]

    try:
        with open(f_path, "r") as file:
            
            # --- GESTIONE ERRORI INTERNI ---
            for row in range(nvalues):
                line = file.readline().strip()

                if not line:
                    raise ValueError(f"File has only {row} rows. Expected {nvalues}.")

                try:

                    row_of_ints = [int(char) for char in line]

                    RowLen = len(row_of_ints)
                    if RowLen != nvalues:
                        raise ValueError(f"Size of row {row + 1} was: {RowLen}. Expected: {nvalues}")

                    for c in row_of_ints:
                        if c < 0 or c > nvalues:
                            raise ValueError(f"Value {c} was found at row: {row + 1}. Value must be between 0 and {nvalues}.")
                    grid[row] = row_of_ints

                except ValueError as e:
                    if "invalid literal for int()" in str(e):
                        print(f"Error: The grid in file '{f_path}' contains non numerical value: {e}")
                    else:
                        print(f"Error: The grid in file '{f_path}' contains invalid value: {e}")
                    exit(1)

            ExtraLine = file.readline().strip()
            if ExtraLine:
                 raise ValueError(f"File contains more than {nvalues} rows.")

    except FileNotFoundError:
        print(f"file {f_path} does not exists")
        exit(1)

    except Exception as e:
        print(f"An unexpected error has verified during file processing: {e}")
        exit(1)

    return grid
