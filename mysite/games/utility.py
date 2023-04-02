from django.contrib import messages
from .non_web.sudoku_solver import sudoku_solver


def solve_sudoku(SudokuFormSet):
    sudoku = format_as_sudoku(SudokuFormSet, only_values=True)
    solved_sudoku = sudoku_solver(sudoku)
    solved_as_str = "".join([str(x) for row in solved_sudoku for x in row])
    return solved_as_str


def get_invalids(value, rows, columns, sections, y, x, current):
    """Returns a list of all invalid id's given the value that is invalid"""
    output = [current]
    for invalid in (group.get(value, None) for group in (rows[y], columns[x], sections[x//3 + (y//3)*3])):
        if invalid:
            output.append(invalid)
    return output


def apply_class(ids, aclass, FormSet):
    """Applys a class to a formset when given the ids"""
    for form in FormSet:
        print(form.fields["square"].widget.attrs)
        print(form['square'].id_for_label)
        id = form["square"].id_for_label

        if id in ids:
            form.fields["square"].widget.attrs["class"] = form.fields["square"].widget.attrs.get("class", "") + aclass

    return FormSet

def valid_sudoku(SudokuFormSet):

    valid = True
    sudoku = format_as_sudoku(SudokuFormSet)
    sections, rows, columns = [{k: {} for k in range(9)} for _ in range(3)]
    invalid_ids = set()

    for y, line in enumerate(sudoku):
        for x, square in enumerate(line):
            print(square, type(square))

            num = square.cleaned_data.get("square", 0)
            if num == 0:
                continue
            elif num > 9 or num < 0 or num in rows[y] or num in columns[x] or num in sections[x//3 + (y//3)*3]:
                valid = False
                invalids = get_invalids(num, rows, columns, sections, y, x, square["square"].id_for_label)
                for invalid in invalids:
                    invalid_ids.add(invalid)
            else:
                print(square, type(square))
                id = square["square"].id_for_label
                rows[y][num] = id
                columns[x][num] = id
                sections[x//3 + (y//3)*3][num]= id
    SudokuFormSet = apply_class(invalid_ids, " invalid", SudokuFormSet)
    
    return SudokuFormSet, valid
    
def format_as_sudoku(FormSet, only_values=False):
    sudoku = [[] for _ in range(9)]
    for index, square in enumerate(FormSet):
        if only_values:
            square = int(square.cleaned_data.get("square", 0))
        sudoku[index // 9].append(square)
    return sudoku 