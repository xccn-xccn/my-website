from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms import formset_factory
from .forms import SolveSudokuForm
from .non_web.sudoku_solver import sudoku_solver

def home(request):
    context = {

    }
    return render(request, "games/home.html", context)


def sudoku(request):
    SudokuFormSet = formset_factory(SolveSudokuForm, extra=81)
    context = {

    }
    context["solved"] = "NO"
    if request.method == "POST":
        context["solved"] = "kinda"
        SudokuForm = SudokuFormSet(request.POST)
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
            context["solved_sudoku"] = solved_sudoku
            context["solved"] = "YES"
            # return render("sudoku", {"solved_sudoku": solved_sudoku})
    # else:
    #     SudokuForm = SudokuFormSet()
    context["forms"] = SudokuFormSet()
    return render(request, "games/sudoku.html", context)