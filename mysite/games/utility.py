from django.contrib import messages
from .non_web.sudoku_solver import sudoku_solver


def solve_sudoku(SudokuForm):
    grid = [[] for _ in range(9)]
    for count, square in enumerate([x.cleaned_data.get("square", 0) for x in SudokuForm]):
        grid[count // 9].append(int(square))
    solved_sudoku = sudoku_solver(grid)
    solved_as_str = "".join([str(x) for row in solved_sudoku for x in row])
    return solved_as_str


def valid_sudoku(FormSet):
    puzzle = [[] for _ in range(9)]
    invalid = False
    for count, square in enumerate(FormSet):
        puzzle[count // 9].append(square)
    sections, rows, columns = [{k: set() for k in range(9)} for _ in range(3)]
    for y, line in enumerate(puzzle):
        for x, square in enumerate(line):
            num = square.cleaned_data.get("square", 0)
            if num == 0:
                continue
            elif num > 9 or num < 0 or num in rows[y] or num in columns[x] or num in sections[x//3 + (y//3)*3]:
                invalid = True
                for field in square:
                    field.widget.attrs['square'] = field.widget.attrs.get('square', '') + ' is-invalid'
            else:
                rows[y].add(num)
                columns[x].add(num)
                sections[x//3 + (y//3)*3].add(num)
    return invalid
