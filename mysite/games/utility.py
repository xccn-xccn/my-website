from .non_web.sudoku_solver import sudoku_solver


def solve_sudoku(SudokuForm):
    grid = [[] for _ in range(9)]
    for count, square in enumerate([x.cleaned_data.get("square", 0) for x in SudokuForm]):
        grid[count // 9].append(int(square))
    solved_sudoku = sudoku_solver(grid)
    solved_as_str = "".join([str(x) for row in solved_sudoku for x in row])
    return solved_as_str
