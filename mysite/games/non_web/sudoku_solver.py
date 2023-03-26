from time import perf_counter


def valid(y, x, puzzle, section, row, column):
    value = puzzle[y][x]
    return value not in row and value not in column and value not in section




def begin(puzzle):
    mutable = []
    sections, rows, columns = [{k: set() for k in range(9)} for _ in range(3)]
    if len(puzzle) != 9:
        raise Exception("Sudoku has wrong dimensions")
    for y, line in enumerate(puzzle):
        for x, num in enumerate(line):
            if len(puzzle) != 9:
                raise Exception("Sudoku has wrong dimensions")
            if num == 0:
                mutable.append((y, x))
            elif num > 9 or num < 0 or num in rows[y] or num in columns[x] or num in sections[x//3 + (y//3)*3]:
                raise Invalid_Sudoku
            else:
                rows[y].add(num)
                columns[x].add(num)
                sections[x//3 + (y//3)*3].add(num)
    return (mutable, sections, rows, columns)


def solve_single(puzzle, seen=None):
    if seen == None:
        seen = set()
    
    try:
        mutable, sections, rows, columns = begin(puzzle)
    except Invalid_Sudoku:
        return "Invalid Sudoku"
    
    if not mutable:
        return puzzle #sudoku is already solved
    index = 0
    seen = set()
    while True:
        y, x = mutable[index]
        sections_index = x//3 + (y//3)*3
        success = False
        square = puzzle[y][x]
        if square != 0:
            sections[sections_index].remove(square)
            rows[y].remove(square)
            columns[x].remove(square)

        while success == False and puzzle[y][x] < 9:
            puzzle[y][x] += 1
            success = valid(
                y, x, puzzle, sections[sections_index], rows[y], columns[x])
        if success:
            square = puzzle[y][x]
            sections[sections_index].add(square)
            rows[y].add(square)
            columns[x].add(square)
            index += 1
            if index == len(mutable):
                return puzzle
        else:
            index -= 1
            if index < 0:
                break
            puzzle[y][x] = 0
    raise Exception


def sudoku_solver(puzzle):
    solved = solve_single(puzzle)
    return solved

class Invalid_Sudoku(Exception):
    pass

if __name__ == "__main__":
    # TODO make it raise error when there are multiple solutions (or any invalids)
    start = perf_counter()
    print(solve_single([[0, 0, 0, 0, 0, 2, 7, 5, 0],
                        [0, 1, 8, 0, 9, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [4, 9, 0, 0, 0, 0, 0, 0, 0],
                        [0, 3, 0, 0, 0, 0, 0, 0, 8],
                        [0, 0, 0, 7, 0, 0, 2, 0, 0],
                        [0, 0, 0, 0, 3, 0, 0, 0, 9],
                        [7, 0, 0, 0, 0, 0, 0, 0, 0],
                        [5, 0, 0, 0, 0, 0, 0, 8, 0]]))
    print(f"{(perf_counter() - start) * 1000}")
