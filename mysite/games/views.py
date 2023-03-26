from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms import formset_factory
from .forms import SolveSudokuForm, QuickEnterForm, SudokuFormsetValid
from .utility import solve_sudoku, valid_sudoku


def home(request):
    context = {

    }
    return render(request, "games/home.html", context)


def sudoku(request):  # TODO fix current error, make input red but new same, make copy quick enter, make generator, heighlight errors
    SudokuFormSet = formset_factory(SolveSudokuForm, extra=81)
    SudokuForm = SudokuFormSet()
    QuickEnter = QuickEnterForm()
    context = {

    }
    context["solved"] = "NO"
    if request.method == "POST":
        if "sudoku_submit" in request.POST:
            print("sudoku_submited")
            SudokuForm = SudokuFormSet(request.POST)
            print("form with validation created")
            if SudokuForm.is_valid():
                # valid_sudoku(SudokuForm)

                puzzle = [[] for _ in range(9)]
                invalid = False
                for count, square in enumerate(SudokuForm):
                    puzzle[count // 9].append(square)
                sections, rows, columns = [{k: set() for k in range(9)} for _ in range(3)]
                for y, line in enumerate(puzzle):
                    for x, square in enumerate(line):
                        num = square.cleaned_data.get("square", 0)
                        if num == 0:
                            continue
                        elif num > 9 or num < 0 or num in rows[y] or num in columns[x] or num in sections[x//3 + (y//3)*3]:
                            invalid = True
                            for f in square:
                                print(type(f), "/n/n")
                                f.field.widget.attrs['class'] = f.field.widget.attrs.get('class', '') + ' is-invalid'
                        else:
                            rows[y].add(num)
                            columns[x].add(num)
                            sections[x//3 + (y//3)*3].add(num)

                print("form is valid")
                messages.success(request, "Sudoku Solved")
                result = solve_sudoku(SudokuForm)
                context["solved_sudoku"] = result
            else:
                messages.error(request, "Invalid Sudoku")
        elif "quick_enter" in request.POST:
            print("quick entered")
            QuickEnter = QuickEnterForm(request.POST)
            if QuickEnter.is_valid():
                SudokuFormSet = formset_factory(SolveSudokuForm, extra=0)
                SudokuForm = SudokuFormSet(initial=[{"square": value} for value in QuickEnter.cleaned_data["sudoku"]])

    else:
        print("no post")
        
    context["sudoku_forms"] = SudokuForm
    context["quick_enter"] = QuickEnter
    return render(request, "games/sudoku.html", context)


# for form, square in zip(SudokuForm, flattened_solved):
#     form.fields['square'].initial = square