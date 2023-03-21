from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms import formset_factory
from .forms import SolveSudokuForm, QuickEnterForm
from .non_web.sudoku_solver import sudoku_solver

def home(request):
    context = {

    }
    return render(request, "games/home.html", context)


def sudoku(request): #TODO fix current error, create Quick enter, make input red but new same, make copy quick enter, make generator
    SudokuFormSet = formset_factory(SolveSudokuForm, extra=81)
    context = {
        "quick_enter_form" : QuickEnterForm()
    }
    context["solved"] = "NO"
    if request.method == "POST":
        # data = {
        #     'form-TOTAL_FORMS': '81',
        #     'form-INITIAL_FORMS': '0',
        #     }
        context["solved"] = "kinda"
        SudokuForm = SudokuFormSet(request.POST)
        print (SudokuForm.non_form_errors())
        print(SudokuForm.is_valid())
        if SudokuForm.is_valid():
            
            context["solved"] = "yes"
            messages.success(request, "yay")
            grid = []
            count = -1
            for square in [x.cleaned_data.get("square", 0) for x in SudokuForm]:
                count = (count + 1) % 9
                if count == 0:
                    grid.append([])
                grid[-1].append(int(square))
            solved_sudoku = sudoku_solver(grid)
            print(solved_sudoku)
            print([x for row in solved_sudoku for x in row])
            flattened_solved = [str(x) for row in solved_sudoku for x in row]
            context["solved_sudoku"] = "".join(flattened_solved)
            context["solved"] = "YES"
            for form, square in zip(SudokuForm, flattened_solved):
                form.fields['square'].initial = square
            print([x.cleaned_data for x in SudokuForm])
            # return render("sudoku", {"solved_sudoku": solved_sudoku})
        

    else:
         SudokuForm = SudokuFormSet()
    context["sudoku_forms"] = SudokuForm
    return render(request, "games/sudoku.html", context)