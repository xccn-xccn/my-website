from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms import formset_factory
from .forms import SolveSudokuForm, QuickEnterForm
from .utility import solve_sudoku


def home(request):
    context = {

    }
    return render(request, "games/home.html", context)


def sudoku(request):  # TODO make input red but new same, make copy quick enter, make generator, heighlight errors
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
            if SudokuForm.is_valid():
                messages.success(request, "Sudoku Solved")
                context["solved_sudoku"] = solve_sudoku(SudokuForm)
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